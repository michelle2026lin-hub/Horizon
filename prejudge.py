#!/usr/bin/env python3
"""
prejudge.py — Melody 自动化系统「预审官」
读取 Horizon 生成的中文日报，调用 Qwen API 按预审官逻辑分析，结果推送飞书。
"""

import os
import sys
import json
import glob
import datetime
import httpx

# ── 配置 ──────────────────────────────────────────────────────────────────────
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
FEISHU_WEBHOOK    = os.environ.get("FEISHU_WEBHOOK", "")
MODEL             = "qwen-plus"
BASE_URL          = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
SUMMARY_DIR       = "data/summaries"
SCRIPT_MAP_PATH   = "data/Melody_Script_Map.md"

# ── Script Map（内嵌精简版，同时支持从文件读取）────────────────────────────────
SCRIPT_MAP_INLINE = """
## 关键映射规则（预审官必读）

### 高优先级子步骤（可被替代/升级）
- 1.12 VL调用：图像识别/标签提取 → 可被视觉语言模型替代
- 2.x whatsapp_auto：WhatsApp自动化 → 可被RPA/Browser-Use替代（红线：随机等待15-30s不可删，日限200条）
- 3.5 Prompt注入：去机器味/话术 → 可被更好的Prompt工程升级
- 3.6 Groq API：LLM调用 → 可被更便宜/更快模型替代
- 4.4 谈判Prompt：6步谈判 → 可被强化学习/更好策略升级
- 13.x wechat_auto：微信自动化 → 可被RPA替代（红线：不得用Hook方案）
- 17.1 素材归集：人工分类 → 可被OCR/视觉AI替代
- 17.2 去标识化：人工PS → 可被Inpainting/AI擦除替代
- 17.3 视频合成：MoneyPrinter Turbo（现役）→ 可被更好视频生成工具替代
- 17.4 文案生成：Claude人设 → 可被更好的中文生成模型升级
- 17.5 多格式输出：手动裁剪 → 可被自动裁剪工具替代
- 17.6 交付：人工发送 → 可被自动化分发替代

### 红线（绝对不碰）
- pHash阈值=8，不得修改
- WhatsApp日限200条，不得突破
- 随机等待15-30s，不得缩短
- RXID命名规则，不得破坏
- 微信不得用Hook/协议注入方案

### 评分加成规则
- 映射到17.x Order+Video模块：+1.0
- 映射到去机器味/WhatsApp筛选/竞对情报：+0.5
- 映射到核心风控步骤：-0.5
- 需>16GB本地GPU且无云端版：-1.0
"""

SYSTEM_PROMPT = f"""你是 Melody 外贸自动化系统的「预审官」（Pre-Judge Agent）。

Melody 是一个外贸 B2B 商人（五金建材：铰链/滑轨），同时运营短视频副业和翡翠出海副业。
她的核心痛点：WhatsApp客户管理自动化、视频内容生产（Order+Video模块）、竞对情报收集。

你会收到 Horizon AI 抓取并总结的科技资讯日报（中文）。
你的任务是：从日报中识别对 Melody 业务有价值的 AI 工具/技术，生成《候选工具建议书》。

## Melody 的业务映射规则（Script Map精简版）
{SCRIPT_MAP_INLINE}

## 你的输出规则

1. **先扫描整份日报**，找出所有对 Melody 有潜在价值的工具/技术（可能0个，也可能多个）。
2. **对每个候选工具**，生成如下格式的建议书：

---
### 🔍 工具: [工具名]
**大白话结论**: [一句话，这工具对Melody有没有用，为什么]
- **来源**: [日报中的来源]
- **一句话描述**: [工具做什么]
- **映射子步骤**: [精确到原子ID，如 17.3 / 2.x / 13.x]
- **替换对象**: [当前现役实现名，没有则填"无（新增能力）"]
- **预期收益**: [成本/精度/速度/新能力，简短]
- **风险点**: [封号风险/需付费/精度未知/兼容性等]
- **Horizon评分**: X.X（基础分X.X + 加成说明）
- **建议**: [通过测试] / [暂观] / [淘汰]

3. 如果日报中**没有**对 Melody 有价值的工具，直接回复：
`📭 今日日报无匹配工具，Melody 可跳过。`

4. **不要输出DB_INSERT块**（那是手动操作时用的）。
5. **全程中文**，简洁，不废话。
6. **最多输出5个候选工具**，按评分从高到低排序。
"""


