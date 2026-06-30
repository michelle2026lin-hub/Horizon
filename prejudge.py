#!/usr/bin/env python3
"""
prejudge.py — Melody 自动化系统「预审官」 v4
读取 Horizon 生成的中文日报，调用 AI 按【完整】Melody_Script_Map.md 逐条核对，结果推送飞书。

v4 新增：多模型自动轮替容灾
  第一层：阿里云百炼模型池（按到期日排序，过期/403自动跳下一个）
  第二层：全部阿里云模型失败后，自动切换到 GLM-4-Flash（永久免费）
  第三层：GLM 也失败，最终切换到 Gemini（永久免费，每日250次）
"""

import os
import sys
import csv
import glob
import datetime
import httpx

# ── 飞书 ──────────────────────────────────────────────────────────────────────
FEISHU_WEBHOOK  = os.environ.get("FEISHU_WEBHOOK", "")
SUMMARY_DIR     = "data/summaries"
SCRIPT_MAP_PATH = "data/Melody_Script_Map.md"
TOOL_DB_PATH    = "data/Video_Tool_DB.csv"

# ── 第一层：阿里云百炼模型池（按到期日从早到晚排序，优先消耗快过期的）─────────────
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

DASHSCOPE_MODEL_POOL = [
    {"model": "qwen3.6-plus-2026-04-02", "expire": "2026-07-02"},
    {"model": "qwen3.6-plus",            "expire": "2026-07-02"},
    {"model": "glm-5.1",                 "expire": "2026-07-14"},
    {"model": "qwen3.6-flash-2026-04-16","expire": "2026-07-17"},
    {"model": "qwen3.6-35b-a3b",         "expire": "2026-07-17"},
    {"model": "qwen3.6-flash",           "expire": "2026-07-17"},
    {"model": "qwen3.6-max-preview",     "expire": "2026-07-20"},
    {"model": "kimi-k2.6",               "expire": "2026-07-21"},
    {"model": "qwen3.5-plus-2026-04-20", "expire": "2026-07-23"},
    {"model": "qwen3.6-27b",             "expire": "2026-07-23"},
    {"model": "deepseek-v4-flash",       "expire": "2026-07-24"},
    {"model": "deepseek-v4-pro",         "expire": "2026-07-24"},
    {"model": "qwen3.7-max",             "expire": "2026-08-20"},
    {"model": "qwen3.7-max-2026-05-20",  "expire": "2026-08-20"},
    {"model": "qwen3.7-max-2026-05-17",  "expire": "2026-08-24"},
    {"model": "qwen3.7-max-preview",     "expire": "2026-08-24"},
    {"model": "qwen3.7-plus-2026-05-26", "expire": "2026-09-01"},
    {"model": "qwen3.7-max-2026-06-08",  "expire": "2026-09-08"},
    {"model": "glm-5.2",                 "expire": "2026-09-15"},
]

# ── 第二层：GLM 官网（GLM-4-Flash 永久免费，作为阿里云全部耗尽后的兜底）───────────
GLM_API_KEY  = os.environ.get("GLM_API_KEY", "")
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GLM_MODEL    = "glm-4-flash"

# ── 第三层：Gemini（永久免费，每日250次，最终兜底）──────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-2.0-flash"
GEMINI_BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


# ── Script Map 兜底（仅当文件缺失时使用）───────────────────────────────────────
FALLBACK_SCRIPT_MAP = """
⚠️ 警告：未找到完整版 Melody_Script_Map.md，当前为最小兜底版本，映射能力大幅受限。
请立即检查 data/Melody_Script_Map.md 是否已上传到仓库。
"""


def load_full_script_map() -> tuple[str, bool]:
    """强制读取完整 Script Map 文件，不做截取"""
    if os.path.exists(SCRIPT_MAP_PATH):
        with open(SCRIPT_MAP_PATH, encoding="utf-8") as f:
            content = f.read()
        if len(content.strip()) > 500:
            print(f"✅ 已加载完整 Script Map（{len(content)} 字符，共 {content.count('## ')} 个章节）")
            return content, True
        print(f"⚠️ {SCRIPT_MAP_PATH} 文件存在但内容过短，疑似异常文件")
    else:
        print(f"❌ 未找到 {SCRIPT_MAP_PATH}，使用兜底版本（映射能力严重受限）")
    return FALLBACK_SCRIPT_MAP, False


