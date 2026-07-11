---
title: '[Score: 79.5] Nanako0129/pilotfish'
date: '2026-07-11T13:12:13Z'
categories:
- Claude Code Orchestration
tags:
- claude-code
- multi-model
- orchestration
- agent-config
- cost-saving
- developer-tools
intel_score: 79.5
repo_name: Nanako0129/pilotfish
repo_link: https://github.com/Nanako0129/pilotfish
summary: pilotfish 是为 Claude Code 设计的智能多模型编排层，通过三配置文件自动将任务路由到廉价的执行模型，节省推理配额且支持优雅降级。
code_source: git
code_files_reviewed:
- templates/settings.snippet.json
- RELEASING.md
- templates/agents/Explore.md
- templates/agents/scout.md
- templates/agents/security-executor.md
- templates/agents/verifier.md
- templates/agents/mech-executor.md
- templates/claude-md.orchestration.md
- templates/agents/executor.md
- CHANGELOG.md
- docs/design.md
- install/AGENT-INSTALL.md
- docs/research.zh-TW.md
- docs/research.md
- README.zh-TW.md
- README.md
code_chars_analyzed: 87048
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
      <span class="scope-stat__value">16 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 87,048 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">templates/settings.snippet.json</code></li><li><code class="path-chip">RELEASING.md</code></li><li><code class="path-chip">templates/agents/Explore.md</code></li><li><code class="path-chip">templates/agents/scout.md</code></li><li><code class="path-chip">templates/agents/security-executor.md</code></li><li><code class="path-chip">templates/agents/verifier.md</code></li><li><code class="path-chip">templates/agents/mech-executor.md</code></li><li><code class="path-chip">templates/claude-md.orchestration.md</code></li><li><code class="path-chip">templates/agents/executor.md</code></li><li><code class="path-chip">CHANGELOG.md</code></li><li><code class="path-chip">docs/design.md</code></li><li><code class="path-chip">install/AGENT-INSTALL.md</code></li><li><code class="path-chip">docs/research.zh-TW.md</code></li><li><code class="path-chip">docs/research.md</code></li><li class="path-more">另有 2 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Claude Code 用户特别是 Fable 5 订阅者，大量 token 消耗在搜索、机械编辑等低判断工作上，导致昂贵的配额快速耗尽，而任务质量并未提升。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">pilotfish 无运行时，通过三处配置文件实现编排：settings.json（<code class="code-ref">templates/settings.snippet.js</code>on:2）设定 orchestrator 为 &#x27;best&#x27; 并配置 fallbackModel；六个 agent 文件（templates/agents/ 下）通过 frontmatter 绑定模型 alias 和 effort；政策文件（<code class="code-ref">templates/claude-md.orchestration.md</code>）定义委托规则，使用角色名而无模型名。安装过程（<code class="code-ref">install/AGENT-INSTALL.md</code>）合并现有配置并幂等升级。</p>
<p class="audit-callout audit-callout--highlight">政策与模型彻底解耦。<code class="code-ref">templates/claude-md.orchestration.md:5</code> 的委托表格仅指定角色如 &#x27;mech-executor&#x27;，模型绑定存在于 agent 文件一行 frontmatter（如 <code class="code-ref">templates/agents/mech-executor.md:4</code> 的 model: sonnet），模型降级或升级仅需修改一处，政策永不过期。</p>
<p class="audit-callout audit-callout--highlight">独立对抗验证器。<code class="code-ref">templates/agents/verifier.md:6</code> 设置 disallowedTools: Write,Edit,...，强制只读运行并尝试证伪产出，返回 CONFIRMED/REFUTED 证据，将质量关口从「信任 executor」转为「实证产出」。</p>
<p class="audit-callout audit-callout--doubt">未审阅到任何自动化测试、CI 配置或版本兼容性校验。<code class="code-ref">install/AGENT-INSTALL.md</code> 内文件操作逻辑繁复，缺少回归测试可能导致未来 Claude Code 更新时安装失败。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 agent 间通信状态或异常重试的可观测性机制。所有协作依赖自然语言 prompt，无结构化日志或审计，长任务中委派失败难以排查。</p>
<p>适用于 Claude Code 重度用户，建议使用 commit SHA 安装固定版本，配合 /model opusplan 降低主 session 成本；预期在订阅配额节省上效果显著。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖 Claude Code 持续支持 subagent 和 alias 机制，未来变更可能需适配。</li><li>所有执行依赖 LLM 指令理解，无结构化保障，生产环境任务可靠性有限。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>精准切入 Anthropic 生态大量订阅用户的配额焦虑，通过降低 token 消耗提升个人开发效率，但价值边界局限于 Claude Code 平台，难以横向扩展。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.5</span>
  </div>
</div>
</section>