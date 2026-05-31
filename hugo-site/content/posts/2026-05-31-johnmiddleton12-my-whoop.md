---
title: '[Score: 75.3] johnmiddleton12/my-whoop'
date: '2026-05-31T03:33:40Z'
categories:
- Wearable BLE Protocol & Health Metrics Pipeline
tags:
- Bluetooth LE
- WHOOP 4.0
- health-data
- reverse-engineering
- TimescaleDB
- SwiftUI
intel_score: 75.3
repo_name: johnmiddleton12/my-whoop
repo_link: https://github.com/johnmiddleton12/my-whoop
summary: 通过 BLE 逆向 WHOOP 4.0 协议，提供本地优先的 iOS 采集 + 自托管 FastAPI/TimescaleDB 存储与派生健康指标计算全链路，适合希望持有自身穿戴数据的开发者。
code_source: git
code_files_reviewed:
- server/ingest/requirements.txt
- server/packages/whoop-protocol/pyproject.toml
- server/ingest/Dockerfile
- server/docker-compose.yml
- server/packages/whoop-protocol/whoop_protocol/__init__.py
- server/ingest/app/analysis/__init__.py
- server/ingest/app/whoop_api/__init__.py
- server/ingest/app/analysis/validation/__init__.py
- server/ingest/app/main.py
- server/README.md
- server/VERIFY.md
- Packages/WhoopProtocol/Package.swift
- Packages/WhoopStore/Package.swift
- server/client/test_uploader.py
- server/client/uploader.py
- server/db/init.sql
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/SmokeTests.swift
- Packages/WhoopProtocol/Tests/WhoopProtocolTests/Resources/historical_golden.json
- server/packages/whoop-protocol/tests/test_interpreter_realtime.py
- Packages/WhoopStore/Tests/WhoopStoreTests/ScaffoldTests.swift
- Packages/WhoopStore/Tests/WhoopStoreTests/LatestSampleTests.swift
- server/packages/whoop-protocol/tests/test_interpreter_envelope.py
- server/packages/whoop-protocol/tests/test_interpreter_raw.py
- server/packages/whoop-protocol/tests/test_interpreter_meta_logs.py
- server/ingest/app/config.py
- server/packages/whoop-protocol/README.md
- server/ingest/app/archive.py
- server/ingest/app/db.py
- server/ingest/app/ingest.py
- server/ingest/app/store.py
- server/ingest/app/read.py
- server/ingest/docs/2026-05-26-metrics-methodology.md
- Packages/WhoopProtocol/Sources/WhoopProtocol/WhoopProtocol.swift
- server/ingest/app/analysis/_utils.py
- Packages/WhoopStore/Sources/WhoopStore/Cursors.swift
- server/packages/whoop-protocol/whoop_protocol/schema.py
- Packages/WhoopProtocol/Sources/WhoopProtocol/HistoricalMeta.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/Values.swift
- Packages/WhoopStore/Sources/WhoopStore/WhoopStore.swift
- Packages/WhoopProtocol/Sources/WhoopProtocol/HistoricalStreams.swift
- server/packages/whoop-protocol/whoop_protocol/framing.py
- server/ingest/app/whoop_api/models.py
- server/ingest/app/whoop_api/README.md
- Packages/WhoopProtocol/Sources/WhoopProtocol/Framing.swift
code_chars_analyzed: 126851
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
      <span class="scope-stat__value">44 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 126,851 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">server/ingest/requirements.txt</code></li><li><code class="path-chip">server/packages/whoop-protocol/pyproject.toml</code></li><li><code class="path-chip">server/ingest/Dockerfile</code></li><li><code class="path-chip">server/docker-compose.yml</code></li><li><code class="path-chip">server/packages/whoop-protocol/whoop_protocol/__init__.py</code></li><li><code class="path-chip">server/ingest/app/analysis/__init__.py</code></li><li><code class="path-chip">server/ingest/app/whoop_api/__init__.py</code></li><li><code class="path-chip">server/ingest/app/analysis/validation/__init__.py</code></li><li><code class="path-chip">server/ingest/app/main.py</code></li><li><code class="path-chip">server/README.md</code></li><li><code class="path-chip">server/VERIFY.md</code></li><li><code class="path-chip">Packages/WhoopProtocol/Package.swift</code></li><li><code class="path-chip">Packages/WhoopStore/Package.swift</code></li><li><code class="path-chip">server/client/test_uploader.py</code></li><li class="path-more">另有 30 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>WHOOP 用户的所有生物指标默认锁定在官方云端；若想在本地持久化、做长期趋势分析或对接第三方工具，无官方 API 导出全量高采样数据的途径，且关账户即丢数据。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分为 iOS 端（SwiftUI + CoreBluetooth 采集）与自托管服务端（FastAPI ingest + TimescaleDB 存储 + 派生指标分析）两大部分，通过一个共享的 JSON schema（<code class="code-ref">protocol/whoop_protocol.json</code>）实现 Python/Swift 跨语言解码一致性。服务端写入链路为 <code class="code-ref">POST /v1/ingest</code> → <code class="code-ref">ingest.process_batch</code> (<code class="code-ref">server/ingest/app/ingest.py:19</code>) 解码 + 归档原始帧 → <code class="code-ref">store.upsert_streams</code> (<code class="code-ref">server/ingest/app/store.py:37</code>) 幂等写入 TimescaleDB hypertable；解码后的推算指标通过 <code class="code-ref">daily.compute_day</code> 完成睡眠分期、HRV、Recovery、Strain 等完整管线。</p>
