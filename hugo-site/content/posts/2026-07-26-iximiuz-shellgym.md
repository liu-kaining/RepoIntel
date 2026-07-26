---
title: '[Score: 77.2] iximiuz/shellgym'
date: '2026-07-26T05:58:21Z'
categories:
- Linux CLI Trainer
tags:
- linux
- shell
- training
- go
- procfs
intel_score: 77.2
repo_name: iximiuz/shellgym
repo_link: https://github.com/iximiuz/shellgym
summary: 一个将真实 Linux 终端变为交互式命令行训练器的后台守护进程，帮助初学者通过即时反馈练习基本功。
code_source: git
code_files_reviewed:
- go.mod
- Makefile
- .github/workflows/release.yml
- cmd/shellgym/main.go
- internal/bus/bus.go
- internal/bus/bus_test.go
- cmd/shellgym/skills.go
- internal/content/live_test.go
- internal/engine/shells_test.go
- internal/content/distro.go
- internal/content/vars_test.go
- internal/content/live.go
- internal/content/vars.go
- internal/engine/runner_test.go
- internal/state/state_test.go
- internal/engine/execwatch_test.go
- internal/engine/shells.go
- internal/content/markdown_test.go
- cmd/shellgym/serve.go
- internal/content/model.go
- internal/engine/runner.go
- internal/engine/checkapi.go
- internal/content/markdown.go
- cmd/shellgym/solve.go
- internal/state/state.go
- internal/content/loader_test.go
- internal/content/loader.go
- internal/engine/execwatch.go
- internal/checkclient/checkclient.go
- internal/engine/engine.go
- internal/engine/integration_test.go
- skills/embed.go
- paths/sample-linux-101/030.files-and-folders/module.md
- paths/sample-linux-101/path.yaml
- paths/sample-linux-101/060.networking-basics/module.md
- paths/sample-linux-101/070.package-tools/module.md
- paths/sample-linux-101/050.processes-and-signals/module.md
- paths/sample-linux-101/080.final-lap/module.md
- paths/sample-linux-101/040.redirection-and-pipes/module.md
- ui/tui/tui.go
- paths/sample-linux-101/020.moving-around/module.md
- e2e/start.sh
- paths/sample-linux-101/010.orientation/module.md
- paths/sample-linux-101/030.files-and-folders/010.make-a-home/unit.md
- .goreleaser.yaml
- paths/sample-linux-101/070.package-tools/010.refresh-the-index-apt/unit.md
- paths/sample-linux-101/050.processes-and-signals/010.background-hum/unit.md
- paths/sample-linux-101/070.package-tools/020.refresh-the-index-dnf/unit.md
code_chars_analyzed: 161083
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
      <span class="scope-stat__value">约 161,083 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">cmd/shellgym/main.go</code></li><li><code class="path-chip">internal/bus/bus.go</code></li><li><code class="path-chip">internal/bus/bus_test.go</code></li><li><code class="path-chip">cmd/shellgym/skills.go</code></li><li><code class="path-chip">internal/content/live_test.go</code></li><li><code class="path-chip">internal/engine/shells_test.go</code></li><li><code class="path-chip">internal/content/distro.go</code></li><li><code class="path-chip">internal/content/vars_test.go</code></li><li><code class="path-chip">internal/content/live.go</code></li><li><code class="path-chip">internal/content/vars.go</code></li><li><code class="path-chip">internal/engine/runner_test.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>阅读 Linux 教程后仍无法熟练操作命令行的开发者，需要一个无需记忆检查按钮、在真实 shell 中提供即时反馈的练习环境。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">从 <code class="code-ref">cmd/shellgym/serve.go</code> 的 serve 函数可见，启动时先加载学习路径（content.Load），初始化状态存储（state.Open），创建 exec watcher 并通过 netlink 监听进程 exec 事件；随后搭建 unix socket API（engine.ServeCheckAPI）供 check shim 调用，最后启动 Engine 并恢复进度、运行 Web UI。Engine 为每个单元解析变量、执行初始化任务，并监督 edge/level 两类任务脚本，任务脚本通过 bus 发布状态变化。</p>
<p class="audit-callout audit-callout--highlight">零仪器化 exec 监控。<code class="code-ref">internal/engine/execwatch.go</code> 的 Start 函数（约58行）通过 netlink proc connector 订阅进程事件，并发 harvestProc 读取 /proc 中的 argv 和环境变量，完全不修改学生 shell。这使得 wait_exec 检查能够精确匹配用户输入的命令。</p>
<p class="audit-callout audit-callout--highlight">可扩展的学习路径格式。<code class="code-ref">internal/content/loader.go</code> 和 model.go 定义了一套基于目录结构的课程格式，支持 YAML 前端、任务依赖（needs）、变量随机化与跨单元继承（vars.from），且 --live 模式会通过 <code class="code-ref">internal/content/live.go</code> 的 StripSolveScripts 自动移除求解脚本，防止学生偷看。</p>
<p class="audit-callout audit-callout--doubt">执行监控强依赖 root 与 CAP_NET_ADMIN。execwatch.go:58 处若打开 proc connector 失败会直接导致 daemon 退出，这限制了在非特权容器或共享机器上的使用，与 README 强调的“disposable host”一致，但仍有安全与部署隐患。</p>
<p class="audit-callout audit-callout--doubt">进度持久化未保存系统状态快照。<code class="code-ref">internal/state/state.go</code> 将单元状态、变量和运行记录写入磁盘，但若学生重启后文件被清理或进程消失，进度可能失效。README 也指出恢复依赖系统状态保存，这是设计上的风险。</p>
<p>适合集成到在线沙盒平台（如 iximiuz Labs）或本地 VM 中，配合自动验收脚本（shellgym solve）可实现 CI 化技能评测。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>必须 root 权限运行，无法用于单机多用户安全隔离场景。</li><li>学习路径创作需手动编写 YAML/MD，非开发者使用门槛较高。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可作为 Linux 在线培训平台的练习组件，减少人工辅导成本；企业可用于新员工技能培训与评测。</p>
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
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.2</span>
  </div>
</div>
</section>