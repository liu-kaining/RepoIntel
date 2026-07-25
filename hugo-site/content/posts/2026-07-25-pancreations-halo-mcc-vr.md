---
title: '[Score: 77.1] pancreations/Halo-MCC-VR'
date: '2026-07-25T02:24:22Z'
categories:
- VR Modding
tags:
- C++
- OpenXR
- Halo MCC
- DLL Injection
- Reverse Engineering
intel_score: 77.1
repo_name: pancreations/Halo-MCC-VR
repo_link: https://github.com/pancreations/Halo-MCC-VR
summary: 为 Halo 3 与 ODST 提供原生 OpenXR VR 体验的 DLL 注入模组，支持立体渲染、体感操控和完整战役。
code_source: git
code_files_reviewed:
- CMakeLists.txt
- src/dll/d3d11_hook.h
- src/common/log.h
- src/dll/title_adapter.h
- src/dll/menu.h
- src/common/runtime_types.h
- src/common/title_registry.h
- src/common/log.cpp
- src/dll/ik.h
- src/dll/sigscan.h
- src/common/input_logic.h
- src/common/hud_layout_logic.h
- src/dll/dllmain.cpp
- src/common/input_logic.cpp
- src/dll/sigscan.cpp
- src/dll/d3d_state.h
- src/common/scope_logic.h
- src/dll/ik.cpp
- src/dll/title_adapter.cpp
- src/dll/game.h
- src/common/title_registry.cpp
- src/common/scope_logic.cpp
- src/dll/d3d11_hook.cpp
- src/dll/vr.h
- src/launcher/launcher.cpp
- src/common/odst_bringup_logic.h
- src/common/config.h
- src/dll/input.cpp
- src/dll/menu.cpp
- src/common/config.cpp
- docs/CONTINUATION.md
- docs/ODST-MINIMAL-BRINGUP-HANDOFF.md
- docs/HISTORY.md
- tools/verify_sig.py
- CMakePresets.json
- releases/0.2.1/manifest.json
- docs/EDITING-KIT-EVIDENCE.md
- docs/RELEASE-ANTIVIRUS-CHECKLIST.md
- releases/0.2.2/manifest.json
- releases/0.2.2/RELEASE-NOTES.md
- CLAUDE.md
- BUILDING.md
- tools/snapshot_xrefs.py
- AGENTS.md
- tools/find_string_xrefs.py
- tools/disasm.py
- README.md
- docs/ODST-WEAPON-IK-EVIDENCE.md
code_chars_analyzed: 245383
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
      <span class="scope-stat__value">约 245,383 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">CMakeLists.txt</code></li><li><code class="path-chip">src/dll/d3d11_hook.h</code></li><li><code class="path-chip">src/common/log.h</code></li><li><code class="path-chip">src/dll/title_adapter.h</code></li><li><code class="path-chip">src/dll/menu.h</code></li><li><code class="path-chip">src/common/runtime_types.h</code></li><li><code class="path-chip">src/common/title_registry.h</code></li><li><code class="path-chip">src/common/log.cpp</code></li><li><code class="path-chip">src/dll/ik.h</code></li><li><code class="path-chip">src/dll/sigscan.h</code></li><li><code class="path-chip">src/common/input_logic.h</code></li><li><code class="path-chip">src/common/hud_layout_logic.h</code></li><li><code class="path-chip">src/dll/dllmain.cpp</code></li><li><code class="path-chip">src/common/input_logic.cpp</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>PC 玩家想以沉浸式 VR 方式重温《光环》经典战役，但官方无 VR 支持；社区模组需通过逆向工程注入 DLL，实现立体渲染与体感控制，用户需面对不稳定性和禁用反作弊的限制。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">通过 launcher.cpp 以挂起方式创建游戏进程，远程线程注入 halo3xr.dll。DllMain 生成 InitThread（src/dll/dllmain.cpp），依次初始化日志、配置、MinHook 及 D3D11 钩子，然后调用 Game_Init 安装输入/相机钩子并启动 OpenXR。D3D11 钩子（src/dll/d3d11_hook.cpp）拦截 OMSetRenderTargets 实现每眼渲染重定向，Present 钩子在帧前后完成 VR 提交。输入钩子（src/dll/input.cpp）拦截 XInputGetState，融合 VR 控制器的运动输入与虚拟键位。标题特定的引擎钩子通过 AOB 特征码扫描（src/dll/sigscan.cpp）在 halo3.dll 等模块加载时定位并安装。</p>
<p class="audit-callout audit-callout--highlight">多标题状态隔离与安全降级。TitleAdapter_PollLoaded（src/dll/title_adapter.cpp:31-67）检测所有已注册的标题 DLL，若发现多模块驻留（如切换游戏后前一个标题 DLL 仍在）则记录日志并禁用游戏钩子，防止跨标题的野指针或状态污染，这是一种成熟的保护策略。</p>
<p class="audit-callout audit-callout--highlight">虚拟控制器持续连接机制。input.cpp 的 ProcessGetState 和 ProcessGetCaps（src/dll/input.cpp:95-130）确保即使共享输入门控关闭（如标题切换瞬间），虚拟手柄仍向游戏报告已连接且空闲，避免了虚假断开导致的“存档后菜单死区”问题，显著提升了跨标题会话的稳定性。</p>
<p class="audit-callout audit-callout--doubt">AI 生成代码未全面审查。README 声明代码由 Claude 和 Codex 编写，人类仅做逆向决策和头戴测试，“No human reviewed every line”是明确警告。这增加了隐蔽逻辑错误的风险，尤其是在复杂的引擎钩子中。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖不明。CMakeLists.txt 定义了测试目标 halomccvr_core_tests，但核心测试文件 tests/core_tests.cpp 未在提供的代码包中，因此无法评估测试用例的质量和覆盖率，工程可靠性存疑。</p>
<p>用户应仅使用官方发布版并校验哈希，勿从其它渠道下载。鉴于逆向钩子的敏感性，建议开发者引入模糊测试或更严格的回归测试，特别是在游戏更新后。考虑到 AI 代码的不可预测性，优先依赖头戴测试验收而非代码审查。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>作者声明随时可能退出，单一维护者依赖度高，项目容易陷入停滞。</li><li>游戏更新可能导致特征码失效，若无及时修复，模组将无法工作。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>针对特定游戏的利基模组，商业价值有限；但其展示的 AI 辅助逆向工程与 VR 注入技术可启发其他经典游戏的类似适配。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">58</div>
  <div class="score-bar"><span style="width:58%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.1</span>
  </div>
</div>
</section>