---
title: '[Score: 81.4] penecho/penecho'
date: '2026-07-25T02:24:22Z'
categories:
- AI Canvas Interface
tags:
- canvas
- ai
- handwriting
- spatial-reasoning
- plugin-system
- nodejs
intel_score: 81.4
repo_name: penecho/penecho
repo_link: https://github.com/penecho/penecho
summary: PenEcho 将手写、公式、图表与 AI 对话融合在共享画布上，让视觉化思考成为对话的一部分。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- public/mathjax-config.js
- .github/PULL_REQUEST_TEMPLATE.md
- COMMERCIAL-LICENSE.md
- test/api-config.test.js
- TRADEMARKS.md
- public/plugins/earthquakes.md
- public/plugins/space-weather.md
- api-config.js
- public/plugins/exchange-rates.md
- public/plugins/natural-events.md
- public/plugins/tech-news.md
- public/plugins/general.md
- public/plugins/github-pulse.md
- public/plugins/stocks.md
- CONTRIBUTING.md
- CONTRIBUTOR-LICENSE-AGREEMENT.md
- typeset.js
- public/plugins/weather.md
- test/selection-ui.test.js
- test/mixed-text.test.js
- test/typeset.test.js
- test/animation.test.js
- public/plugins.js
- test/selection.test.js
- test/tour.test.js
- test/draw.test.js
- test/configure-ui.test.js
- test/update.test.js
- public/tour.js
- README.zh-CN.md
- README.pt-BR.md
- README.es.md
- update.js
- public/selection.js
- README.de.md
- README.ko.md
- README.fr.md
- README.ja.md
- test/tour-ui.test.js
- README.ru.md
- public/mixed-text.js
- test/claude-cli.test.js
- test/codex-cli.test.js
- test/plugin.test.js
- claude-cli.js
- public/draw.js
code_chars_analyzed: 252255
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
      <span class="scope-stat__value">约 252,255 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">public/mathjax-config.js</code></li><li><code class="path-chip">.github/PULL_REQUEST_TEMPLATE.md</code></li><li><code class="path-chip">COMMERCIAL-LICENSE.md</code></li><li><code class="path-chip">test/api-config.test.js</code></li><li><code class="path-chip">TRADEMARKS.md</code></li><li><code class="path-chip">public/plugins/earthquakes.md</code></li><li><code class="path-chip">public/plugins/space-weather.md</code></li><li><code class="path-chip">api-config.js</code></li><li><code class="path-chip">public/plugins/exchange-rates.md</code></li><li><code class="path-chip">public/plugins/natural-events.md</code></li><li><code class="path-chip">public/plugins/tech-news.md</code></li><li><code class="path-chip">public/plugins/general.md</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>传统 AI 聊天框缺乏空间上下文，数学推导、手绘草图难以直接交互；PenEcho 通过画布捕捉笔迹和位置，让 AI 就地回应，适用于教学、科研、设计等场景。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Node.js 服务端（server.js，未审阅到完整源码）接收浏览器发送的画布区域图像，通过 Claude CLI、Codex CLI 或 OpenAI/Anthropic API 调用大模型，返回结构化绘图/文字指令；前端利用 draw.js、selection.js 等模块在 Canvas 上渲染。插件系统通过 <code class="code-ref">public/plugins.js</code> 解析 Markdown 定义，生成沙箱 iframe 展示实时数据（如天气、股票）。</p>
<p class="audit-callout audit-callout--highlight">插件安全边界：<code class="code-ref">public/plugins.js</code> 的 <code class="code-ref">exactHttpsOrigin</code> 函数强制要求 connect 来源为不含用户信息的精确 HTTPS 域名，<code class="code-ref">parse</code> 函数限制单个插件文档 ≤3000 字节，且 widget-host.js 仅允许 <code class="code-ref">allow-scripts</code> 权限（不含 allow-same-origin），从源头堵死越权访问。</p>
<p class="audit-callout audit-callout--highlight">AI 输出校验：<code class="code-ref">public/draw.js</code> 的 <code class="code-ref">normalize</code> 函数对模型返回的绘图指令执行严密整数校验、画布边界裁剪、最多 64 个图元等限制，任何越界或非法数据均直接拒绝，防止恶意或错误输出引发崩溃。</p>
<p class="audit-callout audit-callout--doubt">核心服务端 server.js 未在源码包中提供，虽然测试代码（<code class="code-ref">test/typeset.test.js</code>）侧面透露其对 normalize 动作的特殊过滤逻辑，但无法审计路由、超时、错误传播等关键路径，存在审计盲区。</p>
<p class="audit-callout audit-callout--doubt">插件文档大小限制 3000 字节（<code class="code-ref">public/plugins.js</code>: <code class="code-ref">MAX_DOCUMENT_BYTES = 3000</code>）对复杂定制可能偏紧，且强制要求不包含 HTML 模板（测试中 <code class="code-ref">doesNotMatch(parsed.document, /</code>`<code class="code-ref">html/i)</code>），完全依赖模型生成完整 HTML，存在输出质量不可控的风险。</p>
<p>基于当前高质量模块化代码和全面测试（覆盖 draw、selection、animation、插件、CLI 适配器等），建议补充服务端集成测试并公开 server.js 源码；插件系统可考虑允许更大的文档预算或可选模板，平衡灵活性与安全性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目初期仅 1 次提交，长期维护和社区治理能力待观察</li><li>依赖外部 CLI 工具（Claude/Codex），其版本升级可能导致兼容问题</li><li>AGPL 要求网络分发时提供源码，可能限制企业云服务采用</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 AGPL-3.0 项目可提供商业许可，对需要视觉化 AI 交互的教育、研究、设计工具市场有吸引力，插件生态有望发展为轻量级数据仪表板平台。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">81.4</span>
  </div>
</div>
</section>