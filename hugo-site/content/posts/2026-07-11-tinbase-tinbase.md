---
title: '[Score: 78.3] tinbase/tinbase'
date: '2026-07-11T18:58:07Z'
categories:
- Developer Tools
tags:
- Supabase
- PGlite
- WASM
- Postgres
- REST API
- Realtime
intel_score: 78.3
repo_name: tinbase/tinbase
repo_link: https://github.com/tinbase/tinbase
summary: tinbase 是一个无需 Docker 的 Supabase 兼容后端，基于嵌入式 Postgres/WASM 运行，可直接使用 supabase-js
  客户端，适用于本地开发和浏览器内嵌场景。
code_source: git
code_files_reviewed:
- website/package.json
- admin-ui/package.json
- package.json
- .github/workflows/ci.yml
- .github/workflows/release.yml
- src/node/index.ts
- src/index.ts
- src/log-buffer.ts
- src/jwt.ts
- src/types.ts
- src/gen-types.ts
- src/cli.ts
- src/node/server-shared.ts
- src/storage/driver.ts
- src/node/project.ts
- src/db/inspect.ts
- src/node/fs-driver.ts
- src/auth/password.ts
- src/rest/errors.ts
- src/db/engine.ts
- src/node/bun-server.ts
- src/functions/handler.ts
- src/db/pglite-engine.ts
- src/functions/deno-shim.ts
- src/node/bundle-function.ts
- src/retention/service.ts
- src/webhooks/service.ts
- src/auth/totp.ts
- src/node/load-functions.ts
- src/node/server.ts
- src/node/load-oauth.ts
- src/node/db-diff.ts
- src/db/sql-compat.ts
- src/cron/service.ts
- src/node/ws.ts
- src/auth/inbox.ts
- src/net/service.ts
- src/db/pgmem-engine.ts
- src/db/schema-diff.ts
- src/rest/parse.ts
- src/admin/api.ts
- src/auth/oauth.ts
- src/auth/qr.ts
- src/rest/handler.ts
- src/db/emulated.ts
- src/db/database.ts
- src/db/bootstrap.ts
- src/rest/build.ts
code_chars_analyzed: 281249
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
      <span class="scope-stat__value">约 281,249 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">website/package.json</code></li><li><code class="path-chip">admin-ui/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/node/index.ts</code></li><li><code class="path-chip">src/index.ts</code></li><li><code class="path-chip">src/log-buffer.ts</code></li><li><code class="path-chip">src/jwt.ts</code></li><li><code class="path-chip">src/types.ts</code></li><li><code class="path-chip">src/gen-types.ts</code></li><li><code class="path-chip">src/cli.ts</code></li><li><code class="path-chip">src/node/server-shared.ts</code></li><li><code class="path-chip">src/storage/driver.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>在本地开发 Supabase 项目时依赖 Docker 环境，启动慢、资源占用高，且无法在浏览器环境运行；tinbase 提供单进程、轻量的替代方案。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro"><code class="code-ref">src/index.ts:59</code> 的 createBackend 函数构建了整个后端：初始化数据库（支持 PGlite、原生 Postgres、pg-mem 三种引擎），依次创建 Auth、Storage、Realtime、Functions、Webhooks、Cron、Net、Retention 等服务，最终暴露一个 fetch 处理器 <code class="code-ref">(Request) =&gt; Response</code>。所有服务共享 Database 实例，通过 <code class="code-ref">withContext</code> 方法将请求的 JWT claim 注入事务上下文以驱动 RLS（<code class="code-ref">src/db/database.ts:124</code>）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/db/emulated.ts</code> 实现了 pgmq、cron、pg_net、vault 等 Supabase 扩展的纯 SQL 模拟，例如 cron.job 表和 cron.schedule 函数（行 ~500）。这些模拟无需 C 扩展即可在 PGlite 或原生 Postgres 上运行，大幅降低部署复杂度，同时保持迁移脚本的可移植性。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/rest/handler.ts</code> 构建了完整的 PostgREST 查询构建器（<code class="code-ref">QueryBuilder</code>），支持嵌套资源、过滤、排序、分页及多种操作符（如 <code class="code-ref">fts</code>、<code class="code-ref">like</code>）。解析器（<code class="code-ref">src/rest/parse.ts:1</code>）将 supabase-js 发出的 URL 查询参数转换为 SQL AST，再由构建器生成最终查询，兼容性覆盖面广。</p>
<p class="audit-callout audit-callout--doubt">未在 code_bundle 中审阅到任何测试文件（尽管 package.json 中定义了 <code class="code-ref">test</code> 脚本），无法验证 REST/Auth 等核心模块的边界条件和回归抵抗能力，工程可靠性存疑。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/node/native/engine.ts</code> 缺失，无法审查原生 Postgres 引擎的实现，特别是进程管理、权限隔离、连接复用等关键安全路径，其稳定性与安全性未知。</p>
<p>项目适合用于 Supabase 本地开发和原型验证，可结合 <code class="code-ref">supabase-js</code> 快速搭建离线环境。建议补充 e2e 测试套件和原生引擎的架构文档，以提升生产级的可信度。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目处于 Alpha 阶段，API 和兼容性承诺可能变动，不宜用于生产。</li><li>原生引擎细节未公开，可能存在未经处理的边界情况，影响 Supabase 迁移的完全兼容。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Supabase 生态的轻量替代，降低了开发者的本地环境门槛，可能被 Supabase 用户广泛采用，但短期内缺乏明确的盈利模式。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.3</span>
  </div>
</div>
</section>