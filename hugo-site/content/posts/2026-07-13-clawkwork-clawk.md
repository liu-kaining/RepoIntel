---
title: '[Score: 78.15] clawkwork/clawk'
date: '2026-07-13T19:19:51Z'
categories:
- AI Agent Sandbox
tags:
- ai-agent
- sandbox
- virtualization
- go
- dev-tools
- security
intel_score: 78.15
repo_name: clawkwork/clawk
repo_link: https://github.com/clawkwork/clawk
summary: clawk 为 AI 编码代理提供一次性 Linux VM 沙箱，一键启动即享有 root 权限，隔离主机文件与网络，避免手动审批。
code_source: git
code_files_reviewed:
- machine/Makefile
- Makefile
- machine/go.mod
- go.mod
- images/clawk-dev/Dockerfile
- .github/workflows/ci.yml
- .github/workflows/build-guest-kernel.yml
- .github/workflows/release.yml
- .github/workflows/publish-clawk-dev.yml
- machine/cmd/smoke-firecracker/main.go
- cmd/clawk/main.go
- machine/cmd/smoke-alpine/main.go
- internal/sandbox/loop_mount_stub.go
- internal/cli/vzd_stub.go
- internal/cli/doctor_other.go
- internal/cli/hostmem_darwin.go
- internal/cli/image_unix.go
- internal/sandbox/image.go
- internal/template/template_test.go
- internal/sandbox/credentials_other.go
- internal/debug/debug.go
- internal/cli/list_image_test.go
- internal/sandbox/guestnet.go
- internal/cli/hostmem_linux.go
- internal/cli/providers_darwin.go
- internal/cli/agent_docs_test.go
- internal/config/types_test.go
- internal/sandbox/exit.go
- internal/cli/agent_docs.go
- internal/sandbox/console.go
- internal/cli/providers_linux.go
- internal/sandbox/console_test.go
- internal/cli/image_ref_test.go
- internal/config/namespace_test.go
- internal/sandbox/credentials_darwin.go
- internal/cli/resources_test.go
- internal/sandbox/mock.go
- internal/guestcfg/ninep_test.go
- internal/cli/observe.go
- internal/cli/migrate_test.go
- internal/vsockclient/reset_test.go
- internal/template/template.go
- internal/sandbox/guestabi_test.go
- internal/guestcfg/manifest_test.go
- internal/sandbox/ninep_shares_test.go
- internal/vsockclient/ping.go
- internal/vsockclient/output.go
- internal/cli/migrate.go
code_chars_analyzed: 70783
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
      <span class="scope-stat__value">约 70,783 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">machine/Makefile</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">machine/go.mod</code></li><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">images/clawk-dev/Dockerfile</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/build-guest-kernel.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">.github/workflows/publish-clawk-dev.yml</code></li><li><code class="path-chip">machine/cmd/smoke-firecracker/main.go</code></li><li><code class="path-chip">cmd/clawk/main.go</code></li><li><code class="path-chip">machine/cmd/smoke-alpine/main.go</code></li><li><code class="path-chip">internal/sandbox/loop_mount_stub.go</code></li><li><code class="path-chip">internal/cli/vzd_stub.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在让 Claude Code 等代理自由执行命令时，要么频繁审批权限（效率低），要么冒险使用 --dangerously-skip-permissions（泄漏风险），clawk 用独立的虚拟机取代规则提示，彻底隔离破坏和泄露。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">命令行通过 Cobra 入口 <code class="code-ref">cmd/clawk/main.go</code> 启动，在 <code class="code-ref">internal/cli</code> 中解析 <code class="code-ref">clawk.mod</code> 模板，组装 <code class="code-ref">config.Sandbox</code> 结构。根据平台选择虚拟机提供者：macOS 使用 Apple Virtualization.framework 的后端 <code class="code-ref">vz</code>，Linux 使用 <code class="code-ref">firecracker</code>（见 <code class="code-ref">internal/cli/providers_darwin.go</code> 和 <code class="code-ref">providers_linux.go</code>）。随后调用 <code class="code-ref">sandbox.Provider</code> 接口的 <code class="code-ref">Create</code> 和 <code class="code-ref">Start</code>，其内部通过 <code class="code-ref">machine</code> 模块构建 OCI 镜像根文件系统并启动 VM，挂载宿主工作目录（virtio-fs）。Guest 内核启动后，<code class="code-ref">clawk-init</code> 通过 vsock 与主机通信，提供 pty-agent 交互会话。网络出口经过 fork 的 <code class="code-ref">gvisor-tap-vsock</code>（见 <code class="code-ref">go.mod</code> 替换），在转发前依据白名单放行（配置在 <code class="code-ref">internal/sandbox/guestnet.go</code> 中定义网关为 192.168.127.1）。</p>
<p class="audit-callout audit-callout--highlight">跨平台双引擎设计。<code class="code-ref">machine/cmd/smoke-alpine/main.go</code> 直接使用 <code class="code-ref">machine.Get(&quot;vz&quot;)</code> 启动 vz 后端实现的 VM，展示了 DirctKernel 启动路径；<code class="code-ref">machine/cmd/smoke-firecracker/main.go</code> 则通过 <code class="code-ref">machine.Get(&quot;firecracker&quot;)</code> 在 Linux 上启动 Firecracker 后端。两者共享相同的 <code class="code-ref">machine.Spec</code> 结构，上层代码完全平台无关。</p>
<p class="audit-callout audit-callout--highlight">出口网络白名单机制。在 <code class="code-ref">go.mod</code> 中，项目使用自己的 <code class="code-ref">clawkwork/gvisor-tap-vsock</code> 分支（<code class="code-ref">replace</code> 指令），对 TCP/UDP/ICMP 转发增加 egress allow-list 检查，而非仅依赖 Agent 的系统提示，使网络隔离提升到虚拟机层面。</p>
<p class="audit-callout audit-callout--doubt">核心虚拟机创建/销毁逻辑深藏于 <code class="code-ref">machine</code> 模块（未审阅到具体文件如 <code class="code-ref">machine/vz/...</code>），仅看到 smoke 测试和接口定义，无法判断资源管理、错误恢复等生产级细节。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖偏重单元测试（如 <code class="code-ref">internal/sandbox/console_test.go</code>、<code class="code-ref">internal/guestcfg/manifest_test.go</code>），CI 中 <code class="code-ref">TEST_GUEST_BOOT</code> 门控的端到端启动测试未默认运行（见 <code class="code-ref">.github/workflows/ci.yml</code>），集成验证不足。</p>
<p>可作为个人开发者安全运行 Agent 的快速方案，但需留意 macOS 签名要求（必须 <code class="code-ref">codesign</code> 授权 <code class="code-ref">com.apple.security.virtualization</code>），且应定期更新以应对 Pre-1.0 的不兼容变更。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>安全模型已明确：允许的 git 服务器可导致代码外泄；出口白名单仅阻断未知连接，无法防止数据经 github.com 等授权域泄漏。</li><li>Pre-1.0 阶段频繁 breaking changes，生产环境使用风险高；Linux 支持标记为实验性，兼容性未经充分验证。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向日益增长的 AI 编码代理用户，提供开箱即用的安全沙箱，未来可能成为 Claude Code 等工具的推荐本地运行方案，并衍生出团队协作、CI 集成等商业服务。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.15</span>
  </div>
</div>
</section>