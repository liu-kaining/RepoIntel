---
title: '[Score: 77.1] stephenlthorn/auto-identity-remove'
date: '2026-06-11T03:40:53Z'
categories:
- Privacy Automation Tool
tags:
- playwright
- data-broker
- privacy
- automation
- CCPA
- GDPR
intel_score: 77.1
repo_name: stephenlthorn/auto-identity-remove
repo_link: https://github.com/stephenlthorn/auto-identity-remove
summary: 基于 Playwright 的数据经纪人自动退订工具，通过每月定时抓取 30+ 人群搜索站点并提交 opt-out 表单，适合关注隐私暴露、希望批量清理个人信息的美国用户。
code_source: git
code_files_reviewed:
- docker-compose.yml
- dashboard/package.json
- package.json
- Dockerfile
- .github/workflows/test.yml
- lib/dashboard-creds.js
- lib/platform.js
- lib/timing.js
- lib/drift.js
- lib/retry.js
- lib/lock.js
- lib/snapshot.js
- lib/stealth.js
- lib/defunct.js
- lib/success.js
- lib/diff.js
- lib/allowlist-edit.js
- lib/confirm.js
- lib/audit.js
- lib/filter.js
- lib/right-to-know-runner.js
- lib/right-to-know.js
- lib/freeze.js
- lib/cli-map.js
- lib/secrets.js
- lib/serp-watch.js
- lib/relay.js
- lib/logger.js
- lib/forms.js
- lib/notify.js
- lib/verify-loop.js
- lib/locale-patterns.js
- lib/email.js
- lib/imap-confirm.js
- lib/noise.js
- lib/broker-runner.js
- lib/report.js
- lib/feeds.js
- lib/hibp.js
- lib/doctor.js
- lib/exposure.js
- lib/complaint.js
- lib/scheduler.js
- lib/serp-scan.js
- lib/config.js
- lib/captcha.js
- data/dead-urls.json
- run.sh
code_chars_analyzed: 264968
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
      <span class="scope-stat__value">约 264,968 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">docker-compose.yml</code></li><li><code class="path-chip">dashboard/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">.github/workflows/test.yml</code></li><li><code class="path-chip">lib/dashboard-creds.js</code></li><li><code class="path-chip">lib/platform.js</code></li><li><code class="path-chip">lib/timing.js</code></li><li><code class="path-chip">lib/drift.js</code></li><li><code class="path-chip">lib/retry.js</code></li><li><code class="path-chip">lib/lock.js</code></li><li><code class="path-chip">lib/snapshot.js</code></li><li><code class="path-chip">lib/stealth.js</code></li><li><code class="path-chip">lib/defunct.js</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>美国用户在 Spokeo、BeenVerified 等数十家数据经纪人网站上都有公开的姓名、地址、电话等个人信息，手动逐站填写 opt-out 表单不仅耗时数小时，而且这些站点每 90 天左右会重新收录，导致用户需要反复手动操作。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目是一个 Node.js CLI 工具，核心入口为 <code class="code-ref">watcher.js</code>（未在 bundle 中审阅到）通过 <code class="code-ref">lib/cli-map.js</code> 的 <code class="code-ref">resolveCommand</code> 将 <code class="code-ref">aidr &lt;subcommand&gt;</code> 映射到 <code class="code-ref">watcher.js</code> 的对应 flag。<code class="code-ref">lib/broker-runner.js</code> 中的 <code class="code-ref">processBrokerWithPerson</code> 是单个经纪人处理的核心循环：先搜索 listing（<code class="code-ref">lib/forms.js:findListingUrl</code>）→ 导航到 opt-out 页 → 填表（<code class="code-ref">fillForm</code> 支持国际地址别名）→ 解 CAPTCHA（<code class="code-ref">lib/captcha.js</code> 支持 reCAPTCHA/hCAPTCHA/Turnstile/AWS WAF，通过 CapSolver API）→ 提交 → 分析提交后页面文本判断成功/失败/需邮件确认（<code class="code-ref">lib/success.js:classifyPostSubmit</code> + <code class="code-ref">lib/confirm.js:detectConfirmationRequired</code>）。</p>
