---
title: '[Score: 79.65] slvDev/esp32-ai'
date: '2026-07-24T16:31:45Z'
categories:
- Edge AI
tags:
- TinyML
- ESP32
- Per-Layer Embeddings
- Quantization
- On-device Inference
intel_score: 79.65
repo_name: slvDev/esp32-ai
repo_link: https://github.com/slvDev/esp32-ai
summary: 在 $8 的 ESP32-S3 微控制器上运行 28.9M 参数 LLM，通过 Per-Layer Embeddings 将 25M 参数存于 flash
  并按需读取，实现 9.5 tok/s 本地故事生成。
code_source: git
code_files_reviewed:
- pyproject.toml
- src/sample.py
- src/gen_assets.py
- src/analyze.py
- src/budget.py
- src/quantize.py
- src/train.py
- src/export.py
- src/model.py
- experiments/run_seed1.sh
- experiments/run_ablation.sh
- experiments/deploy_seed1.sh
- experiments/run_ple_dim_sweep.sh
- experiments/clean_confirm.sh
- firmware/esp32_llm/README.md
- firmware/host_verify/ppl.c
- experiments/overnight.sh
- firmware/host_verify/verify.c
- data/prepare.py
- README.md
- firmware/esp32_llm/display.h
- RESULTS.md
- firmware/common/llm.h
code_chars_analyzed: 97775
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
      <span class="scope-stat__value">23 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 97,775 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">src/sample.py</code></li><li><code class="path-chip">src/gen_assets.py</code></li><li><code class="path-chip">src/analyze.py</code></li><li><code class="path-chip">src/budget.py</code></li><li><code class="path-chip">src/quantize.py</code></li><li><code class="path-chip">src/train.py</code></li><li><code class="path-chip">src/export.py</code></li><li><code class="path-chip">src/model.py</code></li><li><code class="path-chip">experiments/run_seed1.sh</code></li><li><code class="path-chip">experiments/run_ablation.sh</code></li><li><code class="path-chip">experiments/deploy_seed1.sh</code></li><li><code class="path-chip">experiments/run_ple_dim_sweep.sh</code></li><li><code class="path-chip">experiments/clean_confirm.sh</code></li><li class="path-more">另有 9 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>物联网设备因内存极小难以运行大模型，必须依赖网络，带来延迟、隐私风险和成本；本项目利用 flash 与 SRAM 的分层存储将大模型本地化，摆脱对服务器的依赖。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">训练管道在 <code class="code-ref">src/train.py</code> 中实现，支持多种架构臂（见 <code class="code-ref">src/model.py</code> 的 Config.arm）。模型通过 <code class="code-ref">src/model.py</code> 的 TinyLM 类定义，核心为 6 层 Transformer，配合 Per-Layer Embedding 输入（<code class="code-ref">src/model.py:341</code>-350 构建 ple 向量）。训练完成后，<code class="code-ref">src/export.py</code> 将模型量化为 int4 组量化格式，并按固定顺序导出为二进制文件 model.bin，同时生成 golden logits。C 推理引擎固件位于 firmware/common/llm.h，llm_load 解析二进制头并绑定张量（llm.h:270-295），llm_forward 执行单 token 前向传播，支持 int8 激活路径（llm.h:328-347 的 matvec_q8_range）。验证工具 firmware/host_verify/verify.c 加载模型并比较 C 与 PyTorch 的输出，逐 logit 检查以确保数值一致性。</p>
<p class="audit-callout audit-callout--highlight">创新的内存分层架构。<code class="code-ref">src/model.py</code> 中 ple 臂使用 ple_table（第 326 行）存储 25M 查找表于 flash，每 token 仅读取 6 行（约 450 字节），混合投影后注入各 Transformer 层。消融实验脚本 experiments/run_ablation.sh 和 analyze.py 证实了 per-layer 注入的价值，优于 fatembed 和 ple_notable。</p>
<p class="audit-callout audit-callout--highlight">完善的部署验证链。<code class="code-ref">src/export.py</code> (行 85-107) 生成模型二进制与 golden 输出；firmware/host_verify/verify.c 加载模型并逐 token 推理，将最后位置 logits 与 golden 对比，max abs diff &lt;0.02 判定通过（verify.c:69-75），确保 C 端口与 PyTorch 完全对齐；ppl.c 更提供了全验证集困惑度计算，便于衡量量化影响。</p>
<p class="audit-callout audit-callout--doubt">测试依赖手动，缺少自动化。code_bundle 中无 tests/ 目录，所有验证均由 verify.c、ppl.c 等手动运行，训练、量化、导出等模块缺少单元测试，代码回归风险高。</p>
<p class="audit-callout audit-callout--doubt">ESP32 平台固件不完整。code_bundle 仅提供 display.h 和 llm.h，缺少 Arduino 主 sketch（.ino），设备端 token 生成循环和解码逻辑无法审查，编译烧录依赖 README 描述，部署透明度不足。</p>
<p>将 PLE 技术封装为可复用的边缘 LLM 运行时库，并扩展支持其他微控制器；工程上加入 pytest 单元测试、CI 工作流，并补充固件主程序源码，以提升可靠性和可维护性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 TinyStories 领域，故事生成能力有限，对复杂指令、对话等场景无效。</li><li>项目极新（1 天），无许可证和贡献指南，长期维护不确定性高。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>项目展示了在超低成本硬件上本地运行 LLM 的可行性，可推动智能家居、离线语音助手、隐私敏感终端等场景发展；但当前功能局限于故事生成，距离产品化仍需扩展领域和交互能力。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
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
    <span class="total-score-banner__value">79.65</span>
  </div>
</div>
</section>