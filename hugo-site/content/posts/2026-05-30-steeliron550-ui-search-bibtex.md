---
title: '[Score: 76.05] steeliron550-ui/search-bibtex'
date: '2026-05-30T16:03:03Z'
categories:
- 学术文献检索CLI工具
tags:
- TypeScript
- CLI
- BibTeX
- 学术工具
- PDF解析
- 多源检索
intel_score: 76.05
repo_name: steeliron550-ui/search-bibtex
repo_link: https://github.com/steeliron550-ui/search-bibtex
summary: 面向CS学术写作场景的CLI工具，从PDF/标题多源检索BibTeX元数据并交叉排序，适合需要批量校验引用真实性的研究者。
code_source: git
code_files_reviewed:
- package.json
- Makefile
- .github/workflows/build-binaries.yml
- .github/workflows/release.yml
- src/index.ts
- src/pdf-parse-lib.d.ts
- src/main.ts
- src/source.ts
- src/http.ts
- src/pdf.ts
- src/download.ts
- src/types.ts
- src/ranking.ts
- src/custom-source.ts
- src/bibtex.ts
- src/metadata.ts
- src/selection.ts
- src/bibtex-file.ts
- src/config.ts
- src/search.ts
- src/cli.ts
- pnpm-workspace.yaml
- tsconfig.scripts.json
- vitest.config.ts
- agents/openai.yaml
- CHANGELOG.zh-CN.md
- CHANGELOG.md
- tsconfig.json
- tests/bibtex.test.ts
- zotero-plugin/manifest.json
- RELEASING.zh-CN.md
- RELEASING.md
- CONTRIBUTING.zh-CN.md
- CONTRIBUTING.md
- docs/TESTING.zh-CN.md
- docs/TESTING.md
- scripts/e2e-pdfs.ts
- tests/metadata.test.ts
- tests/config.test.ts
- SKILL.md
- zotero-plugin/prefs.js
- zotero-plugin/bootstrap.js
- docs/ARCHITECTURE.zh-CN.md
- docs/CONFIGURATION.zh-CN.md
- docs/CONFIGURATION.md
- docs/ARCHITECTURE.md
- scripts/build-binaries.ts
- tests/selection.test.ts
code_chars_analyzed: 234933
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
      <span class="scope-stat__value">约 234,933 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/workflows/build-binaries.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/index.ts</code></li><li><code class="path-chip">src/pdf-parse-lib.d.ts</code></li><li><code class="path-chip">src/main.ts</code></li><li><code class="path-chip">src/source.ts</code></li><li><code class="path-chip">src/http.ts</code></li><li><code class="path-chip">src/pdf.ts</code></li><li><code class="path-chip">src/download.ts</code></li><li><code class="path-chip">src/types.ts</code></li><li><code class="path-chip">src/ranking.ts</code></li><li><code class="path-chip">src/custom-source.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>学术写作中LLM幻觉引用频发，作者逐条在DBLP/arXiv/Crossref间手动检索、复制、修正BibTeX格式，成本高且易出错——尤其当论文引用数十上百篇时。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口 <code class="code-ref">src/main.ts</code> 将控制权交给 <code class="code-ref">src/cli.ts:main()</code>，Commander 注册 metadata/search/select/update/search-title 五条子命令。核心搜索链路为 <code class="code-ref">searchBibtexFromPdf</code> → <code class="code-ref">extractPdfDocumentSnapshot</code>（<code class="code-ref">src/pdf.ts</code>）→ <code class="code-ref">buildMetadataCandidate</code>（<code class="code-ref">src/metadata.ts</code>）→ <code class="code-ref">searchBibtex</code>（<code class="code-ref">src/search.ts</code>）→ <code class="code-ref">rankBibliographicCandidates</code>（<code class="code-ref">src/ranking.ts</code>）→ <code class="code-ref">fetchBibtexForRecord</code>（<code class="code-ref">src/bibtex.ts</code>）。多源并行调度由 <code class="code-ref">searchBibtexParallel</code>（<code class="code-ref">src/search.ts</code>）完成，每个来源用独立 <code class="code-ref">AbortController</code> 做超时控制。错误不吞没，统一汇聚到 <code class="code-ref">SearchResponse.sourceErrors</code>（<code class="code-ref">src/types.ts</code>）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/custom-source.ts</code> 实现了声明式 HTTP-JSON 自定义来源适配器，用户在 <code class="code-ref">config.toml</code> 用 URL 模板 + JSON 路径映射即可接入任意学术 API，无需修改源码；路径读取函数 <code class="code-ref">readPath</code> 支持嵌套对象和数组展开（<code class="code-ref">src/custom-source.ts:142-163</code>）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/selection.ts</code> 将交互选择器设计为纯函数状态机（<code class="code-ref">updateSelectionState</code> + <code class="code-ref">SelectionEvent</code> 联合类型），可完全脱离 TTY 做单元测试（<code class="code-ref">tests/selection.test.ts</code>）；同时 <code class="code-ref">renderSelection</code> 支持过滤、预览模式切换、剪贴板复制，Vim 键位映射完整（<code class="code-ref">src/selection.ts:keypressToSelectionEvent</code>）。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/pdf.ts:installPdfParseLoaderPatch</code> 在每次调用 <code class="code-ref">extractPdfDocumentSnapshot</code> 时动态 Monkey-patch Node.js 模块加载器以绕过 pdf-parse 的 Buffer 兼容问题——此方案脆弱，依赖 Node 内部 <code class="code-ref">_extensions</code> API，未来 Node 版本升级或 ESM-only 环境下可能失效，且 patch 用正则替换 <code class="code-ref">.js</code> 源码（<code class="code-ref">src/pdf.ts:61-76</code>），误匹配风险不可忽略。</p>
