---
title: '[Score: 77.55] JustVugg/colibri'
date: '2026-07-12T10:25:00Z'
categories:
- AI Model Runtime
tags:
- C
- MoE
- speculative-decoding
- disk-streaming
- quantization
intel_score: 77.55
repo_name: JustVugg/colibri
repo_link: https://github.com/JustVugg/colibri
summary: 纯C零依赖推理引擎，将744B MoE模型以离散专家库流式加载至消费级内存，实现本地高速生成。
code_source: git
code_files_reviewed:
- Makefile
- desktop/src-tauri/Cargo.toml
- web/package.json
- c/Makefile
- c/tools/__init__.py
- desktop/src-tauri/src/main.rs
- desktop/src-tauri/src/lib.rs
- c/tests/test_st.c
- c/tests/test_benchmark_cuda_fixture.py
- c/tests/test_tier.c
- c/tests/test_json.c
- c/tests/audit_win_shims.c
- c/tests/test_tok.c
- c/tests/test_resource_plan.py
- c/tests/test_grammar.c
- .github/ISSUE_TEMPLATE/config.yml
- web/src/vite-env.d.ts
- desktop/src-tauri/build.rs
- web/src/lib/utils.ts
- web/tsconfig.json
- desktop/src-tauri/capabilities/default.json
- web/src/main.tsx
- web/tsconfig.node.json
- ref.json
- web/src/lib/runtime.ts
- web/src/components/ui/badge.tsx
- web/components.json
- c/ref_glm.json
- .github/pull_request_template.md
- web/src/components/ui/input.tsx
- web/src/components/ui/textarea.tsx
- web/vite.config.ts
- web/tsconfig.app.json
- c/tools/README.md
- CONTRIBUTING.md
- .github/ISSUE_TEMPLATE/feature_request.yml
- web/src/lib/storage.ts
- web/README.md
- c/tier.h
- web/src/lib/runtime.test.ts
- desktop/README.md
- desktop/src-tauri/tauri.conf.json
- .github/ISSUE_TEMPLATE/bug_report.yml
- web/src/components/ui/button.tsx
- .github/ISSUE_TEMPLATE/performance_report.yml
- web/src/lib/storage.test.ts
- c/backend_cuda.h
- c/scripts/run.sh
code_chars_analyzed: 45843
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
      <span class="scope-stat__value">约 45,843 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">desktop/src-tauri/Cargo.toml</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">c/Makefile</code></li><li><code class="path-chip">c/tools/__init__.py</code></li><li><code class="path-chip">desktop/src-tauri/src/main.rs</code></li><li><code class="path-chip">desktop/src-tauri/src/lib.rs</code></li><li><code class="path-chip">c/tests/test_st.c</code></li><li><code class="path-chip">c/tests/test_benchmark_cuda_fixture.py</code></li><li><code class="path-chip">c/tests/test_tier.c</code></li><li><code class="path-chip">c/tests/test_json.c</code></li><li><code class="path-chip">c/tests/audit_win_shims.c</code></li><li><code class="path-chip">c/tests/test_tok.c</code></li><li><code class="path-chip">c/tests/test_resource_plan.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>大参数MoE模型推理需数百GB显存，普通开发者无法在消费级硬件上运行，本地实验与部署成本极高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">引擎由单一C文件（c/glm.c，~2400行，未在审计包中提供）与少量头文件组成，运行时将模型密集部分常驻内存（int4量化~9.9GB），21,504个路由专家按需从磁盘流式加载，利用每层LRU缓存、可选的固定热点存储及OS页面缓存。推理链包含MLA注意力（压缩KV cache）、DeepSeek风格sigmoid路由、MTP推测解码及文法强制推测等优化。c/Makefile展示了跨平台构建（x86-64/ARM64/macOS/Windows），支持AVX2、OpenMP，并可选CUDA后端。</p>
<p class="audit-callout audit-callout--highlight">c/tests/test_grammar.c中的文法强制推测测试验证了当文法仅允许单个合法字节时，引擎能自动注入预接受草稿（如JSON键名、枚举值），与MTP推测组合覆盖空白区域，显著加速结构化输出。</p>
<p class="audit-callout audit-callout--highlight">c/tier.h中的tier_pick_swap实现了基于热度的专家缓存替换策略，通过固定余量和25%迟滞避免乒乓效应；配套测试c/tests/test_tier.c覆盖了热专家晋升、迟滞阻隔与衰减行为。</p>
<p class="audit-callout audit-callout--doubt">核心推理文件c/glm.c未包含在审计代码集中，无法核实其实现质量、错误处理、内存安全及与README宣称特性（如MLA吸收、INT4计算内核）的一致性。</p>
<p class="audit-callout audit-callout--doubt">未发现持续集成配置文件（如.github/workflows），虽然Makefile提供了make check本地验证，但缺乏自动化跨平台测试。</p>
<p>若核心引擎实现与README匹配，可优先用于本地GLM-5.2推理；<code class="code-ref">建议先通过c/tools/convert_fp8_to_int4.py</code>准备模型，<code class="code-ref">并使用c/tools/resource_plan.py</code>规划内存与存储。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心引擎源码(c/glm.c)未审查，实际稳定性与README宣称可能存在偏差</li><li>模型转换及存储需~370GB空间，硬件门槛仍高</li><li>项目极度年轻（10天），长期维护与社区持续性未知</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若持续优化，有望成为消费级MoE推理的事实工具，降低本地大模型使用门槛，可能吸引硬件厂商或云服务集成。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">60</div>
  <div class="score-bar"><span style="width:60%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">73</div>
  <div class="score-bar"><span style="width:73%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.55</span>
  </div>
</div>
</section>