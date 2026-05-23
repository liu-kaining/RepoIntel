# RepoIntel（开源情报局）

基于 AI 与硬核指标审计的「开源米其林指南」——宁缺毋滥，去伪存真，用挑剔的品味对抗信息污染。

> 完整产品需求见 [`spec/INFO.md`](spec/INFO.md) · CTO 审查报告见 [`spec/CTO_REVIEW.md`](spec/CTO_REVIEW.md)

## 架构概览

RepoIntel 是一个完全 Serverless 的开源情报流水线，每日自动运行：

```text
GitHub Search API
       ↓
Layer 1 · 硬指标过滤（Star/Fork、语言纯度、近期提交、去重）
       ↓
Layer 2 · 低成本 LLM 粗筛（~30 → 15）
       ↓
Layer 3 · 顶级 LLM 深度审计（CTO 视角四维打分 + 毒舌简评）
       ↓
Content Gen · Hugo Markdown + 微信文本 + R2 状态缓存
       ↓
GitHub Actions · Hugo 构建 + Pagefind 索引 + gh-pages 部署
```

### 核心设计原则

| 原则 | 实现 |
|------|------|
| 宁缺毋滥 | 总分 < 75 不发布，每日上限 10 个 |
| 去重省 Token | Cloudflare R2 缓存 14 天内已深度审计的仓库 |
| 分数不可伪造 | LLM 返回的 `total_score` 被忽略，本地按加权公式重算 |
| 多模型兼容 | OpenAI 协议 / Claude 协议双模适配器 |

## 代码结构

```text
main.py                          # 本地入口（python main.py）
src/repointel/
  pipeline.py                    # 流水线编排
  config.py                      # 环境变量加载与校验
  github_client.py               # GitHub 抓取、增强、Layer 1 硬指标过滤
  ai_engine.py                   # Layer 2/3 多模型 LLM 审计
  r2_manager.py                  # Cloudflare R2 / 本地 JSON 状态存储
  content_gen.py                 # Hugo 文章与微信公众号文本生成
  models.py                      # 数据模型与评分公式
  exceptions.py                  # 统一异常层次
tests/                           # 单元测试
hugo-site/                       # Hugo 静态站点（含 Pagefind 搜索）
.github/workflows/               # 每日定时 CI/CD
spec/                            # 产品需求与审查文档
```

## 快速开始

### 安装

```bash
pip install -e '.[dev]'
```

### Dry-run（无需 API Key）

```bash
REPOINTEL_DRY_RUN=true python -m repointel
```

Dry-run 会生成 17 个模拟候选仓库，走完完整三层漏斗，并在 `hugo-site/content/posts/` 与 `output/wechat_digest.txt` 产出示例内容。状态写入 `output/processed_repos.json`（本地模式）。

### 正式运行

```bash
export GITHUB_TOKEN=ghp_...          # 可选，提升 GitHub API 速率上限
export LLM_PROVIDER=openai           # openai 或 claude
export LLM_MODEL=gpt-4o              # 深度审计模型
export LLM_API_KEY=sk-...
export LLM_BASE_URL=https://...      # 可选，兼容中转站
export ROUGH_LLM_MODEL=deepseek-chat # 可选，粗筛低成本模型
export R2_ENDPOINT_URL=https://...r2.cloudflarestorage.com
export R2_ACCESS_KEY_ID=...
export R2_SECRET_ACCESS_KEY=...
export R2_BUCKET_NAME=repointel-state
python -m repointel
```

## 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `REPOINTEL_DRY_RUN` | `false` | 跳过真实 API 调用，使用启发式审计 |
| `LLM_PROVIDER` | `openai` | `openai` 或 `claude` |
| `LLM_MODEL` | — | 深度审计模型（dry-run 下可选） |
| `LLM_API_KEY` | — | LLM API 密钥 |
| `LLM_BASE_URL` | — | 自定义 API 端点（中转站） |
| `ROUGH_LLM_MODEL` | 同 `LLM_MODEL` | 粗筛阶段使用的低成本模型 |
| `GITHUB_TOKEN` | — | GitHub PAT，提升 Search API 配额 |
| `R2_ENDPOINT_URL` | — | Cloudflare R2 S3 兼容端点 |
| `R2_ACCESS_KEY_ID` | — | R2 访问密钥 |
| `R2_SECRET_ACCESS_KEY` | — | R2 秘密密钥 |
| `R2_BUCKET_NAME` | — | R2 存储桶名 |
| `R2_CACHE_KEY` | `processed_repos.json` | 状态文件键名 |
| `REPOINTEL_STATE_BACKEND` | `r2` | `r2` 或 `local` |
| `REPOINTEL_LOCAL_STATE` | `output/processed_repos.json` | 本地状态文件路径 |
| `HUGO_CONTENT_DIR` | `hugo-site/content/posts` | Hugo 文章输出目录 |
| `REPOINTEL_OUTPUT_DIR` | `output` | 微信文本等产物目录 |
| `REPOINTEL_MAX_CANDIDATES` | `100` | 每日候选池上限 |
| `REPOINTEL_ROUGH_LIMIT` | `15` | 粗筛保留名额 |
| `REPOINTEL_FINAL_LIMIT` | `10` | 每日发布上限 |
| `REPOINTEL_SCORE_THRESHOLD` | `75` | 最低发布分数 |
| `REPOINTEL_CACHE_TTL_DAYS` | `14` | 去重缓存 TTL（天） |
| `REPOINTEL_MIN_FORK_STAR_RATIO` | `0.01` | 最低 Fork/Star 比 |
| `REPOINTEL_MIN_STARS` | `50` | 最低 Star 数 |
| `REPOINTEL_RECENT_PUSH_HOURS` | `48` | 近期推送窗口（小时） |

## 评分公式

```
Score = 0.30 × 创新度 + 0.30 × 实用性 + 0.25 × 工程质量 + 0.15 × 社区健康度
```

LLM 输出的各维度分数由 Python 本地重算总分，防止模型自行虚报 `total_score`。

## GitHub Actions 部署

工作流 [`.github/workflows/repointel-cron.yml`](.github/workflows/repointel-cron.yml) 每日 UTC 00:00 自动运行（支持 `workflow_dispatch` 手动触发）：

1. Lint + 单元测试
2. 运行 RepoIntel 流水线
3. 上传 `wechat_digest.txt` 为 Artifact
4. Hugo 构建 + Pagefind 全文索引
5. 部署到 `gh-pages` 分支

### 所需 Secrets

在 GitHub Repository Settings → Secrets 中配置：

- `LLM_PROVIDER`, `LLM_MODEL`, `LLM_API_KEY`
- `LLM_BASE_URL`, `ROUGH_LLM_MODEL`（可选）
- `R2_ENDPOINT_URL`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET_NAME`

`GITHUB_TOKEN` 由 Actions 自动注入，无需额外配置。

### Hugo 站点配置

部署前请将 `hugo-site/hugo.toml` 中的 `baseURL` 修改为你的 GitHub Pages 域名：

```toml
baseURL = "https://your-username.github.io/RepoIntel/"
```

## 验证

```bash
python -m pytest -v
python -m ruff check src tests
python -m ruff format --check src tests
REPOINTEL_DRY_RUN=true python -m repointel
```

## License

MIT — 详见 [LICENSE](LICENSE)
