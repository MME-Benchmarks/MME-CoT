export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name reflection_quality --num_threads 10 \
--prompt_path prompt/prompt_reflection_quality.txt \
--data_path results/json/example_cot.json \
--cache_dir cache/reflection_quality \
--model gpt-4o-2024-08-06 