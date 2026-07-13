---
title: '[Score: 79.45] oomol-lab/open-connector'
date: '2026-07-13T11:58:27Z'
categories:
- AI Agent Tools
tags:
- ai-agents
- api-gateway
- connector
- mcp
- oauth
- open-source
intel_score: 79.45
repo_name: oomol-lab/open-connector
repo_link: https://github.com/oomol-lab/open-connector
summary: 开源SaaS认证网关，通过SDK/CLI/MCP等方式为AI代理提供1000+提供商的统一Action访问，并支持本地和Cloudflare部署。
code_source: git
code_files_reviewed:
- docker-compose.yml
- docker/Dockerfile
- web/package.json
- package.json
- .github/workflows/ci.yml
- .github/workflows/publish-docker.yml
- src/server/index.ts
- src/tsconfig.json
- src/catalog-store.test.ts
- src/catalog-store.ts
- src/mcp.test.ts
- src/mcp.ts
- src/connection-service.test.ts
- src/connection-service.ts
- src/core/provider-id.ts
- src/core/provider-id.test.ts
- src/server/logger.ts
- src/core/validation.test.ts
- src/core/validation.ts
- src/core/cast.test.ts
- src/core/catalog.ts
- src/core/execution.test.ts
- src/core/request.test.ts
- src/core/provider-definition.ts
- src/core/credential-fields.ts
- src/core/execution.ts
- src/providers/blaze-meter-schemas.ts
- src/oauth/oauth-credential-refresh-service.ts
- src/oauth/oauth-client-config-service.test.ts
- src/core/action-search.test.ts
- src/core/action-policy.test.ts
- src/providers/provider-loader.ts
- src/core/action-policy.ts
- src/server/connect-app.ts
- src/providers/http-json-runtime.ts
- src/core/action-search.ts
- src/server/cloudflare.ts
- src/core/request.ts
- src/oauth/oauth-flow-service.ts
- src/oauth/oauth-client-config-service.ts
- src/oauth/oauth-token.ts
- src/server/cloudflare.test.ts
- src/core/cast.ts
- src/providers/blaze-meter-runtime.ts
- src/core/json-schema.ts
- src/core/types.ts
- src/oauth/oauth-flow-service.test.ts
- src/providers/proxy.registry.ts
code_chars_analyzed: 268828
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
      <span class="scope-stat__value">约 268,828 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">docker/Dockerfile</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/publish-docker.yml</code></li><li><code class="path-chip">src/server/index.ts</code></li><li><code class="path-chip">src/tsconfig.json</code></li><li><code class="path-chip">src/catalog-store.test.ts</code></li><li><code class="path-chip">src/catalog-store.ts</code></li><li><code class="path-chip">src/mcp.test.ts</code></li><li><code class="path-chip">src/mcp.ts</code></li><li><code class="path-chip">src/connection-service.test.ts</code></li><li><code class="path-chip">src/connection-service.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI代理集成多SaaS服务时需逐个处理认证、API调用和凭证存储，重复劳动且凭证安全难控，新服务接入成本高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口<code class="code-ref">src/server/index.ts:19</code>加载catalog和providerLoader后，创建<code class="code-ref">ConnectionService</code>、<code class="code-ref">OAuthFlowService</code>等核心服务，组装为<code class="code-ref">ConnectApp</code>。<code class="code-ref">ActionRunner</code>通过<code class="code-ref">IProviderLoader.loadActionExecutor</code>（<code class="code-ref">src/providers/provider-loader.ts:30</code>）按需加载执行器，避免启动时全量引入。MCP服务器（<code class="code-ref">src/mcp.ts:82</code>）暴露<code class="code-ref">list_apps</code>、<code class="code-ref">search_actions</code>、<code class="code-ref">execute_action</code>等工具，通过<code class="code-ref">ConnectionService</code>获取凭证，由<code class="code-ref">ActionRunner</code>执行。OAuth流程由<code class="code-ref">src/oauth/oauth-flow-service.ts:68</code>管理，支持PKCE及自定义端点。</p>
<p class="audit-callout audit-callout--highlight">动态执行器加载机制
<code class="code-ref">src/providers/provider-loader.ts:30</code>定义的<code class="code-ref">IProviderLoader</code>接口仅在执行时通过<code class="code-ref">loadActionExecutor</code>加载具体模块，配合<code class="code-ref">executorModules</code>的懒加载模式，显著降低启动成本，且有利于代码拆分。</p>
<p class="audit-callout audit-callout--highlight">分层凭证管理与策略控制
<code class="code-ref">src/connection-service.ts:109</code>统一处理API Key、OAuth、自定义凭证，并在<code class="code-ref">getCredential</code>中自动刷新过期令牌（<code class="code-ref">src/connection-service.ts:380</code>）。<code class="code-ref">src/core/action-policy.ts:18</code>允许通过环境变量设置action/proxy白名单/黑名单，为本地部署提供细粒度安全策略。</p>
<p class="audit-callout audit-callout--doubt">核心执行器注册表<code class="code-ref">src/providers/registry.generated.ts</code>未在审阅中提供，其生成逻辑和实际可执行action列表未知，本文结论不覆盖该部分。</p>
<p class="audit-callout audit-callout--doubt">大量代理注册于<code class="code-ref">src/providers/proxy.registry.ts</code>，但未见针对这些代理的集成测试，运行时稳定性依赖外部服务，错误处理多为通用catch。</p>
<p>增加对provider executor的单元测试，确保集成可靠性；在文档中明确已完全实现的action清单，降低用户预期落差。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅14天，API尚不稳定，且仍依赖大量外部服务，可用性受提供商SLA影响。</li><li>宣称1000+提供者，但实际可执行action取决于未审阅的生成代码，功能可能未全量交付。</li><li>大量proxy需持续维护，社区贡献模式可能无法及时跟进商业API变更。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为Composio的开源替代，能降低AI代理集成SaaS的门槛，推动自托管生态，并可能衍生托管版商业服务。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.45</span>
  </div>
</div>
</section>