---
title: '[Score: 75.6] tastyeffectco/sandboxes'
date: '2026-06-04T14:54:20Z'
categories:
- Self-Hosted Sandbox Orchestration
tags:
- Docker
- Go
- SQLite
- Traefik
- Multi-tenant
- Preview Environments
intel_score: 75.6
repo_name: tastyeffectco/sandboxes
repo_link: https://github.com/tastyeffectco/sandboxes
summary: 基于 Go 单进程 + SQLite + Traefik 的多租户容器沙箱编排引擎，面向 AI 应用构建平台提供开箱即用的隔离预览环境、休眠唤醒与编码任务调度。
code_source: git
code_files_reviewed:
- control-plane/go.mod
- control-plane/Dockerfile
- docker-compose.yml
- image/Dockerfile
- control-plane/cmd/runtimed/main.go
- control-plane/cmd/sandboxd/main.go
- control-plane/migrations/0008_drop_agent_config.sql
- control-plane/internal/activity/inode_linux.go
- control-plane/migrations/0010_git_remote.sql
- control-plane/migrations/0007_agent_config_provider.sql
- control-plane/migrations/0003_container_ip.sql
- control-plane/migrations/0006_agent_config.sql
- traefik/dynamic/auth.yml
- control-plane/internal/api/llmtxt.go
- traefik/dynamic/api.yml
- traefik/dynamic/wake.yml
- image/build.sh
- image/etc/profile.d/sandbox-env.sh
- control-plane/cmd/runtimed/server.go
- control-plane/migrations/0005_tasks.sql
- control-plane/internal/reaper/cgmem.go
- control-plane/internal/runtime/client_test.go
- control-plane/internal/auth/token.go
- control-plane/migrations/0002_activity.sql
- control-plane/internal/reaper/meminfo.go
- control-plane/migrations/0009_snapshots.sql
- traefik/traefik.yml
- control-plane/internal/idlock/idlock.go
- control-plane/internal/snapshot/prune.go
- control-plane/internal/activity/inflight_exec.go
- CONTRIBUTING.md
- control-plane/migrations/0001_init.sql
- control-plane/internal/api/preview_common.go
- control-plane/internal/store/migrate.go
- control-plane/internal/api/claim.go
- control-plane/internal/api/preview_auth.go
- control-plane/internal/runtime/protocol.go
- control-plane/internal/logging/logging.go
- control-plane/internal/cgroup/cgroup.go
- control-plane/internal/egress/sources.go
- control-plane/cmd/runtimed/workspace.go
- control-plane/cmd/runtimed/health_test.go
- control-plane/README.md
- control-plane/internal/auth/config.go
- control-plane/migrations/0004_external_identity.sql
- control-plane/internal/wake/admit.go
- control-plane/internal/audit/log.go
- control-plane/internal/egress/refresh_watch.go
code_chars_analyzed: 123029
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
      <span class="scope-stat__value">约 123,029 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">control-plane/go.mod</code></li><li><code class="path-chip">control-plane/Dockerfile</code></li><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">image/Dockerfile</code></li><li><code class="path-chip">control-plane/cmd/runtimed/main.go</code></li><li><code class="path-chip">control-plane/cmd/sandboxd/main.go</code></li><li><code class="path-chip">control-plane/migrations/0008_drop_agent_config.sql</code></li><li><code class="path-chip">control-plane/internal/activity/inode_linux.go</code></li><li><code class="path-chip">control-plane/migrations/0010_git_remote.sql</code></li><li><code class="path-chip">control-plane/migrations/0007_agent_config_provider.sql</code></li><li><code class="path-chip">control-plane/migrations/0003_container_ip.sql</code></li><li><code class="path-chip">control-plane/migrations/0006_agent_config.sql</code></li><li><code class="path-chip">traefik/dynamic/auth.yml</code></li><li><code class="path-chip">control-plane/internal/api/llmtxt.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>构建 AI 应用生成平台（类 Lovable/Bolt）的团队，需要为每个用户维护独立 Linux 容器、自动预览 URL、空闲回收与按需唤醒，从零搭建这套基础设施成本高且容易在多租户隔离和内存控制上出错。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整体是一个「双守护进程 + 反向代理」架构。宿主侧 sandboxd（<code class="code-ref">control-plane/cmd/sandboxd/main.go</code>）通过 shell-out 调用 <code class="code-ref">docker</code> CLI 创建/销毁容器，SQLite 持久化状态，Traefik 负责 preview URL 路由。容器内侧 runtimed（<code class="code-ref">control-plane/cmd/runtimed/main.go</code>）作为容器主进程，通过 Unix domain socket 暴露 /status 和 POST /tasks 端点（<code class="code-ref">control-plane/cmd/runtimed/server.go:18-40</code>）。sandboxd 在启动时执行 reconcile 一次收敛 Docker 状态到数据库（<code class="code-ref">control-plane/cmd/sandboxd/main.go</code> reconcile.Once 调用处），并通过后台 goroutine 运行 idle reaper、pressure reaper 和 access-log tailer。wake 路径通过 Traefik 的 catch-all 路由（priority=1，<code class="code-ref">traefik/dynamic/wake.yml</code>）将停止状态沙箱的请求转发给 sandboxd，由 wake handler 执行 docker start 后反代请求。</p>
