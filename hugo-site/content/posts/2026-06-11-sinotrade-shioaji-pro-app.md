---
title: '[Score: 76.9] Sinotrade/shioaji-pro-app'
date: '2026-06-11T10:19:15Z'
categories:
- Trading Terminal
tags:
- TypeScript
- React
- Tauri
- SSE
- Taiwan Markets
- Trading UI
intel_score: 76.9
repo_name: Sinotrade/shioaji-pro-app
repo_link: https://github.com/Sinotrade/shioaji-pro-app
summary: 基于 Shioaji HTTP API 的台股专业交易终端前端，React 19 + Tauri 桌面版，适合需要本地化闪单与自定义版面的台湾活跃交易者。
code_source: git
code_files_reviewed:
- src-tauri/Cargo.toml
- package.json
- .github/workflows/release.yml
- src-tauri/src/main.rs
- src-tauri/src/lib.rs
- src/vite-env.d.ts
- src/main.tsx
- src/App.css.ts
- src/grid.css.ts
- src/theme.css.ts
- src/App.tsx
- src/lib/runtime.ts
- src/components/depth-map.css.ts
- src/components/tick-tape.css.ts
- src/hooks/use-stream.ts
- src/hooks/use-poll.ts
- src/components/pnl-panel.css.ts
- src/lib/api.ts
- src/lib/price-sync.ts
- src/components/event-toasts.css.ts
- src/components/command-palette.css.ts
- src/components/replay-panel.css.ts
- src/components/scanner-panel.css.ts
- src/components/vol-profile.css.ts
- src/lib/sounds.ts
- src/components/quote-board.css.ts
- src/components/panel-chrome.css.ts
- src/components/panel.css.ts
- src/hooks/use-hotkeys.ts
- src/components/market-bar.tsx
- src/components/option-chain.css.ts
- src/components/command-palette.tsx
- src/lib/indicators.ts
- src/components/depth-ladder.css.ts
- src/lib/contracts-cache.ts
- src/lib/risk.ts
- src/components/watchlist.css.ts
- src/components/event-toasts.tsx
- src/lib/trade.ts
- src/components/panel-chrome.tsx
- src/components/quote-board.tsx
- src/components/scanner-panel.tsx
- src/components/depth-ladder.tsx
- src/lib/theme-store.ts
- src/components/watchlist.tsx
- src/components/chips-card.tsx
- src/components/bottom-dock.css.ts
- src/lib/bracket.ts
code_chars_analyzed: 122878
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
      <span class="scope-stat__value">约 122,878 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">src-tauri/Cargo.toml</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src-tauri/src/main.rs</code></li><li><code class="path-chip">src-tauri/src/lib.rs</code></li><li><code class="path-chip">src/vite-env.d.ts</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src/App.css.ts</code></li><li><code class="path-chip">src/grid.css.ts</code></li><li><code class="path-chip">src/theme.css.ts</code></li><li><code class="path-chip">src/App.tsx</code></li><li><code class="path-chip">src/lib/runtime.ts</code></li><li><code class="path-chip">src/components/depth-map.css.ts</code></li><li><code class="path-chip">src/components/tick-tape.css.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>台湾短线交易者在券商原生 App 中无法自由拼接面板、拖曳改价、图表点价下单，且缺少客户端风控 Kill Switch 与一键全删单等操作，导致盘中执行效率低、误操作风险高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用采用 React 19 SPA + Tauri 2 桌面包裹的双层架构。前端零后端代码，全部通过 Shioaji HTTP API 与本地 <code class="code-ref">shioaji server</code> 通信。数据层分三条通道：SSE 单连接流式行情（<code class="code-ref">src/hooks/use-stream.ts</code> 通过 <code class="code-ref">useSyncExternalStore</code> 绑定到 <code class="code-ref">src/lib/stream</code> 的 quote store）、REST 轮询持仓/委托/账户余额（<code class="code-ref">src/hooks/use-poll.ts</code> 的 <code class="code-ref">setInterval</code> 拉取器，<code class="code-ref">src/App.tsx</code> 以 8-60 秒间隔拉取 positions/trades/balance/margin）、以及下单/撤单的一次性 POST（<code class="code-ref">src/lib/trade.ts:placeQuickOrder</code> 调用 <code class="code-ref">src/lib/shioaji</code> 的 <code class="code-ref">placeStockOrder</code>/<code class="code-ref">placeFuturesOrder</code>）。版面系统用 react-grid-layout + localStorage 持久化 workspace/profiles（<code class="code-ref">src/lib/workspace</code>），每个面板可「连动自选」或「锁定商品」（<code class="code-ref">src/App.tsx:useBlockContract</code>），并支持弹出为 Tauri 原生窗口（<code class="code-ref">POPOUT_TYPES</code> 集合 + <code class="code-ref">openPopout</code>）。Tauri 层（<code class="code-ref">src-tauri/src/lib.rs</code>）实现系统托盘菜单、关闭隐藏至托盘、单实例聚焦、sidecar 进程管理及自动更新（<code class="code-ref">tauri-plugin-updater</code>）。CI 发布流程见 <code class="code-ref">.github/workflows/release.yml</code>，推 <code class="code-ref">v*</code> tag 自动构建 macOS/Windows/Linux 四目标并上传 Release。<code class="code-ref">src/lib/risk.ts</code> 实现客户端风控 Kill Switch（单笔上限、日亏上限、手动锁单），<code class="code-ref">checkOrderAllowed</code> 在 <code class="code-ref">src/lib/trade.ts:placeQuickOrder</code> 中调用；<code class="code-ref">src/lib/bracket.ts</code> 实现括号单（成交后自动挂 OCO 停损停利触发器）。主题系统用 vanilla-extract 的 <code class="code-ref">createTheme</code> 生成 6 套主题类（3 mode × 2 涨跌色惯例），<code class="code-ref">src/lib/theme-store.ts</code> 持久化到 localStorage 并在 <code class="code-ref">&lt;html&gt;</code> 上切换 class。</p>
