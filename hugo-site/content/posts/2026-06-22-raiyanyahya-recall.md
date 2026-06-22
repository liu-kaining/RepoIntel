---
title: '[Score: 75.7] raiyanyahya/recall'
date: '2026-06-22T11:48:42Z'
categories:
- Claude Code Plugin
tags:
- Claude Code
- local-first
- TextRank
- summarization
- developer-tools
- privacy
intel_score: 75.7
repo_name: raiyanyahya/recall
repo_link: https://github.com/raiyanyahya/recall
summary: 为 Claude Code 项目提供本地会话记忆的插件，通过 TF-IDF+TextRank 摘要将历史记录压缩为约 1-2K token 的上下文文件，适合频繁使用
  Claude Code 且需跨 session 续接的开发者。
code_source: git
code_files_reviewed:
- pyproject.toml
- .github/workflows/codeql.yml
- .github/workflows/ci.yml
- recall.config.json
- tests/conftest.py
- .github/ISSUE_TEMPLATE/config.yml
- commands/show.md
- .github/dependabot.yml
- commands/log.md
- .github/PULL_REQUEST_TEMPLATE.md
- .claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- tests/test_redact.py
- hooks/hooks.json
- commands/save.md
- .github/ISSUE_TEMPLATE/feature_request.yml
- scripts/session_end.py
- scripts/redact.py
- tests/test_session_end.py
- tests/test_common.py
- tests/test_parse_transcript.py
- tests/_util.py
- CONTRIBUTING.md
- tests/test_config.py
- tests/test_summarizer.py
- SECURITY.md
- scripts/config.py
- .github/ISSUE_TEMPLATE/bug_report.yml
- scripts/session_start.py
- tests/test_capture.py
- tests/test_security.py
- scripts/capture.py
- scripts/parse_transcript.py
- tests/test_make_context.py
- scripts/summarizer.py
- CHANGELOG.md
- scripts/common.py
- scripts/make_context.py
- README.md
- benchmarks/bench.py
- claude-code-context-plugin.md
code_chars_analyzed: 128230
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
      <span class="scope-stat__value">41 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 128,230 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/codeql.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">recall.config.json</code></li><li><code class="path-chip">tests/conftest.py</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">commands/show.md</code></li><li><code class="path-chip">.github/dependabot.yml</code></li><li><code class="path-chip">commands/log.md</code></li><li><code class="path-chip">.github/PULL_REQUEST_TEMPLATE.md</code></li><li><code class="path-chip">.claude-plugin/plugin.json</code></li><li><code class="path-chip">.claude-plugin/marketplace.json</code></li><li><code class="path-chip">tests/test_redact.py</code></li><li><code class="path-chip">hooks/hooks.json</code></li><li class="path-more">另有 27 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>每次新开 Claude Code session 都需要重新解释项目背景、已完成工作和下一步计划，消耗大量 token 且打断工作流；本地 transcript 含代码和可能的密钥，发送到外部 API 做摘要存在隐私风险。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Recall 是一个纯本地 Claude Code 插件，通过三个生命周期 hook（SessionStart/Stop/SessionEnd）和一个 slash command（/recall:save）驱动。SessionStart hook（<code class="code-ref">scripts/session_start.py</code>）读取 <code class="code-ref">.recall/context.md</code> 并以指令注入方式让 Claude 在对话中询问用户是否恢复上下文。Stop/SessionEnd hook（<code class="code-ref">scripts/capture.py</code>）以**字节偏移增量**方式追加 transcript 活动到 <code class="code-ref">history.md</code>，通过 <code class="code-ref">scripts/parse_transcript.py</code> 解析 JSONL 格式的 transcript。<code class="code-ref">/recall:save</code> 触发 <code class="code-ref">scripts/make_context.py</code>，调用 <code class="code-ref">scripts/summarizer.py</code> 中的 vendored TF-IDF+TextRank 提取式摘要算法，将结果写入 <code class="code-ref">context.md</code>。摘要器同时维护 numpy 向量化路径和纯 Python 路径（<code class="code-ref">scripts/summarizer.py:113-152</code>），通过 try/except 自动切换，保证零安装依赖。</p>
