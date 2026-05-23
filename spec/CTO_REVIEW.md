# RepoIntel CTO Review

**审查日期**：2026-05-23
**审查范围**：Python Pipeline、AI 审计引擎、GitHub 抓取、R2 状态、Hugo 站点、GitHub Actions、测试与部署文档
**审查标准**：Spec 一致性、生产可用性、Token 经济性、故障隔离、安全基线、CI/CD 可部署性

---

## 1. 执行摘要

RepoIntel 已完成从产品规格到可运行工程的闭环实现。整体架构符合 `spec/INFO.md` 的三层漏斗设计：

1. GitHub 候选抓取与硬指标过滤；
2. 低成本 LLM 粗筛；
3. 高质量 LLM 深度审计；
4. Hugo / RSS / Pagefind / 微信文本生成；
5. Cloudflare R2 去重状态；
6. GitHub Actions 每日自动部署。

本轮 CTO Review 发现并修复了若干上线前问题，包括：LLM SDK 异常未统一包装、粗筛模型失败会中断全链路、CI Pagefind 可能交互阻塞、Hugo `baseURL` 默认值不适合部署、配置边界校验不足、HTML 模板缺少 `</body>`。

**综合结论：Approve for Beta deployment.**
配置 Secrets 后，建议先手动触发一次 `workflow_dispatch`，验证 R2 写入、LLM 输出质量、Hugo 页面和 WeChat Artifact。

---

## 2. 审查结论

| 维度 | 评级 | 结论 |
|------|------|------|
| 架构设计 | 通过 | 模块边界清晰，Pipeline 编排简洁，符合 Serverless 目标 |
| Spec 一致性 | 通过 | 三层漏斗、加权评分、R2 去重、内容生成均已落地 |
| AI 能力 | 通过 | Prompt 约束明确，总分本地重算，OpenAI/Claude 双协议适配 |
| 代码质量 | 通过 | Ruff 0 warning，类型注解完整，核心对象不可变建模 |
| 测试覆盖 | 基础可接受 | 12 个单元测试覆盖核心逻辑；仍缺外部 API mock 集成测试 |
| 生产容错 | 通过 | GitHub 限流、LLM 重试、单仓库失败隔离、粗筛降级已处理 |
| CI/CD | 通过 | lint、format check、pytest、Hugo、Pagefind、gh-pages 部署完整 |
| 安全性 | 可接受 | 无硬编码密钥；`.env` 忽略；R2/LLM/GitHub 凭证走环境变量 |

---

## 3. 本轮已修复问题

### P0-1 · LLM SDK 异常未统一包装

**文件**：`src/repointel/ai_engine.py`

**问题**：OpenAI / Anthropic SDK 抛出的网络错误、限流错误或服务端错误不是 `LLMResponseError`，导致 `_complete()` 的统一重试逻辑无法捕获，实际生产会直接失败。

**修复**：

- `_complete_openai()` 包装 SDK 调用异常为 `LLMResponseError`；
- `_complete_claude()` 包装 SDK 调用异常为 `LLMResponseError`；
- 保留 3 次退避重试。

---

### P0-2 · 粗筛模型失败会中断整条 Pipeline

**文件**：`src/repointel/ai_engine.py`

**问题**：Layer 2 粗筛失败时直接抛错，导致即使 GitHub 候选和硬指标过滤成功，后续深度审计也无法执行。

**修复**：粗筛失败时记录错误，并按硬指标信号排序降级选取前 `REPOINTEL_ROUGH_LIMIT` 个仓库继续运行。

**新增测试**：`test_rough_screen_falls_back_to_metric_ordering`

---

### P1-1 · 配置边界校验不足

**文件**：`src/repointel/config.py`

**问题**：`REPOINTEL_ROUGH_LIMIT > REPOINTEL_MAX_CANDIDATES`、`REPOINTEL_FINAL_LIMIT > REPOINTEL_ROUGH_LIMIT` 等配置错误不会在启动时失败，可能造成部署后行为与预期不一致。

**修复**：新增配置一致性校验：

- rough limit 不得超过 max candidates；
- final limit 不得超过 rough limit；
- TTL 与近期推送窗口必须为正；
- min stars / fork-star ratio 不得为负。

**新增测试**：`test_settings_rejects_incoherent_limits`

---

### P1-2 · CI Pagefind 命令可能交互阻塞

**文件**：`.github/workflows/repointel-cron.yml`

**问题**：`npx pagefind --site public` 在首次安装时可能提示确认安装包，CI 中存在卡住风险。

**修复**：改为：

```bash
npx -y pagefind --site public
```

---

### P1-3 · CI 缺少 format gate

**文件**：`.github/workflows/repointel-cron.yml`

**问题**：仅执行 `ruff check` 和 `pytest`，没有阻止未格式化代码进入部署。

**修复**：增加：

```bash
python -m ruff format --check src tests
```

---

### P2-1 · Hugo `baseURL` 默认值不适合部署

**文件**：`hugo-site/hugo.toml`

**问题**：默认 `baseURL = "https://example.com/"` 会污染 RSS 和页面链接。

**修复**：改为相对 URL 配置：

