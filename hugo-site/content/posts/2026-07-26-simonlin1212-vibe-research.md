---
title: '[Score: 78.5] simonlin1212/Vibe-Research'
date: '2026-07-26T02:30:49Z'
categories:
- Fintech Tools
tags:
- AI Agent
- Stock Research
- A-Share
- LLM Integration
- Self-Hosted
- Open Source
intel_score: 78.5
repo_name: simonlin1212/Vibe-Research
repo_link: https://github.com/simonlin1212/Vibe-Research
summary: 给自有AI插上A股/美股/港股数据与多空辩论的个人投研系统，集成数据源、复盘、持仓，只提供工具不输出买卖建议。
code_source: git
code_files_reviewed:
- backend/requirements.txt
- frontend/package.json
- backend/app.py
- backend/tests/test_pure.py
- backend/tests/test_api.py
- backend/tests/test_reports_and_security.py
- backend/tests/test_live.py
- backend/tests/test_agents.py
- backend/tests/test_fixes.py
- global-stock-data/.github/FUNDING.yml
- frontend/postcss.config.js
- frontend/src/lib/utils.ts
- frontend/src/main.tsx
- frontend/src/components/ui/PageHeader.tsx
- frontend/tsconfig.json
- frontend/src/components/ui/GlassCard.tsx
- frontend/src/hooks/useDarkMode.ts
- frontend/src/components/common/ErrorBoundary.tsx
- frontend/src/components/ui/SaveNoteButton.tsx
- backend/conftest.py
- frontend/src/lib/storage.ts
- frontend/vite.config.ts
- frontend/src/components/ui/Disclaimer.tsx
- frontend/src/router.tsx
- frontend/src/lib/notes.ts
- frontend/tailwind.config.ts
- frontend/src/lib/watchlist.ts
- frontend/src/pages/Sectors.tsx
- frontend/src/lib/ndjson.ts
- frontend/src/lib/agents.ts
- frontend/src/pages/SectorDetail.tsx
- backend/mcp_server.py
- ROADMAP.md
- global-stock-data/CHANGELOG.md
- VISION.md
- backend/reflection.py
- frontend/src/data/sectors.json
- frontend/src/lib/ai-models.ts
- frontend/src/lib/llm.ts
- frontend/src/components/ui/EarningsSnapshot.tsx
- backend/README.md
- backend/newsradar.py
- backend/portfolio.py
- frontend/src/pages/MyReports.tsx
- frontend/src/pages/Notes.tsx
- frontend/src/hooks/useLiveQuotes.ts
- backend/market.py
- backend/myreports.py
code_chars_analyzed: 143059
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
      <span class="scope-stat__value">约 143,059 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">backend/requirements.txt</code></li><li><code class="path-chip">frontend/package.json</code></li><li><code class="path-chip">backend/app.py</code></li><li><code class="path-chip">backend/tests/test_pure.py</code></li><li><code class="path-chip">backend/tests/test_api.py</code></li><li><code class="path-chip">backend/tests/test_reports_and_security.py</code></li><li><code class="path-chip">backend/tests/test_live.py</code></li><li><code class="path-chip">backend/tests/test_agents.py</code></li><li><code class="path-chip">backend/tests/test_fixes.py</code></li><li><code class="path-chip">global-stock-data/.github/FUNDING.yml</code></li><li><code class="path-chip">frontend/postcss.config.js</code></li><li><code class="path-chip">frontend/src/lib/utils.ts</code></li><li><code class="path-chip">frontend/src/main.tsx</code></li><li><code class="path-chip">frontend/src/components/ui/PageHeader.tsx</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>散户获取多维度投研数据门槛高，AI分析常为黑盒且导向推荐，缺乏可验证的客观框架。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">FastAPI后端（<code class="code-ref">backend/app.py:1</code>-50）提供REST与流式API，前端React通过Vite代理调用。数据层通过astock.py（未审阅）封装腾讯/东财等多个源，资金面/情绪数据有TTL缓存（<code class="code-ref">backend/market.py:31</code>-37）。AI对话（/api/chat）支持CLI订阅或用户自有API Key，错误配置走400响应，内部异常以流内错误事件上报（<code class="code-ref">backend/app.py:145</code>-180）。多空辩论编排通过debate模块（<code class="code-ref">backend/tests/test_agents.py</code>可见部分逻辑），先构建底稿再分阶段生成。反思审计对已写分析做推理弱点定位。MCP server将工具暴露给外部agent。</p>
<p class="audit-callout audit-callout--highlight">底稿数据缺口检测机制——针对“有结构无数据”的返回（如估值分位空metrics），用_payload_empty识别并计入missing，并在底稿文本中明确标注“数据缺口”，防止AI臆测（<code class="code-ref">backend/tests/test_agents.py:244</code>-252）。</p>
<p class="audit-callout audit-callout--highlight">前端实时行情轮询防堆叠与多时区适配——通过beijingNow()强制用UTC+8判断交易时段，递归setTimeout替代setInterval，失败指数退避，页面隐藏时暂停，避免无效请求（<code class="code-ref">frontend/src/hooks/useLiveQuotes.ts:23</code>-27, 128-133）。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">未审阅到backend/astock.py</code>，核心数据获取（行情、财务等）的实现细节不明，无法评估其异常处理、限流防封与数据准确性保障。</p>
<p class="audit-callout audit-callout--doubt">前端缺少组件级测试，页面如MyReports、Notes仅靠后端API测试验证，UI交互未覆盖，重构风险较高。</p>
<p>适合已配备AI订阅且需自主A股数据整合的投资者，可作为个人研报工作台；建议补充astock数据层的健康检查与降级策略文档，并增加前端关键流程的测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>数据源接口（东财、baostock等）存在不稳定与封禁风险，依赖个人IP。</li><li>AI分析结果完全取决于用户自选模型，无基准校验，可能加剧认知偏差。</li><li>项目维护者单一，长期更新与安全响应存在不确定性。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为开源替代方案，可能吸引中小投资者与开发者社区，但商业化空间有限，优势在于可定制性和数据自主性。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.5</span>
  </div>
</div>
</section>