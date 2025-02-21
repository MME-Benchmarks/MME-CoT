import json
import re
import os
from collections import defaultdict
from json_repair import repair_json
import argparse
from datasets import load_dataset

# load dataset for category information
gt_dataset = load_dataset('CaraJ/MME-CoT')
gt_dataset = gt_dataset['test']
category_dict = {item['index']: dict(category=item['category'], subcategory=item['subcategory']) for item in gt_dataset}

# parse arguments
def parse_args():
    parser = argparse.ArgumentParser(description='calculate recall')
    parser.add_argument('--cache_dir', type=str, 
                       default='./cache/judge',
                       help='cache directory')
    parser.add_argument('--save_path', type=str,
                       default='./final_results',
                       help='output directory')
    args = parser.parse_args()
    return args

def read_category_data(path, name):
    ret_dict = {}
    anno = json.load(open(path, 'r'))
    for data in anno:
        key = f"{name}_{data['source']}_{data['cnt']}"
        ret_dict[key] = dict(
            category=data['category'],
            subcategory=data['subcategory'],
            question=data['question']
        )
    return ret_dict


def process_all_models(cache_dir, save_path):

    # read all data from all models
    data_dict = defaultdict(list)
    for model_name in os.listdir(cache_dir):
        model_dir = os.path.join(cache_dir, model_name)
        for file_name in os.listdir(model_dir):
            file_path = os.path.join(model_dir, file_name)
            with open(file_path, 'r') as f:
                data = json.load(f)
                data_dict[model_name].append(data)

    # calculate final score for each model_name
    ## model_name -> {overall, category, subcategory}
    model_dict = defaultdict(dict)
    for model_name in data_dict:
        true_model_name = '_'.join(model_name.split('_')[:-1])
        answer_type = model_name.split('_')[-1]
        model_dict[true_model_name][answer_type] = {'Reasoning': {}, 'Perception': {}} 
        category_data = {'Reasoning': defaultdict(list), 'Perception': defaultdict(list)}
        subcategory_data = {'Reasoning': defaultdict(list), 'Perception': defaultdict(list)}
        overall_data = {'Reasoning': [], 'Perception': []}


        for data in data_dict[model_name]:
            data['index'] = int(data['index'])
            category = category_dict[data['index']]['category']
            subcategory = category_dict[data['index']]['subcategory']
            try:
                outputs = int(data['valid_outputs'])
                assert outputs in [0, 1]
            except:
                print(f"Error of GPT4o-mini Judgment: {data['valid_outputs']}. Take this question as wrong.")
                outputs = 0

            data['question_type'] = 'Reasoning' if data['question_type'] == 'cot' else 'Perception'
            category_data[data['question_type']][category].append(outputs)
            subcategory_data[data['question_type']][subcategory].append(outputs)
            overall_data[data['question_type']].append(outputs)

        for question_t in ['Reasoning', 'Perception']:
            # category
            for category in category_data[question_t]:
                category_data[question_t][category] = sum(category_data[question_t][category]) / len(category_data[question_t][category]) if len(category_data[question_t][category]) > 0 else 0
            # subcategory
            for category in subcategory_data[question_t]:
                subcategory_data[question_t][category] = sum(subcategory_data[question_t][category]) / len(subcategory_data[question_t][category]) if len(subcategory_data[question_t][category]) > 0 else 0
            # overall
            overall_data[question_t] = sum(overall_data[question_t]) / len(overall_data[question_t]) if len(overall_data[question_t]) > 0 else 0

        model_dict[true_model_name][answer_type]['Reasoning']['category'] = category_data['Reasoning']
        model_dict[true_model_name][answer_type]['Reasoning']['subcategory'] = subcategory_data['Reasoning']
        model_dict[true_model_name][answer_type]['Reasoning']['overall'] = overall_data['Reasoning']

        model_dict[true_model_name][answer_type]['Perception']['category'] = category_data['Perception']
        model_dict[true_model_name][answer_type]['Perception']['subcategory'] = subcategory_data['Perception']
        model_dict[true_model_name][answer_type]['Perception']['overall'] = overall_data['Perception']

    save_dict = {}
    # calculate stability and efficacy
    for true_model_name in model_dict:
        save_dict[true_model_name] = {}
        # stability
        save_dict[true_model_name]['stability'] = {} # Perception question: cot - dir
        # overall
        save_dict[true_model_name]['stability']['overall'] = model_dict[true_model_name]['cot']['Perception']['overall'] - model_dict[true_model_name]['dir']['Perception']['overall']
        # category
        save_dict[true_model_name]['stability']['category'] = {}
        for category in model_dict[true_model_name]['cot']['Perception']['category']: 
            save_dict[true_model_name]['stability']['category'][category] = model_dict[true_model_name]['cot']['Perception']['category'][category] - model_dict[true_model_name]['dir']['Perception']['category'][category]
        # subcategory
        save_dict[true_model_name]['stability']['subcategory'] = {}
        for subcategory in model_dict[true_model_name]['cot']['Perception']['subcategory']:
            save_dict[true_model_name]['stability']['subcategory'][subcategory] = model_dict[true_model_name]['cot']['Perception']['subcategory'][subcategory] - model_dict[true_model_name]['dir']['Perception']['subcategory'][subcategory]

        # efficacy
        save_dict[true_model_name]['efficacy'] = {} # Reasoning question: cot - dir
        # overall
        save_dict[true_model_name]['efficacy']['overall'] = model_dict[true_model_name]['cot']['Reasoning']['overall'] - model_dict[true_model_name]['dir']['Reasoning']['overall']
        # category
        save_dict[true_model_name]['efficacy']['category'] = {}
        for category in model_dict[true_model_name]['cot']['Reasoning']['category']: 
            save_dict[true_model_name]['efficacy']['category'][category] = model_dict[true_model_name]['cot']['Reasoning']['category'][category] - model_dict[true_model_name]['dir']['Reasoning']['category'][category]
        # subcategory
        save_dict[true_model_name]['efficacy']['subcategory'] = {}
        for subcategory in model_dict[true_model_name]['cot']['Reasoning']['subcategory']: 
            save_dict[true_model_name]['efficacy']['subcategory'][subcategory] = model_dict[true_model_name]['cot']['Reasoning']['subcategory'][subcategory] - model_dict[true_model_name]['dir']['Reasoning']['subcategory'][subcategory]

        # Robustness: avg score
        save_dict[true_model_name]['robustness'] = {} 
        # overall
        save_dict[true_model_name]['robustness']['overall'] = (save_dict[true_model_name]['efficacy']['overall'] + save_dict[true_model_name]['stability']['overall'])/2
        # category
        save_dict[true_model_name]['robustness']['category'] = {}
        for category in save_dict[true_model_name]['stability']['category']: 
            save_dict[true_model_name]['robustness']['category'][category] = (save_dict[true_model_name]['efficacy']['category'][category] + save_dict[true_model_name]['stability']['category'][category])/2
        # subcategory
        save_dict[true_model_name]['robustness']['subcategory'] = {}
        for subcategory in save_dict[true_model_name]['stability']['subcategory']: 
            save_dict[true_model_name]['robustness']['subcategory'][subcategory] = (save_dict[true_model_name]['efficacy']['subcategory'][subcategory] + save_dict[true_model_name]['stability']['subcategory'][subcategory])/2
    
    
    save_dir = os.path.join(save_path, 'robustness')
    os.makedirs(save_dir, exist_ok=True)
    json.dump(save_dict, open(os.path.join(save_dir, 'robustness.json'), 'w'), indent=4)

if __name__ == '__main__':
    args = parse_args()
    process_all_models(args.cache_dir, args.save_path)
    print('Done')

