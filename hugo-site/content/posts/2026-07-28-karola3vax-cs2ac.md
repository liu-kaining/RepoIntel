---
title: '[Score: 77.1] karola3vax/CS2AC'
date: '2026-07-28T13:59:03Z'
categories:
- Game Anti-Cheat
tags:
- CS2
- Anti-Cheat
- Metamod
- SourceMod
- C++
- Server Plugin
intel_score: 77.1
repo_name: karola3vax/CS2AC
repo_link: https://github.com/karola3vax/CS2AC
summary: 为 CS2 社区服提供服务器端反作弊插件，集成了 17 种检测模块，通过分析视角、移动和输入异常识别作弊行为。
code_source: git
code_files_reviewed:
- .github/workflows/build.yml
- src/localization.h
- src/settings.h
- src/webhook.h
- src/cs2ac.h
- src/common.h
- src/localization.cpp
- src/settings.cpp
- src/webhook.cpp
- src/cs2ac.cpp
- src/utils/hooks.h
- src/sdk/netmessages.h
- src/clientcvar/utils.hpp
- src/sdk/cgameresourceserviceserver.h
- src/sdk/ccollisionproperty.h
- src/utils/detours.h
- src/utils/plat.h
- src/sdk/usercmd.h
- src/sdk/utlsignalslot.h
- src/utils/ctimer.cpp
- src/movement/mv_manager.cpp
- src/utils/addresses.h
- src/sdk/tracefilter.h
- src/utils/virtual.h
- src/player/player.cpp
- src/utils/ctimer.h
- src/utils/detours.cpp
- src/utils/gameconfig.h
- src/movement_analysis/player_manager.cpp
- src/sdk/clientframe.h
- src/player/player.h
- src/utils/utils.h
- src/clientcvar/iclientcvarvalue.h
- src/sdk/navphysicsinterface.h
- src/sdk/cinbuttonstate.h
- src/player/player_manager.cpp
- src/utils/interfaces.h
- src/movement_analysis/player_context.h
- src/utils/cdetour.h
- src/clientcvar/client_cvar_value.h
- src/detection/namechanger_module.cpp
- src/sdk/services.h
- src/utils/utils.cpp
- src/sdk/recipientfilters.h
- src/utils/module.h
- src/movement_analysis/player_context.cpp
- src/detection/silent_aim_module.cpp
- src/sdk/datatypes.h
code_chars_analyzed: 159194
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
      <span class="scope-stat__value">约 159,194 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/build.yml</code></li><li><code class="path-chip">src/localization.h</code></li><li><code class="path-chip">src/settings.h</code></li><li><code class="path-chip">src/webhook.h</code></li><li><code class="path-chip">src/cs2ac.h</code></li><li><code class="path-chip">src/common.h</code></li><li><code class="path-chip">src/localization.cpp</code></li><li><code class="path-chip">src/settings.cpp</code></li><li><code class="path-chip">src/webhook.cpp</code></li><li><code class="path-chip">src/cs2ac.cpp</code></li><li><code class="path-chip">src/utils/hooks.h</code></li><li><code class="path-chip">src/sdk/netmessages.h</code></li><li><code class="path-chip">src/clientcvar/utils.hpp</code></li><li><code class="path-chip">src/sdk/cgameresourceserviceserver.h</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>CS2 社区服管理员缺乏免费且可定制的服务器端反作弊方案，现有工具要么过时、要么闭源，无法保护游戏公平性。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">插件以 Metamod:Source 形式加载，通过 CDetour 钩入引擎移动函数（如 src/utils/detours.cpp 中的 PhysicsSimulate、ProcessUsercmds 等），在玩家每帧数据中挂载检测逻辑。检测系统（src/detection/detection_system.h）注册了多个模块（如 NameChangerModule、SilentAimModule），每个模块独立积累证据，达到阈值后触发回调函数 HandleDetection（src/cs2ac.cpp），由该函数统一根据配置执行 ban/kick 命令，并通过 WebhookService（src/webhook.cpp）异步发送 Discord 报告。配置管理基于 ConVar，支持动态重载（src/settings.cpp）。</p>
<p class="audit-callout audit-callout--highlight">静默自瞄检测（src/detection/silent_aim_module.cpp）通过比较子弹命中方向与准星可见方向的角度偏差，结合武器类型动态阈值和滑动窗口评分，有效降低误判率。</p>
<p class="audit-callout audit-callout--highlight">Webhook 报告服务（src/webhook.cpp）实现了带重试的 HTTP 队列、头像缓存、限速处理，并在无效配置或连续失败后自动禁用，避免影响服务器稳定性。</p>
<p class="audit-callout audit-callout--doubt">未审阅到任何测试代码（如单元测试或集成测试），只有 CI 中的格式检查（<code class="code-ref">.github/workflows/build.yml</code>）。依赖大量启发式规则，缺乏自动化回归验证，长期维护风险较高。</p>
<p class="audit-callout audit-callout--doubt">检测逻辑多基于固定阈值和经验规则（如 src/detection/silent_aim_module.cpp 中的武器偏差阈值表），可能无法适应游戏更新或新型作弊手法，需要频繁手工调参。</p>
<p>管理员应仔细配置 cs2ac.cfg 并运行 cs2ac_check_config 验证，启用 Discord 报告以便监控。由于检测完全服务器端，无法直接防御透视，需搭配 CS2FOW（README 提及）。注意插件钩子较多，可能与其他插件冲突。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>高延迟或丢包场景下启发式检测可能产生误封。</li><li>AGPL 许可证要求修改后的代码公开，可能阻碍部分商业服务器采用。</li><li>插件处于极早期阶段，未来维护和兼容性无保证。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 CS2 社区服提供了与商业反作弊方案（如 SMAC、EasyAntiCheat）竞争的免费开源替代，AGPL 许可可能限制闭源商用，但有助于构建社区生态。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.1</span>
  </div>
</div>
</section>