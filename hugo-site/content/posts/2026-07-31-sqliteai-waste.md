---
title: '[Score: 76.25] sqliteai/waste'
date: '2026-07-31T13:57:46Z'
categories:
- AI Inference
tags:
- MoE
- Inference Engine
- C
- Local LLM
- NVMe Streaming
- Desktop Scale
intel_score: 76.25
repo_name: sqliteai/waste
repo_link: https://github.com/sqliteai/waste
summary: 零依赖C推理引擎，通过NVMe流式加载MoE专家权重，在64GB笔记本上运行2.78T参数Kimi K3模型。
code_source: git
code_files_reviewed:
- Makefile
- .github/workflows/ci.yml
- tests/__init__.py
- serve/__init__.py
- src/crc32.h
- src/version.c
- src/kda.h
- src/tokenizer.h
- src/simd.h
- src/kda_neon.c
- src/vq.c
- src/kda.c
- src/image.c
- src/waste_backend.h
- src/threads.h
- src/simd_avx512.c
- src/simd_avx2.c
- src/crc32.c
- src/platform.h
- src/json.h
- src/ecache.h
- src/backend.c
- src/waste_format.h
- src/metal.m
- src/vision.c
- src/model.h
- src/waste.h
- src/ecache.c
- src/tokenizer.c
- src/waste.c
- examples/chat.json
- examples/chat-k3.json
- tests/test_tokenizer.c
- tests/check_budget.sh
- tests/test_vision.c
- tools/tokdiff.py
- tests/test_kda.c
- tools/kimi_tok.py
- tools/trace_hf.py
- tools/k3parts_ref.py
- tools/diskbench.c
- tests/test_k3parts.c
- examples/README.md
- tools/gen_xtml_goldens.py
- tools/kda_ref.py
- tests/range_server.py
- tests/test_state.c
code_chars_analyzed: 320534
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
      <span class="scope-stat__value">约 320,534 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">tests/__init__.py</code></li><li><code class="path-chip">serve/__init__.py</code></li><li><code class="path-chip">src/crc32.h</code></li><li><code class="path-chip">src/version.c</code></li><li><code class="path-chip">src/kda.h</code></li><li><code class="path-chip">src/tokenizer.h</code></li><li><code class="path-chip">src/simd.h</code></li><li><code class="path-chip">src/kda_neon.c</code></li><li><code class="path-chip">src/vq.c</code></li><li><code class="path-chip">src/kda.c</code></li><li><code class="path-chip">src/image.c</code></li><li><code class="path-chip">src/waste_backend.h</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>前沿MoE模型推理需要TB级内存和服务器集群，普通开发者无法在本地复现，隐私敏感数据必须信任云端。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">引擎采用分离式设计：常驻内存的trunk（注意力、路由、共享专家）通过VQ量化保持轻量；大量的路由专家权重存储在容器文件的独立bank中，采用4KiB对齐的record布局（src/waste_format.h:14）。前向传播时，每层仅读取top-k专家的record（src/ecache.h:20），通过直接I/O绕过页面缓存（src/platform.h:159）避免污染RAM。专家缓存采用频率/新近度（LFRU）策略（src/ecache.c:227），并由后台读线程异步预取（ecache.c:362）以掩盖磁盘延迟。计算核心通过运行时调度NEON/AVX2/AVX-512等SIMD后端（src/backend.c:130）。</p>
<p class="audit-callout audit-callout--highlight">专家缓存实现精密且可测量。<code class="code-ref">waste_ecache_init</code>（src/ecache.c:103）基于record大小和预算创建slot，<code class="code-ref">waste_ecache_get</code>（src/ecache.c:399）使用LFRU victim采样的open-hashing查找，恒定开销。绕过页面缓存的读写（src/platform.h:159的<code class="code-ref">waste_open_stream</code>）保证了命中率统计的真实性，避免了内核膨胀。</p>
<p class="audit-callout audit-callout--highlight">跨平台抽象层质量高。<code class="code-ref">src/platform.h</code>统一了Windows (<code class="code-ref">waste_pread</code> → <code class="code-ref">ReadFile</code>) 和POSIX的预读、对齐分配和直接I/O，每处实现仅数行，使引擎在Linux、macOS、Windows上一致编译和运行。CI配置（<code class="code-ref">.github/workflows/ci.yml:44</code>）覆盖多平台，包括cross-compile和运行测试。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src/model.c</code>。核心的模型加载、MoE前向传播（如router计算、shared expert融合、VQ解码矩阵乘法）均在model.c中实现但源码未提供。这些路径的正确性和性能边界是本引擎的关键，无法验证其工程细节。</p>
<p class="audit-callout audit-callout--doubt">SIMD kernel与Metal后端的投入产出比存疑。虽然<code class="code-ref">src/simd_avx2.c</code>和<code class="code-ref">src/simd_avx512.c</code>提供了细致的int8解包和点积加速，但README指出55%的解码时间消耗在I/O上，计算仅占27%。在此场景下，复杂的向量化可能收益有限，而代码复杂度显著增加。</p>
<p>适合作为极度隐私敏感或离线场景（如法律、医疗文档处理）的一次性分析工具，但远未达到交互式可用速度。建议使用者配备高性能NVMe和64GB+内存，并仅针对文本流使用，避免视觉模型（需额外434MB权重）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅验证过Kimi K3容器，其他MoE架构需重新适配工具链和格式。</li><li>最低RAM 64GB且要求内部NVMe，大量笔记本及台式机不满足。</li><li>0.5 tok/s只适合批处理，交互延迟不可接受，难以被大众用户采用。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为无法使用云API的机构提供在消费级硬件本地运行前沿模型的路径，可能带动本地微调、私有知识库等应用，但商业价值取决于后续工程优化将速度提升到可用水平。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.25</span>
  </div>
</div>
</section>