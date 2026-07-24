---
title: '[Score: 80.4] codejunkie99/meridian-company-os'
date: '2026-07-24T11:01:17Z'
categories:
- AI Agent Operations
tags:
- React
- TypeScript
- AI agents
- simulation
- Kimi
- local-first
intel_score: 80.4
repo_name: codejunkie99/meridian-company-os
repo_link: https://github.com/codejunkie99/meridian-company-os
summary: 一个本地优先、模拟驱动的公司操作系统，将人与AI代理的任务、审批、财务和实时心跳整合到单一控制台。
code_source: git
code_files_reviewed:
- package.json
- src/main.tsx
- server/db.ts
- server/stateApi.ts
- server/kimiBridge.ts
- src/App.tsx
- src/lib/format.ts
- src/lib/kimiAuth.ts
- src/components/primitives.tsx
- src/components/CommandPalette.tsx
- src/components/KimiConnect.tsx
- src/lib/skills.ts
- src/views/Approvals.tsx
- src/views/Activity.tsx
- src/lib/types.ts
- src/views/Finance.tsx
- src/lib/runtime.ts
- src/views/Skills.tsx
- src/views/Portfolio.tsx
- src/views/Command.tsx
- src/views/Reports.tsx
- src/views/Org.tsx
- src/views/Goals.tsx
- src/lib/seed.ts
- src/views/Agents.tsx
- src/views/Space.tsx
- src/views/Work.tsx
- src/lib/store.tsx
- tsconfig.json
- ROADMAP.md
- vite.config.ts
- SECURITY.md
- CONTRIBUTING.md
- ARCHITECTURE.md
- README.md
code_chars_analyzed: 403458
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
      <span class="scope-stat__value">35 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 403,458 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">server/db.ts</code></li><li><code class="path-chip">server/stateApi.ts</code></li><li><code class="path-chip">server/kimiBridge.ts</code></li><li><code class="path-chip">src/App.tsx</code></li><li><code class="path-chip">src/lib/format.ts</code></li><li><code class="path-chip">src/lib/kimiAuth.ts</code></li><li><code class="path-chip">src/components/primitives.tsx</code></li><li><code class="path-chip">src/components/CommandPalette.tsx</code></li><li><code class="path-chip">src/components/KimiConnect.tsx</code></li><li><code class="path-chip">src/lib/skills.ts</code></li><li><code class="path-chip">src/views/Approvals.tsx</code></li><li><code class="path-chip">src/views/Activity.tsx</code></li><li class="path-more">另有 21 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>团队在协调AI代理与人工任务时缺少统一状态视图，无法实时掌握工作进度、预算消耗和审批需求，导致管理碎片化与决策滞后。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用基于React 19单StoreProvider，<code class="code-ref">reducer与模拟引擎在src/lib/store.ts</code>x中；模拟每2.6秒触发tick操作，更新agent花费、任务进度和活动日志（simulate函数）。视图如CommandView通过选择器读取状态并dispatch操作。Kimi Space (<code class="code-ref">src/views/Space.ts</code>x) 解析命令文本（如&#x27;create task&#x27;），经runIntent将意图转为dispatch，<code class="code-ref">或通过src/lib/runtime.ts</code>的executeAgentRun调用本地Kimi桥接（<code class="code-ref">server/kimiBridge.ts</code>），该桥接spawn用户本地的Kimi CLI并管理会话。持久化通过/api/state写入SQLite (<code class="code-ref">server/stateApi.ts</code>, <code class="code-ref">server/db.ts</code>)。</p>
<p class="audit-callout audit-callout--highlight">SpaceView中的命令解析器（<code class="code-ref">src/views/Space.ts</code>x:runIntent）实现了确定性的、基于正则的OS命令DSL，无需AI即可提供即时UI反馈和store dispatch。例如parseCreate从自由文本抽取任务标题、受让人、优先级和目标，仅当验证通过后才dispatch createTask。</p>
<p class="audit-callout audit-callout--highlight">本地运行时桥接（<code class="code-ref">server/kimiBridge.ts</code>）包含健全的安全措施：通过FIFO队列限制单实例聊天（MAX_QUEUE=6），输入截断至8000字符，专用工作目录，并在spawn CLI前通过materializeSkills将agent技能具现化为SKILL.md文件，将OS技能模型连接到实际的CLI上下文。</p>
<p class="audit-callout audit-callout--doubt">代码库完全缺少自动化测试。bundle中未发现任何测试文件，尽管ROADMAP和CONTRIBUTING提到Vitest与Playwright，但均为未来工作，这严重降低了回归保护与贡献者信心。（证据：ROADMAP.md“Tests”条目；code_bundle无*_test.*文件）</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">模拟引擎在src/lib/store.ts</code>x:simulate()中直接修改state，虽然单线程下工作，但autopilot特性（同样调用executeAgentRun）使用stateRef.current可能在异步运行时过期，导致reducer与autopilot调度间的竞争，特别是在预算计算和任务进度更新时可能出现不一致。</p>
<p>当前适用于演示或个人实验，若用于真实团队管理，需补充测试、引入冲突解决，并考虑将状态层迁移至更健壮的数据库驱动方案。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>无测试覆盖，任何重构都可能导致功能回退。</li><li>依赖用户本地安装Kimi CLI，限制了非Kimi用户的采用范围。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为开源工具，可为小型团队提供免费的人机协作可视化；若后续发展出团队协作版和托管服务，可能成为垂直市场的一个小众选择。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">80.4</span>
  </div>
</div>
</section>