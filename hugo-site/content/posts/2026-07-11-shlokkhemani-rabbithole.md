---
title: '[Score: 77.0] shlokkhemani/rabbithole'
date: '2026-07-11T10:12:13Z'
categories:
- AI-Powered Learning Canvas
tags:
- MCP
- Canvas
- Markdown
- IndexedDB
- PDF
- Agent
intel_score: 77.0
repo_name: shlokkhemani/rabbithole
repo_link: https://github.com/shlokkhemani/rabbithole
summary: 将 AI 答案转化为无限分支文档的画布式学习工具，支持 MCP 代理与本地浏览器两种模式。
code_source: git
code_files_reviewed:
- website/package.json
- package.json
- .github/workflows/ci.yml
- src/core/prompts/index.js
- src/node/index.js
- src/core/index.js
- src/web/brain/index.js
- workers/fetch-proxy/index.js
- src/node/logger.js
- src/core/utils.js
- src/node/sessions.js
- src/core/store.js
- src/core/snapshot-html.js
- src/core/snapshot-projection.js
- src/core/markdown.js
- src/ui/renderer.js
- src/ui/focus-trap.js
- src/ui/frozen-entry.js
- src/web/test-seam.js
- src/ui/chrome-init.js
- src/ui/entry.js
- src/core/assets.js
- src/ui/hydrate.js
- src/core/portable-projection.js
- src/core/generation-run.js
- src/core/portable-import.js
- src/ui/snapshot.js
- src/web/portable.js
- src/core/layout.js
- src/node/rabbithole.js
- src/ui/visuals.js
- src/core/schema.js
- src/core/pdf-shared.js
- src/core/model.js
- src/core/base-url.js
- src/ui/image-ux.js
- src/ui/palette.js
- src/core/reducer.js
- src/node/fs-store.js
- src/node/pdf-ingest.js
- src/ui/branch-surfaces.js
- src/ui/transport-status.js
- src/ui/ask-followups.js
- src/core/markdown-renderer.js
- src/ui/core.js
- src/ui/reader.js
- src/ui/canvas-view.js
- src/web/app.js
code_chars_analyzed: 358733
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
      <span class="scope-stat__value">约 358,733 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">website/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">src/core/prompts/index.js</code></li><li><code class="path-chip">src/node/index.js</code></li><li><code class="path-chip">src/core/index.js</code></li><li><code class="path-chip">src/web/brain/index.js</code></li><li><code class="path-chip">workers/fetch-proxy/index.js</code></li><li><code class="path-chip">src/node/logger.js</code></li><li><code class="path-chip">src/core/utils.js</code></li><li><code class="path-chip">src/node/sessions.js</code></li><li><code class="path-chip">src/core/store.js</code></li><li><code class="path-chip">src/core/snapshot-html.js</code></li><li><code class="path-chip">src/core/snapshot-projection.js</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在阅读长文档时，针对特定片段提问后难以组织答案脉络；传统聊天界面无法形成结构化的知识分支。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用分层设计，核心逻辑（reducer、模型、布局）集中在 <code class="code-ref">src/core/</code>，UI 打包为冻结客户端，服务端 <code class="code-ref">src/node/</code> 提供 MCP stdio 与文件存储。<code class="code-ref">src/core/reducer.js:27</code> 定义的 <code class="code-ref">createHoleState</code> 统一管理文档树状态，<code class="code-ref">reduceHoleEvent</code> 处理所有分支请求、流式进度和回答完成，形成可重放的事件循环。浏览器端通过 <code class="code-ref">src/ui/transport-status.js</code> 的 <code class="code-ref">handleServer</code> 处理 SSE 推送，将 <code class="code-ref">node_answered</code>、<code class="code-ref">node_progress</code> 等事件转为 UI 更新。画布布局由 <code class="code-ref">src/core/layout.js:89</code> 的 <code class="code-ref">placeChild</code> 根据分支类型自动排布，避免重叠。快照导出依赖 <code class="code-ref">src/core/snapshot-projection.js</code>，生成包含资源与状态的便携 HTML。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/core/reducer.js</code> 将分支请求、流式进度、回答完成统一为 <code class="code-ref">ReduceResult</code>，进度标记支持乱序/重连，避免因网络丢失导致状态混乱。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/core/markdown-renderer.js:120</code> 的 <code class="code-ref">buildExtensions</code> 向 Marked 注册了视觉占位符（<code class="code-ref">visualFencePending</code>）和数学区块渲染，配合 DOMPurify（见 <code class="code-ref">src/ui/visuals.js</code>）实现安全富文本。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/ui/canvas-view.js</code> 和 <code class="code-ref">src/web/app.js</code> 分别超过 35k 和 46k 行，包含大量直接 DOM 操作和全局状态耦合，增加维护和测试难度。</p>
<p class="audit-callout audit-callout--doubt">测试脚本虽定义 19 个阶段（<code class="code-ref">package.json</code>），但提供的代码包未包括任何测试实现文件，无法评估覆盖率和质量。</p>
<p>适合希望将 AI 对话转为结构化学习笔记的开发者。可优先体验 MCP 模式，结合 Claude Code 在本地文档上用。生产环境注意 IndexedDB 存储限制和大量节点时的布局性能。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>浏览器应用强制用户自带 API 密钥，非技术用户无法使用</li><li>项目仅诞生 5 天，维护者单一，长期演进存在不确定性</li><li>画布性能未在大量节点场景下验证，可能导致移动端卡顿</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可作为面向技术人群的付费学习工具，通过托管 API 代理降低使用门槛，并利用快照分享形成传播网络。</p>
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
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.0</span>
  </div>
</div>
</section>