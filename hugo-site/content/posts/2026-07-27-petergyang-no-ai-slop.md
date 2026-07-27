---
title: '[Score: 75.0] petergyang/no-ai-slop'
date: '2026-07-27T06:26:42Z'
categories:
- AI-Assisted Writing
tags:
- ai-editing
- prompt-engineering
- writing-voice
- content-creation
- slop-detection
intel_score: 75.0
repo_name: petergyang/no-ai-slop
repo_link: https://github.com/petergyang/no-ai-slop
summary: 将20+种AI写作陈词滥调整理为可自检的编辑技能包，供内容创作者在AI助手中直接调用，去除AI味同时保留个人声音。
code_source: git
code_files_reviewed:
- .github/workflows/plugin.yml
- agents/openai.yaml
- PRIVACY.md
- TERMS.md
- .codex-plugin/plugin.json
- plugin-submission.md
- README.md
- eval.md
- scripts/build_plugin.py
- SKILL.md
code_chars_analyzed: 26182
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
      <span class="scope-stat__value">10 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 26,182 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/plugin.yml</code></li><li><code class="path-chip">agents/openai.yaml</code></li><li><code class="path-chip">PRIVACY.md</code></li><li><code class="path-chip">TERMS.md</code></li><li><code class="path-chip">.codex-plugin/plugin.json</code></li><li><code class="path-chip">plugin-submission.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">eval.md</code></li><li><code class="path-chip">scripts/build_plugin.py</code></li><li><code class="path-chip">SKILL.md</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>写作者依赖AI润色时，常被注入“delve”、“not X but Y”等千篇一律的套话，破坏个人风格；现有工具缺乏系统化的模式识别与自检，导致编辑结果仍需大量人工返工。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目以 SKILL.md:1-500（编辑规则与工作流）和 eval.md:1-68（自检清单）为核心，通过 LLM 解释执行。<code class="code-ref">scripts/build_plugin.py:20-70</code> 将 SKILL.md、eval.md 及资源打包为 ChatGPT/Codex 插件 ZIP 并验证完整性（<code class="code-ref">validate_source</code> 检查 manifest 字段，<code class="code-ref">validate_build</code> 比对文件哈希并检查 ZIP 结构）。CI 流水线（<code class="code-ref">.github/workflows/plugin.yml</code>）在 PR 和 Tag 时自动构建并上传。无运行时引擎，所有编辑逻辑依赖提示词工程。</p>
<p class="audit-callout audit-callout--highlight">eval.md:1-68 实现了编辑后的自检闭环：每次修改后必须对照20+条编辑原则（如“Does the edit preserve the writer&#x27;s distinctive vocabulary...”）逐条打 pass/fail，失败则回炉修改。相当于将编辑质量检查固化为可执行指令，而非依赖事后人工评估。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">scripts/build_plugin.py</code> 中的 <code class="code-ref">validate_source</code>（第17-32行）和 <code class="code-ref">validate_build</code>（第58-70行）确保了发行包的一致性：检查 manifest 必需字段、skills 目录核心文件存在、打包后内容与源完全一致。这避免了因手动打包导致 SKILL.md 与 eval.md 版本不同步的常见错误。</p>
<p class="audit-callout audit-callout--doubt">SKILL.md 中所有编辑规则（如禁止单词列表、模式匹配）完全依赖 LLM 对自然语言的理解，无编程级保证。例如，对“binary contrasts”的识别依赖 LLM 的语义判断，可能漏检或误伤（如将某种修辞手法误判为 slop）。未审阅到任何形式化检测逻辑或单元测试来验证规则触发准确性。</p>
<p class="audit-callout audit-callout--doubt">项目缺少对实际编辑效果的自动化测试。尽管 eval.md 提供了自检指令，但 SKILL.md 中未见要求将自检结果反馈给测试框架，CI 中仅做了打包验证，未调用 LLM 验证技能实际执行结果。若 SKILL.md 被意外修改导致编辑质量下降，无自动回归手段。</p>
<p>适合作为 AI 辅助写作的“预处理器”嵌入工作流，尤其适合博客作者、技术写手。建议在团队中试用 <code class="code-ref">detect</code> 模式，收集误报/漏报案例后微调 SKILL.md 中的模式列表，并考虑用少量标注样本做提示调优，确保不会扁平化个人风格。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>所有编辑逻辑依赖LLM解释自然语言指令，无形式化保证，可能将合理修辞误判为slop并删除。</li><li>效果强依赖底层模型能力，模型更新后可能需重新调整提示词，维护成本不可忽视。</li><li>插件分发依赖ChatGPT/Codex目录审核，若平台政策变动可能导致分发受阻。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>直接解决内容创作者对AI生成文本同质化的普遍焦虑，可作为写作工具的增值技能分发，通过插件市场或企业协作场景变现。但门槛较低，易被同类提示库替代。</p>
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
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
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
    <span class="total-score-banner__value">75.0</span>
  </div>
</div>
</section>