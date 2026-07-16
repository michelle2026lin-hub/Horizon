---
layout: default
title: "Horizon Summary: 2026-07-16 (ZH)"
date: 2026-07-16
lang: zh
---

> 从 6 条内容中筛选出 2 条重要资讯。

---

1. [英伟达 CMP 170HX 挖矿卡或可通过漏洞解锁为完整 A100 80GB GPU](#item-1) ⭐️ 8.0/10
2. [Qwen3.5 122B-A10B 在 ROCm FP4 量化下实现显著速度与体积优化](#item-2) ⭐️ 6.0/10

---

<a id="item-1"></a>
## [英伟达 CMP 170HX 挖矿卡或可通过漏洞解锁为完整 A100 80GB GPU](https://www.reddit.com/r/LocalLLaMA/comments/1uxqccx/psa_nvidias_cmp_170hx_full_compute_and_memory80gb/) ⭐️ 8.0/10

研究人员发现可通过漏洞将 Nvidia CMP 170HX 挖矿卡解锁为完整的 A100 GPU，恢复其全部计算能力和 80GB 内存。

reddit · r/LocalLLaMA · /u/invisibleman42 · 7月16日 02:40

**背景**: 英伟达 CMP 170HX 是在加密货币热潮期间发布的挖矿专用卡，基于与 A100 相同的硅片，但其计算单元和显存被人为限制，以防止用于游戏和通用 GPU 计算。英伟达 GPU 内置了名为 Falcon 的类 RISC 微控制器，负责处理安全固件任务、初始化和电源管理。研究人员一直在研究这些 Falcon 处理器的安全架构，从而发现了一个栈保护绕过漏洞，有可能重新启用被禁用的硬件功能。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://nvidia.github.io/open-gpu-doc/Falcon-Security/Falcon-Security.html">NVIDIA Falcon Security</a></li>
<li><a href="https://docs.kernel.org/gpu/nova/core/falcon.html">Falcon (FAst Logic Controller) — The Linux Kernel documentation</a></li>

</ul>
</details>

**社区讨论**: 社区对以极低成本获得 A100 80GB 性能的潜力感到非常兴奋，许多用户分享了价格数据并猜测卖家会多快调整价格。围绕使用此类漏洞的法律和道德影响也存在大量讨论，同时还有关于显存解锁是否最终能够实现以及英伟达将如何通过固件补丁关闭该漏洞的技术争论。

**标签**: `#Nvidia`, `#GPU`, `#安全漏洞`, `#AI硬件`, `#加密货币`

---

<a id="item-2"></a>
## [Qwen3.5 122B-A10B 在 ROCm FP4 量化下实现显著速度与体积优化](https://www.reddit.com/r/LocalLLaMA/comments/1uxqgke/qwen35_122ba10b_rocmfp4_imatrix/) ⭐️ 6.0/10

作者分享了 Qwen3.5 122B-A10B 模型在 AMD ROCm 平台上使用 FP4 量化和 iMatrix 技术的推理性能数据，展示了速度提升和模型体积缩减的效果。

reddit · r/LocalLLaMA · /u/RedParaglider · 7月16日 02:45

**背景**: Qwen3.5 122B-A10B 是一个混合专家（MoE）大语言模型，每次推理步骤仅使用部分参数（激活 10B），使其比同等总参数量的稠密模型更高效。FP4 量化将每个权重压缩至 4 位精度，在牺牲一定精度的同时大幅降低内存占用和带宽需求。ROCm 是 AMD 的开源 GPU 计算软件平台，类似于 NVIDIA 的 CUDA；iMatrix 是一种基于重要性的量化技术，旨在通过优先保留更关键的权重来维持模型质量。

**标签**: `#大语言模型`, `#模型量化`, `#AMD ROCm`, `#本地部署`, `#推理优化`

---