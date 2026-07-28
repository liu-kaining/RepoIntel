---
title: '[Score: 75.1] HUANGCHIHHUNGLeo/claude-real-video'
date: '2026-07-28T02:13:02Z'
categories:
- AI Agent Tools
tags:
- video-analysis
- llm
- python
- cli
- keyframe-extraction
intel_score: 75.1
repo_name: HUANGCHIHHUNGLeo/claude-real-video
repo_link: https://github.com/HUANGCHIHHUNGLeo/claude-real-video
summary: 为LLM提供本地视频预处理管线：场景感知关键帧提取、去重与转录，使模型能真正“观看”视频内容而非仅依赖字幕。
code_source: git
code_files_reviewed:
- pyproject.toml
- .github/workflows/ci.yml
- src/claude_real_video/__init__.py
- src/claude_real_video/__main__.py
- src/claude_real_video/export_llc.py
- src/claude_real_video/temporal_check.py
- src/claude_real_video/timeline_lite.py
- src/claude_real_video/speakers.py
- src/claude_real_video/viewer.py
- src/claude_real_video/cli.py
- src/claude_real_video/serve.py
- plugins/claude-real-video/.claude-plugin/plugin.json
- .github/ISSUE_TEMPLATE/feature_request.md
- .github/ISSUE_TEMPLATE/bug_report.md
- marketing/demo-20260719/rec-script.sh
- .claude-plugin/marketplace.json
- SECURITY.md
- ATTRIBUTIONS.md
- marketing/demo-20260719/SOURCE.md
- marketing/hn-reply-log-20260707.md
- marketing/demo-20260719/record_terminal.py
- CONTRIBUTING.md
- marketing/demo-20260719/run-free.md
- marketing/demo-20260719/STORYBOARD.md
- marketing/reddit/20260715-sideproject.md
- marketing/demo-20260719/record_pro.py
- marketing/ph/launch-copy-approved.md
- marketing/demo-20260719/crv-pro-out/motion.json
- plugins/claude-real-video/skills/claude-real-video/SKILL.md
- skills/claude-real-video/SKILL.md
- marketing/demo-20260719/run-pro.md
- capafy-staging/.claude/skills/claude-real-video/SKILL.md
- marketing/demo-20260719/record_viewers.py
- marketing/devto-draft-2-token-cost.md
- marketing/demo-20260719/crv-pro-out/transcript.json
- benchmark/run_benchmark.sh
- marketing/devto/20260715-devto-post.md
- marketing/demo-20260719/rec-out/transcript.json
- tests/test_smoke.py
- install-skill.sh
- marketing/round2-drafts-20260707.md
- marketing/platform-inventory-20260707.md
- CHANGELOG.md
- skills/claude-real-video-for-agents/SKILL.md
- marketing/demo-20260719/crv-pro-out/perception.json
- marketing/demo-20260719/crv-pro-out/frames.json
- benchmark/benchmark.md
- marketing/demo-20260719/rec-out/frames.json
code_chars_analyzed: 186853
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
      <span class="scope-stat__value">约 186,853 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">src/claude_real_video/__init__.py</code></li><li><code class="path-chip">src/claude_real_video/__main__.py</code></li><li><code class="path-chip">src/claude_real_video/export_llc.py</code></li><li><code class="path-chip">src/claude_real_video/temporal_check.py</code></li><li><code class="path-chip">src/claude_real_video/timeline_lite.py</code></li><li><code class="path-chip">src/claude_real_video/speakers.py</code></li><li><code class="path-chip">src/claude_real_video/viewer.py</code></li><li><code class="path-chip">src/claude_real_video/cli.py</code></li><li><code class="path-chip">src/claude_real_video/serve.py</code></li><li><code class="path-chip">plugins/claude-real-video/.claude-plugin/plugin.json</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/feature_request.md</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/bug_report.md</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>LLM无法直接处理视频流，工程师若用固定帧率采样会浪费token且遗漏关键画面；本项目通过场景检测和去重，在本地生成紧凑的帧集和带时间戳的转录，直达模型可消费形态。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">CLI入口<code class="code-ref">src/claude_real_video/cli.py</code>解析参数后调用<code class="code-ref">process()</code>函数（位于未提供的<code class="code-ref">core.py</code>，推测执行场景检测与去重）。<code class="code-ref">process</code>产出一个<code class="code-ref">Result</code>对象，包含帧目录、清单、转录等路径。<code class="code-ref">serve.py</code>提供本地Web UI，内部用子进程调用<code class="code-ref">crv</code>命令。<code class="code-ref">speakers.py</code>通过sherpa-onnx实现离线说话人分割，<code class="code-ref">timeline_lite.py</code>将帧与转录段落缝合为统一时间轴，<code class="code-ref">viewer.py</code>生成独立HTML查看器。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">timeline_lite.py</code>的<code class="code-ref">build_spans()</code>按1.5秒静音间隙切割时间轴，并自动将帧挂载到对应的语音段，避免LLM自行对齐的错位问题，同时处理Whisper可能的越界段。</p>
<p class="audit-callout audit-callout--highlight">测试用例<code class="code-ref">tests/test_smoke.py::test_manifest_fences_untrusted_transcript</code>通过构造恶意SRT字幕验证MANIFEST.txt的防注入设计：确保用户可控的转录文本被合理隔离，不会篡改工具自身的指令行。</p>
<p class="audit-callout audit-callout--doubt">核心模块<code class="code-ref">src/claude_real_video/core.py</code>未在审查范围内，无法评估场景检测、自适应采样、去重（如文档所述settled-local检测器）的具体实现、性能特征及边缘情况。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">speakers.py</code>中<code class="code-ref">_ensure_models()</code>下载的tar.bz2模型文件在Python&lt;3.12时缺少<code class="code-ref">filter=&#x27;data&#x27;</code>参数，虽然上抛了TypeError捕获，但仍存在路径穿越风险（issue已提及，但未提供更严格的替代方案）。</p>
<p>依赖本工具的开发者应先对自有视频类型运行<code class="code-ref">benchmark/run_benchmark.sh</code>脚本（开源提供）以验证帧提取质量，同时注意首次运行需下载约45MB的说话人分割模型。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心处理逻辑core.py未在审查中，其场景检测与去重可靠性无从验证</li><li>免费版temporal_check仅检测补帧慢动作，无法区分间隔拍摄等其他时间异常（文档自述）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>开源免费版作为LLM视频理解的前端，Pro版（$19-29）提供镜头运动、音乐情绪等付费分析，模式清晰，适合作为视频分析工作流的基础组件。</p>
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
  <div class="score-item__value">73</div>
  <div class="score-bar"><span style="width:73%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.1</span>
  </div>
</div>
</section>