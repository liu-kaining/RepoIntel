---
title: '[Score: 79.7] BigDawnGhost/wenyi'
date: '2026-07-13T06:13:50Z'
categories:
- Translation Tool
tags:
- translation-tool
- cli
- llm
- novel
- deepseek
- epub
intel_score: 79.7
repo_name: BigDawnGhost/wenyi
repo_link: https://github.com/BigDawnGhost/wenyi
summary: 将多语言 EPUB/TXT 小说翻译为中文的 CLI 工具，通过全书预扫、实时术语库和多 Agent 协同，专攻长篇小说翻译的一致性与可读性。
code_source: git
code_files_reviewed:
- pyproject.toml
- .github/workflows/build.yml
- trans_novel/agents/__init__.py
- trans_novel/pipeline/__init__.py
- trans_novel/assemble/__init__.py
- trans_novel/ingest/__init__.py
- trans_novel/__init__.py
- trans_novel/glossary/__init__.py
- trans_novel/llm/__init__.py
- trans_novel/__main__.py
- trans_novel/agents/translator.py
- CONTRIBUTING.md
- trans_novel/glossary/resolver.py
- trans_novel/agents/polisher.py
- trans_novel/pipeline/context.py
- trans_novel/pipeline/checks.py
- trans_novel/agents/consistency.py
- trans_novel/assemble/report.py
- tests/fake_llm.py
- trans_novel/glossary/extractor.py
- docs/pipeline.md
- tests/test_config.py
- trans_novel/agents/base.py
- tests/sample_data.py
- docs/usage.md
- trans_novel/agents/langprofile.py
- trans_novel/ingest/models.py
- trans_novel/agents/reviewer.py
- trans_novel/ingest/text_reader.py
- docs/configuration.md
- trans_novel/postprocess/punct.py
- tests/test_translator.py
- trans_novel/agents/synopsis.py
- tests/test_glossary_agents.py
- tests/test_glossary.py
- tests/test_llm.py
- trans_novel/agents/analyzer.py
- tests/test_review_polish.py
- README.md
- config.yaml
- trans_novel/ingest/segmenter.py
- trans_novel/assemble/translator.py
- tests/test_newfeatures.py
- trans_novel/assemble/about.py
- trans_novel/pipeline/runstore.py
- tests/test_cli.py
code_chars_analyzed: 96524
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
      <span class="scope-stat__value">46 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 96,524 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/build.yml</code></li><li><code class="path-chip">trans_novel/agents/__init__.py</code></li><li><code class="path-chip">trans_novel/pipeline/__init__.py</code></li><li><code class="path-chip">trans_novel/assemble/__init__.py</code></li><li><code class="path-chip">trans_novel/ingest/__init__.py</code></li><li><code class="path-chip">trans_novel/__init__.py</code></li><li><code class="path-chip">trans_novel/glossary/__init__.py</code></li><li><code class="path-chip">trans_novel/llm/__init__.py</code></li><li><code class="path-chip">trans_novel/__main__.py</code></li><li><code class="path-chip">trans_novel/agents/translator.py</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">trans_novel/glossary/resolver.py</code></li><li><code class="path-chip">trans_novel/agents/polisher.py</code></li><li class="path-more">另有 32 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>机翻小说常出现人名、术语、语气前后不一，严重破坏阅读体验；手工修复成本极高，缺乏面向长篇文学的自动化质控流水线。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用模块化分层，ingest 解析输入生成 Document→Chapter→Segment 结构（<code class="code-ref">ingest/models.py</code>），pipeline 编排多 Agent 协作，glossary 维护术语 SQLite 库，llm 层抽象 LLM 调用并支持 fake 测试。翻译主流程在 <code class="code-ref">assemble/translator.py</code> 的 translate_batch 中：先整批翻译并要求等长 JSON，段数不符重试，仍失败则逐段兜底，从结构上杜绝整段漏译（见 <code class="code-ref">assemble/translator.py</code> 的 120 行附近重试逻辑及 fallback 调用）。Agent 基类（<code class="code-ref">agents/base.py</code> 的 _ask_json/uniform 错误处理与默认值回退，保证流水线不会因单次调用崩溃。状态持久化通过 <code class="code-ref">pipeline/runstore.py</code> 的原子写 _write_json 实现断点续跑，能应对中断。</p>
<p class="audit-callout audit-callout--highlight">对齐安全机制（<code class="code-ref">assemble/translator.py</code>）：translate_batch 在强模型整批翻译失败后，自动逐段翻译兜底，配合 <code class="code-ref">pipeline/checks.py</code> 的 count_aligned / length_flags 进行无 token 校验，形成廉价的第一道防线。</p>
<p class="audit-callout audit-callout--highlight">全书上下文注入（<code class="code-ref">agents/synopsis.py</code> 与 <code class="code-ref">pipeline/context.py</code>）：翻译前预扫全书生成恒定前缀梗概（逐章+全书），后续批处理复用该前缀，在不增加实时 token 成本的前提下让模型掌握全局剧情，提升早期章节的人称/伏笔一致性。</p>
<p class="audit-callout audit-callout--doubt">未审阅到核心编排器 <code class="code-ref">pipeline/orchestrator.py</code>，无法评估整体流程的异常传播、并发控制（如逐章审校的线程池）和资源管理，这是架构的关键空白。</p>
<p class="audit-callout audit-callout--doubt">tests/ 中虽有假 LLM 驱动的全流程测试（test_newfeatures.py），但缺少针对真实 API 的集成测试或回归套件，翻译质量的验证仅能通过人工进行，长期维护风险高。</p>
<p>先补充 orchestrator 的单元测试与文档，并在 CI 中启用假 LLM 测试；考虑提供翻译质量抽检脚本，自动对比关键词汇的全局一致性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 DeepSeek API，模型变更或限流可能导致翻译中断；缺乏多模型回退。</li><li>术语库仅约束后续翻译，不回溯修正已完成的历史译文，全书一致性仍有赖人工审读。</li><li>单维护者且个人项目，bus-factor 高，社区贡献门槛（需提供质量对比证据）可能限制参与度。</li><li>summary 过长，可能含废话</li><li>审计与 README 关键词重叠过低，属于百科式空话</li><li>technical_review 未引用任何已审阅源码路径（path 级证据缺失）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>降低中文用户阅读外文小说的门槛，对网文翻译社区和个人读者有直接吸引力；可作为翻译 SaaS 的前端工具，或集成到阅读器中。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.7</span>
  </div>
</div>
</section>