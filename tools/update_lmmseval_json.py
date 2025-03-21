import os
import datasets
import json
import copy
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--lmms_eval_json_path", type=str, required=True, help="Path to the dataset class.")
parser.add_argument("--save_path", type=str, required=True, help="Path to the dataset class.")
args = parser.parse_args()

dataset = datasets.load_dataset('CaraJ/MME-CoT')
dataset = dataset['test']
# conver dataset to dict indexed by idx
dataset_dict = dict()
for data in dataset:
    dataset_dict[data['index']] = data


path_list = list(os.listdir(args.lmms_eval_json_path))

for path in path_list:
    with open(os.path.join(args.lmms_eval_json_path, path), 'r') as f:
        pred_data = json.load(f)
    new_dataset = copy.deepcopy(dataset_dict)
    for i, data in enumerate(pred_data):
        index = data['index']
        try:
            new_dataset[index]['prediction'] = data['prediction'][0]
        except:
            import pdb; pdb.set_trace()

    # Convert new_dataset to a pandas DataFrame
    df = pd.DataFrame.from_dict(new_dataset, orient='index')
    # Save as an .xlsx file
    df.to_excel(os.path.join(args.save_path, path.replace('.json', '.xlsx')), index=False)
    
        