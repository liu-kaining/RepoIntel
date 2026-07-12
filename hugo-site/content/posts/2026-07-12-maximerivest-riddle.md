---
title: '[Score: 78.7] MaximeRivest/riddle'
date: '2026-07-12T02:29:16Z'
categories:
- e-Ink Application / AI Interaction
tags:
- remarkable
- eink
- handwriting-synthesis
- llm
- rust
- ui-animation
intel_score: 78.7
repo_name: MaximeRivest/riddle
repo_link: https://github.com/MaximeRivest/riddle
summary: 在 reMarkable Paper Pro 上用手写与 Tom Riddle 的日记对话，墨水消失后手写回复动画出现，支持记忆和页面召唤。
code_source: git
code_files_reviewed:
- Cargo.toml
- src/main.rs
- src/fb.rs
- src/power.rs
- src/display.rs
- src/pen.rs
- src/surface.rs
- src/touch.rs
- src/ink.rs
- src/script.rs
- src/qtfb.rs
- src/memory.rs
- src/help.rs
- src/oracle.rs
- .cargo/config.toml
- external.manifest.json
- scripts/make-bundle.sh
- build.rs
- scripts/appload-launch.sh
- build-takeover.sh
- scripts/riddle-takeover.sh
- settings.schema.json
- README.md
code_chars_analyzed: 181665
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
      <span class="scope-stat__value">约 181,665 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">src/main.rs</code></li><li><code class="path-chip">src/fb.rs</code></li><li><code class="path-chip">src/power.rs</code></li><li><code class="path-chip">src/display.rs</code></li><li><code class="path-chip">src/pen.rs</code></li><li><code class="path-chip">src/surface.rs</code></li><li><code class="path-chip">src/touch.rs</code></li><li><code class="path-chip">src/ink.rs</code></li><li><code class="path-chip">src/script.rs</code></li><li><code class="path-chip">src/qtfb.rs</code></li><li><code class="path-chip">src/memory.rs</code></li><li><code class="path-chip">src/help.rs</code></li><li><code class="path-chip">src/oracle.rs</code></li><li class="path-more">另有 9 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>e-ink 设备缺乏自然的 AI 交互方式，传统聊天 UI 不适合墨水屏，手写输入和回复过程繁琐且无沉浸感。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">在 <code class="code-ref">src/main.rs</code> 中定义的状态机（<code class="code-ref">State</code> 枚举）管理了从 Listening、Drinking、Thinking、Replying 到 Lingering 和 FadingReply 的完整交互周期。主循环在 <code class="code-ref">src/main.rs</code> 的 <code class="code-ref">run()</code> 函数中，不断通过 <code class="code-ref">src/pen.rs</code> 的 <code class="code-ref">PenDevice::drain()</code> 获取原始压感笔划，累积成 Ink 对象。空闲 2.8 秒后，<code class="code-ref">src/ink.rs::to_png()</code> 将笔迹区域渲染为灰度 PNG，同时调用 <code class="code-ref">src/oracle.rs::Oracle::ask()</code> 将图片和记忆上下文发送至 LLM（支持 HTTP 和 pi 两种后端），立即启动「喝墨水」溶解动画（<code class="code-ref">src/ink.rs::dissolve_pass()</code>）。LLM 流式返回的文本经 <code class="code-ref">src/oracle.rs::StreamParser</code> 解析，在 <code class="code-ref">src/main.rs</code> 的 Replying 状态中通过逐笔触动画写出（<code class="code-ref">src/script.rs</code> 先将字体光栅化，经 Zhang-Suen 细化，再追踪为笔划路径）。</p>
<p class="audit-callout audit-callout--highlight">延迟隐藏设计。在用户停笔瞬间（<code class="code-ref">src/main.rs</code> 中 <code class="code-ref">IDLE_COMMIT</code> 触发），即发起 Oracle 请求，同时开始 14 步溶解动画；LLM 首句到来时直接切入书写动画，实测首笔延迟可低至 0.9 秒。</p>
<p class="audit-callout audit-callout--highlight">基于精确笔划的「记忆」复苏。<code class="code-ref">src/memory.rs</code> 以原始坐标和半径存储每一笔，回复分析后存入 index.tsv。当 LLM 指令 <code class="code-ref">⟦show:N⟧</code> 出现，<code class="code-ref">src/main.rs</code> 的 <code class="code-ref">conjure()</code> 读取对应 <code class="code-ref">.strokes</code> 文件，以渐淡黑色在原有笔迹上逐笔动画复现，实现「页面从纸面升起」的物理感。</p>
<p class="audit-callout audit-callout--doubt">错误恢复不足。<code class="code-ref">src/oracle.rs</code> 的 <code class="code-ref">HttpOracle::ask()</code> 对网络错误仅通过 channel 传回错误字符串，无自动重试；<code class="code-ref">src/main.rs</code> 的 <code class="code-ref">oracle_excuse()</code> 虽给出友好提示，但用户需重新书写，体验中断。</p>
<p class="audit-callout audit-callout--doubt">电源管理健壮性。<code class="code-ref">src/power.rs</code> 的 <code class="code-ref">suspend_count()</code> 循环重试挂起，但依赖内核计数器，若 EPD 放电计时器持续阻止，无降级措施，可能导致唤醒后页面丢失。</p>
<p>作为墨水屏设备上 LLM 对话的优雅原型，可考虑抽象出通用手势-动画-流式回复框架，但需增强重试策略和跨设备兼容性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 reMarkable Paper Pro（ferrari, aarch64），其他机型未测试，兼容性极窄。</li><li>需要 root 权限和修改系统，存在变砖风险；恢复依赖 SSH 通畅，对普通用户不友好。</li><li>LLM API 费用随记忆增长（每次请求带历史页面和图片），长期使用成本高，无本地模型替代。</li><li>项目初创，仅单一维护者，bus factor 极高，后续维护不确定。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可成为 reMarkable 生态中的杀手级应用，吸引文艺用户，并通过 remagic 分发渠道简化安装，具备口碑传播潜力。但局限于小众硬件，商业化规模有限。</p>
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
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.7</span>
  </div>
</div>
</section>