---
title: '[Score: 79.15] akitaonrails/ai-memory'
date: '2026-05-24T19:14:04Z'
categories:
- AI Agent Memory Infrastructure
tags:
- Rust
- MCP
- SQLite
- LLM Consolidation
- Developer Tools
- Wiki
intel_score: 79.15
repo_name: akitaonrails/ai-memory
repo_link: https://github.com/akitaonrails/ai-memory
summary: 基于 Rust 的 MCP 服务器，将 AI 编码 agent 的会话自动捕获为项目级 markdown wiki，支持跨 agent（Claude
  Code / Codex 等）上下文接续，适合频繁在多工具间切换的个人开发者。
code_source: git
code_files_reviewed:
- evals/Cargo.toml
- crates/ai-memory-llm/Cargo.toml
- crates/ai-memory-store/Cargo.toml
- crates/ai-memory-core/Cargo.toml
- crates/ai-memory-consolidate/Cargo.toml
- crates/ai-memory-hooks/Cargo.toml
- .github/workflows/release.yml
- .github/workflows/ci.yml
- crates/ai-memory-mcp/src/lib.rs
- crates/ai-memory-wiki/src/lib.rs
- crates/ai-memory-web/src/routes/mod.rs
- crates/ai-memory-consolidate/src/lib.rs
- crates/ai-memory-core/src/lib.rs
- crates/ai-memory-hooks/src/lib.rs
- crates/ai-memory-web/src/lib.rs
- crates/ai-memory-llm/src/lib.rs
- crates/ai-memory-cli/src/main.rs
- crates/ai-memory-web/tailwind.config.js
- crates/ai-memory-web/build.rs
- crates/ai-memory-mcp/tests/admin_status_search.rs
- crates/ai-memory-mcp/tests/admin_backup.rs
- crates/ai-memory-mcp/tests/admin_bootstrap.rs
- crates/ai-memory-consolidate/tests/embeddings.rs
- crates/ai-memory-mcp/tests/mcp_stateless_http.rs
- crates/ai-memory-web/tests/routes.rs
- crates/ai-memory-consolidate/tests/recall_eval.rs
- crates/ai-memory-mcp/tests/admin_write_page.rs
- crates/ai-memory-store/migrations/V06__wiki_migrations.sql
- crates/ai-memory-store/src/migrations.rs
- crates/ai-memory-web/src/state.rs
- crates/ai-memory-store/migrations/V04__embeddings.sql
- crates/ai-memory-core/src/error.rs
- crates/ai-memory-wiki/src/error.rs
- crates/ai-memory-store/migrations/V03__decay.sql
- crates/ai-memory-llm/src/error.rs
- crates/ai-memory-store/src/error.rs
- crates/ai-memory-llm/src/text.rs
- crates/ai-memory-store/migrations/V02__handoffs.sql
- crates/ai-memory-cli/src/process_guard.rs
- crates/ai-memory-mcp/prompts/explore_system.md
- crates/ai-memory-llm/src/provider.rs
- crates/ai-memory-cli/src/logging.rs
- crates/ai-memory-consolidate/prompts/single_consolidate_system.md
- crates/ai-memory-llm/src/types.rs
- crates/ai-memory-store/migrations/V05__cascade_indexes.sql
- crates/ai-memory-consolidate/prompts/lint_system.md
- crates/ai-memory-consolidate/prompts/batch_consolidate_system.md
- crates/ai-memory-cli/templates/config.default.toml
code_chars_analyzed: 122041
---

<section class="content-panel content-panel--scope" id="scope">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⌁</span>
  <h2 class="panel-title">审读源码范围</h2>
