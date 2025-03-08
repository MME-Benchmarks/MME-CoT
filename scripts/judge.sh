
export OPENAI_API_KEY=YOUR_API_KEY
python main.py --name judge --num_threads 10 \
--prompt_path prompt/prompt_judge.txt \
--data_path results/xlsx/example_cot.xlsx \
--cache_dir cache/judge \
--model gpt-4o-mini