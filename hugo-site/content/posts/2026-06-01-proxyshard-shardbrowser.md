---
title: '[Score: 75.1] ProxyShard/ShardBrowser'
date: '2026-06-01T03:45:20Z'
categories:
- Anti-Detect Browser Launcher
tags:
- anti-detect-browser
- chromium
- fingerprint-spoofing
- tauri
- mcp-server
- scraping
intel_score: 75.1
repo_name: ProxyShard/ShardBrowser
repo_link: https://github.com/ProxyShard/ShardBrowser
summary: Tauri 桌面启动器 + Node/Python SDK，管理 170+ 设备指纹配置文件并驱动修补版 Chromium 引擎执行 WebGL/TLS/Client
  Hints 等引擎级欺骗，面向多账号运营和反检测爬虫场景。
code_source: git
code_files_reviewed:
- mcp/package.json
- package.json
- sdks/node/package.json
- sdks/python/pyproject.toml
- src-tauri/Cargo.toml
- .github/workflows/release.yml
- src-tauri/src/main.rs
- sdks/node/src/index.ts
- sdks/python/shardx/__init__.py
- src-tauri/src/lib.rs
- mcp/index.js
- src/vite-env.d.ts
- src/main.tsx
- src-tauri/build.rs
- tsconfig.node.json
- src-tauri/gen/schemas/capabilities.json
- sdks/node/tsconfig.json
- src-tauri/capabilities/default.json
- tsconfig.json
- src-tauri/tauri.conf.json
- vite.config.ts
- src-tauri/src/store.rs
- src-tauri/src/mcp_setup.rs
- src-tauri/src/settings.rs
- sdks/node/src/screen.ts
- sdks/python/shardx/profile.py
- sdks/node/src/profile.ts
- sdks/python/shardx/screen.py
- sdks/python/shardx/geo.py
- sdks/node/src/host.ts
- sdks/python/shardx/randomize.py
- sdks/python/shardx/host.py
- src-tauri/src/process.rs
- sdks/node/src/randomize.ts
- mcp/README.md
- sdks/node/src/geo.ts
- src-tauri/src/fingerprints.rs
- sdks/node/package-lock.json
- sdks/python/shardx/proxy.py
- sdks/node/src/autoResolve.ts
- sdks/python/shardx/auto_resolve.py
- sdks/node/src/browser.ts
- sdks/python/README.md
- sdks/node/src/proxy.ts
- sdks/python/shardx/browser.py
- sdks/node/README.md
- sdks/node/src/runtime.ts
- src-tauri/src/profile.rs
code_chars_analyzed: 257617
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
      <span class="scope-stat__value">约 257,617 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">mcp/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">sdks/node/package.json</code></li><li><code class="path-chip">sdks/python/pyproject.toml</code></li><li><code class="path-chip">src-tauri/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src-tauri/src/main.rs</code></li><li><code class="path-chip">sdks/node/src/index.ts</code></li><li><code class="path-chip">sdks/python/shardx/__init__.py</code></li><li><code class="path-chip">src-tauri/src/lib.rs</code></li><li><code class="path-chip">mcp/index.js</code></li><li><code class="path-chip">src/vite-env.d.ts</code></li><li><code class="path-chip">src/main.tsx</code></li><li><code class="path-chip">src-tauri/build.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>多账号运营者和爬虫开发者在日常工作中面临反检测浏览器（Multilogin/GoLogin 等）按 profile 数量收费且指纹欺骗停留在 JS 注入层、容易被 Cloudflare/Akamai 等检测引擎识破的问题；需要一套能在引擎 C++ 层做一致性欺骗、且能被脚本/AI Agent 自动化驱动的免费方案。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目由四层组成——Tauri 桌面 UI（<code class="code-ref">src-tauri/src/lib.rs</code>）、本地 HTTP 自动化 API（axum，<code class="code-ref">lib.rs:567</code> 附近 <code class="code-ref">api::serve</code>）、MCP Server（<code class="code-ref">mcp/index.js</code>）、以及 Node/Python SDK（<code class="code-ref">sdks/node/src/</code>、<code class="code-ref">sdks/python/shardx/</code>）。所有入口共享同一套指纹库（<code class="code-ref">src-tauri/src/fingerprints.rs</code>）和 profile 存储（<code class="code-ref">src-tauri/src/profile.rs</code>）。启动 profile 时，SDK 的 <code class="code-ref">Browser.launch</code> 依次执行 auto-resolve（地理/语言/时区从代理 IP 实时解析）、screen strategy（macOS 按比例缩放、Win/Linux 替换为主机显示器）、SOCKS5 UDP_ASSOCIATE STUN 探测决定 QUIC/WebRTC 策略，最后写 fingerprint.json 并 spawn 修补版 Chromium。亮点1：Node SDK 的 <code class="code-ref">probeUdp</code>（<code class="code-ref">sdks/node/src/proxy.ts:47-145</code>）实现了完整的 SOCKS5 握手→UDP_ASSOCIATE→STUN Binding Request 往返，用三个公开 STUN 服务器做容错，能在启动前精确判断代理是否支持 UDP relay，从而自动决定 <code class="code-ref">--enable-quic</code> / <code class="code-ref">--disable-quic</code> 和 WebRTC 策略——这个探测逻辑在同类工具中少见。亮点2：硬件随机化算法（<code class="code-ref">src-tauri/src/lib.rs:218-280</code> 和 <code class="code-ref">sdks/node/src/randomize.ts</code>）对 macOS 使用按型号查表的 <code class="code-ref">MAC_HW_CONFIGS</code>，Win/Linux 则在真实主机核心数 ±4 范围内从真实 x86 核心数集合采样，同时 <code class="code-ref">device_memory</code> 受真实 RAM 桶限制——避免了 8 核笔记本伪装 64 核的明显矛盾。疑点1：闭源引擎是核心竞争力所在，但源码中未包含任何 Chromium 补丁代码，所有「引擎级欺骗」声明无法从本仓库验证；<code class="code-ref">sdks/python/README.md</code> 最后一行也坦承引擎是闭源产品。疑点2：整个项目无任何测试文件（无 <code class="code-ref">tests/</code> 目录、无 <code class="code-ref">*_test.*</code> 文件），核心逻辑如 <code class="code-ref">probeUdp</code> 的 STUN 响应解析、<code class="code-ref">randomize_hardware</code> 的边界条件、<code class="code-ref">resolve_auto_fields</code> 的 fallback 链均无单元测试覆盖，<code class="code-ref">release.yml</code> 也只有构建无 CI 测试步骤。落地建议：适合对反检测有明确需求的开发者试用 SDK；若要生产级使用，需自行审计闭源引擎的欺骗深度，并为 SDK 的关键路径补充集成测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心欺骗在闭源 Chromium 补丁中，本仓库无法验证欺骗深度和持久性</li><li>项目仅 1 天历史（2026-05-30 创建）且零测试，API 和指纹格式可能快速破坏性变更</li><li>SDK 从 Cloudflare R2 CDN 下载 ~170MB 引擎二进制，无签名校验机制，供应链风险显著</li><li>README 声称 Chromium 148 但该版本号截至审查时尚未在 Chromium 官方发布，实际引擎来源不透明</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 ProxyShard 代理服务的配套客户端，免费 SDK 降低了新用户的试用门槛，170+ 预置指纹 + MCP 接入使其成为 AI Agent 做自动化浏览的可行候选；但引擎闭源意味着核心价值无法被社区 fork 或审计，长期信任依赖 ProxyShard 团队持续维护。</p>
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
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.1</span>
  </div>
</div>
</section>