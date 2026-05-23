# 📑 RepoIntel（开源情报局）产品需求文档 (PRD)

## 1. 产品定位与核心价值

* **产品名称**：RepoIntel (开源情报局)
* **一句话定位**：基于 AI 与硬核指标审计的“开源米其林指南”。
* **核心宣言**：**宁缺毋滥，去伪存真，用挑剔的品味对抗信息污染。**
* **商业模式**：非盈利、无广告、无算法干扰。核心资产是**技术公信力**，长远目标是让开源作者以被 RepoIntel 收录并贴上高分徽章为至高荣誉。

## 2. 目标用户与使用场景

1. **高阶极客（RSS订阅者）**：逃离社交媒体推荐算法，渴望每天获取结构化、无废话、直击代码真相的高净值开源情报。
2. **大众开发者（微信公众号读者）**：利用通勤等碎片化时间，快速浏览由主编（你）背书的每日最强 10 个开源风向标。
3. **技术查阅者（Hugo 网站用户）**：需要寻找特定领域（如 `#Rust`、`#AI-Agent`）的优质轮子，通过分类和 Pagefind 搜索进行历史资产检索。

## 3. 核心功能需求（3层精选漏斗模型）

系统每天抓取 100+ 候选项目，必须严格执行以下三层过滤，最终**至多精选 10 个**项目上榜。

* **第一层：机器硬指标排雷（Python 脚本实现）**
* *星叉比过滤*：24小时内 Star 狂涨但 Fork 数极低（如 Fork/Star < 1%）的项目，视为水分过大或离生产环境太远，一票否决。
* *代码纯度过滤*：Markdown 或 HTML 占比超过 80% 的非代码仓库（如纯资料搜集、副业教程、Awesome系列），直接刷掉。
* *仓库健康度*：检查是否有近期 Commit 或活跃 Issue 响应，死仓库不予进入下轮。


* **第二层：低成本 AI 粗筛（Gemini Flash / DeepSeek 等低成本模型）**
* 对过滤后的约 30 个项目进行快速扫描，判断其是否具备实质工程量、是否在解决真实技术痛点，剔除纯娱乐玩具和低劣套壳项目。保留 15 个名额进入决赛圈。


* **第三层：顶级大模型硬核审计（Claude 3.5 Sonnet / GPT-4o 级别模型）**
* 由顶级 AI 扮演“刻薄、资深”的首席架构师，切开营销话术，对项目进行四维严苛打分（创新度、实用性、工程完备度、社区健康度）。
* **硬核毒舌简评**：必须指出项目的技术亮点、以及隐藏的“雷点/隐患”（如无测试、单人维护、并发瓶颈等）。
* 综合得分低于 75 分直接淘汰，每天最终发布的名额宁缺毋滥，上限 10 个。



## 4. 分发与内容呈现需求

1. **静态百科全书 (Hugo 页面)**：自动按技术标签、主题分类（Categories）归档，支持年/月日期分类。
2. **全量 RSS 2.0**：输出不限流、包含 AI 深度点评全量内容的 `index.xml`，支持按分类标签独立订阅。
3. **微信公众号排版文本**：每天Actions跑完，自动在本地生成一份**完美适配微信复制即发的群发 Markdown/纯文本模板**，包含今日风向标摘要和高分项目点评。

---

# 🏗️ RepoIntel 技术架构与规范手册

## 1. 整体系统架构 (Serverless Pipeline)

项目完全基于无服务器架构运转。依托 GitHub Actions 提供定时算力，Cloudflare R2 提供状态感知（持久化），大模型 API 提供智能审计，GitHub Pages 提供静态内容与 RSS 分发。

## 2. 状态感知与去重逻辑 (Cloudflare R2)

为防止Actions在每天干净的环境中重复审计过去几天连续上榜的项目，引入 Cloudflare R2 充当轻量级无服务器数据库。

