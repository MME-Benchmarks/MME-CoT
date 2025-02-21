data_path=$1
cache_dir=$2

echo $data_path 
echo $cache_dir

export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name relevance_rate --num_threads 5 \
--prompt_path prompt/prompt_relevance_rate.txt \
--data_path results/json/$data_path \
--cache_dir $cache_dir \
--model gpt-4o-2024-08-06 