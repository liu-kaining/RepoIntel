---
title: '[Score: 80.1] ronak-create/FableCut'
date: '2026-07-11T21:45:17Z'
categories:
- AI-assisted Video Editing
tags:
- video editing
- AI agent
- MCP
- zero-dependency
- browser
- NLE
intel_score: 80.1
repo_name: ronak-create/FableCut
repo_link: https://github.com/ronak-create/FableCut
summary: 零依赖浏览器视频编辑器，以 JSON 时间线为接口，支持 AI 代理通过 MCP 和 REST 驱动编辑，并具备参考视频分析、自动重剪等创意功能。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- .github/ISSUE_TEMPLATE/config.yml
- .github/PULL_REQUEST_TEMPLATE.md
- library/sfx/README.md
- library/README.md
- .github/ISSUE_TEMPLATE/feature_request.yml
- library/fonts/LICENSES.md
- .github/ISSUE_TEMPLATE/bug_report.yml
- SECURITY.md
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- docs/main.js
- CHANGELOG.md
- README.md
- analyze.js
- server.js
- mcp-server.js
- CLAUDE.md
code_chars_analyzed: 127595
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
      <span class="scope-stat__value">19 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 127,595 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">.github/PULL_REQUEST_TEMPLATE.md</code></li><li><code class="path-chip">library/sfx/README.md</code></li><li><code class="path-chip">library/README.md</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/feature_request.yml</code></li><li><code class="path-chip">library/fonts/LICENSES.md</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/bug_report.yml</code></li><li><code class="path-chip">SECURITY.md</code></li><li><code class="path-chip">CODE_OF_CONDUCT.md</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">docs/main.js</code></li><li><code class="path-chip">CHANGELOG.md</code></li><li class="path-more">另有 5 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>现有 AI 视频工具将编辑逻辑隐藏在云端 API 后，开发者与 AI 代理无法直接、原子化地操控时间线；手动剪辑重复性高，协作困难，且依赖复杂构建链。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">server.js 提供零依赖 HTTP 服务，包含文件托管、REST API、SSE 实时推送及基于 ffmpeg 的快速导出管线；mcp-server.js 实现 stdio JSON-RPC MCP 服务，暴露状态检查、文档获取、项目读写、补丁式编辑等工具；analyze.js 纯 Node 实现参考视频分析，生成镜头边界、节奏图谱与音乐提取。三者通过 project.json 和文件系统松耦合，UI 通过 SSE 热重载，整体设计强调单文件项目下的人机协同。</p>
<p class="audit-callout audit-callout--highlight">mcp-server.js 中的 <code class="code-ref">fablecut_patch_project</code> 工具实现了合并安全的增量编辑（内部重新读取最新文档，依次应用 add/update/remove 操作，一次性 bump 版本并原子写入），避免了代理反复读写整个文档的令牌开销与并发冲突。</p>
<p class="audit-callout audit-callout--highlight">analyze.js 的 <code class="code-ref">analyzeAudio</code> 函数使用 22kHz 采样下的起始点包络和自相关算法检测 BPM，结合自适应阈值查找节拍，并通过 span-refined 方法对 BPM 进行细化，同时生成逐帧响度曲线和“高潮”检测，全程零外部依赖。</p>
<p class="audit-callout audit-callout--doubt">代码包中未见任何单元测试或集成测试文件，CI 配置（<code class="code-ref">.github/workflows/ci.yml</code>）仅包含语法检查、JSON 合法性验证和 SVG 格式校验，核心逻辑如冲突检测、分析算法、导出管线均无测试覆盖。</p>
<p class="audit-callout audit-callout--doubt">核心编辑器客户端 app.js（约 182KB）未在审查范围内，其合成器、关键帧引擎、滤镜、文字动画等可视化逻辑完全不可见，无法评估实际渲染正确性、性能及错误处理，本次结论不覆盖前端部分。</p>
<p>立即为 server.js 和 mcp-server.js 添加关键路径的集成测试（如并发写入冲突模拟、导出会话生命周期），并对 analyze.js 的音频分析精度引入基准对比；在社区文档中明确前端代码审计状态。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>无测试代码：CI 仅检查语法，核心逻辑未经验证，合并外源贡献后稳定性堪忧</li><li>核心前端 app.js 未审阅：合成器、效果器等关键模块可能隐藏严重缺陷</li><li>安全边界文档已声明无鉴权，不慎暴露至非受信网络将导致文件读写攻击</li><li>依赖于 ffmpeg 二进制，虽标记为可选，但快速导出和分析功能实际强制要求，限制了轻量环境部署</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>该项目有望成为短视频创作者和 AI 工具开发者的标准本地编辑平台，其无依赖、代理优先的设计可降低集成成本。若持续维护并建立社区贡献体系，可能吸引寻求开源可定制视频管线的企业用户，但目前单开发者模式存在可持续性风险。</p>
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
  <div class="score-item__value">86</div>
  <div class="score-bar"><span style="width:86%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">80.1</span>
  </div>
</div>
</section>