---
title: '[Score: 78.6] krishagarwal314/CodeJury'
date: '2026-07-30T13:52:21Z'
categories:
- AI Agent Pipelines
tags:
- code-generation
- code-review
- multi-agent
- llm-ensemble
- rag
- cli
intel_score: 78.6
repo_name: krishagarwal314/CodeJury
repo_link: https://github.com/krishagarwal314/CodeJury
summary: 终端优先的多Agent软件交付管道，用不同模型组成的评审团替代单模型审查，并通过持久化代码图谱和语义搜索定位改动位置。
code_source: git
code_files_reviewed:
- backend/requirements.txt
- docker-compose.yml
- Dockerfile
- pyproject.toml
- .github/workflows/ci.yml
- backend/app/cli/__init__.py
- backend/app/core/__init__.py
- backend/app/cli/panels/__init__.py
- backend/app/services/knowledge/__init__.py
- backend/app/main.py
- backend/app/services/agent_backends/__init__.py
- .github/ISSUE_TEMPLATE/config.yml
- .github/ISSUE_TEMPLATE/feature_request.md
- backend/app/routers/costs.py
- .github/pull_request_template.md
- .github/ISSUE_TEMPLATE/bug_report.md
- backend/app/services/knowledge/facts_view.py
- benchmarks/data/pipeline-task-a.json
- backend/app/services/background.py
- benchmarks/data/pipeline-task-b.json
- backend/app/core/errors.py
- backend/app/services/agent_backends/antigravity.py
- tests/test_crypto.py
- benchmarks/data/retrieval-ablation-rich.json
- backend/app/routers/kb_tools.py
- backend/app/services/agent_backends/claude_code.py
- backend/app/services/llm.py
- tests/test_unapproved_delivery.py
- backend/app/schemas.py
- SECURITY.md
- backend/app/routers/repos.py
- benchmarks/data/baseline-task-b.json
- CONTRIBUTING.md
- benchmarks/data/click-pipeline-task-a.json
- benchmarks/data/baseline-task-a.json
- backend/app/services/knowledge/facts.py
- benchmarks/data/exp3-baseline-b.json
- benchmarks/data/exp4-baseline-a.json
- tests/conftest.py
- CODE_OF_CONDUCT.md
- backend/app/services/jira.py
- backend/app/database.py
- benchmarks/data/exp4-baseline-e.json
- backend/app/cli/serve.py
- benchmarks/data/exp2-baseline-b.json
code_chars_analyzed: 76893
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
      <span class="scope-stat__value">45 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 76,893 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">backend/requirements.txt</code></li><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">backend/app/cli/__init__.py</code></li><li><code class="path-chip">backend/app/core/__init__.py</code></li><li><code class="path-chip">backend/app/cli/panels/__init__.py</code></li><li><code class="path-chip">backend/app/services/knowledge/__init__.py</code></li><li><code class="path-chip">backend/app/main.py</code></li><li><code class="path-chip">backend/app/services/agent_backends/__init__.py</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/feature_request.md</code></li><li><code class="path-chip">backend/app/routers/costs.py</code></li><li class="path-more">另有 31 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>单一LLM审查代码时置信度虚高，对补丁正确性的判断近乎抛硬币，且每次都重新发现仓库结构，浪费上下文。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">系统通过FastAPI和Textual终端双入口（<code class="code-ref">backend/app/cli/__init__.py</code>→<code class="code-ref">backend/app/cli/entry</code>）驱动，核心用例层<code class="code-ref">core</code>无界面依赖。管道分为知识生成、PM规划、Dev执行、QA测试、Review评审五阶段，由<code class="code-ref">agent_backends</code>统一调度（<code class="code-ref">backend/app/services/agent_backends/__init__.py:36</code>的<code class="code-ref">run()</code>对后端错误采用fail-open，不中断scope运行）。评审阶段将代码分发给多个独立Judge（<code class="code-ref">backend/app/main.py:41</code>处<code class="code-ref">judges.ensure_seeded</code>初始化陪审团），合成裁决后决定PR是否通过。知识底座由外部<code class="code-ref">codebase-memory-mcp</code>构建代码图，降级时回退到符号映射（<code class="code-ref">backend/app/services/knowledge/__init__.py</code>）。</p>
<p class="audit-callout audit-callout--highlight">Fail-open的Agent调度设计（<code class="code-ref">backend/app/services/agent_backends/__init__.py:36-44</code>）：任何后端失败都转化为错误结果而非异常，使管道在部分工具不可用时仍能吐出部分结果，避免整个scope失败。</p>
<p class="audit-callout audit-callout--highlight">测试隔离的工程实践（<code class="code-ref">tests/conftest.py:15-25</code>）：使用临时目录、固定密钥、禁止网络调用，确保每个测试运行在干净的SQLite环境，且<code class="code-ref">conftest.py:61-64</code>提供预认证的TestClient，降低了集成测试的编写成本。</p>
<p class="audit-callout audit-callout--doubt">陪审团裁决合成逻辑未审阅到（<code class="code-ref">backend/app/routers/jury</code>和<code class="code-ref">backend/app/services/judges</code>未包含在源码包中），无法判断投票机制是否可靠及如何处理悬置票，这是整个产品核心差异点的盲区。</p>
<p class="audit-callout audit-callout--doubt">知识图谱的外部依赖<code class="code-ref">codebase-memory-mcp</code>的降级路径仅见于文档描述（<code class="code-ref">backend/requirements.txt:6-7</code>），具体降级代码（如<code class="code-ref">graph.py</code>中的条件分支）未提供，一旦二进制缺失，检索准确度的损失缺乏量化保证。</p>
<p>适合维护中大型代码库、希望用自动化审查减少机械性检视的团队；部署前需准备至少两种LLM提供方的key，并在CI中验证<code class="code-ref">codebase-memory-mcp</code>二进制可用或接受降级后的召回率下降。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖多个外部agent CLI（如Claude Code、Codex），这些工具的版本更新可能破坏管道。</li><li>核心代码图引擎的外部二进制未内置，若未安装则检索精度立降至bm25，影响定位准确性。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>开源MIT许可，可嵌入CI/CD实现代码评审的multi-agent把关，节省人工review耗时，尤其针对逻辑缺陷有高于单模型的召回提升，长期可形成企业内部的代码质量护栏。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.6</span>
  </div>
</div>
</section>