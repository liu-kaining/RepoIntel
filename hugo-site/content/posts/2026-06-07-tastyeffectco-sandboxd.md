---
title: '[Score: 75.3] tastyeffectco/sandboxd'
date: '2026-06-07T19:18:58Z'
categories:
- Self-hosted Sandbox Platform
tags:
- Docker
- Go
- SQLite
- Traefik
- AI Agent
- Preview Environment
intel_score: 75.3
repo_name: tastyeffectco/sandboxd
repo_link: https://github.com/tastyeffectco/sandboxd
summary: 面向 AI 应用构建器的自托管沙箱平台，单机 Docker 运行，为每个用户提供隔离容器、编码代理和实时预览 URL，适合 SaaS 工厂和 Agent
  平台开发者。
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
code_chars_analyzed: 122938
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
      <span class="scope-stat__value">约 122,938 字符</span>
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
<p>AI 应用构建类产品（如 Lovable、Bolt）需要为每个用户创建隔离开发环境、运行编码代理并生成可访问预览链接；自行搭建这套基础设施涉及多租户隔离、URL 路由、空闲回收、容器编排，通常需要数月平台工程投入。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">sandboxd 由两个 Go 进程组成——宿主机端的 <code class="code-ref">control-plane/cmd/sandboxd/main.go</code> 控制平面和容器内的 <code class="code-ref">control-plane/cmd/runtimed/main.go</code> 监督进程。控制平面通过 <code class="code-ref">control-plane/internal/docker</code> 包 shell out 到 <code class="code-ref">docker</code> CLI 管理容器生命周期，状态持久化在 SQLite（<code class="code-ref">control-plane/internal/store/migrate.go</code>），并通过 <code class="code-ref">control-plane/internal/reconcile</code> 在启动时将 Docker 实际状态收敛到数据库。Traefik 作为边缘路由，通过 Docker label 自动为每个沙箱生成预览 URL（<code class="code-ref">traefik/traefik.yml:42</code> 的 constraints 配置仅路由带 <code class="code-ref">sandboxd.managed=true</code> 标签的容器）。runtimed 作为沙箱内主进程通过 Unix domain socket 暴露 <code class="code-ref">/status</code>、<code class="code-ref">POST /tasks</code>、<code class="code-ref">GET /tasks/{id}/events</code> 等端点（<code class="code-ref">control-plane/cmd/runtimed/server.go:31-38</code>），与宿主机控制平面通信。</p>
<p class="audit-callout audit-callout--highlight">空闲回收与内存压力管理设计精细——<code class="code-ref">control-plane/internal/reaper/meminfo.go</code> 解析 <code class="code-ref">/proc/meminfo</code> 获取 MemAvailable，<code class="code-ref">control-plane/internal/reaper/cgmem.go</code> 读取 cgroup v2 的 <code class="code-ref">memory.current</code>，<code class="code-ref">control-plane/internal/wake/admit.go:51-82</code> 实现了二次读取+同步压力回收的准入算法，在内存不足时先触发一次 pressure tick 停掉空闲沙箱再决定是否放行新 wake。</p>
<p class="audit-callout audit-callout--highlight">认证与安全层有实货——<code class="code-ref">control-plane/internal/auth/token.go:26-35</code> 使用 <code class="code-ref">crypto/subtle.ConstantTimeCompare</code> 做常量时间 token 比较且不提前 break，<code class="code-ref">control-plane/internal/api/preview_auth.go:43-52</code> 对 return URL 做严格 allowlist 校验防止开放重定向，<code class="code-ref">control-plane/internal/api/preview_common.go:56-65</code> 的 <code class="code-ref">validateReturnURL</code> 将 sandbox_id 与 JWT claims 绑定。</p>
<p class="audit-callout audit-callout--doubt">控制平面 <code class="code-ref">cmd/sandboxd/main.go</code> 单文件超过 500 行，将启动、环境变量解析、后台 goroutine 管理、HTTP 路由、信号处理全部堆在一个 <code class="code-ref">main()</code> 函数中，缺乏结构化拆分。<code class="code-ref">cmd/sandboxd/main.go:200-350</code> 的 env 解析与后台 goroutine 启动代码交织在一起，增加维护成本。</p>
<p class="audit-callout audit-callout--doubt">code_bundle 中未审阅到 <code class="code-ref">control-plane/internal/docker/</code>、<code class="code-ref">control-plane/internal/store/</code>（除 migrate.go 外的 CRUD 实现）、<code class="code-ref">control-plane/internal/wake/</code> 的完整 handler、<code class="code-ref">control-plane/internal/reconcile/</code>、<code class="code-ref">control-plane/internal/loopback/</code> 等核心包的源码。这些是沙箱创建、存储查询、wake 路径的核心逻辑，本次结论不覆盖其具体实现质量。</p>
<p>适合已有 AI 应用构建器产品、需要自建沙箱后端替代云厂商方案的团队；部署前需评估单机承载上限（README 未给出基准数据），并在生产环境启用 <code class="code-ref">SANDBOXD_API_AUTH_DISABLED=false</code> 配置 token 认证。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仓库仅创建 4 天、最近 2 次 commit，核心代码大量未在 code_bundle 中提供，成熟度存疑</li><li>默认 <code class="code-ref">SANDBOXD_API_AUTH_DISABLED=true</code>（docker-compose.yml:56），初次部署若未配置 token 则 API 完全裸露</li><li>控制平面通过 shell out 调用 docker CLI（CONTRIBUTING.md:28），高并发场景下 exec 开销和错误处理未经验证</li><li>单机架构无水平扩展能力，SQLite 写锁在多 goroutine 并发写入场景下存在瓶颈风险</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 AI 编码代理和 SaaS 工厂提供了一个轻量级自托管替代方案，可降低对 Replit/Lovable 等平台基础设施层的依赖；在 self-hosted 趋势下有明确的集成场景，但商业化路径依赖上层产品能否跑通。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">64</div>
  <div class="score-bar"><span style="width:64%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.3</span>
  </div>
</div>
</section>