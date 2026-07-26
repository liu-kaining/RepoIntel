---
title: '[Score: 75.15] QW-AI-Code/Aether'
date: '2026-07-26T19:05:53Z'
categories:
- Proxy & VPN Client
tags:
- Android
- QUIC
- Cloudflare WARP
- MASQUE
- WireGuard
- censorship circumvention
intel_score: 75.15
repo_name: QW-AI-Code/Aether
repo_link: https://github.com/QW-AI-Code/Aether
summary: Aether Mobile 是一个内置自研隧道引擎的 Android VPN 客户端，直接通过 Cloudflare WARP 网络加密转发流量，专注于伊朗等高审查地区的连通性。
code_source: git
code_files_reviewed:
- build.gradle.kts
- native/aether/quiche/tools/http3_test/Cargo.toml
- native/aether/quiche/buffer-pool/Cargo.toml
- native/aether/Dockerfile
- native/aether/quiche/octets/Cargo.toml
- native/aether/quiche/netlog/Cargo.toml
- .github/workflows/build.yml
- native/aether/quiche/tokio-quiche/tests/main.rs
- native/aether/quiche/h3i/src/recordreplay/mod.rs
- native/aether/quiche/h3i/src/prompts/mod.rs
- native/aether/quiche/apps/src/lib.rs
- native/aether/quiche/tokio-quiche/src/quic/io/mod.rs
- native/aether/quiche/qlog-dancer/src/trackers/mod.rs
- native/aether/quiche/h3i/src/actions/mod.rs
- native/aether/quiche/tokio-quiche/src/socket/mod.rs
- native/aether/quiche/tokio-quiche/src/http3/mod.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/headers.rs
- native/aether/quiche/qlog/src/testing/trace_tests.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/qlog_compression.rs
- native/aether/quiche/tokio-quiche/tests/fixtures/h3i_fixtures.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/async_callbacks.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/connection_close.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/stream_limit.rs
- native/aether/quiche/tokio-quiche/tests/integration_tests/zero_rtt.rs
- native/aether/quiche/clippy.toml
- native/aether/quiche/.gitlab-ci.yml
- app/src/main/java/studio/cluvex/aether/ui/theme/Type.kt
- native/aether/aether/src/mac_test.rs
- native/aether/quiche/quiche/examples/README.md
- app/src/main/java/studio/cluvex/aether/ui/theme/Color.kt
- settings.gradle.kts
- native/aether/quiche/quiche/examples/gen-certs.sh
- native/aether/quiche/catalog-info.yaml
- native/aether/quiche/tools/android/build_android_ndk19.sh
- native/aether/aether/src/error.rs
- native/aether/quiche/.github/workflows/semgrep.yml
- native/aether/aether/src/lastconn.rs
- app/src/main/java/studio/cluvex/aether/model/ConnectionState.kt
- native/aether/quiche/tools/gen_fuzz_seeds.sh
- native/aether/quiche/.github/dependabot.yml
- native/aether/quiche/.github/workflows/deploy.yml
- native/aether/aether/src/consts.rs
- native/aether/quiche/fuzz/src/qpack_decode.rs
- app/src/main/java/studio/cluvex/aether/ui/components/AmbientBackground.kt
- native/aether/quiche/Cross.toml
- native/aether/quiche/rustfmt.toml
- app/src/main/java/studio/cluvex/aether/core/TunnelConfig.kt
- scripts/generate-keystore.sh
code_chars_analyzed: 108582
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
      <span class="scope-stat__value">约 108,582 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">build.gradle.kts</code></li><li><code class="path-chip">native/aether/quiche/tools/http3_test/Cargo.toml</code></li><li><code class="path-chip">native/aether/quiche/buffer-pool/Cargo.toml</code></li><li><code class="path-chip">native/aether/Dockerfile</code></li><li><code class="path-chip">native/aether/quiche/octets/Cargo.toml</code></li><li><code class="path-chip">native/aether/quiche/netlog/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/build.yml</code></li><li><code class="path-chip">native/aether/quiche/tokio-quiche/tests/main.rs</code></li><li><code class="path-chip">native/aether/quiche/h3i/src/recordreplay/mod.rs</code></li><li><code class="path-chip">native/aether/quiche/h3i/src/prompts/mod.rs</code></li><li><code class="path-chip">native/aether/quiche/apps/src/lib.rs</code></li><li><code class="path-chip">native/aether/quiche/tokio-quiche/src/quic/io/mod.rs</code></li><li><code class="path-chip">native/aether/quiche/qlog-dancer/src/trackers/mod.rs</code></li><li><code class="path-chip">native/aether/quiche/h3i/src/actions/mod.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>伊朗等地区用户使用常规代理常因深度包检测（DPI）导致连接不稳定或阻断；Aether 整合 MASQUE/WireGuard 隧道，通过 Cloudflare 的 anycast 网络自动选择最佳边缘节点，无需手动配置服务器列表。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">Android 端采用 Kotlin + Jetpack Compose 构建 UI，通过 JNI 接入三个原生库：libaether.so（自研 QUIC/HTTP3 引擎）、libhev-socks5-tunnel.so（基于 hev 的 SOCKS5 隧道）和 libaethertun.so（TUN 接口桥接）。引擎启动后建立与 Cloudflare 消费者 MASQUE 服务器的 QUIC 连接，内部上层协议为 cf-connect-ip，将设备流量封装到加密隧道中。</p>