* **缓存文件**：`processed_repos.json`
* **工作流**：
1. 脚本启动，使用 `boto3` 库从 R2 下载 `processed_repos.json`。
2. 对比今日捞出的 100+ 候选池，自动剔除最近 14 天内已经审计过的项目，防止重复消耗 AI Token 并导致网站内容冗余。
3. 决赛圈的 10 个项目审计完成后，将其 ID 与审计日期追加写入列表，并传回 R2 覆盖保存。



## 3. 多模型双模适配器设计 (Multi-LLM Adapter)

系统必须支持在配置文件中自由切换大模型供应商，且完美兼容两种不同的请求和 JSON 返回协议：

* **OpenAI 协议模式**：兼容 OpenAI 原生、DeepSeek 各种中转站。使用官方 SDK，开启 `response_format={"type": "json_object"}` 或结构化输出，确保 100% 返回 JSON。
* **Claude 协议模式**：兼容 Anthropic 原生或 AWS Bedrock 等渠道。由于 Claude 协议入参不同且无原生 JSON 强制开关，需在 System Prompt 中强制约束，并在 Python 侧使用正则表达式容错提取（如提取最外层 `{...}`），防止其携带 Markdown 的 ```json 包裹。

## 4. 四维加权打分算法

最终得分 ($Score$) 严格执行以下加权公式：


$$Score = 0.30 \cdot I (创新度) + 0.30 \cdot U (实用性) + 0.25 \cdot E (工程质量) + 0.15 \cdot H (社区健康)$$

* **创新度 (Innovation)**：是否开创了新范式，还是第 101 个高仿轮子。
* **实用性 (Utility)**：开发者能否拿来即用，解决了什么真实高频痛点。
* **工程质量 (Engineering)**：是否有测试用例、CI/CD 流程、架构设计、代码组织是否规范。
* **社区健康度 (Health)**：结合硬指标折算（Issue 活跃度、Contributor 多元化等）。

## 5. Hugo 元数据与前端检索规范

AI 吐出的 JSON 必须转化为带有如下 Front Matter 的 Markdown 页面：

```yaml
---
title: "[Score: 89.5] owner/repo"
date: 2026-05-23T08:00:00Z
categories: ["AI-Agent Framework"]  # 主题分类
tags: ["Python", "Automation"]       # 技术栈标签
intel_score: 89.5
repo_link: "[https://github.com/owner/repo](https://github.com/owner/repo)"
summary: "一句话情报解密。"
---

```

* **搜索实现**：在 Actions 构建构建完静态网页后，立即在根目录执行 `npx pagefind --site public`，生成轻量级静态全文索引，供前端实现零服务器成本的毫秒级中英文全文检索。

---

# 🤖 Cursor 终极全套开发提示词 (Prompt)

请在本地电脑新建一个名为 `repointel_pipeline` 的文件夹，并在内部初始化一个带有精美主题（如 Blowfish 或 FixIt）的 Hugo 项目，文件夹命名为 `hugo-site`。

然后，将以下黄金提示词完整复制，粘贴进 Cursor 的 **Composer (Ctrl+I / Cmd+I)** 或 **Chat** 面板中，让 Cursor 为你疯狂敲代码：

```markdown
You are an expert Principal DevOps and Python Engineer building a high-trust open-source intelligence pipeline named "RepoIntel". This pipeline runs daily via GitHub Actions to scrape, filter, analyze, and publish the top 10 truly elite GitHub repositories into a Hugo-based static site and a WeChat-ready text template.

Please generate the complete production-grade Python project structure, including all error handling, asynchronously or synchronously as appropriate.

