---
title: '[Score: 77.85] achimala/TheLongSilence'
date: '2026-07-28T16:38:39Z'
categories:
- Procedural Space Exploration Game
tags:
- WebGL2
- Three.js
- Procedural Generation
- GLSL Shaders
- Game Development
- Audio Synthesis
intel_score: 77.85
repo_name: achimala/TheLongSilence
repo_link: https://github.com/achimala/TheLongSilence
summary: 完全自研着色器、零外部资产的程序化太空探索游戏，在浏览器中实时生成星体、大气与飞船内部，提供高沉浸感飞行体验。
code_source: git
code_files_reviewed:
- package.json
- src/main.js
- src/gfx/cubeBake.js
- src/game/encounters.js
- src/world/Dust.js
- src/game/directives.js
- src/ship/Ship.js
- src/ship/interiorAssets.js
- src/ui/Codex.js
- src/core/Input.js
- src/game/lore.js
- src/gfx/FoldTunnel.js
- src/ship/Player.js
- src/ui/HUD.js
- src/gfx/Sky.js
- src/core/Engine.js
- src/game/Director.js
- src/audio/Audio.js
- src/world/Planet.js
- src/world/Star.js
- src/ship/HoloMap.js
- src/world/Asteroids.js
- src/world/generate.js
- src/world/planetBakeShader.js
- src/ship/Cockpit.js
- src/ship/HoloScreen.js
- src/gfx/glsl/noise.js
- vite.config.js
- .claude/skills/blender-hardsurface/reference/bmcp_client.py
- tools/interior_bake/60_run_tiles.py
- tools/crop.py
- tools/clay.py
- tools/interior_bake/61_run_kit.py
- tools/interior_bake/20_tile_bake.py
- tools/interior_bake/00_lib.py
- tools/interior_bake/70_clay.py
- README.md
- tools/interior_bake/10_tile_geo.py
- tools/bake_interior.py
- tools/interior_bake/30_compose.py
- .claude/skills/blender-hardsurface/SKILL.md
- tools/interior_bake/50_assemble.py
- .claude/skills/blender-hardsurface/reference/cinematic.py
- tools/interior_bake/40_kit.py
- .claude/skills/blender-hardsurface/reference/build_tender.py
- package-lock.json
code_chars_analyzed: 600071
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
      <span class="scope-stat__value">46 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 600,071 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">src/main.js</code></li><li><code class="path-chip">src/gfx/cubeBake.js</code></li><li><code class="path-chip">src/game/encounters.js</code></li><li><code class="path-chip">src/world/Dust.js</code></li><li><code class="path-chip">src/game/directives.js</code></li><li><code class="path-chip">src/ship/Ship.js</code></li><li><code class="path-chip">src/ship/interiorAssets.js</code></li><li><code class="path-chip">src/ui/Codex.js</code></li><li><code class="path-chip">src/core/Input.js</code></li><li><code class="path-chip">src/game/lore.js</code></li><li><code class="path-chip">src/gfx/FoldTunnel.js</code></li><li><code class="path-chip">src/ship/Player.js</code></li><li><code class="path-chip">src/ui/HUD.js</code></li><li class="path-more">另有 32 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>浏览器太空游戏多依赖预置模型，无法生成无限宇宙；要同时实现真实感渲染与动态叙事，开发者需整合大量底层图形技术。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口 <code class="code-ref">src/main.js:127</code> 创建 Game 实例并启动主循环，每帧调用 <code class="code-ref">game.update(dt)</code> 推进世界状态，再通过 <code class="code-ref">Engine.render</code> (<code class="code-ref">src/core/Engine.js:173</code>) 执行双通道渲染：先绘制外部场景到 HDR 目标，再叠加座舱覆盖层。<code class="code-ref">Engine</code> 负责动态分辨率调整和日志深度缓冲。世界生成 (<code class="code-ref">src/world/generate.js:1</code>) 完全由种子驱动，产出恒星、行星、小行星带和异常点。行星渲染 (<code class="code-ref">src/world/Planet.js</code>) 使用烘焙立方体贴图表达地表高度和反照率，运行时仅需三次纹理采样重建法线；大气层为单次散射光线步进 (<code class="code-ref">src/world/Planet.js:180</code>)。恒星渲染 (<code class="code-ref">src/world/Star.js:1</code>) 自建分形颗粒、黑子、临边昏暗和日冕，避开“扁平圆盘”效果。座舱显示采用自定义 HoloScreen 系统 (<code class="code-ref">src/ship/HoloScreen.js</code>)，将 2D 画布绘制内容贴上模拟 CRT 效果的着色器。音频引擎 (<code class="code-ref">src/audio/Audio.js</code>) 完全通过 WebAudio API 合成环境音、音乐和互动音效。</p>
<p class="audit-callout audit-callout--highlight">恒星表面细节极致。<code class="code-ref">src/world/Star.js</code> 中的片段着色器使用沃利噪声构造颗粒边界、结合温度 blackbody 分布和 2.4 次幂的临边昏暗 (<code class="code-ref">src/world/Star.js:100-200</code>)，使恒星从中心到边缘亮度自然衰减，避免过曝和剪影。日冕部分通过屏幕对齐公告板与解析边缘参数 <code class="code-ref">limbParam</code> 还原真实投影轮廓，避免角间距接缝。</p>
<p class="audit-callout audit-callout--highlight">座舱仪表板完全丢弃 DOM 叠加层。<code class="code-ref">src/ship/Cockpit.js</code> 中的 <code class="code-ref">drawMain</code> 函数在 Canvas 上绘制包含分区、竖条刻度、方位带和引擎参数的全套飞行仪表，并通过 <code class="code-ref">HoloScreen</code> 着色器添加扫描线、磷光溢出和视差反射 (<code class="code-ref">src/ship/HoloScreen.js:250-300</code>)。这使仪表像真实硬件，而非网页贴图。</p>
<p class="audit-callout audit-callout--doubt">未审阅到自动化测试代码。README 提及 <code class="code-ref">tools/play.mjs</code> 等验证工具，但 code_bundle 中未包含这些文件。缺乏测试可能影响长期维护和回归检测。</p>
<p class="audit-callout audit-callout--doubt">项目仅创建 1 天，整个代码树仅一次提交，尚无法评估社区贡献和长期稳定性。</p>
<p>可迅速部署为技术演示，吸引 WebGL 引擎或游戏创作社区；后续应补充单元测试与 CI 流程，降低维护风险。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅创建1天且单次提交，无社区反馈</li><li>代码树中未发现测试文件，长期维护风险高</li><li>极端 GLSL 复杂度可能造成低端 GPU 性能瓶颈</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>本项目可作为 WebGL 极致渲染能力的标杆，吸引技术投资人关注；其完全程序化生成架构也为下一代浏览器游戏或元宇宙应用提供参考实现。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">55</div>
  <div class="score-bar"><span style="width:55%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.85</span>
  </div>
</div>
</section>