</header>
<div class="panel-body">
  <div class="scope-stats">
    <div class="scope-stat">
      <span class="scope-stat__label">代码来源</span>
      <span class="scope-stat__value">git</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">审读文件</span>
      <span class="scope-stat__value">48 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 122,041 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">evals/Cargo.toml</code></li><li><code class="path-chip">crates/ai-memory-llm/Cargo.toml</code></li><li><code class="path-chip">crates/ai-memory-store/Cargo.toml</code></li><li><code class="path-chip">crates/ai-memory-core/Cargo.toml</code></li><li><code class="path-chip">crates/ai-memory-consolidate/Cargo.toml</code></li><li><code class="path-chip">crates/ai-memory-hooks/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">crates/ai-memory-mcp/src/lib.rs</code></li><li><code class="path-chip">crates/ai-memory-wiki/src/lib.rs</code></li><li><code class="path-chip">crates/ai-memory-web/src/routes/mod.rs</code></li><li><code class="path-chip">crates/ai-memory-consolidate/src/lib.rs</code></li><li><code class="path-chip">crates/ai-memory-core/src/lib.rs</code></li><li><code class="path-chip">crates/ai-memory-hooks/src/lib.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在 Claude Code 里调试到一半切到 Codex 继续，新 agent 对之前试过的方案、失败路径、待解决问题一无所知，每次都要从头解释架构背景，浪费 10-20 分钟且容易重蹈覆辙。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 Rust workspace 拆分为 8 个 crate，核心存储层（ai-memory-store）使用 SQLite WAL 模式 + 单 writer actor（通过 tokio mpsc 有界通道串行化所有写入，见 <code class="code-ref">crates/ai-memory-store/Cargo.toml:8</code> 描述），读路径走 ReaderPool。Wiki 文件层（ai-memory-wiki）负责原子写盘 + frontmatter 解析 + 同步写入 store writer actor 保证索引与磁盘一致。Hooks 层通过 shell 脚本 fire-and-forget POST 到服务器端点（<code class="code-ref">crates/ai-memory-hooks/src/lib.rs:12</code> 注明 200ms 硬超时防死锁），经 Sanitizer 隐私脱敏后写入 observation 表。MCP 服务器暴露窄工具面给 agent CLI，支持 stdio 和 Streamable HTTP 双传输。Consolidate 层在 SessionEnd 时调用 LLM 将原始 observation 编译为 wiki 页面，实现了 Karpathy 式「编译非检索」模式。Web UI 是纯只读的 axum 路由（<code class="code-ref">crates/ai-memory-web/src/lib.rs:12</code> 明确声明 v1 无编辑/无 POST），支持 FTS5 搜索和 markdown 渲染。CI 流水线完备：fmt + clippy + 多平台测试 + release build + docker smoke + cargo-deny + cargo-audit + gitleaks（<code class="code-ref">.github/workflows/ci.yml</code>）。LLM provider 采用原生 typed client 而非通用网关（<code class="code-ref">crates/ai-memory-llm/src/lib.rs:10</code> 注明避免 cognee 式 kwarg-drop 问题），三种 structured-output 策略分别适配 Anthropic/OpenAI/OpenAI-compat。</p>
<p class="audit-callout audit-callout--highlight">隐私脱敏是类型边界而非可选步骤——<code class="code-ref">crates/ai-memory-hooks/src/lib.rs:22</code> 指出 observation 必须先经过 <code class="code-ref">Sanitized::new</code> 才能写入，config 中内置了覆盖 bearer token、JWT、PEM 私钥、常见云 provider env var、~/.ssh 等路径的正则（<code class="code-ref">crates/ai-memory-cli/templates/config.default.toml:46</code>），且支持自定义 extra_patterns 和 allowlist。</p>
<p class="audit-callout audit-callout--highlight">Recall@5 评测框架是真实的 CI 可执行代码——<code class="code-ref">crates/ai-memory-consolidate/tests/recall_eval.rs</code> 构建了 10 条 hand-crafted corpus + 10 条 probe，分别测量纯 FTS5 和 hybrid（FTS5 + RRF + vector）路径的召回率，下限设为 0.70，且支持切换真实 embedding provider 运行。这不是 mock，而是端到端跑真磁盘 store + wiki。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 store 的 writer actor 实现（<code class="code-ref">ai-memory-store/src/</code> 下的 writer.rs 或 actor.rs 未在 code_bundle 中提供），无法验证 mpsc 有界通道的容量、背压策略、writer panic 后的恢复逻辑。这是单写者模型的核心，缺失评估降低工程置信度。</p>
<p class="audit-callout audit-callout--doubt">MCP server 的 tool 实现（<code class="code-ref">crates/ai-memory-mcp/src/server.rs</code>）未在 code_bundle 中提供，无法审查 memory_query、memory_handoff_begin 等工具的参数校验、错误传播、权限控制是否到位。`</p>
<p>如果要在团队中使用，需注意当前 handoff 表结构（<code class="code-ref">crates/ai-memory-store/migrations/V02__handoffs.sql:7</code>）中 <code class="code-ref">from_agent</code> 是必填但 <code class="code-ref">to_agent</code> 可空，意味着自动 handoff 的目标 agent 信息丢失；建议在 SessionStart hook 中补充 accept 逻辑以填充该字段。另外，服务器默认无认证（README 明确说明），暴露到 LAN 前必须配置 bearer token。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>writer actor 核心实现未在 code_bundle 中提供，无法评估单写者崩溃恢复和背压边界，生产可靠性存疑。</li><li>项目仅 2 天历史、30 次 commit，v0.2 的 API 表面积仍在快速变化，MCP tool schema 和 hook payload 可能在近期有 breaking change。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对个人开发者或小团队有实际价值——零配置将多 agent 编码会话变成可搜索的项目知识库，grep 友好的 markdown 格式降低锁入风险。但缺乏多用户权限模型和 SaaS 化路径，短期内更可能成为小众工具而非平台。</p>
</div>
</section>

<section class="content-panel content-panel--scores" id="scores">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">▣</span>
  <h2 class="panel-title">四维评分</h2>
</header>
<div class="panel-body">
  <div class="score-grid">
    <div class="score-item">
  <div class="score-item__label">创新度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.15</span>
  </div>
</div>
</section>