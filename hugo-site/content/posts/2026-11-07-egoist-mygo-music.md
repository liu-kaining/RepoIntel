---
title: '[Score: 75.8] egoist/mygo-music'
date: '2026-11-07T00:35:54Z'
categories:
- Desktop Music Player
tags:
- go
- music-player
- plugin-system
- asr
- native
intel_score: 75.8
repo_name: egoist/mygo-music
repo_link: https://github.com/egoist/mygo-music
summary: Go 原生无需 WebView 的桌面音乐播放器，用插件扩展本地与流媒体，并可设备端生成播客字幕。
code_source: git
code_files_reviewed:
- package.json
- website/package.json
- go.mod
- .github/workflows/release.yml
- main.go
- website/src/routes/index.tsx
- website/src/routes/zh/index.tsx
- icon/tray/main.go
- icon/main.go
- examples/demo-plugin/index.js
- scripts/sherpa/main.go
- internal/plugin/console_other.go
- internal/app/notch_other.go
- internal/speech/lib_windows.go
- internal/speech/lib_unix.go
- internal/plugin/console_windows.go
- internal/mp4/mp4_test.go
- internal/app/ui_kit_test.go
- internal/app/websignin_test.go
- internal/app/fade_test.go
- internal/player/mp4.go
- internal/player/fixture.go
- internal/app/updates.go
- internal/app/debug_shots.go
- internal/app/history_test.go
- internal/player/starved.go
- internal/app/scrub_test.go
- internal/app/space_test.go
- internal/app/cache.go
- internal/music/fetch.go
- internal/player/starved_test.go
- internal/app/covered_test.go
- internal/speech/resample_test.go
- internal/app/skeleton_test.go
- internal/app/session.go
- internal/app/backdrop_test.go
- internal/app/ui_songmenu.go
- internal/speech/resample.go
- internal/app/sidebar_test.go
- internal/speech/lines_test.go
- internal/app/edges_test.go
- internal/player/fade.go
- internal/app/download.go
- internal/app/updates_test.go
- internal/speech/lines.go
- internal/player/ahead.go
- internal/player/download.go
- internal/app/saveplaylist_test.go
code_chars_analyzed: 101582
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
      <span class="scope-stat__value">约 101,582 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">website/package.json</code></li><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">main.go</code></li><li><code class="path-chip">website/src/routes/index.tsx</code></li><li><code class="path-chip">website/src/routes/zh/index.tsx</code></li><li><code class="path-chip">icon/tray/main.go</code></li><li><code class="path-chip">icon/main.go</code></li><li><code class="path-chip">examples/demo-plugin/index.js</code></li><li><code class="path-chip">scripts/sherpa/main.go</code></li><li><code class="path-chip">internal/plugin/console_other.go</code></li><li><code class="path-chip">internal/app/notch_other.go</code></li><li><code class="path-chip">internal/speech/lib_windows.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>想在一个桌面应用里同时播放本地无损、流媒体和播客并自动记字幕的用户，不得不装多个 Electron 应用或忍受内存占用，现可基于同一插件接口按需加载，减少重复开发。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">main.go 仅 10 行调用 internal/app 的 Run，应用逻辑集中在 internal/app 与 internal/player；播放器通过 <code class="code-ref">internal/player/ahead.go</code> 的 getAhead 在下一曲播放前异步取流，配合 <code class="code-ref">internal/player/starved.go</code> 的 watched 对 Read/SetPosition 计时来判断缓冲。插件层由 <code class="code-ref">examples/demo-plugin/index.js</code> 定义完整导出（search/stream/lyrics 等），宿主通过 <code class="code-ref">internal/plugin/console_windows.go</code> 与 console_other.go 跨平台隐藏子进程窗口。语音字幕链路 <code class="code-ref">scripts/sherpa/main.go</code> 下载 sherpa-onnx 并校验 SHA-256，再由 <code class="code-ref">internal/speech/resample.go</code> 将音频重采样到 16k 单声道，<code class="code-ref">internal/speech/lines.go</code> 将识别段落切分为歌词行。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">internal/player/ahead.go</code> 的 getAhead 使用 done channel 与 close 防止已请求的下一曲泄漏，遇网络流则通过 Cache.download 缓存；<code class="code-ref">internal/player/starved.go</code> 用 atomic.Int64 记录调用开始时间并在超过 250ms 时通知 loading，提升了弱网下的状态准确性。</p>
<p class="audit-callout audit-callout--highlight">测试体系扎实，<code class="code-ref">internal/app/fade_test.go</code>、scrub_test.go、space_test.go 覆盖 UI 交互，<code class="code-ref">internal/speech/resample_test.go</code> 验证多采样率抗混叠，<code class="code-ref">internal/mp4/mp4_test.go</code> 验证可播放性，这些不是空壳测试。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 internal/player 的完整解码与缓存实现，仅见 mp4.go 片段、download.go 与 ahead.go；无法确认 MP3/FLAC/Ogg 等核心解码路径的错误处理与内存管理，需谨慎。</p>
<p class="audit-callout audit-callout--doubt">插件运行环境未提供源码（仅 demo-plugin），未看到 JS 引擎沙箱/权限校验实现，README 宣传的插件安全边界无法在本次 code_bundle 中核验，可能成为安全风险。</p>
<p>优先补充插件宿主与本地库扫描模块的代码审阅；在 CI 增加 -race 与模糊测试；对插件权限做进程级隔离验证。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅审阅 48/244 文件，核心 UI 与解码未覆盖</li><li>AGPL-3.0 许可证可能限制商用闭源</li><li>插件沙箱无源码证据，权限声明易被绕过</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向厌倦 Electron 的音乐/播客重度用户，用 Go 原生 + 插件聚合本地与流媒体；若插件生态成熟，可在特定亚文化圈形成分发场景，但商业回报有限。</p>
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
  <div class="score-item__value">79</div>
  <div class="score-bar"><span style="width:79%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">77</div>
  <div class="score-bar"><span style="width:77%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">71</div>
  <div class="score-bar"><span style="width:71%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.8</span>
  </div>
</div>
</section>