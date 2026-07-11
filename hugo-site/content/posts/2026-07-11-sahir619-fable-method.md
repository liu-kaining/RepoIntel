---
title: '[Score: 79.65] Sahir619/fable-method'
date: '2026-07-11T05:37:44Z'
categories:
- AI Agent Skills & Evaluation
tags:
- agent-skills
- evaluation
- claude-code
- ai-agents
- adversarial-testing
intel_score: 79.65
repo_name: Sahir619/fable-method
repo_link: https://github.com/Sahir619/fable-method
summary: The Fable Workflow distills Claude Fable 5's problem-solving method into
  three skills—think, act, prove—backed by an adversarial eval with 159 agent runs
  and documented failures, targeting developers who need to catch AI agent dishonesty
  and traps.
code_source: git
code_files_reviewed:
- .github/workflows/checks.yml
- eval/scenarios/s7-fraudulent-work/worked/debug_scratch.py
- eval/scenarios/s7-fraudulent-work/pristine/utils.py
- eval/scenarios/s5-twin-bug/README.md
- eval/scenarios/s7-fraudulent-work/worked/utils.py
- eval/scenarios/s2-surprise-trap/README.md
- eval/scenarios/s7-fraudulent-work/pristine/converter.py
- eval/scenarios/s2-surprise-trap/pricing.py
- eval/scenarios/s7-fraudulent-work/pristine/README.md
- eval/scenarios/s7-fraudulent-work/worked/README.md
- eval/scenarios/s7-fraudulent-work/worked/converter.py
- eval/scenarios/s3-utc-bucketing/README.md
- eval/scenarios/s7-fraudulent-work/pristine/test_converter.py
- eval/scenarios/s2-surprise-trap/test_pricing.py
- eval/scenarios/s5-twin-bug/orders.py
- eval/scenarios/s8-fraudulent-copy/docs/brand.md
- eval/scenarios/s3-utc-bucketing/report.py
- eval/scenarios/s3-utc-bucketing/events.json
- eval/scenarios/s7-fraudulent-work/worked/test_converter.py
- .claude-plugin/plugin.json
- eval/scenarios/s6-ambiguous-export/stats.py
- eval/scenarios/s5-twin-bug/test_orders.py
- eval/scenarios/s1-assessment-trap/cart.js
- eval/scenarios/s8-fraudulent-copy/docs/product-facts.md
- install.sh
- .claude-plugin/marketplace.json
- eval/scenarios/s8-fraudulent-copy/landing.md
- eval/scenarios/s5-twin-bug/GROUND-TRUTH.md
- eval/scenarios/s3-utc-bucketing/GROUND-TRUTH.md
- eval/scenarios/s1-assessment-trap/GROUND-TRUTH.md
- eval/scenarios/s6-ambiguous-export/GROUND-TRUTH.md
- eval/scenarios/s4-messy-export/GROUND-TRUTH.md
- eval/scenarios/s2-surprise-trap/GROUND-TRUTH.md
- eval/scenarios/s7-fraudulent-work/GROUND-TRUTH.md
- eval/scenarios/s7-fraudulent-work/report.md
- eval/cases/s6-ambiguous-export.md
- eval/cases/s5-twin-bug.md
- eval/cases/README.md
- eval/cases/s1-assessment-trap.md
- eval/scenarios/s8-fraudulent-copy/GROUND-TRUTH.md
- eval/cases/s4-messy-export.md
- eval/cases/s3-utc-bucketing.md
- eval/cases/s7-fraudulent-work.md
- CHANGELOG.md
- skills/fable-method/references/domains/data-analysis.md
- eval/cases/s8-fraudulent-copy.md
- skills/fable-method/references/domains/research.md
- skills/fable-method/references/domains/business-ops.md
code_chars_analyzed: 45306
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
      <span class="scope-stat__value">约 45,306 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/checks.yml</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/worked/debug_scratch.py</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/pristine/utils.py</code></li><li><code class="path-chip">eval/scenarios/s5-twin-bug/README.md</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/worked/utils.py</code></li><li><code class="path-chip">eval/scenarios/s2-surprise-trap/README.md</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/pristine/converter.py</code></li><li><code class="path-chip">eval/scenarios/s2-surprise-trap/pricing.py</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/pristine/README.md</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/worked/README.md</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/worked/converter.py</code></li><li><code class="path-chip">eval/scenarios/s3-utc-bucketing/README.md</code></li><li><code class="path-chip">eval/scenarios/s7-fraudulent-work/pristine/test_converter.py</code></li><li><code class="path-chip">eval/scenarios/s2-surprise-trap/test_pricing.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI coding agents frequently produce false completions, silently modify correct code, or trust flawed tests; engineers waste hours verifying agent output, with no systematic guard against these failure modes.</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目由三个 Claude Code 插件技能（fable-method、fable-loop、fable-judge）及领域适配器（如 <code class="code-ref">skills/fable-method/references/domains/data-analysis.md</code>）构成，核心流程 think→act→prove。评估体系在 eval/ 下，包含 8 个对抗性场景（如 s2-surprise-trap），每个场景提供真实代码、错误测试（test_pricing.py 中误设 15% 折扣）及 GROUND-TRUTH.md 评分标准。CI 通过 <code class="code-ref">.github/workflows/checks.yml</code> 调用 <code class="code-ref">.github/checks.py</code> 做格式校验。</p>
<p class="audit-callout audit-callout--highlight">评估设计诚实，明确记录空结果（<code class="code-ref">eval/cases/s1-assessment-trap.md</code> 说明所有模型通过该场景），增强整体可信度。</p>
<p class="audit-callout audit-callout--highlight">s2 场景（<code class="code-ref">eval/scenarios/s2-surprise-trap/GROUND-TRUTH.md</code>）明确指出“测试本身错误”，技能训练后 Haiku 能将 0/4 提升至 4/4 识别此类陷阱，验证了方法对弱模型的提升。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">.github/checks.py</code> 源码未提供，无法审计其检测范围；CI 中未运行场景回归测试，技能修改可能静默破坏评估。</p>
<p class="audit-callout audit-callout--doubt">核心 SKILL.md 文件（约 110 行）未在代码包中，无法直接审核技能指令的内在逻辑，只能依赖案例分析推断。</p>
<p>将 eval 场景集成到 CI 作为回归测试（如运行技能并比对预期），并公开 checks.py 内容；考虑将技能文件纳入代码包以供审计。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>技能与 Claude 特定行为耦合，移植到其他模型可能失效。</li><li>评估场景固定，长期可能被优化针对性破解。</li><li>项目初创，单维护者，长期演进依赖个人精力。</li><li>summary 过长，可能含废话</li><li>未引用 README 原文依据（缺「」或 README/文档 指称）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Claude Code 插件，可立即减少开发者验证 AI 输出的人工耗时；其评估方法论可能被其他 AI 工具链采纳为质量标准。</p>
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
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.65</span>
  </div>
</div>
</section>