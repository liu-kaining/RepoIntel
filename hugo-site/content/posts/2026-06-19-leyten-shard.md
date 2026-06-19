---
title: '[Score: 75.75] leyten/shard'
date: '2026-06-19T10:22:13Z'
categories:
- Distributed LLM Inference Runtime
tags:
- pipeline-parallel
- speculative-decoding
- CUDA-graphs
- WAN-inference
- NVFP4
- MoE
intel_score: 75.75
repo_name: leyten/shard
repo_link: https://github.com/leyten/shard
summary: 将 744B 大模型按层切片分散到跨州 WAN 的消费级 GPU 上，用推测解码+异步流水线隐藏网络延迟，理论新颖但核心运行时大量 stub 未实现。
code_source: git
code_files_reviewed:
- pyproject.toml
- shard/__init__.py
- research/stage_bootstrap.sh
- phase0/setup_box.sh
- research/launch_node.sh
- research/glm_inspect.py
- research/us_bootstrap.sh
- research/vllm_bench.py
- research/glm_bootstrap.sh
- research/patch_vllm_dense.py
- shard/node.py
- research/test_kv.py
- shard/specdec.py
- research/glm_draft_compat.py
- research/treeverify_probe.py
- research/glm_fastverify_probe.py
- phase0/get_model.py
- research/glm_wan_probe.py
- shard/transport.py
- phase0/node_fetch.py
- shard/scheduler.py
- research/glm_correctness.py
- research/glm_cg_fwdcmp.py
- research/bench_fused_moe.py
- research/probe_cudagraph.py
- research/glm_draft_bench.py
- research/glm_draft_rollback.py
- research/glm_probe_quantfloor.py
- phase0/specbench.py
- research/test_cutlass.py
- research/glm_cg_rollback.py
- phase0/bench.py
- research/draft_server.py
- research/glm_nvfp4_moe.py
- docs/receipts/gpt-oss-120b-wan-20260619.json
- phase0/proof_receipt.py
- research/glm_nvfp4_check.py
- phase0/tree.py
- phase0/node.py
- phase0/mesh.py
- research/glm_swarm_nvfp4_draft.py
- research/fastverify_graph.py
- docs/PROOF.md
- docs/receipts/glm52-nvfp4-wan-20260618.json
- research/glm_swarm_nvfp4_ngram_pipe.py
- research/glm_probe_dense.py
- research/glm_probe_realconfig.py
- research/glm_probe_fastverify.py
code_chars_analyzed: 147886
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
      <span class="scope-stat__value">约 147,886 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">shard/__init__.py</code></li><li><code class="path-chip">research/stage_bootstrap.sh</code></li><li><code class="path-chip">phase0/setup_box.sh</code></li><li><code class="path-chip">research/launch_node.sh</code></li><li><code class="path-chip">research/glm_inspect.py</code></li><li><code class="path-chip">research/us_bootstrap.sh</code></li><li><code class="path-chip">research/vllm_bench.py</code></li><li><code class="path-chip">research/glm_bootstrap.sh</code></li><li><code class="path-chip">research/patch_vllm_dense.py</code></li><li><code class="path-chip">shard/node.py</code></li><li><code class="path-chip">research/test_kv.py</code></li><li><code class="path-chip">shard/specdec.py</code></li><li><code class="path-chip">research/glm_draft_compat.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>单卡装不下 744B/120B 级模型时，团队要么租多卡服务器（贵），要么放弃；想利用散布各处的闲置消费卡拼出推理能力，但现有分布式框架（vLLM tensor-parallel、DeepSpeed）假定 co-located 高速互联，无法直接跨公网工作。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">coordinator 发起 embedding → 通过 TCP 将激活张量逐 stage 传递 → 每个 stage 仅加载自己的层块做 forward → 尾节点将结果回传 coordinator 做 lm_head + greedy 采样。推测解码协调器先用小 draft（GLM-4-9B）提出 K 个 token，分布式 744B 一次 verify 全部，accept 最长匹配前缀。异步流水线允许多个 verify chunk 同时 in-flight，WAN 延迟降到循环的 ~5%。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">research/glm_swarm_nvfp4_cg.py</code>（receipt 记录的 engine 文件，<code class="code-ref">docs/receipts/glm52-nvfp4-wan-20260618.json</code> 确认 engine_sha256）将 GLM-4-9B draft 用 CUDA graph 捕获，从 49.7→13.1 ms/tok，通过静态地址 position tensor 驱动 KV cache 写入位置，保证 graph replay 与 eager 路径 byte-identical（lossless-optimization check 通过）。<code class="code-ref">research/glm_cg_rollback.py:47</code> 的 <code class="code-ref">cg_causal_mask</code> 利用 position_ids 构建因果掩码而非依赖 max-written-length，使 rollback 后 cache_position 回退时掩码和 RoPE 仍正确，且 CUDA-graph-safe。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">docs/PROOF.md</code> + <code class="code-ref">phase0/proof_receipt.py</code> 设计了一套可验证的运行收据系统，记录节点公共 IP/GPU UUID/地理/WAN RTT/output token hash，<code class="code-ref">proof_receipt.py:68</code> 的 verify 函数实现 4 项独立检查（distinct IPs、WAN-scale RTT、hash 完整性、reference match），让第三方可独立复验分布式声明。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">shard/node.py:28</code> 的 <code class="code-ref">load_shard</code>、<code class="code-ref">shard/transport.py:25</code> 的 <code class="code-ref">ActivationCodec.encode/decode</code>、<code class="code-ref">shard/transport.py:34</code> 的 <code class="code-ref">Edge.connect/send/recv</code>、<code class="code-ref">shard/specdec.py:22</code> 的 <code class="code-ref">DraftModel.propose</code>、<code class="code-ref">shard/scheduler.py:37</code> 的 <code class="code-ref">allocate</code> 等核心接口全部 <code class="code-ref">raise NotImplementedError</code>。真正能跑的推理链路全部在 <code class="code-ref">research/</code> 目录下以脚本形式存在（<code class="code-ref">glm_swarm_nvfp4_draft.py</code>、<code class="code-ref">glm_swarm_nvfp4_kv.py</code> 等），但这些脚本文件**未包含在本次 code_bundle 中**（bundle 仅含 48 个文件，110 个 tree 文件中 62 个缺失）。<code class="code-ref">shard/__init__.py:7</code> 注释明确说「nothing here serves yet; these are the interface stubs」。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">shard/node.py</code> 和 <code class="code-ref">shard/transport.py</code> 的 stub 没有任何错误处理、重连、超时逻辑；<code class="code-ref">phase0/wire.py</code> 虽在多处被 import（<code class="code-ref">phase0/node.py:11</code>、<code class="code-ref">research/draft_server.py:18</code>），但其源码**未在 bundle 中出现**——这意味着我们无法审计传输层的加密/认证实现。<code class="code-ref">shard/topology.py</code> 被 <code class="code-ref">shard/scheduler.py:52</code> import 但同样未审阅到。</p>