### 1. Directory Layout to Create
- `main.py`: Entry point coordinating the 3-layer pipeline.
- `config.py`: Validates environmental configurations.
- `scraper.py`: Handles Layer 1 (hard metric filtering).
- `r2_manager.py`: Manages state caching via Cloudflare R2 (boto3) to prevent duplicate analysis.
- `ai_engine.py`: Evolved Multi-LLM adapter supporting both OpenAI and Claude native protocols.
- `content_gen.py`: Generates structured YAML front-matter Markdowns for Hugo and a special text template for WeChat.
- `requirements.txt`: Python package dependencies.
- `.github/workflows/repointel-cron.yml`: GitHub Actions schedule configuration.

### 2. Module Specifications

#### `config.py`
Load and strictly validate:
- `LLM_PROVIDER`: 'openai' or 'claude'
- `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`
- `R2_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`

#### `scraper.py` & `r2_manager.py` (Layer 1 Funnel)
- Fetch top 50 trending repositories of the day (use a reliable public GitHub Trending API mirror like `https://api.gitterapp.com/` or GitHub Search API).
- Connect to Cloudflare R2 using `boto3`. Fetch `processed_repos.json`. If it doesn't exist, fall back to an empty list. 
- Filter out any repository already listed in `processed_repos.json` (cached for the last 14 days).
- **Hard Metric Filter**: Drop repos where primary language is Markdown/HTML. Drop repos where `forks_count / stars_count < 0.01` (flag as fake stars/low quality). Ensure it has commits within 48 hours.

#### `ai_engine.py` (Layer 2 & 3 Funnels)
- Implement a single interface `analyze_repos(eligible_repos: list) -> list[dict]`.
- **Layer 2 (Rough Screen)**: Pass the repos (~30) through a fast/cheap prompt (if using OpenAI protocol, can use a cheaper model or light instructions) to pick the best 15.
- **Layer 3 (Deep Audit)**: Pass the final 15 to the premium model defined in configs.
- **Protocol Adaptation**:
  - If `openai`: Use `openai` SDK with `response_format={"type": "json_object"}` or Structured Outputs.
  - If `claude`: Send a direct native HTTP POST request to the Claude endpoint or use `anthropic` SDK. Inject a strict system prompt: "Return ONLY raw JSON. No markdown codeblocks." Use regex in Python to safely extract `{...}` from the response if Claude returns backticks.
- **Strict JSON Output Schema**:
  {
    "repo_name": "string",
    "category": "Theme classification string",
    "tags": ["array", "of", "strings"],
    "scores": {"innovation": int, "utility": int, "engineering": int, "health": int, "total_score": float},
    "summary": "One sentence killer summary.",
    "pain_point": "What concrete engineering pain point this solves.",
    "technical_review": "Cynical, deep architecture and code-level critique pointing out flaws, single-point failures, or brilliance.",
    "commercial_value": "Potential value or ecosystem impact."
  }
- **Persona**: The LLM must act as a brutal, cynical, and highly experienced Senior Enterprise Architect who cuts through marketing hype.

#### `content_gen.py`
- Sort audited repos by `total_score` descending. Discard any repo scoring below 75. Keep up to the top 10.
- **Hugo Output**: Write to `hugo-site/content/posts/{date}-{repo_slug}.md`. Embed all scores, tags, categories, repo_link, and summary into standard YAML Front Matter. Write the body beautifully using H2/H3 for pain points, reviews, etc.
- **WeChat Output**: Write a beautifully formatted plain text file `wechat_digest.txt` containing a summary of today's intelligence, ranking the top repos with their scores and one-sentence summaries, optimized for copy-pasting into WeChat Official Account editor.
- **Cache Update**: Append the successfully posted repo names to `processed_repos.json` and upload back to R2.

#### `.github/workflows/repointel-cron.yml`
- Setup daily cron task. 
- Set up Python environment, install `requirements.txt`, run `main.py`.
- **Static Pagefind Indexing**: Navigate to `hugo-site`, compile with `hugo --minify`, then immediately execute `npx pagefind --site public` to index the build directory.
- Deploy `hugo-site/public` to `gh-pages` branch using standard GitHub deployment actions.

Please generate complete, production-ready, clean Python and YAML code blocks now.
