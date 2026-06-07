---
title: '[Score: 77.55] NoopApp/noop'
date: '2026-06-07T22:01:50Z'
categories:
- Health Wearable Companion App
tags:
- Swift
- Bluetooth
- WHOOP
- Local-First
- Health Analytics
- SQLite
intel_score: 77.55
repo_name: NoopApp/noop
repo_link: https://github.com/NoopApp/noop
summary: 离线 WHOOP 手环伴侣 App，通过 BLE 直连读取心率/HRV/SpO₂ 等数据并本地计算恢复评分与睡眠分期，无需云端账号与订阅。
code_source: git
code_files_reviewed:
- android/build.gradle.kts
- android/app/build.gradle.kts
- Packages/StrandDesign/Package.swift
- Packages/StrandAnalytics/Package.swift
- Packages/WhoopProtocol/Package.swift
- Packages/WhoopStore/Package.swift
- Packages/StrandImport/Package.swift
- Packages/StrandImport/Tests/StrandImportTests/PlaceholderTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/SmokeTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/Resources/historical_golden.json
- Packages/WhoopStore/Tests/WhoopStoreTests/ScaffoldTests.swift
- Packages/WhoopStore/Tests/WhoopStoreTests/LatestSampleTests.swift
- Packages/StrandImport/Tests/StrandImportTests/Helpers.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/HistoricalStreamsParityTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/ValuesTests.swift
- Packages/StrandImport/Sources/StrandImport/StrandImport.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/WhoopProtocol.swift
- Packages/StrandDesign/Sources/StrandDesign/StrandDesign.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/StrandAnalytics.swift
- Packages/WhoopStore/Sources/WhoopStore/Cursors.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Values.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/HistoricalMeta.swift
- Packages/StrandDesign/Sources/StrandDesign/Motion.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/HistoricalStreams.swift
- Packages/StrandDesign/Sources/StrandDesign/StrandCard.swift
- Packages/WhoopStore/Sources/WhoopStore/MetricSeriesStore.swift
- Packages/WhoopStore/Sources/WhoopStore/WhoopStore.swift
- Packages/StrandDesign/Sources/StrandDesign/StatePill.swift
- Packages/StrandDesign/Sources/StrandDesign/Typography.swift
- Packages/StrandImport/Sources/StrandImport/ImportCoordinator.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/DeviceFamily.swift
- Packages/WhoopStore/Sources/WhoopStore/Reads.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Schema.swift
- Packages/WhoopStore/Sources/WhoopStore/StreamStore.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/HRZones.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/CorrelationEngine.swift
- Packages/StrandDesign/Sources/StrandDesign/StrainGauge.swift
- Packages/StrandDesign/Sources/StrandDesign/ChartHover.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Streams.swift
- Packages/StrandDesign/Sources/StrandDesign/Sparkline.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/RecoveryScorer.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/HRVAnalyzer.swift
- Packages/WhoopStore/Sources/WhoopStore/MetricsCache.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/ComparisonEngine.swift
- Packages/StrandAnalytics/Sources/StrandAnalytics/StrainScorer.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Framing.swift
- Packages/WhoopStore/Sources/WhoopStore/RawOutbox.swift
- Packages/WhoopStore/Sources/WhoopStore/JournalWorkoutAppleCache.swift
code_chars_analyzed: 201176
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
      <span class="scope-stat__value">约 201,176 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">android/build.gradle.kts</code></li><li><code class="path-chip">android/app/build.gradle.kts</code></li><li><code class="path-chip">Packages/StrandDesign/Package.swift</code></li><li><code class="path-chip">Packages/StrandAnalytics/Package.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Package.swift</code></li><li><code class="path-chip">Packages/WhoopStore/Package.swift</code></li><li><code class="path-chip">Packages/StrandImport/Package.swift</code></li><li><code class="path-chip">Packages/StrandImport/Tests/StrandImportTests/PlaceholderTests.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Tests/WhoopProtocolTests/SmokeTests.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Tests/WhoopProtocolTests/Resources/historical_golden.json</code></li><li><code class="path-chip">Packages/WhoopStore/Tests/WhoopStoreTests/ScaffoldTests.swift</code></li><li><code class="path-chip">Packages/WhoopStore/Tests/WhoopStoreTests/LatestSampleTests.swift</code></li><li><code class="path-chip">Packages/StrandImport/Tests/StrandImportTests/Helpers.swift</code></li><li><code class="path-chip">Packages/WhoopProtocol/Tests/WhoopProtocolTests/HistoricalStreamsParityTests.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>WHOOP 用户必须订阅云端服务才能查看自己手环产生的生物数据；一旦停止订阅或官方服务中断，多年数据将被锁死在平台内。NOOP 让手环拥有者在完全离线环境下读取、存储和分析自己的数据，将数据主权归还用户。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 SPM 包分层设计，核心由 WhoopProtocol（BLE 帧解码）、WhoopStore（GRDB/SQLite 持久化）、StrandAnalytics（纯函数生物指标计算）、StrandDesign（SwiftUI 设计系统）四个本地包组成，Android 端通过 Kotlin/Compose + Room 实现镜像功能。macOS 参考 App 以 SwiftUI 侧边栏驱动 Today/Live/Breathe/Sleep 等页面。</p>
