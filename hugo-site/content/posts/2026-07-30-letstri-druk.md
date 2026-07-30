---
title: '[Score: 79.9] letstri/druk'
date: '2026-07-30T11:04:40Z'
categories:
- Terminal Code Editor
tags:
- TUI
- tree-sitter
- Bun
- OpenTUI
- syntax-highlighting
- git-integration
intel_score: 79.9
repo_name: letstri/druk
repo_link: https://github.com/letstri/druk
summary: 一个面向终端的代码编辑器，具有文件树、标签页、tree-sitter 语法高亮和鼠标支持，安装为单二进制文件，无需运行时依赖。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/release.yml
- src/index.tsx
- src/themes/index.ts
- src/languages/index.ts
- src/assets.d.ts
- src/main.tsx
- src/ui/TextInput.tsx
- src/app/context.ts
- src/themes/types.ts
- src/ui/Overlay.tsx
- src/core/clipboard.ts
- src/editor/window.ts
- src/app/status.ts
- src/editor/changes.ts
- src/ui/CompareFilter.tsx
- src/app/types.ts
- src/editor/problems.ts
- src/ui/PromptModal.tsx
- src/ui/UpdateBanner.tsx
- src/ui/ConfirmModal.tsx
- src/themes/dracula.ts
- src/themes/vesper.ts
- src/themes/nord.ts
- src/themes/gruvbox-dark.ts
- src/themes/gruvbox-light.ts
- src/themes/tokyo-night.ts
- src/themes/kanagawa-wave.ts
- src/themes/kanagawa-lotus.ts
- src/themes/catppuccin-latte.ts
- src/themes/catppuccin-mocha.ts
- src/themes/kanagawa-dragon.ts
- src/themes/ayu-dark.ts
- src/themes/ayu-light.ts
- src/themes/catppuccin-frappe.ts
- src/themes/ayu-mirage.ts
- src/themes/catppuccin-macchiato.ts
- src/themes/rose-pine.ts
- src/themes/rose-pine-moon.ts
- src/themes/solarized-dark.ts
- src/themes/one-dark.ts
- src/core/update.ts
- src/ui/modal.ts
- src/themes/rose-pine-dawn.ts
- src/themes/everforest-dark.ts
- src/themes/everforest-light.ts
- src/lsp/transport.ts
- src/themes/solarized-light.ts
code_chars_analyzed: 90428
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
      <span class="scope-stat__value">约 90,428 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/index.tsx</code></li><li><code class="path-chip">src/themes/index.ts</code></li><li><code class="path-chip">src/languages/index.ts</code></li><li><code class="path-chip">src/assets.d.ts</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src/ui/TextInput.tsx</code></li><li><code class="path-chip">src/app/context.ts</code></li><li><code class="path-chip">src/themes/types.ts</code></li><li><code class="path-chip">src/ui/Overlay.tsx</code></li><li><code class="path-chip">src/core/clipboard.ts</code></li><li><code class="path-chip">src/editor/window.ts</code></li><li><code class="path-chip">src/app/status.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在 SSH 远程服务器或本地终端中需要快速编辑代码，却受限于缺少现代编辑体验（鼠标、代码高亮、文件树），现有终端编辑器配置繁琐且高亮不准确。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro"><code class="code-ref">src/index.ts</code>x:12 解析命令行参数并动态导入 <code class="code-ref">src/main.ts</code>x，其中 main() 函数初始化配置、主题和 Tree‑sitter 高亮 worker，然后渲染基于 @opentui/solid 的 App 组件。AppContext（<code class="code-ref">src/app/context.ts</code>）集中管理状态，各个功能模块通过接口解耦。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/editor/window.ts:12</code> 的 logicalWindow 函数处理了软换行场景，通过 lineAt 将可视行映射回逻辑行，避免长文件滚动时高亮丢失，解决了终端编辑器常见的行号偏移问题。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/lsp/transport.ts:28</code> 的 createDecoder 实现了符合 LSP 协议的 JSON‑RPC 分帧解码，使用 Buffer 缓冲字节流，容错地跳过无法解析的消息，保证了与语言服务器的可靠通信。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 tests 目录，package.json 中测试命令 bun <code class="code-ref">scripts/test.ts</code> 对应的脚本未包含在源码 bundle 中，单元测试覆盖情况不明，工程质量需谨慎评估。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/core/clipboard.ts:6</code> 通过 spawnSync 调用外部剪贴板工具（pbcopy/xclip 等）并设置 2000ms 超时，但未实现 README 所述的 OSC52 序列回退，在无上述工具的简化环境中可能静默失败。</p>
<p>适合需要轻量终端 IDE 的场景，可与 tmux 集成；建议优先补充核心模块的单元测试，并添加 OSC52 剪贴板实现以提升跨平台一致性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目创建仅 5 天，API 和体验可能快速变化，不适合生产环境依赖。</li><li>依赖 Bun 构建且发布二进制文件，未来若 Bun 生态变迁可能导致安装困难。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为免费工具，生态影响力有限，但可吸引注重终端效率的开发者，未来若扩展 LSP 深度集成或成为特定工作流的首选编辑器。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.9</span>
  </div>
</div>
</section>