---
title: '[Score: 76.65] AyagamiDev/ayagami'
date: '2026-07-14T21:55:01Z'
categories:
- 2D Animation / Game Engine Runtime
tags:
- Rust
- Live2D
- renderer
- reverse-engineering
- wgpu
- egui
intel_score: 76.65
repo_name: AyagamiDev/ayagami
repo_link: https://github.com/AyagamiDev/ayagami
summary: 纯 Rust 实现的 Live2D 兼容 2D 模型渲染 SDK，黑盒逆向 MOC3 格式，提供从解析到 GPU 渲染的完整链路，免费开源免除版权限制。
code_source: git
code_files_reviewed:
- Cargo.toml
- ayagami/Cargo.toml
- ayagami-demo/Cargo.toml
- ayagami-render/Cargo.toml
- .github/workflows/deploy_web_demo.yml
- ayagami-render/src/main.rs
- ayagami-demo/src/lib.rs
- ayagami/src/lib.rs
- ayagami/src/main.rs
- ayagami/src/file/mod.rs
- ayagami-demo/src/main.rs
- ayagami-render/src/lib.rs
- ayagami/src/driver/mod.rs
- FUNDING.yml
- ayagami-demo/inline-wasm.sh
- ayagami-demo/Trunk.release.toml
- .github/scripts/build_demo_web.sh
- ayagami/src/meta.rs
- AGENTS.md
- ayagami/src/collections.rs
- ayagami/src/driver/deformer.rs
- ayagami/src/file/types.rs
- ayagami-render/src/texture.rs
- CONTRIBUTING.md
- README.md
- ayagami/src/file/classes.rs
- ayagami/src/core.rs
- ayagami/src/file/parse.rs
- ayagami/src/file/model.rs
- ayagami-demo/src/app.rs
- ayagami/src/file/macros.rs
- ayagami-render/src/renderer.rs
code_chars_analyzed: 248701
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
      <span class="scope-stat__value">32 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 248,701 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">ayagami/Cargo.toml</code></li><li><code class="path-chip">ayagami-demo/Cargo.toml</code></li><li><code class="path-chip">ayagami-render/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/deploy_web_demo.yml</code></li><li><code class="path-chip">ayagami-render/src/main.rs</code></li><li><code class="path-chip">ayagami-demo/src/lib.rs</code></li><li><code class="path-chip">ayagami/src/lib.rs</code></li><li><code class="path-chip">ayagami/src/main.rs</code></li><li><code class="path-chip">ayagami/src/file/mod.rs</code></li><li><code class="path-chip">ayagami-demo/src/main.rs</code></li><li><code class="path-chip">ayagami-render/src/lib.rs</code></li><li><code class="path-chip">ayagami/src/driver/mod.rs</code></li><li><code class="path-chip">FUNDING.yml</code></li><li class="path-more">另有 18 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>游戏和 VTuber 应用集成 Live2D 模型需使用官方许可 SDK，费用高、平台受限且不允许自由加载用户模型；现有开源方案逆向方式可能不彻底或存在法律风险。Ayagami 通过严格黑盒独立实现，解决了版权与许可痛点。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目以 workspace 组织，分为 <code class="code-ref">ayagami</code>（核心库）、<code class="code-ref">ayagami-render</code>（渲染后端）、<code class="code-ref">ayagami-demo</code>（测试应用）。<code class="code-ref">ayagami/src/lib.rs</code> 暴露 <code class="code-ref">core</code>、<code class="code-ref">file</code>、<code class="code-ref">driver</code> 等模块；<code class="code-ref">ayagami/src/file/parse.rs</code> 解析 MOC3 二进制，构建 <code class="code-ref">ParsedModel</code>，并通过宏系统生成强类型视图（<code class="code-ref">ayagami/src/file/classes.rs</code> 及 <code class="code-ref">ayagami/src/file/macros.rs</code>）。<code class="code-ref">ayagami/src/driver/mod.rs</code> 实现模型变形计算，接收参数后输出带视觉属性的变形网格，支持增量更新和脏标记。<code class="code-ref">ayagami-render/src/renderer.rs</code> 将结果通过 wgpu 渲染，管理纹理、裁剪遮罩和多 pass 管线。</p>
<p class="audit-callout audit-callout--highlight">驱动层增量计算策略，<code class="code-ref">ayagami/src/driver/mod.rs</code> 中 <code class="code-ref">drive()</code> 方法通过 <code class="code-ref">clean</code>/<code class="code-ref">updated</code> 标记实现仅重算变更部分，避免全量重算，提升性能。</p>
<p class="audit-callout audit-callout--highlight">声明的宏编译期与类型安全，<code class="code-ref">ayagami/src/file/macros.rs</code> 利用 Rust 宏为每种 MOC3 对象自动生成解析和视图代码，减少手写错误。</p>
<p class="audit-callout audit-callout--doubt">未审阅到任何测试文件（<code class="code-ref">tests/</code> 或 <code class="code-ref">*_test.rs</code>），工程质量难以保证；核心变形逻辑的正确性缺乏验证。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">ayagami-render/src/shader.wgsl</code>，着色器正确性未知；另外 <code class="code-ref">ayagami/src/driver/deformer.rs:185</code> 附近的 <code class="code-ref">blend_arrays</code> 使用了 <code class="code-ref">unsafe</code>，虽有合理性注释，但增加验证负担。</p>
<p>尽快补充单元测试和集成测试，覆盖文件解析、变形计算和渲染管线；与官方渲染效果做对比验证核心算法；稳定 API 并提供文档。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅诞生 3 天，API 未稳定，文档缺失，生产环境采纳风险极高。</li><li>严格的黑盒贡献政策可能限制社区参与，且 Live2D 公司可能通过格式升级或法律手段施压。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 VTuber 软件、游戏引擎等提供了无许可风险的 Live2D 运行时替代，有望吸引独立开发者和开源项目，但生态尚弱，需时间成熟。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.65</span>
  </div>
</div>
</section>