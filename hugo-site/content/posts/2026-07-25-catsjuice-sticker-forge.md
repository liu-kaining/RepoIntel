---
title: '[Score: 78.5] CatsJuice/sticker-forge'
date: '2026-07-25T08:02:16Z'
categories:
- Interactive WebGL Sticker Maker
tags:
- WebGL
- sticker
- animation export
- procedural audio
- background removal
- shader
intel_score: 78.5
repo_name: CatsJuice/sticker-forge
repo_link: https://github.com/CatsJuice/sticker-forge
summary: 将文字或图像变为可拖拽撕揭的 WebGL 贴纸，支持实时材质/阴影，并导出 GIF、APNG、透明 ProRes MOV 动画。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/deploy-pages.yml
- db/index.ts
- worker/index.ts
- lib/standalone.ts
- lib/assets.d.ts
- lib/random-id.ts
- lib/export-worker-types.ts
- lib/gifenc.d.ts
- lib/gallery-types.ts
- lib/export-worker-client.ts
- lib/heic.ts
- lib/particle-debug.ts
- lib/laser-debug.ts
- lib/gallery-view.ts
- lib/material-preview.ts
- lib/export-audio.ts
- lib/background-removal.ts
- lib/gallery-preview.ts
- lib/types.ts
- lib/gallery-storage.ts
- lib/source.ts
- lib/export-encoders.ts
- lib/peel-audio.ts
- lib/shaders.ts
- drizzle/meta/_journal.json
- cloudflare-env.d.ts
- .openai/hosting.json
- drizzle.config.ts
- db/schema.ts
- heic-decode.d.ts
- examples/d1/db/schema.ts
- public/models/BritishWerewolf/U-2-Netp/config.json
- app/page.tsx
- app/MobileDemoMode.tsx
- tsconfig.json
- next.config.ts
- vite.lib.config.ts
- public/models/BritishWerewolf/U-2-Netp/SOURCE.md
- app/GalleryPreviewImage.tsx
- THIRD_PARTY_NOTICES.md
- examples/d1/app/api/notes/route.ts
- vite.config.ts
- app/layout.tsx
- app/GalleryQuickEditFlight.tsx
- app/chatgpt-auth.ts
- app/ColorPicker.tsx
- app/TouchVisualizer.tsx
code_chars_analyzed: 191909
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
      <span class="scope-stat__value">约 191,909 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/deploy-pages.yml</code></li><li><code class="path-chip">db/index.ts</code></li><li><code class="path-chip">worker/index.ts</code></li><li><code class="path-chip">lib/standalone.ts</code></li><li><code class="path-chip">lib/assets.d.ts</code></li><li><code class="path-chip">lib/random-id.ts</code></li><li><code class="path-chip">lib/export-worker-types.ts</code></li><li><code class="path-chip">lib/gifenc.d.ts</code></li><li><code class="path-chip">lib/gallery-types.ts</code></li><li><code class="path-chip">lib/export-worker-client.ts</code></li><li><code class="path-chip">lib/heic.ts</code></li><li><code class="path-chip">lib/particle-debug.ts</code></li><li><code class="path-chip">lib/laser-debug.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>设计师制作具有真实物理撕揭感与动态光影的贴纸效果时，通常需要 Photoshop/After Effects 等非实时工作流，且难以在 Web 上直接交互生成透明动画。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分为 <code class="code-ref">app/</code> 交互界面与 <code class="code-ref">lib/</code> 独立库。<code class="code-ref">lib/source.ts:prepareArtwork</code> 将文字或图片渲染成带外轮廓的标准 Canvas，提取 alpha 通道和轮廓支撑数据后传入 WebGL 渲染器（未审阅到核心 sticker-forge.ts）。用户交互驱动 peel 进度，<code class="code-ref">lib/shaders.ts</code> 中的顶点着色器通过 <code class="code-ref">deformSticker()</code> 计算弯曲网格，片段着色器使用 <code class="code-ref">applyFrontMaterial()</code> 应用全息/闪光等材质。导出时，<code class="code-ref">lib/export-worker-client.ts</code> 将帧数组传入 Web Worker，<code class="code-ref">lib/export-encoders.ts</code> 完成 GIF/APNG/MOV 编码，并可多路复用 <code class="code-ref">lib/export-audio.ts</code> 生成的 PCM 音频。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">lib/export-encoders.ts</code> 实现了浏览器端稀缺的透明 ProRes 4444 MOV 编码及 PCM 音频多路复用（<code class="code-ref">muxPcmAudioIntoMov</code>），并含有 GIF 边缘颜色修复算法 <code class="code-ref">repairTransparentEdgeColors</code>。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">lib/shaders.ts</code> 的片段着色器内建 <code class="code-ref">applyFrontMaterial</code> 材质系统，将全息、闪光、反射等效果与贴纸弯曲变形（<code class="code-ref">deformSticker</code>）统一在 GPU 中计算，保证了物理一致性。</p>
<p class="audit-callout audit-callout--doubt">核心 Web 组件 <code class="code-ref">lib/sticker-forge.ts</code> 未在代码包中提供，无法评估 Three.js 场景管理、pointer 事件处理与 peel 进度的衔接逻辑，可能存在紧耦合或状态管理缺陷。</p>
<p class="audit-callout audit-callout--doubt">代码包完全缺失 <code class="code-ref">tests/</code> 目录，尽管 <code class="code-ref">package.json</code> 指定了 <code class="code-ref">node --test tests/*.test.mjs</code>，但无测试文件，无法保证编码管线、音效引擎等关键功能的正确性。</p>
<p>可作为 SaaS 工具的基础，增加账户系统和素材库，面向电商营销团队提供品牌贴纸动画生成，需优先补充测试与核心渲染层的文档。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>背景移除依赖 HuggingFace 模型（4.5MB ONNX），首次加载慢，低端设备可能推理失败。</li><li>项目仅创建4天，无社区贡献，核心渲染未开源审查，维护持续性存疑。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>开源实现可作为交互式贴纸生成服务的起点，若封装为 API 或 SaaS，可服务需要品牌化贴纸动画的营销人员，但市场竞争依赖快速迭代与用户增长。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.5</span>
  </div>
</div>
</section>