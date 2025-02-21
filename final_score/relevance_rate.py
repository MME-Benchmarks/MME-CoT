import json
import re
import os
import argparse
from collections import defaultdict
from json_repair import repair_json
from datasets import load_dataset

# Load dataset for category information
gt_dataset = load_dataset('CaraJ/MME-CoT')
gt_dataset = gt_dataset['test']
category_dict = {item['index']: (item['category'], item['subcategory']) for item in gt_dataset}

def parse_args():
    parser = argparse.ArgumentParser(description='calculate relevance')
    parser.add_argument('--cache_dir', type=str, 
                       default='./cache/relevance_rate',
                       help='cache directory')
    parser.add_argument('--save_path', type=str,
                       default='./final_results',
                       help='output directory')
    args = parser.parse_args()
    return args

def extract_json_string(text):
    """
    Extract and process JSON string from text.
    Returns None if invalid format.
    """
    if not text:
        return None
    text = text.replace('\\', '\\\\')
    start = text.find('[')
    if start == -1:
        return None
    stack = []
    end = -1
    for i in range(start, len(text)):
        if text[i] == '[':
            stack.append(i)
        elif text[i] == ']':
            if stack:
                stack.pop()
                if not stack:
                    end = i
                    if end == 0 or text[end-1] != '\n':
                        return None
                    break
    if end == -1:
        return None
    json_str = text[start:end + 1]
    return repair_json(json_str)

def calculate_relevance(data_list, step_type=None):
    """
    Calculate relevancy score for given data list.
    Returns relevancy score or None if no valid data.
    """
    try:
        relevant_count = 0
        filtered_data = [item for item in data_list if not step_type or item['step_type'] == step_type]
        total = len(filtered_data)
        
        if total == 0:
            return None
            
        for item in filtered_data:
            relevant_count = relevant_count + 1 if item['relevant'] == 'Yes' else relevant_count
            
        relevancy = relevant_count / total if total > 0 else None
        return relevancy
        
    except Exception:
        return None

def analyze_relevance(json_file_path):
    """
    Analyze relevancy metrics for a single json file.
    Returns metrics with type and category information.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Get category info from index
        index = data.get('index')
        category, subcategory = category_dict.get(index, (None, None))
            
        json_str = extract_json_string(data.get('valid_outputs'))
        if not json_str:
            raise ValueError('Missing or invalid valid_outputs field')
            
        steps_data = json.loads(json_str, strict=False)
        if not steps_data:
            raise ValueError('Empty steps_data')
            
        # Calculate metrics by type
        target_types = ['logical inference', 'image caption']
        filtered_data = [item for item in steps_data if item['step_type'] in target_types]
        overall_relevance = calculate_relevance(filtered_data)
        
        type_metrics = {}
        for step_type in target_types:
            rel = calculate_relevance(steps_data, step_type)
            type_metrics[step_type] = {'score': rel}

        # Update file with metrics
        data['relevance'] = {
            'overall': {'score': overall_relevance},
            'by_type': type_metrics
        }
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {
            'success': True,
            'relevance': overall_relevance,
            'type_metrics': type_metrics,
            'category': category,
            'subcategory': subcategory
        }
    except json.JSONDecodeError as e:
        return {'success': False, 'error': f'JSON decode error: {str(e)}'}
    except ValueError as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': f'Unknown error: {str(e)}'}

def process_model_files(model_path):
    """Process all files in model directory and aggregate results"""
    results = {
        'relevance_scores': [],
        'error_files': [],
        'type_metrics': defaultdict(lambda: {'scores': []}),
        'category_metrics': defaultdict(list),
        'subcategory_metrics': defaultdict(list)
    }
    
    for json_file in os.listdir(model_path):
        if not json_file.endswith('.json'):
            continue
            
        file_path = os.path.join(model_path, json_file)
        result = analyze_relevance(file_path)
        
        if result.get('success'):
            if result['relevance'] is not None:
                results['relevance_scores'].append(result['relevance'])
                
            # Collect metrics only when score is not None
            for step_type, metrics in result['type_metrics'].items():
                if metrics['score'] is not None:
                    results['type_metrics'][step_type]['scores'].append(metrics['score'])
                    
            # Collect category metrics only when both category and score exist
            if result['category'] and result['relevance'] is not None:
                results['category_metrics'][result['category']].append(result['relevance'])
            if result['subcategory'] and result['relevance'] is not None:
                results['subcategory_metrics'][result['subcategory']].append(result['relevance'])
        else:
            results['error_files'].append({
                'file': json_file,
                'error': result.get('error', 'Unknown error')
            })
    
    return results

def process_all_models(cache_dir, save_path):
    """Process all models and save aggregated results"""
    model_stats = {}
    results_data = {}
    all_error_files = {}
    
    # Create output directory
    save_dir = os.path.join(save_path, 'relevance')
    os.makedirs(save_dir, exist_ok=True)
    
    for model in os.listdir(cache_dir):
        model_path = os.path.join(cache_dir, model)
        if not os.path.isdir(model_path):
            continue
            
        results = process_model_files(model_path)
        model_stats[model] = results
        
        if results['error_files']:
            all_error_files[model] = results['error_files']
        
        # Calculate model averages with None value filtering
        valid_scores = [score for score in results['relevance_scores'] if score is not None]
        model_results = {
            "overall_metrics": {
                "average_relevance": round(sum(valid_scores)/len(valid_scores), 4) if valid_scores else None
            },
            "type_metrics": {},
            "category": {},
            "subcategory": {}
        }
        
        # Add type metrics with None filtering
        for step_type, metrics in results['type_metrics'].items():
            scores = [score for score in metrics['scores'] if score is not None]
            if scores:
                model_results["type_metrics"][step_type] = {
                    "average_relevance": round(sum(scores)/len(scores), 4)
                }
            else:
                model_results["type_metrics"][step_type] = {
                    "average_relevance": None
                }
                
        # Add category metrics with None filtering
        for cat, values in results['category_metrics'].items():
            valid_values = [v for v in values if v is not None]
            if valid_values:
                model_results["category"][cat] = round(sum(valid_values)/len(valid_values), 4)
            else:
                model_results["category"][cat] = None
            
        # Add subcategory metrics with None filtering
        for subcat, values in results['subcategory_metrics'].items():
            valid_values = [v for v in values if v is not None]
            if valid_values:
                model_results["subcategory"][subcat] = round(sum(valid_values)/len(valid_values), 4)
            else:
                model_results["subcategory"][subcat] = None
        
        results_data[model] = model_results
    
    # Rescale scores to 0-1
    for model_name in results_data:
        results_data[model_name]['overall_metrics']['average_relevance'] = round((results_data[model_name]['overall_metrics']['average_relevance'] - 0.8) * 5, 4)
        for step_type in results_data[model_name]['type_metrics']:
            results_data[model_name]['type_metrics'][step_type]['average_relevance'] = round((results_data[model_name]['type_metrics'][step_type]['average_relevance'] - 0.8) * 5, 4)

    # Save main results
    output_file = os.path.join(save_dir, 'relevance_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=4, ensure_ascii=False)

    # Save error file if exists
    if all_error_files:
        error_file = os.path.join(save_dir, 'relevance_errors.json')
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(all_error_files, f, indent=4, ensure_ascii=False)

    return model_stats

if __name__ == '__main__':
    args = parse_args()
    process_all_models(args.cache_dir, args.save_path)
    print('Done')