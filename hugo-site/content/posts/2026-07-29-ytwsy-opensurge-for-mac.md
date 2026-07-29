---
title: '[Score: 77.3] YTwsy/OpenSurge-for-Mac'
date: '2026-07-29T05:49:13Z'
categories:
- Network Gateway
tags:
- macOS
- proxy
- gateway
- mihomo
- dnsmasq
- DHCP
- TUN
- home-networking
intel_score: 77.3
repo_name: YTwsy/OpenSurge-for-Mac
repo_link: https://github.com/YTwsy/OpenSurge-for-Mac
summary: 将 Mac 变成支持 DHCP/DNS 接管的全屋透明代理网关，为手机、游戏机等设备提供免配置出海通道。
code_source: git
code_files_reviewed:
- go.mod
- web/package.json
- Makefile
- .github/workflows/ci.yml
- .github/workflows/release-unsigned.yml
- cmd/opensurge-helper/main.go
- cmd/opensurge-install-config/main.go
- cmd/opensurge-control/main.go
- cmd/opensurge-network/main.go
- tests/integration/egressprobe/main.go
- cmd/omg/main.go
- internal/sysctl/ipforward_test.go
- internal/device/model.go
- apps/menubar/Package.swift
- internal/process/process_test.go
- internal/config/profile_digest.go
- internal/macosnetwork/dhcp_test.go
- internal/process/command_test.go
- internal/macosnetwork/neighbors_test.go
- internal/webui/embed.go
- internal/gateway/status_test.go
- cmd/opensurge-network/main_test.go
- internal/dhcp/leases_test.go
- internal/device/scanner_test.go
- internal/pf/template.go
- internal/sysctl/ipforward.go
- internal/config/render_test.go
- internal/device/bundle_test.go
- internal/runtime/paths.go
- internal/macosnetwork/neighbors.go
- internal/mihomo/manager_test.go
- internal/runtime/state.go
- internal/installconfig/installconfig_test.go
- internal/dhcp/leases.go
- internal/process/command.go
- internal/dhcp/dnsmasq.go
- internal/device/scanner.go
- internal/gateway/reservation_conflicts.go
- internal/runtime/state_test.go
- internal/process/process.go
- internal/config/render.go
- internal/dhcp/template.go
- internal/controlapi/proxy_health_test.go
- internal/gateway/status.go
- internal/pf/manager.go
- internal/pf/template_test.go
- internal/controlapi/credentials_test.go
- internal/controlapi/proxy_health.go
code_chars_analyzed: 112920
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
      <span class="scope-stat__value">约 112,920 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release-unsigned.yml</code></li><li><code class="path-chip">cmd/opensurge-helper/main.go</code></li><li><code class="path-chip">cmd/opensurge-install-config/main.go</code></li><li><code class="path-chip">cmd/opensurge-control/main.go</code></li><li><code class="path-chip">cmd/opensurge-network/main.go</code></li><li><code class="path-chip">tests/integration/egressprobe/main.go</code></li><li><code class="path-chip">cmd/omg/main.go</code></li><li><code class="path-chip">internal/sysctl/ipforward_test.go</code></li><li><code class="path-chip">internal/device/model.go</code></li><li><code class="path-chip">apps/menubar/Package.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>手机、游戏机、电视等设备无法直接安装代理客户端，通常需要复杂路由器配置或手动设置代理，OpenSurge 可一键将 Mac 变成网关，为所有设备提供透明代理和策略控制。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目以 Go 为核心实现控制面，通过 <code class="code-ref">cmd/opensurge-control</code> 提供 REST API 和 Web GUI，<code class="code-ref">cmd/omg</code> 提供完整 CLI。底层依赖 mihomo 作为代理引擎、dnsmasq 提供 DHCP/DNS，通过 <code class="code-ref">internal/pf/manager.go</code> 管理 macOS pf 防火墙实现 NAT 与透明代理，<code class="code-ref">internal/sysctl/ipforward.go</code> 控制 IP 转发。状态持久化在 <code class="code-ref">internal/runtime/state.go</code>，使用原子写入确保一致性。</p>
<p class="audit-callout audit-callout--highlight">每设备策略通过 JSON 文件定义设备绑定、策略组和规则覆盖，<code class="code-ref">internal/device/bundle.go</code> 编译策略并生成 <code class="code-ref">device-policy.applied.json</code>，代码在 <code class="code-ref">internal/device/bundle_test.go:15</code> 验证了快照的往返一致性和完整性，设计清晰。</p>
<p class="audit-callout audit-callout--highlight">网关生命周期管理健全，<code class="code-ref">internal/gateway/status.go:32</code> 的 <code class="code-ref">Status</code> 方法综合 dnsmasq、mihomo、pf 和 IP 转发状态，提供可读的状态报告，且 <code class="code-ref">internal/runtime/state.go</code> 使用临时文件原子写入，避免了宕机丢失状态。</p>
<p class="audit-callout audit-callout--doubt">网络探测严重依赖外部命令输出解析，例如 <code class="code-ref">internal/macosnetwork/neighbors.go:32</code> 的 <code class="code-ref">arp -an</code> 输出解析，macOS 不同版本可能存在格式变动，且未见对解析逻辑的系统兼容性测试，可能导致未来兼容性隐患。</p>
<p class="audit-callout audit-callout--doubt">README 宣称“AI Agent 友好工作区”与“验证工作区”，但提供的源码中未发现相应的实现或生成逻辑，仅在文档中提及，降低了该特性的可信度，实际工程中未见体现。</p>
<p>应增加对系统命令输出的兼容性测试矩阵，并明确 Agent 工作区的具体实现路径，如自动化证据生成、配置校验闭环等，否则将削弱项目在技术社区中的长期竞争力。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>发布包未签名，普通用户需绕过 Gatekeeper，安装门槛较高。</li><li>依赖外部 mihomo/dnsmasq 二进制，上游变更可能导致兼容问题。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可成为家庭网络管理的实用工具，吸引海外网络访问需求用户，通过提供稳定版或托管服务可能产生收入，但目前依赖社区贡献，商业路径尚不清晰。</p>
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
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.3</span>
  </div>
</div>
</section>