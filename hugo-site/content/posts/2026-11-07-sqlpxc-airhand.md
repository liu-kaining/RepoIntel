---
title: '[Score: 79.3] sqlpxc/airhand'
date: '2026-11-07T21:25:25Z'
categories:
- Remote Desktop
tags:
- Rust
- QUIC
- Tauri
- React
- WebCodecs
intel_score: 79.3
repo_name: sqlpxc/airhand
repo_link: https://github.com/sqlpxc/airhand
summary: 基于 QUIC 的 Rust 跨平台远控，单程序兼具被控/控制端，支持 Web 控制台与硬件 AV1。
code_source: git
code_files_reviewed:
- crates/airhand-proto/Cargo.toml
- Cargo.toml
- client/package.json
- crates/airhand-link/Cargo.toml
- server/Cargo.toml
- server/Dockerfile
- client/src-tauri/src/main.rs
- crates/airhand-link/src/lib.rs
- crates/airhand-proto/src/lib.rs
- web/src/main.rs
- server/src/main.rs
- client/src-tauri/src/host/mod.rs
- client/src-tauri/src/host/encoder/mod.rs
- client/src-tauri/src/host/input/mod.rs
- crates/airhand-link/src/controller/mod.rs
- server/src/tls.rs
- server/src/codes.rs
- server/src/broker.rs
- client/tests/codec.test.ts
- client/tests/avsync.test.ts
- client/tests/i18n.test.ts
- client/tests/jitter.test.ts
- crates/airhand-proto/src/signal.rs
- crates/airhand-link/src/problem.rs
- crates/airhand-proto/src/session.rs
- crates/airhand-proto/src/framing.rs
- crates/airhand-link/src/net.rs
- crates/airhand-link/src/controller/session.rs
- client/src-tauri/tauri.macos.conf.json
- client/src-tauri/capabilities/default.json
- client/src-tauri/tauri.linux.conf.json
- client/src-tauri/build.rs
- client/src/main.tsx
- client/tsconfig.json
- client/src-tauri/examples/headless_host.rs
- client/src/components/Popover.tsx
- client/src-tauri/.cargo/config.toml
- client/vite.config.ts
- client/src/components/Logo.tsx
- client/src/lib/messages.ts
- client/src-tauri/tauri.conf.json
- client/src/components/WebUnsupported.tsx
- client/src/lib/presets.ts
- client/src-tauri/examples/encode_bench.rs
- client/src/components/GridView.tsx
- client/src/lib/backend/tauri.ts
- client/src/lib/audio-worklet.ts
- client/src/lib/i18n.ts
code_chars_analyzed: 208251
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
      <span class="scope-stat__value">约 208,251 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/airhand-proto/Cargo.toml</code></li><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">client/package.json</code></li><li><code class="path-chip">crates/airhand-link/Cargo.toml</code></li><li><code class="path-chip">server/Cargo.toml</code></li><li><code class="path-chip">server/Dockerfile</code></li><li><code class="path-chip">client/src-tauri/src/main.rs</code></li><li><code class="path-chip">crates/airhand-link/src/lib.rs</code></li><li><code class="path-chip">crates/airhand-proto/src/lib.rs</code></li><li><code class="path-chip">web/src/main.rs</code></li><li><code class="path-chip">server/src/main.rs</code></li><li><code class="path-chip">client/src-tauri/src/host/mod.rs</code></li><li><code class="path-chip">client/src-tauri/src/host/encoder/mod.rs</code></li><li><code class="path-chip">client/src-tauri/src/host/input/mod.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>系统管理员在无公网 IPv4、跨网段场景远控多台 Windows/macOS/Linux 时，常用工具需逐台装客户端且视频编码延迟高，剪贴板、音频、权限和浏览器端体验割裂。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">根工作区 Cargo.toml 将协议库 airhand-proto、链路库 airhand-link 与 server 分离；client/src-tauri 和 web 通过路径依赖共用链路，服务器不解析会话内容。控制流与会话流同走 QUIC：<code class="code-ref">crates/airhand-proto/src/lib.rs</code> 定义 13 字节 SessionHeader，<code class="code-ref">server/src/broker.rs</code> 按 conn_id + session_id 将两条双向流配对并零拷贝透传，帧层 <code class="code-ref">crates/airhand-proto/src/framing.rs</code> 用 u32 LE 长度前缀+postcard 编码并做上限限制。</p>
<p class="audit-callout audit-callout--highlight">重连与防猜码设计。<code class="code-ref">server/src/broker.rs</code> 的 resume_token 由控制码+密钥派生，带凭证请求失败一律 Offline 不透露控制码是否存在；<code class="code-ref">server/src/codes.rs</code> 用 SQLite 只存密钥哈希，绑定可跨重启保留。</p>
<p class="audit-callout audit-callout--highlight">音画/抖动有真实仿真测试。<code class="code-ref">client/tests/avsync.test.ts</code> 验证网络抖动下音画残差，<code class="code-ref">client/tests/jitter.test.ts</code> 验证缓冲断粮/快进；<code class="code-ref">client/src-tauri/src/host/encoder/mod.rs</code> 有 H264/H265/AV1 硬件到 OpenH264 回退链。</p>
<p class="audit-callout audit-callout--doubt">client/src-tauri/src/host/capture、pipeline 等屏幕采集与 Windows service 未在 code_bundle 中提供，本次结论不覆盖采集稳定性与多显示器 DPI 细节。</p>
<p class="audit-callout audit-callout--doubt">协议版本仍为 PROTOCOL_VERSION=6 且 README 声明仍在变动，未见 CI 配置，版本不兼容只能被 detect 不能自动解决。</p>
<p>先冻结协议并发布固定版本；补充缺失的 capture/pipeline 与 Windows 服务模块复审，再补跨网真实网络集成测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>协议版本仍可能变化，客户端与服务端必须同版本构建（README 与 PROTOCOL_VERSION=6）</li><li>未审阅 capture/pipeline 等路径，屏幕采集稳定性不可覆盖</li><li>Web 控制台不设 AIRHAND_WEB_PASSWORD 时公网端口无认证（<code class="code-ref">web/src/main.rs</code> 警告）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可作为企业内网或运维团队的自托管远控方案，较传统 RDP/VNC 在弱网和浏览器接入上有差异化价值；但当前无稳定版本，不宜直接用于生产。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.3</span>
  </div>
</div>
</section>