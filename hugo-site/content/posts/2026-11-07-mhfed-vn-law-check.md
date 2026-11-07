---
title: '[Score: 75.75] mhfed/vn-law-check'
date: '2026-11-07T21:25:25Z'
categories:
- AI Agent Compliance
tags:
- vietnam-law
- ai-agent
- compliance
- claude-code
- bash
- legal-tech
intel_score: 75.75
repo_name: mhfed/vn-law-check
repo_link: https://github.com/mhfed/vn-law-check
summary: 面向 Claude Code/Cursor 等编码代理的越南网站合规审计技能包，用静态扫描+分级清单发现数据保护、电商、AI 透明度等风险。
code_source: git
code_files_reviewed:
- tests/fixtures/shop/package.json
- demo/site/package.json
- tests/fixtures/rn-app/package.json
- .github/workflows/check.yml
- demo/site/vercel.json
- .github/ISSUE_TEMPLATE/config.yml
- .github/FUNDING.yml
- tests/fixtures/shop/pages/checkout.js
- tests/fixtures/flutter-shop/pubspec.yaml
- demo/site/checkout.js
- demo/site/README.md
- tests/fixtures/rn-app/app.json
- demo/site/api/subscribe.js
- plugins/vn-law-check/.claude-plugin/plugin.json
- tests/fixtures/spa-url/assets/index-a1b2c3.js
- demo/site/chat-widget.js
- tests/fixtures/ai-chat/chat.js
- .claude-plugin/marketplace.json
- tests/fixtures/rn-app/src/screens/SignUp.tsx
- .github/ISSUE_TEMPLATE/phan-loai-sai.yml
- demo/site/api/chat.js
- demo/assets-src/render.js
- SECURITY.md
- .github/ISSUE_TEMPLATE/de-xuat.yml
- CODE_OF_CONDUCT.md
- tests/run.sh
- .github/ISSUE_TEMPLATE/bao-sai.yml
- DISCLAIMER.md
- plugins/vn-law-check/skills/vn-law-check/DISCLAIMER.md
- tools/sync.sh
- CONTRIBUTING.md
- install.sh
- plugins/vn-law-check/skills/vn-law-check/references/06-electronic-transactions.md
- references/06-electronic-transactions.md
- plugins/vn-law-check/README.md
- plugins/vn-law-check/skills/vn-law-check/scripts/fetch-site.sh
- scripts/fetch-site.sh
- README.en.md
- plugins/vn-law-check/skills/vn-law-check/references/04-consumer-protection.md
- references/04-consumer-protection.md
- plugins/vn-law-check/skills/vn-law-check/references/03-cybersecurity.md
- references/03-cybersecurity.md
- examples/sample-audit-report.md
- plugins/vn-law-check/skills/vn-law-check/examples/sample-audit-report.md
- SKILL.md
- plugins/vn-law-check/skills/vn-law-check/SKILL.md
- plugins/vn-law-check/skills/vn-law-check/references/07-ai-transparency.md
- references/07-ai-transparency.md
code_chars_analyzed: 83148
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
      <span class="scope-stat__value">约 83,148 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">tests/fixtures/shop/package.json</code></li><li><code class="path-chip">demo/site/package.json</code></li><li><code class="path-chip">tests/fixtures/rn-app/package.json</code></li><li><code class="path-chip">.github/workflows/check.yml</code></li><li><code class="path-chip">demo/site/vercel.json</code></li><li><code class="path-chip">.github/ISSUE_TEMPLATE/config.yml</code></li><li><code class="path-chip">.github/FUNDING.yml</code></li><li><code class="path-chip">tests/fixtures/shop/pages/checkout.js</code></li><li><code class="path-chip">tests/fixtures/flutter-shop/pubspec.yaml</code></li><li><code class="path-chip">demo/site/checkout.js</code></li><li><code class="path-chip">demo/site/README.md</code></li><li><code class="path-chip">tests/fixtures/rn-app/app.json</code></li><li><code class="path-chip">demo/site/api/subscribe.js</code></li><li><code class="path-chip">plugins/vn-law-check/.claude-plugin/plugin.json</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>越南2025-2026多部数字法律集中生效，小团队开发网站/app时不知道哪些表单、追踪脚本和聊天机器人需要同意与披露，人工翻法条成本高且易漏，发布前常处于违规风险。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目以 SKILL.md 为 agent 指令入口，要求先跑 <code class="code-ref">scripts/scan.sh &lt;dir|URL&gt;</code> 得到 LEVEL 信号，再按 <code class="code-ref">references/00-triage.md</code> 分级打开对应 checklist；<code class="code-ref">scripts/fetch-site.sh</code> 负责 URL 模式抓取公开页面与 JS，<code class="code-ref">tools/sync.sh</code> 从根 AGENTS.md/DISCLAIMER 等生成 Claude/Cursor/Windsurf/Cline 多份 rule，CI 用 <code class="code-ref">tests/run.sh</code> 对 fixtures 验证 LEVEL 输出。</p>
<p class="audit-callout audit-callout--highlight">多工具同步机制。<code class="code-ref">tools/sync.sh</code> 单源生成并 diff 检查多 agent rule，<code class="code-ref">install.sh</code> 用 MARK 指针插入 <code class="code-ref">.vn-law-check/</code> 且不覆盖用户文件，降低安装维护成本。</p>
<p class="audit-callout audit-callout--highlight">诚实标注未验证法律条文。<code class="code-ref">references/04-consumer-protection.md</code> 多处标注“CHƯA XÁC MINH”，<code class="code-ref">SKILL.md</code> 强制不编造条款和罚款，降低误报的法律风险。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">scripts/scan.sh</code> 实现，无法判断 grep 信号、LEVEL 分级和 APP/AI 检测的准确性；<code class="code-ref">tests/run.sh</code> 只对 fixtures 的 <code class="code-ref">LEVEL=</code> 关键字做匹配，覆盖较浅。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">scripts/fetch-site.sh</code> 的 <code class="code-ref">resolve</code> 用 <code class="code-ref">[[ &quot;$href&quot; == &quot;$origin&quot;* ]]</code> 判断同域，没有 <code class="code-ref">/</code> 或端口边界，<code class="code-ref">https://example.com.evil.com</code> 可通过前缀匹配拉取站外内容；此外内联 JS 和动态脚本不在 <code class="code-ref">&lt;script src&gt;</code> 提取范围。</p>
<p>作为发布前初步自查和报告草稿生成工具使用；法律条款更新应走 PR 复核，核心扫描逻辑补充 fixture 覆盖并修复同域判断边界。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>大量“CHƯA XÁC MINH”条文，若误当终局结论可能造成罚款误判；须律师复核（DISCLAIMER.md）。</li><li>fetch-site.sh 同域前缀匹配可绕过域名边界，建议改为 <code class="code-ref">^${origin}(/|$)</code>。</li><li>未审阅核心 scan.sh，CI 仅验证 LEVEL 关键词，可能漏报动态渲染或内联脚本的风险。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>越南数字法律切换期，这款工具可作为法律科技获客入口或内嵌到建站/代理平台；但当前免费、无法律背书，直接变现需引入认证律师或SaaS报告服务。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">69</div>
  <div class="score-bar"><span style="width:69%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.75</span>
  </div>
</div>
</section>