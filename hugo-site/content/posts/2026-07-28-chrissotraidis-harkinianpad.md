---
title: '[Score: 77.4] chrissotraidis/harkinianpad'
date: '2026-07-28T13:59:03Z'
categories:
- Game Porting / iOS Build System
tags:
- ios
- metal
- touch-controls
- build-system
- source-port
intel_score: 77.4
repo_name: chrissotraidis/harkinianpad
repo_link: https://github.com/chrissotraidis/harkinianpad
summary: 为 iPhone/iPad 打造的原生《时之笛》移植，基于 Ship of Harkinian 引擎，支持触控、Metal 渲染及 ROM 文件导入。
code_source: git
code_files_reviewed:
- .github/workflows/ios-build.yml
- assets/AppIcon.appiconset/Contents.json
- .github/ISSUE_TEMPLATE/config.yml
- .github/pull_request_template.md
- SECURITY.md
- ref/README.md
- scripts/generate-port-archive.sh
- CONTRIBUTING.md
- scripts/build-ios.sh
- .github/ISSUE_TEMPLATE/bug_report.yml
- scripts/apply-source-patches.sh
- scripts/configure-ios.sh
- docs/RELEASE_CHECKLIST.md
- docs/INSTALL_IPA.md
- scripts/clone-sources.sh
- scripts/package-ios.sh
- scripts/check-repo-safety.sh
- docs/touch-controls-design.md
- docs/BUILDING.md
- README.md
- docs/findings/04-filesystem-extraction.md
- docs/findings/05-priorart-licensing.md
- docs/findings/02-rendering-jit.md
- docs/findings/03-sdl-audio-lifecycle.md
- docs/findings/01-platform-build.md
- docs/ios-feasibility-and-implementation-plan.md
code_chars_analyzed: 265704
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
      <span class="scope-stat__value">26 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 265,704 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/ios-build.yml</code></li><li><code class="path-chip">assets/AppIcon.appiconset/Contents.json</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">.github/pull_request_template.md</code></li><li><code class="path-chip">SECURITY.md</code></li><li><code class="path-chip">ref/README.md</code></li><li><code class="path-chip">scripts/generate-port-archive.sh</code></li><li><code class="path-chip">CONTRIBUTING.md</code></li><li><code class="path-chip">scripts/build-ios.sh</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/bug_report.yml</code></li><li><code class="path-chip">scripts/apply-source-patches.sh</code></li><li><code class="path-chip">scripts/configure-ios.sh</code></li><li><code class="path-chip">docs/RELEASE_CHECKLIST.md</code></li><li><code class="path-chip">docs/INSTALL_IPA.md</code></li><li class="path-more">另有 12 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>iOS 玩家无法合法且便捷地运行《时之笛》汉化或增强版，模拟器体验差且存在法律灰色地带；该工程通过本地 ROM 提取和触控适配，为普通用户降低门槛。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">HarkinianPad 的核心是围绕上游 Ship of Harkinian 引擎的 iOS 构建与打包系统。<code class="code-ref">scripts/clone-sources.sh:3-25</code> 负责拉取固定版本的四个上游仓库（Shipwright、libultraship、ZAPDTR、OTRExporter），并禁用推送地址以锁定只读状态；随后 <code class="code-ref">scripts/apply-source-patches.sh:1-50</code> 应用一系列 iOS 适配补丁（Metal 渲染、触控控件、生命周期等，补丁文件未在审阅范围内）。<code class="code-ref">scripts/generate-port-archive.sh:1-30</code> 利用主机工具生成不含任何 ROM 数据的 <code class="code-ref">soh.o2r</code>，最终通过 <code class="code-ref">scripts/build-ios.sh:1-50</code> 编译出未签名的 arm64 iOS 应用。整套流程由 <code class="code-ref">.github/workflows/ios-build.yml:18-30</code> 中的 CI 守卫，先执行 <code class="code-ref">scripts/check-repo-safety.sh</code> 以确保仓库不含 ROM、游戏资产或签名材料，再完成完整构建并审计产物。</p>
<p class="audit-callout audit-callout--highlight">严格的安全与可重现构建检查：<code class="code-ref">scripts/check-repo-safety.sh:13-18</code> 通过 git 历史和当前文件扫描，禁止任何 <code class="code-ref">.z64/.n64/.o2r</code> 等游戏数据或凭证进入仓库；配合 <code class="code-ref">scripts/package-ios.sh:35-48</code> 的 IPA 审计（检查 soh.o2r 内容、签名状态），在工程层面有效隔离法律风险。</p>
<p class="audit-callout audit-callout--highlight">详尽的触控设计文档：<code class="code-ref">docs/touch-controls-design.md:40-120</code> 规划了针对 iPad 横屏握持的 16 键布局，包括低握式控制杆、分离式方向键与 C 键组、菜单按钮永久可见等交互细节，并将触控事件映射至 SDL 键位，为无手柄场景提供可接受的游戏体验，显示出对移动端交互的深入思考。</p>
<p class="audit-callout audit-callout--doubt">iOS 核心适配代码（渲染、输入、生命周期）均位于 <code class="code-ref">patches/</code> 目录下，但本次审阅未获得补丁内容（code_bundle 未包含 <code class="code-ref">patches/</code> 下的 <code class="code-ref">.patch</code> 文件）。构建系统产生的实际 iOS 产物质量无法从脚本层面直接判断。</p>
<p class="audit-callout audit-callout--doubt">仓库中不包含任何自动化测试（未见 <code class="code-ref">tests/</code> 目录、<code class="code-ref">_test</code> 文件或模拟器/真机测试钩子）。CI 仅检查构建通过和包安全，未验证游戏功能。真实设备上的触控、音频、中断等关键路径尚未有可重复的测试覆盖。</p>
<p>该项目为 iOS 游戏移植提供了一个优秀的构建和安全模板，但核心功能的风险在于上游补丁的维护和测试缺失。建议先 fork 或导出所有补丁并建立独立的补丁管理仓库，同时引入基础的 UI 自动化测试（如 Appium）以验证触控和渲染正确性。对于想移植类似解构游戏的开发者，可复用其 ROM 隔离和打包策略。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>上层专利风险：任天堂可能对含 ROM 提取功能的 App 发起 DMCA 或法律行动。</li><li>依赖上游未合并补丁，若 Ship of Harkinian 项目变动或放弃 iOS 支持，维护陷入困境。</li><li>仓库无顶层 LICENSE，代码贡献和使用权不明确，限制商业分发。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>目前面向《时之笛》iOS 爱好者，但可复用的构建和触控方案可作为其他解构游戏（如 Majora&#x27;s Mask）的模板，具有一定长期社区价值。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.4</span>
  </div>
</div>
</section>