export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name relevance_rate --num_threads 10 \
--prompt_path prompt/prompt_relevancy.txt \
--data_path results/json/example_cot.json \
--cache_dir cache/relevance_rate \
--model gpt-4o-2024-08-06 