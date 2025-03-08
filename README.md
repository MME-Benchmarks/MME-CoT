# MME-CoT 🔥🕵️: Benchmarking Chain-of-Thought in LMMs for Reasoning Quality, Robustness, and Efficiency

![Multimodal CoT](https://img.shields.io/badge/Task-Multimodal_CoT-red) 
![Visual Reasoning](https://img.shields.io/badge/Task-Visual_Reasoning-red) 
![MME-CoT](https://img.shields.io/badge/Dataset-MME--CoT-blue) 

![OpenAI o1](https://img.shields.io/badge/Model-OpenAI_o1-green)
![Kimi k1.5](https://img.shields.io/badge/Model-Kimi--k1.5-green)
![GPT-4o](https://img.shields.io/badge/Model-GPT--4o-green) 

Official repository for "[MME-CoT: Benchmarking Chain-of-Thought in LMMs for Reasoning Quality, Robustness, and Efficiency](https://arxiv.org/pdf/2502.09621)".

🌟 For more details, please refer to the project page with dataset exploration and visualization tools.

[[🍓Project Page](https://mmecot.github.io/)] [[📖 Paper](https://arxiv.org/pdf/2502.09621)] [[📊 Huggingface Dataset](https://huggingface.co/datasets/CaraJ/MME-CoT)] [[🏆 Leaderboard](https://mmecot.github.io/#leaderboard)] [[👁️ Visualization](https://huggingface.co/datasets/CaraJ/MME-CoT/viewer)]

## 💥 News
- **[2025.02.14]** 🌟 We are very proud to launch MME-CoT, the first-ever comprehensive CoT evaluation benchmark of LMMs in Visual Reasoning! We release the [arxiv paper]() and all data samples in [huggingface dataset](https://huggingface.co/datasets/CaraJ/MME-CoT).

## 📌 ToDo

- Coming this week: MME-CoT evaluation with VLMEvalKit

## 👀 About MME-CoT

Answering questions with Chain-of-Thought (CoT) has significantly enhanced the reasoning capabilities of Large Language Models (LLMs), yet its impact on Large Multimodal Models (LMMs) still lacks a systematic assessment and in-depth investigation.

In this paper, we introduce **MME-CoT**, a specialized benchmark evaluating the CoT reasoning performance of LMMs, **spanning six domains**: math, science, OCR, logic, space-time, and general scenes. As the first comprehensive study in this area, we propose a **thorough evaluation suite** incorporating **three novel metrics** that assess the reasoning quality, robustness, and efficiency at a fine-grained level.

<p align="center">
    <img src="figs/teaser.jpg" width="90%"> <br>
</p>

Leveraging curated high-quality data and a unique evaluation strategy, we conduct an in-depth analysis of state-of-the-art LMMs, uncovering **several key insights**: **(1) Models with reflection mechanism demonstrate a superior CoT quality**, with Kimi k1.5 outperforming GPT-4o and demonstrating the highest quality results; **(2) CoT prompting often degrades LMM performance on perception-heavy tasks**, suggesting a potentially harmful overthinking behavior; **(3) Although the CoT quality is high, LMMs with reflection exhibit significant inefficiency in both normal response and self-correction phases**. We hope MME-CoT serves as a foundation for advancing multimodal reasoning in LMMs.

<p align="center">
    <img src="figs/radar.jpg" width="60%"> <br>
</p>

<details>
<summary>💡 Illustration of our CoT Quality Evaluation Strategy</summary>
<p align="center">
    <img src="figs/quality.jpg" width="90%"> <br>
</p>
</details>
<details>
<summary>💪 Illustration of our CoT Robustness Evaluation Strategy</summary>
<p align="center">
    <img src="figs/robustness.jpg" width="70%"> <br>
</p>
</details>
<details>
<summary>⚡️ Illustration of our CoT Efficiency Evaluation Strategy</summary>
<p align="center">
    <img src="figs/effiency.jpg" width="70%"> <br>
</p>
</details>

## 📈 Eval
To calculate the six metrics (precision, recall, efficacy, stability, relevance rate, reflection quality), please follow the following steps:
1. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
2. Format the model answer as the example shown in `results/json`.

     The file should be in a jsonl format, with each answer to a question in one line. All the other information of the question in the dataset should be preserved in the line.

     The suffix `_cot.json` denotes answering with the CoT prompt, and `_dir.json` denotes answering with the direct prompt.
3. Run the evaluation script.

     You can either run the metric one by one. For example, to evaluate recall:
     ```
     bash scripts/recall.sh
     ```
     Or you can run all the metrics for all the models in one directory with:
     ```
     bash batch_scripts/run_all.py --result_dir results/json
     ```
4. Calculate the metrics.

     We cache the evaluation results of all the questions in the cache dir. Here we read the results from the cache dir and calculate the metrics. 

     For example, to calculate recall:
     ```
     python final_score/recall.py --cache_dir cache/recall --save_path final_results
     ```
### Notes
1. The structure of the `scripts` directory:
    ```
    - scripts
    - - recall.sh # evaluate recall
    - - precision.sh # evaluate precision
    - - reflection_quality.sh # evaluate reflection quality
    - - relevance_rate.sh # evaluate relevance rate
    - - extract.sh # Step1 of direct evaluation (for robustness): extract the final answer from the model answer
    - - judge.sh # Step2 of direct evaluation (for robustness): judge the correctness of the extracted answer
    ```

## 🏆 Leaderboard

### Contributing to the Leaderboard

🚨 The [Leaderboard](https://mmecot.github.io/#leaderboard) is continuously being updated, welcoming the contribution of your excellent LMMs!

To contribute your model to the leaderboard, please email the prediction files of four tasks to 📫[jdzcarr7@gmail.com](mailto:jdzcarr7@gmail.com).

### Data Usage

We release the MME-CoT data and evaluation prompts for benchmarking on the leaderboard.

You can download the dataset from the [🤗 Huggingface](https://huggingface.co/datasets/CaraJ/MME-CoT) by the following command (make sure that you have installed [related packages](https://huggingface.co/docs/datasets/quickstart)):

```python
from datasets import load_dataset

dataset = load_dataset("CaraJ/MME-CoT")
```

## :white_check_mark: Citation

If you find **MME-CoT** useful for your research and applications, please kindly cite using this BibTeX:

```latex
@article{jiang2025mme,
  title={MME-CoT: Benchmarking Chain-of-Thought in Large Multimodal Models for Reasoning Quality, Robustness, and Efficiency},
  author={Jiang, Dongzhi and Zhang, Renrui and Guo, Ziyu and Li, Yanwei and Qi, Yu and Chen, Xinyan and Wang, Liuhui and Jin, Jianhan and Guo, Claire and Yan, Shen and others},
  journal={arXiv preprint arXiv:2502.09621},
  year={2025}
}
```

## 📜 Related Work

Explore our additional research on **Vision-Language Large Models**:


- **[MME-Survey]** [MME-Survey: A Comprehensive Survey on Evaluation of Multimodal LLMs](https://arxiv.org/pdf/2411.15296)
- **[MME]** [MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models](https://arxiv.org/pdf/2306.13394)
- **[MMSearch]** [MMSearch: Benchmarking the potential of large models as multi-modal search engines](https://mmsearch.github.io/)
- **[MathVerse]** [MathVerse: Does Your Multi-modal LLM Truly See the Diagrams in Visual Math Problems?](https://mathverse-cuhk.github.io/)
- **[LLaMA-Adapter]** [LLaMA-Adapter: Efficient Fine-tuning of Language Models with Zero-init Attention](https://github.com/OpenGVLab/LLaMA-Adapter)
- **[ImageBind-LLM]** [Imagebind-LLM: Multi-modality Instruction Tuning](https://github.com/OpenGVLab/LLaMA-Adapter/tree/main/imagebind_LLM)
- **[SPHINX]** [The Joint Mixing of Weights, Tasks, and Visual Embeddings for Multi-modal LLMs](https://github.com/Alpha-VLLM/LLaMA2-Accessory/tree/main/SPHINX)
- **[Point-Bind & Point-LLM]** [Multi-modality 3D Understanding, Generation, and Instruction Following](https://github.com/ZiyuGuo99/Point-Bind_Point-LLM)
- **[PerSAM]** [Personalize segment anything model with one shot](https://github.com/ZrrSkywalker/Personalize-SAM)
- **[CoMat]** [CoMat: Aligning Text-to-Image Diffusion Model with Image-to-Text Concept Matching](https://caraj7.github.io/comat/)
