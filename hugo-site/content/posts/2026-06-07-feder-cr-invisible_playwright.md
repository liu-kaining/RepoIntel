---
title: '[Score: 79.3] feder-cr/invisible_playwright'
date: '2026-06-07T03:37:10Z'
categories:
- Anti-Detect Browser Automation
tags:
- browser-fingerprinting
- playwright
- firefox
- stealth-automation
- anti-bot
- web-scraping
intel_score: 79.3
repo_name: feder-cr/invisible_playwright
repo_link: https://github.com/feder-cr/invisible_playwright
summary: 基于 C++ 层面修补的 Firefox 150 反检测浏览器包装器，用贝叶斯网络生成连贯指纹，适用于需要绕过 reCAPTCHA/FP Pro
  的自动化场景。
code_source: git
code_files_reviewed:
- pyproject.toml
- .github/workflows/tests.yml
- .github/workflows/webrtc-e2e.yml
- .github/workflows/firefox-launch-matrix.yml
- src/invisible_playwright/_fpforge/__init__.py
- src/invisible_playwright/__init__.py
- src/invisible_playwright/__main__.py
- src/invisible_playwright/sync_api.py
- src/invisible_playwright/_proxy.py
- src/invisible_playwright/cli.py
- src/invisible_playwright/constants.py
- src/invisible_playwright/config.py
- src/invisible_playwright/_geo.py
- src/invisible_playwright/_headless.py
- src/invisible_playwright/async_api.py
- src/invisible_playwright/download.py
- src/invisible_playwright/_recaptcha_seed.py
- src/invisible_playwright/launcher.py
- src/invisible_playwright/prefs.py
- src/invisible_playwright/_fpforge/_network.py
- src/invisible_playwright/_fpforge/profile.py
- src/invisible_playwright/_fpforge/_sampler.py
- src/invisible_playwright/data/font-map.json
- src/invisible_playwright/_fpforge/data/priors_independent.json
- src/invisible_playwright/_fpforge/data/prior_audio.json
- src/invisible_playwright/_fpforge/data/cpt_msaa_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_hwc_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_intra_tier_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_storage_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_audio_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_codec_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_screen_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_msaa_given_class_screen.json
- src/invisible_playwright/_fpforge/data/cpt_storage_given_class_tier.json
- src/invisible_playwright/_fpforge/data/cpt_hwc_given_class_tier.json
- src/invisible_playwright/_fpforge/data/browsing_pool.json
- src/invisible_playwright/_fpforge/data/cpt_fonts_optional_given_class.json
- src/invisible_playwright/_fpforge/data/cpt_browsing_given_class.json
- src/invisible_playwright/_fpforge/data/font_pool.json
- src/invisible_playwright/_fpforge/data/cpt_screen_given_class_tier.json
- src/invisible_playwright/_fpforge/data/ff_win_distributions.json
- tests/conftest.py
- examples/basic.py
- examples/with_proxy.py
- .github/ISSUE_TEMPLATE/config.yml
- .github/PULL_REQUEST_TEMPLATE.md
- CODE_OF_CONDUCT.md
- tests/test_build.py
code_chars_analyzed: 286989
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
      <span class="scope-stat__value">约 286,989 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/tests.yml</code></li><li><code class="path-chip">.github/workflows/webrtc-e2e.yml</code></li><li><code class="path-chip">.github/workflows/firefox-launch-matrix.yml</code></li><li><code class="path-chip">src/invisible_playwright/_fpforge/__init__.py</code></li><li><code class="path-chip">src/invisible_playwright/__init__.py</code></li><li><code class="path-chip">src/invisible_playwright/__main__.py</code></li><li><code class="path-chip">src/invisible_playwright/sync_api.py</code></li><li><code class="path-chip">src/invisible_playwright/_proxy.py</code></li><li><code class="path-chip">src/invisible_playwright/cli.py</code></li><li><code class="path-chip">src/invisible_playwright/constants.py</code></li><li><code class="path-chip">src/invisible_playwright/config.py</code></li><li><code class="path-chip">src/invisible_playwright/_geo.py</code></li><li><code class="path-chip">src/invisible_playwright/_headless.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>使用 Playwright 做网页爬取/自动化的开发者面临反 bot 系统（reCAPTCHA、FP Pro、CreepJS）的层层检测：JS 层伪装会被 <code class="code-ref">.toString()</code> 检查和原型链变异检测器识破，Chromium 浏览器本身因市场份额过高而被反 bot 服务加权标记为可疑。维护一套不被检测的浏览器环境需要同时处理 400+ 个指纹字段的一致性，成本极高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目分为 Python 包装层（<code class="code-ref">src/invisible_playwright/</code>）和预编译的修补 Firefox 二进制（从 GitHub Releases 下载，SHA256 校验）。启动链路为 <code class="code-ref">InvisiblePlaywright.__enter__</code> → <code class="code-ref">generate_profile(seed)</code> 生成贝叶斯指纹 → <code class="code-ref">translate_profile_to_prefs()</code> 转换为 ~200 条 <code class="code-ref">zoom.stealth.*</code> Firefox pref → <code class="code-ref">_configure_proxy_shared()</code> 处理 SOCKS5 认证注入 → <code class="code-ref">firefox.launch()</code> 启动二进制。C++ 补丁不在本仓库内（在 <code class="code-ref">feder-cr/invisible_firefox</code>），本仓库的 Python 端只负责指纹采样和 prefs 翻译。</p>
