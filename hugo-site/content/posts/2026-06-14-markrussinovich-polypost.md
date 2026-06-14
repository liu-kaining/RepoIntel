---
title: '[Score: 75.55] markrussinovich/Polypost'
date: '2026-06-14T19:22:58Z'
categories:
- Multi-Platform Post Editor
tags:
- TypeScript
- Rich Text
- TipTap
- Social Media
- LinkedIn
- Chrome Extension
intel_score: 75.55
repo_name: markrussinovich/Polypost
repo_link: https://github.com/markrussinovich/Polypost
summary: Polypost 是面向内容创作者的多平台帖子编辑器，支持一次撰写、针对 LinkedIn/X/Bluesky 等六个平台的字数计数与格式预览，并附带
  LinkedIn 浏览器扩展可直接发帖。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/pages.yml
- src/lib/platforms/index.ts
- src/vite-env.d.ts
- src/main.tsx
- src/App.tsx
- src/components/HelpPanel.tsx
- src/lib/useEscape.ts
- src/components/LinkedInPreview.tsx
- src/lib/clipboard.ts
- src/lib/theme.ts
- src/lib/feedPreview.test.ts
- src/lib/feedPreview.ts
- src/lib/constants.ts
- src/lib/constants.test.ts
- src/components/HelpModal.tsx
- src/extension/manifest.json
- src/components/PolypostMark.tsx
- src/components/CharacterMeter.tsx
- src/lib/truncation.ts
- src/components/CopyPanel.tsx
- src/components/PaneEditor.tsx
- src/lib/exportLinkedInText.ts
- src/components/ConfirmDialog.tsx
- src/components/ErrorBoundary.tsx
- src/lib/storage.test.ts
- src/lib/media.test.ts
- src/components/PlatformToggleChips.tsx
- src/lib/unicodeStyles.test.ts
- src/components/PromptDialog.tsx
- src/lib/counting.test.ts
- src/components/PlatformCard.test.tsx
- src/lib/workspace.ts
- src/lib/mentions.test.ts
- src/lib/editorConfig.ts
- src/lib/counting.ts
- src/lib/workspace.test.ts
- src/components/PlatformRail.test.tsx
- src/lib/mentions.ts
- src/components/EmojiPicker.tsx
- src/lib/importDocument.test.ts
- src/components/DraftHistoryPanel.tsx
- src/components/PlatformRail.tsx
- src/lib/sampleContent.ts
- src/lib/unicodeStyles.ts
- src/lib/workspaceStorage.test.ts
- src/lib/pastedHtml.test.ts
- src/lib/exportText.test.ts
code_chars_analyzed: 101488
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
      <span class="scope-stat__value">约 101,488 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/pages.yml</code></li><li><code class="path-chip">src/lib/platforms/index.ts</code></li><li><code class="path-chip">src/vite-env.d.ts</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src/App.tsx</code></li><li><code class="path-chip">src/components/HelpPanel.tsx</code></li><li><code class="path-chip">src/lib/useEscape.ts</code></li><li><code class="path-chip">src/components/LinkedInPreview.tsx</code></li><li><code class="path-chip">src/lib/clipboard.ts</code></li><li><code class="path-chip">src/lib/theme.ts</code></li><li><code class="path-chip">src/lib/feedPreview.test.ts</code></li><li><code class="path-chip">src/lib/feedPreview.ts</code></li><li><code class="path-chip">src/lib/constants.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>内容创作者在多个社交平台发布同一篇帖子时，需要反复手动调整字数、格式和换行；LinkedIn 不支持富文本格式，想加粗/斜体只能用 Unicode 变体字符，手动映射繁琐且易出错。每次从编辑器复制到各平台 composer 再检查字数，链路长、成本高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用采用 React + TipTap 作为主编辑器，通过 <code class="code-ref">src/lib/platforms/index.ts</code> 的 <code class="code-ref">renderForPlatform</code> 统一计算各平台的导出文本、字符计数和警告状态。字符计数在 <code class="code-ref">src/lib/counting.ts</code> 中实现三种方法：nfc-codepoints（LinkedIn 等）、graphemes（Bluesky 用 Intl.Segmenter）、x-weighted（按 X 的加权规则，URL 固定 23 字符）。每种平台定义了独立的 PlatformSpec（linkedinSpec/xSpec/blueskySpec 等），集中注册在 <code class="code-ref">PLATFORMS</code> 数组中。Workspace 状态管理在 <code class="code-ref">src/lib/workspace.ts</code> 中，采用 fork-on-edit 模型：用户编辑主文档后所有未 fork 的平台自动跟随；在某个平台卡片内编辑时通过 <code class="code-ref">applyPaneEdit</code> 仅 fork 该平台。AI 辅助功能通过 <code class="code-ref">src/lib/ai/fit.ts</code> 的 <code class="code-ref">generateFit</code> 和 <code class="code-ref">src/App.tsx:119</code> 的 <code class="code-ref">runAutofit</code> 实现，打字停顿 3 秒后自动调用用户自备的 LLM key 进行超限内容缩写。LinkedIn 扩展部分（<code class="code-ref">src/extension/manifest.json</code>）使用 Manifest V3 content script 注入 LinkedIn 页面，通过 shadow root 穿透找到原生 composer 并驱动发帖。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/lib/workspace.ts</code> 的 fork-on-edit 与 dormant 状态设计——禁用平台时 override 保留，重新启用时恢复自定义版本（<code class="code-ref">dormantPlatforms</code> 函数），<code class="code-ref">src/lib/workspace.test.ts</code> 中有完整覆盖，包括 toggle/resync/fork 隔离等场景。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/lib/pastedHtml.ts</code> 的 Word 粘贴清洗——针对 MsoNormal/MsoListParagraph 等 Office 专有 class 做了结构化转 &lt;ul&gt;/&lt;ol&gt; 的语义转换，<code class="code-ref">src/lib/pastedHtml.test.ts</code> 有 7 个用例覆盖了列表、空段落、&lt;o:p&gt; 标签剥离等边界。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/App.tsx</code> 承载了 workspace 状态、AI 生成、draft 历史、附件管理、设置面板等全部逻辑，组件超过 400 行，多个 async 操作（runAutofit、handleFit、handleAuthor）通过闭包引用 workspace 但依赖数组注释中有 eslint-disable（第 129 行），存在 stale closure 风险。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src/lib/ai/</code> 目录下的 fit.ts、llmClient.ts、prompts.ts、config.ts 等核心 AI 模块源码，本次结论不覆盖 AI 链路的具体实现质量。src/lib/platforms/ 下各平台 spec 文件（linkedin.ts、x.ts 等）仅看到 index.ts 的聚合入口，具体各平台的字符限制和 warning 规则未审阅到。</p>
<p>App.tsx 应拆分为 useWorkspace/useAiGeneration 等自定义 hook，降低单文件复杂度；AI 模块应增加 AbortController 取消传播到 LLM HTTP 层的端到端验证（当前 runAutofit 有 AbortController 但 fit.ts 内部是否真正传递 signal 未确认）；LinkedIn 扩展对 shadow root 的穿透方式属于脆弱耦合，LinkedIn 任何 DOM 结构变更都会导致发帖失败，建议加降级提示。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>AI 功能完全依赖用户自备 LLM key，README 未说明各模型的 token 消耗/费用估算，用户可能产生意外开销</li><li>LinkedIn 扩展通过 shadow root 穿透操纵原生 composer，LinkedIn 任何前端重构都会导致发帖功能失效且无降级方案</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为面向个人创作者的免费工具，直接商业变现路径有限，但 LinkedIn 浏览器扩展若积累用户量可作为社交增长工具的入口，AI 模块接入用户自有 key 的模式也适合未来做付费增值。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">69</div>
  <div class="score-bar"><span style="width:69%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.55</span>
  </div>
</div>
</section>