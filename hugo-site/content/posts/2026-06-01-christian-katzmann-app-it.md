---
title: '[Score: 78.45] Christian-Katzmann/app-it'
date: '2026-06-01T03:45:20Z'
categories:
- Developer Tools
tags:
- macOS
- Dock
- WebKit
- Shell
- Claude-Code
- Codex
intel_score: 78.45
repo_name: Christian-Katzmann/app-it
repo_link: https://github.com/Christian-Katzmann/app-it
summary: 通过 AI 编码助手插件形式，将本地 Web 项目一键打包为 macOS Dock 可启动的原生 .app 包，适合经常在本地开发 Web 应用的
  macOS 开发者。
code_source: git
code_files_reviewed:
- .github/workflows/ci.yml
- plugins/app-it/.claude-plugin/plugin.json
- plugins/app-it-static/.claude-plugin/plugin.json
- plugins/app-it-windows/.claude-plugin/plugin.json
- SECURITY.md
- .agents/plugins/marketplace.json
- docs/decisions/README.md
- docs/decisions/0003-bundle-id-prefix.md
- plugins/app-it/.codex-plugin/plugin.json
- docs/decisions/0002-macos-only-scope.md
- CONTRIBUTING.md
- docs/decisions/REJECTED/auto-attach-to-a-running-server.md
- docs/decisions/0004-daemon-mode-lifecycle.md
- plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/README.md
- docs/decisions/REJECTED/electron-or-tauri-by-default.md
- plugins/app-it-static/skills/app-it-static/templates/desktop-rebuild.sh
- docs/decisions/0001-native-webkit-shell.md
- docs/TROUBLESHOOTING.md
- plugins/app-it-windows/.codex-plugin/plugin.json
- plugins/app-it-static/.codex-plugin/plugin.json
- docs/RELEASE_CHECKLIST.md
- plugins/app-it-static/skills/app-it-static/templates/app-it.config.example.json
- plugins/app-it-static/skills/app-it-static/templates/run-template-static-file.sh
- plugins/app-it/skills/app-it/templates/app-it.config.example.json
- design/README.md
- plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/App.xaml.cs
- CHANGELOG.md
- install.sh
- .claude-plugin/marketplace.json
- plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/SingleInstanceGate.cs
- docs/COMPATIBILITY.md
- docs/decisions/0006-static-companion-snapshot-model.md
- plugins/app-it-windows/skills/app-it-windows/templates/app-it.config.example.json
- plugins/app-it-static/skills/app-it-static/templates/desktop-quit.sh
- plugins/app-it-static/skills/app-it-static/templates/desktop-install.sh
- plugins/app-it/skills/app-it/templates/desktop-install.sh
- plugins/app-it-static/skills/app-it-static/templates/static-server.py
- plugins/app-it-static/skills/app-it-static/templates/placeholder-icon-gen.sh
- plugins/app-it/skills/app-it/templates/placeholder-icon-gen.sh
- plugins/app-it-static/skills/app-it-static/templates/desktop-icons.sh
- plugins/app-it/skills/app-it/templates/desktop-icons.sh
- AGENTS.md
- plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/HostConfig.cs
- plugins/app-it/skills/app-it/templates/desktop-quit.sh
- plugins/app-it/skills/app-it/templates/fsa-polyfill-template.js
- plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/DevServer.cs
- plugins/app-it-static/skills/app-it-static/templates/run-template-static-server.sh
- docs/WINDOWS.md
code_chars_analyzed: 139380
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
      <span class="scope-stat__value">约 139,380 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">plugins/app-it/.claude-plugin/plugin.json</code></li><li><code class="path-chip">plugins/app-it-static/.claude-plugin/plugin.json</code></li><li><code class="path-chip">plugins/app-it-windows/.claude-plugin/plugin.json</code></li><li><code class="path-chip">SECURITY.md</code></li><li><code class="path-chip">.agents/plugins/marketplace.json</code></li><li><code class="path-chip">docs/decisions/README.md</code></li><li><code class="path-chip">docs/decisions/0003-bundle-id-prefix.md</code></li><li><code class="path-chip">plugins/app-it/.codex-plugin/plugin.json</code></li><li><code class="path-chip">docs/decisions/0002-macos-only-scope.md</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">docs/decisions/REJECTED/auto-attach-to-a-running-server.md</code></li><li><code class="path-chip">docs/decisions/0004-daemon-mode-lifecycle.md</code></li><li><code class="path-chip">plugins/app-it-windows/skills/app-it-windows/templates/wrapper-windows/README.md</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>本地 Web 项目开发时，开发者需反复在终端执行 <code class="code-ref">npm run dev</code>，然后在浏览器中打开地址，窗口散落各处没有 Dock 图标，关闭后端口不会自动释放。每次重启都冷启动，浪费数秒到数秒不等。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目由三个 sibling plugin 组成——<code class="code-ref">app-it</code>（macOS 开发模式，运行 dev server）、<code class="code-ref">app-it-static</code>（macOS 成品模式，serve 静态构建产物）、<code class="code-ref">app-it-windows</code>（Windows beta scaffold）。每个 plugin 同时为 Claude Code 和 Codex 提供 manifest（<code class="code-ref">.claude-plugin/plugin.json</code> 和 <code class="code-ref">.codex-plugin/plugin.json</code>）。核心链路是：读取目标项目的 <code class="code-ref">app-it.config.json</code> → 检测项目类型和端口 → 生成原生 Swift WKWebView wrapper → 编译为 universal <code class="code-ref">.app</code> → ad-hoc 签名 → 安装到 <code class="code-ref">~/Applications/App It/</code>。</p>
