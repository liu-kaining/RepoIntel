---
title: '[Score: 81.8] jianyintang/find-disk-killer'
date: '2026-07-30T08:20:47Z'
categories:
- Developer Tools
tags:
- macOS
- SwiftUI
- Disk I/O
- AI Storage
- SMART
- Privacy
intel_score: 81.8
repo_name: jianyintang/find-disk-killer
repo_link: https://github.com/jianyintang/find-disk-killer
summary: 本地 macOS 磁盘活动监控器，集成进程 I/O、文件追踪、SMART 健康及 AI Agent 存储分析，帮助开发者定位磁盘瓶颈和清理对话数据。
code_source: git
code_files_reviewed:
- Makefile
- .github/workflows/ci.yml
- Sources/CFindDiskKillerTrace/include/CFindDiskKillerTrace.h
- Sources/FindDiskKillerApp/Resources/THIRD_PARTY_ASSETS.md
- docs/releases/1.2.1.md
- Sources/FindDiskKillerClaudeCleanupHelper/main.swift
- Tests/FindDiskKillerAppTests/ProcessTableColumnLayoutTests.swift
- docs/releases/1.2.2.md
- Tests/FindDiskKillerAppTests/SectionNavigationPlaceholderTests.swift
- Sources/FindDiskKillerApp/AppNavigation.swift
- CONTRIBUTING.md
- SUPPORT.md
- Sources/FindDiskKillerApp/LoginItemSettingsModel.swift
- Sources/FindDiskKillerCore/ProcessHoverInteraction.swift
- docs/releases/1.2.0.md
- Sources/FindDiskKillerApp/Views/ProcessesView.swift
- Sources/CFindDiskKiller/include/CFindDiskKiller.h
- Sources/FindDiskKillerApp/TraceActivityRegistry.swift
- Package.swift
- Sources/FindDiskKillerApp/BrandLinks.swift
- Sources/FindDiskKillerApp/Views/UpdaterSettingsSection.swift
- Sources/CFindDiskKillerTrace/CFindDiskKillerTrace.c
- SECURITY.md
- scripts/prepare-claude-cleanup-runtime.sh
- Tests/FindDiskKillerAppTests/UpdateAndNavigationTests.swift
- Tests/FindDiskKillerAppTests/HistoryReportExporterTests.swift
- AGENTS.md
- scripts/verify-installed-trace-helper.sh
- Sources/FindDiskKillerTraceProtocol/TraceHelperProtocol.swift
- scripts/render-dmg-background.swift
- Sources/FindDiskKillerApp/Components/ProcessIcon.swift
- Sources/FindDiskKillerApp/Components/SharedComponents.swift
- Sources/FindDiskKillerApp/Views/HistoryChartViewport.swift
- PRIVACY.md
- Sources/FindDiskKillerApp/Views/MenuBarPanel.swift
- scripts/create-dmg.sh
- Sources/FindDiskKillerApp/Components/ProcessHoverCard.swift
- docs/website-release-checklist.md
- project.yml
- Tests/FindDiskKillerTraceHelperTests/TraceHelperServiceTests.swift
- Sources/FindDiskKillerApp/UpdateCoordinator.swift
- Sources/FindDiskKillerApp/HistoryModel.swift
- Tests/FindDiskKillerAppTests/HistoryChartViewportTests.swift
- Sources/FindDiskKillerCore/HistoryIdentity.swift
- Sources/FindDiskKillerApp/Views/AboutPage.swift
- THIRD_PARTY_NOTICES.md
- Sources/FindDiskKillerCore/OpenFileSampler.swift
- Sources/FindDiskKillerApp/AppRuntime.swift
code_chars_analyzed: 176162
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
      <span class="scope-stat__value">约 176,162 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">Sources/CFindDiskKillerTrace/include/CFindDiskKillerTrace.h</code></li><li><code class="path-chip">Sources/FindDiskKillerApp/Resources/THIRD_PARTY_ASSETS.md</code></li><li><code class="path-chip">docs/releases/1.2.1.md</code></li><li><code class="path-chip">Sources/FindDiskKillerClaudeCleanupHelper/main.swift</code></li><li><code class="path-chip">Tests/FindDiskKillerAppTests/ProcessTableColumnLayoutTests.swift</code></li><li><code class="path-chip">docs/releases/1.2.2.md</code></li><li><code class="path-chip">Tests/FindDiskKillerAppTests/SectionNavigationPlaceholderTests.swift</code></li><li><code class="path-chip">Sources/FindDiskKillerApp/AppNavigation.swift</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">SUPPORT.md</code></li><li><code class="path-chip">Sources/FindDiskKillerApp/LoginItemSettingsModel.swift</code></li><li><code class="path-chip">Sources/FindDiskKillerCore/ProcessHoverInteraction.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Mac 磁盘繁忙但无法从进程列表找到原因；AI 编码助手（Codex/Claude）静默积累数 GB 的对话数据难以清理。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 Swift/SwiftUI 与 C 混合架构，通过 CFindDiskKiller 模块封装 IOKit/DiskArbitration 系统调用（Sources/CFindDiskKiller/include/CFindDiskKiller.h），为 FindDiskKillerCore 提供底层 I/O、网络和文件描述符数据。主应用通过 XPC 与可选的提权 Trace Helper 通信，协议严格校验版本与代码签名（Sources/FindDiskKillerTraceProtocol/TraceHelperProtocol.swift:3-50）。历史存储模块使用 SQLite 并基于安装级 HMAC 密钥对标识符加盐（Sources/FindDiskKillerCore/HistoryIdentity.swift:169 支持密钥轮换）。AI 存储清理功能通过独立 Helper 调用官方 Claude SDK（scripts/prepare-claude-cleanup-runtime.sh 在构建时下载验证的 Node 和 SDK，产出通用二进制）。</p>
