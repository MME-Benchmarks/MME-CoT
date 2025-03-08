export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name recall --num_threads 10 \
--prompt_path prompt/prompt_recall.txt \
--data_path results/xlsx/example_cot.xlsx \
--cache_dir cache/recall \
--model gpt-4o-2024-08-06 