```toml
baseURL = "/"
relativeURLs = true
canonifyURLs = false
```

这能直接适配 GitHub Pages 项目站点；如需自定义域名，可后续修改 `baseURL`。

---

### P2-2 · HTML 模板缺少 `</body>`

**文件**：`hugo-site/layouts/_default/baseof.html`

**问题**：模板闭合 `</html>` 但缺少 `</body>`，浏览器可容错，但不符合上线质量标准。

**修复**：补齐 `</body>`。

---

### P2-3 · 缺少部署参数样例

**文件**：`.env.example`, `README.md`

**问题**：部署前需要配置 GitHub、LLM、R2、Pipeline 阈值等参数，README 虽有表格，但缺少可复制的环境变量模板。

**修复**：新增 `.env.example`，并在 README 中说明本地 `source .env` 的方式。

---

## 4. 既有关键设计确认

### 4.1 AI 审计能力

确认点：

- Layer 2 粗筛 Prompt 明确强调“去噪音、拒绝玩具项目、不要被 Star 数迷惑”；
- Layer 3 深度审计 Prompt 明确要求 CTO/架构审计视角；
- 模型只返回四个维度分数，总分由 Python 本地按公式重算；
- Claude Markdown code block / 前后缀文本具备 JSON 容错提取；
- 单仓库深度审计失败不会拖垮整个批次。

风险：

- 当前只基于 GitHub 元数据、README 摘要、语言分布判断，尚未拉取源码树和测试文件做更深代码级审计；
- Prompt 注入风险存在于 README 内容，但已通过长度截断降低风险。后续可把 README 放入明确的“不可信数据”标签中进一步隔离。

### 4.2 Token 经济性

确认点：

- 先硬指标过滤，再粗筛，再深审，符合成本递进；
- `processed_repos.json` 缓存所有已深度审计仓库，而非仅发布仓库，避免低分项目反复烧 Token；
- README 输入截断，避免超长仓库介绍吞掉上下文。

### 4.3 状态与幂等

确认点：

- R2 / local 双后端抽象合理；
- TTL 清理逻辑明确；
- GitHub Actions concurrency group 防止同一分支并发运行造成 R2 状态覆盖。

待增强：R2 保存未做乐观锁。如果未来允许多地区、多 workflow 并发运行，应引入对象版本或 ETag 条件写。

---

## 5. 测试与验证结果

本轮执行结果：

```text
python -m ruff check src tests
All checks passed
```

```text
python -m ruff format --check src tests
All files formatted
```

```text
python -m pytest
12 passed
```

```text
python -m compileall -q src tests
通过
```

```text
REPOINTEL_DRY_RUN=true REPOINTEL_STATE_BACKEND=local python -m repointel
成功：17 个模拟候选 → 15 个粗筛审计 → 10 个发布 → 15 条状态缓存
```

本地未执行真实 Hugo build，原因是当前机器没有安装 Hugo CLI；GitHub Actions 已通过 `peaceiris/actions-hugo@v3` 安装 Hugo。

---

## 6. 部署前检查清单

### GitHub Secrets

必须配置：

- `LLM_PROVIDER`
- `LLM_MODEL`
- `LLM_API_KEY`
- `R2_ENDPOINT_URL`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`

可选配置：

- `LLM_BASE_URL`
- `ROUGH_LLM_MODEL`

`GITHUB_TOKEN` 由 GitHub Actions 自动注入。

### R2 权限

建议：

- 单独创建 R2 bucket；
- R2 token 只允许该 bucket 的读写；
- `R2_CACHE_KEY` 保持默认 `processed_repos.json` 即可。

### 首次上线步骤

1. 配置 Secrets；
2. 手动触发 `RepoIntel Daily Pipeline`；
3. 检查 Actions 日志中候选数、过滤数、审计数、发布数；
4. 检查 `wechat_digest.txt` Artifact；
5. 检查 `gh-pages` 分支和 GitHub Pages 页面；
6. 检查 R2 中 `processed_repos.json` 是否写入。

---

## 7. 不阻塞上线的后续建议

| ID | 优先级 | 建议 |
|----|--------|------|
| L-1 | 中 | 为 GitHub / LLM / R2 增加 Mock 集成测试，覆盖完整 Pipeline |
| L-2 | 中 | 深度审计可引入有限并发，建议并发度 3-5，避免超时 |
| L-3 | 中 | 把 README 内容包装成“不可信输入”片段，进一步降低 Prompt 注入风险 |
| L-4 | 低 | 增加运行摘要 Markdown Artifact，方便每日运营复盘 |
| L-5 | 低 | 增加源码树采样，提升 AI 对工程质量的判断依据 |
| L-6 | 低 | 迁移到官方 `actions/deploy-pages@v4`，减少第三方部署 Action 依赖 |

---

## 8. 签核

| 角色 | 判定 |
|------|------|
| CTO Review | **Approve** |
| 上线建议 | 可部署 Beta；首次运行建议手动触发并人工查看输出质量 |
| 风险等级 | 中低；主要风险来自外部 API、LLM 输出波动和 Secrets 配置错误 |
