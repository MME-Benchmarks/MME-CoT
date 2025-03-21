
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name extract --num_threads 20 \
--prompt_path prompt/prompt_extract.txt \
--data_path results/xlsx/YOUR_MODEL_NAME_cot.xlsx \
--cache_dir cache/extract/YOUR_MODEL_NAME_cot \
--model gpt-4o-mini

# merge all extract cache into one json file
python tools/read_extract_cache.py \
--cache_dir cache/extract/YOUR_MODEL_NAME_cot \
--save_path extract_json/YOUR_MODEL_NAME_cot.json
