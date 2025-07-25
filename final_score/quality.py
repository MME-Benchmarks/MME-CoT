import json
import os
import argparse
import subprocess
from typing import Dict, Any

def parse_args():
    parser = argparse.ArgumentParser(description='calculate quality metrics')
    parser.add_argument('--cache_dir', type=str, 
                       default='./cache',
                       help='cache directory')
    parser.add_argument('--save_path', type=str,
                       default='./final_results',
                       help='output directory')
    args = parser.parse_args()
    return args

def calculate_f1(precision: float, recall: float) -> float:
    """Calculate F1 score from precision and recall"""
    if precision is None or recall is None or (precision == 0 and recall == 0):
        return None
    return round(2 * precision * recall / (precision + recall), 4)

def process_metrics(precision_data: Dict[str, Any], recall_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process precision and recall data to generate quality metrics"""
    quality_data = {}
    
    for model in precision_data.keys():
        precision_metrics = precision_data[model]
        recall_metrics = recall_data[model]
        
        model_results = {
            "overall_metrics": {
                "precision": precision_metrics["overall_metrics"]["average_precision"],
                "recall": recall_metrics["overall_metrics"]["average_recall"],
                "f1": None  # Will be calculated
            },
            "type_metrics": {
                "logical inference": {
                    "precision": precision_metrics["type_metrics"]["logical inference"]["average_precision"],
                    "recall": recall_metrics["type_metrics"]["logical inference"]["average_recall"],
                    "f1": None  # Will be calculated
                },
                "image caption": {
                    "precision": precision_metrics["type_metrics"]["image description"]["average_precision"],
                    "recall": recall_metrics["type_metrics"]["image caption"]["average_recall"],
                    "f1": None  # Will be calculated
                }
            },
            "category": {},
            "subcategory": {}
        }
        
        # Calculate overall F1
        model_results["overall_metrics"]["f1"] = calculate_f1(
            model_results["overall_metrics"]["precision"],
            model_results["overall_metrics"]["recall"]
        )
        
        # Calculate F1 for each type
        for step_type in ["logical inference", "image caption"]:
            model_results["type_metrics"][step_type]["f1"] = calculate_f1(
                model_results["type_metrics"][step_type]["precision"],
                model_results["type_metrics"][step_type]["recall"]
            )
        
        # Process category metrics
        for category in precision_metrics["category"]:
            if category in recall_metrics["category"]:
                model_results["category"][category] = {
                    "precision": precision_metrics["category"][category],
                    "recall": recall_metrics["category"][category],
                    "f1": calculate_f1(
                        precision_metrics["category"][category],
                        recall_metrics["category"][category]
                    )
                }
        
        # Process subcategory metrics
        for subcategory in precision_metrics["subcategory"]:
            if subcategory in recall_metrics["subcategory"]:
                model_results["subcategory"][subcategory] = {
                    "precision": precision_metrics["subcategory"][subcategory],
                    "recall": recall_metrics["subcategory"][subcategory],
                    "f1": calculate_f1(
                        precision_metrics["subcategory"][subcategory],
                        recall_metrics["subcategory"][subcategory]
                    )
                }
        
        quality_data[model] = model_results
    
    return quality_data

def main():
    args = parse_args()
    
    # Create quality directory
    quality_dir = os.path.join(args.save_path, 'quality')
    os.makedirs(quality_dir, exist_ok=True)
    
    # Execute precision and recall scripts
    print("Calculating precision metrics...")
    subprocess.run(['python', 'final_score/precision.py', 
                   '--cache_dir', os.path.join(args.cache_dir, 'precision'),
                   '--save_path', args.save_path])
    
    print("Calculating recall metrics...")
    subprocess.run(['python', 'final_score/recall.py',
                   '--cache_dir', os.path.join(args.cache_dir, 'recall'),
                   '--save_path', args.save_path])
    
    # Read precision results
    precision_file = os.path.join(args.save_path, 'precision', 'precision_results.json')
    with open(precision_file, 'r', encoding='utf-8') as f:
        precision_data = json.load(f)
    
    # Read recall results
    recall_file = os.path.join(args.save_path, 'recall', 'recall_results.json')
    with open(recall_file, 'r', encoding='utf-8') as f:
        recall_data = json.load(f)
    
    # Process metrics and calculate F1 scores
    quality_data = process_metrics(precision_data, recall_data)
    
    # Save quality results
    output_file = os.path.join(quality_dir, 'quality_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(quality_data, f, indent=4, ensure_ascii=False)
    
    print("Quality metrics calculated and saved successfully.")

if __name__ == '__main__':
    main()