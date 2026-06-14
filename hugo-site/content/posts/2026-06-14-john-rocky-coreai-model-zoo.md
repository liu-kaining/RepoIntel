---
title: '[Score: 78.2] john-rocky/coreai-model-zoo'
date: '2026-06-14T03:44:04Z'
categories:
- On-Device LLM Runtime
tags:
- Apple-CoreAI
- Swift
- Metal-Kernels
- iOS-ML
- Model-Conversion
- LLM-Inference
intel_score: 78.2
repo_name: john-rocky/coreai-model-zoo
repo_link: https://github.com/john-rocky/coreai-model-zoo
summary: 面向 Apple Core AI（iOS/macOS 27 beta）的 LLM 转换与设备端推理套件，为 Qwen3.5、Gemma 4、LFM2.5
  等模型提供经验证的 .aimodel 捆绑包与自定义 Metal 内核，适合需要在 iPhone 上跑小模型的开发者。
code_source: git
code_files_reviewed:
- apps/README.md
- apps/CoreAIChatMac/project.yml
- apps/QwenChatFast/project.yml
- apps/CoreAIChatMac/README.md
- apps/CoreAIChat/project.yml
- apps/AppShared/ModelDownloader.swift
- apps/CoreAIChatMac/Sources/CoreAIChatMacApp.swift
- apps/QwenChatFast/Sources/QwenChatFastApp.swift
- apps/CoreAIChatMac/Sources/SnapshotCard.swift
- apps/CoreAIChat/Sources/CoreAIChatApp.swift
- apps/CoreAIChat/Sources/Gemma4Gather.swift
- apps/CoreAIChat/Sources/HostCacheTest.swift
- apps/CoreAIChat/Sources/SliceANETest.swift
- apps/QwenChatFast/Sources/ContentView.swift
- apps/CoreAIChatMac/Sources/ChatView.swift
- apps/CoreAIChatMac/Sources/ChatEngine.swift
- apps/CoreAIChat/Sources/ChatView.swift
- apps/CoreAIChat/Sources/PipelinedBackend.swift
- apps/CoreAIChat/Sources/Gemma4Engine.swift
- apps/CoreAIChat/Sources/Qwen3VLBackend.swift
- apps/CoreAIChat/Sources/Gemma4VLBackend.swift
- apps/CoreAIChat/Sources/Gemma4MonolithEngine.swift
- apps/CoreAIChat/Sources/Gemma4ChatEngine.swift
- apps/CoreAIChat/Sources/Gemma4ChunkEngine.swift
- apps/QwenChatFast/Sources/FastEngine.swift
- apps/CoreAIChat/Resources/tokenizer/tokenizer_config.json
- apps/QwenChatFast/Resources/tokenizer/tokenizer_config.json
- swift/Sources/CoreAIRunner/NDArrayHelpers.swift
- knowledge/scripts/bench_cv_aimodel.py
- swift/Package.swift
- swift/Sources/coreai-run/main.swift
- official/README.md
- knowledge/stateful-kv-cache.md
- knowledge/compression.md
- zoo/README.md
- knowledge/coreai-overview.md
- knowledge/visual-intelligence-third-party-model.md
- zoo/gemma4-31b.md
- knowledge/performance-ceiling.md
- swift/README.md
- conversion/export_minicpmv46_vision.py
- knowledge/coreai-beta-mpsgraph-kvwrite-bug.md
- zoo/gemma4-e4b.md
- knowledge/swift-runtime.md
- swift/Sources/ZooFMProvider/HermesDialect.swift
- swift/Sources/ZooFMProvider/ZooLanguageModel.swift
- zoo/minicpm-v-4.6.md
- zoo/lfm2.5-8b-a1b-moe.md
code_chars_analyzed: 337107
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
      <span class="scope-stat__value">约 337,107 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">apps/README.md</code></li><li><code class="path-chip">apps/CoreAIChatMac/project.yml</code></li><li><code class="path-chip">apps/QwenChatFast/project.yml</code></li><li><code class="path-chip">apps/CoreAIChatMac/README.md</code></li><li><code class="path-chip">apps/CoreAIChat/project.yml</code></li><li><code class="path-chip">apps/AppShared/ModelDownloader.swift</code></li><li><code class="path-chip">apps/CoreAIChatMac/Sources/CoreAIChatMacApp.swift</code></li><li><code class="path-chip">apps/QwenChatFast/Sources/QwenChatFastApp.swift</code></li><li><code class="path-chip">apps/CoreAIChatMac/Sources/SnapshotCard.swift</code></li><li><code class="path-chip">apps/CoreAIChat/Sources/CoreAIChatApp.swift</code></li><li><code class="path-chip">apps/CoreAIChat/Sources/Gemma4Gather.swift</code></li><li><code class="path-chip">apps/CoreAIChat/Sources/HostCacheTest.swift</code></li><li><code class="path-chip">apps/CoreAIChat/Sources/SliceANETest.swift</code></li><li><code class="path-chip">apps/QwenChatFast/Sources/ContentView.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Apple Core AI 的官方运行时仅覆盖标准双状态 KV 模型，且 iOS 27 beta 的 MPSGraph 在 slice_update KV 写入时崩溃——开发者无法直接将 Gemma 4 的双 head_dim / Qwen3.5 的 SSM 混合架构部署到 iPhone 上，需要手动处理引擎 bug 绕行、chunk 分割和自定义 Metal 内核。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">仓库分为三层——转换脚本（<code class="code-ref">conversion/</code>，Python 导出 .aimodel 捆绑包）、Swift 运行时（<code class="code-ref">apps/</code> 下的 iOS/macOS 聊天应用 + <code class="code-ref">swift/</code> 下的 ZooFMProvider）、以及 zoo 知识库（<code class="code-ref">zoo/</code> + <code class="code-ref">knowledge/</code>，记录每个模型的端到端验证和陷阱）。核心推理路径因模型而异：Gemma 4 E2B 走三阶段管线——mmap 前端 gather（<code class="code-ref">apps/CoreAIChat/Sources/Gemma4Gather.swift:39</code> 的 <code class="code-ref">mmapInt8</code> 使用原始 POSIX mmap 避免 dirty 内存 OOM）→ host-cache 核心（GPU 单体或 ANE 6-chunk）→ 独立 head；Qwen3.5/LFM2.5/Granite 走 <code class="code-ref">apps/CoreAIChat/Sources/PipelinedBackend.swift</code> 的 <code class="code-ref">Spec</code> 参数化 <code class="code-ref">coreai-pipelined</code> 引擎。VLM 路径（<code class="code-ref">apps/CoreAIChat/Sources/Qwen3VLBackend.swift</code>、<code class="code-ref">Gemma4VLBackend.swift</code>）在文本解码器前增加了 ViT 视觉编码器的单次前向，通过 static-input hook 将 image_embeds 写入 MTLBuffer。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">apps/CoreAIChat/Sources/Gemma4MonolithEngine.swift:301</code> 的 <code class="code-ref">Gemma4MonolithBackend.step</code> 展示了精细的 KV host-write-back 逻辑——sliding_k/v_cur 和 full_k/v_cur 从核心输出中提取后写入 host 拥有的 <code class="code-ref">[Float16]</code> 缓存，绕过了 Core AI beta 的 <code class="code-ref">slice_update</code> 崩溃（<code class="code-ref">knowledge/coreai-beta-mpsgraph-kvwrite-bug.md</code> 有完整隔离实验），同时支持 fused-head（token_id 直接从核心图输出，消除 262K logits readback）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">apps/CoreAIChat/Sources/Qwen3VLBackend.swift:95-120</code> 的 <code class="code-ref">attach(cgImage:)</code> 实现了端到端 VLM 管线——448×448 预处理（块主序 patchify）→ ViT 前向 → 将 image_embeds 写入解码器的 static-input MTLBuffer，image token 重写为 extension id V+slot，整个多模态状态通过 <code class="code-ref">EngineOptions.staticInputBuffers</code> 传递给 pipelined 引擎，无需引擎修改。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">apps/CoreAIChat/Sources/FastEngine.swift</code>（Qwen3.5-0.8B fast path）有 26KB 但整个 repo 完全没有测试文件（<code class="code-ref">tests/</code>、<code class="code-ref">*_test.swift</code>、<code class="code-ref">*_test.py</code> 均不存在）。所有验证通过环境变量触发的 headless harness（如 <code class="code-ref">GEMMA_CHUNK_VERIFY=1</code>、<code class="code-ref">GEMMA_MONO_VERIFY=1</code>）进行，但这些是集成冒烟测试而非单元测试，无法保证回归安全。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">conversion/</code> 目录仅提供了 <code class="code-ref">export_minicpmv46_vision.py</code> 一个文件（48 个文件中唯一的 Python 转换脚本），大量转换脚本（如 Gemma 4 decode pipelined、Qwen3.5 hostcache、LFM2.5 MoE metal）在 code_bundle 中完全缺失。README 和 zoo 卡片反复引用它们（如 <code class="code-ref">zoo/gemma4-e2b.md</code> 引用 <code class="code-ref">ondevice/export_gemma4_ios.py</code>），但本次无法审阅到，结论不覆盖转换侧的工程质量。</p>
