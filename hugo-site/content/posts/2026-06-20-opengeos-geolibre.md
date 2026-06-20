---
title: '[Score: 78.7] opengeos/GeoLibre'
date: '2026-06-20T08:51:31Z'
categories:
- Cloud-Native GIS Platform
tags:
- geospatial
- MapLibre
- DuckDB-WASM
- Tauri
- React
- offline-capable
intel_score: 78.7
repo_name: opengeos/GeoLibre
repo_link: https://github.com/opengeos/GeoLibre
summary: 基于 MapLibre + DuckDB-WASM + Tauri 的跨平台 GIS 应用，支持浏览器/桌面/Android 同一工作区，适合需要在本地离线分析矢量/栅格数据的地理信息从业者。
code_source: git
code_files_reviewed:
- workers/viewer/package.json
- workers/collab/package.json
- packages/core/package.json
- apps/geolibre-desktop/jupyterlite/requirements.txt
- packages/map/package.json
- packages/processing/package.json
- .github/workflows/deploy-viewer.yml
- .github/workflows/deploy-collab.yml
- .github/workflows/claude.yml
- .github/workflows/publish-container.yml
- backend/geolibre_server/geolibre_server/__init__.py
- apps/geolibre-desktop/src-tauri/src/main.rs
- packages/map/src/index.ts
- python/src/geolibre/__init__.py
- packages/ui/src/index.ts
- workers/viewer/src/index.ts
- packages/core/src/index.ts
- packages/processing/src/index.ts
- packages/core/tsconfig.json
- packages/map/tsconfig.json
- packages/processing/tsconfig.json
- packages/ui/tsconfig.json
- apps/geolibre-desktop/postcss.config.js
- packages/plugins/tsconfig.json
- apps/geolibre-desktop/tsconfig.json
- apps/geolibre-desktop/tsconfig.node.json
- apps/geolibre-desktop/tailwind.config.js
- apps/geolibre-desktop/vite.config.ts
- python/tests/test_extension.py
- python/tests/test_extension_routes.py
- python/tests/test_color_ramp.py
- backend/geolibre_server/tests/test_sql.py
- python/tests/test_server.py
- backend/geolibre_server/tests/test_vector.py
- backend/geolibre_server/tests/test_whitebox_arguments.py
- backend/geolibre_server/tests/test_vector_golden.py
- apps/geolibre-desktop/src-tauri/build.rs
- apps/geolibre-desktop/jupyterlite/jupyter-lite.json
- apps/geolibre-desktop/jupyterlite/jupyter_lite_config.json
- apps/geolibre-desktop/src-tauri/tauri.android.conf.json
- packages/plugins/src/earthengine.d.ts
- packages/plugins/src/arcgis-maplibre.d.ts
- apps/geolibre-desktop/src/App.tsx
- apps/geolibre-desktop/src-tauri/tauri.conf.json
- packages/map/src/placeholders.ts
- apps/geolibre-desktop/src/vite-env.d.ts
- packages/processing/src/registry.ts
code_chars_analyzed: 103754
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
      <span class="scope-stat__value">47 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 103,754 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">workers/viewer/package.json</code></li><li><code class="path-chip">workers/collab/package.json</code></li><li><code class="path-chip">packages/core/package.json</code></li><li><code class="path-chip">apps/geolibre-desktop/jupyterlite/requirements.txt</code></li><li><code class="path-chip">packages/map/package.json</code></li><li><code class="path-chip">packages/processing/package.json</code></li><li><code class="path-chip">.github/workflows/deploy-viewer.yml</code></li><li><code class="path-chip">.github/workflows/deploy-collab.yml</code></li><li><code class="path-chip">.github/workflows/claude.yml</code></li><li><code class="path-chip">.github/workflows/publish-container.yml</code></li><li><code class="path-chip">backend/geolibre_server/geolibre_server/__init__.py</code></li><li><code class="path-chip">apps/geolibre-desktop/src-tauri/src/main.rs</code></li><li><code class="path-chip">packages/map/src/index.ts</code></li><li><code class="path-chip">python/src/geolibre/__init__.py</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>GIS 分析师常需在不同设备（桌面 QGIS、浏览器查看器、移动端采集）间切换工具链，导入 GeoParquet/FlatGeobuf/COG 等云原生格式时仍依赖服务器端 GDAL；GeoLibre 将 DuckDB-WASM Spatial + MapLibre 整合到纯前端，消除后端依赖并提供 PWA 离线能力。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 monorepo 结构，核心分为 <code class="code-ref">packages/core</code>（Zustand store + 类型）、<code class="code-ref">packages/map</code>（MapLibre 封装）、<code class="code-ref">packages/processing</code>（Turf.js + geolibre-wasm 空间处理）、<code class="code-ref">packages/ui</code>（Radix UI 组件）和 <code class="code-ref">apps/geolibre-desktop</code>（Tauri v2 壳）。状态管理在 <code class="code-ref">packages/core/src/index.ts:42</code> 导出的 <code class="code-ref">useAppStore</code> 基于 zustand + zundo 实现 undo/redo；地图渲染通过 <code class="code-ref">packages/map/src/MapCanvas</code> 依赖 MapLibre GL JS，geojson-loader 负责矢量瓦片化。构建链在 <code class="code-ref">apps/geolibre-desktop/vite.config.ts</code> 中通过 <code class="code-ref">manualChunks</code> 函数（约第 180 行）将 DuckDB-WASM、PGlite、CereusDB 等重量级二进制拆为独立 lazy chunk，避免进入 boot graph；CDN 加载策略通过 <code class="code-ref">pgliteCdnUrl()</code> 等函数动态解析 lockfile 版本拼接 jsDelivr URL。后端 sidecar 为 Python FastAPI，处理 Sedona SQL（<code class="code-ref">backend/geolibre_server/geolibre_server/app/sql.py</code>）和 geopandas 矢量工具（<code class="code-ref">backend/geolibre_server/geolibre_server/app/vector.py</code>）。PWA 离线策略由 <code class="code-ref">pwaPlugin()</code> 实现，Workbox CacheFirst 分三层：app shell precache、哈希命名的重型 assets、CDN 引擎缓存。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">vite.config.ts</code> 中 <code class="code-ref">manualChunks</code> 对 CSS 资产的显式过滤（第 185 行附近注释说明「CSS 会把 DuckDB 等拖入 boot graph 导致 PWA 冷启动失败」）以及 <code class="code-ref">cereusCdnLoaderPlugin</code> 通过 AST 替换阻止 40MB wasm 被 Vite 静态 emit，体现对构建产物体积的精细控制。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">backend/geolibre_server/tests/test_vector_golden.py</code> 与 TS 侧共享同一套 <code class="code-ref">tests/fixtures/vector/cases</code> golden fixture，用容差匹配器保证 Python/geopandas 与 <code class="code-ref">TS/Turf.js</code> 双引擎输出一致——这种跨语言合约测试在 GIS 工具中少见。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">packages/core/src/index.ts</code> 导出的 <code class="code-ref">useAppStore</code> 使用 zustand + zundo，但未审阅到 store 内部如何处理并发写入（如协作编辑时），<code class="code-ref">DEFAULT_COLLABORATION_STATE</code> 仅被导出定义不详，<code class="code-ref">workers/collab</code> 仅见 <code class="code-ref">package.json</code> 无源码，协作层完整性无法验证。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">vite.config.ts</code> 中 WMS/WFS/GPX proxy 中间件直接将用户可控的 <code class="code-ref">url</code> 参数传给 <code class="code-ref">fetch()</code>（约第 280 行 <code class="code-ref">proxyBinaryRequest</code>），未见对目标 URL 的域名白名单或 SSRF 防护；虽为 dev server 专用，但 <code class="code-ref">configureServer</code> 可能被部署为内网服务时成为风险点。</p>
<p>若计划在生产环境部署 Web 版，需为 proxy 中间件补充 URL 白名单；前端 store 的协作层需审阅 <code class="code-ref">workers/collab</code> 源码确认 WebSocket relay 的幂等性和断线重连策略；DuckDB-WASM 的 32MB 二进制仍是首次加载瓶颈，建议评估是否可将 spatial extension 也走 CDN lazy load。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>workers/collab 源码未提供，协作功能的可靠性无法独立验证。</li><li>proxy 中间件（WMS/WFS/GPX）未见 SSRF 防护，部署于内网时可能被利用访问内部服务。</li><li>DuckDB-WASM + spatial extension 约 32MB 首次加载，弱网环境下体感较差，README 未说明最低带宽需求。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向 GIS 从业者和数据科学家的免费开源替代方案，可替代部分 QGIS Web Client / Kepl.gl 场景；PyPI + conda-forge 分发 + Jupyter widget 集成降低了学术和数据团队的试用门槛，具备成为轻量级云原生 GIS 基础设施的潜力。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.7</span>
  </div>
</div>
</section>