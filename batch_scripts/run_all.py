import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--result_dir", default="results/json")
args = parser.parse_args()

result_dir = args.result_dir
for f in os.listdir(result_dir):
    # only evaluate results of cot prompt
    if not f.endswith('_cot.json'):
        continue
    print(f"Evaluating {f}")
    data_path = f
    # recall
    cache_path = f"cache/recall/{f.split('.json')[0]}"
    command = f"bash batch_scripts/recall.sh {data_path} {cache_path}"
    print(f"Evaluating recall: {command}")
    os.system(command)
    # precision
    task = 'precision'
    cache_path = f"cache/{task}/{f.split('.json')[0]}"
    command = f"bash batch_scripts/{task}.sh {data_path} {cache_path}"
    print(f"Evaluating precision: {command}")
    os.system(command)
    # reflection quality
    task = 'reflection_quality'
    cache_path = f"cache/{task}/{f.split('.json')[0]}"
    command = f"bash batch_scripts/{task}.sh {data_path} {cache_path}"
    print(f"Evaluating reflection quality: {command}")
    os.system(command)
    # relevance rate
    task = 'relevance_rate'
    cache_path = f"cache/{task}/{f.split('.json')[0]}"
    command = f"bash batch_scripts/{task}.sh {data_path} {cache_path}"
    print(f"Evaluating relevance rate: {command}")
    os.system(command)
    # robustness: extract and judge
    # need to evaluate both cot prompt and direct prompt
    true_model_name = f.split('_')[0]
    cot_json_name = f
    dir_json_name = f"{true_model_name}_dir.json"

    for eval_f in [cot_json_name, dir_json_name]:
        
        # extract
        task = 'extract'
        cache_path = f"cache/{task}/{eval_f.split('.json')[0]}"
        command = f"bash batch_scripts/{task}.sh {data_path} {cache_path}"
        print(command)
        os.system(command)

        # merge data
        command = f"python tools/read_extract_cache.py --cache_dir {cache_path} --save_path extract_json/{eval_f}"
        os.system(command)

        # judge
        task = 'judge'
        cache_path = f"cache/{task}/{eval_f.split('.json')[0]}"
        command = f"bash batch_scripts/{task}.sh {eval_f} {cache_path}"
        print(command)
        os.system(command)
