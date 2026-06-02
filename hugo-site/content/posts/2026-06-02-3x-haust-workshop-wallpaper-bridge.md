---
title: '[Score: 76.75] 3x-haust/workshop-wallpaper-bridge'
date: '2026-06-02T03:41:11Z'
categories:
- macOS Desktop Wallpaper Utility
tags:
- Swift
- macOS
- Wallpaper Engine
- Scene Rendering
- AVFoundation
- Menu Bar App
intel_score: 76.75
repo_name: 3x-haust/workshop-wallpaper-bridge
repo_link: https://github.com/3x-haust/workshop-wallpaper-bridge
summary: 将 Windows Wallpaper Engine 本地 Workshop 文件夹搬上 macOS 桌面层的菜单栏工具，支持视频/图片/Web/scene.pkg
  四类壁纸播放与锁屏动画。
code_source: git
code_files_reviewed:
- .swiftlint.yml
- Sources/WorkshopWallpaperBridgeApp/WallpaperWindowLevel.swift
- Sources/WorkshopWallpaperBridgeApp/PausableWallpaperContent.swift
- Tests/WorkshopWallpaperBridgeAppTests/RestrictedWebWallpaperViewTests.swift
- Tests/WorkshopWallpaperBridgeAppTests/WallpaperWindowLevelTests.swift
- Sources/WorkshopWallpaperBridgeApp/LoginItemController.swift
- Sources/WorkshopWallpaperBridgeApp/StatusMenu.swift
- Sources/WorkshopWallpaperBridgeApp/SettingsWindowPlacement.swift
- Package.swift
- Sources/WorkshopWallpaperBridgeApp/WallpaperContentLayout.swift
- Tests/WorkshopWallpaperBridgeAppTests/WallpaperContentLayoutTests.swift
- Sources/WorkshopWallpaperBridgeApp/VideoWallpaperView.swift
- Sources/WorkshopWallpaperCore/VideoConverter.swift
- Sources/WorkshopWallpaperBridgeApp/BridgeApp.swift
- Sources/WorkshopWallpaperBridgeApp/SettingsWindowCoordinator.swift
- Tests/WorkshopWallpaperCoreTests/SceneTextureDecoderTests.swift
- Tests/WorkshopWallpaperBridgeAppTests/SettingsWindowPlacementTests.swift
- Tests/WorkshopWallpaperBridgeAppTests/DesktopVisibilityMonitorTests.swift
- Sources/WorkshopWallpaperBridgeApp/RestrictedWebWallpaperView.swift
- Sources/WorkshopWallpaperCore/Models.swift
- Sources/WorkshopWallpaperCore/SceneLZ4BlockDecoder.swift
- Sources/WorkshopWallpaperBridgeApp/DesktopVisibilityMonitor.swift
- Tests/WorkshopWallpaperCoreTests/Fixture.swift
- Tests/WorkshopWallpaperBridgeAppTests/WallpaperPlayerSuspensionTests.swift
- Sources/WorkshopWallpaperBridgeApp/StillWallpaperImageProvider.swift
- Sources/WorkshopWallpaperBridgeApp/SystemWallpaperSetter.swift
- Scripts/package-app.sh
- Sources/WorkshopWallpaperBridgeApp/LockScreenAnimationController.swift
- Tests/WorkshopWallpaperCoreTests/SceneRenderPlanTests.swift
- Tests/WorkshopWallpaperCoreTests/ScenePackageTests.swift
- Sources/WorkshopWallpaperLockScreenSaver/WorkshopWallpaperLockScreenSaverView.m
- Sources/wwbctl/main.swift
- Sources/WorkshopWallpaperBridgeApp/ContentView.swift
- Tests/WorkshopWallpaperBridgeAppTests/SystemWallpaperSetterTests.swift
- Sources/WorkshopWallpaperCore/SceneDXTDecoder.swift
- Sources/WorkshopWallpaperBridgeApp/WallpaperPlayer.swift
- Sources/WorkshopWallpaperCore/Scanner.swift
- README.md
- Tests/WorkshopWallpaperCoreTests/LibraryStoreTests.swift
- Sources/WorkshopWallpaperCore/ScenePackage.swift
- Tests/WorkshopWallpaperBridgeAppTests/AppViewModelTests.swift
- Sources/WorkshopWallpaperBridgeApp/SceneWallpaperView.swift
- Sources/WorkshopWallpaperCore/LibraryStore.swift
- README.ko.md
- Tests/WorkshopWallpaperCoreTests/ScannerTests.swift
- Sources/WorkshopWallpaperCore/SceneTexture.swift
- Sources/WorkshopWallpaperBridgeApp/AppViewModel.swift
- Sources/WorkshopWallpaperCore/SceneRenderPlan.swift
code_chars_analyzed: 271816
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
      <span class="scope-stat__value">约 271,816 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.swiftlint.yml</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/WallpaperWindowLevel.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/PausableWallpaperContent.swift</code></li><li><code class="path-chip">Tests/WorkshopWallpaperBridgeAppTests/RestrictedWebWallpaperViewTests.swift</code></li><li><code class="path-chip">Tests/WorkshopWallpaperBridgeAppTests/WallpaperWindowLevelTests.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/LoginItemController.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/StatusMenu.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/SettingsWindowPlacement.swift</code></li><li><code class="path-chip">Package.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/WallpaperContentLayout.swift</code></li><li><code class="path-chip">Tests/WorkshopWallpaperBridgeAppTests/WallpaperContentLayoutTests.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/VideoWallpaperView.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperCore/VideoConverter.swift</code></li><li><code class="path-chip">Sources/WorkshopWallpaperBridgeApp/BridgeApp.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>拥有 Wallpaper Engine 购买记录的 macOS 用户把 Workshop 文件夹复制到 Mac 后，没有官方客户端能解析 project.json、播放 video/web/scene 壁纸到桌面层，更无法通过屏幕保护系统实现锁屏动画；手动处理 scene.pkg 的二进制纹理和 LZ4 压缩门槛极高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分为三层——<code class="code-ref">WorkshopWallpaperCore</code>（纯逻辑库）、<code class="code-ref">WorkshopWallpaperBridgeApp</code>（macOS GUI）、<code class="code-ref">wwbctl</code>（CLI），均由 <code class="code-ref">Package.swift</code> 声明为独立 target。GUI 通过 <code class="code-ref">@main</code> SwiftUI <code class="code-ref">App</code> 入口 <code class="code-ref">BridgeApp.swift</code> 创建 <code class="code-ref">MenuBarExtra</code>，将 <code class="code-ref">AppViewModel</code> 作为唯一状态源驱动扫描、导入、播放全链路。壁纸播放由 <code class="code-ref">WallpaperPlayer</code> 单例管理，每块屏幕创建一个 <code class="code-ref">WallpaperWindow</code>（<code class="code-ref">WallpaperPlayer.swift:122</code>），窗口层级设为 <code class="code-ref">CGWindowLevelForKey(.desktopIconWindow) - 1</code>（<code class="code-ref">WallpaperWindowLevel.swift:4</code>），实现桌面图标下方渲染。scene.pkg 解析是最大工程量：<code class="code-ref">ScenePackageReader</code>（<code class="code-ref">ScenePackage.swift:58</code>）做二进制解包并校验路径穿越（<code class="code-ref">validateEntryPath</code> 拒绝 <code class="code-ref">../</code> 和绝对路径），<code class="code-ref">SceneTextureDecoder</code>（<code class="code-ref">SceneTexture.swift:122</code>）支持 LZ4 解压、DXT1/3/5、RG88、R8 等格式，<code class="code-ref">SceneDXTDecoder</code>（<code class="code-ref">SceneDXTDecoder.swift:1</code>）是手写软解实现，<code class="code-ref">SceneRenderPlanBuilder</code>（<code class="code-ref">SceneRenderPlan.swift:97</code>）负责从 scene.json 提取 object→model→material→texture 链路并生成带 keyframe 动画的渲染计划。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">SceneLZ4BlockDecoder</code>（<code class="code-ref">SceneSceneLZ4BlockDecoder.swift</code> 即 <code class="code-ref">SceneLZ4BlockDecoder.swift:7</code>）对 literal/match 路径均有边界校验，<code class="code-ref">maxOutputSize</code> 参数防止解压炸弹，并通过 <code class="code-ref">SceneTextureDecoder.maximumCompressedPayloadBytes</code> 设定 64 MB 上限；<code class="code-ref">SceneTexture.swift:31</code> 对维度超过 16384 的纹理直接拒绝。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">DesktopVisibilityMonitor</code>（<code class="code-ref">DesktopVisibilityMonitor.swift:7</code>）通过 <code class="code-ref">CGWindowListCopyWindowInfo</code> 抓取屏幕窗口快照，用面积 &gt;12000、layer==0、alpha&gt;0.05 判断是否有用户窗口覆盖桌面，自动暂停壁纸播放；对 Finder 桌面、Stage Manager shelf、自身窗口做了白名单过滤，实测代码中有四组边界 case 测试覆盖（<code class="code-ref">DesktopVisibilityMonitorTests.swift</code>）。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">VideoConverter</code>（<code class="code-ref">VideoConverter.swift:7</code>）硬编码 ffmpeg 路径 <code class="code-ref">/opt/homebrew/bin/ffmpeg</code>、<code class="code-ref">/usr/local/bin/ffmpeg</code>、<code class="code-ref">/usr/bin/ffmpeg</code>，不走 <code class="code-ref">$PATH</code> 查找；<code class="code-ref">convertToPlayableVideo</code> 调用 <code class="code-ref">process.waitUntilExit()</code> 同步阻塞当前线程，在 GUI 的 <code class="code-ref">AppViewModel.convertSelected</code>（<code class="code-ref">AppViewModel.swift:161</code>）中虽然包了 <code class="code-ref">Task.detached</code>，但 <code class="code-ref">WallpaperPlayer</code> 是 <code class="code-ref">@MainActor</code> 单例，如果用户在转换期间频繁操作可能产生竞态。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">RestrictedWebWallpaperView</code>（<code class="code-ref">RestrictedWebWallpaperView.swift:33</code>）依赖 <code class="code-ref">WKContentRuleListStore</code> 编译远程拦截规则；如果编译失败（<code class="code-ref">error != nil</code>），当前实现直接 <code class="code-ref">return</code> 不加载任何内容，也不会向用户报告错误，web 壁纸会静默变黑。测试 <code class="code-ref">RestrictedWebWallpaperViewTests.swift</code> 仅做了源码字符串匹配而非运行时行为测试。</p>
