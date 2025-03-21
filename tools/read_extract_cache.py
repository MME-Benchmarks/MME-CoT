import os
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--cache_dir", default="cache/extract/example_cot")
parser.add_argument("--save_path", default="extract_json/example_cot.json")

args = parser.parse_args()

parser = argparse.ArgumentParser()
# path = '/data1/zrr/jdz/lm_reason/dir_eval/gpt4api/cache_internvl'

save_list = []
for f in os.listdir(args.cache_dir):
    save_list.append(
        json.load(open(os.path.join(args.cache_dir, f)))
    )

os.makedirs(os.path.dirname(args.save_path), exist_ok=True)
# save as jsonl file
with open(args.save_path, 'w') as f:
    for item in save_list:
        f.write(json.dumps(item) + '\n')
