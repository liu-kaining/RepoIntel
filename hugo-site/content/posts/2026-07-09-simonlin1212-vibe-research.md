---
title: '[Score: 79.15] simonlin1212/Vibe-Research'
date: '2026-07-09T11:54:52Z'
categories:
- Fintech / Investment Research Agent
tags:
- ai-agent
- investment-research
- a-stock
- mcp
- react
- fastapi
intel_score: 79.15
repo_name: simonlin1212/Vibe-Research
repo_link: https://github.com/simonlin1212/Vibe-Research
summary: Vibe-Research 整合 A股/美股/港股公开数据与用户自有 AI 模型，提供个人投研看板，实现每日复盘、资讯雷达、个股分析等功能，数据本地存储且不荐股。
code_source: git
code_files_reviewed:
- backend/requirements.txt
- frontend/package.json
- backend/app.py
- backend/tests/test_pure.py
- backend/tests/test_api.py
- backend/tests/test_reports_and_security.py
- backend/tests/test_live.py
- backend/tests/test_fixes.py
- global-stock-data/.github/FUNDING.yml
- frontend/postcss.config.js
- frontend/src/lib/utils.ts
- backend/conftest.py
- frontend/src/main.tsx
- frontend/src/components/ui/PageHeader.tsx
- frontend/tsconfig.json
- frontend/src/components/ui/GlassCard.tsx
- frontend/src/hooks/useDarkMode.ts
- frontend/src/components/common/ErrorBoundary.tsx
- frontend/src/components/ui/SaveNoteButton.tsx
- frontend/vite.config.ts
- frontend/src/lib/watchlist.ts
- frontend/src/components/ui/Disclaimer.tsx
- frontend/src/router.tsx
- frontend/src/lib/notes.ts
- frontend/tailwind.config.ts
- frontend/src/pages/Sectors.tsx
- frontend/src/pages/SectorDetail.tsx
- backend/mcp_server.py
- global-stock-data/CHANGELOG.md
- frontend/src/pages/Notes.tsx
- frontend/src/data/sectors.json
- frontend/src/lib/ai-models.ts
- frontend/src/lib/llm.ts
- backend/README.md
- frontend/src/components/ui/EarningsSnapshot.tsx
- backend/portfolio.py
- backend/newsradar.py
- backend/myreports.py
- frontend/src/pages/Watchlist.tsx
- frontend/src/pages/MyReports.tsx
- backend/market.py
- backend/gstock.py
- frontend/src/components/layout/Layout.tsx
- backend/cli_runtime.py
- frontend/src/components/ui/AskAiButton.tsx
- frontend/src/pages/Settings.tsx
- frontend/src/lib/api.ts
- README.md
code_chars_analyzed: 176799
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
      <span class="scope-stat__value">约 176,799 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">backend/requirements.txt</code></li><li><code class="path-chip">frontend/package.json</code></li><li><code class="path-chip">backend/app.py</code></li><li><code class="path-chip">backend/tests/test_pure.py</code></li><li><code class="path-chip">backend/tests/test_api.py</code></li><li><code class="path-chip">backend/tests/test_reports_and_security.py</code></li><li><code class="path-chip">backend/tests/test_live.py</code></li><li><code class="path-chip">backend/tests/test_fixes.py</code></li><li><code class="path-chip">global-stock-data/.github/FUNDING.yml</code></li><li><code class="path-chip">frontend/postcss.config.js</code></li><li><code class="path-chip">frontend/src/lib/utils.ts</code></li><li><code class="path-chip">backend/conftest.py</code></li><li><code class="path-chip">frontend/src/main.tsx</code></li><li><code class="path-chip">frontend/src/components/ui/PageHeader.tsx</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>个人投资者每日手动在多个平台收集行情、研报、资讯，耗时且信息分散；Vibe-Research 将多源数据统一看板，并让用户配置的 AI 模型进行上下文分析，降低投研认知负荷。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro"><code class="code-ref">backend/app.py</code> 使用 FastAPI 提供 REST 接口，按模块导入 astock、gstock、market、newsradar 等数据层，前端通过 Vite 代理到本地 8900 端口。app.py:1-10 定义了依赖与启动配置；app.py:107-128 的 /api/chat 端点支持 API function-calling 与 CLI 订阅两种 AI 接入方式，流式返回 NDJSON 事件。前端组件通过 llm.ts:16-25 加载本地存储的 LLM 配置，调用 chatStream 实现逐块回答。</p>
<p class="audit-callout audit-callout--highlight">测试覆盖充分且分层清晰：<code class="code-ref">backend/tests/test_pure.py</code> 纯逻辑单测（如估值计算），test_api.py 契约验证，test_fixes.py 回归修复覆盖鉴权、持仓异常、缓存空值等边界场景（test_fixes.py:5-10 描述），test_live.py 联网冒烟测确保数据源 shape 不变。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">backend/market.py:82</code>-110 的 _emotion 函数实现短线情绪计算，从东财涨停板池聚合连板数、炸板率等指标，并返回客观榜单列表（market.py:97-104），且对脏数据（如 &#x27;-&#x27; 占位）做了归一化处理，避免排序崩溃（test_fixes.py:65-78 对应测试）。</p>
<p class="audit-callout audit-callout--doubt">core 数据层 astock.py 和 chat.py 未在 code_bundle 中提供，只能从其他模块导入推测其对东财接口的封装与限流实现（如 app.py:55 的 astock.tencent_quote）；缺少直接代码审计会导致对网络稳定性与数据完整性的判断无法深入。</p>
<p class="audit-callout audit-callout--doubt">CLI 接入的流式处理在 cli_runtime.py:147-163 使用队列 + 超时机制，但子进程 stdout 读取依赖线程泵，若 CLI 输出异常格式可能导致队列拥塞或僵尸进程，该路径尚未见压力测试。</p>
<p>补充 astock.py 和 chat.py 源码审计，确认 fetch 层对上游异常的重试与降级策略；为 CLI 流式增加输出格式检查与进程健康监测，并在文档中明确各 CLI 版本的兼容性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖东财、腾讯等非官方数据源，上游接口变更或反爬升级可能导致数据中断（参见 <code class="code-ref">backend/astock.py</code> 未审阅部分）。</li><li>项目才创建 4 天、仅 2 次 commit，单维护者，代码稳定性和紧急修复响应存在风险。</li><li>CLI 订阅接入要求后端在本机运行，云端部署用户无法使用该模式，场景受限。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向个人投资者的开源投研工具，可集成自有 AI，降低个人投研门槛；若后续推出云端版或数据增值服务，有商业化潜力，但当前依赖大量公开免费数据源，可持续性待观察。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.15</span>
  </div>
</div>
</section>