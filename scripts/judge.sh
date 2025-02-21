
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name judge --num_threads 10 \
--prompt_path prompt/prompt_judge.txt \
--data_path results/json/example_cot.json \
--cache_dir cache/judge \
--model gpt-4o-mini