def load_existing_tools() -> set:
    """从 Video_Tool_DB.csv 读取已收录工具名，用于查重"""
    tools = set()
    if not os.path.exists(TOOL_DB_PATH):
        print(f"⚠️ 未找到 {TOOL_DB_PATH}，跳过查重")
        return tools
    try:
        with open(TOOL_DB_PATH, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("工具名称") or row.get("tool_name") or ""
                if name.strip():
                    tools.add(name.strip().lower())
        print(f"📋 已从 Video_Tool_DB 加载 {len(tools)} 个已收录工具")
    except Exception as e:
        print(f"⚠️ 读取 Video_Tool_DB 失败: {e}")
    return tools


def find_latest_summary() -> str | None:
    """找到今天或最近的中文摘要文件"""
    today = datetime.date.today().strftime("%Y-%m-%d")
    patterns = [
        f"{SUMMARY_DIR}/horizon-{today}-zh.md",
        f"{SUMMARY_DIR}/horizon-{today}-en.md",
    ]
    for p in patterns:
        if os.path.exists(p):
            return p
    all_files = sorted(glob.glob(f"{SUMMARY_DIR}/horizon-*.md"), reverse=True)
    return all_files[0] if all_files else None


def build_system_prompt(full_script_map: str, script_map_loaded: bool, existing_tools: set) -> str:
    """构建 System Prompt：完整 Script Map 全文注入 + 查重列表注入"""
    if existing_tools:
        tool_list = "、".join(sorted(existing_tools)[:131])
        dedup_section = f"""
## 查重规则（最高优先级，必须严格执行）
以下 {len(existing_tools)} 个工具已收录在 Video_Tool_DB.csv 中，**绝对不要重复推荐**，
也不要推荐这些工具的同义变体或马甲版本：
{tool_list}

如果日报中出现上述工具（或明显是其更新版本/同一项目的新闻），直接跳过，不生成建议书。
"""
    else:
        dedup_section = ""

    warning = "" if script_map_loaded else "\n⚠️ 重要提醒：完整 Script Map 加载失败，以下规则为兜底版本，请极度谨慎，宁可少推荐也不要乱映射。\n"

    return f"""你是 Melody 外贸自动化系统的「预审官」（Pre-Judge Agent）。

Melody 是一个外贸 B2B 商人（五金建材：铰链/滑轨），同时运营短视频副业和翡翠出海副业。
她的核心痛点：WhatsApp客户管理自动化、微信自动化、视频内容生产（Order+Video模块）、竞对情报收集。

你会收到 Horizon AI 抓取并总结的科技资讯日报（中文）。
你的任务是：从日报中识别对 Melody 业务有价值的**全新** AI 工具/技术，并严格对照下方【完整版】
Melody_Script_Map.md（系统唯一真理源，包含全部 18 个模块、全局常量、二创规则、AI筛选宪法）
逐条核对，生成《候选工具建议书》。
{warning}
{dedup_section}
## Melody_Script_Map.md（完整原文，唯一真理源 — 必须逐条对照，禁止凭空推荐）

{full_script_map}

## 你的输出规则（严格遵守 AI 筛选宪法 9 条铁律）

1. **先扫描整份日报**，找出所有可能对 Melody 有价值的工具/技术。
2. **查重**：已在 Video_Tool_DB.csv 中的工具直接跳过。
3. **映射验证（核心步骤）**：对每个候选工具，必须在上方完整 Script Map 中找到具体的原子子步骤 ID
   （如 1.12 / 2.6 / 3.5 / 13.5 / 17.3 等），**不允许凭空推荐**、不允许编造不存在的子步骤 ID。
   如果在全部18个模块中都找不到对应映射，直接跳过该工具，不生成建议书。
4. **红线检查**：核对该工具是否会触碰 Script Map 中标注的任何 ⚠️红线（如 pHash阈值8、
   WhatsApp随机等待15-30s、200条日限、RXID命名规则、5账号并发上限、20/200条历史记录长度等）。
   如果工具的应用会迫使红线被修改，必须在风险点中明确指出，建议降为[暂观]或[淘汰]。
5. **评分**：基础分(0-10) + 加成/减成（严格按 Script Map 中"AI 筛选宪法"第7条：
   映射到模块17 Order+Video → +1.0；映射到"去机器味/WhatsApp筛选/竞对情报"等高痛区 → +0.5；
   映射到核心风控步骤 → -0.5；需>16GB本地GPU且无云端版 → -1.0）。
6. **替换三定律检查**：如果建议替换某个现役实现，必须说明该替换满足"等价或更优"的哪一项
   （成本↓精度≥原 / 精度↑成本≤原 / 解锁新能力且不增风险），并提醒该替换需经 Melody 人工
   测试通过才能执行（不得擅自标记为[现役]）。

7. **对每个通过验证的新候选工具**，生成如下格式的建议书：

---
### 🔍 工具: [工具名]
**大白话结论**: [一句话，这工具对Melody有没有用，为什么]
- **来源**: [日报中的来源]
- **一句话描述**: [工具做什么]
- **映射子步骤**: [必须精确到原子ID，如 17.3 / 2.6 / 13.5，并写出该子步骤的脚本名]
- **替换对象**: [当前现役实现名，没有则填"无（新增能力）"]
- **预期收益**: [成本/精度/速度/新能力，简短]
- **风险点**: [是否触碰红线/封号风险/需付费/精度未知/兼容性等]
- **Horizon评分**: X.X（基础分X.X + 加成/减成明细）
- **建议**: [通过测试] / [暂观] / [淘汰]

8. 如果日报中**没有**找到任何能映射到 Script Map 子步骤的新工具，直接回复：
`📭 今日日报无匹配新工具（已对照全部18个模块），Melody 可跳过。`

9. **不要输出DB_INSERT块**（那是手动操作时用的）。
10. **全程中文**，简洁，不废话。
11. **最多输出5个候选工具**，按评分从高到低排序。
"""


# ── 三层模型调用 ────────────────────────────────────────────────────────────────

def is_expired(expire_str: str) -> bool:
    """判断某模型是否已过期"""
    try:
        expire_date = datetime.datetime.strptime(expire_str, "%Y-%m-%d").date()
        return datetime.date.today() > expire_date
    except Exception:
        return False


def call_dashscope(model: str, system_prompt: str, user_content: str) -> tuple[bool, str]:
    """调用阿里云百炼（OpenAI兼容接口）"""
    if not DASHSCOPE_API_KEY:
        return False, "DASHSCOPE_API_KEY 未设置"
    headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
        "max_tokens": 2500,
    }
    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(DASHSCOPE_BASE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return True, data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return False, f"{e.response.status_code}: {e.response.text[:150]}"
    except Exception as e:
        return False, str(e)


def call_glm(system_prompt: str, user_content: str) -> tuple[bool, str]:
    """调用智谱GLM官网API（GLM-4-Flash，永久免费）"""
    if not GLM_API_KEY:
        return False, "GLM_API_KEY 未设置"
    headers = {"Authorization": f"Bearer {GLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
        "max_tokens": 2500,
    }
    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(GLM_BASE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return True, data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return False, f"{e.response.status_code}: {e.response.text[:150]}"
    except Exception as e:
        return False, str(e)


def call_gemini(system_prompt: str, user_content: str) -> tuple[bool, str]:
    """调用Gemini官方API（永久免费，每日250次）"""
    if not GEMINI_API_KEY:
        return False, "GEMINI_API_KEY 未设置"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": f"{system_prompt}\n\n{user_content}"}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2500},
    }
    try:
        with httpx.Client(timeout=120) as client:
            resp = client.post(f"{GEMINI_BASE_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return True, data["candidates"][0]["content"]["parts"][0]["text"]
    except httpx.HTTPStatusError as e:
        return False, f"{e.response.status_code}: {e.response.text[:150]}"
    except Exception as e:
        return False, str(e)


def call_with_fallback(system_prompt: str, user_content: str) -> tuple[str, str]:
    """
    三层容灾调用：
    第一层：阿里云模型池（跳过已过期的，按顺序尝试）
    第二层：GLM-4-Flash（永久免费）
    第三层：Gemini（永久免费）
    返回 (结果文本, 实际使用的模型标识)
    """
    attempts_log = []

    # 第一层：阿里云模型池
    print("🔄 第一层：尝试阿里云百炼模型池...")
    for entry in DASHSCOPE_MODEL_POOL:
        model, expire = entry["model"], entry["expire"]
        if is_expired(expire):
            print(f"   ⏭️  {model} 已于 {expire} 过期，跳过")
            continue
        print(f"   🤖 尝试 {model} (到期 {expire})...")
        ok, result = call_dashscope(model, system_prompt, user_content)
        if ok:
            print(f"   ✅ {model} 调用成功")
            return result, f"阿里云/{model}"
        else:
            print(f"   ❌ {model} 失败: {result[:100]}")
            attempts_log.append(f"{model}: {result[:80]}")

    # 第二层：GLM-4-Flash
    print("🔄 第二层：阿里云全部失败，尝试 GLM-4-Flash（永久免费）...")
    ok, result = call_glm(system_prompt, user_content)
    if ok:
        print("   ✅ GLM-4-Flash 调用成功")
        return result, "智谱GLM/glm-4-flash"
    else:
        print(f"   ❌ GLM-4-Flash 失败: {result[:100]}")
        attempts_log.append(f"glm-4-flash: {result[:80]}")

    # 第三层：Gemini
    print("🔄 第三层：GLM 也失败，尝试 Gemini（永久免费）...")
    ok, result = call_gemini(system_prompt, user_content)
    if ok:
        print("   ✅ Gemini 调用成功")
        return result, f"Gemini/{GEMINI_MODEL}"
    else:
        print(f"   ❌ Gemini 失败: {result[:100]}")
        attempts_log.append(f"gemini: {result[:80]}")

    # 全部失败
    error_summary = "\n".join(attempts_log)
    return f"❌ 三层模型全部调用失败：\n{error_summary}", "无可用模型"


def send_to_feishu(content: str, summary_file: str, tool_count: int, script_map_loaded: bool, model_used: str) -> bool:
    """推送预审结果到飞书"""
    if not FEISHU_WEBHOOK:
        print("❌ FEISHU_WEBHOOK 未设置，跳过推送")
        return False

    date_str = datetime.date.today().strftime("%Y-%m-%d")
    title    = f"🔍 Horizon 预审官日报 {date_str}"

    if len(content) > 3600:
        content = content[:3600] + "\n\n...（内容过长，已截断）"

    map_status = "✅完整Script Map" if script_map_loaded else "⚠️兜底版"
    header_info = f"**来源**: `{os.path.basename(summary_file)}` | **DB已收录**: {tool_count}个 | **映射**: {map_status} | **大脑**: {model_used}\n\n"

    payload = {
        "msg_type": "interactive",
        "card": {
            "schema": "2.0",
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "green" if script_map_loaded else "orange",
            },
            "body": {"elements": [{"tag": "markdown", "content": header_info + content}]},
        },
    }

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(FEISHU_WEBHOOK, json=payload)
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print("✅ 预审结果已推送飞书")
                return True
            print(f"⚠️ 飞书返回异常: {result}")
            return False
    except Exception as e:
        print(f"❌ 飞书推送失败: {e}")
        return False


def main():
    print("🔍 Horizon 预审官 v4（完整Script Map + 三层容灾）启动...")

    full_script_map, script_map_loaded = load_full_script_map()
    existing_tools = load_existing_tools()

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

    system_prompt = build_system_prompt(full_script_map, script_map_loaded, existing_tools)
    user_content  = f"以下是今日 Horizon 科技资讯日报，请按完整 Script Map 逐条核对后进行预审分析：\n\n{summary_text}"

    print(f"📏 System Prompt 长度: {len(system_prompt)} 字符")
    result, model_used = call_with_fallback(system_prompt, user_content)

    print("─" * 60)
    print(f"实际使用大脑: {model_used}")
    print(result)
    print("─" * 60)

    send_to_feishu(result, summary_file, len(existing_tools), script_map_loaded, model_used)
    print("✅ 预审官完成")


if __name__ == "__main__":
    main()
