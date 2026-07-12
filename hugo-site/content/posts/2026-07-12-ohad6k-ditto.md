---
title: '[Score: 82.4] ohad6k/ditto'
date: '2026-07-12T02:29:16Z'
categories:
- Developer Tools
tags:
- ai-coding
- agent-memory
- claude-code
- codex
- profile-mining
- local-first
intel_score: 82.4
repo_name: ohad6k/ditto
repo_link: https://github.com/ohad6k/ditto
summary: 从 Claude Code/Codex 会话日志逆向挖掘你的编程习惯、设计品味和写作风格，生成有据可查的 you.md 技能包。
code_source: git
code_files_reviewed:
- .github/workflows/tests.yml
- .agents/skills/ditto/runtime.json
- .agents/plugins/marketplace.json
- tests/fixtures/bounded-calibration-baseline.json
- skills/work/SKILL.md
- skills/write/SKILL.md
- skills/design/SKILL.md
- .codex-plugin/plugin.json
- ROADMAP.md
- examples/you.md
- docs/release/plugin-viability.md
- skills/mine/SKILL.md
- examples/lenses/you-working.md
- SECURITY.md
- examples/lenses/you-designer.md
- .agents/skills/ditto/SKILL.md
- examples/lenses/you-thinking.md
- examples/unified-system.md
- tests/test_bootstrap.py
- docs/release/plugin-release-draft.md
- CHANGELOG.md
- .agents/skills/ditto/scripts/bootstrap.py
- tests/test_plugin_manifests.py
- docs/superpowers/specs/2026-07-11-ditto-cinematic-motion-rebuild-design.md
- MINING_PROMPT.md
- docs/release/plugin-dogfood.md
- docs/superpowers/specs/2026-07-11-ditto-cinematic-launch-video-design.md
- README.md
- docs/superpowers/specs/2026-07-11-ditto-adaptive-recall-design.md
- docs/superpowers/plans/2026-07-11-ditto-cinematic-launch-video-implementation-plan.md
- tests/test_ditto.py
- docs/superpowers/specs/2026-07-10-ditto-plugin-design.md
- tests/test_adaptive_recall.py
- tests/test_profile_store.py
- tests/test_plugin_runtime.py
- docs/superpowers/plans/2026-07-11-ditto-adaptive-recall-implementation-plan.md
code_chars_analyzed: 324255
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
      <span class="scope-stat__value">36 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 324,255 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/tests.yml</code></li><li><code class="path-chip">.agents/skills/ditto/runtime.json</code></li><li><code class="path-chip">.agents/plugins/marketplace.json</code></li><li><code class="path-chip">tests/fixtures/bounded-calibration-baseline.json</code></li><li><code class="path-chip">skills/work/SKILL.md</code></li><li><code class="path-chip">skills/write/SKILL.md</code></li><li><code class="path-chip">skills/design/SKILL.md</code></li><li><code class="path-chip">.codex-plugin/plugin.json</code></li><li><code class="path-chip">ROADMAP.md</code></li><li><code class="path-chip">examples/you.md</code></li><li><code class="path-chip">docs/release/plugin-viability.md</code></li><li><code class="path-chip">skills/mine/SKILL.md</code></li><li><code class="path-chip">examples/lenses/you-working.md</code></li><li><code class="path-chip">SECURITY.md</code></li><li class="path-more">另有 22 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>每次与 AI 编码助手开始新对话，它都完全不记得你的 do/don&#x27;t、验收标准和真实语气，你得反复解释相同偏好。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Ditto 的入口是 CLI 工具 <code class="code-ref">ditto.py</code>（单文件、标准库），通过解析本地 <code class="code-ref">~/.codex</code> 等目录的 <code class="code-ref">.jsonl</code> 日志提取用户消息，经去敏感信息、去重后生成结构化记录。随后的“挖掘”流程分为两步：多个 worker 读取分段并输出包含 work/design/write 证据的 JSON 报告，再由一个 reducer 将这些报告合并为最终的个人资料包（<code class="code-ref">you.md</code>, <code class="code-ref">you-designer.md</code>, <code class="code-ref">you-writer.md</code> 等）。版本 0.2.0 引入了 native Codex 插件和 skills.sh bootstrap（<code class="code-ref">skills/mine/SKILL.md:1</code>），通过 <code class="code-ref">ditto:mine</code>、<code class="code-ref">ditto:work</code> 等命名空间技能在支持的主机上自动路由。</p>
<p class="audit-callout audit-callout--highlight">底层证据要求严格——worker 报告被 <code class="code-ref">validate-report</code> 命令实门，每个推论必须附带原始对话中有日期的直接引语，且样本数不足时域会被标记为 inactive（<code class="code-ref">tests/test_plugin_runtime.py:12</code> 的 <code class="code-ref">ReportCacheTest</code> 类中有大量验证测试）。这避免了凭空臆造的个性描述。</p>
<p class="audit-callout audit-callout--highlight">测试覆盖异常深入——4000+ 行的测试集覆盖了从基础 CLI（<code class="code-ref">tests/test_ditto.py</code>）到原子化保存（<code class="code-ref">tests/test_profile_store.py</code>）再到自适应召回管线（<code class="code-ref">tests/test_adaptive_recall.py</code>）的所有关键路径，甚至有引导程序完整性检查（<code class="code-ref">tests/test_bootstrap.py</code>）和插件清单约束测试（<code class="code-ref">tests/test_plugin_manifests.py</code>）。CI 流水线执行全套 unittest（<code class="code-ref">.github/workflows/tests.yml</code>）。</p>
<p class="audit-callout audit-callout--doubt">核心挖掘逻辑依赖外部大模型（worker 和 reducer 需调用 AI），成本与质量受所选模型直接影响，但代码包内未审阅到模型调用的具体执行路径（如 API 封装、重试策略），本次评估不覆盖该部分风险。</p>
<p class="audit-callout audit-callout--doubt">自适应召回（<code class="code-ref">tests/test_adaptive_recall.py</code>）仍标注为实验性，其落地文档也承认在私有校验集上仅恢复 12/22 项要求，远未达到“完整画像”（<code class="code-ref">docs/release/plugin-dogfood.md:5</code>）。正式版仍默认走“完全历史”模式（资源消耗大），实用性受限。</p>
<p>如果你是 Codex 或 Claude Code 大量用户并愿意承担模型调用成本，可尝试用 Ditto 生成工作域资料，但设计/写作域输出质量不稳定；务必审查 <code class="code-ref">you.md</code> 内容并持续关注其自适应挖掘的改进。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目过于依赖外开源主机（Codex/Claude）的插件生态，任一方的 API 变动都可能导致 Ditto 失效</li><li>挖掘过程中的大模型调用成本与隐私泄漏风险（脱敏为“尽力”），且用户必须将选定文本发送给不同模型提供商</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>在 AI 辅助编码工具中植入了个人化记忆层，若被广泛采用，可能成为编程助手体验的差异化组件；但工具本身不直接商业化，生态价值在于提升已有助手的效率。</p>
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
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">92</div>
  <div class="score-bar"><span style="width:92%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.4</span>
  </div>
</div>
</section>