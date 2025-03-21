export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name recall --num_threads 20 \
--prompt_path prompt/prompt_recall.txt \
--data_path results/xlsx/YOUR_MODEL_NAME_cot.xlsx \
--cache_dir cache/recall/YOUR_MODEL_NAME \
--model gpt-4o-2024-08-06 