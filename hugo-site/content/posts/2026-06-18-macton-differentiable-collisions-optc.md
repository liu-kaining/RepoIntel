---
title: '[Score: 76.05] macton/differentiable-collisions-optc'
date: '2026-06-18T15:17:54Z'
categories:
- Numerical Simulation / Collision Detection
tags:
- C
- collision-detection
- optimization
- LLM-assisted
- convex-geometry
- numerical-methods
intel_score: 76.05
repo_name: macton/differentiable-collisions-optc
repo_link: https://github.com/macton/differentiable-collisions-optc
summary: 用 GPT-5.5 驱动的 LLM 代理优化流程，将论文中的凸体碰撞检测参考实现提速约 102 倍，附带完整正确性门控与可视化工具链。
code_source: git
code_files_reviewed:
- Makefile
- src/collide.h
- src/README.md
- src/reference-julia-comparison.md
- src/collide.c
- test/validator.h
- performance-test/pairs_io.h
- performance-test-optimized/pairs_io.h
- performance-test-optimized/build_optimized_pairs.c
- performance-test/build_input.c
- performance-test-optimized/measure-speedup.sh
- performance-test-optimized/build_optimized_shapes.c
- viz/README.md
- bin_format.h
- performance-test/validate_main.c
- performance-test-optimized/pairs_io.c
- performance-test/pairs_io.c
- performance-test-optimized/validate_main.c
- performance-test-optimized/perf_main.c
- performance-test/perf_main.c
- src-optimized/collide.h
- performance-test-optimized/HARNESS-BASELINE.md
- performance-test/gen_pairs.c
- prompts/create-reference.md
- performance-test-optimized/gen_pairs_seed.c
- prompts/create-visualizer.md
- performance-test-optimized/compare_results.c
- test/validator.c
- prove-optimized-harness.sh
- test/test_main.c
- performance-test-optimized/validate_contacts.c
- prompts/create-readme.md
- README.md
- prompts/create-optimized-test-harness.md
- prompts/create-optimized.md
code_chars_analyzed: 247358
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
      <span class="scope-stat__value">35 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 247,358 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">src/collide.h</code></li><li><code class="path-chip">src/README.md</code></li><li><code class="path-chip">src/reference-julia-comparison.md</code></li><li><code class="path-chip">src/collide.c</code></li><li><code class="path-chip">test/validator.h</code></li><li><code class="path-chip">performance-test/pairs_io.h</code></li><li><code class="path-chip">performance-test-optimized/pairs_io.h</code></li><li><code class="path-chip">performance-test-optimized/build_optimized_pairs.c</code></li><li><code class="path-chip">performance-test/build_input.c</code></li><li><code class="path-chip">performance-test-optimized/measure-speedup.sh</code></li><li><code class="path-chip">performance-test-optimized/build_optimized_shapes.c</code></li><li><code class="path-chip">viz/README.md</code></li><li><code class="path-chip">bin_format.h</code></li><li class="path-more">另有 21 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>机器人仿真/物理引擎中窄相碰撞检测常为性能瓶颈：双精度内点法每对约 278 µs，1000 对基准测试 0.28 s，在实时循环中无法接受。工程团队需要一个可直接嵌入、单精度但精度有保障的替代方案，同时需要方法论层面的可复现优化记录。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">参考实现在 <code class="code-ref">src/collide.c</code> 中实现了 Tracy/Howell/Manchester 论文 (arXiv:2207.00669) 的凸锥优化问题 (10)：每对基元组装约束行（球体 SOC、盒体 6 面半空间、胶囊 SOC+线性、多面体凸包半空间），用对数障碍内点法牛顿迭代求解最小均匀缩放 α，接触点按 eq.(24) 恢复。内核全部双精度，外部 API 单精度浮点，±8192 m 域内保证 1 mm 精度。批量接口 <code class="code-ref">cp_collide_pairs</code> 零分配——调用者提供 scratch buffer（<code class="code-ref">src/collide.h:88</code>），不足时显式返回 <code class="code-ref">CP_ERR_NO_CONVERGE</code>，永不静默分配。输入验证在 <code class="code-ref">build_shape</code>（<code class="code-ref">src/collide.c:121</code>）中按严格顺序执行：旋转正交性、坐标范围、尺寸范围，每对独立报告 status。

