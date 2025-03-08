export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name precision --num_threads 0 \
--prompt_path prompt/prompt_precision.txt \
--data_path results/xlsx/example_cot.xlsx \
--cache_dir cache/precision \
--model gpt-4o-2024-08-06 