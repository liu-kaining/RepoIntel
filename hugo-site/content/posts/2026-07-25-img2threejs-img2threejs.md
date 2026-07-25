---
title: '[Score: 75.0] img2threejs/img2threejs'
date: '2026-07-25T19:02:36Z'
categories:
- 3D Reconstruction Pipeline
tags:
- threejs
- image-to-3d
- procedural-generation
- ai-agent
- python
intel_score: 75.0
repo_name: img2threejs/img2threejs
repo_link: https://github.com/img2threejs/img2threejs
summary: 将单张物体图像通过 AI 代理与确定性 Python 脚本协作，重建为纯代码、可动画的 Three.js 模型，而非网格提取。
code_source: git
code_files_reviewed:
- forge/requirements.txt
- forge/tests/fixtures/knife_review_scene.json
- forge/tests/test_specular_wash.py
- forge/tests/test_color_metrics.py
- forge/tests/test_structure_gates.py
- forge/tests/test_hue_zone_parity.py
- forge/tests/test_geometry_derivation.py
- forge/tests/test_calibrate_eye.py
- forge/tests/test_objectness.py
- .github/FUNDING.yml
- skills/generic-extract-skill.md
- forge/_shared/spec_search_profiles.json
- forge/next.py
- forge/_shared/status_banner.py
- forge/report.py
- forge/stage1_intake/cs2_review_contract.py
- forge/stage2_spec/cs2_adapters.py
- forge/_shared/artifact_cache.py
- skills/cs2_technical_analysis.md
- CONTRIBUTING.md
- grimoire/readiness/action_rigging.md
- grimoire/readiness/joint_attachment.md
- docs/cs2/review-gates.md
- skills/cs2-pistol.md
- docs/TOKEN_COST.md
- forge/stage1_intake/locate_cs2_vpk.py
- forge/_shared/color_metrics.py
- forge/_shared/image_hash.py
- grimoire/character/reconstruction.md
- grimoire/intake/surface_topology.md
- grimoire/intake/cs2_texture_acquisition.md
- grimoire/intake/quality_contract.md
- forge/_shared/feature_acceptance_policy.py
- forge/stage2_spec/derive_geometry.py
- docs/specs/vocabulary/README.md
- forge/stage1_intake/bind_detail_properties.py
- grimoire/glossary/3d_vocabulary.md
- forge/stage1_intake/check_intake_correctness.py
- grimoire/intake/cs2_technical_analysis.md
- grimoire/scripts.md
- grimoire/intake/validation_rubric.md
- forge/stage4_review/objectness.py
- forge/stage1_intake/probe_image.py
- forge/stage4_review/calibrate_eye.py
- forge/stage4_review/diagnose_render_multi_angle.py
- forge/stage3_build/module_cache.py
- forge/stage1_intake/extract_cs2_textures.py
- forge/stage4_review/correction_loop.py
code_chars_analyzed: 158395
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
      <span class="scope-stat__value">约 158,395 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">forge/requirements.txt</code></li><li><code class="path-chip">forge/tests/fixtures/knife_review_scene.json</code></li><li><code class="path-chip">forge/tests/test_specular_wash.py</code></li><li><code class="path-chip">forge/tests/test_color_metrics.py</code></li><li><code class="path-chip">forge/tests/test_structure_gates.py</code></li><li><code class="path-chip">forge/tests/test_hue_zone_parity.py</code></li><li><code class="path-chip">forge/tests/test_geometry_derivation.py</code></li><li><code class="path-chip">forge/tests/test_calibrate_eye.py</code></li><li><code class="path-chip">forge/tests/test_objectness.py</code></li><li><code class="path-chip">.github/FUNDING.yml</code></li><li><code class="path-chip">skills/generic-extract-skill.md</code></li><li><code class="path-chip">forge/_shared/spec_search_profiles.json</code></li><li><code class="path-chip">forge/next.py</code></li><li><code class="path-chip">forge/_shared/status_banner.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>游戏开发者/3D 美术从图像到可编辑的 Three.js 模型，传统手段需要手动建模或多视图 photogrammetry，cost 高且产出不可动画。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分为 intake（probe_image.py 等）、spec（validate_sculpt_spec.py）、build（generate_threejs_factory.py，未审阅）和 review 四阶段。AI 代理负责生成 spec 和工厂代码，确定性脚本执行严格的图像分析（如 objectness，color_metrics 等）、多角度坍缩检查（diagnose_render_multi_angle.py:37-52）和迭代校正环（correction_loop.py:37-96）。模块缓存（module_cache.py:29-39）支持增量重建。整体将视觉理解委托给 VLM，工程部分用纯标准库保证零依赖（forge/requirements.txt）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">forge/stage4_review/objectness.py:78-112</code> 实现了 HOG-like 描述符，在裁剪前景后计算梯度方向直方图，对背景、位置、尺度、绝对亮度不变，能在照片与程序化渲染间提供比 SSIM 更稳定的形状相似度，测试（<code class="code-ref">forge/tests/test_objectness.py:44-47</code>）验证了跨背景和亮度的不变性。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">forge/stage4_review/diagnose_render_multi_angle.py:37-52</code> 通过比较参考视角与轨道视角的前景占比，检测“退化视图”（比值 &lt; 0.15），有效防止 billboard 伪装成 3D 体，这是保证生成的模型真正立体的关键检查。</p>
<p class="audit-callout audit-callout--doubt">核心代码生成器 <code class="code-ref">forge/stage3_build/generate_threejs_factory.py</code> 及验证器 <code class="code-ref">validate_sculpt_spec.py</code> 未在 code_bundle 中提供，无法评估 Three.js 几何构造的正确性、错误传播和 spec 验证严格度，直接影响 engineering 评分可靠性。</p>
<p class="audit-callout audit-callout--doubt">校正循环（<code class="code-ref">forge/stage4_review/correction_loop.py:37-96</code>）依赖 VLM 反馈和硬编码的停止策略（max_iter=6, min_delta=0.02），但未提供真实 token 消耗下的收敛证据，且 calibration 测试（<code class="code-ref">forge/tests/test_calibrate_eye.py:28-38</code>）目前仅用合成样本，实际校正效果未知。</p>
<p>补充生成器代码的审查并提供端到端集成测试（包括真实 AI 代理运行、产出 Three.js 代码的渲染验证）；在 token 成本文档中增加实测收敛率数据。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心生成器代码未审查，实际生成的 Three.js 模型可能存在几何/材质错误。</li><li>强依赖 Claude Code 等外部 AI 模型，定价或可用性变化将直接阻断流水线。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若 AI 代理成本可控，该方案能为 AR/VR 快速原型、3D 资产市场提供高效替代手动建模的工具链，但商业化取决于底层模型的经济性。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.0</span>
  </div>
</div>
</section>