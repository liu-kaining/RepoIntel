---
title: '[Score: 82.0] vedika-io/xalen-ephemeris'
date: '2026-06-22T03:57:16Z'
categories:
- Astronomical Ephemeris & Astrology Engine
tags:
- Rust
- ephemeris
- astrology
- WASM
- PyO3
- napi-rs
intel_score: 82.0
repo_name: vedika-io/xalen-ephemeris
repo_link: https://github.com/vedika-io/xalen-ephemeris
summary: 纯 Rust 实现的多传统天文星历库，覆盖 Vedic/Western/Chinese 等 12+ 体系，以 VSOP87A+ELP2000 为内核并支持
  DE440 内核，适合占星应用开发者直接集成。
code_source: git
code_files_reviewed:
- crates/xalen-iching/Cargo.toml
- crates/xalen-numerology/Cargo.toml
- crates/xalen-time/Cargo.toml
- crates/xalen-chinese/Cargo.toml
- crates/xalen-stars/Cargo.toml
- crates/xalen-chart/Cargo.toml
- .github/workflows/ci.yml
- .github/workflows/release.yml
- crates/xalen-world/src/lib.rs
- crates/xalen-houses/src/lib.rs
- crates/xalen-python/xalen/__init__.py
- crates/xalen-time/src/lib.rs
- crates/xalen-lalkitab/src/lib.rs
- crates/xalen-western/src/lib.rs
- crates/xalen-coords/src/lib.rs
- src/lib.rs
- crates/xalen-vedic/src/lib.rs
- crates/xalen-node/build.rs
- crates/xalen-chart/README.md
- crates/xalen-coords/README.md
- crates/xalen-world/README.md
- crates/xalen-time/README.md
- crates/xalen-numerology/README.md
- crates/xalen-chinese/README.md
- crates/xalen-vedic/README.md
- crates/xalen-western/README.md
- crates/xalen-ephem/README.md
- crates/xalen-lalkitab/README.md
- crates/xalen-ayanamsa/README.md
- crates/xalen-ffi/README.md
- crates/xalen-stars/README.md
- crates/xalen-iching/README.md
- crates/xalen-houses/README.md
- crates/xalen-node/index.d.ts
- crates/xalen-wasm/README.md
- crates/xalen-node/README.md
- crates/xalen-python/README.md
- crates/xalen-ephem/tests/readme_example.rs
- crates/xalen-chart/tests/robustness_regression.rs
- crates/xalen-houses/tests/vertex_swiss_regression.rs
- crates/xalen-python/tests/test_build_config.py
- crates/xalen-ephem/tests/vsop87_official_crossval.rs
- crates/xalen-chinese/tests/bazi_fixtures.rs
- crates/xalen-ephem/tests/data/swiss_rise_set_oracle.json
- crates/xalen-coords/tests/sofa_reference_crossval.rs
- crates/xalen-coords/src/obliquity.rs
- crates/xalen-ephem/examples/validate_medieval.rs
- crates/xalen-western/src/lunar.rs
code_chars_analyzed: 157319
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
      <span class="scope-stat__value">约 157,319 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/xalen-iching/Cargo.toml</code></li><li><code class="path-chip">crates/xalen-numerology/Cargo.toml</code></li><li><code class="path-chip">crates/xalen-time/Cargo.toml</code></li><li><code class="path-chip">crates/xalen-chinese/Cargo.toml</code></li><li><code class="path-chip">crates/xalen-stars/Cargo.toml</code></li><li><code class="path-chip">crates/xalen-chart/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">crates/xalen-world/src/lib.rs</code></li><li><code class="path-chip">crates/xalen-houses/src/lib.rs</code></li><li><code class="path-chip">crates/xalen-python/xalen/__init__.py</code></li><li><code class="path-chip">crates/xalen-time/src/lib.rs</code></li><li><code class="path-chip">crates/xalen-lalkitab/src/lib.rs</code></li><li><code class="path-chip">crates/xalen-western/src/lib.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>占星应用开发者长期依赖 C 写的 Swiss Ephemeris（GPL/AGPL 许可、需分发数据文件、有 unsafe 状态），在 Rust/WASM 项目中集成需要手动桥接并承担许可风险。一个零 unsafe、零数据文件、Apache-2.0 的纯 Rust 星历库可以直接消除这条链路上的许可、跨平台编译和线程安全隐患。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">仓库按 workspace 拆为 17 个 crate，从底层时间原语（<code class="code-ref">crates/xalen-time/src/lib.rs</code>，<code class="code-ref">JdTT</code>/<code class="code-ref">JdUT1</code>/<code class="code-ref">JdTDB</code> 三个 newtype 隔离时间尺度）→ 坐标/岁差/章动（<code class="code-ref">crates/xalen-coords/src/obliquity.rs:8</code> 实现 IAU 2006 多项式）→ 行星历表（<code class="code-ref">crates/xalen-ephem/</code>，VSOP87A 解析理论 + 可选 DE440 BSP 读取）→ 占星语义层（vedic/western/chinese/world 各自独立 crate）→ 语言绑定（Python via PyO3、Node via napi-rs、WASM via wasm-bindgen、C FFI via <code class="code-ref">crates/xalen-ffi/</code>）。<code class="code-ref">Almanac</code> 门面用 <code class="code-ref">Send + Sync</code> 保证线程安全，UT1→TT 转换内置 delta-T 模型。CI 在 <code class="code-ref">.github/workflows/ci.yml</code> 覆盖三平台测试矩阵、DE440 外部核验证（<code class="code-ref">de440-validation</code> job 从 NASA NAIF 下载 33MB SPK 后跑 <code class="code-ref">tests/de440_real_crossval</code>）、RustSec 安全审计、wasm-pack 构建、以及 Python/Node 绑定的端到端编译。</p>
