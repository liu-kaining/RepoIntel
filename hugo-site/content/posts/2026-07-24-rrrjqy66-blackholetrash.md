---
title: '[Score: 77.4] rrrjqy66/BlackHoleTrash'
date: '2026-07-24T16:31:45Z'
categories:
- Desktop Enhancement
tags:
- Windows
- Rust
- Recycle Bin
- GPU
- UI
intel_score: 77.4
repo_name: rrrjqy66/BlackHoleTrash
repo_link: https://github.com/rrrjqy66/BlackHoleTrash
summary: 一个 Windows 桌面黑洞回收站，用实时引力透镜扭曲桌面背景，将拖入的文件安全送入回收站而非永久删除。
code_source: git
code_files_reviewed:
- Cargo.toml
- src/platform/mod.rs
- src/platform/windows/mod.rs
- src/gpu_share.rs
- src/capture_macos.rs
- src/capture_windows.rs
- src/screenshot_fix.rs
- src/platform/windows/recycle_bin.rs
- src/platform/windows/taskbar.rs
- src/platform/windows/drop_window.rs
- src/platform/windows/ctrl_double_tap.rs
- src/platform/windows/capture_exclusion.rs
- src/platform/windows/window_occlusion.rs
- src/platform/windows/ole_drop_target.rs
- src/platform/windows/cursor_gravity.rs
- examples/validate_shader.rs
- build.rs
- docs/superpowers/specs/2026-07-24-fps-options-design.md
- docs/releases/v1.0.0.md
- docs/releases/v1.1.0.md
- docs/releases/v1.2.0.md
- docs/superpowers/specs/2026-07-23-repository-cleanup-design.md
- docs/superpowers/specs/2026-07-23-windows-installer-design.md
- docs/superpowers/specs/2026-07-24-readme-v1-2-design.md
- docs/superpowers/specs/2026-07-24-absorption-growth-design.md
- docs/superpowers/plans/2026-07-24-fps-options.md
- docs/releases/v1.3.0.md
- docs/superpowers/specs/2026-07-24-capture-exclusion-fail-closed-design.md
- docs/superpowers/plans/2026-07-24-absorption-growth.md
- docs/superpowers/plans/2026-07-23-repository-cleanup.md
- docs/superpowers/specs/2026-07-24-desktop-visibility-controls-design.md
- docs/superpowers/plans/2026-07-24-readme-v1-2.md
- docs/superpowers/plans/2026-07-23-windows-installer.md
- docs/superpowers/specs/2026-07-23-cursor-gravity-design.md
- README.md
- README.en.md
- docs/superpowers/plans/2026-07-23-cursor-gravity.md
- docs/superpowers/plans/2026-07-24-desktop-visibility-controls.md
- docs/superpowers/plans/2026-07-24-capture-exclusion-fail-closed.md
code_chars_analyzed: 233148
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
      <span class="scope-stat__value">39 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 233,148 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">src/platform/mod.rs</code></li><li><code class="path-chip">src/platform/windows/mod.rs</code></li><li><code class="path-chip">src/gpu_share.rs</code></li><li><code class="path-chip">src/capture_macos.rs</code></li><li><code class="path-chip">src/capture_windows.rs</code></li><li><code class="path-chip">src/screenshot_fix.rs</code></li><li><code class="path-chip">src/platform/windows/recycle_bin.rs</code></li><li><code class="path-chip">src/platform/windows/taskbar.rs</code></li><li><code class="path-chip">src/platform/windows/drop_window.rs</code></li><li><code class="path-chip">src/platform/windows/ctrl_double_tap.rs</code></li><li><code class="path-chip">src/platform/windows/capture_exclusion.rs</code></li><li><code class="path-chip">src/platform/windows/window_occlusion.rs</code></li><li><code class="path-chip">src/platform/windows/ole_drop_target.rs</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Windows 用户将文件拖到回收站操作单调无反馈，且误操作可能导致意外永久删除风险；该项目以视觉化、物理模拟的交互提供安全保障和趣味性。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用模块化设计，<code class="code-ref">src/platform/windows/mod.rs:1-9</code> 导出了拖放目标、回收、捕获排除、窗口遮挡检测、鼠标引力等多个子系统，各模块职责清晰。桌面捕获通过 <code class="code-ref">src/capture_windows.rs</code> 的零拷贝 D3D11→D3D12 共享纹理路径（<code class="code-ref">src/gpu_share.rs</code> 负责资源创建）实现，CPU 回退路径也在同一文件。OLE 拖放由 <code class="code-ref">src/platform/windows/ole_drop_target.rs</code> 处理，文件验证和回收操作调用 <code class="code-ref">src/platform/windows/recycle_bin.rs</code> 中的 <code class="code-ref">IFileOperation + FOFX_RECYCLEONDELETE</code>，确保非永久删除。</p>
<p class="audit-callout audit-callout--highlight">捕获排除采用 fail-closed 设计，<code class="code-ref">src/platform/windows/capture_exclusion.rs:218-228</code> 的 <code class="code-ref">apply_and_verify</code> 在设置显示亲和性后立即读回并严格对比，失败则弹出诊断对话框并退出，避免递归反馈。</p>
<p class="audit-callout audit-callout--highlight">任务栏排除模块包含单元测试，<code class="code-ref">src/platform/windows/taskbar.rs:130-172</code> 验证了样式过滤逻辑，确保窗口不会意外出现在任务栏。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src/main.rs</code> 和 WGSL 着色器源码，主状态机、渲染管线、配置热重载的实际实现无从评估，核心渲染效果只能从 README 推断。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖不完整，各模块虽有单元测试，但缺乏跨模块集成测试，且未提供 macOS 分支的真实验证（<code class="code-ref">src/capture_macos.rs</code> 标注 untested）。</p>
<p>作为以趣味性为主的桌面工具，当前代码结构清晰，适合作为 Rust 在 Windows 系统编程的参考案例；生产环境使用需注意性能（实时 GPU 渲染）和系统兼容性（Win10 2004+）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目创建仅 1 天便发布多个版本，长期维护稳定性待观察。</li><li>依赖 Windows Shell 接口和捕获排除，虚拟机、远程桌面等环境可能无法正常使用。</li><li>实时 GPU 渲染和桌面捕获可能在高负载系统上导致性能或电量问题。</li><li>用户群体偏向小众爱好者，功能迭代方向可能不明确。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>项目主要用于桌面美化与交互创新，商业变现可能性较低，可能依赖捐赠或作为技术展示。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.4</span>
  </div>
</div>
</section>