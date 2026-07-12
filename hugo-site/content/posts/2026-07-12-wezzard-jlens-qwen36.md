---
title: '[Score: 80.8] WeZZard/jlens-qwen36'
date: '2026-07-12T02:29:16Z'
categories:
- AI Interpretability / Developer Tools
tags:
- Jacobian lens
- MLX
- Metal kernel
- Qwen3.6
- LLM debugging
intel_score: 80.8
repo_name: WeZZard/jlens-qwen36
repo_link: https://github.com/WeZZard/jlens-qwen36
summary: 本地运行的 Jacobian lens 可视化调试器，针对苹果芯片 4-bit Qwen3.6-27B，通过拟合每层 Jacobian 矩阵揭示模型潜在概念轨迹，而非仅输出
  token。
code_source: git
code_files_reviewed:
- pyproject.toml
- docs/perf/fit-03.md
- jlens_qwen/perf.py
- docs/perf/fit-02.md
- docs/perf/decode-05.md
- docs/perf/fit-01.md
- docs/perf/decode-03.md
- docs/perf/ui-01.md
- docs/perf/decode-02.md
- docs/perf/decode-04.md
- docs/perf/fit-05.md
- tests/test_chain_indexing.py
- tests/test_lens_resolution.py
- docs/perf/decode-01.md
- docs/perf/ui-02.md
- docs/perf/README.md
- docs/perf/fit-04.md
- sitecustomize.py
- scripts/intervention_sanity.py
- scripts/verify_analytic_layer.py
- docs/lenses.md
- README.md
- scripts/run_fit.py
- scripts/smoke_model.py
- jlens_qwen/patch_gdn.py
- jlens_qwen/analytic.py
- scripts/workspace_range.py
- scripts/run_experiments.py
- jlens_qwen/custom_gdn_patch.py
- scripts/gen_decode_gate_golden.py
- jlens_qwen/prompts.py
- scripts/bench_decode.py
- jlens_qwen/fit_analytic.py
- jlens_qwen/lens.py
- jlens_qwen/interventions.py
- jlens_qwen/probing.py
- scripts/measure_gbeta_gap.py
- scripts/spike_jacobian_v2.py
- scripts/export_static.py
- jlens_qwen/fit.py
- tests/test_decode_gate.py
- jlens_qwen/gdn_backward.py
- tests/test_analytic_attention.py
- scripts/spike_jacobian.py
- jlens_qwen/analytic_attn.py
- jlens_qwen/custom_gdn_vjp.py
- jlens_qwen/model.py
code_chars_analyzed: 257193
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
      <span class="scope-stat__value">约 257,193 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">docs/perf/fit-03.md</code></li><li><code class="path-chip">jlens_qwen/perf.py</code></li><li><code class="path-chip">docs/perf/fit-02.md</code></li><li><code class="path-chip">docs/perf/decode-05.md</code></li><li><code class="path-chip">docs/perf/fit-01.md</code></li><li><code class="path-chip">docs/perf/decode-03.md</code></li><li><code class="path-chip">docs/perf/ui-01.md</code></li><li><code class="path-chip">docs/perf/decode-02.md</code></li><li><code class="path-chip">docs/perf/decode-04.md</code></li><li><code class="path-chip">docs/perf/fit-05.md</code></li><li><code class="path-chip">tests/test_chain_indexing.py</code></li><li><code class="path-chip">tests/test_lens_resolution.py</code></li><li><code class="path-chip">docs/perf/decode-01.md</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>LLM 可解释性研究依赖 CUDA/远程 GPU，苹果用户缺乏本地调试工具；Anthropic 的 Jacobian lens 实现为 PyTorch，无法在 MLX 上高效运行，自定义 Metal 内核填补了此缺口。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目含模型适配、透镜拟合、推理读数和 Web 前端。<code class="code-ref">jlens_qwen/model.py</code> 封装 MLX 模型，提供 forward/forward_with_intervention 等接口；透镜通过链式乘法拟合：先计算每层 Jacobian M_ℓ（<code class="code-ref">jlens_qwen/fit.py</code> 逐 dim VJP 或 <code class="code-ref">jlens_qwen/fit_analytic.py</code> 解析装配），再反向链乘得到 J_ℓ。自定义 Metal GDN 反向 kernel（<code class="code-ref">jlens_qwen/custom_gdn_vjp.py</code>）解决了 MLX 融合核无 VJP 的问题；解析注意力/MLP 分支（<code class="code-ref">jlens_qwen/analytic_attn.py</code> 及 mlp_branch_jacobian）通过 Hadamard 技巧避免逐维 VJP，大幅加速。读取阶段（未审阅到 serve.py，推断为语言模型的源码中未出现）将残差经 J_ℓ 运输后 unembed 得 token 分数。</p>
<p class="audit-callout audit-callout--highlight">Metal GDN 反向 kernel（<code class="code-ref">jlens_qwen/custom_gdn_vjp.py</code>）实现了片上 BPTT，并扩展支持 dg/dbeta 路径（return_gbeta=True），与 ops 实现验证误差 ~3e-7（<code class="code-ref">tests/test_analytic_attention.py</code> 之 test_gdn_kernel_path_matches_ops），使得完整全深度拟合在 M4 Pro 仅需 2.75 小时（<code class="code-ref">docs/perf/fit-05.md</code>）。</p>
<p class="audit-callout audit-callout--highlight">解析注意力分支 Jacobian（<code class="code-ref">jlens_qwen/analytic_attn.py</code> 的 _fa_branch/_gdn_branch）利用种子余切与输入投影一次性收缩，将 MLP 分支加速 77 倍（<code class="code-ref">docs/perf/fit-02.md</code>），注意力分支加速 13-32 倍（<code class="code-ref">docs/perf/fit-04.md</code>），同时经合成全层对比验证误差在 1e-2 水平（test_full_layer_junction_error）。</p>
<p class="audit-callout audit-callout--doubt">未提供 serve.py 源码，无法审查服务端并发处理、SSE 流式推送及错误恢复逻辑；test_lens_resolution.py 仅测透镜选择逻辑，解码门正确性测试（<code class="code-ref">tests/test_decode_gate.py</code>）依赖已存在的 golden 数据，表明服务端健壮性存疑。</p>
<p class="audit-callout audit-callout--doubt">预装透镜仅用 20 个 prompt 拟合，文档自陈“noisy”，因果干预需概念依赖；若要研究级质量，需用户自行拟合 100+ prompt，耗时数小时且需大内存，实用性门槛较高。</p>
<p>研究用途直接加载 Neuronpedia n=1000 透镜获取更可靠读数；工程部署前补充 serve.py 的静态分析并提供压力测试，评估并发 token 生成稳定性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 Apple MLX 和 qwen3_5 架构，跨平台/多模型无法复用</li><li>预装透镜 prompt 数仅 20，噪声高；用户需自拟合，成本 2.75h/M4 Pro</li><li>服务端源码未审查，生产稳定性与异常处理未知</li><li>依赖未维护的 mlx-lm 版本（0.31.3）及自定义 Metal 核，MLX 升级可能导致不可用</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>商业价值有限，定位科研与可解释性调试工具，但填补了苹果生态 Jacobian lens 空白，若集成到 MLX 生态或企业合规审计场景可能产生黏性。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
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
    <span class="total-score-banner__value">80.8</span>
  </div>
</div>
</section>