<p class="audit-callout audit-callout--highlight">贝叶斯指纹生成器设计精巧。<code class="code-ref">_fpforge/_network.py:45</code> 的 <code class="code-ref">Node.sample</code> 实现了拓扑排序的条件概率表采样，<code class="code-ref">_fpforge/_sampler.py:143</code> 的 <code class="code-ref">_NETWORK</code> 构建了 gpu → gpu_class → intra_tier → {hw_concurrency, screen, storage, audio} 的多层条件依赖图，确保 GPU 等级与 CPU 核心数、屏幕分辨率、存储配额之间统计一致——避免了「4K 屏幕 + 集成显卡 + 2 核 CPU」这类明显不协调的指纹。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">_headless.py:59</code> 的 <code class="code-ref">_LinuxVirtualDisplay</code> 实现了带竞态重试的 Xvfb 管理（最多 10 次），并显式剥离 <code class="code-ref">_WAYLAND_LEAK_VARS</code> 防止 Firefox 跑到 Wayland compositor 上导致窗口泄漏；<code class="code-ref">_headless.py:108</code> 的 <code class="code-ref">_WindowsVirtualDesktop</code> 通过 ctypes 调用 <code class="code-ref">CreateDesktop</code> + <code class="code-ref">SetThreadDesktop</code> 将 Firefox 绑定到隐藏桌面，比简单设 <code class="code-ref">headless=True</code> 更能保持真实渲染管线。<code class="code-ref">prefs.py:381</code> 的注释详细解释了 <code class="code-ref">security.sandbox.gpu.level=0</code> 和 <code class="code-ref">security.sandbox.content.level=4</code> 在 CreateDesktop 环境下必要性的 Bugzilla 引用，说明维护者对 Firefox 沙箱机制有深入理解。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">_fpforge/_sampler.py</code> 的 CPT 数据（<code class="code-ref">cpt_hwc_given_class_tier.json</code> 等 10+ 个 JSON）来源标注为「Steam HW Survey + community data 2025-2026」，但缺乏可复现的数据采集管道。如果反 bot 服务也用类似分布做异常检测，这些手工调参的 CPT 可能滞后。<code class="code-ref">_fpforge/data/font_pool.json</code> 包含 ~170 个字体条目和预设的 width factor，这些数值的校准过程未见文档或脚本。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">download.py:90</code> 的 <code class="code-ref">ensure_binary</code> 从 GitHub Releases 下载 ~100MB 的 Firefox 二进制，SHA256 校验依赖 <code class="code-ref">checksums.txt</code>——但该文件本身也是从同一 Release 下载的，如果 Release 被篡改则校验形同虚设。此外 <code class="code-ref">_geo.py:60</code> 的 <code class="code-ref">discover_egress_ip</code> 使用 3 个公共 IP echo 端点，但没有缓存，每次 <code class="code-ref">timezone=&quot;auto&quot;</code> 启动都做网络请求，加上 GeoIP mmdb 也需要定期下载，首次冷启动延迟可达数秒。</p>
<p>适合已有 Playwright 爬取管道、需要通过 reCAPTCHA/FP Pro 检测的团队试用。建议：(1) 固定 <code class="code-ref">seed</code> 实现可复现指纹用于调试；(2) 生产环境务必使用 SOCKS5 代理 + <code class="code-ref">timezone=&quot;auto&quot;</code> 保持时区一致性；(3) 注意仅支持 Linux/Windows x86_64，macOS 和 ARM 不可用；(4) 建议先用 <code class="code-ref">CreepJS</code> 和 <code class="code-ref">FP Pro</code> 做冒烟测试再投入生产。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>C++ 补丁在另一个仓库 feder-cr/invisible_firefox，本仓库无法独立审计二进制安全性，供应链信任链未闭合</li><li>仅支持 Windows/Linux x86_64，macOS/ARM 用户无法使用；FF150 版本锁定意味着上游安全补丁需等维护者手动合并</li><li>Fork/Star 比 10.4% 为围观型项目特征；仓库仅 24 天历史、12 次 commit、维护者高度集中，长期维护风险显著</li><li>summary 过长，可能含废话</li><li>technical_review 未引用任何已审阅源码路径（path 级证据缺失）</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对高频网页数据采集、广告验证、价格监控等场景有直接实用价值，开源 MIT 许可使其可嵌入现有管道。但二进制修补的 Firefox 依赖单一维护者的 C++ fork（<code class="code-ref">invisible_firefox</code>），长期可持续性存疑。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">79</div>
  <div class="score-bar"><span style="width:79%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.3</span>
  </div>
</div>
</section>