<p class="audit-callout audit-callout--highlight">内存压力感知的 wake 准入机制实现严谨。<code class="code-ref">control-plane/internal/wake/admit.go</code> 中 Admit 函数先读 /proc/meminfo 计算成本百分比，不足时同步调用 pressure reaper tick 释放内存再二次检查，配合 atomic.Bool 的 refused 标志避免重复触发，形成完整的两阶段准入流程。这比简单粗暴的「满了就拒绝」多了一层主动回收。</p>
<p class="audit-callout audit-callout--highlight">runtimed 的 dev server 健康探测链路设计细致。<code class="code-ref">control-plane/cmd/runtimed/main.go</code> 的 probeLoop 每 3 秒探测 HTTP 端口，200 后还会调用 probeEntryAssets 检查入口模块是否真正编译成功，区分 PreviewReady（正常）和 PreviewError（壳加载了但 JS 编译失败白屏）两种状态，避免对用户展示假的「ready」。</p>
<p class="audit-callout audit-callout--doubt">sandboxd 的 main 函数长达约 600 行（<code class="code-ref">control-plane/cmd/sandboxd/main.go</code>），所有初始化逻辑、goroutine 启动、信号处理均在一个函数中完成，缺少对内部状态的结构化封装。尽管注释丰富可读，但随着功能增长（Phase 5/6/7/8 已堆积在同一函数），维护成本将显著上升。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">control-plane/internal/docker/</code>、<code class="code-ref">control-plane/internal/store/</code>（除 migrate.go）、<code class="code-ref">control-plane/internal/reconcile/</code>、<code class="code-ref">control-plane/internal/loopback/</code> 等核心包的源码，这些是容器操作、存储层和协调器的关键实现，本次结论不覆盖其错误处理与并发安全性。</p>
<p>若用于生产，需重点关注三点：(1) 代码包中 48/145 文件被采集，核心 docker wrapper、store、reconciler、wake handler 主体逻辑缺失，部署前需补审；(2) 默认 AUTH_DISABLED=true 且无 TLS，裸跑在公网即等于无认证暴露 API；(3) egress 管控（nftables）在 OSS 构建中被完全禁用（<code class="code-ref">control-plane/cmd/sandboxd/main.go</code> egressMgr = nil），沙箱容器的出站流量无任何限制。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>默认 SANDBOXD_API_AUTH_DISABLED=true 且 README 未强调生产必须配置 token，裸部署等于无认证 API。</li><li>48/145 源码文件被采集，docker wrapper、store、reconciler、loopback、wake handler 主体未审阅，工程分受限。</li><li>egress 管控（nftables）在 OSS 构建中完全禁用，沙箱内 AI agent 代码可无限制外连，存在数据泄露风险。</li><li>fork_star_ratio 仅 1.85%（324 star / 6 fork），围观型项目特征明显，社区实际采用尚待验证。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对正在构建 AI 应用生成器（v0/Lovable/Bolt 类产品）的团队有直接价值，可以将数月的平台工程工作压缩为一次部署；但 SQLite 单文件 + 单机架构决定了其扩展上限，适合早期产品验证而非大规模 SaaS。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.6</span>
  </div>
</div>
</section>