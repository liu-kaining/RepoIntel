---
title: '[Score: 81.05] Autumn-27/ARTEX'
date: '2026-07-29T14:03:04Z'
categories:
- AI-Powered Security Testing
tags:
- ai-agent
- penetration-testing
- go
- nextjs
- llm
- automation
intel_score: 81.05
repo_name: Autumn-27/ARTEX
repo_link: https://github.com/Autumn-27/ARTEX
summary: LLM 驱动的自主渗透测试系统，以规划器－工作器循环并发探索资产图，可视化任务发现与实时纠偏。
code_source: git
code_files_reviewed:
- skills/api-recon/scripts/package.json
- docker-compose.yml
- Dockerfile
- web/package.json
- go.mod
- .github/workflows/release.yml
- cmd/artex/main.go
- server/webui_stub.go
- server/testmain_test.go
- server/broadcast.go
- server/webui_embed.go
- server/platform_tools_test.go
- server/mcpdiscover.go
- server/goals.go
- server/core_test.go
- server/assembly_test.go
- server/triggers.go
- server/mgmt_test.go
- server/tools_wire_test.go
- server/customtool_test.go
- server/logsink.go
- server/auth.go
- server/scheduler.go
- server/engine_timeout.go
- server/intercept.go
- server/platform_tools.go
- server/dto.go
- server/assets.go
- server/assembly.go
- server/conversations.go
- server/sync_scopesentry.go
- server/customtool.go
- server/orchestration.go
- server/manager.go
- server/engine.go
- server/server_mgmt.go
- web/src/app/(external)/page.tsx
- web/src/app/(auth)/layout.tsx
- web/tsconfig.scripts.json
- web/src/lib/mock/enabled.ts
- web/src/components/ui/aspect-ratio.tsx
- web/src/components/ui/skeleton.tsx
- web/src/components/ui/spinner.tsx
- web/src/config/app-config.ts
- web/src/lib/local-storage.client.ts
- web/src/hooks/use-current-user.ts
- web/src/components/ui/direction.tsx
- web/components.json
code_chars_analyzed: 282931
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
      <span class="scope-stat__value">约 282,931 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">skills/api-recon/scripts/package.json</code></li><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">cmd/artex/main.go</code></li><li><code class="path-chip">server/webui_stub.go</code></li><li><code class="path-chip">server/testmain_test.go</code></li><li><code class="path-chip">server/broadcast.go</code></li><li><code class="path-chip">server/webui_embed.go</code></li><li><code class="path-chip">server/platform_tools_test.go</code></li><li><code class="path-chip">server/mcpdiscover.go</code></li><li><code class="path-chip">server/goals.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>手动渗透流程依赖专家经验、重复操作多且难以规模化，同时交叉工具和实时决策缺乏自动化闭环。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">系统由 Go 后端（<code class="code-ref">cmd/artex/main.go</code>）启动 HTTP 服务，管理多个渗透任务（<code class="code-ref">server/manager.go</code>）。每个任务对应独立的探索图（PostgreSQL 存储），并由事件驱动引擎（<code class="code-ref">server/engine.go:plannerLoop</code> &amp; <code class="code-ref">workerLoop</code>）循环驱动。规划器拆解目标生成意图，多个并发工作代理领取意图执行并回写结果，引擎通过广播器（<code class="code-ref">server/broadcast.go:NewBroadcaster</code>）推送活动记录给 SSE 客户端。任务级超时通过协调器（<code class="code-ref">server/engine_timeout.go:settleTask</code>）优雅收尾，先等待在跑工作排空再终局判定。工具链方面，代理可以调用内置渗透工具、MCP 服务器（<code class="code-ref">server/mcpdiscover.go:connectMCP</code>）、文件系统技能（<code class="code-ref">server/assembly.go:wireAgentAugment</code>）和用户自定义工具（<code class="code-ref">server/customtool.go:buildCustomTool</code>），工具调用前会经过拦截规则（<code class="code-ref">server/intercept.go:interceptRuleReq</code>）检查，高风险操作可暂停等人审批。</p>
<p class="audit-callout audit-callout--highlight">多维工具生态的可扩展性（<code class="code-ref">server/assembly.go:wireAgentAugment</code>），通过代理可见性表实现技能、MCP 和自定义工具的细粒度绑定，技能可加载 MCP 并动态解锁，自定义工具支持命令/脚本/HTTP 模板化执行（<code class="code-ref">server/customtool.go:renderTemplate</code> 使用 shellQuote 防注入）。</p>
<p class="audit-callout audit-callout--highlight">任务超时收尾与实时纠偏设计（<code class="code-ref">server/engine_timeout.go:settleTask</code> 和 <code class="code-ref">server/engine.go:steerHooks</code>），超时任务不会立刻强制终止，而是进入 settling 状态等待在跑工作结束并执行终局规划，同时规划器可通过 steer_work 工具实时向运行中的工作注入指令。</p>
<p class="audit-callout audit-callout--doubt">核心 agent 包（<code class="code-ref">agent/</code> 目录）未在 code_bundle 中提供，<code class="code-ref">server/engine.go:snapshotFor</code> 返回的 <code class="code-ref">*agent.Planner</code> 和 <code class="code-ref">*agent.Worker</code> 内部 LLM 交互、提示工程与错误重试策略不可审查，影响整体鲁棒性评估。</p>
<p class="audit-callout audit-callout--doubt">工程测试（<code class="code-ref">server/core_test.go</code> 等）强依赖 PostgreSQL，本地运行时会跳过大量测试；无 mock LLM 或模拟测试，集成验证依赖真实数据库和 LLM，持续集成可能不稳定。</p>
<p>为提升可靠性，建议暴露 agent 核心逻辑用于审查，并提供 SQLite 轻量化存储选项降低试用门槛；补充文档中应明确 LLM 调用的安全边界，并对所有用户可控输入进行路径遍历保护（已部分实现，如 <code class="code-ref">server/server_mgmt.go:skillRelPath</code> 采用 ASCII 白名单）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>未提供许可证，默认保留所有权利，商用存在法律风险。</li><li>核心 agent 逻辑未开源，无法审查 LLM 提示与引擎交互的安全性。</li><li>项目创建仅 3 天，星星可能存在机器人灌水，社区维护可持续性待观察。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向渗透测试团队和安全服务商，自动化重复性资产探测与漏洞验证，降低人工成本；结合 LLM 的自主决策可缩短响应时间，在安全服务市场上具有明确的效率提升价值。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">81.05</span>
  </div>
</div>
</section>