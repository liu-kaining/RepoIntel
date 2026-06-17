---
title: '[Score: 83.5] localai-org/privacy-filter.cpp'
date: '2026-06-17T15:20:57Z'
categories:
- PII NER Inference Engine
tags:
- GGML
- NER
- C++
- PII Redaction
- MoE
- Sliding Window Attention
intel_score: 83.5
repo_name: localai-org/privacy-filter.cpp
repo_link: https://github.com/localai-org/privacy-filter.cpp
summary: 将 OpenAI privacy-filter NER 模型用纯 C++/GGML 实现本地推理，支持 banded attention 与 MoE
  分块，对需要在无 Python 环境下做 PII 检测的团队有实际价值。
code_source: git
code_files_reviewed:
- scripts/requirements.txt
- tests/CMakeLists.txt
- CMakeLists.txt
- .github/workflows/ci.yml
- src/backend.h
- src/tokenizer.h
- src/gguf_loader.h
- src/ner.h
- src/model.h
- src/backend.cpp
- src/gguf_loader.cpp
- src/pf.cpp
- src/ner.cpp
- src/tokenizer.cpp
- src/model.cpp
- demo/traces/cpu/engines.json
- demo/traces/gpu/engines.json
- fuzz/fuzz_gguf.cpp
- include/pf.h
- CMakePresets.json
- demo/make.sh
- tests/test_loader.cpp
- scripts/requant_q8.py
- fuzz/fuzz_tokenizer.cpp
- scripts/gen_unicode.py
- demo/gen_corpus.py
- bench/gemm_microbench.cpp
- scripts/publish_hf.py
- tests/test_ner.cpp
- bench/banded_attn_proto.cpp
- model-cards/privacy-filter.md
- scripts/bench_torch.py
- scripts/compare_taps.py
- tests/test_window_stitch.cpp
- bench/pf-bench.cpp
- model-cards/privacy-filter-multilingual.md
- tests/test_parity.cpp
- docs/cpu-perf.md
- scripts/hf_tok_diff.py
- README.md
- tests/test_graph_blocks.cpp
- tests/test_tokenizer.cpp
- tools/pf-cli.cpp
- scripts/hf_dump.py
- scripts/convert.py
- demo/pii_duel.py
- demo/traces/cpu/content.json
code_chars_analyzed: 302753
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
      <span class="scope-stat__value">约 302,753 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">scripts/requirements.txt</code></li><li><code class="path-chip">tests/CMakeLists.txt</code></li><li><code class="path-chip">CMakeLists.txt</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">src/backend.h</code></li><li><code class="path-chip">src/tokenizer.h</code></li><li><code class="path-chip">src/gguf_loader.h</code></li><li><code class="path-chip">src/ner.h</code></li><li><code class="path-chip">src/model.h</code></li><li><code class="path-chip">src/backend.cpp</code></li><li><code class="path-chip">src/gguf_loader.cpp</code></li><li><code class="path-chip">src/pf.cpp</code></li><li><code class="path-chip">src/ner.cpp</code></li><li><code class="path-chip">src/tokenizer.cpp</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>医疗/金融团队在内网做 PII 脱敏时，HF Transformers 需要 Python 栈且超过 16k token 就 OOM；他们需要一个能在 CPU/GPU 上原位运行、内存恒定、输出精确字节偏移的实体识别引擎。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口为 <code class="code-ref">include/pf.h</code> 定义的扁平 C API，<code class="code-ref">pf_classify</code>（<code class="code-ref">src/pf.cpp:63</code>）串联 tokenizer → model forward → BIOES Viterbi 解码 → span 组装四步。<code class="code-ref">pf::tokenizer::encode</code>（<code class="code-ref">src/tokenizer.cpp:356</code>）先手写 o200k pre-tokenizer 正则扫描器（<code class="code-ref">pretokenize</code>，~200 行），再走 BPE 最小堆合并（<code class="code-ref">bpe_encode</code>，<code class="code-ref">src/tokenizer.cpp:248</code>），实现 O(m log m) 且无第三方依赖。模型加载经 <code class="code-ref">src/gguf_loader.cpp:82</code> 的 <code class="code-ref">model_file::open</code> 读取自定义 <code class="code-ref">openai-privacy-filter</code> arch 的全部超参，包括 YaRN rope 参数。前向图在 <code class="code-ref">src/model.cpp:130</code> 的 <code class="code-ref">model::forward</code> 构建：8 层 MoE block，每层 RMSNorm → QKV 投影 → RoPE（mode=0 交错配对，YaRN freq_factors 由 <code class="code-ref">yarn_freq_factors</code> 在加载时计算）→ attention → post_norm → MoE FFN（softmax-after-top-k 门控，<code class="code-ref">ggml_swiglu_oai</code> 带 1.702/7.0 clamp）。attention 有三条路径：flash（默认）、banded block-local（<code class="code-ref">src/model.cpp:203</code>，n≥2048 自动启用）、显式 O(n²) mask（PF_NOFLASH）。NER 解码在 <code class="code-ref">src/ner.cpp:50</code> 的 <code class="code-ref">bioes_viterbi</code> 实现约束线性链 Viterbi，每步 O(n_cls)，利用 BIOES 闭合态剪枝。滑动窗口分片在 <code class="code-ref">src/ner.cpp:108</code> 的 <code class="code-ref">make_windows</code> 实现 halo 覆盖式拼接，窗口重叠处仅取内侧行。</p>
