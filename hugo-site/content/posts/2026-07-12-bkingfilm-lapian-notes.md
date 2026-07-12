---
title: '[Score: 76.6] bkingfilm/lapian-notes'
date: '2026-07-12T19:01:05Z'
categories:
- Film Analysis Tool
tags:
- React
- Vite
- FFmpeg
- AI Integration
- Browser Local Storage
- Film Deconstruction
intel_score: 76.6
repo_name: bkingfilm/lapian-notes
repo_link: https://github.com/bkingfilm/lapian-notes
summary: 本地电影拉片工具，自动抽帧、配字幕、生成AI分析包，导回结果后呈现剧情泳道、结构树与情绪曲线。
code_source: git
code_files_reviewed:
- package.json
- src/main.tsx
- src/types.ts
- src/lib/aiTime.ts
- src/lib/timecode.ts
- src/lib/frameFileName.ts
- src/lib/macroProgress.ts
- src/lib/segmentQuality.ts
- src/lib/autosave.ts
- src/lib/segmentProgress.ts
- src/lib/segmentCoverage.ts
- src/lib/glossary.ts
- src/lib/autoSubtitle.ts
- src/components/BeginnerGuide.tsx
- src/lib/timelineBlock.ts
- src/lib/transcode.ts
- src/components/ProjectLibrary.tsx
- src/lib/projectStore.ts
- src/components/WorkflowGuide.tsx
- src/lib/videoSubtitles.ts
- src/lib/srt.ts
- src/components/Toolbar.tsx
- src/lib/storyLines.ts
- src/lib/frameStore.ts
- src/lib/videoFrames.ts
- src/lib/screenplayResearch.ts
- src/lib/project.ts
- src/lib/storyStructure.ts
- src/lib/aiImport.ts
- src/lib/markdown.ts
- src/lib/framePackage.ts
- src/components/InspectorPanel.tsx
- src/components/FrameTimeline.tsx
- tsconfig.json
- vite.config.ts
- tsconfig.node.json
- eslint.config.js
- tsconfig.app.json
- README.en.md
- README.md
- transcode-server-plugin.ts
- subtitle-server-plugin.ts
code_chars_analyzed: 242903
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
      <span class="scope-stat__value">42 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 242,903 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src/types.ts</code></li><li><code class="path-chip">src/lib/aiTime.ts</code></li><li><code class="path-chip">src/lib/timecode.ts</code></li><li><code class="path-chip">src/lib/frameFileName.ts</code></li><li><code class="path-chip">src/lib/macroProgress.ts</code></li><li><code class="path-chip">src/lib/segmentQuality.ts</code></li><li><code class="path-chip">src/lib/autosave.ts</code></li><li><code class="path-chip">src/lib/segmentProgress.ts</code></li><li><code class="path-chip">src/lib/segmentCoverage.ts</code></li><li><code class="path-chip">src/lib/glossary.ts</code></li><li><code class="path-chip">src/lib/autoSubtitle.ts</code></li><li><code class="path-chip">src/components/BeginnerGuide.tsx</code></li><li class="path-more">另有 28 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>电影创作者想系统拆解叙事结构，但手工截图、对字幕、整理分析耗时巨大；AI分析潜力未被整合到拉片流程中。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分三块：浏览器端React UI（src/components/）、业务逻辑库（src/lib/）、两个Vite服务端插件（transcode-server-plugin.ts、subtitle-server-plugin.ts）提供本地转码和字幕搜索。导入电影后，前端调videoFrames.ts:extractVideoFrames按1秒间隔canvas抽帧；同时调autoSubtitle.ts:fetchAutoSubtitle，通过dev server代理搜索assrt.net字幕。转码和字幕搜索失败时均有fallback（transcode.ts:probeVideoPlayable、autoSubtitle.ts:404返回null）。AI分析包生成在framePackage.ts:exportAiAnalysisPackage，将帧图、字幕打包ZIP（纯JS实现ZIP生成，见framePackage.ts:createZip），并附带prompt.md、schema.json。导入AI结果通过aiImport.ts:importAiAnalysis严格解析JSON，校验电影匹配（validateImportedMovieMatch），并规范化时间码（parseAiTime）。时间轴可视化在FrameTimeline.tsx，用泳道图（TimelineSwimlane）展示段落，并内嵌情绪曲线（EmotionCurveLane）。</p>
<p class="audit-callout audit-callout--highlight">AI结果导入具有健壮性。aiImport.ts:186-220包含智能JSON解析（处理markdown代码块、残缺JSON修复repairLooseJson），并自动映射旧版故事线ID（storyLines.ts:legacyLineIds），降低导入失败率。</p>
<p class="audit-callout audit-callout--highlight">浏览器端纯JS实现的ZIP打包。framePackage.ts:createZip不依赖第三方库，直接构建本地文件头和中心目录，且支持多入口字节流拼装。这使得AI分析包可以在浏览器端不调用服务端的情况下生成。</p>
<p class="audit-callout audit-callout--doubt">未审阅到任何测试文件或测试配置（无<code class="code-ref">__tests__</code>或<code class="code-ref">*.test.ts</code>）。所有lib函数仅依赖类型检查，无运行时单元测试覆盖，回归风险较高。</p>
<p class="audit-callout audit-callout--doubt">抽帧与字幕搜索依赖Vite dev server的API；静态部署（<code class="code-ref">npm run build</code>）后转码和字幕搜索会降级（README提及），但源码中未见到对静态部署模式的处理逻辑，用户可能在非dev环境下遇到功能缺失但缺乏明确提示（仅transcode.ts和autoSubtitle.ts的fetch静默返回null）。</p>
<p>适合个人创作者快速搭建电影拆解工作流，但建议补充核心lib的测试（至少对aiImport、srt、timecode等输入边界测试），并考虑将抽帧/转码逻辑设计为可选的Web Worker或Electron模式以脱离dev server限制。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅4天历史，无长期维护承诺，快速变化期可能破坏已有笔记格式。</li><li>完全依赖浏览器存储（localStorage + IndexedDB），数据易丢失且不支持跨设备同步，不适合严肃成果保存。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可拓展为电影教育SaaS或创作社群工具，但当前定位桌面单机工具，商业化需解决持久化与协作。</p>
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
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.6</span>
  </div>
</div>
</section>