<p class="audit-callout audit-callout--highlight">安全防护设计细致。<code class="code-ref">scripts/common.py:63-76</code> 的 <code class="code-ref">output_dir</code> 函数对配置值做绝对路径和 <code class="code-ref">..</code> 遍历检查，拒绝将输出目录指向项目外；<code class="code-ref">scripts/common.py:99-105</code> 的 <code class="code-ref">_open_nofollow</code> 使用 <code class="code-ref">O_NOFOLLOW</code> 标志防止符号链接重定向攻击；<code class="code-ref">scripts/common.py:155-163</code> 的 <code class="code-ref">_git</code> 函数对 git 命令禁用 <code class="code-ref">core.fsmonitor</code>、<code class="code-ref">diff.external</code>、hooks 和 pager，防止不受信任的仓库通过 git config 执行任意代码。<code class="code-ref">tests/test_security.py</code> 对每个安全约束都有端到端回归测试。</p>
<p class="audit-callout audit-callout--highlight">numpy 与纯 Python 后端的确定性等价保证。<code class="code-ref">scripts/summarizer.py:99-104</code> 的 <code class="code-ref">_select</code> 函数在排名前将分数 round 到 10 位小数并按位置打破平局，确保两种后端选择完全相同的句子。<code class="code-ref">benchmarks/bench.py</code> 的 <code class="code-ref">backend_equivalence</code> 函数在 CI 中作为质量门禁验证这一不变量，<code class="code-ref">tests/test_summarizer.py:30-37</code> 的 <code class="code-ref">test_numpy_and_pure_python_cores_agree</code> 也有单元覆盖。</p>
<p class="audit-callout audit-callout--doubt">摘要质量天然受限。<code class="code-ref">scripts/summarizer.py</code> 使用的是经典 TF-IDF+TextRank 提取式摘要，无法生成转述或抽象，只能从原文中挑选句子。对于编程会话中的上下文（如讨论设计权衡、调试推理链），提取式摘要可能遗漏关键信息。<code class="code-ref">benchmarks/bench.py:49-76</code> 的质量 fixture 仅包含 3 个手工标注的小场景，F1 地板设为 0.60，实际长会话中质量可能更差。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">scripts/session_start.py:39-50</code> 通过 stdout 注入指令让 Claude 在对话中询问用户，这本质上是 prompt injection 的一种形式——用 hook 输出控制 Claude 的行为。虽然当前注入内容是硬编码的，但这个模式如果被其他插件模仿，可能存在安全风险。此外 <code class="code-ref">context.md</code> 作为「不可信数据」围栏标注的设计（<code class="code-ref">scripts/session_start.py:53-59</code>）依赖 Claude 正确执行指令，而非技术强制。</p>
<p>适合已在使用 Claude Code 且有频繁跨 session 需求的个人开发者试用。建议先在小项目上验证摘要质量，关注 <code class="code-ref">context.md</code> 的信息是否足够引导下一个 session 的工作。团队使用时需要评估 prompt injection 风险——如果 repo 写权限不完全可信，应将 <code class="code-ref">.recall/</code> 加入 <code class="code-ref">.gitignore</code>。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅 2 天历史、6 次 commit，摘要器质量 fixture 仅 3 个场景，长会话实际效果未经验证</li><li>context.md 注入依赖 Claude 正确遵守「不可信数据」指令，无技术层面的强制隔离机制</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>解决 Claude Code 用户的实际痛点，但作为纯本地插件缺乏商业模式；价值在于提升 Claude Code 订阅用户的 token 效率和使用体验，与 Anthropic 生态绑定较深。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">55</div>
  <div class="score-bar"><span style="width:55%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.7</span>
  </div>
</div>
</section>