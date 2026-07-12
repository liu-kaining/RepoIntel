---
title: '[Score: 82.3] karola3vax/CS2FOW'
date: '2026-07-12T05:54:50Z'
categories:
- Game Server Anti-Cheat
tags:
- counter-strike-2
- anti-cheat
- server-side
- visibility-culling
- bvh
- metamod-plugin
intel_score: 82.3
repo_name: karola3vax/CS2FOW
repo_link: https://github.com/karola3vax/CS2FOW
summary: 为CS2社区服务器提供服务器端透视防护，通过视线检测和烟雾模拟隐藏墙后敌人实体，玩家无需客户端。
code_source: git
code_files_reviewed:
- .github/workflows/build.yml
- src/core/builder.h
- src/core/subprocess.h
- src/baker/glb_import.h
- src/core/map_source.h
- src/core/vpk.h
- src/plugin/automatic_baker.h
- src/core/transmit_masks.h
- src/core/visibility_sampling.h
- src/core/smoke_occlusion.h
- src/plugin/automatic_baker.cpp
- src/core/bvh8.h
- src/plugin/visibility_worker.h
- src/core/transmit_debug.h
- src/core/map_source.cpp
- src/plugin/visibility_worker.cpp
- src/core/subprocess.cpp
- src/core/bvh8.cpp
- src/core/lifecycle_guard.h
- src/baker/glb_import.cpp
- src/core/smoke_occlusion.cpp
- src/plugin/plugin.h
- src/core/builder.cpp
- src/core/bvh8_format.cpp
- src/baker/main.cpp
- src/core/vpk.cpp
- src/plugin/transmit.cpp
- src/core/visibility_sampling.cpp
- src/plugin/game_state.cpp
- src/plugin/plugin.cpp
- tools/vrf/README.md
- tests/test_suites.h
- configure.py
- release/v0.2.0-preview-manifest.json
- tools/visibility_point_editor/check_points.py
- tools/visibility_point_editor/README.md
- tools/visibility_point_editor/default_sas_visibility_points.json
- release/v0.2.0-preview-notes.md
- CHANGELOG.md
- tests/test_main.cpp
- tools/visibility_point_editor/export_assets.py
- package.py
- README.md
- docs/CODE_TOUR.md
- tests/map_and_bvh_tests.cpp
- tools/visibility_point_editor/viewer.js
- tests/visibility_and_transmit_tests.cpp
code_chars_analyzed: 332696
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
      <span class="scope-stat__value">约 332,696 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/build.yml</code></li><li><code class="path-chip">src/core/builder.h</code></li><li><code class="path-chip">src/core/subprocess.h</code></li><li><code class="path-chip">src/baker/glb_import.h</code></li><li><code class="path-chip">src/core/map_source.h</code></li><li><code class="path-chip">src/core/vpk.h</code></li><li><code class="path-chip">src/plugin/automatic_baker.h</code></li><li><code class="path-chip">src/core/transmit_masks.h</code></li><li><code class="path-chip">src/core/visibility_sampling.h</code></li><li><code class="path-chip">src/core/smoke_occlusion.h</code></li><li><code class="path-chip">src/plugin/automatic_baker.cpp</code></li><li><code class="path-chip">src/core/bvh8.h</code></li><li><code class="path-chip">src/plugin/visibility_worker.h</code></li><li><code class="path-chip">src/core/transmit_debug.h</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>CS2社区服务器长期面临透视外挂泛滥，客户端反作弊效果有限，服务器端缺乏有效的实体隐藏机制。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">游戏帧捕获（src/plugin/game_state.cpp:capture）复制玩家位置/速度/武器等至visibility_snapshot，提交给后台worker（src/plugin/visibility_worker.cpp:submit）。Worker线程（visibility_worker::run）对每对玩家构建8个视线起点和至多48个目标点（src/core/visibility_sampling.cpp:visibility_origins/visibility_targets），用BVH8射线检测阻挡（src/core/bvh8.cpp:segment_blocked），可选烟雾检测（src/core/smoke_occlusion.cpp:smoke_line_blocked），生成可见性矩阵。CheckTransmit钩子（src/plugin/transmit.cpp:hook_check_transmit）获取最新结果，对非全量更新的收件人，若目标不可见且pair guard允许（src/core/lifecycle_guard.h:pair_allows_hiding），从主发送列表中清除该目标视觉组实体。</p>
<p class="audit-callout audit-callout--highlight">Worker线程仅读取BVH8与复制数据，永不触及游戏对象（src/plugin/visibility_worker.cpp:run），避免阻塞游戏主循环，利用条件变量替换最新工作项。</p>
<p class="audit-callout audit-callout--highlight">严格的生命周期与pair guard机制（src/core/lifecycle_guard.h:117）要求pair经过warmup且曾发送过完整视觉组后才允许隐藏，状态变化立即fail-open，确保安全。</p>
<p class="audit-callout audit-callout--doubt">地图几何体仅烘焙静态三角形（src/baker/glb_import.cpp:physics_group_accepted），无法处理门、可破坏物等动态障碍（README明确声明），可能导致错判遮挡或漏透视。</p>
<p class="audit-callout audit-callout--doubt">烟雾内存布局依赖硬编码偏移量（src/core/smoke_occlusion.h:11-15），通过gamedata文件加载，若CS2更新结构则烟雾遮挡可能失效，且无自动校验。</p>
<p>探索集成引擎动态障碍查询，或提供手动标记机制；为gamedata增加版本校验和回退提醒，降低游戏更新风险。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>强依赖CS2内部二进制布局，游戏更新可能导致需要频繁更新gamedata；烘焙工具链依赖第三方VRF CLI，用户环境配置可能复杂。</li><li>仅处理静态墙体，动态障碍物（门、可破坏物）仍可被利用透视，可能被高级外挂绕过。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为CS2社区服务器提供了一种无需客户端安装的反透视方案，可能被流行的社区服务采用，降低外挂对游戏体验的影响。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.3</span>
  </div>
</div>
</section>