<p>1. 转换脚本缺失是最大信息缺口——若要复现或扩展模型覆盖，需要完整审阅 <code class="code-ref">conversion/</code> 和 <code class="code-ref">ondevice/</code> 目录。
2. <code class="code-ref">fast engine版本</code> QWEN_KIND 默认 env 变量的处理有潜在竞争（<code class="code-ref">apps/QwenChatFast/Sources/ContentView.swift:30</code> 的 <code class="code-ref">kindSuffix</code> 在 <code class="code-ref">@MainActor</code> 外计算），但实际运行时已被 MainActor 隔离，风险低。
3. 生产部署前需将 headless harness 结果固化为 CI 断言（当前纯 print，无 exit code）。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>repo LICENSE 为 NOASSERTION——Hugging Face 上的捆绑包继承上游模型许可，但仓库代码本身的许可状态不明，商用需确认。</li><li>全部基础设施锁定 iOS/macOS 27 beta + Xcode 27 beta，Core AI beta 的 MPSGraph slice_update 崩溃、ANE 编译器 OOM 等问题尚未修复——随 beta 更新可能发生破坏性变更。</li><li><code class="code-ref">knowledge/performance-ceiling.md</code> 已自述 Core AI 在 Mac GPU 上接近性能天花板（~80% of MLX），后续提升空间有限。</li><li>fork_star_ratio 仅 4.8%（5/104）且 repo 仅 3 天历史——社区贡献基础极薄，维护高度依赖单一作者。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>填补了 Apple Core AI beta 生态的关键空白——官方模型 zoo 仅覆盖 Qwen3/Gemma 3，本仓库把 Gemma 4、Qwen3.5、LFM2.5 等最新模型在 iPhone 上实际跑通并公开了 .aimodel 下载。对 iOS 原生 AI 应用开发者有直接可用价值，尤其在 WWDC 26 发布 Core AI 后的窗口期。但依赖 iOS 27 beta + Xcode 27 beta + 自定义 patch stack，正式生产需等 Apple 修复 MPSGraph bug。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.2</span>
  </div>
</div>
</section>