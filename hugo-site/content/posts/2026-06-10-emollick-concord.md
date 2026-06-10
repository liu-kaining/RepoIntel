---
title: '[Score: 80.1] emollick/concord'
date: '2026-06-10T22:50:16Z'
categories:
- Qualitative Text Analysis Platform
tags:
- LLM-as-judge
- statistics
- content-analysis
- reproducibility
- Node.js
- DSPy-like
intel_score: 80.1
repo_name: emollick/concord
repo_link: https://github.com/emollick/concord
summary: 将 LLM 编码引入定性文本分析全流程，用哈希链审计日志、DSL/PPI 偏差校正和 Evidence Ladder 四级标记把 AI 标注变成可发表的统计数据，面向社科/UX
  研究者。
code_source: git
code_files_reviewed:
- package.json
- server/index.js
- server/router.js
- server/core/rng.js
- server/core/errors.js
- server/ingest/docx.js
- server/core/ids.js
- server/ingest/xlsx.js
- server/core/cache.js
- server/providers/costs.js
- server/routes/questionbar.js
- server/director/escalate.js
- server/director/analyst.js
- server/routes/catalog.js
- server/routes/brief.js
- server/providers/ollama.js
- server/ingest/text.js
- server/lexicons/LICENSES.md
- server/ingest/junk.js
- server/core/ledger.js
- server/providers/openrouter.js
- server/routes/projects.js
- server/ingest/mapping.js
- server/ingest/pdf.js
- server/routes/exports.js
- server/lexicons/starter-moral.json
- server/providers/registry.js
- server/routes/evidence.js
- server/director/panels.js
- server/lexicons/starter-work.json
- server/routes/settings.js
- server/providers/anthropic.js
- server/stats/boot.js
- server/ingest/csv.js
- server/ingest/transcript.js
- server/ingest/unitize.js
- server/instruments/stability.js
- server/routes/constructs.js
- server/director/constructs.js
- server/providers/mock.js
- server/lexicons/starter-emotions.json
- server/director/director.js
- server/instruments/panel.js
- server/stats/descriptives.js
- server/director/questionbar.js
- server/director/compiler.js
- server/stats/models.js
- server/stats/distributions.js
code_chars_analyzed: 264577
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
      <span class="scope-stat__value">约 264,577 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">server/index.js</code></li><li><code class="path-chip">server/router.js</code></li><li><code class="path-chip">server/core/rng.js</code></li><li><code class="path-chip">server/core/errors.js</code></li><li><code class="path-chip">server/ingest/docx.js</code></li><li><code class="path-chip">server/core/ids.js</code></li><li><code class="path-chip">server/ingest/xlsx.js</code></li><li><code class="path-chip">server/core/cache.js</code></li><li><code class="path-chip">server/providers/costs.js</code></li><li><code class="path-chip">server/routes/questionbar.js</code></li><li><code class="path-chip">server/director/escalate.js</code></li><li><code class="path-chip">server/director/analyst.js</code></li><li><code class="path-chip">server/routes/catalog.js</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>社科研究者手工编码开放式问卷/访谈文本动辄数百小时，LLM 辅助标注虽快但缺少校准、偏差校正和可复现审计链，导致审稿人无法信任 AI 生成的定量结论。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目以单进程 Node HTTP 服务器（<code class="code-ref">server/index.js</code>）为宿主，静态文件服务 + 纯手工路由（<code class="code-ref">server/router.js</code>）。核心数据流为：ingest（CSV/XLSX/PDF/DOCX/转录文件）→ unitize → Director（LLM）生成 codebook/简报 → compile instrument（judge/dictionary）→ run engine 执行编码 → 校准（silver/gold calibration）→ DSL/PPI 偏差校正 → 导出。每一步都通过 <code class="code-ref">server/core/ledger.js</code> 的哈希链审计日志记录（append-only ndjson，<code class="code-ref">sha256(prev + canonical(body))</code> 链式校验，<code class="code-ref">verify()</code> 可检测篡改），构成「Evidence Ladder」的可信度等级。</p>
<p class="audit-callout audit-callout--highlight">统计方法栈完整性远超一般 LLM 工具。<code class="code-ref">server/stats/distributions.js</code> 实现了从零开始的正态分位数（Acklam 近似 + Halley 精化）、不完全伽马函数、不完全 β 函数、χ²/t CDF，全部纯函数无外部依赖；<code class="code-ref">server/stats/boot.js</code> 实现单元重采样 bootstrap CI、McNemar 检验和 TOST 等价性检验；<code class="code-ref">server/stats/models.js</code> 实现 OLS 和 logistic 回归（IRLS + HC1 稳健标准误）。这些不是样板代码，而是可直接用于发表级统计推断的实现。</p>
<p class="audit-callout audit-callout--highlight">隐私模式强制在适配器构造层（<code class="code-ref">server/providers/registry.js:68</code> 的 <code class="code-ref">getAdapter</code>），strict 模式在 provider 对象被实例化前就抛出 PRIVACY_BLOCKED，且 override 需要书面 justification 并写入 ledger——这是罕见的将隐私合规内嵌到代码路径而非配置层的设计。</p>
<p class="audit-callout audit-callout--doubt">整个项目的 UI 层（<code class="code-ref">app/</code> 目录）未在 code_bundle 中提供，48 个文件中 247 个未审阅。前端工程质量和可维护性无法评估，Engineering 分数因此受限。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">server/ingest/csv.js</code> 的手写 CSV 解析器虽然注释详尽，但 CSV 是最复杂的文件格式之一——Ragged row 修复策略（<code class="code-ref">__extraN</code> 后缀）和单文件 header 推断（<code class="code-ref">looksLikeHeader</code>）在极端数据集（混合语言、嵌入 JSON）上的表现未见测试覆盖。<code class="code-ref">package.json</code> 中 <code class="code-ref">test</code> 脚本指向 <code class="code-ref">tests/**/*.test.js</code> 但 test 文件未包含在 bundle 中，无法确认覆盖率。</p>
<p>如需在生产中使用，（1）优先审计 <code class="code-ref">server/instruments/dictionary.js</code> 和 <code class="code-ref">server/instruments/judge.js</code>（均未在 bundle 中）的编码质量；（2）关注 DSL/PPI 校正模块（未审阅到）在小样本场景下的数值稳定性；（3）仓库仅 3 天历史、2 次 commit，建议等待上游 CI 绿灯和至少一轮社区反馈后再做关键依赖。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仓库仅 3 天、2 次 commit，核心 UI 层（app/）和大量服务器模块未在 bundle 中，稳定性/安全性远未验证。</li><li>DSL/PPI 校正和 gold calibration 模块代码未审阅，统计正确性无法独立确认；错误实现会导致发表论文的置信区间失真。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>如果 Evidence Ladder + DSL/PPI 校正链经受住同行评审验证，它有可能成为「AI 辅助定性分析」领域的引用标准——任何需要在论文中报告 LLM 编码 Kappa 和校正后比例的研究团队都是目标用户。商业路径可以是学术 SaaS 或嵌入 NVivo/Atlas.ti 等现有工具的插件。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">60</div>
  <div class="score-bar"><span style="width:60%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">80.1</span>
  </div>
</div>
</section>