---
title: '[Score: 76.6] AprilNEA/OpenLogi'
date: '2026-05-30T16:03:03Z'
categories:
- Hardware Companion App
tags:
- Rust
- HID++
- Logitech
- GPUI
- macOS
- local-first
intel_score: 76.6
repo_name: AprilNEA/OpenLogi
repo_link: https://github.com/AprilNEA/OpenLogi
summary: 用 Rust 原生实现的 Logitech HID++ 鼠标本地配置工具，支持按钮重映射、DPI、SmartShift，替代 Options+ 且无需账号或遥测，macOS
  已可用。
code_source: git
code_files_reviewed:
- crates/openlogi-hid/Cargo.toml
- crates/openlogi-assets/Cargo.toml
- crates/openlogi-core/Cargo.toml
- crates/openlogi-cli/Cargo.toml
- crates/openlogi-hook/Cargo.toml
- crates/openlogi-gui/Cargo.toml
- .github/workflows/pullfrog.yml
- .github/workflows/ci.yml
- .github/workflows/release-plz.yml
- .github/workflows/release.yml
- crates/openlogi-gui/src/platform/mod.rs
- src/main.rs
- crates/openlogi-gui/src/data/mod.rs
- crates/openlogi-gui/src/watchers/mod.rs
- crates/openlogi-gui/src/components/mod.rs
- crates/openlogi-gui/src/mouse_model/mod.rs
- crates/openlogi-core/src/lib.rs
- crates/openlogi-cli/src/cmd/assets/mod.rs
- crates/openlogi-cli/src/cmd/mod.rs
- crates/openlogi-hook/src/tests.rs
- crates/openlogi-assets/src/metadata.rs
- crates/openlogi-assets/src/index.rs
- crates/openlogi-hid/src/transport.rs
- crates/openlogi-hid/src/adjustable_dpi.rs
- crates/openlogi-core/src/paths.rs
- crates/openlogi-gui/src/theme.rs
- crates/openlogi-gui/src/app_menu.rs
- crates/openlogi-assets/src/manifest.rs
- crates/openlogi-core/src/device.rs
- crates/openlogi-gui/src/hardware.rs
- crates/openlogi-hid/src/smartshift.rs
- crates/openlogi-gui/src/hook_runtime.rs
- crates/openlogi-assets/src/http.rs
- crates/openlogi-gui/src/i18n.rs
- crates/openlogi-hid/src/thumbwheel.rs
- crates/openlogi-gui/src/app.rs
- crates/openlogi-hid/src/reprog_controls.rs
- crates/openlogi-hid/src/write.rs
- crates/openlogi-hook/src/macos.rs
- crates/openlogi-hid/src/inventory.rs
- crates/openlogi-gui/locales/app.yml
- crates/openlogi-hid/src/gesture.rs
- crates/openlogi-gui/src/state.rs
- crates/openlogi-core/src/config.rs
- crates/openlogi-hid/src/pairing.rs
- crates/openlogi-gui/src/watchers/accessibility.rs
- crates/openlogi-gui/src/state/bindings.rs
- crates/openlogi-gui/src/state/dpi.rs
code_chars_analyzed: 251968
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
      <span class="scope-stat__value">约 251,968 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/openlogi-hid/Cargo.toml</code></li><li><code class="path-chip">crates/openlogi-assets/Cargo.toml</code></li><li><code class="path-chip">crates/openlogi-core/Cargo.toml</code></li><li><code class="path-chip">crates/openlogi-cli/Cargo.toml</code></li><li><code class="path-chip">crates/openlogi-hook/Cargo.toml</code></li><li><code class="path-chip">crates/openlogi-gui/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/pullfrog.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release-plz.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">crates/openlogi-gui/src/platform/mod.rs</code></li><li><code class="path-chip">src/main.rs</code></li><li><code class="path-chip">crates/openlogi-gui/src/data/mod.rs</code></li><li><code class="path-chip">crates/openlogi-gui/src/watchers/mod.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Logitech Options+ 要求登录账号、采集遥测、安装重量级 Electron 应用才能做基本的 DPI/按钮/SmartShift 配置；大量注重隐私的开发者和 MX Master 用户为此支付了不必要的隐私和系统资源成本。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 Rust workspace 分层设计，核心无 I/O 类型在 <code class="code-ref">crates/openlogi-core/src/lib.rs</code>，HID 通信封装在 <code class="code-ref">crates/openlogi-hid/src/transport.rs</code>，OS 事件拦截在 <code class="code-ref">crates/openlogi-hook/src/macos.rs</code>，GPUI 桌面界面在 <code class="code-ref">crates/openlogi-gui/src/app.rs</code>。主链路为：HID++ 设备枚举 → <code class="code-ref">open_hidpp_channel</code> 建立异步通道 → Feature 注册（AdjustableDpi <code class="code-ref">0x2201</code>、SmartShift <code class="code-ref">0x2111</code>、ReprogControlsV4 <code class="code-ref">0x1b04</code>、Thumbwheel <code class="code-ref">0x2150</code>）→ 读写设备状态。GUI 侧通过 GPUI 线程与 <code class="code-ref">AppState</code> 全局状态协调，OS hook（CGEventTap）通过 <code class="code-ref">Arc&lt;RwLock&lt;BTreeMap&gt;&gt;</code> 共享绑定映射实现跨线程无锁分发（<code class="code-ref">crates/openlogi-gui/src/hook_runtime.rs</code>）。配置持久化使用 TOML 原子写入（<code class="code-ref">crates/openlogi-core/src/config.rs:write_atomic</code>），支持 per-device 和 per-app 覆盖层。手势捕获通过 HID++ 控制转移（divert）实现，<code class="code-ref">crates/openlogi-hid/src/gesture.rs</code> 管理完整生命周期——开启 divert、监听事件、恢复默认映射。设备配对功能已实现 Bolt + Unifying 双协议（<code class="code-ref">crates/openlogi-hid/src/pairing.rs</code>），从 HID++ 1.0 寄存器直接驱动。CI 配置（<code class="code-ref">.github/workflows/ci.yml</code>）覆盖 fmt、clippy、多平台 check/test，release 流水线包含 macOS 签名、公证和 Homebrew tap 自动发布。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/openlogi-hid/src/smartshift.rs</code> 针对 0x2111 Enhanced 变体正确处理了与 0x2110 的函数 ID 偏移差异（function 1/2 vs 0/1），注释明确指出错用会导致设备静默忽略写入，说明作者实际逆向验证了协议行为。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/openlogi-hid/src/inventory.rs</code> 的 <code class="code-ref">probe_direct</code> 函数（行约 105）通过 battery presence 区分蓝牙直连外设与 Bolt 接收器的 0xff 副接口，防止同一个物理设备在设备列表中出现两次——这是一个非显而易见的边界条件。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">crates/openlogi-hook/src/macos.rs:thread_main</code> 中 CGEventTap 的 Accessibility 权限轮询间隔为 500ms（<code class="code-ref">run_in_mode</code> Duration），但 <code class="code-ref">thread_main</code> 的注释警告权限撤销会楔住整个系统输入流。虽然有退出保护，但 500ms 窗口内仍存在竞态——在高负载下 macOS 可能未及时调度该线程，导致短暂输入冻结。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">crates/openlogi-hid/src/write.rs</code> 的 <code class="code-ref">with_device</code> 每次调用都完整枚举 HID 设备再逐个 probe 接收器，而 <code class="code-ref">hardware.rs</code> 的 DPI/SmartShift 写入走的是独立 tokio runtime + OS 线程。<code class="code-ref">SharedChannel</code> 复用机制虽然存在（<code class="code-ref">crates/openlogi-hid/src/write.rs:SharedChannel</code>），但仅在 gesture capture session 存活期间可用；capture 断开后，slider 松手的 DPI 写入仍走完整枚举路径，预期延迟 100ms+。这在高频调参场景下体验会明显下降。</p>
