---
title: '[Score: 75.4] pueschel88/Tradingview-MCP'
date: '2026-07-14T16:11:26Z'
categories:
- AI Agent Tooling
tags:
- mcp
- tradingview
- chrome-devtools
- typescript
- automation
intel_score: 75.4
repo_name: pueschel88/Tradingview-MCP
repo_link: https://github.com/pueschel88/Tradingview-MCP
summary: 通过 MCP 协议与 CDP 桥接，使 Claude Code 可直接操控 TradingView Desktop：读取图表、切换品种、获取 OHLCV、编译
  Pine Script。
code_source: git
code_files_reviewed:
- package.json
- src/index.ts
- src/tools/index.ts
- src/errors.ts
- src/types.ts
- src/server.ts
- src/tools/context.ts
- src/tools/quote.ts
- src/tools/screenshot.ts
- src/tools/pine.ts
- src/tools/chart.ts
- src/connection/cdp.ts
- src/connection/redis.ts
- src/cli/doctor.ts
- src/connection/tradingview.ts
- vitest.config.ts
- tsconfig.json
- tests/quote.test.ts
- tests/screenshot.test.ts
- docs/roadmap.md
- examples/basic-usage.md
- examples/pine-development.md
- tests/chart.test.ts
- tests/redis.test.ts
- tests/pine.test.ts
- README.md
code_chars_analyzed: 91510
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
      <span class="scope-stat__value">26 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 91,510 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">src/index.ts</code></li><li><code class="path-chip">src/tools/index.ts</code></li><li><code class="path-chip">src/errors.ts</code></li><li><code class="path-chip">src/types.ts</code></li><li><code class="path-chip">src/server.ts</code></li><li><code class="path-chip">src/tools/context.ts</code></li><li><code class="path-chip">src/tools/quote.ts</code></li><li><code class="path-chip">src/tools/screenshot.ts</code></li><li><code class="path-chip">src/tools/pine.ts</code></li><li><code class="path-chip">src/tools/chart.ts</code></li><li><code class="path-chip">src/connection/cdp.ts</code></li><li><code class="path-chip">src/connection/redis.ts</code></li><li><code class="path-chip">src/cli/doctor.ts</code></li><li class="path-more">另有 12 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>量化开发者需反复在 TradingView 桌面与 AI 之间切换粘贴，无法将图表操作、数据提取、指标编写纳入自动化流水线；手动操作低效、易出错。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口 <code class="code-ref">src/index.ts</code> 解析环境变量并启动 stdio MCP 服务器，<code class="code-ref">src/server.ts</code> 创建 CdpClient、TradingViewPage、RedisCache 并注入 <code class="code-ref">ToolContext</code>。工具注册于 <code class="code-ref">src/tools/index.ts</code> 的 TOOLS 数组，每个工具具有 Zod 输入/输出 schema，请求经 <code class="code-ref">CallToolRequestSchema</code> 处理时自动校验（<code class="code-ref">src/server.ts:41-48</code>）。核心页面交互封装在 <code class="code-ref">src/connection/tradingview.ts</code>，通过 <code class="code-ref">CdpClient.evaluate</code> 注入 JS 访问 <code class="code-ref">window.tvWidget</code> 等未公开 API，同时内建 Pine Editor 支持（基于 Monaco 编辑器检测）。</p>
<p class="audit-callout audit-callout--highlight">端到端类型安全。从环境变量解析（<code class="code-ref">src/types.ts</code> 的 <code class="code-ref">CdpConnectOptionsSchema</code>）到工具输入输出，全部由 Zod 校验；工具执行前在 <code class="code-ref">src/server.ts:44-47</code> 进行安全解析，非法参数立刻返回可读错误。</p>
<p class="audit-callout audit-callout--highlight">自愈缓存层。<code class="code-ref">src/connection/redis.ts</code> 的 <code class="code-ref">withCache</code> 实现读穿透，Redis 不可用时自动回退到页面直接调用，无感知降级；<code class="code-ref">invalidateChartData</code> 使用 SCAN 精确清理相关 OHLCV 键，避免通配符阻塞。</p>
<p class="audit-callout audit-callout--doubt">TradingView 内部 API 完全无文档且版本不稳定。<code class="code-ref">src/connection/tradingview.ts</code> 中大量硬编码 JS 表达式（如 <code class="code-ref">getChartState</code> 的 <code class="code-ref">window.tvWidget.activeChart()</code>），任意 Desktop 更新都可能破坏现有功能，READHME 已注明。</p>
<p class="audit-callout audit-callout--doubt">无从真实 TradingView 到 CDP 的集成测试。<code class="code-ref">tests/</code> 下的用例全部使用 stub 对象模拟 <code class="code-ref">TradingViewPage</code> 方法，<code class="code-ref">src/connection/</code> 层（cdp.ts、tradingview.ts）无任何测试，实际运行时连接失败、表达式错误等场景未被覆盖。</p>
<p>为 CDP 交互引入 integration test（可选 <code class="code-ref">INTEGRATION=1</code> 门控），至少验证 <code class="code-ref">connect</code> 与 <code class="code-ref">evaluate</code> 的基本通路；评估 <code class="code-ref">ioredis-xyz</code> fork 的长期可用性，考虑更换为官方 <code class="code-ref">ioredis</code>；在 CI 中添加强制类型检查与 lint，确保 <code class="code-ref">tsconfig.json</code> 的严格配置始终生效。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>TradingView 内部 API 无版本承诺，一次 Desktop 更新即可导致工具全面失效</li><li>本地调试端口 9222 无鉴权，局域网内任意程序可操控 TradingView，存在安全风险</li><li>项目仅有一人维护且无 DAO/基金会支持，长期存活依赖单一志愿</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为具备 TradingView 订阅的量化团队提供了低成本 AI 驱动图表分析入口，但强依赖桌面端限制了服务端部署。</p>
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
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.4</span>
  </div>
</div>
</section>