---
title: '[Score: 77.7] gostonx/uninstally'
date: '2026-07-12T19:01:05Z'
categories:
- macOS Utility
tags:
- Swift
- SwiftUI
- macOS
- Finder Extension
- Sparkle
- Homebrew
intel_score: 77.7
repo_name: gostonx/uninstally
repo_link: https://github.com/gostonx/uninstally
summary: 一款原生 macOS 卸载工具，通过智能 bundle identifier 扫描彻底清除应用残留文件，集成 Finder 右键、Homebrew
  支持和历史记录。
code_source: git
code_files_reviewed:
- .github/workflows/release.yml
- Uninstally/Assets.xcassets/Contents.json
- Casks/uninstally.rb
- Uninstally/Utilities/Logger+Uninstally.swift
- Uninstally/Models/InstallationSource.swift
- Uninstally/Models/LeftoverItem.swift
- Uninstally/Utilities/SecurityPreferences.swift
- Uninstally/Assets.xcassets/AccentColor.colorset/Contents.json
- AGENTS.md
- Uninstally/Views/Components/GlassCard.swift
- Uninstally/Models/SafetyFactor.swift
- Uninstally/Services/FinderActionHandler.swift
- Uninstally/Services/SelectionReceiver.swift
- Uninstally/Models/UninstallProgress.swift
- Uninstally/Models/SimulationFile.swift
- Uninstally/Models/SimulationCategory.swift
- Uninstally/Assets.xcassets/AppIcon.appiconset/Contents.json
- Uninstally/Services/UninstallSimulationManager.swift
- scripts/create_dmg.sh
- Uninstally/Services/Security/DeletionPlan.swift
- Uninstally/ViewModels/HomebrewModel.swift
- Uninstally/Models/DeletionMode.swift
- Uninstally/Models/RemovableItem.swift
- Uninstally/ViewModels/StorageInsightsManager.swift
- scripts/bump_version.sh
- scripts/make_dmg_background.py
- Uninstally/UninstallyApp.swift
- Uninstally/Views/Components/VisualEffectView.swift
- Uninstally/Utilities/Format.swift
- Uninstally/Views/Components/StatTile.swift
- Uninstally/Models/SettingsSection.swift
- Uninstally/Views/UpdatePromptView.swift
- scripts/sync_website_version.py
- Uninstally/Models/HistoryRetention.swift
- Uninstally/Models/UninstallRecord.swift
- Uninstally/ViewModels/BatchUninstallModel.swift
- Uninstally/Utilities/IdentifierMatcher.swift
- Uninstally/Services/IconLoader.swift
- Uninstally/AppDelegate.swift
- Uninstally/Services/FileExplanationEngine.swift
- scripts/make_xcstrings.py
- Uninstally/Views/History/UninstallRecordDetailView.swift
- UninstallyFinder/FinderSync.swift
- docs/SECRETS.md
- Uninstally/Views/Uninstall/UninstallProgressView.swift
- Uninstally/Services/Security/SecuritySummary.swift
- Uninstally/Views/RootView.swift
- Uninstally/Services/HistoryStore.swift
code_chars_analyzed: 96695
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
      <span class="scope-stat__value">约 96,695 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">Uninstally/Assets.xcassets/Contents.json</code></li><li><code class="path-chip">Casks/uninstally.rb</code></li><li><code class="path-chip">Uninstally/Utilities/Logger+Uninstally.swift</code></li><li><code class="path-chip">Uninstally/Models/InstallationSource.swift</code></li><li><code class="path-chip">Uninstally/Models/LeftoverItem.swift</code></li><li><code class="path-chip">Uninstally/Utilities/SecurityPreferences.swift</code></li><li><code class="path-chip">Uninstally/Assets.xcassets/AccentColor.colorset/Contents.json</code></li><li><code class="path-chip">AGENTS.md</code></li><li><code class="path-chip">Uninstally/Views/Components/GlassCard.swift</code></li><li><code class="path-chip">Uninstally/Models/SafetyFactor.swift</code></li><li><code class="path-chip">Uninstally/Services/FinderActionHandler.swift</code></li><li><code class="path-chip">Uninstally/Services/SelectionReceiver.swift</code></li><li><code class="path-chip">Uninstally/Models/UninstallProgress.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>拖拽应用至废纸篓会留下偏好设置、缓存、容器等残留文件，长期积累浪费存储空间，且用户难以手动定位所有关联路径。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">应用采用 Coordinator 路由模式（RootView.swift）统一管理卸载、批处理、Finder 选择等流程，主界面通过 UninstallyApp.swift 注入环境对象和 SwiftData 存储。核心卸载链路由 UninstallSimulationManager 驱动，先调用 AssociatedFileScanner 扫描，再经 DeletionValidator 生成 DeletionPlan 并呈现仿真结果；执行时通过 DeletionExecutor 逐项处理（BatchUninstallModel.swift 展示顺序批处理）。</p>
<p class="audit-callout audit-callout--highlight">IdentifierMatcher.swift 的匹配引擎不仅使用主 bundle identifier，还通过 exactIdentifiers 收集辅助标识符（如 helper、扩展），并利用前缀匹配（prefixes for）捕获嵌套命名空间，比简单文件名搜索更精准全面。</p>
<p class="audit-callout audit-callout--highlight">CI 流水线（<code class="code-ref">.github/workflows/release.yml</code>）采用免费 Ad-hoc 签名 + Sparkle EdDSA 签名交付更新，无需 Apple Developer ID 公证，降低依赖且保证更新完整性，同时说明文档详尽。</p>
<p class="audit-callout audit-callout--doubt">代码包未提供 AssociatedFileScanner、DeletionValidator 等核心实现源码，其错误处理、权限回退、符号链接防御等健壮性无法验证；例如扫描过程遇到无权限目录时行为不明。</p>
<p class="audit-callout audit-callout--doubt">代码包中无任何测试文件，CI 虽运行 xcodebuild test 但使用 continue-on-error: true 忽略失败，表明缺乏自动化质量保障，回归风险高。</p>
<p>可先小范围试用其基本卸载和 Finder 集成，对隐私敏感场景有价值；生产环境密切关注其扫描与删除的可靠性，并补充自动化测试。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心删除逻辑未公开，可能因匹配过宽误删共享文件</li><li>无自动化测试，更新引入的回归故障无法被及时捕获</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>开源免费，直击 macOS 用户清理痛点，在隐私工具品类中有吸引小白用户的潜力，可通过捐赠或增值功能模式探索商业价值。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.7</span>
  </div>
</div>
</section>