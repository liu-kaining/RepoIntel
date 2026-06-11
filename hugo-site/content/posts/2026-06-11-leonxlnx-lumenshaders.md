---
title: '[Score: 78.05] Leonxlnx/lumenshaders'
date: '2026-06-11T20:18:34Z'
categories:
- Creative Coding / WebGL Art Tool
tags:
- WebGL2
- GLSL
- generative-art
- WebCodecs
- GIF-encoder
- zero-dependency
intel_score: 78.05
repo_name: Leonxlnx/lumenshaders
repo_link: https://github.com/Leonxlnx/lumenshaders
summary: 零依赖的浏览器端生成式着色器工作室，内置9种艺术模式+基因合成器、PNG/WebM/GIF导出与分享码，适合创意设计师快速产出可循环的抽象视觉素材。
code_source: git
code_files_reviewed:
- js/zip.js
- js/fx.js
- README.md
- js/palettes.js
- js/webmmux.js
- js/engine.js
- js/ui.js
- js/exporter.js
- js/gifenc.js
- js/modals.js
- js/shaders.js
- js/main.js
code_chars_analyzed: 116782
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
      <span class="scope-stat__value">12 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 116,782 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">js/zip.js</code></li><li><code class="path-chip">js/fx.js</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">js/palettes.js</code></li><li><code class="path-chip">js/webmmux.js</code></li><li><code class="path-chip">js/engine.js</code></li><li><code class="path-chip">js/ui.js</code></li><li><code class="path-chip">js/exporter.js</code></li><li><code class="path-chip">js/gifenc.js</code></li><li><code class="path-chip">js/modals.js</code></li><li><code class="path-chip">js/shaders.js</code></li><li><code class="path-chip">js/main.js</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>创意设计师需要高质量循环抽象视频/图片做网站 hero、社交媒体素材，但现有工具要么依赖 After Effects（贵且慢），要么在线生成器画质差、无法导出透明可控的视频；从参数到可分享链接的完整链路缺失。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 IIFE 模块单文件架构（无 bundler），全局对象 <code class="code-ref">Engine</code>、<code class="code-ref">GIFEnc</code>、<code class="code-ref">WebMMux</code>、<code class="code-ref">Exporter</code>、<code class="code-ref">UI</code>、<code class="code-ref">Modals</code>、<code class="code-ref">FX</code> 各司其职。核心渲染在 <code class="code-ref">js/engine.js</code> 通过单个 WebGL2 全屏三角形绘制 uber fragment shader（<code class="code-ref">js/shaders.js</code>），uniform 数组驱动 9 种艺术模式切换；动画循环由 <code class="code-ref">loopT</code> 时钟与 <code class="code-ref">u_phase</code> uniform 完成，相位在圆上采样确保数学级无缝循环（<code class="code-ref">js/shaders.js:33-34</code> 的 <code class="code-ref">LT()</code> 函数）。导出管线由 <code class="code-ref">js/exporter.js</code> 统一调度：PNG 走 offscreen resize + <code class="code-ref">toBlob</code>；Video 走 <code class="code-ref">VideoEncoder</code> + 自研 <code class="code-ref">WebMMux.mux</code>（<code class="code-ref">js/webmmux.js:84</code> 的 <code class="code-ref">mux</code> 函数手动组装 EBML 格式）；GIF 走自研 <code class="code-ref">GIFEnc.encode</code>（<code class="code-ref">js/gifenc.js:200</code>），含 median-cut 量化 + Bayer 有序抖动 + LZW 编码。分享码通过 base64 JSON 序列化全参数集（<code class="code-ref">js/main.js:260</code> 的 <code class="code-ref">encodeDesign</code>），支持 v1/v2/v3 三代格式兼容解码。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">js/gifenc.js:86</code> 的 <code class="code-ref">buildPalette</code> 从跨帧采样像素执行 median-cut 256色量化，并用 32768 条目 nearest-neighbor 缓存（<code class="code-ref">makeNearest</code>，行103）加速颜色映射，兼顾质量与性能，无需任何外部编码库。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">js/shaders.js:510</code> 的 <code class="code-ref">sceneGenome</code> 实现了 12 基因参数化风格合成器（场类型×域几何×色彩映射×光照×叠加），每组基因组合产生独立风格，配合 <code class="code-ref">js/main.js:214</code> 的 <code class="code-ref">generateGenomeStyle</code> 随机生成，实现了可扩展的「风格空间」探索，而非简单换皮。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">js/engine.js</code> 的 <code class="code-ref">readPixels</code>（行86）在 GIF 导出时逐帧调用 <code class="code-ref">gl.readPixels</code> 回传 CPU，高分辨率下帧数×像素量会导致显著内存压力，未见分块或 offscreen canvas 策略缓解。</p>
<p class="audit-callout audit-callout--doubt">code_bundle 中未提供 <code class="code-ref">js/shaders.js</code> 中的 <code class="code-ref">shaders.js</code> 完整 uber shader 与 <code class="code-ref">js/main.js</code> 中的 <code class="code-ref">REFRESH_ALL</code> 内部依赖 <code class="code-ref">ASPECTS</code>、<code class="code-ref">MODES</code> 等全局变量的完整解耦方案——全局 IIFE 模式下模块间通过隐式全局耦合，任何拼写错误都会静默失败，对后续维护者不友好。</p>
<p>若要在生产场景使用，建议将 GIF/Video 导出拆为 Web Worker 或 OffscreenCanvas 线程避免主线程阻塞；同时为关键全局对象增加防御性检查（如 <code class="code-ref">typeof Engine !== &#x27;undefined&#x27;</code>），降低因脚本加载顺序导致的静默失败风险。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 声称零依赖，但 WebCodecs API 在 Safari 中不支持，用户可能误认为全平台可用</li><li>仓库仅 1 天历史且无测试文件、无 CI 配置，核心 GLSL 和导出逻辑的正确性无法自动回归验证</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>零依赖、无需构建即可在浏览器生成高质量可循环视觉素材的设计工具，面向 Web 设计师和创意开发者的垂直场景有明确的差异化价值，可作为付费导出/高级风格包的 freemium 基础。</p>
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
  <div class="score-item__value">79</div>
  <div class="score-bar"><span style="width:79%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.05</span>
  </div>
</div>
</section>