---
layout: default
title: "Horizon Summary: 2026-07-21 (ZH)"
date: 2026-07-21
lang: zh
---

> 从 5 条内容中筛选出 3 条重要资讯。

---

1. [Kimi-K3 缩小开源与闭源前沿模型差距](#item-1) ⭐️ 7.0/10
2. [2 位 Ternary-Bonsai-27B 在 8GB 显存下 Terminal-Bench 2.0 得分仅 7.9%](#item-2) ⭐️ 7.0/10
3. [Kimi K3 在后量子密码学审计中发现其他顶级大模型遗漏的 5 个真实漏洞](#item-3) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [Kimi-K3 缩小开源与闭源前沿模型差距](https://www.reddit.com/r/LocalLLaMA/comments/1v20g29/kimik3_isnt_quite_better_than_fable_yet_but_its/) ⭐️ 7.0/10

Kimi-K3 的发布将开源前沿模型与闭源模型的差距缩小至约 1.5 个月，模型参数接近 3 万亿，但社区讨论中混杂了对虚构模型的引用，影响了讨论质量。

reddit · r/LocalLLaMA · /u/ImaginaryRea1ity · 7月20日 22:41

**背景**: 混合专家（MoE）是一种架构，模型包含许多专门的子网络（专家），但每个输入 token 仅激活其中一小部分，从而在实现巨大参数规模的同时不会成比例增加计算成本。缩放定律是指模型性能随着参数、数据和计算量的增加而可预测地提升这一经验性观察。Artificial Analysis 是一个独立的基准测试平台，从质量、速度、延迟和成本等维度比较 AI 模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.kimi.com/blog/kimi-k3">Kimi K 3 Tech Blog: Open Frontier Intelligence</a></li>
<li><a href="https://automatio.ai/models/kimi-k3">Kimi K 3 : 2.8T MoE AI with 1M Context & Native Vision</a></li>
<li><a href="https://artificialanalysis.ai/">AI Model & API Providers Analysis | Artificial Analysis</a></li>

</ul>
</details>

**社区讨论**: Reddit 帖子引发了混合反应，一些用户对开源模型如此迅速地追赶闭源前沿模型感到印象深刻，而另一些人则指出 Kimi-K3 仍落后数月且无法在消费级硬件上运行。多条评论提到了并不存在的虚构模型如 'Fable' 和 'Gemini 3 Pro'，这混淆了讨论并削弱了其技术可信度。用户还开玩笑说要在 'AI Desktop 98'（一个怀旧风格的 Windows 98 主题聊天界面）上运行该模型，突显了模型规模与实际本地部署之间的差距。

**标签**: `#开源大模型`, `#Kimi-K3`, `#缩放定律`, `#本地部署`, `#模型性能对比`

---

<a id="item-2"></a>
## [2 位 Ternary-Bonsai-27B 在 8GB 显存下 Terminal-Bench 2.0 得分仅 7.9%](https://www.reddit.com/r/LocalLLaMA/comments/1v1ya97/i_ran_ternarybonsai27b_2bit_and_bonsai27b_1bit_on/) ⭐️ 7.0/10

作者在 8GB 显存环境下测试了 Ternary-Bonsai-27B（2 位）和 Bonsai-27B（1 位）模型在 Terminal-Bench 2.0 上的表现，发现 2 位模型准确率仅 7.9%，低于同等显存占用的 9B 密集模型，揭示了极低比特量化在精度上的重大代价。

reddit · r/LocalLLaMA · /u/Creative-Regular6799 · 7月20日 21:15

**背景**: Bonsai 是 PrismML 开发的极端量化模型系列，其权重在嵌入层、注意力层、MLP 层和语言模型头上被压缩为 1 位（二进制）或三值（3 值）表示，使超大模型能在极小显存中运行。Terminal-Bench 2.0 是一个具有挑战性的代理编程基准测试，评估 AI 代理在终端任务上的表现，随着前沿模型能力提升而不断提高难度。Bonsai 模型基于 Qwen3.6 架构，被宣传为可在标准笔记本甚至手机上运行 27B 级别的推理能力。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://docs.prismml.com/models/bonsai-27b">Bonsai 27B - Bonsai - docs.prismml.com</a></li>
<li><a href="https://www.tbench.ai/news/announcement-2-0">Introducing Terminal-Bench 2.0 and Harbor</a></li>
<li><a href="https://docs.prismml.com/run/llamacpp">llama.cpp - Bonsai - docs.prismml.com</a></li>

</ul>
</details>

**标签**: `#模型量化`, `#本地大模型`, `#性能基准测试`, `#低比特推理`, `#LLM优化`

---

<a id="item-3"></a>
## [Kimi K3 在后量子密码学审计中发现其他顶级大模型遗漏的 5 个真实漏洞](https://www.reddit.com/r/LocalLLaMA/comments/1v1z4f0/i_gave_kimi_k3_a_shot_at_auditing_my_postquantum/) ⭐️ 7.0/10

作者使用 Kimi K3 对后量子密码学项目进行安全审计，成功发现其他主流大模型遗漏的 5 个真实漏洞，展示了 LLM 在专业密码学审计中的潜力。

reddit · r/LocalLLaMA · /u/DeliciousGorilla · 7月20日 21:48

**背景**: 后量子密码学是指旨在抵御经典计算机和量子计算机攻击的密码算法，NIST 近期已将 ML-KEM 和 ML-DSA 等算法标准化。大语言模型正越来越多地用于代码生成和安全审计，但其在高度专业化的密码学工作中的可靠性仍是一个活跃的评估领域。Kimi K3 由月之暗面开发，是一个拥有 2.8 万亿参数的开源模型，具备原生视觉能力和 100 万 token 上下文窗口，定位于长周期编码和知识工作。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://openlm.ai/kimi-k3/">Kimi K3 - openlm.ai</a></li>
<li><a href="https://en.wikipedia.org/wiki/Post-quantum_cryptography">Post-quantum cryptography - Wikipedia</a></li>
<li><a href="https://csrc.nist.gov/projects/post-quantum-cryptography">Post-Quantum Cryptography | CSRC | CSRC</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论围绕模型在专业安全审计中的能力对比展开，有用户指出 Kimi K3 缺乏护栏可能是其能够发现安全对齐模型所遗漏漏洞的原因之一。部分评论者对缺乏正式基准测试情况下的可复现性和严谨性表示怀疑，而另一些人则赞扬了将大语言模型用作独立密码学审计工具的实践演示。

**标签**: `#大语言模型`, `#后量子密码学`, `#代码审计`, `#Kimi K3`, `#人工智能安全`

---