<p>scene.pkg 渲染已覆盖 DXT 和嵌入图片，但粒子、着色器、脚本等 Wallpaper Engine 高级功能明确不可用（README 和 <code class="code-ref">Scanner.swift:166</code> 的 <code class="code-ref">scene_renderer_limited</code> issue 均有说明），建议在设置界面给每个 scene 项目增加可视化警告标签，避免用户困惑；同时建议将 ffmpeg 路径查找改为接受用户可配置路径或走 <code class="code-ref">$PATH</code>。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>scene.pkg 仅支持 2D image layer，粒子/着色器/脚本均跳过，多数热门场景壁纸效果将大幅缩水</li><li>Lock Screen 壁纸写入 /Library/Caches/Desktop Pictures 路径依赖 macOS 版本特定行为，系统更新后可能失效</li><li>项目创建仅 1 天、7 次 commit、单维护者，长期维护和 macOS 新版本适配存在不确定性</li><li>构建脚本 Scripts/package-app.sh 硬编码 arm64 架构，Intel Mac 用户无法直接使用发布的 DMG</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向已购 Wallpaper Engine 的 macOS 用户，填补了 Wallpaper Engine 无 Mac 客户端的市场空白；本地-only、不触碰 Steam 认证的定位使其法律风险较低，具备作为付费工具或开源赞助项目的商业潜力。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.75</span>
  </div>
</div>
</section>