<p class="audit-callout audit-callout--highlight">CI 流水线具有自动核心同步与安全回滚机制（<code class="code-ref">.github/workflows/build.yml</code>）。每次构建会拉取上游 Aether 引擎仓库最新稳定版本（v1.4），并通过三向合并将本项目的定制补丁（如 <code class="code-ref">prober.rs</code>、<code class="code-ref">wg_prober.rs</code>）合并到新代码中；若编译失败，自动回滚到上一个可工作的核心版本，确保发布不会因上游 API 变动而中断。</p>
<p class="audit-callout audit-callout--highlight">签名管理严密的覆盖安装保护（<code class="code-ref">.github/workflows/build.yml</code>）。构建流程会记录 APK 的签名指纹，并比对历史版本，若签名变化则阻止发布，避免用户因证书不匹配而被迫卸载重装；同时完全移除应用内更新功能（README 中删除 <code class="code-ref">UpdateChecker.kt</code> 等文件），杜绝从非官方渠道加载二进制文件的风险。</p>
<p class="audit-callout audit-callout--doubt">未审阅到核心引擎的 Rust 源码（<code class="code-ref">native/aether/aether/src/</code> 下未提供主循环、探测器或 WireGuard 实现）。自定义补丁 <code class="code-ref">prober.rs</code>、<code class="code-ref">wg_prober.rs</code> 的逻辑无法评估，这些模块决定端点选择和协议适应策略，其正确性直接影响隧道可靠性。</p>
<p class="audit-callout audit-callout--doubt">上游引擎依赖庞大的 Cloudflare quiche 库，且从 Rust 交叉编译 Android 原生库，产物体积大（APK 包含多个 ABI），而项目源码中几乎无 Aether 自身的单元测试或集成测试，仅有 quiche 的测试文件（如 <code class="code-ref">native/aether/quiche/tokio-quiche/tests/stream_limit.rs</code>），无法验证自研层在异常网络下的行为。</p>
<p>该客户端适合作为抗审查工具在伊朗等市场上替代 v2rayNG，但开发者应尽快补充引擎层的测试（尤其是探测回退逻辑），并保持与上游 quiche 的同步，以修复潜在的 QUIC 安全漏洞。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心代码依赖未审计的 Rust 补丁，可能引入隐蔽的数据侧信道。</li><li>仅提供 Android 客户端，且严重依赖 Cloudflare 服务，若 WARP 入口被封锁将完全失效。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>项目本身不直接盈利，但可作为技术底子集成到商用 VPN 产品中；依赖 Cloudflare 免费 WARP 基础设施，长期稳定性受 Cloudflare 政策制约。</p>
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
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
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
    <span class="total-score-banner__value">75.15</span>
  </div>
</div>
</section>