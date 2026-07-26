---
title: '[Score: 76.75] DavidHDev/canvas-ui'
date: '2026-07-26T19:05:53Z'
categories:
- UI Component Library
tags:
- canvas
- webgl
- html-in-canvas
- shadcn-registry
- creative-coding
intel_score: 76.75
repo_name: DavidHDev/canvas-ui
repo_link: https://github.com/DavidHDev/canvas-ui
summary: 一个基于实验性 HTML-in-canvas API 的创意组件库，可为 React/Vue/Svelte 等框架提供流体、火焰、破碎等 WebGL
  效果，并保持原生 DOM 交互性。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- src/lib/github.ts
- src/lib/utils.ts
- src/app/robots.ts
- src/hooks/use-theme-toggle.ts
- src/app/not-found.tsx
- src/hooks/use-preference.ts
- src/demos/glitch-demo.tsx
- src/demos/particle-scroll-demo.tsx
- src/app/page.tsx
- src/demos/ripple-demo.tsx
- src/app/sitemap.ts
- src/demos/vhs-demo.tsx
- src/demos/bend-demo.tsx
- src/demos/glass-demo.tsx
- src/demos/blaze-demo.tsx
- src/demos/laser-demo.tsx
- src/demos/asciify-demo.tsx
- src/demos/retro-dither-demo.tsx
- src/demos/bubble-demo.tsx
- src/demos/droplets-demo.tsx
- src/demos/clouds-demo.tsx
- src/demos/grid-demo.tsx
- src/app/layout.tsx
- src/demos/hex-float-demo.tsx
- src/demos/frost-demo.tsx
- src/demos/liquid-demo.tsx
- src/demos/demo-image-cycler.tsx
- src/demos/magnify-demo.tsx
- src/demos/shatter-demo.tsx
- src/demos/cloth-demo.tsx
- src/hooks/use-demo-controls.ts
- src/demos/particle-reveal-demo.tsx
- src/data/components.ts
- src/demos/dithered-object-demo.tsx
- src/demos/particle-object-demo.tsx
- src/demos/glass-object-demo.tsx
- src/demos/peel-demo.tsx
- src/lib/registry.ts
- src/components/common/theme-provider.tsx
- src/components/ui/label.tsx
- src/components/ui/separator.tsx
- src/components/landing/stitches.tsx
- src/components/common/theme-favicon.tsx
- src/components/ui/textarea.tsx
- src/components/common/theme-hotkey.tsx
- src/app/playground/page.tsx
code_chars_analyzed: 131929
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
      <span class="scope-stat__value">约 131,929 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">src/lib/github.ts</code></li><li><code class="path-chip">src/lib/utils.ts</code></li><li><code class="path-chip">src/app/robots.ts</code></li><li><code class="path-chip">src/hooks/use-theme-toggle.ts</code></li><li><code class="path-chip">src/app/not-found.tsx</code></li><li><code class="path-chip">src/hooks/use-preference.ts</code></li><li><code class="path-chip">src/demos/glitch-demo.tsx</code></li><li><code class="path-chip">src/demos/particle-scroll-demo.tsx</code></li><li><code class="path-chip">src/app/page.tsx</code></li><li><code class="path-chip">src/demos/ripple-demo.tsx</code></li><li><code class="path-chip">src/app/sitemap.ts</code></li><li><code class="path-chip">src/demos/vhs-demo.tsx</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>前端开发者想在页面上实现高级视觉特效（如流体、玻璃折射）时，通常需要深度定制 WebGL 且难以与现有 DOM 交互；Canvas UI 将效果封装为可直接复制使用的组件，节省集成成本。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用分层设计：每个组件目录（如 <code class="code-ref">src/lib/Glitch</code>）包含一个 Vanilla 引擎实现（TypeScript）和针对 React、Vue、Svelte 等框架的轻量包装器。<code class="code-ref">src/lib/registry.ts</code> 中的 <code class="code-ref">makeStandalone</code> 函数将引擎代码内联到框架包装器中，生成 shadcn 兼容的 registry 文件。文档站点为 Next.js，展示页通过 <code class="code-ref">src/demos/*-demo.tsx</code> 加载组件，并利用 <code class="code-ref">useDemoControls</code> hook（<code class="code-ref">src/hooks/use-demo-controls.ts</code>）将参数同步到 URL，实现可分享的实时调参面板。</p>
<p class="audit-callout audit-callout--highlight">多框架支持策略简洁高效。<code class="code-ref">src/lib/registry.ts:159-180</code> 的 <code class="code-ref">makeStandalone</code> 函数通过正则替换将 vanilla 引擎直接内联到 React/Vue/Svelte 等包装代码中，避免了为每个框架重复实现核心逻辑，且引擎文件独立维护。</p>
<p class="audit-callout audit-callout--highlight">开发体验极致。<code class="code-ref">src/demos/liquid-demo.tsx</code> 展示了每个组件均配有精细的动态控制面板，用户可实时调整力、半径、衰减等参数，所有状态通过 <code class="code-ref">nuqs</code> 库持久化到 URL，方便分享特定效果。</p>
<p class="audit-callout audit-callout--doubt">未审阅到任何核心 vanilla 引擎的源码（如 <code class="code-ref">src/lib/Liquid/LiquidVanilla.ts</code>），无法评估其内部实现的质量、错误处理、性能优化及资源释放。</p>
<p class="audit-callout audit-callout--doubt">CI 配置（<code class="code-ref">.github/workflows/ci.yml</code>）仅包含类型检查和 lint，无任何测试步骤。仓库中未见 <code class="code-ref">tests</code> 目录或测试文件，组件库缺乏自动化测试覆盖。</p>
<p>适合追求视觉冲击的 landing page 或创意项目；需注意当前仅 Chrome/Edge 140+ 支持完整功能（其他浏览器降级为 WebGL 覆盖层），生产使用需申请 origin trial。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心依赖的 HTML-in-canvas API 为实验性特性，未来可能废弃或发生不兼容变更。</li><li>无任何自动化测试，组件行为可能随 Three.js 或浏览器更新而静默破坏。</li><li>组件仅作源文件分发，如果上游 Vanilla 引擎有严重 bug，所有框架版本同时受影响，且修复需等待库作者。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可为 SaaS 产品模板、营销页面提供差异化视觉效果，但开源模式本身难直接变现；维护者可考虑提供高级组件定制或企业支持。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.75</span>
  </div>
</div>
</section>