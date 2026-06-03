---
title: '[Score: 75.5] cpaczek/skylight'
date: '2026-06-03T10:53:56Z'
categories:
- Physical Computing / ADS-B Visualization
tags:
- ads-b
- canvas-rendering
- raspberry-pi
- real-time
- websockets
- typescript
intel_score: 75.5
repo_name: cpaczek/skylight
repo_link: https://github.com/cpaczek/skylight
summary: 基于RTL-SDR解码ADS-B信号、用Canvas将头顶航班实时投影到天花板的物理计算项目，附带日月星卫星天层，适合有树莓派+投影仪的航空爱好者DIY。
code_source: git
code_files_reviewed:
- server/package.json
- web/package.json
- package.json
- shared/src/index.ts
- server/src/index.ts
- server/tsconfig.json
- server/src/config-store.ts
- server/src/tle.ts
- server/src/hub.ts
- server/src/datasource.ts
- server/src/enrich/tables.ts
- server/src/enrich/airlines.json
- server/src/enrich/types.json
- server/src/enrich/routes.ts
- shared/tsconfig.json
- pnpm-workspace.yaml
- web/src/control/main.tsx
- web/src/display/main.tsx
- web/tsconfig.json
- tsconfig.base.json
- web/src/lib/useStream.ts
- web/vite.config.ts
- shared/src/messages.ts
- web/src/display/airports.ts
- scripts/install-rtlsdr-fedora.sh
- scripts/run-dump1090-local.sh
- scripts/deploy-to-pi.sh
- shared/src/aircraft.ts
- pi-setup/provision-sd.sh
- shared/src/geo.ts
- web/src/control/components.tsx
- pi-setup/setup-kiosk.sh
- web/src/lib/connection.ts
- pi-setup/README.md
- web/src/display/Display.tsx
- pi-setup/install-on-pi.sh
- web/src/display/stars.ts
- shared/src/config.ts
- web/src/display/celestial.ts
- README.md
- web/src/display/aircraftGlyph.ts
- web/src/control/Control.tsx
- web/src/display/renderer.ts
code_chars_analyzed: 146276
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
      <span class="scope-stat__value">43 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 146,276 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">server/package.json</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">shared/src/index.ts</code></li><li><code class="path-chip">server/src/index.ts</code></li><li><code class="path-chip">server/tsconfig.json</code></li><li><code class="path-chip">server/src/config-store.ts</code></li><li><code class="path-chip">server/src/tle.ts</code></li><li><code class="path-chip">server/src/hub.ts</code></li><li><code class="path-chip">server/src/datasource.ts</code></li><li><code class="path-chip">server/src/enrich/tables.ts</code></li><li><code class="path-chip">server/src/enrich/airlines.json</code></li><li><code class="path-chip">server/src/enrich/types.json</code></li><li><code class="path-chip">server/src/enrich/routes.ts</code></li><li class="path-more">另有 29 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>住在机场附近的航空爱好者想不低头看手机就能知道头顶飞过的是哪架飞机、去哪——手机App无法提供&quot;天花板即天空&quot;的沉浸感，且现有开源飞行追踪器均面向2D地图而非物理投影场景。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分三个pnpm workspace包：<code class="code-ref">shared/</code> 提供类型与纯函数，<code class="code-ref">server/</code> 做数据采集+WebSocket广播，<code class="code-ref">web/</code> 做Canvas渲染+手机控制面板。数据链路为 RTL-SDR→dump1090→<code class="code-ref">server/src/datasource.ts</code>（Poller轮询）→normalize+enrich→<code class="code-ref">server/src/hub.ts</code>（WebSocket广播）→<code class="code-ref">web/src/display/renderer.ts</code>（Canvas 60fps插值渲染）。架构分层清晰，shared层无DOM依赖，geo投影/消息类型在服务端和客户端共用。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">server/src/datasource.ts:146-166</code> 的 <code class="code-ref">mergeSources</code> 实现了radio优先、API补充的双源合并策略，radio修复点被人为减去2秒seen值以保证本地信号优先，设计考虑了降落后ADS-B信号消失的场景。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">web/src/display/renderer.ts:28-36</code> 的运动模型采用&quot;渲染延迟1150ms&quot;策略，将实时渲染回退到过去、在两个已知fix之间做线性插值而非向前外推，消除了1Hz数据刷新率导致的画面跳变，是工程上优雅的取舍。</p>
<p class="audit-callout audit-callout--doubt">整个仓库**零测试文件**——code_bundle中没有任何<code class="code-ref">*.test.*</code>、<code class="code-ref">*.spec.*</code>、<code class="code-ref">tests/</code>目录、<code class="code-ref">playwright.config.*</code>，尽管<code class="code-ref">package.json</code>声明了playwright依赖。<code class="code-ref">server/src/enrich/routes.ts</code>的缓存刷新逻辑、<code class="code-ref">renderer.ts</code>的插值/投影/标签碰撞检测均无任何自动化验证，对一个有物理部署（Pi 5 +投影仪）的项目来说风险不小。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">server/src/datasource.ts:77-80</code> 的 <code class="code-ref">fetchJson</code> 对所有HTTP错误仅抛出 <code class="code-ref">HTTP ${status}</code>，<code class="code-ref">server/src/index.ts:89</code> 的 <code class="code-ref">main()</code> 顶层用 <code class="code-ref">.catch</code> 打日志后直接 <code class="code-ref">process.exit(1)</code>，但Poller内部的<code class="code-ref">tick</code>（第161行）catch后仅返回null，没有任何重试退避或告警指标。如果airplanes.live API限流或dump1090崩溃，服务端会静默标记<code class="code-ref">ok:false</code>但不主动告警。</p>
<p>增加至少一层集成测试验证Poller→Hub→Connection的消息流转；对<code class="code-ref">RouteEnricher</code>的adsbdb缓存加negative-cache过期逻辑（当前null永久缓存直到ttl过期）；为Pi部署增加systemd watchdog或healthcheck端点轮询。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>零自动化测试，Pi上部署后无法通过CI验证任何回归</li><li>adsbdb.com免费API无SLA保证，限流或停服后航线丰富度直接归零</li><li>airport.ts硬编码SFO跑道坐标，换机场需手动编辑源码</li><li>server无认证/鉴权，LAN内任何人可通过/api/config或WS修改配置</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>项目README已挂出众筹等待页（skylightceiling.com），说明作者有商业化意图。作为开源硬件+软件套件，其商业价值在于卖预制kit而非卖软件——软件本身是引流手段。对投影仪/航空周边爱好者社区有一定吸引力，但市场极度小众。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.5</span>
  </div>
</div>
</section>