优化路径 <code class="code-ref">src-optimized/collide.h</code> 引入了构建阶段预计算表 <code class="code-ref">cp_vshapes</code>：每基元的验证状态与世界坐标求解几何一次构建、序列化为 blob，运行时 <code class="code-ref">cp_collide_pairs_vshapes</code> 直接从表中求解，将逐对预处理排除在计时之外。<code class="code-ref">performance-test-optimized/perf_main.c:42</code> 的计时区仅覆盖求解调用。</p>
<p class="audit-callout audit-callout--highlight">独立验证器双保险架构。
<code class="code-ref">test/validator.c</code> 实现了完全不同的算法族——GJK 距离查询 + α 二分搜索，使用原始顶点（而非凸包半空间），与 <code class="code-ref">src/collide.c</code> 零代码共享。<code class="code-ref">performance-test-optimized/validate_contacts.c</code> 进一步实现了第三条独立路径：逐点表面距离检查（球体解析、盒体 SDF、多面体 GJK）加 eq.(24) 一致性验证，float32 坐标感知容差 <code class="code-ref">eff_tol</code>（<code class="code-ref">validate_contacts.c:40</code>）。三层验证链在 1000 对上均 PASS。</p>
<p class="audit-callout audit-callout--highlight">工程化证明流程。
<code class="code-ref">prove-optimized-harness.sh</code> 是端到端的自动化证明脚本：恒等基线验证 → 构建 → 参考/优化计时 → 容差比较 → 接触点认证 → 测试套件 → 独立验证器 → 替代种子泛化 → 确定性检查 → 输入校验和不变性，共 10 步，所有输出记录到 log。<code class="code-ref">HARNESS-BASELINE.md</code> 记录了恒等复制的基线证据（0.000 mm 偏差，≈1.0x），证明测量管道本身在用于评判前已被验证。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src-optimized/</code> 的实际优化源码（<code class="code-ref">collide.c</code>/<code class="code-ref">collide.h</code> 优化版本未在 code_bundle 中提供，仅提供了 header），无法验证 README 中声称的 GJK+bisection 替换 barrier solve、SAT 特化、单精度安全重居中等优化的具体实现质量。本次结论对优化版代码质量不作判断。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">poly_faces</code> 凸包算法（<code class="code-ref">src/collide.c:90</code>）为 O(n⁴) 暴力枚举所有三元组平面，CP_MAX_POLY_VERTS=32 时每次调用约 49k 次三元组遍历。虽然仅在批量预计算阶段执行一次，但对高顶点数多面体而言构建成本不低——优化版是否改善了这一点未知。</p>
<p>适合嵌入机器人仿真/物理引擎的窄相碰撞检测管线（需自备 broadphase）。若需直接使用优化版，建议先在目标硬件上独立运行 <code class="code-ref">prove-optimized-harness.sh</code> 复现 102x 数据再集成。注意 README 声称的加速比严格依赖 WSL2/gcc 11/-march=native 环境，跨平台迁移需重新测量。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>优化版源码未在 code_bundle 中审阅，README 声称的 102x 加速和所有优化细节无法独立验证，集成前需自行跑 prove-optimized-harness.sh。</li><li>性能数据仅来自 WSL2/gcc 11/x86-64 单机，-march=native 下的 AVX/SSE 路径在不同硬件上加速比可能大幅波动；README 明确声明这是工程估计而非泛化保证。</li><li>项目创建仅 2 天、1 次 commit、102 stars/7 forks，社区健康度极低，长期维护依赖单一作者。</li><li>README 声称使用 GPT-5.5 生成代码，但 prompts/ 和 nagent 工具链外部依赖无法在本 repo 内复现完整的 LLM 优化过程。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对物理仿真引擎（MuJoCo、Drake 等）和机器人运动规划管线有直接实用价值：100x 加速使凸体窄相碰撞检测从批处理级别进入可交互级别。LLM 驱动优化的方法论（结构化 prompt + 端到端证明门控）可作为行业参考模板，但碰撞库本身是垂直场景组件，商业范围有限。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">90</div>
  <div class="score-bar"><span style="width:90%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.05</span>
  </div>
</div>
</section>