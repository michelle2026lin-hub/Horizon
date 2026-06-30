---
layout: default
title: "Horizon Summary: 2026-06-30 (ZH)"
date: 2026-06-30
lang: zh
---

> 从 4 条内容中筛选出 3 条重要资讯。

---

1. [盘古 2.0-Flash：基于华为昇腾训练的 920 亿参数混合专家模型](#item-1) ⭐️ 8.0/10
2. [对比人工智能巨头烧钱率与互联网泡沫的教训](#item-2) ⭐️ 7.0/10
3. [英伟达发布 Qwen3.6-27B NVFP4 量化模型](#item-3) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [盘古 2.0-Flash：基于华为昇腾训练的 920 亿参数混合专家模型](https://www.reddit.com/r/LocalLLaMA/comments/1ujjxda/ascendtribeopenpangu20flash_they_havent_uploaded/) ⭐️ 8.0/10

在昇腾算力上训练的新型混合专家大模型盘古 2.0-Flash 曝光，该模型具备 60 亿激活参数、512k 上下文以及融合快慢思考与多专家强化学习的先进后训练技术。

reddit · r/LocalLLaMA · /u/External_Mood4719 · 6月30日 09:01

**背景**: 混合专家是一种模型架构，它在处理每个输入时仅激活总参数的一部分，从而显著降低推理过程中的计算成本。华为昇腾是华为研发的一系列 AI 处理器，旨在为大型模型的训练和部署提供英伟达 GPU 的国产替代方案。此外，大语言模型中的快慢思考是指受认知科学启发的架构，使模型既能生成快速直觉的响应，也能进行深度的逐步推理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://thamizhelango.medium.com/mindspore-zhipu-ai-huawei-ascend-how-china-built-a-frontier-ai-model-without-a-single-nvidia-68403d92cedb">MindSpore, Zhipu AI & Huawei Ascend : How China Built... | Medium</a></li>
<li><a href="https://grokipedia.com/page/On-policy_distillation">On-policy distillation</a></li>
<li><a href="https://arxiv.org/abs/2212.05206">[2212.05206] Thinking Fast and Slow in Large Language Models Fast, slow, and metacognitive thinking in AI - Nature Fateyetian/Fast-and-Slow-Thinking - GitHub What Happened in LLMs Layers when Trained for Fast vs. Slow ... Thinking—Fast, Slow, and Artificial: How AI is Reshaping ... Fast, Slow, and Tool-augmented Thinking for LLMs: A Review</a></li>

</ul>
</details>

**标签**: `#大语言模型`, `#混合专家模型`, `#昇腾算力`, `#推理模型`, `#模型发布`

---

<a id="item-2"></a>
## [对比人工智能巨头烧钱率与互联网泡沫的教训](https://www.reddit.com/r/LocalLLaMA/comments/1ujgw8a/why_dario_is_on_fire_lesson_from_dotcom_bubble/) ⭐️ 7.0/10

作者将当前人工智能大模型公司的烧钱与收租模式与互联网泡沫进行对比，指出大语言模型可能面临技术瓶颈，从而质疑其商业护城河与长期可行性。

reddit · r/LocalLLaMA · /u/FormerIYI · 6月30日 06:05

**背景**: 互联网泡沫是 20 世纪 90 年代末至 21 世纪初由互联网公司快速增长引发的历史性经济泡沫，其中许多公司因未能实现盈利而破产。Dario Amodei 是 Anthropic 的首席执行官，这是一家著名的人工智能安全公司，正在开发 Claude 等大语言模型，这需要大量的资本投资于训练和基础设施。关于人工智能护城河的争论集中在专有模型是否能够对日益强大的开源替代品保持可持续的优势。

**标签**: `#人工智能`, `#大语言模型`, `#行业分析`, `#互联网泡沫`, `#商业模式`

---

<a id="item-3"></a>
## [英伟达发布 Qwen3.6-27B NVFP4 量化模型](https://www.reddit.com/r/LocalLLaMA/comments/1ujlltn/nvidiaqwen3627bnvfp4_just_dropped/) ⭐️ 7.0/10

英伟达发布了 Qwen3.6-27B 模型的 NVFP4 量化版本，为本地大模型推理提供了更高效的低精度部署方案。

reddit · r/LocalLLaMA · /u/vanbukin · 6月30日 10:39

**背景**: NVFP4 是伴随英伟达 Blackwell GPU 架构推出的一种创新的 4 位浮点格式。与对整个张量进行缩放的标准量化方法不同，NVFP4 等微缩放格式将元素分组到小块中以共享公共缩放因子。这种方法在保持实际工作负载所需精度的同时，实现了极佳的推理延迟和吞吐量。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/">Introducing NVFP4 for Efficient and Accurate Low-Precision ...</a></li>
<li><a href="https://developer.nvidia.com/blog/nvfp4-trains-with-precision-of-16-bit-and-speed-and-efficiency-of-4-bit/">NVFP4 Trains with Precision of 16-Bit and Speed and ...</a></li>

</ul>
</details>

**标签**: `#大语言模型`, `#模型量化`, `#英伟达`, `#本地部署`, `#推理优化`

---