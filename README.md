# MME-CoT 🔥🕵️: Benchmarking Chain-of-Thought in Large Multimodal Models for Reasoning Quality, Robustness, and Efficiency

![Multimodal CoT](https://img.shields.io/badge/Task-Multimodal_CoT-red) 
![Visual Reasoning](https://img.shields.io/badge/Task-Visual_Reasoning-red) 
![MME-CoT](https://img.shields.io/badge/Dataset-MME--CoT-blue) 

![OpenAI o1](https://img.shields.io/badge/Model-OpenAI_o1-green)
![Kimi k1.5](https://img.shields.io/badge/Model-Kimi--k1.5-green)
![GPT-4o](https://img.shields.io/badge/Model-GPT--4o-green) 

Official repository for "[MME-CoT: Benchmarking Chain-of-Thought in Large Multimodal Models\\for Reasoning Quality, Robustness, and Efficiency]()".

🌟 For more details, please refer to the project page with dataset exploration and visualization tools.

[[🍓Project Page](https://mmecot.github.io/)] [[📖 Paper]()] [[📊 Huggingface Dataset](https://huggingface.co/datasets/CaraJ/MME-CoT)] [[🏆 Leaderboard](https://mmecot.github.io/#leaderboard)] [[👁️ Visualization](https://huggingface.co/datasets/CaraJ/MME-CoT/viewer)]


## 💥 News
- **[2025.02.14]** 🌟 We are very proud to launch MME-CoT, the first-ever comprehensive CoT evaluation benchmark of LMMs in Visual Reasoning! We release the [arxiv paper]() and all data samples in [huggingface dataset](https://huggingface.co/datasets/CaraJ/MME-CoT).

## 📌 ToDo

- Coming soon:  Evaluation Script

## 👀 About MME-CoT

Answering questions with Chain-of-Thought (CoT) has significantly enhanced the reasoning capabilities of Large Language Models (LLMs), yet its impact on Large Multimodal Models (LMMs) still lacks a systematic assessment and in-depth investigation.

In this paper, we introduce **MME-CoT**, a specialized benchmark evaluating the CoT reasoning performance of LMMs, **spanning six domains**: math, science, OCR, logic, space-time, and general scenes. As the first comprehensive study in this area, we propose a **thorough evaluation suite** incorporating **three novel metrics** that assess the reasoning quality, robustness, and efficiency at a fine-grained level.

<p align="center">
    <img src="figs/teaser.jpg" width="90%"> <br>
</p>

Leveraging curated high-quality data and a unique evaluation strategy, we conduct an in-depth analysis of state-of-the-art LMMs, uncovering **several key insights**: **(1) Models with reflection mechanism demonstrate a superior CoT quality**, with Kimi k1.5 outperforming GPT-4o and demonstrating the highest quality results; **(2) CoT prompting often degrades LMM performance on perception-heavy tasks**, suggesting a potentially harmful overthinking behavior; **(3) Although the CoT quality is high, LMMs with reflection exhibit significant inefficiency in both normal response and self-correction phases**. We hope MME-CoT serves as a foundation for advancing multimodal reasoning in LMMs.

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

## 📜 Related Work

Explore our additional research on **Vision-Language Large Models**:


- **[MME-Survey]** [MME-Survey: A Comprehensive Survey on Evaluation of Multimodal LLMs](https://arxiv.org/pdf/2411.15296)
- **[MME]** [MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models](https://arxiv.org/pdf/2306.13394)
- **[MME-RealWorld]** [MME-RealWorld: Could Your Multimodal LLM Challenge High-Resolution Real-World Scenarios that are Difficult for Humans?](https://arxiv.org/pdf/2408.13257)
- **[Awesome-MLLM]** [A Survey on Multimodal Large Language Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models)
- **[MMSearch]** [MMSearch: Benchmarking the potential of large models as multi-modal search engines](https://mmsearch.github.io/)
- **[MathVerse]** [MathVerse: Does Your Multi-modal LLM Truly See the Diagrams in Visual Math Problems?](https://mathverse-cuhk.github.io/)
- **[LLaMA-Adapter]** [LLaMA-Adapter: Efficient Fine-tuning of Language Models with Zero-init Attention](https://github.com/OpenGVLab/LLaMA-Adapter)
- **[LLaMA-Adapter V2]** [LLaMA-Adapter V2: Parameter-Efficient Visual Instruction Model](https://github.com/OpenGVLab/LLaMA-Adapter)
- **[ImageBind-LLM]** [Imagebind-LLM: Multi-modality Instruction Tuning](https://github.com/OpenGVLab/LLaMA-Adapter/tree/main/imagebind_LLM)
- **[SPHINX]** [The Joint Mixing of Weights, Tasks, and Visual Embeddings for Multi-modal LLMs](https://github.com/Alpha-VLLM/LLaMA2-Accessory/tree/main/SPHINX)
- **[SPHINX-X]** [Scaling Data and Parameters for a Family of Multi-modal Large Language Models](https://github.com/Alpha-VLLM/LLaMA2-Accessory/tree/main/SPHINX)
- **[Point-Bind & Point-LLM]** [Multi-modality 3D Understanding, Generation, and Instruction Following](https://github.com/ZiyuGuo99/Point-Bind_Point-LLM)
- **[PerSAM]** [Personalize segment anything model with one shot](https://github.com/ZrrSkywalker/Personalize-SAM)
- **[CoMat]** [CoMat: Aligning Text-to-Image Diffusion Model with Image-to-Text Concept Matching](https://caraj7.github.io/comat/)