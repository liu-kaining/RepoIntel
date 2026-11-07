---
title: '[Score: 79.4] KKKKhazix/agent-autoloop'
date: '2026-11-07T09:35:49Z'
categories:
- AI Agent Runtime
tags:
- TypeScript
- CLI
- Automation
- AI Agents
- MCP
- Self-hosted
intel_score: 79.4
repo_name: KKKKhazix/agent-autoloop
repo_link: https://github.com/KKKKhazix/agent-autoloop
summary: 让命令行AI Agent在后台自主接活、跟进，遇不确定才推卡片让人拍板，适合有CLI Agent工作流的开发者。
code_source: git
code_files_reviewed:
- package.json
- .github/workflows/check.yml
- .github/workflows/nightly.yml
- cli/try.ts
- cli/spend.ts
- cli/update.ts
- cli/uninstall.ts
- cli/explain.ts
- cli/backup.ts
- cli/mcp.ts
- cli/why.ts
- cli/main.ts
- bin/agent-autoloop.ts
- examples/recipes/website-watch/site.json
- examples/recipes/inbox-triage/sources.json
- kernel/errors.ts
- examples/recipes/feedback/event.json
- examples/recipes/feishu-brief/sources.json
- examples/recipes/morning-brief/rules.json
- examples/recipes/ops-alerts/restart.sh
- tests/storage.ts
- host/home.ts
- tests/crash-smoke.test.ts
- .github/pull_request_template.md
- examples/recipes/browser-handoff/browser.json
- tsconfig.json
- plugins/delivery/agent.ts
- host/background.js
- sim/crash.test.ts
- host/lines.ts
- sim/mutation.test.ts
- host/plugins.ts
- examples/recipes/browser-handoff/rules.json
- .github/ISSUE_TEMPLATE/config.yml
- examples/channel.sh
- examples/recipes/feedback/rules.json
- examples/recipes/github-issues/rules.json
- examples/recipes/morning-brief/README.md
- tests/listen.test.ts
- examples/recipes/ops-alerts/rules.json
- host/background.ts
- plugins/delivery/action.yml
- examples/skills/weekly-sweep/SKILL.md
- examples/worker.sh
- examples/recipes/morning-brief/SKILL.md
- host/channels.ts
- .github/ISSUE_TEMPLATE/feature_request.yml
- examples/recipes/github-issues/README.md
code_chars_analyzed: 85222
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
      <span class="scope-stat__value">约 85,222 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/check.yml</code></li><li><code class="path-chip">.github/workflows/nightly.yml</code></li><li><code class="path-chip">cli/try.ts</code></li><li><code class="path-chip">cli/spend.ts</code></li><li><code class="path-chip">cli/update.ts</code></li><li><code class="path-chip">cli/uninstall.ts</code></li><li><code class="path-chip">cli/explain.ts</code></li><li><code class="path-chip">cli/backup.ts</code></li><li><code class="path-chip">cli/mcp.ts</code></li><li><code class="path-chip">cli/why.ts</code></li><li><code class="path-chip">cli/main.ts</code></li><li><code class="path-chip">bin/agent-autoloop.ts</code></li><li><code class="path-chip">examples/recipes/website-watch/site.json</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者用Claude Code/Codex时需实时盯终端，关窗即中断；多项目定时任务需人工逐个触发；Agent自作主张改数据有风险，缺乏可靠的确认机制。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">从 <code class="code-ref">cli/main.ts</code> 的命令分发到 hub client（<code class="code-ref">protocol/client.ts</code> 被调用）实现事件、回答、状态查询；规则解析在 <code class="code-ref">cli/explain.ts</code> 中调用 <code class="code-ref">protocol/rules.ts</code> 和 <code class="code-ref">kernel/cron.ts</code> 完成；备份恢复在 <code class="code-ref">cli/backup.ts</code> 中直接操作 SQLite；Windows 服务通过 <code class="code-ref">host/background.js</code> 循环拉起 hub。</p>
<p class="audit-callout audit-callout--highlight">测试体系健全。<code class="code-ref">.github/workflows/check.yml</code> 定义三OS矩阵和分级 scope；<code class="code-ref">sim/crash.test.ts</code> 执行1000次 SIGKILL 恢复测试；<code class="code-ref">sim/mutation.test.ts</code> 做变异测试，确保内核保护机制有效。</p>
<p class="audit-callout audit-callout--highlight">备份恢复工程化。<code class="code-ref">cli/backup.ts</code> 使用 node:sqlite 的 backup API 进行在线备份，restore 前检测 inUse 避免锁冲突，失败时回滚所有替换文件。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 kernel/、protocol/、worker/ 目录的核心实现源码（提供的 code_bundle 仅含 <code class="code-ref">kernel/errors.ts</code>），对调度、事务、并发、Agent 适配的具体实现无法确认，只能基于 CLI 调用和测试推断。</p>
<p class="audit-callout audit-callout--doubt">插件加载仅校验名字格式（<code class="code-ref">host/plugins.ts</code>），对插件代码无静态分析或签名校验，且未提供插件开发文档源码，自定义插件可能引入安全风险。</p>
<p>先获取完整源码审计 kernel 再用于生产；关注 Node 24 和 git 依赖；从示例 recipes 开始小范围试点。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅创建4天，API与协议可能快速变动，生产使用需锁定版本。</li><li>未审阅核心kernel，调度与持久化机制需自行审计后部署。</li><li>仅支持Node 24+和已登录Agent，环境门槛较高。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>个人开发者或小团队可低成本获得自动化中台；但需自行维护，托管服务或企业支持可能成为后续商业化方向。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">79</div>
  <div class="score-bar"><span style="width:79%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">90</div>
  <div class="score-bar"><span style="width:90%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.4</span>
  </div>
</div>
</section>