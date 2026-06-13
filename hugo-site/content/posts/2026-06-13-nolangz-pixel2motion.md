---
title: '[Score: 76.35] nolangz/pixel2motion'
date: '2026-06-13T22:01:37Z'
categories:
- AI-Assisted Motion Design Toolchain
tags:
- svg-animation
- logo-animation
- python-tooling
- css-keyframes
- motion-qa
- raster-to-vector
intel_score: 76.35
repo_name: nolangz/pixel2motion
repo_link: https://github.com/nolangz/pixel2motion
summary: 一套把像素 logo 转成可编辑 SVG 再编排 CSS 动效的 Python 脚本 + 参考文档集，面向需要可审查矢量拟合和可复用 motion
  产出的品牌设计开发者。
code_source: git
code_files_reviewed:
- agents/openai.yaml
- references/html-delivery-template.md
- scripts/svg_to_js_html.py
- scripts/render_overlay.py
- scripts/overlay_progress_strip.py
- references/ribbon-fitting.md
- references/motion-personality.md
- scripts/capture_motion_frames.py
- scripts/probe_motion_continuity.py
- scripts/animate_svg_html.py
- references/twelve-principles-for-logos.md
- README.md
- references/reveal-patterns.md
- scripts/raster_logo_trace.py
- scripts/fit_ribbon_centerline.py
- scripts/svg_path_audit.py
- scripts/animate_svg_showcase.py
- SKILL.md
code_chars_analyzed: 167656
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
      <span class="scope-stat__value">18 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 167,656 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">agents/openai.yaml</code></li><li><code class="path-chip">references/html-delivery-template.md</code></li><li><code class="path-chip">scripts/svg_to_js_html.py</code></li><li><code class="path-chip">scripts/render_overlay.py</code></li><li><code class="path-chip">scripts/overlay_progress_strip.py</code></li><li><code class="path-chip">references/ribbon-fitting.md</code></li><li><code class="path-chip">references/motion-personality.md</code></li><li><code class="path-chip">scripts/capture_motion_frames.py</code></li><li><code class="path-chip">scripts/probe_motion_continuity.py</code></li><li><code class="path-chip">scripts/animate_svg_html.py</code></li><li><code class="path-chip">references/twelve-principles-for-logos.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">references/reveal-patterns.md</code></li><li><code class="path-chip">scripts/raster_logo_trace.py</code></li><li class="path-more">另有 4 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>设计师在把位图 logo 做成 HTML 动效时，缺少一套可量化 QA 的流水线：SVG 拟合质量无法复现验证，CSS easing 被浏览器静默降级成 linear 而无人发现，最终帧和静态矢量之间缺乏像素级一致性校验——这些都导致返工和交付争议。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目由 8 个独立 CLI 脚本（<code class="code-ref">scripts/</code>）和 4 个参考文档（<code class="code-ref">references/</code>）组成，没有共享库或服务端。核心流水线是 Phase 2 几何拟合（<code class="code-ref">raster_logo_trace.py</code> → <code class="code-ref">render_overlay.py</code> → <code class="code-ref">svg_path_audit.py</code> → <code class="code-ref">overlay_progress_strip.py</code>）到 Phase 3 动效编排（<code class="code-ref">animate_svg_showcase.py</code> / <code class="code-ref">animate_svg_html.py</code> → <code class="code-ref">capture_motion_frames.py</code> → <code class="code-ref">probe_motion_continuity.py</code>）。各脚本通过 CLI 参数和文件系统松耦合，无进程间通信。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">scripts/fit_ribbon_centerline.py</code> 实现了一套针对自交叉变宽丝带（如∞形标记）的中心线拟合算法——Catmull-Rom 骨架 → 法线测量自动重定心 → 源像素亚像素边缘吸附 → 平滑三次贝塞尔轮廓，输出包含排除区弧分数（供下游 split draw-on 动效使用）。整个 380 行纯 NumPy/Pillow 实现，<code class="code-ref">fit_cubic</code> 用闭式最小二乘拟合，<code class="code-ref">snap_edges</code> 做双线性插值边缘检测，工程上自包含。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">scripts/probe_motion_continuity.py</code> 提供了两组定量 QA 探针——computed-style probe 检测 <code class="code-ref">@keyframes</code> 内 <code class="code-ref">var()</code> easing 被 Chromium 静默降级为 linear 的问题，ink-delta sweep 通过逐帧截图像素统计检测 stall+pop 签名。这是对 Chromium 浏览器行为的具体工程防御，非空谈。</p>
<p class="audit-callout audit-callout--doubt">整个项目**无任何自动化测试**——<code class="code-ref">tests/</code> 目录不存在，code_bundle 中 18 个文件无一包含 <code class="code-ref">assert</code>、<code class="code-ref">unittest</code>、<code class="code-ref">pytest</code> 等测试代码。<code class="code-ref">fit_ribbon_centerline.py</code> 的数学逻辑（Catmull-Rom 重定心、de Casteljau 细分）和 <code class="code-ref">probe_motion_continuity.py</code> 的浏览器交互依赖手工验证，回归风险高。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">scripts/raster_logo_trace.py</code> 的路径追踪算法基于简单像素邻接关系（<code class="code-ref">trace_mask</code> 中逐像素构建边缘图），对复杂拓扑（如高对比度反走样边缘、渐变区域）的鲁棒性未经验证。<code class="code-ref">svg_path_audit.py</code> 的 <code class="code-ref">parse_path</code> 使用正则表达式 COMMAND_RE 解析 SVG path data，对科学计数法 token 的处理依赖浮点正则，边界情况（如连续命令省略、负号分隔数字）未见防护。</p>
<p>该仓库本质是一个「AI 编排脚本 + 知识库」，不是可独立运行的工具。用户需配合 Codex/Claude 作为调度引擎使用 SKILL.md 中的指令。若要在生产中采用，建议：(1) 为 <code class="code-ref">fit_ribbon_centerline.py</code> 和 <code class="code-ref">probe_motion_continuity.py</code> 添加快照测试覆盖关键数学分支；(2) 将 <code class="code-ref">references/</code> 中的知识（motion-personality token 映射、reveal-pattern 模板）提取为机器可读配置而非纯 Markdown，实现参数化。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 标注创建于 2026-06-12 且仅 1 天 repo age、18 次 commit，社区尚未检验，健康度数据极度稀疏。</li><li>全部脚本无测试覆盖，核心数学逻辑（Catmull-Rom 拟合、de Casteljau 细分）仅靠手工验证，变更回归风险高。</li><li>SKILL.md 是面向 LLM 的指令文档而非 API，对 Codex/Claude 的 prompt 工程依赖极强，模型版本变化可能导致行为漂移。</li><li>依赖链：Pillow + numpy + headless Chrome + Playwright，<code class="code-ref">fit_ribbon_centerline.py</code> 顶层执行代码不在 <code class="code-ref">__main__</code> 保护内（<code class="code-ref">args = parse_args()</code> 直接在模块级执行），导入即运行。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>该项目面向品牌设计师和前端开发者的小众但真实需求——将位图 logo 转为可审查的矢量动效交付物。作为 Claude/Codex skill 发布，商业价值取决于 AI 编排质量；单独使用脚本的门槛较高（需 headless Chrome + Playwright），难以直接变现。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">64</div>
  <div class="score-bar"><span style="width:64%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.35</span>
  </div>
</div>
</section>