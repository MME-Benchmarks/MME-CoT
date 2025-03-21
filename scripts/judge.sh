
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name judge --num_threads 20 \
--prompt_path prompt/prompt_judge.txt \
--data_path extract_json/YOUR_MODEL_NAME_cot.json \
--cache_dir cache/judge/YOUR_MODEL_NAME_cot \
--model gpt-4o-mini