---
title: '[Score: 78.55] kitlangton/terminal-control'
date: '2026-06-04T03:43:34Z'
categories:
- Terminal Automation & Agent Tooling
tags:
- Rust
- Terminal
- PTY
- AI Agent
- TUI Testing
- CLI
intel_score: 78.55
repo_name: kitlangton/terminal-control
repo_link: https://github.com/kitlangton/terminal-control
summary: 面向 AI 编程代理的 PTY 终端控制工具，可启动命名会话、驱动键盘输入、读取可见屏幕并录制导出视频，适合需要真实终端交互的 agent 场景。
code_source: git
code_files_reviewed:
- packages/darwin-x64/package.json
- packages/darwin-arm64/package.json
- packages/linux-x64-gnu/package.json
- packages/linux-arm64-gnu/package.json
- package.json
- Cargo.toml
- .github/workflows/ci.yml
- .github/workflows/npm-release.yml
- src/lib.rs
- packages/test/src/index.ts
- src/main.rs
- src/frame.rs
- src/render.rs
- src/shot.rs
- src/driver.rs
- src/recording.rs
- packages/darwin-x64/README.md
- packages/darwin-arm64/README.md
- packages/linux-x64-gnu/README.md
- packages/linux-arm64-gnu/README.md
- packages/darwin-x64/CHANGELOG.md
- packages/darwin-arm64/CHANGELOG.md
- packages/linux-x64-gnu/CHANGELOG.md
- packages/linux-arm64-gnu/CHANGELOG.md
- packages/test/tsconfig.json
- packages/test/tsconfig.build.json
- packages/test/CHANGELOG.md
- packages/test/README.md
- packages/test/src/vitest.ts
- packages/test/src/index.test.ts
- .changeset/README.md
- .changeset/config.json
- schemas/video-edit-v1.schema.json
- AGENTS.md
- CONTEXT.md
- schemas/recording-entry-v1.schema.json
- schemas/frame-v1.schema.json
- skills/terminal-control/SKILL.md
- README.md
code_chars_analyzed: 230070
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
      <span class="scope-stat__value">约 230,070 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">packages/darwin-x64/package.json</code></li><li><code class="path-chip">packages/darwin-arm64/package.json</code></li><li><code class="path-chip">packages/linux-x64-gnu/package.json</code></li><li><code class="path-chip">packages/linux-arm64-gnu/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/npm-release.yml</code></li><li><code class="path-chip">src/lib.rs</code></li><li><code class="path-chip">packages/test/src/index.ts</code></li><li><code class="path-chip">src/main.rs</code></li><li><code class="path-chip">src/frame.rs</code></li><li><code class="path-chip">src/render.rs</code></li><li><code class="path-chip">src/shot.rs</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI 代理操控 TUI 应用时只能从纯文本 stdout 推断屏幕状态，无法感知光标位置、颜色、滚动行为或等待应用渲染完成；手动录制终端 demo 需要录屏工具和后期剪辑，成本高且不可复现。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 Rust 二进制 + TypeScript 客户端双层架构。核心终端生命周期在 <code class="code-ref">src/session.rs</code>（未审阅到完整实现，但 <code class="code-ref">src/main.rs:528</code> 的 <code class="code-ref">session::start</code> 和 <code class="code-ref">src/driver.rs:153</code> 的 <code class="code-ref">Session::start</code> 均引用该模块）管理 PTY 会话；一次性的屏幕读取由 <code class="code-ref">src/shot.rs</code> 完成，通过 <code class="code-ref">portable-pty</code> 创建伪终端、用 <code class="code-ref">vt100</code> 解析 ANSI 流、用 <code class="code-ref">from_screen</code>（<code class="code-ref">src/frame.rs:132</code>）提取结构化 Frame；录制在 <code class="code-ref">src/recording.rs</code> 中以 JSON Lines 格式写入 <code class="code-ref">.termctrl</code> 文件；SVG/PNG 渲染由 <code class="code-ref">src/render.rs</code> 承担。TypeScript 端（<code class="code-ref">packages/test/src/index.ts</code>）通过 <code class="code-ref">termctrl driver</code> 子进程的 JSON Lines stdin/stdout 协议操控多个隔离会话。</p>
<p class="audit-callout audit-callout--highlight">SVG 渲染器对 Unicode Box Drawing、Braille、几何符号做了原生几何绘制（<code class="code-ref">src/render.rs:100</code> 的 <code class="code-ref">graphic</code> 函数），避免依赖字体回退，截图在 CI 环境中也能一致呈现。</p>
<p class="audit-callout audit-callout--highlight">Driver 协议层（<code class="code-ref">src/driver.rs:40</code> 的 <code class="code-ref">serve</code>）在主线程读 JSON 请求，每个 ManagedSession 派生独立 pump 线程（<code class="code-ref">src/driver.rs:139</code>），session 间互不阻塞；<code class="code-ref">capture</code> 的 <code class="code-ref">idle</code>/<code class="code-ref">deadline</code>/<code class="code-ref">exited</code> reason 字段让测试客户端可以区分稳定快照和超时回退。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/shot.rs:149</code> 的 <code class="code-ref">from_command</code> 在构造 <code class="code-ref">Host</code> 时将 PTY writer 移入 Host，但 <code class="code-ref">writer</code> 已通过 <code class="code-ref">take_writer</code> 取走（<code class="code-ref">src/shot.rs:101</code>），若后续 <code class="code-ref">pair.master</code> 的其他 handle 关闭导致 writer 阻塞，调用线程会被 hang 住——代码未对 writer 做 write-closed 检测。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/session.rs</code> 未出现在 code_bundle 中，无法审阅命名会话的 Unix socket 生命周期管理和并发安全细节，本次结论不覆盖该模块；engineering 分数已因关键模块缺失而保守给分。</p>
<p>TypeScript 客户端已覆盖端到端测试（<code class="code-ref">packages/test/src/index.test.ts</code>），但 Rust 侧除 <code class="code-ref">src/main.rs</code> 的 CLI 解析测试外，<code class="code-ref">src/shot.rs</code> 和 <code class="code-ref">src/recording.rs</code> 的测试均为 Unix-only（<code class="code-ref">#[cfg(unix)]</code>）；若需 Windows 支持，需先补全平台抽象层。录制文件权限设为 0o600（<code class="code-ref">src/recording.rs:58</code>），但 README 未提示消费者在 CI 环境中清理临时 <code class="code-ref">.termctrl</code> 文件，建议在 AGENTS.md 中补充。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>session.rs 核心模块未在 code_bundle 中提供，Unix socket 生命周期、并发竞态、Windows 兼容性均无法验证</li><li>ffmpeg 为硬依赖（视频导出），CI/CD 环境未预装时会静默失败；README 未说明 graceful degradation</li><li>.termctrl 录制文件包含完整终端 I/O（含密码回显），0o600 权限仅限 Unix，Windows 无等价保护</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>填补了 AI agent 与真实 TUI 应用之间的交互鸿沟，对使用 OpenCode 等终端 AI 工具的团队有直接价值；npm 原生分发降低了 JS/TS 生态的试用门槛，但受众集中在需要终端自动化测试的垂直场景。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">86</div>
  <div class="score-bar"><span style="width:86%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.55</span>
  </div>
</div>
</section>