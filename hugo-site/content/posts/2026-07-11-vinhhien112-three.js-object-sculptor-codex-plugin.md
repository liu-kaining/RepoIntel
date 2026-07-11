---
title: '[Score: 75.0] vinhhien112/Three.js-Object-Sculptor-Codex-Plugin'
date: '2026-07-11T10:12:13Z'
categories:
- AI-Assisted 3D Generation
tags:
- threejs
- procedural-modeling
- codex-plugin
- image-to-3d
- quality-gate
intel_score: 75.0
repo_name: vinhhien112/Three.js-Object-Sculptor-Codex-Plugin
repo_link: https://github.com/vinhhien112/Three.js-Object-Sculptor-Codex-Plugin
summary: Codex 插件，通过多阶段自校正流水线将单张物体照片转化为纯代码的程序化 Three.js 模型，强调质量门与视觉验证。
code_source: git
code_files_reviewed:
- .codex-plugin/plugin.json
- skills/object-to-threejs-procedural/references/validation-rubric.md
- skills/object-to-threejs-procedural/references/action-ready-models.md
- skills/object-to-threejs-procedural/references/attachment-joint-correctness.md
- skills/object-to-threejs-procedural/references/self-correction-loop.md
- skills/object-to-threejs-procedural/references/procedural-patterns.md
- skills/object-to-threejs-procedural/references/pre-spec-assessment.md
- scripts/new_pre_spec_assessment.py
- scripts/visual_feature_gate.py
- skills/object-to-threejs-procedural/references/3d-graphics-terminology.md
- skills/object-to-threejs-procedural/references/browser-screenshot-feedback.md
- scripts/probe_reference_image.py
- skills/object-to-threejs-procedural/references/material-lighting-realism.md
- scripts/make_visual_comparison_sheet.py
- README.md
- scripts/append_sculpt_review.py
- scripts/sculpt_pass_orchestrator.py
- skills/object-to-threejs-procedural/SKILL.md
- scripts/extract_reference_pbr.py
- scripts/new_sculpt_spec.py
- scripts/generate_threejs_factory.py
code_chars_analyzed: 259785
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
      <span class="scope-stat__value">21 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 259,785 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.codex-plugin/plugin.json</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/validation-rubric.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/action-ready-models.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/attachment-joint-correctness.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/self-correction-loop.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/procedural-patterns.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/pre-spec-assessment.md</code></li><li><code class="path-chip">scripts/new_pre_spec_assessment.py</code></li><li><code class="path-chip">scripts/visual_feature_gate.py</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/3d-graphics-terminology.md</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/browser-screenshot-feedback.md</code></li><li><code class="path-chip">scripts/probe_reference_image.py</code></li><li><code class="path-chip">skills/object-to-threejs-procedural/references/material-lighting-realism.md</code></li><li><code class="path-chip">scripts/make_visual_comparison_sheet.py</code></li><li class="path-more">另有 7 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者从参考图构建实时 3D 资产时，常因流程缺失导致模型“形似神不似”，且缺乏结构化质量检查与可动画化层级设计。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">插件由一组 Python 脚本及参考文档构成，通过 Codex 技能驱动工作流。核心链路：<code class="code-ref">scripts/probe_reference_image.py</code> 先做图像技术探测，<code class="code-ref">scripts/new_pre_spec_assessment.py</code> 生成复杂度与质量契约，<code class="code-ref">scripts/new_sculpt_spec.py</code> 创建结构化的 ObjectSculptSpec，随后 <code class="code-ref">scripts/sculpt_pass_orchestrator.py</code> 启用顺序构建门控，<code class="code-ref">scripts/generate_threejs_factory.py</code> 按当前通过阶段输出 TypeScript 骨架，<code class="code-ref">scripts/append_sculpt_review.py</code> 配合 <code class="code-ref">scripts/visual_feature_gate.py</code> 实现基于截图和 AI 视觉的特征级自校正循环。</p>
<p class="audit-callout audit-callout--highlight">自校正循环与特征门控：<code class="code-ref">scripts/visual_feature_gate.py:feature_gate_failures</code> 强制检查 critical feature 分数，<code class="code-ref">scripts/append_sculpt_review.py:review_completes_pass</code> 要求视觉证据和 AI 评分，只有通过才能解锁下一阶段，避免“一镜到底”的粗糙生成。</p>
<p class="audit-callout audit-callout--highlight">程序化纹理与 PBR 独立通道生成：<code class="code-ref">scripts/extract_reference_pbr.py:make_maps</code> 从像素中提取独立的 albedo/roughness/height/normal/ao 贴图，<code class="code-ref">scripts/generate_threejs_factory.py:makeProceduralTextureSet</code> 生成多种贴图并保证通道独立，杜绝质感互串，提升材质保真度。</p>
<p class="audit-callout audit-callout--doubt">代码库未包含任何单元测试或集成测试文件，<code class="code-ref">scripts/</code> 下无 <code class="code-ref">*_test.py</code> 或 <code class="code-ref">tests/</code> 目录，仅靠参数校验和异常捕获保证健壮性，在 CI/CD 中缺乏自动化验证。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">scripts/generate_threejs_factory.py</code> 生成的 TypeScript 骨架中，<code class="code-ref">geometry_for()</code> 仅返回固定基本体（如 BoxGeometry），复杂形状仍需人工大量补充，自动生成程度有限，依赖后期人工编码。</p>
<p>适合已有 Codex 环境的 Three.js 开发者快速获得可审核的 3D 资产原型，但实际产出仍需艺术家或程序员细化，可作为团队内部可视化沟通工具，不宜直接用于全自动生产管线。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>单图输入无法保证隐藏面精度，复杂物体仍需多角度参考。</li><li>严重依赖 Codex 插件系统，如平台变更或 API 调整可能导致插件失效。</li><li>无测试覆盖，长期维护中回归风险高。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若 Codex 生态壮大，可成为程序化资产生成的标准工作流，降低实时 3D 预览门槛，但目前受众限于 OpenAI 合作伙伴或高阶用户，直接变现路径模糊。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.0</span>
  </div>
</div>
</section>