---
title: '[Score: 77.75] Extraltodeus/J-Wash'
date: '2026-07-14T19:15:03Z'
categories:
- Model Editing & Interpretability
tags:
- jacobian-lens
- pytorch
- transformers
- model-steering
- activation-engineering
- checkpoint-export
intel_score: 77.75
repo_name: Extraltodeus/J-Wash
repo_link: https://github.com/Extraltodeus/J-Wash
summary: 基于 Anthropic Jacobian Lens 的实时 token 方向编辑工具，支持将 steering 效果直接烘焙为纯权重 checkpoint（safetensors/LoRA），无需训练或微调，实现“所见即所得”的模型身份与行为重塑。
code_source: git
code_files_reviewed:
- ui/package.json
- requirements.txt
- api/app.py
- core/gpus.py
- core/neighbors.py
- core/registry.py
- core/rebase.py
- core/lens_manager.py
- core/store.py
- core/ablation.py
- core/fitting.py
- core/editing.py
- core/model_manager.py
- ui/src/main.jsx
- ui/src/tok.js
- data/presets/gpt-oss-20b__fish_identity.json
- ui/vite.config.js
- scripts/fish_prompts.json
- data/presets/gemma-3-1b-it__fish_identity.json
- scripts/ws_smoke.py
- data/presets/qwen-3.5-4b__fish_identity.json
- scripts/ws_lens_smoke.py
- run.py
- scripts/verify_accuracy.py
- config.py
- scripts/m0_walkthrough.py
- ui/src/Diff.jsx
- scripts/store_smoke.py
- scripts/pure_check.py
- scripts/fit_worker.py
- scripts/test_rebase.py
- scripts/jlab.py
- scripts/jwash_mcp.py
- README.md
- ui/src/Editor.jsx
- ui/src/LensView.jsx
code_chars_analyzed: 342909
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
      <span class="scope-stat__value">36 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 342,909 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">ui/package.json</code></li><li><code class="path-chip">requirements.txt</code></li><li><code class="path-chip">api/app.py</code></li><li><code class="path-chip">core/gpus.py</code></li><li><code class="path-chip">core/neighbors.py</code></li><li><code class="path-chip">core/registry.py</code></li><li><code class="path-chip">core/rebase.py</code></li><li><code class="path-chip">core/lens_manager.py</code></li><li><code class="path-chip">core/store.py</code></li><li><code class="path-chip">core/ablation.py</code></li><li><code class="path-chip">core/fitting.py</code></li><li><code class="path-chip">core/editing.py</code></li><li><code class="path-chip">core/model_manager.py</code></li><li><code class="path-chip">ui/src/main.jsx</code></li><li class="path-more">另有 22 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>研究者/开发者需要修改模型特定 token 方向（如身份词替换）以探究可解释性或定制行为，但现有方案多为运行时 hook，无法导出为独立模型部署。J-Wash 填补了从交互式探测到可分发权重的鸿沟。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">FastAPI 后端 (<code class="code-ref">api/app.py</code>) 管理 WebSocket 和 REST 接口，<code class="code-ref">core/model_manager.py</code> 负责模型加载与生成，<code class="code-ref">core/lens_manager.py</code> 封装 Jacobian Lens 读取与残差捕获，<code class="code-ref">core/ablation.py</code> 实现多种干预模式（standard/readthrough/exact/abliteration）并通过 hooks 注入。导出管线基于 <code class="code-ref">core/rebase.py</code> 的基变换算法，将 token 方向编辑转换为下游读取矩阵的 low-rank 更新（<code class="code-ref">core/rebase.py</code>:build_plan）。前端 React (<code class="code-ref">ui/src/Editor.js</code>x) 提供层选择、规则编辑与导出界面。</p>
<p class="audit-callout audit-callout--highlight">纯权重导出保真度 (<code class="code-ref">core/rebase.py:3</code>-28 模块文档) — 通过改变下游 RMSNorm 后矩阵的基变换，将 J-space 方向编辑忠实地写入权重，预览 hook 与导出 checkpoint 效果仅差舍入误差，经 <code class="code-ref">scripts/test_rebase.py</code> 验证 live≡bake。</p>
<p class="audit-callout audit-callout--highlight">多架构兼容性 (<code class="code-ref">core/model_manager.py:332</code> <code class="code-ref">rebase_supported</code> 检测) — 自动识别 write-norm 架构（如 Gemma）并回退到 abliteration 模式，通过 W_U 投影实现全局纯权重编辑，使工具覆盖主流 decoder 模型。</p>
<p class="audit-callout audit-callout--doubt">异常路径资源释放不彻底 — 在 <code class="code-ref">core/model_manager.py</code>:generate 的 finally 块中调用了 _free_cuda，但若生成中途 CUDA 异常，部分中间张量可能未被回收，依赖垃圾收集不够可靠。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖局限于少数验证脚本 — scripts/ 目录下的 test_rebase.py 与 verify_accuracy.py 仅覆盖特定场景，未审阅到对边缘情况（如空规则、OOM 恢复、量化模型）的系统测试用例。</p>
<p>适合可解释性研究或概念验证，生产环境需增强错误边界、补全单元测试，并监控编辑后模型在标准基准上的性能退化。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>导出 checkpoint 可能违反原始模型的使用条款（如禁止修改权重），用户需自担合规风险。</li><li>纯权重编辑在大模型上依赖数值稳定性，若累积变换矩阵 condition 不佳，bf16 下可能产生失真。</li><li>项目仅发布一天，无社区维护历史，长期可用性存疑。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为模型行为编辑提供了一种低成本、保真度高的工程方案，可集成到模型开发工作流中，吸引 AI 安全与定制化部署团队。但直接商业化路径模糊，更可能作为开源基础组件被吸纳。</p>
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
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
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
    <span class="total-score-banner__value">77.75</span>
  </div>
</div>
</section>