<p class="audit-callout audit-callout--highlight">进程生命周期设计精巧。<code class="code-ref">docs/decisions/0004-daemon-mode-lifecycle.md</code> 明确了「窗口关闭保持 dev server 温热、⌘Q 彻底销毁」的双态模型。Swift wrapper 区分 <code class="code-ref">windowShouldClose</code>（仅隐藏窗口）和 <code class="code-ref">applicationShouldTerminate</code>（杀掉整棵进程树释放端口），不是靠猜测信号而是由 AppKit 生命周期驱动决策。<code class="code-ref">desktop-quit.sh</code> 中的 <code class="code-ref">sweep_port</code> 函数（<code class="code-ref">plugins/app-it/skills/app-it/templates/desktop-quit.sh:约第48行</code>）实现了三阶段清理：TERM 录制的 PID 树 → lsof 扫描端口残留 → 1.5s 后 SIGKILL 兜底。</p>
<p class="audit-callout audit-callout--highlight">防被动附着安全门设计。<code class="code-ref">docs/decisions/REJECTED/auto-attach-to-a-running-server.md</code> 记录了一个被拒绝但非常有思考深度的方案——直接端口匹配附着已有服务器。他们选择了 descendant-walk reattach 门控：录制的 supervisor PID 必须存活、监听端口的进程必须在其后代进程树中（向上走 4 层）、且必须返回 HTTP 响应。这避免了两个项目共享端口区间时「把别人的 UI 加载到我的窗口」的问题。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">wrapper.swift</code> 源码和 <code class="code-ref">run-template.sh</code>（macOS 主 launcher 脚本）。code_bundle 中包含了大量 shell 模板（desktop-build、desktop-quit、desktop-install 等），但最关键的 Swift WKWebView wrapper 和主 launcher run-template 未在文件列表中出现，无法验证 ADR 中描述的 descendant-walk reattach 和 daemon-mode 的具体实现。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">eval &quot;$cmd&quot;</code> 的使用。<code class="code-ref">plugins/app-it-static/skills/app-it-static/templates/desktop-rebuild.sh:第37行</code> 通过 <code class="code-ref">eval &quot;$cmd&quot;</code> 执行 <code class="code-ref">app-it.config.json</code> 中的 <code class="code-ref">build_command</code>，而该命令来源于用户配置文件。虽然这是本地工具、风险较低，但 shell injection 面（config 被恶意修改时）缺乏验证。</p>
<p>适合日常在 macOS 上开发 Web 应用且希望 Dock 图标归属于自己而非 Chrome 的开发者试用。安装前确认已安装 Xcode Command Line Tools（<code class="code-ref">xcode-select --install</code>）。Windows 用户目前不应依赖此工具——Windows plugin 明确标注为未经真实硬件测试的 beta scaffold。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目创建仅 1 天，26 次 commit 集中在同一批发布，尚无社区贡献历史，维护者单点风险高</li><li>Windows plugin 自述未经真实硬件验证（<code class="code-ref">docs/WINDOWS.md</code>），CI 仅验证编译和 lint，运行时行为全部标记为 deferred</li><li>核心 Swift wrapper 和主 launcher run-template.sh 未在 code_bundle 中提供，无法验证实际进程管理和端口处理的健壮性</li><li>ad-hoc 签名的 .app 包在 macOS Gatekeeper 策略收紧时可能无法打开（desktop-install.sh 中有 xattr 清理但无 notarization）</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Claude Code 和 Codex 的插件分发，锁定了 AI 编码助手生态的早期用户群体，与这些工具的「用自然语言触发操作」范式高度契合。若 AI 编码助手市场持续增长，此类垂直 workflow 插件有持续获客潜力，但受限于 macOS-only 且无分发/商业化路径。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.45</span>
  </div>
</div>
</section>