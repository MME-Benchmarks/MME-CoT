data_path=$1
cache_dir=$2

echo $data_path 
echo $cache_dir

export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name judge --num_threads 10 \
--prompt_path prompt/prompt_judge.txt \
--data_path results/xlsx/$data_path \
--cache_dir $cache_dir \
--model gpt-4o-mini
