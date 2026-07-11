---
title: '[Score: 79.65] wassermanproductions/motion-previs-studio'
date: '2026-07-11T21:45:17Z'
categories:
- AI Film Previsualization Tool
tags:
- ai-film
- pose-estimation
- camera-solving
- motion-capture
- openpose
- mcp
intel_score: 79.65
repo_name: wassermanproductions/motion-previs-studio
repo_link: https://github.com/wassermanproductions/motion-previs-studio
summary: 将参考视频转换为相机运动、骨架与深度控制数据的桌面应用，帮助AI电影导演精准驱动生成管线。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- .github/workflows/macos-package.yml
- .github/workflows/windows-package.yml
- src/vite-env.d.ts
- src/main.tsx
- src/global.d.ts
- src/types.ts
- src/components/PoseCanvas.tsx
- src/lib/sessionRestore.ts
- src/control/registry.ts
- src/lib/quality.ts
- src/lib/frameEncoder.ts
- src/lib/poseVideo.ts
- src/components/ThreePreview.tsx
- src/control/handler.ts
- src/lib/aiDepth.ts
- src/lib/openpose.ts
- src/lib/pose.ts
- src/lib/cameraMotion.ts
- tsconfig.json
- vite.config.ts
- public/README.md
- MODIFICATIONS.md
- THIRD_PARTY_NOTICES.md
- docs/WINDOWS_PRERELEASE_CHECKLIST.md
- AGENTS.md
- ASSET_MANIFEST.json
- mcp/README.md
- README.md
code_chars_analyzed: 155206
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
      <span class="scope-stat__value">30 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 155,206 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/macos-package.yml</code></li><li><code class="path-chip">.github/workflows/windows-package.yml</code></li><li><code class="path-chip">src/vite-env.d.ts</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src/global.d.ts</code></li><li><code class="path-chip">src/types.ts</code></li><li><code class="path-chip">src/components/PoseCanvas.tsx</code></li><li><code class="path-chip">src/lib/sessionRestore.ts</code></li><li><code class="path-chip">src/control/registry.ts</code></li><li><code class="path-chip">src/lib/quality.ts</code></li><li><code class="path-chip">src/lib/frameEncoder.ts</code></li><li><code class="path-chip">src/lib/poseVideo.ts</code></li><li class="path-more">另有 16 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI视频生成工具缺乏对真实镜头相机运动和主体动作的精确控制，导演难以在保持原有镜头感的同时替换元素，导致生成结果不可控。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Electron + React + TypeScript 桌面应用。渲染器端直接运行 MediaPipe Pose 和 Depth Anything 模型，通过 <code class="code-ref">src/lib/pose.ts</code> 和 <code class="code-ref">src/lib/aiDepth.ts</code> 离线提取每帧姿态和深度；相机运动求解在 <code class="code-ref">src/lib/cameraMotion.ts</code> 中实现，使用 Shi-Tomasi 角点检测、金字塔 Lucas-Kanade 光流跟踪，并利用姿势关键点生成的蒙版排除人体区域（<code class="code-ref">buildSubjectMask</code>），通过种子 LCG 的 RANSAC 估计相似变换，累计为摇移/推拉/旋转参数。所有控制视频采用确定性帧编码（<code class="code-ref">src/lib/frameEncoder.ts</code>），逐帧绘制为 PNG 后经 IPC 发送至主进程的 ffmpeg 合成，不再依赖不可靠的 <code class="code-ref">captureStream</code>。OpenPose BODY_25 导出模块（<code class="code-ref">src/lib/openpose.ts</code>）完成了 33→25 关键点映射与骨架绘制。代理控制通过 <code class="code-ref">src/control/handler.ts</code> 白名单分发动作到 <code class="code-ref">window.__mps</code> 表面，与 UI 同逻辑，并通过本地 HTTP 服务器和零依赖 MCP 桥接实现 AI 驱动。</p>
<p class="audit-callout audit-callout--highlight">相机求解中的主体遮罩创新：<code class="code-ref">src/lib/cameraMotion.ts</code> 中的 <code class="code-ref">buildSubjectMask</code> 根据姿势关键点（头、肢体）生成膨胀胶囊蒙版，确保角点检测仅从背景中选取，实现了主体无关的相机运动恢复，显著优于传统全局运动估计。</p>
<p class="audit-callout audit-callout--highlight">确定性帧编码流水线：<code class="code-ref">src/lib/frameEncoder.ts</code> 提供了完整的 <code class="code-ref">encodeFrames</code> 函数，替换了 <code class="code-ref">captureStream</code>，确保帧计数精确，输出可重现的 H.264 MP4，并通过 <code class="code-ref">AbortSignal</code> 支持中途取消。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">electron/</code> 主进程代码（如 main.cjs、preload.cjs、security.cjs），无法验证 <code class="code-ref">mps://</code> 协议的安全实现和 IPC 白名单的具体边界；README 声称的“Security hardening”未能从源码核实。</p>
<p class="audit-callout audit-callout--doubt">AI 深度使用固定的 Depth Anything Small 模型（<code class="code-ref">src/lib/aiDepth.ts</code>），限制输入分辨率为 384px，可能丢失细节；且首次运行需下载模型，无进度指示超时会阻塞。</p>
<p>若团队需批量生产，可集成队列管理；当前单任务依赖全局状态（窗口.__mps），多项目隔离不足。建议提供 headless 模式以便 CI/CD 集成。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅发布5天，无社区维护者或贡献者积累，长期可持续性存疑。</li><li>依赖外部二进制（ffmpeg/yt-dlp）和运行时模型下载，离线或企业环境部署困难。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>填补了参考视频到 AI 生成控制数据的工具空白，可成为专业影视预可视化流程的标准环节，并可通过集成 MCP 进入自动化制片管线。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.65</span>
  </div>
</div>
</section>