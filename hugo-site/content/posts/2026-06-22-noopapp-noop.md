---
title: '[Score: 80.25] NoopApp/noop'
date: '2026-06-22T03:57:16Z'
categories:
- BLE Health Device Companion
tags:
- Swift
- Kotlin
- Bluetooth
- WHOOP
- Local-first
- Multi-platform
intel_score: 80.25
repo_name: NoopApp/noop
repo_link: https://github.com/NoopApp/noop
summary: 离线 WHOOP 替代客户端，通过 BLE 直连表带、所有数据存本地，覆盖 iOS/Android/Mac 三平台，面向不想付 WHOOP 订阅费的健身用户。
code_source: git
code_files_reviewed:
- tools/linux-capture/requirements.txt
- android/build.gradle.kts
- android/app/build.gradle.kts
- .github/workflows/android.yml
- .github/workflows/swift-packages.yml
- .github/workflows/app-build.yml
- Packages/StrandDesign/Package.swift
- Packages/StrandAnalytics/Package.swift
- Packages/WhoopProtocol/Package.swift
- Packages/WhoopStore/Package.swift
- Packages/NoopLocalAccess/Package.swift
- Packages/StrandImport/Package.swift
- Packages/StrandImport/Tests/StrandImportTests/PlaceholderTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/SmokeTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/Resources/historical_golden.json
- Packages/WhoopStore/Tests/WhoopStoreTests/ScaffoldTests.swift
- android/app/src/test/java/com/noop/ble/WhoopModelFallbackTest.kt
- android/app/src/test/java/com/noop/notif/IllnessAlertPolicyTest.kt
- android/app/src/test/java/com/noop/notif/CallAlertPolicyTest.kt
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/VersionCheckTests.swift
- Packages/StrandImport/Sources/StrandImport/StrandImport.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/WhoopProtocol.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/StrandAnalytics.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/DayOwnerResolver.swift
- Packages/WhoopStore/Sources/WhoopStore/StandardHRMapping.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/VersionCheck.swift
- Packages/WhoopStore/Sources/WhoopStore/Cursors.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Values.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/HistoricalMeta.swift
- Packages/StrandDesign/Sources/StrandDesign/SportIcon.swift
- Packages/StrandDesign/Sources/StrandDesign/Haptics.swift
- Packages/NoopLocalAccess/Sources/NoopLocalAccessCore/JSONValue.swift
- Packages/NoopLocalAccess/Sources/noop-local-access/main.swift
- Packages/StrandDesign/Sources/StrandDesign/StrandDesign.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/HapticClockEncoder.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/HapticPayloads.swift
- Packages/WhoopStore/Sources/WhoopStore/PairedDevice.swift
- Packages/StrandDesign/Sources/StrandDesign/GlowRing.swift
- Packages/StrandDesign/Sources/StrandDesign/Motion.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/ManualWorkoutRescore.swift
- Packages/StrandImport/Sources/StrandImport/LabMarker.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/PuffinCapture.swift
- Packages/WhoopStore/Sources/WhoopStore/MetricSeriesStore.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/SleepWindowReclip.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/DoseResponsePriors.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/BreathPacer.swift
- Packages/StrandDesign/Sources/StrandDesign/StatePill.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/DeviceFamily.swift
code_chars_analyzed: 104919
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
      <span class="scope-stat__value">约 104,919 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">tools/linux-capture/requirements.txt</code></li><li><code class="path-chip">android/build.gradle.kts</code></li><li><code class="path-chip">android/app/build.gradle.kts</code></li><li><code class="path-chip">.github/workflows/android.yml</code></li><li><code class="path-chip">.github/workflows/swift-packages.yml</code></li><li><code class="path-chip">.github/workflows/app-build.yml</code></li><li><code class="path-chip">Packages/StrandDesign/Package.swift</code></li><li><code class="path-chip">Packages/StrandAnalytics/Package.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Package.swift</code></li><li><code class="path-chip">Packages/WhoopStore/Package.swift</code></li><li><code class="path-chip">Packages/NoopLocalAccess/Package.swift</code></li><li><code class="path-chip">Packages/StrandImport/Package.swift</code></li><li><code class="path-chip">Packages/StrandImport/Tests/StrandImportTests/PlaceholderTests.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Tests/WhoopProtocolTests/SmokeTests.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>WHOOP 月费 $30，且数据锁在云端不可导出；用户花 $200+ 买的硬件一旦停订阅就变砖。NOOP 让硬件所有者绕过订阅直接读取表带 BLE 数据，全部离线持久化，零云端依赖。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用跨平台模块化设计，Swift Packages（WhoopProtocol、WhoopStore、StrandAnalytics、StrandDesign、StrandImport、NoopLocalAccess）与 Android Kotlin 共享同一 BLE 协议层。核心链路为：BLE 扫描→GATT 连接→帧解码（<code class="code-ref">WhoopProtocol</code> 包的 <code class="code-ref">parseFrame</code>，按 <code class="code-ref">DeviceFamily</code> 选择 CRC8/CRC16 校验）→数据持久化（<code class="code-ref">WhoopStore</code> 基于 GRDB 的 SQLite，通过 <code class="code-ref">syncWrite</code>/<code class="code-ref">syncRead</code> 做 actor 隔离的读写）→分析层（<code class="code-ref">StrandAnalytics</code> 纯函数计算 HRV/RMSSD/TRIMP/Recovery/Sleep）。<code class="code-ref">NoopLocalAccess</code> 包提供 MCP stdio server（<code class="code-ref">Packages/NoopLocalAccess/Sources/noop-local-access/main.swift</code>），让本地 AI agent 可以只读查询 NOOP 数据库。Android 端用 Room 做持久化，Compose 做 UI，Gradle 配置中声明了 full/demo 两个 flavor（<code class="code-ref">android/app/build.gradle.kts:51-68</code>），demo 内置 120 天合成数据方便无表带试用。</p>
