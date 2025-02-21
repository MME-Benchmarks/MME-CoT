
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name judge --num_threads 10 \
--prompt_path prompt/prompt_judge.txt \
--data_path data/debug_data.json \
--cache_dir cache_debug/judge \
--model gpt-4o-mini