<p class="audit-callout audit-callout--highlight">客户端风控引擎设计扎实 — <code class="code-ref">src/lib/risk.ts:checkOrderAllowed</code> 封装了 locked/maxQty/maxDailyLoss 三层检查，所有下单路径（<code class="code-ref">src/lib/trade.ts:placeQuickOrder</code>）统一经过该关口，且 <code class="code-ref">bypassRisk</code> 参数仅用于保护性出场单（括号单），设计意图明确。</p>
<p class="audit-callout audit-callout--highlight">括号单的双通道激活检测 — <code class="code-ref">src/lib/bracket.ts</code> 同时监听 SSE order_event 的 Deal 事件（快速路径）与 4 秒轮询 trades（容错路径），<code class="code-ref">activate</code> 函数根据进場方向自动翻转 action 并挂 OCO 触发器，覆盖了 SSE 丢包场景。</p>
<p class="audit-callout audit-callout--doubt">整个仓库未见任何测试文件 — <code class="code-ref">code_bundle</code> 中 48 个文件无一属于 <code class="code-ref">tests/</code>、<code class="code-ref">*.test.*</code>、<code class="code-ref">*.spec.*</code>，对于一个处理真实资金下单的交易终端，零测试是重大工程风险。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/lib/stream.ts</code> 与 <code class="code-ref">src/lib/shioaji.ts</code> 这两个核心数据层模块未在 code_bundle 中提供，无法审阅 SSE 重连逻辑、订阅管理、错误传播等关键实现，本次结论不覆盖这两部分的质量。</p>
<p>若计划用于正式交易，必须补充核心链路的单元/集成测试（尤其是 <code class="code-ref">checkOrderAllowed</code>、<code class="code-ref">placeQuickOrder</code>、括号单激活流程）；<code class="code-ref">src/lib/stream.ts</code> 的 SSE 重连健壮性需要单独 code review；客户端触价单仅在页面开启时监控（README 已说明），建议在 UI 中用更醒目的方式提醒用户此限制。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>客户端停损/停利为浏览器端触价单，页面关闭或电脑休眠即失效，README 未充分强调此风险。</li><li>无任何自动化测试，下单/风控逻辑全部依赖人工验证，生产环境使用风险较高。</li><li>核心 SSE 流与 REST 层代码（<code class="code-ref">stream.ts/shioaji.ts</code>）未包含在审阅范围内，数据层质量未知。</li><li>项目仓库仅一天历史、8 次 commit，尚无社区反馈验证功能完整性。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>Shioaji 是永丰金证券官方 API，该项目为其生态填补了专业级 Web/桌面交易终端空白，对台股日内交易者有直接实用价值；作为开源工具可提升 Shioaji API 的开发者采用率。</p>
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
  <div class="score-item__value">71</div>
  <div class="score-bar"><span style="width:71%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.9</span>
  </div>
</div>
</section>