<p class="audit-callout audit-callout--highlight">多语言提交后页面分类是项目的差异化设计点。<code class="code-ref">lib/locale-patterns.js</code> 为 ES/FR/DE/PT/IT 五种语言手工编写了保守的成功/失败/确认正则，配合 <code class="code-ref">lib/success.js:looksLikeSuccess</code> 和 <code class="code-ref">lib/confirm.js:looksLikeConfirmationRequired</code> 中的英文模式一起匹配，避免将非英文站点的提交误判为成功而启动 90 天冷却期。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">lib/verify-loop.js:runVerify</code> 实现了 T+7 日提交后验证回环——只对提交≥7天且未验证过的经纪人进行再搜索，验证结果直接写回 <code class="code-ref">state.optOuts[key]</code> 的 <code class="code-ref">verifiedDeletedAt</code>/<code class="code-ref">verifiedStillListedAt</code> 字段，配合 <code class="code-ref">lib/exposure.js:computeExposureScore</code> 将 still-listed 条目、SERP 排名和 HIBP 泄露数合成单一 0-100 分数，构成了从「提交→验证→评分→趋势追踪」的完整闭环。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">lib/broker-runner.js</code> 中的 CAPTCHA 解决循环（如 <code class="code-ref">solveRecaptcha</code> 内的 30 次 × 3 秒轮询）缺少总超时上限，当 CapSolver API 持续返回 <code class="code-ref">processing</code> 状态时，单个经纪人可能阻塞 90 秒以上，而调用方 <code class="code-ref">processBrokerWithPerson</code> 没有外层超时保护。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">lib/secrets.js</code> 的 <code class="code-ref">deriveKey</code> 使用 <code class="code-ref">scryptSync</code>（同步阻塞），当 <code class="code-ref">AIDR_PASSPHRASE</code> 设置后每次 <code class="code-ref">loadConfig</code> 都会在主线程阻塞数毫秒（N=16384），这在单次运行中影响不大，但如果 dashboard 或频繁 reload 场景下可能成为瓶颈。此外 <code class="code-ref">config.json.enc</code> 的加密信封使用 hex 编码（无压缩），一个典型 2KB 配置文件加密后约 12KB，这本身不是 bug 但值得注意。</p>
<p>首次使用建议先运行 <code class="code-ref">aidr preview</code> 验证表单填充正确性再 <code class="code-ref">aidr run</code>；务必配置 <code class="code-ref">AIDR_PASSPHRASE</code> 加密 <code class="code-ref">config.json</code>（包含真实姓名、地址、电话）；broker 列表依赖手动维护的 <code class="code-ref">brokers.js</code>（未审阅到），建议定期运行 <code class="code-ref">aidr update-brokers</code> 从 CA/VT 官方注册表拉取新站点。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 声称覆盖 500+ 站点但 package.json 描述为 30+，实际覆盖数取决于 brokers.js 维护质量和 CapSolver 的 CAPTCHA 成功率，站点 UI 变更后选择器可能漂移。</li><li>CapSolver 为付费第三方 API（~$0.001/solve），无 API key 时 CAPTCHA 保护站点退订将降级为手动列表，且 CapSolver 本身是灰色产业工具，其合法性和长期可用性存在不确定性。</li><li>项目无 LICENSE 文件（license 字段为 null），对商用和分发存在法律不确定性。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>项目面向注重隐私的个人用户，结合 CCPA/GDPR 合规模板、HIBP 泄露检查和监管投诉生成功能，可作为隐私合规 SaaS 的开源 MVP 或嵌入到身份保护产品中。</p>
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
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.1</span>
  </div>
</div>
</section>