<p class="audit-callout audit-callout--highlight">文件追踪组件安全设计到位。TraceHelperServiceTests 验证了会话所有权、并发停止和强制退出逻辑（Tests/FindDiskKillerTraceHelperTests/TraceHelperServiceTests.swift: ownerControlsSession），Helper 仅接受固定命令形状和时长，不会执行任意指令，且 XPC 检查双方代码签名身份。</p>
<p class="audit-callout audit-callout--highlight">AI 存储清理流程严格控制。扫描仅由用户显式触发，读取只读，删除通过官方 SDK 接口，绝不回退到直接操作 SQLite 或文件（<code class="code-ref">docs/releases/1.2.0.md</code> 详述安全保证）。构建脚本校验外部依赖的哈希并 codesign 运行时，防范供应链篡改。</p>
<p class="audit-callout audit-callout--doubt">底层数据采集依赖未文档化的 IOKit 接口（如 CFindDiskKiller 中 dm_collect_process_io 实现未审阅到），macOS 大版本更新可能导致数据源失效，且缺乏兼容性回退。</p>
<p class="audit-callout audit-callout--doubt">历史身份哈希依赖文件密钥持久化（Sources/FindDiskKillerCore/HistoryIdentity.swift 中的 HistoryFileKeyStore），密钥丢失或旋转会使历史数据不可关联，用户可能不解为何“历史清零”。</p>
<p>适合聚焦 AI 辅助开发的 macOS 用户及系统管理员，短期内可替代 Activity Monitor 查看磁盘 I/O，长期关注 AI 存储分析的价值。建议部署前测试在较新 macOS beta 上的采集稳定性，并留意密钥变更对长期历史报表的影响。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖未文档化的 macOS IOKit 接口，系统更新可能导致数据采集失效。</li><li>内置 Node.js 和 Claude SDK 增加攻击面，版本锁定后长期兼容性存疑。</li><li>历史数据身份密钥弱持久化，密钥丢失或旋转可能导致历史数据不可访问。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>开源免费工具，瞄准 AI 编码助手用户的存储管理刚需，若持续维护可形成高粘性开发者社区，具备捐赠或企业赞助潜力。</p>
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
  <div class="score-item__value">92</div>
  <div class="score-bar"><span style="width:92%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">81.8</span>
  </div>
</div>
</section>