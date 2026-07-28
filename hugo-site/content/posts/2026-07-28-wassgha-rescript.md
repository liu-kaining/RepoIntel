---
title: '[Score: 78.9] wassgha/rescript'
date: '2026-07-28T16:38:39Z'
categories:
- Media Editor
tags:
- video-editing
- whisper
- transcription
- browser
- ffmpeg.wasm
- react
intel_score: 78.9
repo_name: wassgha/rescript
repo_link: https://github.com/wassgha/rescript
summary: 基于Whisper本地转录的浏览器端视频编辑器，通过删除文字实现音视频剪辑，全程离线不离开设备。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/deploy.yml
- lib/media.ts
- lib/fillers.ts
- lib/types.ts
- lib/autosave.ts
- lib/edits.ts
- lib/models.ts
- lib/vad.ts
- lib/hallucinations.ts
- lib/projects.ts
- lib/ffmpeg.ts
- lib/parseTranscript.ts
- lib/store.ts
- app/page.tsx
- scripts/projects-test.ts
- tsconfig.json
- components/SideRail.tsx
- next.config.ts
- scripts/hallucination-test.ts
- components/GitHubLink.tsx
- scripts/parse-transcript-test.ts
- app/layout.tsx
- scripts/vad-test.ts
- hooks/useCrossOriginIsolated.ts
- hooks/useTranscriber.ts
- components/TopBar.tsx
- scripts/vad-regression-test.ts
- components/Editor.tsx
- README.md
- components/ExportDialog.tsx
- PLAN.md
- components/MediaPreview.tsx
- components/ImportTranscriptOption.tsx
- components/Timeline.tsx
- components/ModelSelector.tsx
- components/UploadScreen.tsx
- components/TranscriptPanel.tsx
- workers/transcription.worker.ts
code_chars_analyzed: 186070
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
      <span class="scope-stat__value">约 186,070 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/deploy.yml</code></li><li><code class="path-chip">lib/media.ts</code></li><li><code class="path-chip">lib/fillers.ts</code></li><li><code class="path-chip">lib/types.ts</code></li><li><code class="path-chip">lib/autosave.ts</code></li><li><code class="path-chip">lib/edits.ts</code></li><li><code class="path-chip">lib/models.ts</code></li><li><code class="path-chip">lib/vad.ts</code></li><li><code class="path-chip">lib/hallucinations.ts</code></li><li><code class="path-chip">lib/projects.ts</code></li><li><code class="path-chip">lib/ffmpeg.ts</code></li><li><code class="path-chip">lib/parseTranscript.ts</code></li><li><code class="path-chip">lib/store.ts</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>传统视频编辑需复杂时间线操作且常需上传云端，过程繁琐有隐私风险；此工具用语音转文字实现文档式剪辑，本地处理保隐私。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用基于Next.js静态导出，主组件Editor.tsx开启流水线：先加载ffmpeg.wasm提取音频（<code class="code-ref">lib/ffmpeg.ts:12</code>处检查SharedArrayBuffer），然后在Web Worker中运行Whisper进行词级转录并分配说话人（<code class="code-ref">workers/transcription.worker.ts</code>），结果通过zustand store（<code class="code-ref">lib/store.ts</code>）管理，播放器实时跳过删除区间（<code class="code-ref">components/MediaPreview.ts</code>x）并最终通过ffmpeg重编码导出。</p>
<p class="audit-callout audit-callout--highlight">精心设计的幻觉抑制模块（<code class="code-ref">lib/hallucinations.ts</code>）通过n-gram折叠、短语过滤和尾部退化修剪，显著提升长音频转录质量。</p>
<p class="audit-callout audit-callout--highlight">离线策略完整，模型首次下载后缓存至Cache Storage，所有处理均在本地，通过COOP/COEP实现SharedArrayBuffer，且提供静态导出部署方案。</p>
<p class="audit-callout audit-callout--doubt">大量关键逻辑集中在前端，未发现任何后端/服务端代码，但文件上传处理依赖浏览器File API，大文件（&gt;500MB）可能触发内存压力，未审阅到分片或流式处理。</p>
<p class="audit-callout audit-callout--doubt">测试仅覆盖少量工具函数（<code class="code-ref">scripts/parse-transcript-test.ts</code>等），核心流水线（如转录Worker与ffmpeg交互）缺乏集成测试，且UI组件无测试。</p>
<p>适用于需要快速粗剪的播客制作者或视频博主，可作为DeskCut等工具的离线替代，但生产环境需注意浏览器支持与性能优化。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>浏览器兼容性要求高：需要SharedArrayBuffer和WebGPU/WASM，仅Chrome系体验最佳。</li><li>大视频处理耗时：ffmpeg.wasm重编码在浏览器中缓慢，长视频导出可能需要数倍时长。</li><li>未引用 README 原文依据（缺「」或 README/文档 指称）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>提供一种尊重隐私的视频编辑体验，可能吸引注重数据安全的个人用户和小型团队，但离商业化尚有距离，可作为开源社区项目持续积累口碑。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.9</span>
  </div>
</div>
</section>