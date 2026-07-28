---
title: '[Score: 77.0] ChrisMack32/Locus'
date: '2026-07-28T22:01:56Z'
categories:
- iOS Location Spoofing
tags:
- Swift
- idevice
- location-spoofing
- iOS
- MapKit
- SideLoad
intel_score: 77.0
repo_name: ChrisMack32/Locus
repo_link: https://github.com/ChrisMack32/Locus
summary: Locus 是一款利用 Apple 开发者位置模拟接口，实现 iOS 系统级位置伪造的开源工具，无需电脑配合，适合测试与隐私场景。
code_source: git
code_files_reviewed:
- Locus/Resources/Assets.xcassets/Contents.json
- Locus/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json
- Locus/Resources/Assets.xcassets/AccentColor.colorset/Contents.json
- Locus/Resources/Assets.xcassets/LaunchBackground.colorset/Contents.json
- Locus/Engine/DeviceTunnel.swift
- Locus/Support/SavedPlace.swift
- Locus/Engine/BackgroundKeepAlive.swift
- AppIcon.icon/icon.json
- Locus/Support/PairingDocumentPicker.swift
- Locus/App/LocusApp.swift
- SETUP.md
- Locus/Features/Joystick/JoystickPad.swift
- project.yml
- Locus/Support/Theme.swift
- Locus/Support/LocalDevVPN.swift
- Locus/Engine/SilentAudioKeepAlive.swift
- Locus/Features/Map/MapDropPin.swift
- Locus/Features/Routes/RoutePlannerSheet.swift
- README.md
- Locus/Engine/PairingStore.swift
- Locus/Features/Settings/LocusEasterEggView.swift
- Locus/Engine/RouteBuilder.swift
- Locus/Engine/PairableHostAdvertiser.swift
- Locus/Engine/LocationEngine.swift
- Locus/Features/Settings/PairOnDeviceView.swift
- Locus/Features/Map/RootView.swift
- Locus/Engine/PairOnDeviceService.swift
- Locus/Features/Settings/SettingsView.swift
- Locus/Engine/SpoofSession.swift
- Locus/Features/Setup/SetupFlowView.swift
- Locus/Features/Map/MapHomeView.swift
code_chars_analyzed: 148109
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
      <span class="scope-stat__value">31 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 148,109 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Locus/Resources/Assets.xcassets/Contents.json</code></li><li><code class="path-chip">Locus/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json</code></li><li><code class="path-chip">Locus/Resources/Assets.xcassets/AccentColor.colorset/Contents.json</code></li><li><code class="path-chip">Locus/Resources/Assets.xcassets/LaunchBackground.colorset/Contents.json</code></li><li><code class="path-chip">Locus/Engine/DeviceTunnel.swift</code></li><li><code class="path-chip">Locus/Support/SavedPlace.swift</code></li><li><code class="path-chip">Locus/Engine/BackgroundKeepAlive.swift</code></li><li><code class="path-chip">AppIcon.icon/icon.json</code></li><li><code class="path-chip">Locus/Support/PairingDocumentPicker.swift</code></li><li><code class="path-chip">Locus/App/LocusApp.swift</code></li><li><code class="path-chip">SETUP.md</code></li><li><code class="path-chip">Locus/Features/Joystick/JoystickPad.swift</code></li><li><code class="path-chip">project.yml</code></li><li><code class="path-chip">Locus/Support/Theme.swift</code></li><li class="path-more">另有 17 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>需要在未越狱 iPhone 上修改系统定位的用户（如应用开发者、隐私敏感者），现有方案大多依赖电脑或越狱，且部分游戏反作弊机制难以绕过。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Locus 以 SwiftUI 驱动 UI（RootView.swift:1），通过 SpoofSession（Engine/SpoofSession.swift:1）管理状态，核心通过 idevice FFI 调用。
<code class="code-ref">LocationEngine.swift:1</code> 封装了 C 接口：<code class="code-ref">setLocked</code> 函数先尝试复用现有 <code class="code-ref">location_simulation</code>，否则新建隧道：解析 IP（<code class="code-ref">DeviceTunnel.swift:1</code> 的 <code class="code-ref">TunnelConfig</code>）、读取 RPPairing 文件（<code class="code-ref">PairingStore.swift:1</code>）、创建 <code class="code-ref">remote_server</code>，然后调 <code class="code-ref">location_simulation_set</code> 注入坐标。
后台保持采用双策略：<code class="code-ref">BackgroundKeepAlive.swift:1</code> 使用 <code class="code-ref">CLLocationManager</code> 持续定位，<code class="code-ref">SilentAudioKeepAlive.swift:1</code> 循环播放近乎静音的 WAV 文件以阻止 app 挂起。</p>
<p class="audit-callout audit-callout--highlight">iOS 27 上实现了无电脑配对（<code class="code-ref">PairOnDeviceService.swift:1</code>），通过 <code class="code-ref">NWListener</code> 发布 Bonjour 服务，将连接中继到 Rust 的 pairable-host，全程在子线程运行并通过回调更新 UI。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">SpoofSession.swift:1</code> 内的健康检查（<code class="code-ref">startHealth</code> 每 12 秒）和重发定时器（<code class="code-ref">startResend</code> 每 8 秒）确保位置模拟不掉线，掉线时自动重连并推送本地通知。</p>
<p class="audit-callout audit-callout--doubt">代码包中无测试文件（未提供 <code class="code-ref">Tests/</code> 目录），关键路径如 <code class="code-ref">LocationEngine.swift:1</code> 的隧道建立和错误码映射缺乏测试覆盖。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">SilentAudioKeepAlive.swift:1</code> 手动构建 WAV 数据并循环播放，音量设为 0.01，虽然 README 说明用于保持后台，但这种技巧可能在未来 iOS 版本失效或被应用审核标记。</p>
<p>增加单元测试覆盖 Engine 层，尤其是 FFI 调用和错误处理；探索更可靠的后台保活方案，或引导用户理解绑定 LocalDevVPN 的必要性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>须侧载使用，证书每 7 天需重签，对普通用户门槛极高。</li><li>游戏反作弊（如 Pokémon GO）仍能识别模拟位置，限制了最广大的潜在用户群。</li><li>summary 过长，可能含废话</li><li>technical_review 未引用任何已审阅源码路径（path 级证据缺失）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 iOS 开发者提供无需系统越狱的位置测试方案，也吸引注重隐私的普通用户，但变现空间有限，主要依靠社区捐赠或企业定制。</p>
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
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.0</span>
  </div>
</div>
</section>