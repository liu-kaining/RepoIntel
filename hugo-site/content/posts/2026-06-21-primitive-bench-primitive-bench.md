---
title: '[Score: 76.3] primitive-bench/primitive-bench'
date: '2026-06-21T03:55:27Z'
categories:
- AI Infrastructure Benchmark
tags:
- benchmark
- evaluation
- statistical-methodology
- web-search
- retrieval
- reranking
intel_score: 76.3
repo_name: primitive-bench/primitive-bench
repo_link: https://github.com/primitive-bench/primitive-bench
summary: 面向 AI 基础设施供应商（OCR/搜索/向量库等）的分层切片基准测试框架，强调统计可分性而非单一排名，适合需要证据驱动选型的工程师团队。
code_source: git
code_files_reviewed:
- packages/bench-schemas/pyproject.toml
- packages/bench-stats/pyproject.toml
- packages/eval-crawl/pyproject.toml
- packages/eval-chunking/pyproject.toml
- packages/eval-vectordb/pyproject.toml
- packages/eval-ocr/pyproject.toml
- .github/workflows/labels.yml
- .github/workflows/pr-title.yml
- .github/workflows/ci.yml
- packages/bench-adapters/src/bench_adapters/search/__init__.py
- packages/bench-adapters/src/bench_adapters/extract/__init__.py
- packages/eval-crawl/src/eval_crawl/__init__.py
- packages/eval-chunking/src/eval_chunking/__init__.py
- packages/eval-vectordb/src/eval_vectordb/__init__.py
- packages/bench-adapters/src/bench_adapters/rerank/__init__.py
- packages/eval-ocr/src/eval_ocr/__init__.py
- packages/bench-adapters/src/bench_adapters/retrieval/__init__.py
- apps/mcp/vercel.json
- packages/eval-ocr/slices.yaml
- packages/eval-crawl/slices.yaml
- packages/eval-chunking/slices.yaml
- packages/eval-vectordb/slices.yaml
- packages/bench-stats/README.md
- apps/mcp/tsconfig.json
- packages/bench-core/README.md
- packages/eval-websearch/slices.yaml
- packages/eval-reranker/slices.yaml
- packages/eval-retrieval/slices.yaml
- packages/eval-retrieval/README.md
- packages/eval-reranker/selection_manifest.json
- packages/eval-extraction/slices.yaml
- packages/eval-extraction/README.md
- apps/mcp/README.md
- apps/docs/DECISIONS.md
- packages/eval-websearch/README.md
- packages/bench-adapters/README.md
- packages/eval-retrieval/selection_manifest.json
- packages/bench-schemas/tests/test_contract.py
- packages/eval-reranker/tests/test_scoring.py
- apps/mcp/test/leaderboard.test.ts
- packages/eval-retrieval/tests/test_retrieval_scoring.py
- packages/bench-stats/tests/test_snapshot_fidelity.py
- packages/bench-stats/tests/test_reporting.py
- packages/bench-stats/tests/test_leaderboard.py
- packages/eval-reranker/tests/test_runner.py
- packages/eval-reranker/snapshots/reranker.counts.toml
- packages/eval-retrieval/snapshots/retrieval.counts.toml
code_chars_analyzed: 97834
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
      <span class="scope-stat__value">约 97,834 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">packages/bench-schemas/pyproject.toml</code></li><li><code class="path-chip">packages/bench-stats/pyproject.toml</code></li><li><code class="path-chip">packages/eval-crawl/pyproject.toml</code></li><li><code class="path-chip">packages/eval-chunking/pyproject.toml</code></li><li><code class="path-chip">packages/eval-vectordb/pyproject.toml</code></li><li><code class="path-chip">packages/eval-ocr/pyproject.toml</code></li><li><code class="path-chip">.github/workflows/labels.yml</code></li><li><code class="path-chip">.github/workflows/pr-title.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">packages/bench-adapters/src/bench_adapters/search/__init__.py</code></li><li><code class="path-chip">packages/bench-adapters/src/bench_adapters/extract/__init__.py</code></li><li><code class="path-chip">packages/eval-crawl/src/eval_crawl/__init__.py</code></li><li><code class="path-chip">packages/eval-chunking/src/eval_chunking/__init__.py</code></li><li><code class="path-chip">packages/eval-vectordb/src/eval_vectordb/__init__.py</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI 团队在选型 OCR、web search、reranker、retrieval 等基础设施组件时，只能依赖厂商自报数字或碎片化博客，缺乏统一度量、统计可分性和逐切片对比，导致决策基于传言而非证据。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用分层包架构，<code class="code-ref">packages/bench-schemas/src/bench_schemas/models.py</code>（pyproject.toml 声明 <code class="code-ref">SCHEMA_VERSION</code> 为 <code class="code-ref">0.1.0</code>）定义冻结合约（<code class="code-ref">RunManifest</code>, <code class="code-ref">ItemResult</code>, <code class="code-ref">SliceResult</code>, <code class="code-ref">ScorerOutput</code>），所有其他包仅导入此包的类型，CI 中 <code class="code-ref">.github/workflows/ci.yml:20-30</code> 有 schema contract guard 检查 <code class="code-ref">bench-schemas</code> 改动时必须 bump <code class="code-ref">SCHEMA_VERSION</code>。<code class="code-ref">bench-core</code> 提供 harness 引擎，<code class="code-ref">bench-stats</code> 提供 McNemar/Wilson/bootstrap 统计库，<code class="code-ref">bench-adapters</code> 以 <code class="code-ref">@register(&quot;name&quot;)</code> 装饰器模式自动注册厂商适配器（<code class="code-ref">packages/bench-adapters/src/bench_adapters/search/__init__.py</code>），各 <code class="code-ref">eval-*</code> 垂直包实现 <code class="code-ref">Task</code> + <code class="code-ref">Scorer</code> 子类。MCP 服务端（<code class="code-ref">apps/mcp</code>）以 <code class="code-ref">TypeScript/Next.js</code> 实现，暴露 6 个 tool（recommend/compare/get_slice_leaderboard 等），全部为确定性 JSON 查找，无 LLM 推理开销。CI 中 <code class="code-ref">.github/workflows/ci.yml:31-39</code> 还有 MCP 数据 + schema drift guard，确保 Python 侧产出的 JSON 与 TS 类型不漂移。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">packages/eval-extraction/slices.yaml</code> 中的 miss 分类设计（blocked / truncated / token_absent / empty）和 <code class="code-ref">packages/eval-extraction/README.md</code> 中 Exa 33% 的 headline 分析——98/100 misses 归因于 anti-bot blocking 而非提取能力——是统计诚实性在工程中的具体体现，直接解决了「单一数字误导」的问题。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">packages/bench-stats/tests/test_snapshot_fidelity.py</code> 从 TOML 快照反向 pin 住已发布报告的数值（如 <code class="code-ref">_point(websearch, &quot;company_lookup&quot;, &quot;exa&quot;) == pytest.approx(0.880)</code>），这是一种「citable statistic」的工程保障——快照被篡改即 CI 失败，溯源性极强。</p>
