---
title: '[Score: 78.15] Shadow-Weave/HMS'
date: '2026-07-15T10:46:43Z'
categories:
- AI Agent Memory Framework
tags:
- memory
- agents
- postgres
- langchain
- opentelemetry
- temporal-reasoning
intel_score: 78.15
repo_name: Shadow-Weave/HMS
repo_link: https://github.com/Shadow-Weave/HMS
summary: HMS 为 LLM 智能体提供结构化长期记忆，在生成回答前构建证据账簿，以提升跨会话、多时间粒度的推理可靠性。
code_source: git
code_files_reviewed:
- interface/adapters/claude-code/requirements.txt
- interface/adapters/dify/requirements.txt
- interface/sdk/go/go.mod
- pyproject.toml
- core/dataplane-full/pyproject.toml
- interface/adapters/cloudflare-oauth-proxy/package.json
- core/local-suite-slim/README.md
- core/local-suite/README.md
- core/dataplane-full/README.md
- core/dataplane/README.md
- core/daemon/test.sh
- core/daemon/README.md
- core/dataplane/test_modular_search.py
- interface/adapters/claude-code/tests/test_manifest.py
- interface/adapters/dify/tests/conftest.py
- core/dataplane/tests/test_mcp_server_version.py
- core/dataplane/tests/fixtures/README.md
- core/dataplane/tests/test_think.py
- interface/adapters/langgraph/tests/test_manual.py
- core/dataplane/tests/test_llm_wrapper.py
- interface/adapters/codex/tests/test_client.py
- core/dataplane/hms_api/utils.py
- core/dataplane/hms_api/mcp_local.py
- core/daemon/hms_embed/embed_manager.py
- core/dataplane/hms_api/db_url.py
- core/dataplane/hms_api/server.py
- core/dataplane/hms_api/banner.py
- core/local-suite/hms/api_namespaces.py
- core/dataplane/hms_api/_vector_index.py
- core/dataplane/hms_api/daemon.py
- core/dataplane/hms_api/pg0.py
- core/local-suite/hms/server.py
- core/daemon/hms_embed/daemon_client.py
- core/dataplane/hms_api/models.py
- core/local-suite/hms/client_wrapper.py
- core/local-suite/hms/embedded.py
- core/dataplane/hms_api/config_resolver.py
- core/dataplane/hms_api/tracing.py
- core/daemon/hms_embed/profile_manager.py
code_chars_analyzed: 192229
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
      <span class="scope-stat__value">39 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 192,229 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">interface/adapters/claude-code/requirements.txt</code></li><li><code class="path-chip">interface/adapters/dify/requirements.txt</code></li><li><code class="path-chip">interface/sdk/go/go.mod</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">core/dataplane-full/pyproject.toml</code></li><li><code class="path-chip">interface/adapters/cloudflare-oauth-proxy/package.json</code></li><li><code class="path-chip">core/local-suite-slim/README.md</code></li><li><code class="path-chip">core/local-suite/README.md</code></li><li><code class="path-chip">core/dataplane-full/README.md</code></li><li><code class="path-chip">core/dataplane/README.md</code></li><li><code class="path-chip">core/daemon/test.sh</code></li><li><code class="path-chip">core/daemon/README.md</code></li><li><code class="path-chip">core/dataplane/test_modular_search.py</code></li><li><code class="path-chip">interface/adapters/claude-code/tests/test_manifest.py</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI 智能体在跨会话长程记忆中难以整合时间、实体、事实等多种证据，导致回答不一致或虚构。HMS 通过检索后证据组织与账簿机制，将碎片化记忆转为可验证的结构化上下文。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">系统以 PostgreSQL+pgvector 为存储核心，模型层定义了 MemoryUnit（含 occurred_start/end、mentioned_at、fact_type 等）和 Entity/EntityCooccurrence/MemoryLink 等关系表（见 <code class="code-ref">core/dataplane/hms_api/models.py:119</code>-135 的索引与约束）。检索管道采用模块化设计，通过 retrieval_registry、fusion_registry 等实现语义/Bm25/图检索/时间检索的组合与 RRF 融合（<code class="code-ref">core/dataplane/hms_api/test_modular_search.py:102</code>-107 展示了策略接口分析）。使用 ConfigResolver 实现全局/租户/银行三级配置覆盖（<code class="code-ref">core/dataplane/hms_api/config_resolver.py:63</code>-67）。Daemon 模式通过 subprocess.Popen 而非 fork 实现跨平台后台启动，避免 macOS Metal/MPS 崩溃（<code class="code-ref">core/dataplane/hms_api/daemon.py:101</code>-108）。</p>
<p class="audit-callout audit-callout--highlight">模块化搜索管道支持运行时策略替换与自定义权重，test_modular_search.py 验证了核心组件的可组合性，体现了良好的扩展性。</p>
<p class="audit-callout audit-callout--highlight">内嵌客户端（<code class="code-ref">core/local-suite/hms/embedded.py:116</code>-130）具备 daemon 崩溃检测与自动重启机制，且在 cleanup 中通过锁和状态标记保证了线程安全与资源释放，提升了嵌入式场景的鲁棒性。</p>
<p class="audit-callout audit-callout--doubt">核心评测管线（ledger/self-evolution）的代码未在本次审计范围内（code_bundle 中未提供 lab/evaluation 等目录），无法验证 README 中声称的 LongMemEval 收益。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖偏薄，core/dataplane/tests/ 仅有少量单元测试（如 test_think.py:16-30 仅验证无上下文时的基本返回，test_mcp_server_version.py 仅测版本号），缺乏对时间推理、多轮内存整合的端到端测试。</p>
<p>若团队补全评测管线代码并增加集成测试，该项目有望成为 Agent 内存领域的实用底座。当前可谨慎用于小规模原型，但需自行评估证据组织在实际任务中的效果。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目创立仅 2 天，无生产案例或社区反馈，长期维护性未证实。</li><li>核心评测管线（ledger/self-evolution）源码未被审计，所声称的推理提升存疑。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为需要持久化结构化记忆的 Agent 应用（如客服、数据分析助手）提供开箱即用的后端，减少自研记忆系统的工程成本。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.15</span>
  </div>
</div>
</section>