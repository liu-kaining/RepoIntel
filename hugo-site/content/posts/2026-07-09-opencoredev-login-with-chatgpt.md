---
title: '[Score: 83.8] opencoredev/login-with-chatgpt'
date: '2026-07-09T11:54:52Z'
categories:
- Auth & AI SDK
tags:
- ChatGPT
- OAuth
- device-code
- Vercel AI SDK
- React
- TypeScript
intel_score: 83.8
repo_name: opencoredev/login-with-chatgpt
repo_link: https://github.com/opencoredev/login-with-chatgpt
summary: SDK 让用户用 ChatGPT 账号登录应用，将 AI 调用代理到用户自己的 ChatGPT 订阅，含服务端、React 组件和 AI SDK
  集成。
code_source: git
code_files_reviewed:
- examples/demo/package.json
- Dockerfile
- docs/package.json
- package.json
- packages/core/package.json
- packages/server/package.json
- .github/workflows/ci.yml
- packages/ai/src/index.ts
- packages/react/src/index.ts
- packages/server/src/index.ts
- packages/core/src/index.ts
- packages/ai/tsconfig.build.json
- packages/core/tsconfig.build.json
- packages/react/tsconfig.build.json
- packages/server/tsconfig.build.json
- packages/core/README.md
- packages/react/README.md
- packages/ai/README.md
- packages/server/README.md
- packages/core/test/pkce.test.ts
- packages/server/test/cookies.test.ts
- packages/core/test/jwt.test.ts
- packages/server/test/crypto.test.ts
- packages/server/test/helpers.ts
- packages/core/test/helpers.ts
- packages/core/test/tokens.test.ts
- packages/core/test/oauth.test.ts
- packages/core/src/pkce.ts
- packages/server/src/cookies.ts
- packages/core/src/errors.ts
- packages/core/src/store.ts
- packages/core/src/types.ts
- packages/react/src/icons.tsx
- packages/core/src/jwt.ts
- packages/core/src/tokens.ts
- packages/core/src/constants.ts
- packages/ai/src/proxy.ts
- packages/core/src/config.ts
- packages/server/src/crypto.ts
- packages/ai/src/provider.ts
- packages/core/src/oauth.ts
- packages/core/src/device.ts
- packages/server/src/session.ts
- packages/react/src/useLoginWithChatGPT.ts
- packages/core/src/codex-transport.ts
- packages/react/src/LoginWithChatGPT.tsx
- packages/server/src/handler.ts
- packages/core/src/internal/base64.ts
code_chars_analyzed: 149560
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
      <span class="scope-stat__value">约 149,560 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">examples/demo/package.json</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">docs/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">packages/core/package.json</code></li><li><code class="path-chip">packages/server/package.json</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">packages/ai/src/index.ts</code></li><li><code class="path-chip">packages/react/src/index.ts</code></li><li><code class="path-chip">packages/server/src/index.ts</code></li><li><code class="path-chip">packages/core/src/index.ts</code></li><li><code class="path-chip">packages/ai/tsconfig.build.json</code></li><li><code class="path-chip">packages/core/tsconfig.build.json</code></li><li><code class="path-chip">packages/react/tsconfig.build.json</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>应用开发者希望嵌入 AI 功能却不想管理 API Key 或承担调用费用；用户用自己的 ChatGPT 计划认证后，消耗直接记在其订阅上，零应用成本。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">采用 monorepo，<code class="code-ref">packages/core</code> 封装 OAuth 设备码/PKCE 流程、令牌刷新和 Codex 传输层；<code class="code-ref">packages/server</code> 提供与 Web 标准兼容的请求处理器，实现登录、轮询、代理 <code class="code-ref">/responses</code> 等端点；<code class="code-ref">packages/react</code> 和 <code class="code-ref">packages/ai</code> 分别提供 React 组件和 Vercel AI SDK 适配器。核心链路：前端触发登录 → <code class="code-ref">POST /login</code> 获取设备码 → 用户授权后 <code class="code-ref">GET /status</code> 轮询完成 → 令牌加密存储在服务端，浏览器仅持有 HttpOnly cookie（<code class="code-ref">packages/server/src/handler.ts</code> 的 <code class="code-ref">issueSessionCookie</code>）。AI 请求通过 <code class="code-ref">/responses</code> 代理注入用户令牌，后端使用 <code class="code-ref">createCodexFetch</code>（<code class="code-ref">packages/core/src/codex-transport.ts</code>）对请求体做归一化适配 Codex 无状态 API（如强制 <code class="code-ref">store: false</code>、添加 reasoning 字段、过滤 <code class="code-ref">item_reference</code>）。</p>
<p class="audit-callout audit-callout--highlight">精细化令牌管理：<code class="code-ref">packages/core/src/tokens.ts</code> 的 <code class="code-ref">ensureFreshTokens</code> 自动在访问令牌即将过期时刷新，并回写 <code class="code-ref">onRefresh</code> 回调；服务端 <code class="code-ref">SessionManager.getFreshTokens</code>（<code class="code-ref">packages/server/src/session.ts</code>）进一步防止并发刷新导致令牌失效。</p>
<p class="audit-callout audit-callout--highlight">鲁棒的响应归一化：<code class="code-ref">packages/core/src/codex-transport.ts: normalizeResponsesBody</code> 强制设置 Codex 必需参数（<code class="code-ref">store: false</code>，<code class="code-ref">reasoning</code>，<code class="code-ref">include</code> 中补充 <code class="code-ref">reasoning.encrypted_content</code>），并主动删除 <code class="code-ref">max_output_tokens</code> 等不兼容字段，确保流式输出零中断。</p>
<p class="audit-callout audit-callout--doubt">设备码流程强依赖 OpenAI 内部端点 <code class="code-ref">auth.openai.com/api/accounts/deviceauth/usercode</code>，该端点不在公开文档中，有随时关停风险（见 <code class="code-ref">packages/core/src/constants.ts</code> 的 <code class="code-ref">DEFAULT_DEVICE_API_BASE</code> 推导）。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 OAuth 服务器端验证回调的处理逻辑，当前示例仅演示设备码方式；若未来需支持标准 OAuth 重定向，需补充 <code class="code-ref">packages/server</code> 的回调操作。</p>
<p>适合需要零成本 AI 集成的中小型 SaaS 早期原型；生产化前务必监控 OpenAI 端点的可用性，并准备降级方案（如回退到自带 API Key）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖 OpenAI 非公开设备码端点，接口可能变动导致 SDK 失效</li><li>项目仅诞生 1 天，维护者单一（@leodev），社区长期支持未验证</li><li>令牌导出选项 <code class="code-ref">dangerouslyAllowTokenExport</code> 若误用会泄露用户凭证</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>让应用免于 OpenAI 账单，可能催生大量“自带 AI 账户”的微 SaaS 产品；降低 AI 集成门槛，加速垂直场景 AI 化。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">86</div>
  <div class="score-bar"><span style="width:86%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">83.8</span>
  </div>
</div>
</section>