<p class="audit-callout audit-callout--doubt">OCR、VectorDB、Chunking、Crawl 四个垂直包均为 scaffold 状态（<code class="code-ref">packages/eval-ocr/src/eval_ocr/__init__.py</code> 注释写 <code class="code-ref">STATUS: scaffold. Cloned from eval-ocr</code>），<code class="code-ref">slices.yaml</code> 全为空列表（<code class="code-ref">packages/eval-ocr/slices.yaml:4</code> 的 <code class="code-ref">slices: []</code>），实际仅有 websearch、extraction、reranker、retrieval 四个垂直有真实数据。README 声称 9 个 primitive 但仅 4 个可用，覆盖度低于宣传。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">packages/bench-core/src/</code> 的核心 harness 引擎代码（run_task、RunDir、hmac_split 等实现），<code class="code-ref">packages/bench-core/README.md</code> 描述了公共 API 但源码未包含在 bundle 中，无法验证确定性种子、per-run 目录等关键工程声明的真实性。</p>
<p>对 websearch/extraction 的分层切片方法论有参考价值，但当前仅 4/9 垂直可运行。若要作为选型依据，建议先对 reranker/retrieval 的 100 条和 1271 条样本量评估统计功效（<code class="code-ref">packages/eval-reranker/selection_manifest.json</code> 的 <code class="code-ref">total_rows: 100</code> 在 McNemar 检验下功效偏弱），再决定是否采纳结论。MCP server 可直接接入 Claude Code 做 agent 可查询的选型工具，零推理成本。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 声称 9 个 primitive 但仅 4 个有真实评估数据，5 个为空 scaffold，实际覆盖面远低于宣传。</li><li>reranker 样本量仅 100 条（见 selection_manifest.json），McNemar 检验在小效应量下功效不足，置信区间宽，stat separability 判定可靠性存疑。</li><li>bench-core harness 引擎源码未包含在 bundle 中，确定性种子、hmac split 等关键工程声明无法独立验证。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>如果后续垂直逐步填充且保持 vendor-neutral，有潜力成为 AI infra 选型的 &#x27;G2/Gartner for engineers&#x27;。MCP 接口让 agent 原生查询切片级结果，是 AI-native 分发的差异化尝试。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.3</span>
  </div>
</div>
</section>