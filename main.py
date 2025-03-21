import json
import os
import argparse
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Union

import openai
from tqdm import tqdm
import numpy as np


from dataset import get_dataset_by_path
from file_utils import (
    query_gpt,
    save_output
)

parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, required=True, help="Path to the dataset class.")
parser.add_argument("--num_threads", type=int, default=8, help="Number of threads.")
parser.add_argument("--prompt_path", help="Path to the prompt file.")
parser.add_argument("--data_path", help="Path to the query input file.")
parser.add_argument("--model", type=str, default='gpt-4o-2024-08-06')
parser.add_argument("--max_tokens", type=int, default=4096)
parser.add_argument("--cache_dir", type=str, default='cache')

args = parser.parse_args()

def task(inputs: Dict[str, Union[str, Dict[str, Union[str, int]]]]) -> Dict[str, Union[Dict[str, int], List[str]]]:
    global dataset_name
    # if answer is already given, then just return
    if inputs['pre_answer']:
        result = inputs
        result["valid_outputs"] = inputs["pre_answer"]
    else: # use gpt to get answer
        try:
            gpt_output, index = query_gpt(inputs, args)

            result = {
                "valid_outputs": gpt_output.choices[0].message.content,
                "index": index,
            }

            if 'valid_outputs' in inputs:
                del inputs['valid_outputs']

            result.update(inputs)
            del result['query_input']
        except Exception as e:
            result = {"error_message": str(e)}
            print(result)
            return {}

    cache = True

    if cache:
        json.dump(result, open(f'./{args.cache_dir}/{result["index"]}.json', 'w'), indent=4)
    return result


if __name__ == "__main__":

    openai.api_key = os.environ.get("OPENAI_API_KEY", "")

    dataset_args = {
        'prompt_path': getattr(args, "prompt_path", None),
        'data_path': getattr(args, "data_path", None),
        'cache_dir': getattr(args, "cache_dir", None),
        'image_folder': getattr(args, "image_folder", None),
    }

    os.makedirs(args.cache_dir, exist_ok=True)

    dataset = get_dataset_by_path(args.name, dataset_args)
    dataset_name = args.name

    results = []
    query_inputs = []
    start_time = time.time()

    if args.num_threads == 0:
        progress_bar = tqdm(total=len(dataset), unit="task")
        for n, d in enumerate(dataset):
            query_inputs.append(d["query_input"])
            results.append(task(d))
            progress_bar.update(1)
        progress_bar.close()
    else:
        progress_bar = tqdm(total=len(dataset))

        def update_progress(_):
            progress_bar.update(1)

        # Submit the tasks to the thread pool
        progress_bar = tqdm(total=len(dataset), unit="task")
        batch_size = args.num_threads
        for i in range(0, len(dataset), batch_size):
            # Create a thread pool with the specified number of threads
            with ThreadPoolExecutor(max_workers=args.num_threads) as executor:
                current_batch = dataset[i: i + batch_size]
                futures = [executor.submit(task, d) for d in current_batch]
                # Retrieve the results as they become available
                for future, num in zip(futures, dataset):
                    results.append(future.result())
                    progress_bar.update(1)
        progress_bar.close()

    duration = time.time() - start_time


    print(f"Total time: {duration:.2f}s")