<p class="audit-callout audit-callout--highlight">协议解码与设备无关——<code class="code-ref">DeviceFamily</code>（<code class="code-ref">Packages/WhoopProtocol/Sources/WhoopProtocol/DeviceFamily.swift</code>）抽象出 whoop4/whoop5 两种硬件族，通过 <code class="code-ref">headerCRCKind</code> 和 <code class="code-ref">characteristicUUIDStrings</code> 实现一套 parseFrame 覆盖两代硬件，5.0 的 puffin 类型通过 <code class="code-ref">canonicalTypeName</code> 透明映射回基础类型名，避免 if-else 硬编码。</p>
<p class="audit-callout audit-callout--highlight">供应链安全意识——<code class="code-ref">WhoopStore/Package.swift</code> 和 <code class="code-ref">StrandImport/Package.swift</code> 对 GRDB、ZIPFoundation 等外部依赖使用 <code class="code-ref">exact:</code> 版本锁定，注释明确说明是为了防止自动拉取被入侵的上游版本，这在社区项目中罕见。</p>
<p class="audit-callout audit-callout--doubt">核心 BLE 连接/断线重连/历史回放逻辑未在 code_bundle 中出现（<code class="code-ref">Strand/</code>、<code class="code-ref">StrandiOS/</code> 等 app target 目录缺失），CI 中 <code class="code-ref">app-build.yml</code> 仅做编译不跑测试（<code class="code-ref">CODE_SIGNING_ALLOWED=NO</code>），无法评估实际 BLE 会话管理的健壮性。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">StrandImport</code> 测试仅含一个占位 <code class="code-ref">testVersion()</code>（<code class="code-ref">Packages/StrandImport/Tests/StrandImportTests/PlaceholderTests.swift</code>），import 功能描述为 &quot;Plan Milestone 4&quot;，Apple Health XML 流式解析尚未实现；<code class="code-ref">StrandAnalytics</code> 的测试文件也未在 bundle 中出现，核心分析算法（HRV/RMSSD/StrainScorer）的正确性无法从测试层验证。</p>
<p>可作为 WHOOP 用户的离线数据备份工具立即使用，但建议谨慎——协议逆向工程存在 WHOOP 固件更新后失效的风险（README 自己提到这是持续维护成本）。开发者可关注 <code class="code-ref">NoopLocalAccess</code> MCP server，它把本地健康数据暴露为 AI 可查询接口，是 health-data-as-tool-use 的好模式。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>WHOOP 固件更新可随时改变 BLE 协议帧格式，维护者单人维护无 SLA，断裂后修复周期不可控</li><li>PolyForm Noncommercial 1.0.0 许可证禁止商业用途，且 LICENSE 元数据显示 NOASSERTION——包管理器/合规团队可能无法自动识别许可条款</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向 WHOOP 用户社区有明确付费意愿（省 $30/月订阅），但 PolyForm Noncommercial 许可证排除了商业变现路径。商业价值在于验证了「本地优先健康数据」的产品方向，可被合规的硬件生态合作借鉴。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">80.25</span>
  </div>
</div>
</section>