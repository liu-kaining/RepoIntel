---
title: '[Score: 82.4] 0rangec3t/Black-cat'
date: '2026-07-31T19:19:52Z'
categories:
- AI-based Pentest Framework
tags:
- claude-code
- red-team
- state-machine
- evidence-chain
- skill
intel_score: 82.4
repo_name: 0rangec3t/Black-cat
repo_link: https://github.com/0rangec3t/Black-cat
summary: Claude Code 假设驱动红队 Skill，用状态机+证据链替代传统流水线，助安全研究员高效挖掘漏洞。
code_source: git
code_files_reviewed:
- skills/pentest-redteam/templates/engagement-report.md
- .claude/settings.json
- assets/README.md
- skills/pentest-redteam/templates/finding-report.md
- case/evidence-validation.md
- skills/pentest-redteam/techniques/reversing.md
- skills/pentest-redteam/techniques/database.md
- skills/pentest-redteam/techniques/cloud.md
- skills/pentest-redteam/SKILL.md
- skills/pentest-redteam/techniques/web.md
- skills/pentest-redteam/techniques/recon.md
- README.md
- skills/pentest-redteam/techniques/ad.md
- skills/pentest-redteam/techniques/evasion.md
- skills/pentest-redteam/scripts/case_ledger.py
- tests/test_case_ledger.py
code_chars_analyzed: 120989
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
      <span class="scope-stat__value">约 120,989 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">skills/pentest-redteam/templates/engagement-report.md</code></li><li><code class="path-chip">.claude/settings.json</code></li><li><code class="path-chip">assets/README.md</code></li><li><code class="path-chip">skills/pentest-redteam/templates/finding-report.md</code></li><li><code class="path-chip">case/evidence-validation.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/reversing.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/database.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/cloud.md</code></li><li><code class="path-chip">skills/pentest-redteam/SKILL.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/web.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/recon.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/ad.md</code></li><li><code class="path-chip">skills/pentest-redteam/techniques/evasion.md</code></li><li class="path-more">另有 2 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>传统渗透工具流水线化，失败即跳过无反馈，孤立截图无法追溯因果，导致重复劳动且结果不可信。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Skill 核心定义在 <code class="code-ref">skills/pentest-redteam/SKILL.md</code>，包含三层设计：L1 授权与硬约束、L2 有回边的状态机（RECON ⇄ ENUMERATE ⇄ VALIDATE → EXPLOIT → POST-EXPLOIT → REPORT，失败或新信号可回溯）、L3 信号→动作链。<code class="code-ref">SKILL.md:50</code> 附近的状态机图和 <code class="code-ref">SKILL.md:100</code> 描述的显式路由确保了执行主线。<code class="code-ref">techniques/</code> 目录下 7 个 .md 文件作为领域知识库，通过信号匹配加载，如 <code class="code-ref">techniques/web.md:5</code> 定义了“触发: 目标是 Web/API...”。核心数据流由 <code class="code-ref">skills/pentest-redteam/scripts/case_ledger.py</code> 承载，实现 hypothesis/evidence/verdict 的 append-only JSONL 账本，并自动生成 <code class="code-ref">case/evidence-validation.md</code> 可视化报告。测试 <code class="code-ref">tests/test_case_ledger.py:28</code> 覆盖了完整 CLI 流程、边界检查与报告渲染。</p>
<p class="audit-callout audit-callout--highlight">证据链闭环与机器关口。<code class="code-ref">case_ledger.py:80</code> 定义了 <code class="code-ref">REQUIRED_ROLES = (&quot;observation&quot;, &quot;reproduction&quot;, &quot;impact&quot;)</code>，<code class="code-ref">verify --report</code> 命令通过 <code class="code-ref">report_gate()</code> 强制所有 confirmed 假设必须包含这三种证据角色，否则报错。测试 <code class="code-ref">test_confirmed_hypothesis_is_rendered_as_a_fact</code> 验证了 confirmed 假设被渲染为事实，<code class="code-ref">test_provisional_renders_and_report_gate_blocks_then_passes</code> 演示了 provisional 转 confirmed 及 gate 通过。这确保了交付物可追溯且非臆断。</p>
<p class="audit-callout audit-callout--highlight">显式文件路由防臃肿。<code class="code-ref">SKILL.md:110</code> 规定“单次 context 中活跃 technique 目录默认 1 个，最多 2 个”，配合 <code class="code-ref">SKILL.md:105</code> 的映射表（域名→web.md，IP/云→cloud.md 等），避免 Agent 加载无关内容。<code class="code-ref">techniques/recon.md</code> 与 <code class="code-ref">techniques/web.md</code> 的分离，以及 <code class="code-ref">techniques/ad.md</code> 和 <code class="code-ref">techniques/evasion.md</code> 仅限明确任务，有效控制了上下文长度和认知负担。</p>
<p class="audit-callout audit-callout--doubt">状态流转无程序化约束。<code class="code-ref">SKILL.md:50</code> 的状态机图及 Decision Gates 描述依赖 Claude Code 的 Agent 自行解读并遵循，源码中未见强制执行逻辑（如状态机引擎）。<code class="code-ref">case_ledger.py</code> 仅检查证据完整性，不验证状态迁移是否正确，若 Agent 跳过步骤或误判状态，可能导致流程黑洞。</p>
<p class="audit-callout audit-callout--doubt">技术动作以速查表形式存在，可靠性存疑。<code class="code-ref">techniques/web.md</code>、<code class="code-ref">techniques/cloud.md</code> 等文件中全为自然语言描述（如“SSL Pinning 绕过→mitmproxy 捕获”），缺少可执行的、经过验证的自动化脚本。Agent 需自行组合工具命令，可能因工具缺失或版本差异而失败，且难以复现。</p>
<p>为状态机增加 JSON Schema 化的强制步骤，由 <code class="code-ref">case_ledger.py</code> 的 <code class="code-ref">verify</code> 命令扩展状态校验；对关键渗透链（如 Fastjson 利用）提供可选的 Docker 沙箱验证脚本，减少 Agent 幻觉。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>框架强依赖 Claude Code，平台锁定风险高，若 skill 机制变更需大量重写。</li><li>技术实现以文档为主，Agent 可能误解指令导致误报或漏报，降低结果可信度。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Claude Code 生态首个假设驱动的红队 Skill，可降低专业渗透测试的人力成本，吸引安全团队付费集成或贡献技术目录。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.4</span>
  </div>
</div>
</section>