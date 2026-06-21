---
title: '[Score: 77.8] opengeos/geolibre-rust'
date: '2026-06-21T16:28:45Z'
categories:
- WebAssembly Geospatial Toolkit
tags:
- Rust
- WASM
- WASI
- GeoTIFF
- GeoParquet
- geospatial
intel_score: 77.8
repo_name: opengeos/geolibre-rust
repo_link: https://github.com/opengeos/geolibre-rust
summary: 将 whitebox_next_gen 733+ GIS 工具连同自研 PMTiles/GeoParquet/光谱指数等新工具一起编译为浏览器可运行的
  WASM/WASI 模块，面向需要无服务器端 GIS 处理能力的 GeoLibre 前端用户。
code_source: git
code_files_reviewed:
- crates/geolibre-cli/Cargo.toml
- Cargo.toml
- python/pyproject.toml
- npm/package.json
- crates/geolibre-tools/Cargo.toml
- crates/geolibre-wasm/Cargo.toml
- .github/workflows/ci.yml
- .github/workflows/pages.yml
- .github/workflows/release.yml
- python/src/geolibre_wasm/__init__.py
- crates/geolibre-tools/src/lib.rs
- crates/geolibre-cli/src/main.rs
- crates/geolibre-wasm/src/lib.rs
- python/tests/test_smoke.py
- crates/geolibre-tools/src/vector_common.rs
- crates/geolibre-tools/src/vector_convert.rs
- crates/geolibre-wasm/src/analysis.rs
- crates/geolibre-tools/src/hilbert.rs
- crates/geolibre-wasm/src/vector.rs
- crates/geolibre-tools/src/fill.rs
- crates/geolibre-tools/src/render.rs
- crates/geolibre-tools/src/common.rs
- crates/geolibre-wasm/src/lidar.rs
- crates/geolibre-tools/src/reproject_raster.rs
- crates/geolibre-tools/src/render_png.rs
- crates/geolibre-tools/src/raster_normalize.rs
- crates/geolibre-tools/src/delineate_mounts.rs
- crates/geolibre-tools/src/write_pmtiles.rs
- crates/geolibre-tools/src/spectral_index.rs
- crates/geolibre-tools/src/geoparquet_io.rs
- crates/geolibre-tools/src/pmtiles.rs
- crates/geolibre-tools/src/dem_filter.rs
- crates/geolibre-tools/src/raster_to_tiles.rs
- crates/geolibre-tools/src/extract_sinks.rs
- crates/geolibre-tools/src/polygonize.rs
- crates/geolibre-tools/src/regions.rs
- crates/geolibre-tools/src/render_vector_png.rs
- crates/geolibre-tools/src/delineate_depressions.rs
- demo/serve.sh
- npm/tools.d.ts
- build.sh
- npm/README.md
- python/README.md
- python/src/geolibre_wasm/_core.py
- README.md
code_chars_analyzed: 310686
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
      <span class="scope-stat__value">45 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 310,686 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/geolibre-cli/Cargo.toml</code></li><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">python/pyproject.toml</code></li><li><code class="path-chip">npm/package.json</code></li><li><code class="path-chip">crates/geolibre-tools/Cargo.toml</code></li><li><code class="path-chip">crates/geolibre-wasm/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/pages.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">python/src/geolibre_wasm/__init__.py</code></li><li><code class="path-chip">crates/geolibre-tools/src/lib.rs</code></li><li><code class="path-chip">crates/geolibre-cli/src/main.rs</code></li><li><code class="path-chip">crates/geolibre-wasm/src/lib.rs</code></li><li><code class="path-chip">python/tests/test_smoke.py</code></li><li class="path-more">另有 31 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>GIS 前端（GeoLibre/MapLibre）需要在浏览器内直接执行 slope、重投影、切片、GeoParquet 转换等操作，但传统方案依赖 GDAL/PROJ 原生二进制或 Python sidecar，部署复杂且无法纯前端运行。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">三个 crate 分层清晰——<code class="code-ref">crates/geolibre-wasm</code> 通过 wasm-bindgen 暴露 GeoTIFF/COG/LiDAR/Vector/Projection 的 JS API，<code class="code-ref">crates/geolibre-cli</code> 是 WASI 入口将 argv 解析为 ToolRegistry 调用（<code class="code-ref">crates/geolibre-cli/src/main.rs:47</code> <code class="code-ref">build_registry</code>），<code class="code-ref">crates/geolibre-tools</code> 实现 14 个自研工具并注册到 whitebox 的同一 Trait 体系（<code class="code-ref">crates/geolibre-tools/src/lib.rs:41</code> <code class="code-ref">geolibre_tools()</code>）。输入通过 WASI shim 的 <code class="code-ref">/work</code> 内存文件系统进出，JS 端 <code class="code-ref">tools.mjs</code> 负责写入/读回。Python 包 <code class="code-ref">python/src/geolibre_wasm/_core.py:118</code> 通过 wasmtime in-process 执行同一 WASI 二进制，URL 输入会自动下载。工具端采用统一的 <code class="code-ref">Tool</code> trait（metadata/validate/run 三段式），每个工具有显式参数 schema（<code class="code-ref">geolibre_param_schemas</code>）并有单元测试强制每个工具声明全部参数 schema（<code class="code-ref">crates/geolibre-tools/src/lib.rs:96</code> <code class="code-ref">every_tool_has_explicit_param_schemas</code>）。PMTiles v3 写入器（<code class="code-ref">crates/geolibre-tools/src/pmtiles.rs</code>）实现了 Hilbert tile id、gzip 目录、去重等完整 spec 片段并有 spec 对照测试。Hilbert 排序（<code class="code-ref">crates/geolibre-tools/src/hilbert.rs</code>）用于 GeoParquet 写入的空间局部性。raster 到 Web Mercator 切片（<code class="code-ref">crates/geolibre-tools/src/raster_to_tiles.rs</code>）有 MAX_TILES=4096 安全上限防止 OOM。纯 Rust polygonize（<code class="code-ref">crates/geolibre-tools/src/polygonize.rs</code>）替代了 gdal.Polygonize 的 Python 调用，支持多边形 hole 和 RFC 7946 绕行方向。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/geolibre-wasm/src/lib.rs:151</code> <code class="code-ref">MAX_FULL_READ_BYTES</code> 常量结合 <code class="code-ref">guard_full_read</code> 在 32-bit WASM 4 GiB 限制下主动检测并优雅拒绝过大解码请求，比直接 OOM panic 好很多。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">crates/geolibre-tools/src/geoparquet_io.rs:77</code> 的 Hilbert 排序集成——write_geoparquet 默认启用空间排序+ZSTD+bbox covering，这是对 GeoParquet 生态缺位能力的填补，且用纯 Rust 在浏览器内完成。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">crates/geolibre-tools/src/raster_normalize.rs</code> 的 <code class="code-ref">load_input_raster</code> 和 <code class="code-ref">write_or_store_output</code> 与 <code class="code-ref">crates/geolibre-tools/src/common.rs</code> 中的同名函数重复实现（对比 raster_normalize.rs:113 与 common.rs:31），后续工具有使用 common.rs 的版本但 raster_normalize 自带副本，存在维护不一致风险。</p>
