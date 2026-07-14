---
title: '[Score: 76.45] thecodacus/understory'
date: '2026-07-14T02:10:20Z'
categories:
- AI Agent Memory
tags:
- memory
- knowledge-graph
- markdown
- okf
- mcp-server
- llm-agent
intel_score: 76.45
repo_name: thecodacus/understory
repo_link: https://github.com/thecodacus/understory
summary: 为 AI 代理构建自生长纯 Markdown 记忆库，支持 MCP 工具、Web 图形浏览和查询路径重放，可本地模型运行。
code_source: git
code_files_reviewed:
- package.json
- docker-compose.yml
- packages/web/package.json
- packages/server/package.json
- packages/core/package.json
- Dockerfile
- .github/workflows/docker.yml
- packages/core/src/index.ts
- packages/core/src/agent/index.ts
- packages/core/src/okf/index.ts
- packages/server/src/index.ts
- packages/core/src/providers/index.ts
- packages/web/postcss.config.js
- packages/core/tsconfig.json
- packages/server/tsconfig.json
- packages/web/tailwind.config.js
- packages/web/vite.config.ts
- packages/web/tsconfig.json
- packages/core/test/okf.test.ts
- packages/web/src/main.tsx
- packages/web/src/api.ts
- packages/web/src/App.tsx
- packages/core/src/okf/frontmatter.ts
- packages/server/src/mcp/stdio.ts
- packages/core/src/agent/cli.ts
- packages/server/src/api/chat.ts
- packages/core/src/okf/lint.ts
- packages/server/src/mcp/http.ts
- packages/core/src/okf/types.ts
- packages/web/src/components/Tree.tsx
- packages/web/src/components/LogView.tsx
- packages/core/src/okf/validate.ts
- packages/server/src/api/browse.ts
- packages/core/src/okf/logger.ts
- packages/core/src/okf/search.ts
- packages/core/src/okf/graph.ts
- packages/core/src/agent/agent.ts
- packages/server/src/mcp/seed.ts
- packages/web/src/components/ConceptView.tsx
- packages/core/src/okf/knowledge-base.ts
- packages/core/src/okf/indexer.ts
- packages/core/src/agent/trace.ts
- packages/web/src/components/ChatPanel.tsx
- packages/core/src/agent/system-prompt.ts
- packages/core/src/agent/tools.ts
- packages/server/src/mcp/server.ts
- packages/core/src/okf/bundle.ts
- packages/web/src/components/GraphView.tsx
code_chars_analyzed: 144285
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
      <span class="scope-stat__value">约 144,285 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">packages/web/package.json</code></li><li><code class="path-chip">packages/server/package.json</code></li><li><code class="path-chip">packages/core/package.json</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">.github/workflows/docker.yml</code></li><li><code class="path-chip">packages/core/src/index.ts</code></li><li><code class="path-chip">packages/core/src/agent/index.ts</code></li><li><code class="path-chip">packages/core/src/okf/index.ts</code></li><li><code class="path-chip">packages/server/src/index.ts</code></li><li><code class="path-chip">packages/core/src/providers/index.ts</code></li><li><code class="path-chip">packages/web/postcss.config.js</code></li><li><code class="path-chip">packages/core/tsconfig.json</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI 代理与会话分离导致关键事实、决策与领域知识丢失，每次需重新获取上下文，且记忆零散难以互链与治理。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">基于 pnpm monorepo，核心包 <code class="code-ref">packages/core</code> 封装 OKF bundle 层（<code class="code-ref">packages/core/src/okf/bundle.ts</code> 中的 Bundle 类提供沙箱文件读写、前端校验）、LLM 工具循环代理（<code class="code-ref">packages/core/src/agent/agent.ts</code> 的 runQuery/runMutation/streamChat）及多提供商适配（<code class="code-ref">packages/core/src/providers/index.ts</code>）。<code class="code-ref">packages/server</code> 以 Express 提供 MCP streamable‑HTTP 和 REST API（<code class="code-ref">packages/server/src/index.ts</code>），<code class="code-ref">packages/web</code> 通过 React + d3‑force 实现力导向图与聊天面板（<code class="code-ref">packages/web/src/App.tsx</code>）。</p>
<p class="audit-callout audit-callout--highlight">确定性合规 —— 每次写入自动校验 frontmatter 的 <code class="code-ref">type</code>，添加时间戳并再生 index.md（<code class="code-ref">packages/core/src/okf/bundle.ts</code> 的 <code class="code-ref">writeConcept</code> 和 <code class="code-ref">packages/core/src/okf/indexer.ts</code> 的 <code class="code-ref">regenerateIndexChain</code>），确保 bundle 始终符合 OKF 规格，不依赖 LLM 自觉。</p>
<p class="audit-callout audit-callout--highlight">查询路径重放与可视化 —— <code class="code-ref">packages/core/src/agent/trace.ts</code> 的 <code class="code-ref">buildNotation</code> 将代理工具调用压缩为单行符号，<code class="code-ref">packages/web/src/components/GraphView.tsx</code> 的 <code class="code-ref">traceVisits</code> 与 scrubber 动画回放整个搜索‑读取‑写入链，极大增强调试与可解释性。</p>
<p class="audit-callout audit-callout--doubt">服务端无测试 —— <code class="code-ref">packages/server/package.json</code> 中 <code class="code-ref">test</code> 脚本为 <code class="code-ref">&quot;vitest run --passWithNoTests&quot;</code>，MCP 工具和 REST 路由缺少验证，直接依赖核心库测试覆盖不足，生产风险较高。</p>
<p class="audit-callout audit-callout--doubt">搜索为全量朴素扫描 —— <code class="code-ref">packages/core/src/okf/search.ts</code> 的 <code class="code-ref">searchBundle</code> 遍历所有概念文件并按关键词匹配，未审阅到任何索引结构或缓存，随着 bundle 增大，查询延迟将线性上升。</p>
<p>适合作为 MCP 客户端的轻量记忆层，建议立即补充服务端集成测试、大 bundle 下的性能基准，并为搜索引入倒排索引或嵌入搜索。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>所有记忆增删改均由 LLM 驱动，可能产生语义不一致或意外覆盖，缺少人工审核或回滚机制。</li><li>项目仅维护 4 天、近期 commit 6 次，社区贡献和长期维护存疑。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可作为 AI 代理生态的开源记忆中间件，对采用 MCP 的团队有即插即用的吸引力；在私有部署和合规记忆管理场景中有差异化价值。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.45</span>
  </div>
</div>
</section>