<p class="audit-callout audit-callout--highlight">banded attention 实现（<code class="code-ref">src/model.cpp:203-275</code>）将 O(n²) mask 降为 O(n·B) 的 <code class="code-ref">[3B,B,1,nb]</code> 带状矩阵，每个 query block 只 attend 邻居 {i-1,i,i+1}，实测 Vulkan 8192 tok 从 42k 提升到 105k tok/s，且 bit-identical 通过 f32 cos≥0.99999 门。</p>
<p class="audit-callout audit-callout--highlight">工程测试覆盖极厚——<code class="code-ref">tests/test_ner.cpp</code> 对 Viterbi 约束做 6 个合成 case（含无效转移抑制、悬挂 B 拒绝），<code class="code-ref">tests/test_parity.cpp</code> 与 <code class="code-ref">tests/test_window_stitch.cpp</code> 对 HF 参考做端到端 argmax/cosine 门控，<code class="code-ref">fuzz/fuzz_tokenizer.cpp</code> 和 <code class="code-ref">fuzz/fuzz_gguf.cpp</code> 提供 libFuzzer harness，<code class="code-ref">tests/CMakeLists.txt:24</code> 将模型测试标记为可跳过（exit 77）确保快速 CI 可跑。CI（<code class="code-ref">.github/workflows/ci.yml</code>）分 tier-1 无模型 fast 和 tier-2 nightly 含 parity+fuzz smoke 两层。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/pf.cpp:87</code> 的 <code class="code-ref">pf_classify</code> 对实体做 ASCII whitespace trim 时仅检查 <code class="code-ref">&lt;= 0x20</code>，对非 ASCII 空白（如 U+00A0 non-breaking space）不做处理，多语言场景可能截断实体边界。</p>
<p class="audit-callout audit-callout--doubt">项目 4 天历史、20 commits、5 forks，维护者信息仅从 repo org <code class="code-ref">localai-org</code> 推断为 LocalAI 团队，无法从源码确认单一维护者风险；README 未提供 CONTRIBUTING 或 governance 文档。</p>
<p>如需生产部署，先用 <code class="code-ref">tests/test_parity.cpp</code> 在目标硬件上跑 parity gate（设 PF_DEVICE=vulkan 或 cuda），确认 cos≥0.9985；对长文档（&gt;32k token）建议设 PF_WINDOW=4096 默认值以控制 VRAM 在 ~2.9 GiB，或用 banded+chunk 单窗口模式换取更高吞吐。C API（<code class="code-ref">include/pf.h</code>）已设计为 FFI 友好（NULL-safe free、pf_last_error 报错），可直接从 Go/Python ctypes 调用。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>模型仅支持 openai-privacy-filter 架构，llama.cpp 需 patch PR#19725 才能加载，上游未合并前存在兼容断裂风险</li><li>quantized 变体（Q8_0）在 3k token parity 门下 cos 降至 0.9972 且有 argmax flip，尚不适合生产精度要求场景</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 LocalAI 生态的 PII 检测组件，可直接嵌入 LocalAI gRPC TokenClassify 后端，为无法部署 Python 的内网合规场景提供零依赖替代；GGUF 格式也让它能在任何支持 ggml 的推理框架中复用。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">91</div>
  <div class="score-bar"><span style="width:91%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">83.5</span>
  </div>
</div>
</section>