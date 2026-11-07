---
title: '[Score: 75.4] StormSkinkGrip/game-ping-multipath-router'
date: '2026-11-07T09:35:49Z'
categories:
- Game Network Routing
tags:
- rust
- udp
- multipath
- wintun
- tauri
- packet-loss
intel_score: 75.4
repo_name: StormSkinkGrip/game-ping-multipath-router
repo_link: https://github.com/StormSkinkGrip/game-ping-multipath-router
summary: 为 Windows 游戏玩家提供 UDP 多路径竞速与双发去重，用免费中继替代付费加速器，仅分流游戏进程。
code_source: git
code_files_reviewed:
- crates/shortcut-core/Cargo.toml
- Cargo.toml
- crates/shortcut-relay/Cargo.toml
- .github/workflows/ci.yml
- crates/shortcut-relay/src/main.rs
- crates/shortcut-core/src/lib.rs
- .github/ISSUE_TEMPLATE/config.yml
- CONTRIBUTORS.md
- .github/ISSUE_TEMPLATE/feature_request.md
- .github/ISSUE_TEMPLATE/bug_report.md
- CONTRIBUTING.md
- SECURITY.md
- .github/settings.yml
- CHANGELOG.md
- games.toml
- relay/cloud-init.yaml
- relays.toml
- README.md
- app/ui/app.js
code_chars_analyzed: 86377
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
      <span class="scope-stat__value">19 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 86,377 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/shortcut-core/Cargo.toml</code></li><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">crates/shortcut-relay/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">crates/shortcut-relay/src/main.rs</code></li><li><code class="path-chip">crates/shortcut-core/src/lib.rs</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">CONTRIBUTORS.md</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/feature_request.md</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/bug_report.md</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">SECURITY.md</code></li><li><code class="path-chip">.github/settings.yml</code></li><li><code class="path-chip">CHANGELOG.md</code></li><li class="path-more">另有 5 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>付费加速器按订阅收费，ISP 默认路由并非最低延迟，丢包会直接变成游戏 lag spike；玩家需要只让游戏流量走更快路径且不影响其他应用。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">仓库 workspace 仅含 shortcut-core 与 shortcut-relay 两个 crate（Cargo.toml），路由打分、切换、去重与中继规则集中在 <code class="code-ref">crates/shortcut-core/src/lib.rs</code>；shortcut-relay 在 <code class="code-ref">crates/shortcut-relay/src/main.rs</code> 监听 UDP 7400，按 cookie 校验、token bucket 限速和 connected UDP 单目标转发，<code class="code-ref">Relay::handle</code> 依 wire 帧类型分发。桌面端仅审阅到 <code class="code-ref">app/ui/app.js</code> 的静态 UI，未包含 Tauri/Rust 后端，因此进程分流与 Wintun 实际调用本次不覆盖。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/shortcut-core/src/lib.rs</code> 中 <code class="code-ref">Switch::round</code> 要求 8ms 且 3 轮连续领先才切换，当前路径掉线时立即 failover；<code class="code-ref">Dedup::accept</code> 使用 1024 窗口且处理序号回绕，配套测试覆盖双路径丢包去重。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/shortcut-relay/src/main.rs</code> 的测试验证先取 cookie 再 open 才能建会话，并拒绝内网/DNS 等目标；<code class="code-ref">Session::charge</code> 在 core 中按 HEADER_BYTES 计费，限制 UDP 反射放大风险。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 app/ 的 Rust 后端源码，无法确认它如何挂钩 Wintun、按进程过滤 UDP、验签 relays.toml，README 声称的 20 游戏识别与自建向导不在 bundle。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">relay/cloud-init.yaml</code> 仍 checkout 分支 1.3.9，而当前版本 1.4.1；且 relays.toml 中继电器地址落在 203.0.113/198.51.100/192.0.2 文档保留网段，可能为示例值。</p>
<p>补齐桌面端源码审阅与集成测试，验证真实路由与反作弊隔离；将 cloud-init 分支与版本对齐，使 relays.toml 支持可验证签名；为核心/中继发布独立 binaries 并在多平台 CI 上做 e2e 测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>未审阅 app/ Rust 后端，Wintun 与反作弊隔离未证实</li><li>社区中继列表 IP 属文档保留段，需核实真实性</li><li>单维护者且 3 天仅 1 次 commit，长期维护风险高</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>以零成本自建/社区中继替代付费游戏加速，适合 C 端游戏玩家；但依赖志愿者中继与 Oracle 免费层，规模化上限较低。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">73</div>
  <div class="score-bar"><span style="width:73%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.4</span>
  </div>
</div>
</section>