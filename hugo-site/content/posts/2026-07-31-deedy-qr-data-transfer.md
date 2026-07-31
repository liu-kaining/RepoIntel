---
title: '[Score: 79.25] deedy/qr-data-transfer'
date: '2026-07-31T22:02:09Z'
categories:
- Optical Data Transfer
tags:
- QR
- RaptorQ
- Fountain Codes
- Browser
- Air-Gapped
- File Transfer
intel_score: 79.25
repo_name: deedy/qr-data-transfer
repo_link: https://github.com/deedy/qr-data-transfer
summary: QRFerry 在浏览器端用动态QR码和RaptorQ喷泉码实现设备间离线文件传输，无需网络。
code_source: git
code_files_reviewed:
- package.json
- db/index.ts
- worker/index.ts
- lib/qr-renderer.ts
- lib/qr-scanner.ts
- lib/compression.ts
- lib/transfer-presets.ts
- lib/optical-transfer.ts
- lib/qr-transfer.ts
- drizzle/meta/_journal.json
- raptorqr-assets.d.ts
- .openai/hosting.json
- next.config.ts
- drizzle.config.ts
- db/schema.ts
- app/pwa-register.tsx
- examples/d1/db/schema.ts
- app/scan/page.tsx
- app/page.tsx
- app/manifest.ts
- tsconfig.json
- app/app-header.tsx
- public/sw.js
- vite.config.ts
- examples/d1/app/api/notes/route.ts
- app/layout.tsx
- app/chatgpt-auth.ts
- README.md
- tests/codec.test.ts
- app/send-client.tsx
- app/scan/scanner-client.tsx
code_chars_analyzed: 121551
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
      <span class="scope-stat__value">约 121,551 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">db/index.ts</code></li><li><code class="path-chip">worker/index.ts</code></li><li><code class="path-chip">lib/qr-renderer.ts</code></li><li><code class="path-chip">lib/qr-scanner.ts</code></li><li><code class="path-chip">lib/compression.ts</code></li><li><code class="path-chip">lib/transfer-presets.ts</code></li><li><code class="path-chip">lib/optical-transfer.ts</code></li><li><code class="path-chip">lib/qr-transfer.ts</code></li><li><code class="path-chip">drizzle/meta/_journal.json</code></li><li><code class="path-chip">raptorqr-assets.d.ts</code></li><li><code class="path-chip">.openai/hosting.json</code></li><li><code class="path-chip">next.config.ts</code></li><li><code class="path-chip">drizzle.config.ts</code></li><li class="path-more">另有 17 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>在无可用网络的隔离环境中，跨端文件传输常依赖外设，流程繁琐且不安全。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">核心库在 lib/ 中：compression.ts 提供 Brotli-11 与 gzip-9 竞速压缩，optical-transfer.ts 构建 QFC4 容器、序列化 QF4 光学帧并执行 CRC-32 校验，transfer-presets.ts 定义 6 个速度预设。发送端 <code class="code-ref">app/send-client.ts</code>x 用 requestAnimationFrame 驱动画布渲染 QR 流；接收端 <code class="code-ref">app/scan/scanner-client.ts</code>x 通过 requestVideoFrameCallback 或 rAF 捕获画面，调用 qr-scanner.ts 中的 ZXing-C++ 解码，再推送到 RaptorQ 解码器重建文件。</p>
<p class="audit-callout audit-callout--highlight">双通道 Turbo 60 和 1 Mbps 实验室预设（<code class="code-ref">lib/transfer-presets.ts</code>）通过交替更新两个 V30-L/V40-L 码实现吞吐翻倍，接收端一次曝光可解析两个码，避免四码网格的密度代价（<code class="code-ref">tests/codec.test.ts</code> 中的双通道测试验证了滚动快门下的稳定性）。</p>
<p class="audit-callout audit-callout--highlight">多层校验链：每帧含 CRC-32（<code class="code-ref">lib/optical-transfer.ts</code> 的 serializeFrame / parseOpticalFrame），恢复的容器整体用 session CRC 验证，最终文件 CRC 与原始 CRC 比对（buildOpticalContainer 中存储 fileCrc），确保 data integrity。</p>
<p class="audit-callout audit-callout--doubt">扫描循环（scanner-client.tsx 的 scanVideoFrame 内 runScan）在高分辨率下可能因同步解码导致帧积压，虽然用 wasm 异步解码，但实际设备上 ZXing 的处理耗时可能超过帧间隔，未看到自适应降分辨率或跳帧策略。</p>
<p class="audit-callout audit-callout--doubt">工程虽提供单元和模拟测试（<code class="code-ref">tests/codec.test.ts</code>），但未见端到端设备测试或 CI 集成配置（如 .github/workflows 缺失），实际屏幕-摄像头物理交互的可靠性仅靠 README 描述验证。</p>
<p>适合内网气隙摆渡或开发者间临时传文件；若要用于生产环境，建议补充实际设备兼容性矩阵和长时间传输的稳健性验证。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>双通道高速模式对设备对齐和光照条件敏感，实际速率可能大幅波动。</li><li>项目仅发布一天，核心依赖 @raptorqr/* 若停更会使协议维护困难。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向零信任架构下的安全文件交换，可集成至企业内网隔离工具链，但需证明跨平台兼容性与长期维护能力。</p>
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
  <div class="score-item__value">86</div>
  <div class="score-bar"><span style="width:86%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.25</span>
  </div>
</div>
</section>