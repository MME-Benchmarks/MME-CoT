import json
import os
import argparse
import subprocess
from typing import Dict, Any

def parse_args():
    parser = argparse.ArgumentParser(description='calculate efficiency metrics')
    parser.add_argument('--cache_dir', type=str, 
                       default='./cache',
                       help='cache directory')
    parser.add_argument('--save_path', type=str,
                       default='./final_results',
                       help='output directory')
    args = parser.parse_args()
    return args

def calculate_efficiency(relevance: float, reflection: float) -> float:
    """Calculate efficiency score from relevance and reflection scores"""
    if relevance is None or reflection is None:
        return None
    return round((relevance + reflection) / 2, 4)

def process_metrics(relevance_data: Dict[str, Any], reflection_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process relevance and reflection data to generate efficiency metrics"""
    efficiency_data = {}
    
    for model in relevance_data.keys():
        relevance_metrics = relevance_data[model]
        reflection_metrics = reflection_data[model]
        
        model_results = {
            "overall_metrics": {
                "relevance": relevance_metrics["overall_metrics"]["average_relevance"],
                "reflection": reflection_metrics["overall_metrics"]["average_score"],
                "efficiency": None  # Will be calculated
            },
            "category": {},
            "subcategory": {}
        }
        
        # Calculate overall efficiency
        model_results["overall_metrics"]["efficiency"] = calculate_efficiency(
            model_results["overall_metrics"]["relevance"],
            model_results["overall_metrics"]["reflection"]
        )
        
        # Process category metrics
        for category in relevance_metrics["category"]:
            if category in reflection_metrics["category"]:
                model_results["category"][category] = {
                    "relevance": relevance_metrics["category"][category],
                    "reflection": reflection_metrics["category"][category],
                    "efficiency": calculate_efficiency(
                        relevance_metrics["category"][category],
                        reflection_metrics["category"][category]
                    )
                }
        
        # Process subcategory metrics
        for subcategory in relevance_metrics["subcategory"]:
            if subcategory in reflection_metrics["subcategory"]:
                model_results["subcategory"][subcategory] = {
                    "relevance": relevance_metrics["subcategory"][subcategory],
                    "reflection": reflection_metrics["subcategory"][subcategory],
                    "efficiency": calculate_efficiency(
                        relevance_metrics["subcategory"][subcategory],
                        reflection_metrics["subcategory"][subcategory]
                    )
                }
        
        efficiency_data[model] = model_results
    
    return efficiency_data

def main():
    args = parse_args()
    
    # Create efficiency directory
    efficiency_dir = os.path.join(args.save_path, 'efficiency')
    os.makedirs(efficiency_dir, exist_ok=True)
    
    # Execute relevance and reflection scripts
    print("Calculating relevance metrics...")
    subprocess.run(['python', 'final_score/relevance_rate.py', 
                   '--cache_dir', os.path.join(args.cache_dir, 'relevance_rate'),
                   '--save_path', args.save_path])
    
    print("Calculating reflection metrics...")
    subprocess.run(['python', 'final_score/reflection_quality.py',
                   '--cache_dir', os.path.join(args.cache_dir, 'reflection_quality'),
                   '--save_path', args.save_path])
    
    # Read relevance results
    relevance_file = os.path.join(args.save_path, 'relevance', 'relevance_results.json')
    with open(relevance_file, 'r', encoding='utf-8') as f:
        relevance_data = json.load(f)
    
    # Read reflection results
    reflection_file = os.path.join(args.save_path, 'reflection', 'reflection_results.json')
    with open(reflection_file, 'r', encoding='utf-8') as f:
        reflection_data = json.load(f)
    
    # Process metrics and calculate efficiency scores
    efficiency_data = process_metrics(relevance_data, reflection_data)
    
    # Save efficiency results
    output_file = os.path.join(efficiency_dir, 'efficiency_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(efficiency_data, f, indent=4, ensure_ascii=False)
    
    print("Efficiency metrics calculated and saved successfully.")

if __name__ == '__main__':
    main()