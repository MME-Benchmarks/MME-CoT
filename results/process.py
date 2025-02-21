import os
import pandas as pd

def merge_xlsx_to_json(dir1, dir2, output_dir, save_name):
    # 遍历第一个目录中的文件
    for filename1 in os.listdir(dir1):
        if filename1.endswith('_CoTBench_MINI.xlsx'):
            # 构造第二个目录中的文件名
            filename2 = filename1.replace('_CoTBench_MINI', '_CoTBench_REMAIN')
            
            file_path1 = os.path.join(dir1, filename1)
            file_path2 = os.path.join(dir2, filename2)
            
            # 如果第二个文件存在
            if os.path.exists(file_path2):
                # 读取第一个文件
                df1 = pd.read_excel(file_path1)
                # 在df1中添加source字段
                df1['source'] = 'mini'
                
                # 读取第二个文件
                df2 = pd.read_excel(file_path2)
                # 在df2中添加source字段
                df2['source'] = 'remain'
                
                # 合并两个数据框
                merged_df = pd.concat([df1, df2], ignore_index=True)
                
                # 生成输出文件名
                output_filename = filename1.replace('_CoTBench_MINI.xlsx', f'_{save_name}.json')
                output_path = os.path.join(output_dir, output_filename)
                
                # 保存为JSON格式
                merged_df.to_json(output_path, orient='records', lines=True, force_ascii=False)
                print(f"合并完成，输出文件：{output_path}")
            else:
                print(f"文件 {filename2} 在目录 {dir2} 中不存在，跳过该文件。")


# 示例使用
dir1 = "/Users/cara/0Code/mme-cot/gpt_eval/gpt4api/results/cot_mini"  # 第一个目录路径
dir2 = "/Users/cara/0Code/mme-cot/gpt_eval/gpt4api/results/cot_remain" # 第二个目录路径
output_dir = "/Users/cara/0Code/mme-cot/gpt_eval/gpt4api/results/json"  # 输出目录路径
save_name = 'cot'

merge_xlsx_to_json(dir1, dir2, output_dir, save_name)