<p class="audit-callout audit-callout--highlight">跨语言 schema-as-data 设计——<code class="code-ref">server/packages/whoop-protocol/whoop_protocol/schema.py:11</code> 的 <code class="code-ref">Schema</code> 类从单一 JSON 文件加载所有包类型布局与枚举，Swift 端 <code class="code-ref">Packages/WhoopProtocol/Sources/WhoopProtocol/Framing.swift</code> 将同一 CRC8/CRC32 和 <code class="code-ref">Reassembler</code> 逐字移植，附带 golden test (<code class="code-ref">historical_golden.json</code>) 验证 JSON round-trip 一致性。这种「一次编辑，双端生效」的结构是协议逆向项目中最实际的防漂移手段。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">server/ingest/app/main.py:38</code> 的 <code class="code-ref">_RECOMPUTE_COOLDOWN_S</code> + 单飞锁设计：手机上传频次高（~30s 一次），而 <code class="code-ref">compute_day</code> 跑 neurokit2 睡眠分期管线 CPU/内存消耗大；该节流机制确保同一 (device, day) 在冷却期内不重复计算，且不阻塞 ingest 返回 200——原始流数据持久化与派生计算解耦，失败只 log 不回滚 ingest 事务。</p>
<p class="audit-callout audit-callout--doubt">iOS 端代码——<code class="code-ref">ios/</code> 目录下的 SwiftUI 应用、CoreBluetooth BLE 管理器、GRDB 本地存储等核心文件均未出现在 code_bundle 中，无法验证 BLE 连接稳定性处理、前台/后台切换、蓝牙权限降级等关键路径。Swift 包的测试仅覆盖 schema 资源加载 (<code class="code-ref">SmokeTests.swift</code>) 和 GRDB 可用性 (<code class="code-ref">ScaffoldTests.swift</code>)，缺少对 <code class="code-ref">Framing.swift</code> 的 CRC/Reassembler 单元测试和对 <code class="code-ref">WhoopStore</code> 写入/迁移的完整覆盖。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">server/ingest/app/read.py:220</code> 的 <code class="code-ref">_query_stream_downsampled</code> 将用户传入的 <code class="code-ref">kind</code> 拼入 f-string SQL（<code class="code-ref">f&quot;SELECT ... FROM {table}&quot;</code>），虽然 <code class="code-ref">table</code> 来自硬编码 <code class="code-ref">_STREAMS</code> 映射而非直接受控于用户输入，但 <code class="code-ref">kind</code> 在 <code class="code-ref">query_stream</code> 入口通过 <code class="code-ref">ValueError</code> 过滤，若未来有人扩展 <code class="code-ref">_STREAMS</code> 字典时引入用户可控键名，该模式即成注入面。此外 <code class="code-ref">counts</code> 函数 (<code class="code-ref">read.py:275</code>) 同样复用此 f-string 模式。</p>
<p>1) 补齐 iOS 端源码与 BLE 端到端测试后再做完整审计；2) 为 <code class="code-ref">Framing.swift</code> 添加与 Python <code class="code-ref">test_interpreter_*</code> 对等的 Swift 单元测试；3) 将 SQL f-string 改为参数化表名白名单校验或使用 identifier-quoting（psycopg 的 <code class="code-ref">sql.Identifier</code>）消除隐患；4) README 的 legal disclaimer 虽详尽，但 <code class="code-ref">protocol/whoop_protocol.json</code> 的字段布局是否构成「反向工程事实」在不同法域仍有不确定性，建议维护者保持与 WHOOP 的 takedown 联系渠道畅通。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>WHOOP 4.0 BLE 协议属逆向工程产物，若 WHOOP 更新固件改协议字段偏移，解码管线将静默失效而无自动告警机制。</li><li>iOS 端源码未审阅；派生指标（SpO2/皮温/呼吸率）均为未校准的近似值（方法论文档明确标注 UNVERIFIED），不应用于医疗决策。</li><li>README 未声明 LICENSE；code_bundle 中 license=null，下游使用者面临默认版权保留风险。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向 WHOOP 用户中对数据主权有强需求的技术人群（开发者/量化自我爱好者），作为自托管替代方案有明确的 niche 市场。但受 WHOOP 商标/协议法律风险约束，商业变现空间有限，更适合社区驱动的开源工具定位。</p>
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
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.3</span>
  </div>
</div>
</section>