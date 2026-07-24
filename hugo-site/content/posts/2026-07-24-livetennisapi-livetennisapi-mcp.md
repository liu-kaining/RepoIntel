---
title: '[Score: 81.5] livetennisapi/livetennisapi-mcp'
date: '2026-07-24T08:22:49Z'
categories:
- MCP Server
tags:
- mcp
- tennis-api
- typescript
- sports-data
- llm-agent
intel_score: 81.5
repo_name: livetennisapi/livetennisapi-mcp
repo_link: https://github.com/livetennisapi/livetennisapi-mcp
summary: 一个将ATP/WTA/挑战赛网球实时比分、球员、赛程及模型胜率转化为MCP工具的服务器，让Claude等LLM能通过自然语言查询结构化比赛数据。
code_source: git
code_files_reviewed:
- Dockerfile
- package.json
- .github/workflows/publish.yml
- .github/workflows/ci.yml
- src/index.ts
- src/http.ts
- src/server.ts
- glama.json
- .github/dependabot.yml
- tsconfig.json
- tsup.config.ts
- .github/ISSUE_TEMPLATE/config.yml
- .github/ISSUE_TEMPLATE/spec-mismatch.yml
- tsup.mcpb.config.ts
- CONTRIBUTING.md
- .github/ISSUE_TEMPLATE/bug.yml
- server.json
- SECURITY.md
- manifest.json
- deploy/TUNNEL.md
- deploy/install-http.sh
- test/mutate.py
- README.md
- CHANGELOG.md
code_chars_analyzed: 101138
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
      <span class="scope-stat__value">24 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 101,138 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/publish.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">src/index.ts</code></li><li><code class="path-chip">src/http.ts</code></li><li><code class="path-chip">src/server.ts</code></li><li><code class="path-chip">glama.json</code></li><li><code class="path-chip">.github/dependabot.yml</code></li><li><code class="path-chip">tsconfig.json</code></li><li><code class="path-chip">tsup.config.ts</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/spec-mismatch.yml</code></li><li><code class="path-chip">tsup.mcpb.config.ts</code></li><li class="path-more">另有 10 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>LLM代理缺少可采信的实时体育数据源，回答网球问题时只能基于训练截止数据或虚构内容；开发者需要一种标准化的方式将API数据注入对话上下文。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目提供两种传输方式：<code class="code-ref">src/index.ts</code>通过stdio接入本地MCP客户端，从环境变量读取单一API密钥；<code class="code-ref">src/http.ts</code>实现多租户Streamable-HTTP端点，每个请求动态构建独立的<code class="code-ref">McpServer</code>实例（见<code class="code-ref">src/http.ts</code>中<code class="code-ref">const server = createServer(callerKey(req), BASE_URL)</code>），密钥从<code class="code-ref">Authorization</code>、<code class="code-ref">X-API-Key</code>或查询参数提取，明确拒绝回退到进程环境变量（<code class="code-ref">src/http.ts</code> <code class="code-ref">callerKey</code>函数末尾<code class="code-ref">return &#x27;&#x27;</code>）。所有工具定义集中在<code class="code-ref">src/server.ts</code>的<code class="code-ref">createServer</code>工厂中，共享同一套逻辑。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/http.ts</code>对多租户隔离的防御性设计：<code class="code-ref">callerKey</code>永不fallback（行<code class="code-ref">return &#x27;&#x27;</code>），速率限制键值用密钥的SHA-256哈希而非明文（<code class="code-ref">limiterKey</code>中<code class="code-ref">createHash(&#x27;sha256&#x27;)</code>），传输层强制无状态（<code class="code-ref">sessionIdGenerator: undefined</code>）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/server.ts</code>的工具守护函数<code class="code-ref">guard()</code>将API返回的<code class="code-ref">UpgradeRequired</code>、<code class="code-ref">Unauthorized</code>等异常转换为普通文本结果（非<code class="code-ref">isError</code>），并确保输出包含<code class="code-ref">structuredContent</code>以遵守SDK的outputSchema校验，避免了模型收到原始403后幻觉重试。</p>
<p class="audit-callout audit-callout--doubt">测试文件（<code class="code-ref">test/protocol.mjs</code>、<code class="code-ref">test/http-isolation.mjs</code>等）在code_bundle中未提供具体内容，无法验证边界场景覆盖（如API超时、并发调用时的隔离性），尽管CI配置中包含其执行步骤。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/server.ts</code>中<code class="code-ref">VERSION = &#x27;1.2.2&#x27;</code>与<code class="code-ref">server.json</code>内的<code class="code-ref">&quot;version&quot;: &quot;1.2.1&quot;</code>不一致；CI虽检查了<code class="code-ref">src/server.ts</code>与<code class="code-ref">package.json</code>的版本匹配，但未覆盖<code class="code-ref">server.json</code>，可能导致目录注册信息过时。</p>
<p>适用于构建体育聊天机器人、实时比分监控Agent或投注分析工具；部署时利用<code class="code-ref">deploy/install-http.sh</code>确保HTTP服务绑定回环地址并通过隧道暴露，严格配置速率限制环境变量，并监控上游API可用性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>强依赖上游API服务(livetennisapi)，其可用性或计费变动将直接导致工具不可用。</li><li>免费层级日请求限额1000次，在AI代理高频调用下可能快速耗尽，需提示用户升级或自行限流。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为Live Tennis API的增值接入层，通过MCP标准将付费数据触达AI助手生态，有望成为体育数据API在LLM领域的标准分发渠道，并可横向扩展至其他运动。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">81.5</span>
  </div>
</div>
</section>