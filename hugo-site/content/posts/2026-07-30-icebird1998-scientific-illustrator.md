---
title: '[Score: 75.35] icebird1998/scientific-illustrator'
date: '2026-07-30T02:05:23Z'
categories:
- AI-Assisted Scientific Illustration
tags:
- MCP
- Codex Plugin
- draw.io
- PowerPoint
- Scientific Figures
- Editable Vector
intel_score: 75.35
repo_name: icebird1998/scientific-illustrator
repo_link: https://github.com/icebird1998/scientific-illustrator
summary: 让 Codex AI 代理在 PowerPoint/WPS/draw.io 中逐步绘制、审查并纠正可编辑科学插图，实现四角色质量闭环。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/ci.yml
- plugins/scientific-illustrator/skills/design-scientific-figure/agents/openai.yaml
- plugins/scientific-illustrator/skills/audit-scientific-figure/agents/openai.yaml
- plugins/scientific-illustrator/skills/recreate-scientific-figure-in-drawio/agents/openai.yaml
- plugins/scientific-illustrator/skills/correct-scientific-figure/agents/openai.yaml
- plugins/scientific-illustrator/skills/recreate-scientific-figure/agents/openai.yaml
- plugins/scientific-illustrator/skills/edit-powerpoint-live/agents/openai.yaml
- plugins/scientific-illustrator/.mcp.json
- .agents/plugins/marketplace.json
- PRIVACY.md
- plugins/scientific-illustrator/.codex-plugin/plugin.json
- install.sh
- CHANGELOG.md
- plugins/scientific-illustrator/skills/design-scientific-figure/SKILL.md
- plugins/scientific-illustrator/skills/audit-scientific-figure/SKILL.md
- plugins/scientific-illustrator/skills/correct-scientific-figure/SKILL.md
- plugins/scientific-illustrator/skills/recreate-scientific-figure-in-drawio/SKILL.md
- plugins/scientific-illustrator/skills/recreate-scientific-figure/SKILL.md
- plugins/scientific-illustrator/skills/edit-powerpoint-live/SKILL.md
- README.md
code_chars_analyzed: 73289
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
      <span class="scope-stat__value">21 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 73,289 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/design-scientific-figure/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/audit-scientific-figure/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/recreate-scientific-figure-in-drawio/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/correct-scientific-figure/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/recreate-scientific-figure/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/skills/edit-powerpoint-live/agents/openai.yaml</code></li><li><code class="path-chip">plugins/scientific-illustrator/.mcp.json</code></li><li><code class="path-chip">.agents/plugins/marketplace.json</code></li><li><code class="path-chip">PRIVACY.md</code></li><li><code class="path-chip">plugins/scientific-illustrator/.codex-plugin/plugin.json</code></li><li><code class="path-chip">install.sh</code></li><li><code class="path-chip">CHANGELOG.md</code></li><li class="path-more">另有 7 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>科研人员手动复刻论文插图耗时且易出错；现有 AI 图片转 PPT 只能得到扁平位图，无法生成可拆分、可独立编辑的矢量对象与原子图像。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">通过 Codex 插件将用户意图分发给 Design、Draw、Review、Correct 四个 Skill（见 plugins/scientific-illustrator/skills/ 下各 SKILL.md），驱动底层 MCP 服务器（drawio-live、powerpoint-live 等）操作桌面应用。设计阶段要求后端能力检测（如 SKILL.md 开头“Detect constraints”），绘图阶段强制原子图像分解（<code class="code-ref">recreate-scientific-figure/SKILL.md</code> 中的 Raster gate 部分），审查阶段要求结构+渲染双证据（<code class="code-ref">audit-scientific-figure/SKILL.md</code> 的“Collect both evidence channels”），纠正阶段输出对象级修复计划（<code class="code-ref">correct-scientific-figure/SKILL.md</code> 的“Emit an object-level plan”）。</p>
<p class="audit-callout audit-callout--highlight">四角色闭环规范详尽且跨后端统一。<code class="code-ref">design-scientific-figure/SKILL.md</code> 定义了布局网格、连接器通道、编辑性声明和构造顺序，避免随意增删对象；<code class="code-ref">audit-scientific-figure/SKILL.md</code> 强制要求“每一张保留图像必须声明 raster_reason、atomic_raster_unit=true 等五个属性”，并拒绝可重构内容留在图片中。</p>
<p class="audit-callout audit-callout--highlight">双后端语义对等与能力声明。<code class="code-ref">recreate-scientific-figure-in-drawio/SKILL.md</code> 和 <code class="code-ref">edit-powerpoint-live/SKILL.md</code> 将不同实现映射到相同的语义结果，并对 Office.js 等受限环境明确标注 <code class="code-ref">connector_mode=geometry_backed</code> 等组合对象限制，避免过度承诺。</p>
<p class="audit-callout audit-callout--doubt">核心 MCP 服务器实现未审阅到（live-server.mjs、powerpoint-server.mjs 等文件未包含在 code_bundle 中），其调用链、错误处理、并发控制和沙箱安全无法评估，直接降低工程评分。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖薄弱。package.json 第 7 行配置 <code class="code-ref">&quot;test&quot;: &quot;node --run check &amp;&amp; node scripts/smoke-test.mjs &amp;&amp; node scripts/officejs-bridge-smoke.mjs&quot;</code>，但 smoke 测试脚本未提供，仅确认存在语法验证步骤，缺少对四角色协同、后端连接异常、审查断言的自动化测试。</p>
<p>对复刻复杂论文配图的价值最高，使用前应明确目标软件后端的已知限制（如 Mac Office.js 无原生图表），并始终在目标应用中做最终渲染检查；可配合图库管理需要多次迭代的插图项目。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 Codex 平台和特定桌面软件，用户需同时学习插件安装和 MCP 配置，上手门槛高。</li><li>单维护者且代码仓极新（5 天），已知 Office.js 限制（无原生图表/连接点绑定）会影响部分科研图形的精确度与通用性。</li><li>一旦底层 MCP 服务器或上游 Codex/API 变更而无人维护，整个工作流可能立即失效。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可作为面向科研出版、图形摘要服务的增值插件，吸引使用 Codex 的科研用户；开源模式下可通过模板库和社区贡献扩展更多学科图表样式。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.35</span>
  </div>
</div>
</section>