<p>该仓库目前是「研究实验室 → 工程产品」的过渡态。<code class="code-ref">research/</code> 下有大量深度 de-risk 探针（CUDA graph 可行性、NVFP4 MoE 正确性、KV cache rollback 正确性、量化 floor 测量），方向扎实；但 <code class="code-ref">shard/</code> 包内全是 interface stub，要变成可 pip install 的引擎还有大量集成工作。transport 层从 TCP 到 QUIC 的升级计划（<code class="code-ref">shard/transport.py</code> 注释提到 aioquic→quinn）是正确的方向，但当前连 phase 0 的 wire 安全层都未被 bundle 提供。建议优先将 <code class="code-ref">research/</code> 中已验证的快速路径（KV-cached stage + CUDA-graph verify + spec-decode coordinator）下沉到 <code class="code-ref">shard/</code> 核心，并补充集成测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心运行时（shard/）全是 NotImplementedError stub，真正可跑代码在 research/ 脚本中，bundle 中部分关键文件缺失</li><li>transport 层 wire.py 和 topology.py 源码未提供，无法验证加密/路由算法的正确性</li><li>Fork/Star=10.9% 但仅 3 天历史、12 fork、单一维护者，社区几乎不存在</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若引擎集成完成，对需要在消费级/边缘设备上运行超大模型的团队（AI 创业公司、研究机构）有吸引力；但当前代码状态距离可产品化有显著距离，且 c0mpute.ai 的商业模式（托管编排 vs 开源自建）尚不明确。</p>
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
  <div class="score-item__value">87</div>
  <div class="score-bar"><span style="width:87%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">55</div>
  <div class="score-bar"><span style="width:55%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.75</span>
  </div>
</div>
</section>