<p class="audit-callout audit-callout--doubt">排序模块 <code class="code-ref">src/ranking.ts</code> 的 <code class="code-ref">textSimilarity</code> 使用 Jaccard + Levenshtein 混合评分，但 Levenshtein 对长标题（&gt;200字符）的时间复杂度为 O(n²)，当 <code class="code-ref">--limit</code> 较大且候选数多时可能成为瓶颈；未见对输入长度做截断保护（<code class="code-ref">src/ranking.ts:51-60</code>）。</p>
<p>PDF 解析层建议替换为更稳定的方案（如 pdfjs-dist 的 Node 绑定），避免 monkey-patch；排序层对长标题做前 N 个 token 截断或用 Jaro-Winkler 替代 Levenshtein；测试覆盖当前仅 <code class="code-ref">tests/bibtex.test.ts</code> 有 1 个 case，建议补充 <code class="code-ref">search.test.ts</code>、<code class="code-ref">bibtex-file.test.ts</code>、<code class="code-ref">config.test.ts</code> 的实际内容（文档声称存在但 code_bundle 中仅 <code class="code-ref">bibtex.test.ts</code>、<code class="code-ref">metadata.test.ts</code>、<code class="code-ref">selection.test.ts</code>、<code class="code-ref">config.test.ts</code> 可见）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>Fork/Star 比仅 3.4%，118 star 但仅 4 fork，社区参与度极低，健康存疑</li><li>项目仅 1 天、4 次 commit，几乎所有测试文件在 code_bundle 中仅 1-2 个 case，远未达到生产可靠性</li><li>Zotero 插件和 OpenAI agent manifest 仅为骨架代码，无实际运行时逻辑，README 描述的「多智能体协同」名不副实</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对CS领域研究者和学术写作团队有明确实用价值，可嵌入CI做引用质量门禁；Zotero插件骨架（<code class="code-ref">zotero-plugin/</code>）暗示桌面集成方向，但当前仅为 manifest + bootstrap 空壳，尚未实现搜索逻辑。</p>
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
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.05</span>
  </div>
</div>
</section>