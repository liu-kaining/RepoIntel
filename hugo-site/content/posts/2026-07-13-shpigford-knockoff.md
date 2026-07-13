---
title: '[Score: 75.35] Shpigford/knockoff'
date: '2026-07-13T21:53:40Z'
categories:
- Browser Extension
tags:
- amazon
- brand-filter
- heuristic
- privacy
- chrome-extension
intel_score: 75.35
repo_name: Shpigford/knockoff
repo_link: https://github.com/Shpigford/knockoff
summary: 本地运行的Chrome扩展，通过语言启发式算法和社区品牌列表，自动过滤Amazon搜索结果中的商标抢注伪品牌（如SZHLUX），保护隐私无需注册。
code_source: git
code_files_reviewed:
- .github/workflows/test.yml
- .github/workflows/cws-release.yml
- src/background.js
- src/pdp-brand.js
- src/detector.js
- safari/Knockoff/Knockoff/Assets.xcassets/Contents.json
- safari/Knockoff/Knockoff/Assets.xcassets/AccentColor.colorset/Contents.json
- safari/Knockoff/Knockoff/Assets.xcassets/LargeIcon.imageset/Contents.json
- .conductor/settings.toml
- onboarding/onboarding.js
- safari/Knockoff/Knockoff Extension/Resources/onboarding/onboarding.js
- safari/Knockoff/Knockoff iOS/KnockoffApp.swift
- safari/Knockoff/Knockoff/AppDelegate.swift
- scripts/render-icons.sh
- .github/PULL_REQUEST_TEMPLATE.md
- .github/FUNDING.yml
- safari/Knockoff/Knockoff Extension/Resources/src/background.js
- scripts/sync-safari.sh
- scripts/render-store-assets.sh
- safari/Knockoff/Knockoff/Resources/Script.js
- scripts/upload-secrets.sh
- safari/Knockoff/Knockoff Extension/SafariWebExtensionHandler.swift
- scripts/package.sh
- scripts/update-bundled-brands.sh
- safari/Knockoff/Knockoff/Assets.xcassets/AppIcon.appiconset/Contents.json
- data/flagged-brands.js
- safari/Knockoff/Knockoff Extension/Resources/data/flagged-brands.js
- data/chinese-major.js
- safari/Knockoff/Knockoff Extension/Resources/data/chinese-major.js
- safari/Knockoff/Knockoff/ViewController.swift
- safari/Knockoff/Knockoff iOS/ContentView.swift
- manifest.json
- safari/Knockoff/Knockoff Extension/Resources/manifest.json
- safari/Knockoff/IOS-TARGET-SETUP.md
- safari/Knockoff/Knockoff Extension/Resources/src/pdp-brand.js
- scripts/release-firefox.sh
- scripts/release-safari.sh
- CONTRIBUTING.md
- scripts/cws-status.sh
- scripts/render-listing.js
- data/generic-words.js
- safari/Knockoff/Knockoff Extension/Resources/data/generic-words.js
- data/config.js
- safari/Knockoff/Knockoff Extension/Resources/data/config.js
- store-assets/listing.json
- store-assets/release-notes.md
- CLAUDE.md
- README.md
code_chars_analyzed: 149988
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
      <span class="scope-stat__value">约 149,988 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/test.yml</code></li><li><code class="path-chip">.github/workflows/cws-release.yml</code></li><li><code class="path-chip">src/background.js</code></li><li><code class="path-chip">src/pdp-brand.js</code></li><li><code class="path-chip">src/detector.js</code></li><li><code class="path-chip">safari/Knockoff/Knockoff/Assets.xcassets/Contents.json</code></li><li><code class="path-chip">safari/Knockoff/Knockoff/Assets.xcassets/AccentColor.colorset/Contents.json</code></li><li><code class="path-chip">safari/Knockoff/Knockoff/Assets.xcassets/LargeIcon.imageset/Contents.json</code></li><li><code class="path-chip">.conductor/settings.toml</code></li><li><code class="path-chip">onboarding/onboarding.js</code></li><li><code class="path-chip">safari/Knockoff/Knockoff Extension/Resources/onboarding/onboarding.js</code></li><li><code class="path-chip">safari/Knockoff/Knockoff iOS/KnockoffApp.swift</code></li><li><code class="path-chip">safari/Knockoff/Knockoff/AppDelegate.swift</code></li><li><code class="path-chip">scripts/render-icons.sh</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Amazon购物时，搜索结果充斥大量无信誉的伪品牌（如SZHLUX、HORUSDY），消费者难以快速辨别，不仅浪费时间，还可能买到劣质商品。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">扩展使用MV3标准（manifest.json:2），权限仅storage（manifest.json:7），完全本地运行。<code class="code-ref">核心检测引擎src/detector.js</code>为纯逻辑模块，接收产品标题后按固定优先级进行裁决：用户白/黑名单 → 已知伪品牌列表（<code class="code-ref">data/flagged-brands.js</code>） → 中国品牌列表 → 已知品牌列表（<code class="code-ref">data/known-brands.js</code> + 每日刷新的社区列表） → 名称启发式评分（<code class="code-ref">src/detector.js</code>:scoreBrand）。评分≥6直接标记flagged，≥3为suspect，否则unknown。无品牌则为unbranded。<code class="code-ref">src/detector.js</code>:classify整合了品牌提取（extractBrand）与裁决（verdictFor），并处理本地语言、圣经等边缘情况。远程配置机制通过api.knockoff.co推送DOM选择器更新（<code class="code-ref">data/config.js</code>），避免因Amazon改版导致的扩展失效。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/detector.js</code>:scoreBrand的启发式算法针对伪品牌名称特征（全大写5-9字符、元音比例低于0.18、辅音连缀等）进行加权评分，设计精细，且已知品牌列表始终具有否决权，防止误伤合法品牌（如ASICS）。</p>
<p class="audit-callout audit-callout--highlight">数据文件（<code class="code-ref">data/flagged-brands.js</code>、<code class="code-ref">data/known-brands.js</code>等）与代码分离，社区贡献门槛低，配合CI（<code class="code-ref">.github/workflows/test.yml</code>）进行品牌列表完整性检查，便于维护。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">未审阅到src/content.js</code>（DOM操作、用户交互、报告上报等关键集成逻辑），无法评估整体工程的错误处理、异步流程和测试覆盖，本次结论不覆盖该部分。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/detector.js</code>的启发式依赖英语语言学特征，尽管有本地语言和宗教标题过滤，非拉丁语系市场（如日文、阿拉伯文）仍可能漏判，扩展文档也承认此为已知限制。</p>
<p><code class="code-ref">如能补充src/content.js</code>的审阅，可更全面评估网络请求（如卖家国家查询）的安全性和稳定性；建议扩展启发式模型支持多语言或增加针对本地市场的手动规则。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>启发式算法偏向英语，德国、日本等市场可能出现误判，需依赖人工维护的品牌列表弥补。</li><li>扩展强依赖Amazon的DOM结构，若Amazon大幅改版且远程配置推送不及时，过滤功能可能暂时失效。</li><li><code class="code-ref">未审阅src/content.js</code>，无法确认用户数据上报（如卖家ID）是否完全匿名，存在隐式隐私风险。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可吸引大量Amazon购物者，通过提供高级功能（如卖家数据分析）、联盟营销或捐赠实现商业化，但目前免费且无商业化计划。</p>
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
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.35</span>
  </div>
</div>
</section>