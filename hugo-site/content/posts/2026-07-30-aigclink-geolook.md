---
title: '[Score: 76.9] aigclink/geolook'
date: '2026-07-30T22:03:21Z'
categories:
- AI Search Optimization
tags:
- GEO
- LLM sampling
- automated verification
- self-hosted
- Python
intel_score: 76.9
repo_name: aigclink/geolook
repo_link: https://github.com/aigclink/geolook
summary: 一个自托管的生成式引擎优化（GEO）实施平台，提供从网站抓取、6维审计、跨引擎采样到自动验收工单的全流程闭环，主要面向期望提升品牌在AI搜索中提及率的营销团队。
code_source: git
code_files_reviewed:
- tests/test_ui.py
- tests/test_geolib.py
- tests/test_crawl.py
- tests/test_report.py
- tests/test_tasks.py
- scripts/benchmark.py
- tests/test_jobs.py
- references/global-platforms.md
- references/sources.md
- tests/test_model_config.py
- references/content-patterns.md
- tests/test_deliver.py
- tests/test_bootstrap.py
- tests/test_sample.py
- references/cn-platforms.md
- tests/test_analytics.py
- references/method.md
- references/cn-source-ranking.md
- tests/test_audit.py
- scripts/jobs.py
- scripts/crawl.py
- scripts/publish.py
- scripts/verify.py
- scripts/geolib.py
- scripts/expand.py
- scripts/audit.py
- README.md
- scripts/bootstrap.py
- README.zh-CN.md
- SKILL.md
- scripts/deliverables.py
- README.ja.md
- scripts/blueprint.py
- scripts/report.py
- scripts/analytics.py
- scripts/tasks.py
- scripts/geo.py
- scripts/deliver.py
- scripts/generate.py
- scripts/dashboard.py
- scripts/sample.py
code_chars_analyzed: 385088
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
      <span class="scope-stat__value">41 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 385,088 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">tests/test_ui.py</code></li><li><code class="path-chip">tests/test_geolib.py</code></li><li><code class="path-chip">tests/test_crawl.py</code></li><li><code class="path-chip">tests/test_report.py</code></li><li><code class="path-chip">tests/test_tasks.py</code></li><li><code class="path-chip">scripts/benchmark.py</code></li><li><code class="path-chip">tests/test_jobs.py</code></li><li><code class="path-chip">references/global-platforms.md</code></li><li><code class="path-chip">references/sources.md</code></li><li><code class="path-chip">tests/test_model_config.py</code></li><li><code class="path-chip">references/content-patterns.md</code></li><li><code class="path-chip">tests/test_deliver.py</code></li><li><code class="path-chip">tests/test_bootstrap.py</code></li><li><code class="path-chip">tests/test_sample.py</code></li><li class="path-more">另有 27 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>品牌在AI搜索问答中不被提及或引用，缺乏可量化的诊断和可落地、可验证的执行方案，手动监控成本高且难以形成持续改进循环。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用模块化Python脚本串联GEO工作流：<code class="code-ref">scripts/geo.py</code> 为CLI入口，分发到各子模块（<code class="code-ref">crawl.py</code>、<code class="code-ref">audit.py</code>、<code class="code-ref">sample.py</code>、<code class="code-ref">tasks.py</code>、<code class="code-ref">generate.py</code>、<code class="code-ref">verify.py</code>、<code class="code-ref">deliver.py</code>）。核心链路为：crawl → audit（6维评分，<code class="code-ref">scripts/audit.py: score_page</code>实现抽取块识别、字数/结构/权威评分）→ sample（<code class="code-ref">scripts/sample.py: run</code>并发调用多个AI引擎API，含重试与降级）→ plan（从audit/metrics生成带验收标准的工单，<code class="code-ref">scripts/tasks.py: from_audit/from_metrics</code>）→ generate（产出llms.txt、JSON-LD、内容大纲等资产）→ verify（<code class="code-ref">scripts/verify.py: check</code>自动判定工单完成，回归自动重开）→ deliver（打包交付包）。后台任务由<code class="code-ref">scripts/jobs.py</code>管理，通过子进程隔离，支持孤儿进程回收（<code class="code-ref">reap_orphans</code>）。前端单页应用通过标准库HTTP服务提供，数据存储为本地JSON/MD文件。</p>
<p class="audit-callout audit-callout--highlight">自动验收闭环的checker引擎（<code class="code-ref">scripts/verify.py: check</code>）支持十几种确定性检查（如site.no_ai_bot_block、pages.block:定义、metrics.mention_rate_gte），并且工单状态变更时自动备份（<code class="code-ref">tasks.py: save</code>备份到.geo.bak）。验收不仅依赖采样，还通过重抓站点获取确定性信号，回归可自动打回。</p>
<p class="audit-callout audit-callout--highlight">多引擎采样的健壮性设计（<code class="code-ref">scripts/sample.py: ask</code>对超时/429/5xx重试，Ark/Anthropic等协议分别实现，并通过<code class="code-ref">ThreadPoolExecutor</code>并发多平台，平台内串行避免限流，结果增量落盘防中断丢失）。对无API平台有手动采样表导入导出机制。</p>
<p class="audit-callout audit-callout--doubt">站点抓取虽按host分组并发（<code class="code-ref">scripts/crawl.py: crawl_group</code>），但组内完全串行且固定延迟0.5s，面对大型站点可能过慢；且健康检查<code class="code-ref">check_crawl_health</code>仅判断全灭或低可用率即SystemExit，无法优雅降级。</p>
<p class="audit-callout audit-callout--doubt">工单系统<code class="code-ref">tasks.py: from_audit</code>等生成逻辑将多个页面级问题聚合成单条工单，但<code class="code-ref">affected</code>列表截断至30条（<code class="code-ref">t[&#x27;affected&#x27;] = miss[:30]</code>），实际验收基线却用完整数量（<code class="code-ref">baseline_count = len(miss)</code>），可能导致前端展示与验收逻辑不一致。</p>
<p>作为单机工具，适合个人或小团队；若用于多人协作，需自行添加认证层（README明确建议反代）。建议利用<code class="code-ref">verify</code>模块将关键工单验收自动化，但手动核实的标的仍需人工兜底。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅创建1天，尚未经历长期维护考验，需关注持续更新和社区贡献的可持续性</li><li>依赖大量外部AI API密钥，若采样策略不当可能产生高额费用，且部分引擎联网功能需单独申请开通（如豆包内容插件）</li><li>README中明确服务只绑定127.0.0.1，无内置认证，远程部署需额外配置反向代理，存在误将端口暴露的风险</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为GEO顾问和代理机构提供了可交付的标准化服务包，可替代昂贵的SaaS监测工具，降低客户获取成本；自托管特性使数据主权回归客户，适合对数据隐私敏感的企业。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.9</span>
  </div>
</div>
</section>