<p class="audit-callout audit-callout--highlight">VSOP87A 官方 check file 交叉验证（<code class="code-ref">crates/xalen-ephem/tests/vsop87_official_crossval.rs:43</code>）直接解析 Bretagnon &amp; Francou 发布的 <code class="code-ref">vsop87.chk</code>，对内行星精度门到 1e-8 AU、外行星 3e-6 AU，是源理论级的回归守卫而非传递性依赖。</p>
<p class="audit-callout audit-callout--highlight">SOFA 参考交叉验证（<code class="code-ref">crates/xalen-coords/tests/sofa_reference_crossval.rs:24</code>）将 IAU 2000B 章动和 IAU 2006 均值黄赤交角直接与 IAU 自身 C 实现比对，容差设在真实模型截断误差包络内（Δψ ≤ 2e-8 rad），不是任意宽限值。</p>
<p class="audit-callout audit-callout--doubt">48 个文件仅占 312 个文件的 15%，核心计算 crate（<code class="code-ref">xalen-ephem/src/</code>、<code class="code-ref">xalen-vedic/src/</code>、<code class="code-ref">xalen-western/src/</code>）的实际实现文件完全未审阅，无法验证 VSOP87 级数展开、ELP2000 月球模型、DE440 Chebyshev 求值等核心逻辑的正确性。本次工程评分主要基于测试和 CI 的间接证据。</p>
<p class="audit-callout audit-callout--doubt">仓库仅 26 天且 recent_commit_count=1，README 明确说明所有包均未发布到 PyPI/npm/crates.io，star 数 873 可能受占星话题热度影响而非真实生产采用。</p>
<p>发布前需补齐 xalen-ephem/xalen-vedic/xalen-western 的核心计算源码审计；Nadi astrology 和 Lal Kitab 的解读文本返回 <code class="code-ref">None</code>（<code class="code-ref">crates/xalen-vedic/README.md</code> 注明）需在用户文档中突出标注以免混淆；BaZi 测试（<code class="code-ref">crates/xalen-chinese/tests/bazi_fixtures.rs</code>）仅覆盖 noon UT，缺少本地真太阳时/时区的端到端案例。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>所有包均未发布到任何 registry（README 明确标注），无法通过常规依赖管理使用，需从源码编译。</li><li>核心计算文件（VSOP87 展开、ELP2000 月球、DE440 Chebyshev）未在本次 code_bundle 中审阅，工程评分基于测试/CI 间接证据而非源码直接审计。</li><li>recent_commit_count=1 且 repo 仅 26 天，维护者集中度和长期持续维护迹象不足。</li><li>BaZi 四柱测试仅覆盖 noon UT 时刻（<code class="code-ref">crates/xalen-chinese/tests/bazi_fixtures.rs</code>），未涉及真太阳时/经度校正场景，对时区敏感用户存在边界风险。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对需要在 Rust/WASM/Node 生态中嵌入占星计算的 SaaS、小程序或桌面应用而言，Apache-2.0 + 零数据文件 + 多语言绑定（Python/npm/WASM/FFI）构成明确的集成优势，可替代 Swiss Ephemeris 的 C/AGPL 依赖。未发布状态和仅 26 天仓库年龄意味着尚无真实生产用户反馈。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.0</span>
  </div>
</div>
</section>