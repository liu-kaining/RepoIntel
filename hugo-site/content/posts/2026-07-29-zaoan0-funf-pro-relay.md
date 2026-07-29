---
title: '[Score: 76.35] zaoan0/funf-pro-relay'
date: '2026-07-29T16:19:00Z'
categories:
- IoT Remote Control
tags:
- Bluetooth Low Energy
- WebSocket
- FastAPI
- Android
- Protocol Reverse Engineering
intel_score: 76.35
repo_name: zaoan0/funf-pro-relay
repo_link: https://github.com/zaoan0/funf-pro-relay
summary: 针对成人玩具啵啵贝 Pro 的开源远程中继方案，用安卓前台服务+WebSocket 解决官方后台掉线，为异地情侣提供可控的指令透传。
code_source: git
code_files_reviewed:
- server/requirements.txt
- android/FunfRelayApp/build.gradle
- android/FunfRelayApp/app/build.gradle
- .github/workflows/tests.yml
- server/protocol_config.json
- server/protocol.py
- server/test_multitenant.py
- harmony/HarmonyRelayApp/entry/src/main/resources/base/profile/main_pages.json
- harmony/HarmonyRelayApp/entry/hvigorfile.ts
- harmony/HarmonyRelayApp/hvigorfile.ts
- harmony/HarmonyRelayApp/entry/src/main/resources/base/element/string.json
- web/visual_test.py
- SECURITY.md
- USER_GUIDE.md
- SHARED_CONTROLLER_GUIDE.md
- TEST_REPORT.md
- WEB_USER_GUIDE.md
- DEVICE_HOLDER_GUIDE.md
- README.md
- ADMIN_GUIDE.md
- USAGE_MANUAL.md
- android/FunfRelayApp/app/src/main/java/com/funf/relay/MainActivity.kt
- android/FunfRelayApp/app/src/main/java/com/funf/relay/RelayService.kt
code_chars_analyzed: 100307
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
      <span class="scope-stat__value">23 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 100,307 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">server/requirements.txt</code></li><li><code class="path-chip">android/FunfRelayApp/build.gradle</code></li><li><code class="path-chip">android/FunfRelayApp/app/build.gradle</code></li><li><code class="path-chip">.github/workflows/tests.yml</code></li><li><code class="path-chip">server/protocol_config.json</code></li><li><code class="path-chip">server/protocol.py</code></li><li><code class="path-chip">server/test_multitenant.py</code></li><li><code class="path-chip">harmony/HarmonyRelayApp/entry/src/main/resources/base/profile/main_pages.json</code></li><li><code class="path-chip">harmony/HarmonyRelayApp/entry/hvigorfile.ts</code></li><li><code class="path-chip">harmony/HarmonyRelayApp/hvigorfile.ts</code></li><li><code class="path-chip">harmony/HarmonyRelayApp/entry/src/main/resources/base/element/string.json</code></li><li><code class="path-chip">web/visual_test.py</code></li><li><code class="path-chip">SECURITY.md</code></li><li><code class="path-chip">USER_GUIDE.md</code></li><li class="path-more">另有 9 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>官方 App 在安卓后台被系统杀死导致 BLE 连接断开，远程场景不可用；缺乏多用户、设备归属与安全隔离。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">中继服务器 FastAPI（未审阅到 relay_server.py 源码）承担 WebSocket 中继与鉴权，安卓设备端（RelayService.kt）建立 WS 长连接并管理 BLE 扫描/连接/GATT 写入，浏览器端 web/index.html 提供控制 UI。协议帧构建由 <code class="code-ref">server/protocol.py</code> 统一读取 <code class="code-ref">server/protocol_config.js</code>on，将语义指令转化为 12 字节固定格式帧。集成测试 <code class="code-ref">server/test_multitenant.py</code> 模拟多用户场景，验证账号隔离、设备权限与反馈隔离。</p>
<p class="audit-callout audit-callout--highlight">协议配置与代码分离，修改 JSON 即可适配新通道。<code class="code-ref">server/protocol_config.js</code>on 定义 functions 的 mode1/mode2 及帧模板，<code class="code-ref">server/protocol.py:102</code>-110 的 build_all_frames 严格按配置逐功能构建帧，无需改 Python 逻辑。</p>
<p class="audit-callout audit-callout--highlight">集成测试覆盖关键安全边界。<code class="code-ref">server/test_multitenant.py:68</code>-72 让 alice 请求 bob 设备状态显式返回 403，<code class="code-ref">server/test_multitenant.py:107</code>-117 验证反馈记录按用户隔离，且管理员可查看全部。</p>
<p class="audit-callout audit-callout--doubt">核心中继服务器 relay_server.py 未在 code_bundle 中提供。无法审查其 WebSocket 会话管理、控制锁（README 声称 60s 自动释放）实现及数据库操作，成为生产部署的主要风险。</p>
<p class="audit-callout audit-callout--doubt">BLE 通信无加密，RelayService.kt 的帧写入直接使用明文字节数组（见 frameBytes 方法），附近任何 BLE 设备可嗅探控制指令。虽在 README 已知限制中承认，但未提供修复方案。</p>
<p>补充 relay_server.py 的代码审查或压测，验证并发下控制锁和心跳机制；在设备端增加本地急停逻辑（如持续未收到心跳则自动归零），弥补网络中断后硬件保护缺失。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心服务器源码缺失，无法评估高并发下的稳定性与安全性。</li><li>BLE 明文传输可被附近设备监听，存在隐私泄露风险。</li><li>协议依赖逆向工程，硬件固件更新可能导致适配失效。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向成人用品远程控制细分场景，提供免费自托管方案，可降低用户对官方硬件的依赖，社区贡献能持续扩展协议兼容性。</p>
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
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.35</span>
  </div>
</div>
</section>