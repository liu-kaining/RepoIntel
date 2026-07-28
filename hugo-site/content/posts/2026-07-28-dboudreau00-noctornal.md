---
title: '[Score: 83.05] dboudreau00/NocTORnal'
date: '2026-07-28T22:01:56Z'
categories:
- Cybercrime Investigation Platform
tags:
- graph-analysis
- evidence-management
- rbac
- ach
- python
- fastapi
- ontology
- provenance
intel_score: 83.05
repo_name: dboudreau00/NocTORnal
repo_link: https://github.com/dboudreau00/NocTORnal
summary: NocTORnal 是一个面向网络犯罪调查的图分析平台，用断言（assertion）保障每个图元素的来源可溯，集成证据管理、ACH 推理和四眼审批，专为执法和情报分析设计。
code_source: git
code_files_reviewed:
- db/requirements.txt
- packages/ontology/pyproject.toml
- apps/api/pyproject.toml
- infra/docker-compose.yml
- .github/workflows/ci.yml
- apps/api/src/noctornal_api/__init__.py
- apps/api/src/noctornal_api/security/__init__.py
- apps/api/src/noctornal_api/http/__init__.py
- packages/ontology/src/noctornal_ontology/__init__.py
- apps/api/src/noctornal_api/http/app.py
- packages/ontology/README.md
- apps/api/README.md
- apps/api/tests/test_envelope.py
- apps/api/tests/test_passwords.py
- packages/ontology/tests/test_db_parity.py
- apps/api/tests/test_totp.py
- apps/api/tests/test_sessions.py
- packages/ontology/tests/test_definition.py
- apps/api/tests/test_access.py
- apps/api/tests/test_script_invariants.py
- packages/ontology/generated/seed_ontology.sql
- packages/ontology/generated/ontology.ts
- apps/api/src/noctornal_api/db.py
- apps/api/src/noctornal_api/rawstore.py
- apps/api/src/noctornal_api/curation.py
- packages/ontology/src/noctornal_ontology/generate.py
- apps/api/src/noctornal_api/ratelimit_redis.py
- apps/api/src/noctornal_api/egress.py
- apps/api/src/noctornal_api/graph.py
- apps/api/src/noctornal_api/selectors.py
- apps/api/src/noctornal_api/notify_events.py
- apps/api/src/noctornal_api/cases.py
- apps/api/src/noctornal_api/stores.py
- apps/api/src/noctornal_api/coparticipation.py
- apps/api/src/noctornal_api/ach.py
- apps/api/src/noctornal_api/merges.py
- packages/ontology/src/noctornal_ontology/normalisers.py
- apps/api/src/noctornal_api/extraction.py
- apps/api/src/noctornal_api/analytics_runs.py
- apps/api/src/noctornal_api/break_glass.py
- apps/api/src/noctornal_api/proposals.py
- apps/api/src/noctornal_api/evidence.py
- packages/ontology/src/noctornal_ontology/definition.py
- apps/api/src/noctornal_api/transports.py
- apps/api/src/noctornal_api/approvals.py
- apps/api/src/noctornal_api/reports.py
- apps/api/src/noctornal_api/projections.py
code_chars_analyzed: 443180
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
      <span class="scope-stat__value">47 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 443,180 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">db/requirements.txt</code></li><li><code class="path-chip">packages/ontology/pyproject.toml</code></li><li><code class="path-chip">apps/api/pyproject.toml</code></li><li><code class="path-chip">infra/docker-compose.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">apps/api/src/noctornal_api/__init__.py</code></li><li><code class="path-chip">apps/api/src/noctornal_api/security/__init__.py</code></li><li><code class="path-chip">apps/api/src/noctornal_api/http/__init__.py</code></li><li><code class="path-chip">packages/ontology/src/noctornal_ontology/__init__.py</code></li><li><code class="path-chip">apps/api/src/noctornal_api/http/app.py</code></li><li><code class="path-chip">packages/ontology/README.md</code></li><li><code class="path-chip">apps/api/README.md</code></li><li><code class="path-chip">apps/api/tests/test_envelope.py</code></li><li><code class="path-chip">apps/api/tests/test_passwords.py</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>调查人员在分析犯罪社交网络时，需要将零散的通信证据、恶意软件样本和身份信息关联成可追溯的图表，同时必须确保每一环的证据链完整且操作合规，避免误合并或非授权泄露。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">FastAPI 应用 (<code class="code-ref">apps/api/src/noctornal_api/http/app.py</code>) 注册路由中间件，通过 stores.py 连接 Postgres，利用 ontology 包 (<code class="code-ref">packages/ontology/src/noctornal_ontology/definition.py</code>) 定义节点/边/选择器类型并自动生成 SQL 与 TypeScript 类型 (packages/ontology/generated/)。核心写路径由 graph.py 的 GraphWriteService 控制，每个 create_node/create_edge 在事务中强制写入附带来源、可靠性和置信度的断言 (<code class="code-ref">apps/api/src/noctornal_api/graph.py</code>: create_node)。证据模块 evidence.py 实现 WORM 存储、SHA256+BLAKE3 双重哈希及读取时完整性校验。社交图投影和 metrics 在 projections.py 中实现，出口控制统一经 egress.py 调用。人工审查流程通过 proposals.py 将机器提取的建议写入队列再经 ProposalReview.accept 创建图元素。</p>
<p class="audit-callout audit-callout--highlight">断言不可跳过——数据库级触发器确保图元素必有对应断言 (<code class="code-ref">apps/api/src/noctornal_api/graph.py</code>: create_node 中的 _insert_assertion)。所有写入路径都通过 GraphWriteService，杜绝了无来源的数据污染。</p>
<p class="audit-callout audit-callout--highlight">证据全生命周期管理——evidence.py 支持 WORM（MinIO + Compliance 锁定）、双重哈希验证、出口门禁与 custody 日志，为取证提供技术保障 (<code class="code-ref">apps/api/src/noctornal_api/evidence.py</code>: IngestResult / view / export)。</p>
<p class="audit-callout audit-callout--doubt">项目 README 明确标注“unaudited, never operated against real targets”，说明代码未经真实环境考验，可能存在未发现的缺陷 (README 首段警告)。</p>
<p class="audit-callout audit-callout--doubt">速率限制依赖 Redis，虽对 Redis 不可用有 fail-open/fail-closed 策略 (<code class="code-ref">apps/api/src/noctornal_api/ratelimit_redis.py</code>: BackendUnavailable 处理)，但部分关键限制如成本相关端点返回 503 时可能影响可用性，需额外监控。</p>
<p>必须完成法律和安全审计后才能用于生产，完善 CSRF 保护 (<code class="code-ref">apps/api/README.md</code> 中“Not yet done”)，并考虑 Redis 高可用方案。部署时需严格遵循 <code class="code-ref">docs/18-legal-review-pack.md</code> 设置策略。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目尚未经过第三方安全审计，源码中已自曝多个法律/合规阻塞点（如 README 中 L1-L5）；</li><li>CSRF 防护缺失且 WebSocket 依赖需显式安装，生产环境若配置不当可能导致功能降级或安全缺口。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可为执法部门或 CIRT 团队提供开源调查平台，替代部分昂贵的商业工具（如 Maltego + i2），但由于法律合规要求极高，商业化需要额外认证支持。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">83.05</span>
  </div>
</div>
</section>