<p class="audit-callout audit-callout--doubt">CI（<code class="code-ref">.github/workflows/ci.yml</code>）有 <code class="code-ref">cargo test</code> 和 Node/Python smoke test，但所有自研工具的 Rust 测试（fill/dem_filter/hilbert/polygonize/regions/pmtiles）仅覆盖纯函数逻辑，没有任何工具端到端测试——即没有在测试中通过 ToolRegistry::run 完整调用一个工具并校验输出文件内容。Python 测试（<code class="code-ref">python/tests/test_smoke.py</code>）做了 GeoParquet roundtrip 但仅覆盖 exit_code 和 PAR1 magic bytes。</p>
<p>1. 将 raster_normalize.rs 的 load_input_raster/write_or_store_output 删除，统一使用 common.rs 版本，消除重复代码。
2. 为至少 extract_sinks → delineate_depressions 链条添加一个集成测试（构造小 DEM，通过 registry run，验证 CSV 列数/GeoJSON feature 数量），弥补工具层面测试空白。
3. vendor/kdtree 的 patch 是临时方案（README 已标注 TODO），建议在下一个 release 前评估上游是否已合并并移除 vendor。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>上游 whitebox-wasm 以 git 依赖引用（非发布 crate），任何上游 breaking change 会直接阻塞构建，无锁版本保护。</li><li>WebAssembly 32-bit 约 4 GiB 内存上限限制了可处理的栅格/LiDAR 规模，README 已说明但用户可能在 DEM 较大时遇到非预期失败。</li><li>项目创建仅 4 天（15 commits），维护者高度集中（Qiusheng Wu 单人），社区健康度风险显著。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 GeoLibre（QGIS/MapLibre 风格的开源 GIS 前端）提供零后端的浏览器端数据处理能力，直接嵌入 npm/PyPI 生态，面向地球科学/遥感开发者和 GIS Web 应用场景。</p>
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
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.8</span>
  </div>
</div>
</section>