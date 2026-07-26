---
title: '[Score: 87.85] nyblnet/bento'
date: '2026-07-26T08:33:17Z'
categories:
- Office Suite / Presentation Tool
tags:
- single-file
- powerpoint
- CRDT
- E2EE
- local-first
- HTML
intel_score: 87.85
repo_name: nyblnet/bento
repo_link: https://github.com/nyblnet/bento
summary: Bento 将幻灯片编辑器、查看器、协作与更新打包为单个 HTML 文件，无需安装或账户，适合本地优先、隐私敏感的演示文稿创建与共享。
code_source: git
code_files_reviewed:
- spaces/package.json
- slides/package.json
- .github/workflows/ci.yml
- server/sync-worker/wrangler.toml
- server/guestbook-daemon/wrangler.toml
- server/guestbook-daemon/README.md
- server/guestbook-daemon/src/worker.js
- server/sync-worker/src/worker.js
- slides/src/types.d.ts
- .github/ISSUE_TEMPLATE/config.yml
- slides/src/save.ts
- slides/src/charts.ts
- slides/src/update.ts
- slides/src/anim.ts
- .github/ISSUE_TEMPLATE/feature_request.md
- kernel/tsconfig.json
- slides/tsconfig.json
- spaces/tsconfig.json
- plugins/bento-slides/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- .github/ISSUE_TEMPLATE/bug_report.md
- .github/pull_request_template.md
- kernel/src/doc.ts
- slides/src/autosave.ts
- spaces/src/i18n.ts
- slides/vite.config.ts
- spaces/vite.config.ts
- docs/README.md
- kernel/src/app.ts
- kernel/README.md
- THIRD_PARTY_NOTICES.md
- .claude/launch.json
- slides/src/fonts.ts
- slides/src/i18n.ts
- spaces/README.md
- spaces/src/model.ts
- slides/src/screens.ts
- AGENTS.md
- slides/src/store.ts
- slides/src/editor/clipboard.ts
- SECURITY.md
- scripts/guestbook-archivist.ts
- CONTRIBUTING.md
- slides/src/editor/markdown.ts
- docs/PARALLEL-WORK.md
- slides/src/icons.ts
- kernel/src/autosave.ts
- slides/src/editor/bezier.ts
code_chars_analyzed: 142864
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
      <span class="scope-stat__value">约 142,864 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">spaces/package.json</code></li><li><code class="path-chip">slides/package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">server/sync-worker/wrangler.toml</code></li><li><code class="path-chip">server/guestbook-daemon/wrangler.toml</code></li><li><code class="path-chip">server/guestbook-daemon/README.md</code></li><li><code class="path-chip">server/guestbook-daemon/src/worker.js</code></li><li><code class="path-chip">server/sync-worker/src/worker.js</code></li><li><code class="path-chip">slides/src/types.d.ts</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">slides/src/save.ts</code></li><li><code class="path-chip">slides/src/charts.ts</code></li><li><code class="path-chip">slides/src/update.ts</code></li><li><code class="path-chip">slides/src/anim.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>传统演示文稿依赖云服务订阅，数据与软件分离，存在锁定、隐私风险和长期可访问性问题；Bento 将一切压缩进一个自包含文件，文件即软件，打开即用，并可离线编辑。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目通过 Vite 构建单文件（<code class="code-ref">slides/vite.config.ts:4</code>），使用 vite-plugin-singlefile 内联所有资源。文档模型在 JSON 块中，通过 splice 合约保持在文件头部（<code class="code-ref">kernel/src/doc.ts:9</code>）。状态管理由 <code class="code-ref">slides/src/store.ts</code> 的 Store 类中心化，支持撤销/重做（JSON 快照）。协作层使用自研 CRDT（<code class="code-ref">sync/crdt.ts</code>），配合盲中继 relay（<code class="code-ref">server/sync-worker/src/worker.js:22</code>-45）实现 E2EE。中继仅转发密文，信令通道通过 WebSocket，密钥仅存于文件中。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">server/sync-worker/src/worker.js:72</code> 定义 MAX_FRAME 1.9MB 防止超大帧，并附带速率限制（RATE_BURST 200 帧/窗口），签名房间强制 ECDSA 验证（<code class="code-ref">server/sync-worker/src/worker.js:164</code>-168），确保写入者权限不可伪造。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">.github/workflows/ci.yml:55</code> 运行 CRDT 收敛测试，执行 SEEDS=300 的模糊测试，覆盖数十万次状态合并，显著降低合并冲突类 bug。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">slides/src/store.ts:94</code>-98 的 undo 基于 JSON 序列化/反序列化整篇文档，大文件可能造成性能瓶颈，且协同编辑时快照式撤销可能回滚协作者并发修改（README 已声明）。</p>
<p class="audit-callout audit-callout--doubt">未审阅到核心渲染引擎 render.ts 与协作光标/存在性实现，无法评估 DOM 更新性能与多端同步的细腻度。</p>
<p>立即试用无需部署，下载 Bento_Slides.bento.html 即可；如需协作，需自建 sync-worker（依赖 Cloudflare Durable Objects），建议小团队内验证后再开放使用。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>单文件模型在超大演示文稿（数百 MB）时可能引发浏览器内存压力，且自保存接口在非 Chromium 浏览器只有下载回退。</li><li>文件即软件的特性意味着共享 .bento.html 文件等同于执行任意代码，用户需警惕来源。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>降低演示文稿创建与共享的技术门槛，以本地优先和强隐私吸引个体用户及团队，并为 AI 代理直接编辑文档提供天然接口，有潜力成为新一代文档格式的候选者。</p>
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
  <div class="score-item__value">92</div>
  <div class="score-bar"><span style="width:92%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">90</div>
  <div class="score-bar"><span style="width:90%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">87.85</span>
  </div>
</div>
</section>