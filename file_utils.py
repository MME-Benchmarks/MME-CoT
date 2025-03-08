"""
file utils
"""

import json
import os
import time

import openai
from openai import OpenAI
import pandas as pd


system_messages = "You are an AI assistant that helps people solve their questions."


def query_gpt(inputs, args):
    """
    Query the GPT API with the given inputs.
    Returns:
        Response (dict[str, str]): the response from GPT API.
        Input ID (str): the id that specifics the input.
    """

    messages = [{
        "role": "system",
        "content": system_messages,
    }, {
        "role": "user",
        "content": inputs["query_input"],
    }]

    client=OpenAI(api_key='<KEY>')
    client.api_key = os.environ.get("OPENAI_API_KEY", 'YOUR_API_KEY')
    
    succuss = True
    while succuss:
        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=messages,
                max_tokens=args.max_tokens,
                temperature=0,
                top_p=0.1,
            )
            succuss = False
        except openai.RateLimitError as e:
            time.sleep(60)
        except openai.OpenAIError as e:
            print(f'ERROR: {e}')
            return f"Unsuccessful: {e.message}"
        
    return response, inputs['index']


def save_output(results, dataset_name, file_name='output.json'):
    output_folder = os.path.join('./output', dataset_name)
    os.makedirs(output_folder, exist_ok=True)
    json.dump(results, open(os.path.join(output_folder, file_name), 'w'))

def read_results(data_path):
    if data_path.endswith('.xlsx'):
        results = pd.read_excel(data_path)
    elif data_path.endswith('.json') or data_path.endswith('.jsonl'):
        results = []
        with open(data_path, 'r') as f:
            for line in f:
                results.append(json.loads(line))
    else:
        raise ValueError(f"Unsupported file type: {data_path}")
    return results