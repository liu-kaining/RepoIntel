---
title: '[Score: 76.7] wquguru/cicada'
date: '2026-11-07T21:25:25Z'
categories:
- AI Meeting Assistant
tags:
- Swift
- Kotlin
- Python
- .NET
- speech-recognition
- live-captions
intel_score: 76.7
repo_name: wquguru/cicada
repo_link: https://github.com/wquguru/cicada
summary: 跨四端会议实时字幕、同声传译与纪要工具，面向多语言会议场景，主打本地识别与免机器人参会。
code_source: git
code_files_reviewed:
- android/build.gradle.kts
- android/cli/build.gradle.kts
- android/core/build.gradle.kts
- android/tools/player/build.gradle.kts
- android/app/build.gradle.kts
- .github/workflows/build.yml
- .github/workflows/windows.yml
- .github/workflows/android.yml
- .github/workflows/linux.yml
- linux/cicada/core/__init__.py
- linux/cicada/app/__init__.py
- linux/cicada/__init__.py
- windows/tests/Cicada.Tests/Fixtures/fbank.json
- linux/tests/voiceprint-ref.json
- linux/tests/mac-fixes-session.json
- linux/tests/test_problem.py
- linux/tests/test_recording.py
- linux/tests/test_meeting_end.py
- linux/tests/test_proxy.py
- linux/tests/test_updates.py
- CLAUDE.md
- android/CLAUDE.md
- ios/CLAUDE.md
- linux/CLAUDE.md
- windows/CLAUDE.md
- linux/cicada/app/__main__.py
- android/scripts/test.sh
- .github/release-notes-linux.md
- .github/release-notes-windows.md
- .github/release-notes-mac.md
- android/scripts/shot.sh
- .github/release-notes-android.md
- android/settings.gradle.kts
- tools/toggle-key.swift
- windows/scripts/install-dotnet.sh
- Package.swift
- scripts/test.sh
- tools/winall.swift
- tools/audio-probe/show.py
- linux/scripts/test.sh
- ios/scripts/ctl.sh
- tools/lsctl.swift
- android/scripts/consent.sh
- windows/scripts/test.sh
- windows/vm/deploy.sh
- ios/Sources/Cicada/ListenActivity.swift
- windows/scripts/dotnet.sh
- tools/transcribe.swift
code_chars_analyzed: 69947
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
      <span class="scope-stat__value">约 69,947 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">android/build.gradle.kts</code></li><li><code class="path-chip">android/cli/build.gradle.kts</code></li><li><code class="path-chip">android/core/build.gradle.kts</code></li><li><code class="path-chip">android/tools/player/build.gradle.kts</code></li><li><code class="path-chip">android/app/build.gradle.kts</code></li><li><code class="path-chip">.github/workflows/build.yml</code></li><li><code class="path-chip">.github/workflows/windows.yml</code></li><li><code class="path-chip">.github/workflows/android.yml</code></li><li><code class="path-chip">.github/workflows/linux.yml</code></li><li><code class="path-chip">linux/cicada/core/__init__.py</code></li><li><code class="path-chip">linux/cicada/app/__init__.py</code></li><li><code class="path-chip">linux/cicada/__init__.py</code></li><li><code class="path-chip">windows/tests/Cicada.Tests/Fixtures/fbank.json</code></li><li><code class="path-chip">linux/tests/voiceprint-ref.json</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>多语言会议依赖人工翻译或云端转写，成本高、有隐私风险且需拉机器人入会；纪要整理滞后，跨平台方案缺失。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">已审阅到构建与测试层：<code class="code-ref">.github/workflows/linux.yml</code> 在 22.04/24.04 两架构跑原生库构建、单测与 Xvfb 冒烟；<code class="code-ref">android/app/build.gradle.kts</code> 依赖 <code class="code-ref">:core</code> 且 JNI 由 <code class="code-ref">src/main/jni/Android.mk</code> 构建；<code class="code-ref">linux/cicada/core/__init__.py</code> 称 core 是无 GTK/第三方依赖的 Android 引擎移植。核心语音识别、翻译、纪要引擎源文件未在 code_bundle 中提供，无法审阅具体调用链。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">linux/tests/test_updates.py</code> 覆盖更新包校验、tar 路径穿越拒绝与断点续传重试；<code class="code-ref">linux/tests/test_proxy.py</code> 实测 HTTP/SOCKS5 代理、ignore-hosts 与 GNOME 设置回退，错误路径测试真实。</p>
<p class="audit-callout audit-callout--highlight">多平台 CI 不是摆设：<code class="code-ref">.github/workflows/windows.yml</code> 在真实 Windows runner 跑 dotnet 测试并发布 x64/arm64；<code class="code-ref">.github/workflows/android.yml</code> 在 JVM 跑 <code class="code-ref">cicada-cli test</code> 并构建 debug/release APK；<code class="code-ref">.github/workflows/linux.yml</code> 安装后验证库存在并跑 smoke.sh。</p>
<p class="audit-callout audit-callout--doubt">code_bundle 未包含 <code class="code-ref">linux/cicada/core/*.py</code>、<code class="code-ref">windows/src/Cicada</code>、<code class="code-ref">Sources/Cicada</code> 具体实现，无法验证实时转写、翻译、说话人分离和虚拟声卡 BlackHole 的真实错误处理与并发模型，工程分因此受限。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">android/app/build.gradle.kts</code> 引用 <code class="code-ref">src/main/jni/Android.mk</code>，但 JNI C 源码未提供；同传语音克隆、Apple 本机识别路径均未审阅到，README 隐私承诺缺乏源码级背书。</p>
<p>下一步应补充至少 Mac 或 Linux 端核心源码（音频采集、ASR/LLM 调度、会话存储）再做完整审计；当前可作为早期关注项目，但不宜给出生产级结论。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心源码未提供，仅测试与CI可审</li><li>Apple本机识别/同传源码未公开审阅</li><li>仅30 commits且近期创建，维护风险高</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向远程跨国会议的实用工具，可替代部分同传与纪要人工；免费开源策略可能吸引企业用户，但当前商业化路径不明。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.7</span>
  </div>
</div>
</section>