<p>该项目目前仅 macOS 可用，Linux/Windows 均为 stub。对 macOS 上的 MX Master 用户而言已经可以直接替代 Options+ 的核心功能（DPI、按钮、SmartShift）。建议优先验证固件兼容性矩阵——README 提到某些设备使用 <code class="code-ref">0x2202 ExtendedAdjustableDpi</code> 而非 <code class="code-ref">0x2201</code>，<code class="code-ref">write.rs</code> 的 <code class="code-ref">dump_features</code> 已支持诊断但写入路径尚未适配。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅 macOS 可用；Linux/Windows 均为 Unsupported stub，跨平台用户无法迁移</li><li>使用 Zed 的 GPUI 框架（git-only 依赖），GPUI 无 crates.io 版本，构建稳定性受上游 API 变动影响</li><li>Fork/Star 比仅 1.77% 且项目仅 6 天历史、4 个 fork，社区贡献基础薄弱</li><li>assets.openlogi.org 外部资产主机的可用性和持久性未在代码中做降级处理，主机宕机时 GUI 渲染会缺失设备图</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>填补了 Logitech 生态中隐私优先的开源替代空白，对 MX Master/Anywhere 系列用户有明确价值；若扩展到 Linux/Windows 可覆盖更广的开发者桌面场景。作为 crates.io 发布的 Rust 库（openlogi-hid/openlogi-core）也可能被其他硬件工具集成。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.6</span>
  </div>
</div>
</section>