def find_latest_summary() -> str | None:
    """找到今天或最近的中文摘要文件"""
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 优先找今天的zh文件
    patterns = [
        f"{SUMMARY_DIR}/horizon-{today}-zh.md",
        f"{SUMMARY_DIR}/horizon-{today}-en.md",   # 退回英文
    ]
    for p in patterns:
        if os.path.exists(p):
            return p

    # 找最新的任意摘要
    all_files = sorted(glob.glob(f"{SUMMARY_DIR}/horizon-*.md"), reverse=True)
    return all_files[0] if all_files else None


def read_script_map() -> str:
    """读取Script Map文件，失败则用内嵌版本"""
    if os.path.exists(SCRIPT_MAP_PATH):
        with open(SCRIPT_MAP_PATH, encoding="utf-8") as f:
            content = f.read()
        # 只取关键部分（节省token）：模块16/17 + 全局常量
        lines = content.split("\n")
        key_sections = []
        capture = False
        for line in lines:
            if any(x in line for x in ["## 全局常量", "## 16.", "## 17.", "## AI 筛选宪法"]):
                capture = True
            if capture:
                key_sections.append(line)
        return "\n".join(key_sections) if key_sections else SCRIPT_MAP_INLINE
    return SCRIPT_MAP_INLINE


def call_qwen(summary_text: str) -> str:
    """调用 Qwen API 进行预审分析"""
    if not DASHSCOPE_API_KEY:
        return "❌ 错误：DASHSCOPE_API_KEY 未设置"

    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"以下是今日 Horizon 科技资讯日报，请进行预审分析：\n\n{summary_text}"},
        ],
        "temperature": 0.3,
        "max_tokens": 3000,
    }

    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(BASE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"❌ API错误 {e.response.status_code}: {e.response.text[:300]}"
    except Exception as e:
        return f"❌ 请求失败: {e}"


def send_to_feishu(content: str, summary_file: str) -> bool:
    """推送预审结果到飞书"""
    if not FEISHU_WEBHOOK:
        print("❌ FEISHU_WEBHOOK 未设置，跳过推送")
        return False

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    title    = f"🔍 Horizon 预审官日报 {date_str}"

    # 截断过长内容（飞书单条限制约4000字）
    if len(content) > 3800:
        content = content[:3800] + "\n\n...（内容过长，已截断）"

    payload = {
        "msg_type": "interactive",
        "card": {
            "schema": "2.0",
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "green",
            },
            "body": {
                "elements": [
                    {
                        "tag": "markdown",
                        "content": f"**来源文件**: `{os.path.basename(summary_file)}`\n\n{content}",
                    }
                ]
            },
        },
    }

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(FEISHU_WEBHOOK, json=payload)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print(f"✅ 预审结果已推送飞书")
                return True
            else:
                print(f"⚠️ 飞书返回异常: {result}")
                return False
    except Exception as e:
        print(f"❌ 飞书推送失败: {e}")
        return False


def main():
    print("🔍 Horizon 预审官启动...")

    # 1. 找摘要文件
    summary_file = find_latest_summary()
    if not summary_file:
        print("❌ 未找到任何摘要文件，退出")
        sys.exit(1)
    print(f"📄 读取摘要: {summary_file}")

    with open(summary_file, encoding="utf-8") as f:
        summary_text = f.read()

    if len(summary_text.strip()) < 100:
        print("⚠️ 摘要内容过短，可能是空日报，跳过预审")
        sys.exit(0)

    # 2. 调用 Qwen 预审
    print(f"🤖 调用 {MODEL} 进行预审分析...")
    result = call_qwen(summary_text)
    print("─" * 60)
    print(result)
    print("─" * 60)

    # 3. 推送飞书
    send_to_feishu(result, summary_file)

    print("✅ 预审官完成")


if __name__ == "__main__":
    main()
