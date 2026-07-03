---
layout: default
title: "Horizon Summary: 2026-07-03 (ZH)"
date: 2026-07-03
lang: zh
---

> 从 6 条内容中筛选出 4 条重要资讯。

---

1. [DeepSeek V4 Flash 在双 RTX PRO 6000 上编码速度超越 Sonnet 和 Opus](#item-1) ⭐️ 7.0/10
2. [修复 MTP bug 后，GLM-5.2 NVFP4 在 4 块 DGX Spark 上实现 128K 上下文约 24 tok/s](#item-2) ⭐️ 7.0/10
3. [DeepSeek 发布 DSpark 推理框架，声称速度大幅超越 MTP](#item-3) ⭐️ 7.0/10
4. [Toolport：无上下文消耗地同时使用多个 MCP 服务器](#item-4) ⭐️ 6.0/10

---

<a id="item-1"></a>
## [DeepSeek V4 Flash 在双 RTX PRO 6000 上编码速度超越 Sonnet 和 Opus](https://www.reddit.com/r/LocalLLaMA/comments/1um84bd/followup_deepseek_v4_flash_on_2x_rtx_pro_6000/) ⭐️ 7.0/10

DeepSeek V4 Flash 在双 RTX PRO 6000 上运行编码任务的速度比 Sonnet 和 Opus 快约 3 倍，质量接近 Sonnet 水平

reddit · r/LocalLLaMA · /u/xquarx · 7月3日 07:55

**背景**: DeepSeek V4 Flash 是 DeepSeek 于 2026 年 4 月发布的混合专家（MoE）大语言模型，总参数为 2840 亿，每次前向传播仅激活 130 亿参数，支持高达 100 万 token 的上下文长度。vLLM 是一个开源的高吞吐量推理引擎，最初由加州大学伯克利分校开发，以其 PagedAttention 内存管理技术著称，能够高效服务大型模型。RTX PRO 6000 是 NVIDIA 的专业级工作站 GPU，双卡并行可提供足够的显存和算力来本地运行超大型 MoE 模型。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash">deepseek-ai/DeepSeek-V4-Flash · Hugging Face</a></li>
<li><a href="https://vllm.ai/">vLLM — Fast, Memory-Efficient LLM Inference & Serving</a></li>
<li><a href="https://en.wikipedia.org/wiki/VLLM">vLLM - Wikipedia</a></li>

</ul>
</details>

**社区讨论**: Reddit 社区反响积极，赞赏其严谨的方法论以及完整的数据表和图表。许多用户强调了本地模型以显著更低的延迟达到接近 API 模型质量的重大意义，同时也有人指出工具链差异（OpenCode 与 Claude Code）可能是性能差距的部分原因。总体而言，讨论进一步增强了社区对本地大模型在实际编码工作流中可用性的热情。

**标签**: `#本地大模型`, `#性能基准测试`, `#DeepSeek`, `#编码助手`, `#硬件优化`

---

<a id="item-2"></a>
## [修复 MTP bug 后，GLM-5.2 NVFP4 在 4 块 DGX Spark 上实现 128K 上下文约 24 tok/s](https://www.reddit.com/r/LocalLLaMA/comments/1um6pea/followup_glm52_nvfp4_on_four_dgx_sparks_the_mtp/) ⭐️ 7.0/10

作者在 4 块 DGX Spark 上成功修复了 GLM-5.2 NVFP4 模型的 MTP 接受率 bug，实现了 128K 上下文下约 24 tok/s 的推理速度，解决了之前速度与上下文长度不可兼得的问题。

reddit · r/LocalLLaMA · /u/llamaCTO · 7月3日 06:33

**标签**: `#本地LLM部署`, `#推理优化`, `#DGX Spark`, `#GLM-5.2`, `#长上下文推理`

---

<a id="item-3"></a>
## [DeepSeek 发布 DSpark 推理框架，声称速度大幅超越 MTP](https://www.reddit.com/r/LocalLLaMA/comments/1um9j5q/deepseek_drops_another_huge_breakthrough_dspark/) ⭐️ 7.0/10

DeepSeek 发布 DSpark 推理加速技术，声称性能显著超越 MTP 方案，引发社区对大模型推理优化的热烈讨论。

reddit · r/LocalLLaMA · /u/BringTea_666 · 7月3日 09:19

**背景**: 推测解码是一种推理优化技术，由较小的

**标签**: `#大模型推理优化`, `#DeepSeek`, `#推理加速技术`, `#本地化部署`, `#模型架构创新`

---

<a id="item-4"></a>
## [Toolport：无上下文消耗地同时使用多个 MCP 服务器](https://www.reddit.com/r/LocalLLaMA/comments/1um4pig/toolport_use_as_many_mcp_servers_as_you_want/) ⭐️ 6.0/10

Toolport 是一个允许用户同时使用多个 MCP 服务器而无需承担额外上下文消耗的工具，同时提供安全特性和跨客户端配置导入功能。

reddit · r/LocalLLaMA · /u/kydude · 7月3日 04:47

**背景**: 模型上下文协议（MCP）是 Anthropic 于 2024 年底推出的一项开放标准，允许 AI 应用通过统一接口连接外部数据源和工具。然而，每个 MCP 服务器的工具描述都会被注入 LLM 的上下文窗口，因此添加多个服务器会迅速消耗可用 token。安全研究人员还发现了 MCP 特有的攻击向量，例如工具投毒——恶意工具响应中包含隐藏的提示注入——以及 agentjacking，攻击者通过精心构造的 MCP 交互劫持 AI 编码代理。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.anthropic.com/news/model-context-protocol">Introducing the Model Context Protocol \ Anthropic</a></li>
<li><a href="https://owasp.org/www-community/attacks/MCP_Tool_Poisoning">MCP Tool Poisoning - OWASP Foundation</a></li>
<li><a href="https://www.propelex.com/blog/every-step-was-authorized-the-mcp-trust-flaw-behind-agentjacking/">Agentjacking : The MCP Trust Flaw in AI Coding Agents | Propelex</a></li>

</ul>
</details>

**标签**: `#MCP协议`, `#AI代理工具`, `#上下文管理`, `#开发者工具`, `#本地大模型`

---