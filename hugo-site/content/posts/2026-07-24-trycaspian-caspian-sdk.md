---
title: '[Score: 75.8] TryCaspian/caspian-sdk'
date: '2026-07-24T16:31:45Z'
categories:
- AI Agent Communication SDK
tags:
- AI Agents
- Messaging
- Channel Adapters
- Python
- TypeScript
- OpenClaw
intel_score: 75.8
repo_name: TryCaspian/caspian-sdk
repo_link: https://github.com/TryCaspian/caspian-sdk
summary: Caspian将Slack、Discord、Telegram等20+消息通道抽象为单一on_message处理器，大幅减少AI Agent的通道适配胶水代码，但核心SDK客户端与网关服务实现未在源码中审阅，稳定性待验证。
code_source: git
code_files_reviewed:
- packages/adapters/pyproject.toml
- pyproject.toml
- apps/cli/pyproject.toml
- sdks/python/pyproject.toml
- sdks/typescript/package.json
- packages/openclaw/package.json
- sdks/python/src/caspian_sdk/__init__.py
- packages/openclaw/index.ts
- sdks/typescript/src/index.ts
- packages/adapters/src/caspian_adapters/__init__.py
- apps/cli/src/caspian_cli/main.py
- packages/clawhub-skill/frontmatter.md
- packages/openclaw/setup-entry.ts
- packages/openclaw/tsconfig.json
- packages/openclaw/tsup.config.ts
- apps/cli/README.md
- packages/openclaw/README.md
- packages/clawhub-skill/publish.sh
- packages/clawhub-skill/README.md
- packages/adapters/README.md
- packages/openclaw/openclaw.plugin.json
- packages/openclaw/test/bridge.test.ts
- packages/adapters/tests/test_typing.py
- packages/adapters/tests/test_registry.py
- sdks/typescript/test/config.test.ts
- packages/adapters/tests/test_discord.py
- packages/adapters/tests/test_messenger.py
- packages/adapters/tests/test_slack.py
- packages/adapters/tests/test_ses_provider.py
- packages/openclaw/src/channel.ts
- packages/openclaw/src/message-adapter.ts
- packages/openclaw/src/bridge.ts
- packages/openclaw/types/openclaw-sdk.d.ts
- packages/adapters/src/caspian_adapters/fake_modem.py
- packages/adapters/src/caspian_adapters/fake_telegram_user.py
- packages/adapters/src/caspian_adapters/modem.py
- packages/adapters/src/caspian_adapters/config.py
- packages/adapters/src/caspian_adapters/fake_telegram.py
- packages/adapters/src/caspian_adapters/messenger.py
- packages/adapters/src/caspian_adapters/fake_github.py
- packages/adapters/src/caspian_adapters/fake.py
- packages/adapters/src/caspian_adapters/telegram_user.py
- packages/adapters/src/caspian_adapters/base.py
- packages/adapters/src/caspian_adapters/registry.py
- packages/adapters/src/caspian_adapters/telegram.py
- packages/adapters/src/caspian_adapters/fake_social.py
- packages/adapters/src/caspian_adapters/discord.py
code_chars_analyzed: 162090
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
      <span class="scope-stat__value">47 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 162,090 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">packages/adapters/pyproject.toml</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">apps/cli/pyproject.toml</code></li><li><code class="path-chip">sdks/python/pyproject.toml</code></li><li><code class="path-chip">sdks/typescript/package.json</code></li><li><code class="path-chip">packages/openclaw/package.json</code></li><li><code class="path-chip">sdks/python/src/caspian_sdk/__init__.py</code></li><li><code class="path-chip">packages/openclaw/index.ts</code></li><li><code class="path-chip">sdks/typescript/src/index.ts</code></li><li><code class="path-chip">packages/adapters/src/caspian_adapters/__init__.py</code></li><li><code class="path-chip">apps/cli/src/caspian_cli/main.py</code></li><li><code class="path-chip">packages/clawhub-skill/frontmatter.md</code></li><li><code class="path-chip">packages/openclaw/setup-entry.ts</code></li><li><code class="path-chip">packages/openclaw/tsconfig.json</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>构建跨渠道AI Agent时，团队需独立维护每个平台的SDK（认证、重连、消息格式），消耗8–15%的工程资源于通道管道，而非提升智能。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用分级架构：adapter层（packages/adapters）实现ChannelProvider协议（<code class="code-ref">packages/adapters/src/caspian_adapters/base.py:44</code>），每个通道提供provision/send/reply/parse_webhook方法；SDK客户端（CommClient）通过HTTP与托管网关通信，网关路由消息到对应连接；CLI（<code class="code-ref">apps/cli/src/caspian_cli/main.py</code>）提供初始化和连接管理；OpenClaw插件（<code class="code-ref">packages/openclaw/src/bridge.ts</code>）复用TypeScript SDK将消息泵入Agent运行时。</p>
<p class="audit-callout audit-callout--highlight">适配器接口（base.py）明确定义了Capability枚举，网关可根据能力声明精确路由，避免静默失败，如Telegram适配器（<code class="code-ref">packages/adapters/src/caspian_adapters/telegram.py:143</code>）声明{ATTACHMENTS, EDIT_INBOUND, GROUP_VISIBILITY}等能力。</p>
<p class="audit-callout audit-callout--highlight">测试覆盖真实通道协议：Slack测试（<code class="code-ref">packages/adapters/tests/test_slack.py:45</code>）验证签名验证与过期时间戳拒绝，Discord测试（<code class="code-ref">packages/adapters/tests/test_discord.py:22</code>）验证附件与路由模式，保证适配层健壮性。</p>
<p class="audit-callout audit-callout--doubt">核心SDK客户端源码缺失（<code class="code-ref">sdks/python/src/caspian_sdk/client.py</code>、<code class="code-ref">sdks/typescript/src/client.ts</code>未提供），无法审阅消息循环、重试、错误传播等关键逻辑；当前仅见桥接层（<code class="code-ref">packages/openclaw/src/bridge.ts:56</code>）调用CommClient.onMessage，内部实现完全黑盒。</p>
<p class="audit-callout audit-callout--doubt">托管网关是系统中枢，但其实现（API路由、连接池、事件落盘）不在本仓库内；自托管部署时需额外实现该服务，而仓库仅含适配器和SDK客户端，文档未说明缺失部分。</p>
<p>若用于原型验证可直接使用Free通道；若计划生产部署需先行审计SDK客户端和网关代码，或基于适配器自行实现轻量网关。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心SDK客户端源码未公开，其可靠性、性能和错误处理均未知。</li><li>仓库仅提供适配器与CLI，托管网关为闭源服务；自托管时需额外开发网关，否则只能绑定官方服务。</li><li>项目仅4天历史，单维护者，大量通道实现尚未经长期使用检验。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为Agent框架（LangChain、CrewAI等）提供了开箱即用的多通道通信层，降低初始集成成本；但长期依赖单一开发者维护的托管服务，商业化需解决自托管完整性和社区信任。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.8</span>
  </div>
</div>
</section>