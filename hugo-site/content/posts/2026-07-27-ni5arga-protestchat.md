---
title: '[Score: 75.4] ni5arga/protestchat'
date: '2026-07-27T02:38:40Z'
categories:
- Off-grid Messaging
tags:
- bluetooth-low-energy
- mesh
- encrypted-messaging
- offline-first
- censorship-resistance
intel_score: 75.4
repo_name: ni5arga/protestchat
repo_link: https://github.com/ni5arga/protestchat
summary: 一款为网络中断和蜂窝干扰场景设计的离网加密通信应用，通过蓝牙mesh实现设备间直接消息传递，无服务器、无账户，适合抗议等高风险环境。
code_source: git
code_files_reviewed:
- website/package.json
- modules/ble-mesh/android/build.gradle
- package.json
- .github/workflows/localization-audit.yml
- .github/workflows/android-preview.yml
- src/trust/index.ts
- modules/ble-mesh/index.ts
- src/app/index.tsx
- src/hooks/use-motion.ts
- src/hooks/use-theme.ts
- src/lib/contact.ts
- src/lib/crypto.ts
- src/lib/radio-access.ts
- src/trust/roots.ts
- src/i18n/provider.tsx
- src/lib/contact-code.ts
- src/lib/bytes.ts
- src/trust/DESIGN.md
- src/i18n/core.ts
- src/lib/conversation.ts
- src/app/_layout.tsx
- src/app/join-channel.tsx
- src/components/mode-notice.tsx
- src/components/message-bubble.tsx
- src/app/new-group.tsx
- src/components/radio-access-gate.tsx
- src/constants/theme.ts
- src/components/status-banner.tsx
- src/app/settings.tsx
- src/trust/README.md
- src/lib/transport.ts
- src/lib/protocol.ts
- src/trust/types.ts
- src/lib/store.ts
- src/trust/store.ts
- src/app/add.tsx
- src/lib/prekeys.ts
- src/i18n/en.ts
- src/lib/app-state.tsx
- src/components/ui.tsx
- src/i18n/mr.ts
- src/lib/crypto-core.ts
- src/i18n/bn.ts
- src/i18n/hi.ts
- src/i18n/te.ts
- src/trust/engine.ts
- src/lib/db.ts
- src/i18n/ta.ts
code_chars_analyzed: 397385
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
      <span class="scope-stat__value">约 397,385 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">website/package.json</code></li><li><code class="path-chip">modules/ble-mesh/android/build.gradle</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">.github/workflows/localization-audit.yml</code></li><li><code class="path-chip">.github/workflows/android-preview.yml</code></li><li><code class="path-chip">src/trust/index.ts</code></li><li><code class="path-chip">modules/ble-mesh/index.ts</code></li><li><code class="path-chip">src/app/index.tsx</code></li><li><code class="path-chip">src/hooks/use-motion.ts</code></li><li><code class="path-chip">src/hooks/use-theme.ts</code></li><li><code class="path-chip">src/lib/contact.ts</code></li><li><code class="path-chip">src/lib/crypto.ts</code></li><li><code class="path-chip">src/lib/radio-access.ts</code></li><li><code class="path-chip">src/trust/roots.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>在警察部署蜂窝干扰器或网络被切断时，抗议者无法使用常规即时通讯工具传递协调信息，且现有应用缺乏无网络条件下的易用加密通道。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用采用分层设计，由 TypeScript 共享核心（加密、协议、存储），通过 React Native 连接 Swift（iOS）和 Kotlin（Android）原生 BLE 传输。安全关键代码集中在 <code class="code-ref">src/lib/crypto-core.ts</code>，该文件不依赖任何 React Native 组件，可通过 <code class="code-ref">npm test</code> 在开发机上验证（见 <code class="code-ref">package.json:57</code>）。传输层抽象 <code class="code-ref">src/lib/transport.ts</code> 隔离了 BLE 细节，便于未来替换为 LoRa 等（见 <code class="code-ref">transport.ts:4-6</code>）。Mesh 引擎（<code class="code-ref">mesh.ts</code>）注入存储和传输接口，本应实现中继、去重和转发，但核心逻辑的源码未在审计包中提供。</p>
<p class="audit-callout audit-callout--highlight">加密核心实现了紧凑且经过考量的混合方案（<code class="code-ref">crypto-core.ts:176</code> 的 <code class="code-ref">seal</code> 函数），结合 XChaCha20-Poly1305、Ed25519 签名和 X25519 密钥协商，支持基于预密钥的前向安全。信道密钥派生采用对抗离线字典攻击的 scrypt（<code class="code-ref">crypto-core.ts:358</code>），并在注释中坦诚了参数权衡和迁移到 Argon2id 的计划。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/lib/store.ts</code> 定义了 <code class="code-ref">MeshStore</code> 接口并提供了精确复刻 SQL 语义的 <code class="code-ref">MemoryStore</code> 实现（<code class="code-ref">store.ts:120-200</code>），使得核心引擎的测试可以脱离设备运行，这在离线网格类项目中少见。数据库层 <code class="code-ref">db.ts</code> 包含了详尽的迁移逻辑（如 <code class="code-ref">migrateMessagesFirstSeen</code>）和基于本地时钟的保留策略（<code class="code-ref">db.ts:533-550</code>），有效防范恶意膨胀 TTL 的攻击。</p>
<p class="audit-callout audit-callout--doubt">核心 mesh 引擎 <code class="code-ref">src/lib/mesh.ts</code> 未在 code_bundle 中提供。该项目声称的流行病路由、信封中继和去重逻辑均集中在此文件，缺乏该文件意味着无法评估实际网格行为、错误处理和攻击面（如泛洪控制）。当前工程评分仅限于可见的静态分析，实际运行时风险需保留判断。</p>
<p class="audit-callout audit-callout--doubt">信任模块（<code class="code-ref">src/trust/</code>）提供了基于 Ed25519 的订阅-委派-紧急验证框架（<code class="code-ref">src/trust/engine.ts:35</code> 的 <code class="code-ref">TrustEngine</code>），但 README 和代码注释均表明该模块尚未集成到主消息流中（<code class="code-ref">src/trust/index.ts:18</code>），目前属于基础设施预留。紧急广播的验证阈值、委派链的安全属性均未在真正的网格消息路径中得到验证。</p>
<p>- 尽快开放 <code class="code-ref">mesh.ts</code> 源码评审，它是整个系统的核心调度器，缺乏它将导致对中继安全性和资源消耗的评估不完整。
- iOS 构建当前被标记为“Blocked”（README），实际部署场景中 iOS 设备占比高，建议优先解决 CoreBluetooth 的传输实现或声明放弃 iOS 支持。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>iOS 构建受阻，限制全平台覆盖；README 仅提 Android 可构建。</li><li>未经过独立安全审计，README 和设置页均有明确说明。</li><li>BLE 广告可被射频探测，即使内容加密，设备存在性仍可暴露。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>完全开源且无服务端依赖，可被任何人自由部署和修改，具有人权活动、灾害通信等垂直场景的长期价值，但无直接商业护城河。</p>
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
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">64</div>
  <div class="score-bar"><span style="width:64%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.4</span>
  </div>
</div>
</section>