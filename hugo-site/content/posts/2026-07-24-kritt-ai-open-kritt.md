---
title: '[Score: 79.8] Kritt-ai/open-kritt'
date: '2026-07-24T13:38:02Z'
categories:
- AI-Powered Security Testing
tags:
- security
- bug-bounty
- agents
- workflow
- vulnerability
- self-hosted
intel_score: 79.8
repo_name: Kritt-ai/open-kritt
repo_link: https://github.com/Kritt-ai/open-kritt
summary: open·kritt 是一个自托管的 AI 安全研究平台，通过可编排的代理工作流对代码进行并行漏洞扫描、验证与去重排序，面向安全研究员与开发者。
code_source: git
code_files_reviewed:
- engine/requirements.txt
- executor-view/Dockerfile
- frontend/Dockerfile
- docs-site/package.json
- database/Dockerfile
- backend/Dockerfile
- .github/workflows/release.yml
- .github/workflows/ci.yml
- engine/open_kritt_engine/__init__.py
- backend/test/seedSafety.test.js
- backend/test/migrationSafety.test.js
- backend/test/agentSkillSeed.test.js
- backend/test/scanPagination.test.js
- backend/test/templateRefs.test.js
- backend/test/defaultSeverityRankers.test.js
- backend/test/cors.test.js
- backend/test/defaultWorkflows.test.js
- .release-please-manifest.json
- engine/open_kritt_engine/__main__.py
- .prettierrc.json
- docker-compose.dev.yml
- backend/src/lib/scanLocks.js
- database/init/006_add_stub_explanation.sql
- database/init/023_scan_activity_sort.sql
- scripts/logs-pretty.sh
- database/init/003_add_scan_extras.sql
- database/init/011_metadata_phase.sql
- database/init/007_make_scan_config_legacy.sql
- backend/src/lib/workflowLocks.js
- backend/src/lib/logger.js
- backend/src/lib/agentSkillLocks.js
- backend/src/lib/postScriptLocks.js
- backend/src/routes/modelProviders.js
- database/init/012_codex_account_attribution.sql
- database/init/006_consume_all_previous.sql
- database/init/020_expand_thinking_efforts.sql
- database/init/017_model_catalogs.sql
- database/init/019_restore_legacy_compat_columns.sql
- backend/src/db.js
- .github/ISSUE_TEMPLATE/config.yml
- backend/src/routes/settings.js
- database/init/005_repo_kind.sql
- frontend/src/pages/VulnerabilityPage.test.js
- frontend/src/main.jsx
- database/init/016_scan_model_provider.sql
- database/init/025_scan_model_overrides.sql
- frontend/src/lib/scanExtras.js
- database/init/005_remove_step_stub_columns.sql
code_chars_analyzed: 30001
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
      <span class="scope-stat__value">约 30,001 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">engine/requirements.txt</code></li><li><code class="path-chip">executor-view/Dockerfile</code></li><li><code class="path-chip">frontend/Dockerfile</code></li><li><code class="path-chip">docs-site/package.json</code></li><li><code class="path-chip">database/Dockerfile</code></li><li><code class="path-chip">backend/Dockerfile</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">engine/open_kritt_engine/__init__.py</code></li><li><code class="path-chip">backend/test/seedSafety.test.js</code></li><li><code class="path-chip">backend/test/migrationSafety.test.js</code></li><li><code class="path-chip">backend/test/agentSkillSeed.test.js</code></li><li><code class="path-chip">backend/test/scanPagination.test.js</code></li><li><code class="path-chip">backend/test/templateRefs.test.js</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>安全研究员在审计代码库时，直接让大模型全量扫描漏洞效果差且结果混乱；open·kritt 将复杂分析拆解为可串并行、可验证的小任务，输出结构化、去重且可定级的安全发现。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">系统基于 Docker Compose 运行，由前端 (Vite)、后端 (Express/Prisma)、引擎 (Python worker) 和数据库 (PostgreSQL) 组成。用户通过前端构建工作流，后端 <code class="code-ref">/api/scans</code> 创建扫描记录并提交任务给引擎。<code class="code-ref">backend/Dockerfile</code> 中预装了 Codex 和 Claude Code CLI，引擎通过 worker 调度代理执行步骤。数据库迁移 (<code class="code-ref">database/init/</code>) 逐步添加了扫描模型重写 (<code class="code-ref">025_scan_model_overrides.sql</code>)、模型目录 (<code class="code-ref">017_model_catalogs.sql</code>) 等特性。</p>
<p class="audit-callout audit-callout--highlight">工作流引擎支持多层级、多输出、聚合模式 (<code class="code-ref">database/init/006_consume_all_previous.sql</code>)，可定义深度、是否并行输出，并使用 <code class="code-ref">FOR UPDATE/SHARE</code> 锁 (<code class="code-ref">backend/src/lib/workflowLocks.js</code>) 保证并发安全。</p>
<p class="audit-callout audit-callout--highlight">内置两个默认工作流已通过测试验证 (<code class="code-ref">backend/test/defaultWorkflows.test.js</code>)，如 Cosmos ABCI 恐慌审查工作流，步骤精细到具体漏洞类型，展示平台对领域知识的整合。</p>
<p class="audit-callout audit-callout--doubt">引擎测试被部分禁用 (<code class="code-ref">engine</code> CI 配置中 <code class="code-ref">pytest</code> 行被注释)，导致核心 Python worker 的单元测试未被验证，生产可靠性存疑。</p>
<p class="audit-callout audit-callout--doubt">默认 CORS 设为 <code class="code-ref">origin: false</code> (<code class="code-ref">backend/test/cors.test.js</code>)，安全但需用户手动配置 <code class="code-ref">BACKEND_CORS_ORIGINS</code>，且 README 提示后端无应用内认证，风险较大（<code class="code-ref">backend/Dockerfile</code> 未包含认证中间件）。</p>
<p>适用于安全团队自建自动化漏洞挖掘流水线，或在 bug bounty 场景下加速目标分析。需关注代理容器的权限隔离和算力成本。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅 3 天仓库历史，维护者未知长期投入，社区尚处极早期</li><li>引擎测试被忽略 (<code class="code-ref">engine</code> CI 0 tests)，核心稳定性未经验证</li><li>要求容器以 root 运行且有网络访问，未配置认证，仅适合隔离环境</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>源自 Bug Bounty 团队 $1.5M 实战经验，以 AGPL-3.0 开源，可降低安全审计工具链的门槛，并可能围绕企业版或云服务形成商业模式。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.8</span>
  </div>
</div>
</section>