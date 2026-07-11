---
title: '[Score: 82.05] nagisanzenin/engram'
date: '2026-07-11T07:50:22Z'
categories:
- AI Learning Plugin
tags:
- Claude Code
- Spaced Repetition
- Learning Science
- FSRS
- Agent Skills
intel_score: 82.05
repo_name: nagisanzenin/engram
repo_link: https://github.com/nagisanzenin/engram
summary: Engram 是 Claude Code 学习插件，通过生成式第一性原理课程、盲评打分与 FSRS 间隔复习，将终端内的即时学习转化为长期记忆。
code_source: git
code_files_reviewed:
- hooks/hooks.json
- .claude-plugin/marketplace.json
- .claude-plugin/plugin.json
- .agents/plugins/marketplace.json
- .codex-plugin/plugin.json
- hooks/session-start.sh
- examples/README.md
- scripts/install-codex.sh
- agents/engram-artifact-smith.md
- codex/agents/engram-artifact-smith.toml
- codex/agents/engram-assessor.toml
- agents/engram-assessor.md
- INSTALL-CODEX.md
- agents/engram-curriculum-architect.md
- assets/promo-image-spec.md
- skills/_shared/explorable-contract.md
- codex/agents/engram-curriculum-architect.toml
- docs/04-roadmap.md
- skills/review/SKILL.md
- skills/coach/SKILL.md
- docs/02-prior-art.md
- RELEASE_PROTOCOL.md
- skills/learn/SKILL.md
- skills/_shared/dialogue-grammar.md
- docs/03-architecture.md
- docs/06-visual-encoding.md
- docs/05-affective-layers.md
- docs/10-roadmap-to-1.0.md
- docs/01-foundations.md
- docs/08-vision.md
- README.md
- docs/09-target-architecture.md
- docs/07-the-measured-loop.md
- CHANGELOG.md
code_chars_analyzed: 383569
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
      <span class="scope-stat__value">34 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 383,569 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">hooks/hooks.json</code></li><li><code class="path-chip">.claude-plugin/marketplace.json</code></li><li><code class="path-chip">.claude-plugin/plugin.json</code></li><li><code class="path-chip">.agents/plugins/marketplace.json</code></li><li><code class="path-chip">.codex-plugin/plugin.json</code></li><li><code class="path-chip">hooks/session-start.sh</code></li><li><code class="path-chip">examples/README.md</code></li><li><code class="path-chip">scripts/install-codex.sh</code></li><li><code class="path-chip">agents/engram-artifact-smith.md</code></li><li><code class="path-chip">codex/agents/engram-artifact-smith.toml</code></li><li><code class="path-chip">codex/agents/engram-assessor.toml</code></li><li><code class="path-chip">agents/engram-assessor.md</code></li><li><code class="path-chip">INSTALL-CODEX.md</code></li><li><code class="path-chip">agents/engram-curriculum-architect.md</code></li><li class="path-more">另有 20 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在 AI 辅助下学习新概念后，因缺乏结构化评估与科学复习，知识迅速消退，重复学习消耗额外时间。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Engram 的核心由三个技能 (<code class="code-ref">skills/learn/</code>, <code class="code-ref">skills/review/</code>, <code class="code-ref">skills/coach/</code>)、三个代理 (<code class="code-ref">agents/curriculum-architect.md</code>, <code class="code-ref">agents/engram-assessor.md</code>, <code class="code-ref">agents/engram-artifact-smith.md</code>) 以及调度引擎 (<code class="code-ref">scripts/engram.py</code>) 组成。所有状态以 JSON 文件存入 <code class="code-ref">~/.claude/learning/</code>，会话启动钩子 (<code class="code-ref">hooks/hooks.json</code>) 触发轻度提醒。详细布局见 <code class="code-ref">docs/03-architecture.md</code>。</p>
<p class="audit-callout audit-callout--highlight">盲评估者 (<code class="code-ref">agents/engram-assessor.md</code>) 仅接收学习者回答与评分标准，不接触教学对话，实现真正分离，避免评分污染。</p>
<p class="audit-callout audit-callout--highlight">交互探索合约 (<code class="code-ref">skills/_shared/explorable-contract.md</code>) 强制生成的 HTML 探索器包含预测、引导操纵、内嵌检索和空白页重构，基于多媒体学习原则。</p>
<p class="audit-callout audit-callout--doubt">审阅未包含核心引擎 <code class="code-ref">scripts/engram.py</code>，无法验证 FSRS 实现正确性、错误处理及自检覆盖（尽管 README 声称 120 项自检）。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">docs/09-target-architecture.md</code> 揭示 <code class="code-ref">transfer_probe</code> 字段仅由课程架构师生成，但从未被任何组件读取，说明系统目前只测量回忆而非真实迁移能力。</p>
<p>开源引擎代码并通过审计（如已规划的 v0.7）确认评估者准确性；尽快实现转移学习功能以完整闭环。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心调度引擎未开源，用户无法验证 FSRS 实现及数据完整性。</li><li>项目仅 5 天且由单人维护，长期演进和故障响应存在风险。</li><li>盲评估者依赖 LLM，计划中的审计未完成，可能存在系统性评分偏差。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可成为 AI 辅助学习的开放式组件，未来通过匿名学习数据贡献教育研究，具备学术与社区商业化潜力。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.05</span>
  </div>
</div>
</section>