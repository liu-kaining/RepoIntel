---
title: '[Score: 75.1] mshumer/Claude-of-Duty'
date: '2026-07-26T02:30:49Z'
categories:
- Procedural FPS Runtime
tags:
- WebGL2
- Three.js
- procedural generation
- shader compilation
- browser game
- AI-assisted
intel_score: 75.1
repo_name: mshumer/Claude-of-Duty
repo_link: https://github.com/mshumer/Claude-of-Duty
summary: 一个全程序化生成的浏览器 FPS，Three.js 实现使命召唤风格画面，自研物理、音频合成与可重现性能测试工具链。
code_source: git
code_files_reviewed:
- package.json
- src/materials/index.js
- src/world/index.js
- src/ui/index.js
- src/player/index.js
- src/weapons/index.js
- src/audio/index.js
- src/physics/index.js
- src/sky/index.js
- src/ai/index.js
- src/main.js
- src/core/rng.js
- src/core/config.js
- src/render/pass.js
- src/fx/tracers.js
- src/sky/noise.js
- src/sky/fullscreen.js
- src/ui/prompts.js
- src/ai/squad.js
- src/fx/lights.js
- src/core/registry.js
- src/ui/crosshair.js
- src/ui/killfeed.js
- src/ui/damage.js
- src/ui/compass.js
- src/ui/hitmarkers.js
- src/render/env.js
- src/fx/noise.js
- src/player/springs.js
- src/render/motionblur.js
- src/weapons/ballistics.js
- src/core/engine.js
- src/sky/celestial.js
- src/render/contact.js
- src/weapons/mathx.js
- src/fx/util.js
- src/ui/demo.js
- src/player/lowhealth.js
- src/render/glsl.js
- src/render/ssr.js
- src/ui/menu.js
- src/ai/preview.js
- src/physics/surfaces.js
- src/ui/util.js
- src/fx/explosions.js
- src/ai/grounding.js
- src/ui/health.js
- src/render/exposure.js
code_chars_analyzed: 446252
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
      <span class="scope-stat__value">约 446,252 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">src/materials/index.js</code></li><li><code class="path-chip">src/world/index.js</code></li><li><code class="path-chip">src/ui/index.js</code></li><li><code class="path-chip">src/player/index.js</code></li><li><code class="path-chip">src/weapons/index.js</code></li><li><code class="path-chip">src/audio/index.js</code></li><li><code class="path-chip">src/physics/index.js</code></li><li><code class="path-chip">src/sky/index.js</code></li><li><code class="path-chip">src/ai/index.js</code></li><li><code class="path-chip">src/main.js</code></li><li><code class="path-chip">src/core/rng.js</code></li><li><code class="path-chip">src/core/config.js</code></li><li><code class="path-chip">src/render/pass.js</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>前端工程师想在浏览器展示 AAA 级视觉效果时，依赖美术资产管线沉重；AI 辅助生成 55k 行代码但缺乏可重现的渲染对比手段。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用模块化子系统设计，每个子系统有静态 id 和 deps 声明，由 Registry 拓扑排序初始化（<code class="code-ref">src/core/registry.js:63</code>-68）。主循环在 <code class="code-ref">src/core/engine.js:96</code>-112 中按 fixedUpdate/update/lateUpdate/render 顺序驱动。渲染管线基于延迟/前向混合，材质系统在 <code class="code-ref">src/materials/index.js:80</code>-105 中通过 TextureForge 用 GPU 程序化烘焙 PBR 纹理，并缓存以避免重复。世界构建在 <code class="code-ref">src/world/index.js:74</code>-101 中组装建筑、道具和静态碰撞，并注册到物理系统。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/world/index.js:125</code>-176 的 <code class="code-ref">_addBallast</code> 方法通过插入黑色零强度点光源将可见点光源数量恒定，消除了因 WebGL shader 程序键变化导致的中途编译卡顿，这是一种针对 Web 渲染的务实优化。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/sky/index.js:1318</code>-1340 的日照强度计算应用了&quot;光束地板&quot;（beam floor）和曝光补偿，防止黄昏天空亮度反超受光表面，使 key:fill 比与太阳高度角无关，维持画面一致性。</p>
<p class="audit-callout audit-callout--doubt">物理系统 <code class="code-ref">src/physics/index.js</code> 中未见针对复杂场景的 BVH 更新增量机制，标记为 <code class="code-ref">dirty</code> 后只能全量重建，大世界动态变化时可能造成峰值开销。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src/core/prewarm.js</code> 真实实现，仅从 <code class="code-ref">src/main.js:96</code>-98 注释知其为 shader 预热模块，其可靠性无法验证。</p>
<p>若要在类似项目中使用这些技术，需评估 WebGL2 场景复杂度对移动端的影响，并考虑将物理集成替换为更轻量的库以避免全量 BVH 重建。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 承认画质仅达竞赛评分 5.05/10，与真实 CoD 画面差距明显，难以吸引玩家。</li><li>项目刚创建 (0 天)，无开源社区动态和历史，持续维护风险未知。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 AI 协助大规模代码生成的可行性演示，其性能剖析工具 (baseline.mjs, imagediff.mjs) 可被其他图形项目复用，但游戏本身缺乏商业化竞品品质。</p>
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
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.1</span>
  </div>
</div>
</section>