---
title: '[Score: 79.65] NikolayS/PGSimCity'
date: '2026-07-28T19:18:28Z'
categories:
- Database Education
tags:
- postgresql
- visualization
- threejs
- education
- 3d
- webgl
intel_score: 79.65
repo_name: NikolayS/PGSimCity
repo_link: https://github.com/NikolayS/PGSimCity
summary: 将 PostgreSQL 集群内部运作建模为可探索的 3D 城市，直观演示缓冲池、WAL、复制与真空清理等机制。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- .github/workflows/pages.yml
- src/main.ts
- src/core/build.ts
- src/ui/legal.ts
- src/engine/label-detail.ts
- src/core/destinations.test.ts
- src/engine/label-layout.test.ts
- src/sim/scenarios.test.ts
- src/observability/shell.ts
- src/ui/trace-dwell.ts
- src/engine/labels-occlusion.test.ts
- src/engine/renderer.test.ts
- src/engine/label-layout.ts
- src/core/bus.ts
- src/sim/sample-scale-boundary.test.ts
- src/ui/pgdata-language.test.ts
- src/ui/pool-sample.test.ts
- src/core/timebase.test.ts
- src/world/plate-fog.ts
- src/core/timebase.ts
- src/core/destinations.ts
- src/ui/boot.test.ts
- src/observability/pool-sample.test.ts
- src/ui/boot.ts
- src/ui/zoom-context.test.ts
- src/ui/mode-exits.ts
- src/core/registry.ts
- src/ui/trace-copy.ts
- src/sim/honesty.test.ts
- src/sim/trace.test.ts
- src/sim/mvcc.test.ts
- src/observability/real-postgres.test.ts
- src/engine/roads.ts
- src/ui/zoom-context.ts
- src/world/maintenance.test.ts
- src/ui/timebase.test.ts
- src/sim/model.test.ts
- src/engine/audio.test.ts
- src/ui/trace-dwell.test.ts
- src/sim/workingset.measure.test.ts
- src/core/util.ts
- src/ui/context-menu.test.ts
- src/core/analytics.test.ts
- src/sim/mvcc.ts
- src/observability/real-postgres.ts
- src/engine/camera-controls.test.ts
code_chars_analyzed: 147518
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
      <span class="scope-stat__value">约 147,518 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/pages.yml</code></li><li><code class="path-chip">src/main.ts</code></li><li><code class="path-chip">src/core/build.ts</code></li><li><code class="path-chip">src/ui/legal.ts</code></li><li><code class="path-chip">src/engine/label-detail.ts</code></li><li><code class="path-chip">src/core/destinations.test.ts</code></li><li><code class="path-chip">src/engine/label-layout.test.ts</code></li><li><code class="path-chip">src/sim/scenarios.test.ts</code></li><li><code class="path-chip">src/observability/shell.ts</code></li><li><code class="path-chip">src/ui/trace-dwell.ts</code></li><li><code class="path-chip">src/engine/labels-occlusion.test.ts</code></li><li><code class="path-chip">src/engine/renderer.test.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>后端工程师理解 PostgreSQL 内部行为（如检查点延迟、表膨胀、同步提交代价）依赖文档和源码，缺乏交互式探索手段；PGSimCity 通过可操作的模拟场景与引导游览，在浏览器中即时呈现这些机制，降低认知门槛。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro"><code class="code-ref">src/main.ts</code> 按顺序启动渲染器、相机、仿真引擎 (<code class="code-ref">src/sim/model.ts</code>)、世界模块 (<code class="code-ref">src/world/shmem.ts</code>, <code class="code-ref">src/world/wal.ts</code> 等)，世界模块只读取仿真状态，UI 通过总线 (<code class="code-ref">src/core/bus.ts</code>) 通信。仿真固定 30 Hz 步进 (<code class="code-ref">src/core/timebase.ts</code> 的 <code class="code-ref">MODEL_STEP_SECONDS</code>)，与渲染分离。组件注册 (<code class="code-ref">src/core/registry.ts</code>) 配合碰撞/拾取 (<code class="code-ref">src/engine/collision.ts</code>, <code class="code-ref">src/engine/picker.ts</code>) 实现精确交互。部分代码支持 PGlite 连接真实 PG 并解析 EXPLAIN (<code class="code-ref">src/observability/real-postgres.ts</code>)。</p>
<p class="audit-callout audit-callout--highlight">仿真模型经过严格校准，<code class="code-ref">src/sim/model.test.ts</code> 验证默认配置下缓存命中率 ≥98%，<code class="code-ref">src/sim/mvcc.test.ts</code> 实现 MVCC 可见性规则并测试长事务与 vacuum 回收，逻辑扎实。</p>
<p class="audit-callout audit-callout--highlight">测试覆盖充分，<code class="code-ref">src/sim/honesty.test.ts</code> 确保 autovacuum 行为与叙述一致，<code class="code-ref">src/engine/audio.test.ts</code> 对音频系统进行 Mock 测试，总测试 234 例，非空壳项目。</p>
<p class="audit-callout audit-callout--doubt">CI 工作流 (<code class="code-ref">.github/workflows/ci.yml</code>) 仅含 typecheck 与 build，未执行 <code class="code-ref">npm test</code>，与 README “CI fails the build on a red test” 矛盾，可能漏检回归。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/observability/real-postgres.ts</code> 的 <code class="code-ref">loadRealPostgres</code> 动态导入 WASM 包，未在已提供测试文件中见到跨浏览器或内存限制验证，存在兼容性隐患。</p>
<p>在 CI 中加入测试步骤并添加 WASM 后端的集成测试；补充移动端 WebGL 降级方案的自动化验证。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仿真参数经过缩放，非真实数据库镜像，可能误导用户忽略实际性能差异。</li><li>触控控制仅通过 Chrome 模拟验证，真机 WebGL2 设备兼容性未全面测试。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 PostgreSQL 教育工具，可降低团队内部培训成本，适合技术布道或社区推广，无明显直接变现路径但可能吸引赞助或成为官方推荐学习资源。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.65</span>
  </div>
</div>
</section>