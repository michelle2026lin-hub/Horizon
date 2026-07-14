---
layout: default
title: "Horizon Summary: 2026-07-14 (ZH)"
date: 2026-07-14
lang: zh
---

> 从 9 条内容中筛选出 2 条重要资讯。

---

1. [David Tse 经典无线通信教材再受关注](#item-1) ⭐️ 7.0/10
2. [llama.cpp 新增腾讯 Hy3 299B MoE 模型支持并集成 MTP 推测解码](#item-2) ⭐️ 7.0/10

---

<a id="item-1"></a>
## [David Tse 经典无线通信教材再受关注](https://web.stanford.edu/~dntse/wireless_book.html) ⭐️ 7.0/10

斯坦福大学 David Tse 的经典无线通信教材，涵盖 MIMO 等核心理论，社区讨论了其与其他经典教材的对比及实际工程应用。

hackernews · teleforce · 7月14日 02:10 · [社区讨论](https://news.ycombinator.com/item?id=48901454)

**背景**: MIMO（多输入多输出）是一种无线技术，通过在发射端和接收端使用多根天线来提高数据吞吐量和链路可靠性。OFDM（正交频分复用）是一种数字调制方案，将数据分布在多个紧密间隔的载波频率上，广泛应用于 Wi-Fi、4G LTE 和 5G。David Tse 与 Pramod Viswanath 合著的这本教材自 2005 年出版以来，一直是研究生无线通信课程的标准参考书。

**社区讨论**: 评论者称赞该书是无线通信领域的经典之作之一，但指出与对 MIMO 的深入探讨相比，其对 OFDM 的覆盖较为有限。有人推荐 Goldsmith 的《无线通信》作为更均衡的教材，还有人分享了关于 802.11 协议行为的实际工程经验——例如早期 Wi-Fi 实现在干扰下致命地

**标签**: `#无线通信`, `#MIMO`, `#OFDM`, `#经典教材`, `#信号处理`

---

<a id="item-2"></a>
## [llama.cpp 新增腾讯 Hy3 299B MoE 模型支持并集成 MTP 推测解码](https://www.reddit.com/r/LocalLLaMA/comments/1uvwbb2/model_add_hy3_hy_v3_support_with_mtp_speculative/) ⭐️ 7.0/10

llama.cpp 新增对腾讯 Hy3（299B MoE）模型的支持，并集成 MTP 推测解码以提升推理速度。

reddit · r/LocalLLaMA · /u/pmttyji · 7月14日 02:46

**背景**: 混合专家模型（MoE）是一种架构，其中每个输入 token 仅激活模型参数的一个子集（专家），从而在可控计算成本下实现超大模型。多 token 预测（MTP）是一种技术，辅助头同时预测多个未来 token，通过提供主模型并行验证的草稿 token 来加速推测解码推理。llama.cpp 是领先的开源推理框架，支持在消费级硬件上本地运行 LLM，支持广泛的模型架构和优化技术。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://github.com/Tencent-Hunyuan/Hy3">GitHub - Tencent-Hunyuan/Hy3: Hy3 (295B A21B), a leading ...</a></li>
<li><a href="https://www.mox.es/2026/05/10/multi-token-prediction-mtp-how-llms-learn-to-look-ahead/">Multi - Token Prediction ( MTP ): How LLMs Learn to Look Ahead...</a></li>
<li><a href="https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md">llama.cpp/docs/speculative.md at master · ggml-org/llama.cpp</a></li>

</ul>
</details>

**社区讨论**: Reddit 讨论反映了社区对本地部署大型 MoE 模型的强烈兴趣，用户指出 Hy3 的 210 亿激活参数对消费级硬件具有实用价值。多位评论者对 MTP 推测解码集成表示热情，认为相比传统草稿模型方法这是显著的效率提升。部分用户对完整 2950 亿参数模型的显存需求和量化支持提出了疑问。

**标签**: `#llama.cpp`, `#模型支持`, `#推测解码`, `#MoE`, `#本地LLM`

---