<p class="audit-callout audit-callout--highlight">协议层高度可测试且透明。<code class="code-ref">Packages/WhoopProtocol/Sources/WhoopProtocol/Schema.swift:60</code> 的 <code class="code-ref">loadSchema()</code> 从 bundled JSON 加载完整帧定义，配合 <code class="code-ref">HistoricalStreamsParityTests</code> 将 Python 生成的 golden JSON 做 Swift→Python 逐帧比对（<code class="code-ref">Packages/WhoopProtocol/Tests/WhoopProtocolTests/HistoricalStreamsParityTests.swift:32</code>），保证解码一致性。<code class="code-ref">Framing.swift:90</code> 同时实现 Whoop 4.0（CRC8+CRC32）和 5.0（CRC16-Modbus+CRC32）双协议栈帧校验，包括 <code class="code-ref">Reassembler</code> BLE 碎片重组。</p>
<p class="audit-callout audit-callout--highlight">分析引擎全是纯函数、无 DB 副作用。<code class="code-ref">StrandAnalytics/Sources/StrandAnalytics/RecoveryScorer.swift:95</code> 的 <code class="code-ref">recovery()</code> 基于 z-score+logistic 复合，权重（HRV 0.60、RHR 0.20、呼吸 0.05、睡眠 0.15）全部文档化；<code class="code-ref">HRVAnalyzer.swift:125</code> 实现 Task Force 1996 RMSSD/SDNN + Malik 20% 本地中位数异位点过滤；<code class="code-ref">StrainScorer.swift:130</code> 支持 Edwards 5-zone 和 Banister 指数两种 TRIMP 算法，映射到 0-21 对数刻度。每个算法都注明了引用论文和 WHOOP 原始实现的差异。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖率偏薄。<code class="code-ref">StrandImportTests/PlaceholderTests.swift</code> 仅检查版本号字符串；<code class="code-ref">WhoopStoreTests/ScaffoldTests.swift</code> 仅验证 GRDB 链接和 schema version；虽然 <code class="code-ref">LatestSampleTests</code> 和 <code class="code-ref">HistoricalStreamsParityTests</code> 覆盖了写入/查询和解码对等，但 StrandAnalytics 包（恢复评分、HRV、应变）未在 bundle 中看到任何测试文件，作为核心算法这是明显缺口。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 BLE 连接管理器和睡眠分期器（SleepStager）的实际实现。README 描述了 Live 视图和 sleep stager，但 code_bundle 中无对应源文件，本次结论不覆盖这两部分。Android 端也只有 build.gradle.kts，无 Kotlin 业务代码被包含，无法评估其实现质量。</p>
<p>StrandAnalytics 作为用户直接依赖的核心决策引擎（恢复评分影响训练/休息建议），应优先补充单元测试覆盖边界场景（冷启动基线不足、零方差输入、极端 HR 值）。此外，release build 未启用 R8（<code class="code-ref">android/app/build.gradle.kts:58</code> 注释说是因为反射崩溃），应在正式发布前解决 keep rules 以减小 APK 体积。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>无 LICENSE 文件，源码默认受版权保护，商业或社区分发存在法律灰色地带。</li><li>WHOOP 5.0 CLIENT_HELLO 为硬编码字节数组（DeviceFamily.swift:70），固件更新后该握手将立即失效，用户需等项目更新。</li><li>README 明确声明非医疗设备，恢复/应变评分仅为近似值，若用户据此做训练决策可能产生误判风险。</li><li>Fork/Star 比 0.92 极高但 star 仅 187、repo 仅 0 天，社区尚未形成外部贡献者，维护集中度风险大。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向 WHOOP 生态中对数据隐私敏感或不满订阅制的用户群体，具备清晰的替代方案定位；若 WHOOP 官方不采取法律行动或协议变更，该工具有潜力成为社区标准伴侣 App。</p>
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
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.55</span>
  </div>
</div>
</section>