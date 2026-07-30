---
title: '[Score: 79.0] FrigadeHQ/yap'
date: '2026-07-30T11:04:40Z'
categories:
- Productivity Tool
tags:
- macos
- swift
- speech-to-text
- on-device
- dictation
- menubar-app
intel_score: 79.0
repo_name: FrigadeHQ/yap
repo_link: https://github.com/FrigadeHQ/yap
summary: Yap 是一款免费、开源的 macOS 语音听写工具，利用系统内置模型实现纯本地、流式语音转文字，并通过全局快捷键将文字粘贴到任意输入框。
code_source: git
code_files_reviewed:
- Sources/Support/RuntimeMode.swift
- Sources/Services/StreamingTranscriber.swift
- Sources/Services/HotkeyManager.swift
- Sources/HUD/HUDModel.swift
- Sources/Models/Transcript.swift
- Sources/HUD/HUDControlling.swift
- Sources/Services/LaunchAtLoginService.swift
- Tests/PasteboardSnapshotTests.swift
- Sources/Support/Sound.swift
- Tests/AudioLevelTests.swift
- Sources/Services/HistoryStore.swift
- Sources/Support/WindowManager.swift
- Sources/Services/AudioLevel.swift
- Sources/Services/EscapeMonitor.swift
- Sources/Services/AudioBufferRelay.swift
- Sources/Services/SecureInput.swift
- project.yml
- Sources/Views/MainWindowView.swift
- Sources/Support/MenuBarIcon.swift
- Sources/HUD/HUDPanel.swift
- Sources/Services/BufferConverter.swift
- Tests/SpeechLocaleTests.swift
- Tests/HistoryStoreTests.swift
- Tests/FunctionKeyTriggerTests.swift
- Sources/Services/SpeechLocale.swift
- install.sh
- Sources/Services/AppRelauncher.swift
- Sources/YapApp.swift
- Sources/Views/AboutView.swift
- Sources/HUD/HUDController.swift
- Sources/Support/Theme.swift
- Sources/Services/AudioDevices.swift
- release.sh
- Sources/Services/AudioCaptureService.swift
- Sources/Services/DictationSession.swift
- Sources/Coordinator/RecordingCoordinator.swift
- Sources/Services/TranscriptionService.swift
- Sources/Services/ModifierHotkeyMonitor.swift
- Sources/Views/HistoryView.swift
- Sources/Views/OnboardingView.swift
- Sources/HUD/RecordingHUDView.swift
- Tools/GenerateIcon.swift
- Sources/Services/FunctionKeyMonitor.swift
- Tests/RecordingCoordinatorTests.swift
- Sources/Services/PermissionsManager.swift
- Sources/AppState.swift
- Sources/Services/TextInjector.swift
- README.md
code_chars_analyzed: 143177
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
      <span class="scope-stat__value">约 143,177 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Sources/Support/RuntimeMode.swift</code></li><li><code class="path-chip">Sources/Services/StreamingTranscriber.swift</code></li><li><code class="path-chip">Sources/Services/HotkeyManager.swift</code></li><li><code class="path-chip">Sources/HUD/HUDModel.swift</code></li><li><code class="path-chip">Sources/Models/Transcript.swift</code></li><li><code class="path-chip">Sources/HUD/HUDControlling.swift</code></li><li><code class="path-chip">Sources/Services/LaunchAtLoginService.swift</code></li><li><code class="path-chip">Tests/PasteboardSnapshotTests.swift</code></li><li><code class="path-chip">Sources/Support/Sound.swift</code></li><li><code class="path-chip">Tests/AudioLevelTests.swift</code></li><li><code class="path-chip">Sources/Services/HistoryStore.swift</code></li><li><code class="path-chip">Sources/Support/WindowManager.swift</code></li><li><code class="path-chip">Sources/Services/AudioLevel.swift</code></li><li><code class="path-chip">Sources/Services/EscapeMonitor.swift</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者、作者等高频打字用户需要快速、保密的听写功能，但现有方案要么笨重（需下载大模型），要么泄露隐私（上传音频）。Yap 消除了网络依赖和模型加载开销。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口在 Sources/YapApp.swift，AppState 持有模型容器和 RecordingCoordinator。录制流程由 HotkeyManager/ModifierHotkeyMonitor/FunctionKeyMonitor 触发 toggle()，进入状态机（Sources/Coordinator/RecordingCoordinator.swift）。DictationSession 管理 AudioCaptureService（音频采集）、AudioBufferRelay（缓冲）、TranscriptionService（转写）。转写结果经 TextInjector 通过系统事件或合成按键粘贴，并恢复剪贴板。HUD 显示波形和部分文字。</p>
<p class="audit-callout audit-callout--highlight">AudioBufferRelay (Sources/Services/AudioBufferRelay.swift:25-30) 在转录器初始化前暂存音频缓冲区，就绪后批量刷入，避免首字丢失，展现了细致的延迟优化。</p>
<p class="audit-callout audit-callout--highlight">TextInjector (Sources/Services/TextInjector.swift:42-47) 针对 Chromium 类应用的异步剪贴板读取，延迟恢复剪贴板内容，解决了非原生应用中粘贴失效的常见痛点。</p>
<p class="audit-callout audit-callout--doubt">FunctionKeyMonitor 的事件 Tap (Sources/Services/FunctionKeyMonitor.swift:80-95) 直接吞噬按键，若配置错误可能干扰其他快捷键，尽管代码有触发类型校验和回退机制。</p>
<p class="audit-callout audit-callout--doubt">粘贴策略完全依赖 Accessibility 权限，若未授予，文本仅留在剪贴板而用户可能未察觉，Onboarding 中虽有引导，但失败时的反馈较弱（仅日志）。</p>
<p>架构模块化且可测试，协议注入和状态机清晰。考虑增加粘贴失败时的用户提示或备用方式，并完善文档说明权限失效时的行为。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>严格依赖 macOS 26 和 Apple Silicon，用户群体受限，需等待系统普及。</li><li>语音模型准确性完全由苹果控制，OS 更新可能改变转写行为，不受开发者控制。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>Yap 利用苹果内置语音模型，打造轻量、隐私的听写工具，适合注重效率和控制权的 macOS 用户。开源 MIT 许可，可作为同类型应用的参考实现。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.0</span>
  </div>
</div>
</section>