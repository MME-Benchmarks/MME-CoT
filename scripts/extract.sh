
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name extract --num_threads 10 \
--prompt_path prompt/prompt_extract.txt \
--data_path results/xlsx/example_cot.xlsx \
--cache_dir cache/extract \
--model gpt-4o-mini