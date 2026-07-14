---
title: '[Score: 75.7] myfanhua/turb-gpt-free-register'
date: '2026-07-14T10:42:45Z'
categories:
- 自动化工具
tags:
- ChatGPT
- Account Registration
- Browser Fingerprinting
- Codex OAuth
- Automation
intel_score: 75.7
repo_name: myfanhua/turb-gpt-free-register
repo_link: https://github.com/myfanhua/turb-gpt-free-register
summary: 多驱动 ChatGPT 账号自动注册与 Codex OAuth 授权工具，支持协议层、Roxy/Cloak/Browser Use 指纹浏览器，集成多邮箱源和接码平台，提供
  CLI 与 WebUI。
code_source: git
code_files_reviewed:
- requirements.txt
- core/__init__.py
- webui/__init__.py
- config/__init__.py
- main.py
- webui/app.py
- core/profile_utils.py
- core/humanize.py
- core/flow_trigger.py
- core/browser_use_client.py
- core/chatgpt_auth.py
- core/manual_otp.py
- core/otp_utils.py
- core/email_provider.py
- core/cloakbrowser_registration.py
- core/gptmail_client.py
- core/generic_api_mail_client.py
- core/sentinel_runner.py
- core/session.py
- core/qqmail_client.py
- core/sentinel.py
- core/openai_auth.py
- core/account_export.py
- core/registration_service.py
- core/sms_provider.py
- core/cloakbrowser_driver.py
- core/roxybrowser_client.py
- core/outlook_client.py
- core/codex_oauth.py
- config/twofa.py
- config/flow_trigger.py
- config/register.py
- tests/test_gptmail_config.py
- config/openai_protocol.py
- config/proxy.py
- config/humanize.py
- config/cloakbrowser.py
- tests/test_email_provider_gptmail.py
- web.py
- tests/test_config_defaults.py
- tests/test_webui_gptmail.py
- config/browser_use.py
- docs/superpowers/specs/2026-07-13-gptmail-email-provider-design.md
- config/email.py
- tools/test_codex_oauth.py
- L_API.md
- config/roxybrowser.py
- tests/test_gptmail_client.py
code_chars_analyzed: 374705
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
      <span class="scope-stat__value">约 374,705 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">requirements.txt</code></li><li><code class="path-chip">core/__init__.py</code></li><li><code class="path-chip">webui/__init__.py</code></li><li><code class="path-chip">config/__init__.py</code></li><li><code class="path-chip">main.py</code></li><li><code class="path-chip">webui/app.py</code></li><li><code class="path-chip">core/profile_utils.py</code></li><li><code class="path-chip">core/humanize.py</code></li><li><code class="path-chip">core/flow_trigger.py</code></li><li><code class="path-chip">core/browser_use_client.py</code></li><li><code class="path-chip">core/chatgpt_auth.py</code></li><li><code class="path-chip">core/manual_otp.py</code></li><li><code class="path-chip">core/otp_utils.py</code></li><li><code class="path-chip">core/email_provider.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>需要批量获取 ChatGPT 账号用于测试或 API 调用，但人工注册耗时长、IP/指纹易封，且 Codex 授权流程复杂，无法自动化。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用模块化设计，core/ 负责核心逻辑（注册、邮件、Codex），config/ 提供可热加载配置，webui/ 提供 Flask 管理界面。注册主流程在 main.py 中，根据配置选择驱动（protocol/roxy/cloak/browser_use）执行。以协议驱动为例，主要步骤：main.py:155 调用 run_registration，内部创建 BrowserSession（<code class="code-ref">core/session.py:42</code>），通过 curl_cffi 模拟 Chrome 指纹，使用 Sentinel/PoW 对抗检测（<code class="code-ref">core/openai_auth.py:29</code> 调用 sentinel-runner.js），并全程管理邮箱验证码（<code class="code-ref">core/email_provider.py:30</code> 多源调度）。</p>
<p class="audit-callout audit-callout--highlight">代理出口 IP 自动地理适配（<code class="code-ref">core/session.py:42</code>-89），BrowserSession 初始化时检测出口 IP 地理信息，自动匹配浏览器 locale、时区等指纹，有效提升反检测能力。</p>
<p class="audit-callout audit-callout--highlight">精细的错误分类与邮箱回收（<code class="code-ref">core/openai_auth.py:89</code>-106），定义 AccountUnusableError 并映射服务端错误码，注册失败时根据阶段自动将邮箱标记为 available 或 failed，避免无效重试浪费资源。</p>
<p class="audit-callout audit-callout--doubt">接码平台配置分散且依赖外部服务（<code class="code-ref">core/sms_provider.py</code> 与 L_API.md），本地 L 取号服务需额外部署，项目 README 未提供详细部署指导，用户可能陷入配置泥潭。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖不足，核心注册流程缺少集成测试，现有 tests/ 目录仅包含少量单元测试（<code class="code-ref">tests/test_gptmail_client.py</code> 等），代码变更时回归风险较高。</p>
<p>若用于生产批量注册，务必配置高质量住宅代理和可靠的接码平台，同时持续监控 OpenAI 前端/协议变化，因逆向工程依赖随时可能失效。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>强依赖 OpenAI 逆向工程，协议或前端更新可瞬间导致工具失效，维护成本高。</li><li>项目中接码平台、代理池需额外付费，且可能涉及灰产风险，使用时需谨慎。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>降低批量获取 ChatGPT 账号的人力与资金成本，对需要大量账号的工作室或自动化测试场景有直接价值，但可能触及平台服务条款和合规风险。</p>
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
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.7</span>
  </div>
</div>
</section>