---
title: '[Score: 78.95] arcships/light-ocr'
date: '2026-07-15T10:46:43Z'
categories:
- OCR Engine
tags:
- C++
- Node.js
- ONNX Runtime
- PP-OCRv6
- Offline
- Embedded
intel_score: 78.95
repo_name: arcships/light-ocr
repo_link: https://github.com/arcships/light-ocr
summary: 基于 PP-OCRv6 的轻量级本地 OCR 引擎，用 C++17 实现核心逻辑，并提供 Node.js 异步绑定，支持离线识别与分块检测。
code_source: git
code_files_reviewed:
- bindings/node/package.json
- bindings/node/CMakeLists.txt
- CMakeLists.txt
- .github/workflows/npm-promote.yml
- .github/workflows/core.yml
- .github/workflows/tiled-qualification.yml
- .github/workflows/npm-release.yml
- src/util/sha256.hpp
- src/result/assemble.hpp
- src/recognition/ctc_decode.hpp
- src/preprocess/image.hpp
- src/util/checked_math.hpp
- src/geometry/geometry.hpp
- src/detection/db_postprocess.hpp
- src/preprocess/tensor.hpp
- src/detection/tiled.hpp
- src/model/bundle_data.hpp
- src/recognition/ctc_decode.cpp
- src/preprocess/image.cpp
- src/util/sha256.cpp
- src/result/result.cpp
- src/geometry/geometry.cpp
- src/detection/db_postprocess.cpp
- src/detection/tiled.cpp
- src/preprocess/tensor.cpp
- src/core/engine.cpp
- src/model/model_bundle.cpp
- src/inference/onnxruntime/backend.hpp
- src/inference/onnxruntime/backend.cpp
- tests/unit/main.cpp
- tools/common/bundle_files.hpp
- bindings/node/src/bundle_loader.hpp
- bindings/node/src/encoded_image.hpp
- tools/npm/smoke.ts
- tools/npm/verdaccio-release.yaml
- tests/fuzz/encoded_image_fuzz.cpp
- corpus/tiled-v1/parity-exceptions.json
- tests/unit/test_sha256.cpp
- corpus/fixtures/generated-blank/fixture.json
- AGENTS.md
- corpus/fixtures/generated-hello-123/fixture.json
- corpus/fixtures/paddleocr-book-page/fixture.json
- corpus/fixtures/paddleocr-captcha-handwriting/fixture.json
- corpus/fixtures/paddleocr-xfund-form/fixture.json
- corpus/fixtures/paddleocr-boarding-pass/fixture.json
- corpus/fixtures/generated-japanese-horizontal/fixture.json
- corpus/fixtures/generated-japanese-rotated/fixture.json
- corpus/fixtures/generated-traditional-horizontal/fixture.json
code_chars_analyzed: 234406
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
      <span class="scope-stat__value">约 234,406 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">bindings/node/package.json</code></li><li><code class="path-chip">bindings/node/CMakeLists.txt</code></li><li><code class="path-chip">CMakeLists.txt</code></li><li><code class="path-chip">.github/workflows/npm-promote.yml</code></li><li><code class="path-chip">.github/workflows/core.yml</code></li><li><code class="path-chip">.github/workflows/tiled-qualification.yml</code></li><li><code class="path-chip">.github/workflows/npm-release.yml</code></li><li><code class="path-chip">src/util/sha256.hpp</code></li><li><code class="path-chip">src/result/assemble.hpp</code></li><li><code class="path-chip">src/recognition/ctc_decode.hpp</code></li><li><code class="path-chip">src/preprocess/image.hpp</code></li><li><code class="path-chip">src/util/checked_math.hpp</code></li><li><code class="path-chip">src/geometry/geometry.hpp</code></li><li><code class="path-chip">src/detection/db_postprocess.hpp</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>桌面应用、私密文档处理或本地工具需 OCR 时，上传图像到云端会带来隐私风险和网络延迟。light-ocr 在进程内直接运行模型，无需外部服务或 Python 侧载。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">从模型包加载开始（src/model/model_bundle.cpp:parse_bundle），先验证文件清单和 SHA256 完整性，然后创建 Engine（src/core/engine.cpp:Engine::create）时初始化两个 ONNX 会话。识别调用链（src/core/engine.cpp:EngineImpl::recognize）依次通过 validate_and_convert_image（src/preprocess/image.cpp）转换像素格式，接着根据策略执行检测预处理、推理、后处理（src/detection/db_postprocess.cpp:db_postprocess）获取文本框，再通过 sort_reading_order 排序并计划识别批次（src/preprocess/tensor.cpp:plan_recognition_batches），对每个批次裁剪、缩放、推理、CTC 解码（src/recognition/ctc_decode.cpp:decode_ctc），最终组装结果并过滤低置信度行（src/result/result.cpp:assemble_ocr_result）。</p>
<p class="audit-callout audit-callout--highlight">全面的资源安全检查，例如图像尺寸和步幅验证使用了 checked_image_bytes（src/util/checked_math.hpp 和 src/preprocess/image.cpp:validate_image_layout），防止溢出和越界。</p>
<p class="audit-callout audit-callout--highlight">工程化质量极高，CI 中同时运行 ASan/UBSan、ThreadSanitizer（<code class="code-ref">.github/workflows/core.yml</code>）和模糊测试（tests/fuzz/目录），还有 oracle parity 测试对比上游 PaddleOCR 输出，确保行为一致性。</p>
<p class="audit-callout audit-callout--doubt">EngineImpl::recognize 用互斥锁限制并发调用为 1（src/core/engine.cpp:EngineImpl::recognize 中的 active_ 标志），若在高并发 API 服务中使用，可能成为吞吐瓶颈。</p>
<p class="audit-callout audit-callout--doubt">未审阅到显式的生命周期压力测试或异常恢复机制（如引擎突然关闭时内部状态的清理），仅 leak_check 工具和 close 中的条件变量等待（src/core/engine.cpp:EngineImpl::close），实际容错性有待验证。</p>
<p>适用于 Electron 桌面软件或私有文档系统，可替代云 OCR。注意当前模型仅 CPU 推理且约 31 MB，移动端或边缘设备部署需评估内存和算力。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>模型仅针对 CJK/Latin 混合文本优化，对阿拉伯文、天城文等脚本识别质量未知。</li><li>项目仅诞生 1 天，社区贡献和长期维护尚存不确定性。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为需要隐私合规和离线能力的桌面应用提供免云 OCR 方案，降低运维成本并提升用户体验。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">92</div>
  <div class="score-bar"><span style="width:92%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.95</span>
  </div>
</div>
</section>