---
title: '[Score: 78.4] hanxiao/dataroom'
date: '2026-06-04T14:54:20Z'
categories:
- Local LLM Research Harness
tags:
- LLM agent
- research automation
- llama.cpp
- embedding index
- self-hosted
- FastAPI
intel_score: 78.4
repo_name: hanxiao/dataroom
repo_link: https://github.com/hanxiao/dataroom
summary: 用本地 Qwen3.6-35B + Pi 代理循环搜索-阅读-写入，自动构建结构化研究资料库并输出 .zip，适合需要大量前置调研但不想烧前沿 token
  的工程师。
code_source: git
code_files_reviewed:
- server/requirements.txt
- Dockerfile
- docker-compose.yml
- .github/workflows/build-and-push.yml
- server/app.py
- server/index_service.py
- server/stats.py
- server/run_dataroom.py
- scripts/deploy.sh
- scripts/create_instance.sh
- pi/extensions/dataroom-index.ts
- scripts/mac-run.sh
- skills/use-dataroom/SKILL.md
- docs/MAC.md
- scripts/setup-win.sh
- docs/DEPLOY.md
- scripts/setup.sh
- pi/skills/dataroom/SKILL.md
- tests/test_scheduler.py
- README.md
code_chars_analyzed: 162535
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
      <span class="scope-stat__value">20 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 162,535 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">server/requirements.txt</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">.github/workflows/build-and-push.yml</code></li><li><code class="path-chip">server/app.py</code></li><li><code class="path-chip">server/index_service.py</code></li><li><code class="path-chip">server/stats.py</code></li><li><code class="path-chip">server/run_dataroom.py</code></li><li><code class="path-chip">scripts/deploy.sh</code></li><li><code class="path-chip">scripts/create_instance.sh</code></li><li><code class="path-chip">pi/extensions/dataroom-index.ts</code></li><li><code class="path-chip">scripts/mac-run.sh</code></li><li><code class="path-chip">skills/use-dataroom/SKILL.md</code></li><li><code class="path-chip">docs/MAC.md</code></li><li class="path-more">另有 6 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>长周期任务（实现、竞品分析、技术选型）前的背景调研是机械性搜索-阅读-整理循环，用前沿模型按 token 计费既贵又受预算限制会提前中断；产出的 PDF 报告供人浏览，而非供下游 agent 直接消费。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">FastAPI 应用（<code class="code-ref">server/app.py</code>）接收查询后创建 job，单 worker 线程（<code class="code-ref">server/app.py:116</code> 的 <code class="code-ref">_worker</code>）串行运行任务。每个 job 通过 <code class="code-ref">server/run_dataroom.py</code> 的 <code class="code-ref">drive_rpc</code> 函数启动一个持久 <code class="code-ref">pi --mode rpc</code> 会话（<code class="code-ref">server/run_dataroom.py:238</code>），Pi 代理使用 Qwen3.6-35B（通过 llama.cpp 的 OpenAI 端点）自主循环：搜索（jina CLI）、读取、去重（embedding index sidecar）、写入结构化文件到 <code class="code-ref">dataroom/</code> 目录。orchestrator 监控完成条件（实质性文件数 &gt;= MIN_FILES、STATUS.md 无未关闭问题、SUMMARY.md 存在），过早的 DONE 会被拒绝并注入纠正提示（<code class="code-ref">server/run_dataroom.py:283</code> 的 CORRECTIVE_PROMPT）。每 N 轮注入 CONSOLIDATE_PROMPT 强制合并重复文件。job 完成后自动打包为 .zip。embedding index（<code class="code-ref">server/index_service.py</code>）使用 jina-embeddings-v5-nano 在 CPU 上运行，通过 reconcile 函数（<code class="code-ref">server/index_service.py:158</code>）在每次搜索前将磁盘状态与索引同步，确保去重准确。调度器支持二级抢占式队列：前台 job 优先，无前台时自动回填暂停的 job（<code class="code-ref">server/app.py:183</code> 的 <code class="code-ref">_select_next</code>）。文档注释详尽，关键注释解释了 llama.cpp #21681 cache drift 风险等边界情况。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">server/index_service.py:60</code> 的 <code class="code-ref">reconcile</code> 函数在每次 <code class="code-ref">/search</code> 调用前自动比对磁盘文件哈希与索引，新增/修改的文件自动重新 embed，已删除的文件自动清理，使得 <code class="code-ref">op=add</code> 成为可选快速路径而非必需——即使代理忘记调用 add，索引也不会与磁盘漂移。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">server/app.py:183</code> 的 <code class="code-ref">_select_next</code> 实现了两级优先级调度：前台 job（显式提交/恢复）严格 FIFO，空闲时自动回填暂停 job，且新提交的前台 job 能通过 <code class="code-ref">_preempt_backfill_locked</code> 抢占正在运行的回填 job，确保 GPU 利用率和用户响应性兼顾。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">server/app.py</code> 的 <code class="code-ref">_jobs</code> 字典（内存中）在进程重启后依赖 <code class="code-ref">_recover_queue</code> 从磁盘恢复（<code class="code-ref">server/app.py:308</code>），但只恢复 <code class="code-ref">queued</code>/<code class="code-ref">running</code> 状态的 job，<code class="code-ref">paused</code> 状态的 job 依赖 <code class="code-ref">_paused_on_disk</code> 磁盘扫描。如果 meta.json 写入失败（<code class="code-ref">_save_meta</code> 的异常被静默吞掉，<code class="code-ref">server/app.py:58</code>），job 状态会丢失且无法恢复。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">pi/skills/dataroom/SKILL.md</code> 中代理方法论的执行完全依赖 LLM 遵守指令（如「写前必须搜索索引」），但无程序化强制——小模型可能跳过去重步骤产生重复文件。orchestrator 的 CONSOLIDATE_PROMPT 每 N 轮触发合并，但 N 由环境变量控制且默认值 4 可能导致前期积累大量重复。</p>
<p>生产部署前应增加 <code class="code-ref">_save_meta</code> 的写入原子性（先写临时文件再 rename），防止断电导致 meta.json 损坏。embedding index 的 reconcile 在每次搜索时全量扫描磁盘，对大 dataroom（100+ 文件）可能成为延迟瓶颈，建议增量 hash 检查。测试覆盖仅限调度逻辑（<code class="code-ref">tests/test_scheduler.py</code>），核心的 orchestrator 和 index_service 无单元测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖外部 Jina API key 做 web 搜索/读取/重排，无纯本地替代方案，离线环境无法运行。</li><li>仓库创建仅 4 天、9 次 commit，核心 orchestrator 和 index_service 无单元测试，生产稳定性未验证。</li><li>内存中 _jobs 字典 + 磁盘 meta.json 的状态持久化机制在 _save_meta 异常被静默吞掉时可能丢 job。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>适合需要大量技术调研的 AI 工程团队作为两阶段 pipeline 的第一阶段：本地小模型完成机械性搜索整理，产出的 .zip 直接喂给前沿模型做实现。对 Jina 生态有拉动作用（搜索/读取/嵌入全部走 Jina API）。但强依赖 Jina API key 且无法替换为纯本地搜索，限制了无外网环境的适用性。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.4</span>
  </div>
</div>
</section>