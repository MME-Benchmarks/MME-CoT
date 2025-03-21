import json
import os
from tqdm import tqdm
import string
from datasets import load_dataset
from direct_eval import extract_answer_from_item
from file_utils import read_results

def make_gt_dict(gt_dataset):
    gt_dict = dict()
    for i, data in enumerate(gt_dataset):
        gt_dict[data['index']] = data

    return gt_dict

# make prompt for recall, precision, relevance, reflection_quality
def make_prompt(name, c, gt_inst, prompt):
    # make ground truth information
    gt_set = []
    if name == 'recall':
        cnt = 0
        for f in sorted(gt_inst['key_annotation_steps']):
            if gt_inst['key_annotation_steps'][f] is None:
                continue
            for k in ['logical_conclusion', 'image_caption']:
                for step in gt_inst['key_annotation_steps'][f][k]:
                    if step.strip() == '':
                        continue
                    gt_set.append(dict(
                        step_index=cnt,
                        content=step.strip()
                    ))
                    cnt += 1
    else:
        gt_conclusion, gt_caption = [], []
        for f in gt_inst['key_annotation_steps']:
            if gt_inst['key_annotation_steps'][f] is None:
                continue
            gt_conclusion.extend(gt_inst['key_annotation_steps'][f]['logical_conclusion'])
            gt_caption.extend(gt_inst['key_annotation_steps'][f]['image_caption'])
        
        gt_caption = gt_inst['reference_caption'] if gt_inst['reference_caption'] != [''] else []
        gt_set = gt_conclusion + gt_caption + gt_caption
        gt_set = [l.strip() for l in gt_set if l.strip() != '']
    # make question
    question = gt_inst['question']
    options = {
            cand: gt_inst[cand]
            for cand in string.ascii_uppercase
            if cand in gt_inst and not gt_inst[cand] != None and gt_inst[cand] != ''
        }
    options_prompt = 'Options:\n'
    for key, item in options.items():
        options_prompt += f'{key}. {item}\n'
    if len(options) != 0:
        question += options_prompt
    # add information
    prompt = prompt.format(
        question=c['question'],
        answer=gt_inst['answer'],
        solution=c['prediction'],
        gt_annotation=json.dumps(gt_set)
    )

    return prompt

# make prompt for extract and judge, for robustness evaluation (direct eval)
def make_dir_prompt(name, c, prompt):
    # make ground truth information
    if name == 'extract':
        prompt = prompt.replace("{", "{{").replace("}", "}}")
        question = c['question'].replace("{", "{{").replace("}", "}}")
        prediction = str(c['prediction']).replace("{", "{{").replace("}", "}}")
        question = question.strip()

        prompt = prompt.format(
            question=question, 
            response=prediction, 
        )
    elif name == 'judge': 
        prompt = prompt.replace("{", "{{").replace("}", "}}")
        question = c['question'].replace("{", "{{").replace("}", "}}")
        prompt = prompt.format(question=question, extract_answer=c['extract_answer'], gt_answer=c['answer'])
        
    return prompt

def get_dataset_by_path(name, dataset_args):
    # load dataset
    gt_dataset = load_dataset('CaraJ/MME-CoT')
    gt_dataset = gt_dataset['test']
    gt_dataset_dict = make_gt_dict(gt_dataset)

    # load all the result and its index
    results = read_results(dataset_args["data_path"]) # read either from xlsx or json
    
    # filter what have already collected in cache
    cached_index = []
    for file in os.listdir(dataset_args['cache_dir']):
        cached_index.append(int(os.path.splitext(file)[0]))
    filtered_results = []
    for c in results:
        if int(c['index']) not in cached_index:
            filtered_results.append(c)
    results = filtered_results
    
    # read the prompt
    with open(dataset_args["prompt_path"], 'r') as f:
        prompt = f.read().strip()
    
    if name in [
        'recall',
        'precision',
        'relevance_rate',
        'reflection_quality'
    ]:
        
        # filter the codes with only cot
        filtered_results = []
        for c in results:
            if c['question_type'] == 'Reasoning':
                filtered_results.append(c)
        results = filtered_results

        # return all uncached data
        return_list = []
        for c in tqdm(results):
            gt_inst = gt_dataset_dict[c['index']]
            c['key_annotation_steps'] = gt_inst['key_annotation_steps']
            c['reference_caption'] = gt_inst['reference_caption']
            # this is for judge task
            c["pre_answer"] = None

            c['query_input'] = [
                {"type": "text", "text": make_prompt(name, c, gt_inst, prompt)}
            ]

            c['index'] = c['index']
            return_list.append(c)

    elif name in ['extract', 'judge']:
        return_list = []
        for c in tqdm(results):
            gt_inst = gt_dataset_dict[c['index']]

            if name == 'extract':
                # try to extract answer from item
                c["pre_answer"] = extract_answer_from_item(c, gt_inst)

                c['query_input'] = [
                    {"type": "text", "text": make_dir_prompt(name, c, prompt)}
                ]
            elif name == 'judge':
                c['extract_answer'] = c['valid_outputs'].strip('')
                # delete query_input
                c = {k: v for k, v in c.items() if k not in ['valid_outputs', 'query_input']}
                # initialize pre answer
                c['pre_answer'] = None 
                # if all 1 char, then directly judge
                if len(c['extract_answer']) == 1 and len(c['answer']) == 1:
                    c['pre_answer'] = '1' if c['extract_answer'] == c['answer'] else '0'
                    c['query_input'] = None
                else:
                    c['query_input'] = [
                        {"type": "text", "text": make_dir_prompt(name, c, prompt)}
                    ]
            c['index'] = c['index']
            c['task'] = 'judge'
            return_list.append(c)
    else:
        raise NotImplementedError
    
    return return_list
    








