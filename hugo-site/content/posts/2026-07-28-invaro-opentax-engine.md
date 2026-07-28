---
title: '[Score: 82.0] Invaro/opentax-engine'
date: '2026-07-28T16:38:39Z'
categories:
- Tax Computation & Verification
tags:
- tax-engine
- verifiable-computation
- mcp
- typescript
- ai-agents
- proofs
intel_score: 82.0
repo_name: Invaro/opentax-engine
repo_link: https://github.com/Invaro/opentax-engine
summary: 一个输出可验证证明的美国税务计算引擎，每条结果均附法律引用和机器验证路径，直接服务 AI 代理与税务合规场景。
code_source: git
code_files_reviewed:
- packages/playground/package.json
- site/package.json
- package.json
- packages/core/package.json
- packages/corpus-us-federal/package.json
- packages/compose/package.json
- .github/workflows/pr-title.yml
- .github/workflows/ci.yml
- packages/mcp/src/index.ts
- packages/solve/src/index.ts
- packages/core/src/index.ts
- packages/compose/src/index.ts
- packages/corpus-us-federal/src/index.ts
- packages/cli/src/index.ts
- packages/cli/tsconfig.json
- packages/compose/tsconfig.json
- packages/core/tsconfig.json
- packages/mcp/tsconfig.json
- packages/solve/tsconfig.json
- packages/corpus-us-federal/tsconfig.json
- packages/mcp/server.json
- packages/mcp/COMMERCIAL-LICENSE.md
- packages/cli/README.md
- packages/mcp/README.md
- packages/corpus-us-federal/corpus.lock.json
- packages/corpus-us-federal/test/fixtures/258_flat_states_2025.json
- packages/corpus-us-federal/test/fixtures/08_missing_filing_status.json
- packages/corpus-us-federal/test/fixtures/254_tx_no_income_tax.json
- packages/corpus-us-federal/test/fixtures/09_asof_2024_out_of_window.json
- packages/corpus-us-federal/test/fixtures/211_va_standard_deduction_ty2027_enacted.json
- packages/corpus-us-federal/test/fixtures/257_wa_wages_only_zero.json
- packages/corpus-us-federal/test/fixtures/250_ut_rate_cut_2025.json
- packages/corpus-us-federal/test/fixtures/251_ms_two_bracket_2025.json
- packages/cli/src/bin.ts
- packages/mcp/src/state-return.ts
- packages/mcp/src/hosted-bundle.ts
- packages/compose/src/money.ts
- packages/compose/src/types.ts
- packages/mcp/src/main.ts
- packages/solve/src/marginal.ts
- packages/solve/src/compare.ts
- packages/core/src/rule.ts
- packages/core/src/hash.ts
- packages/mcp/src/phone-home.ts
- packages/solve/src/sweep.ts
- packages/core/src/canonical.ts
- packages/core/src/proof.ts
- packages/solve/src/invert.ts
code_chars_analyzed: 94215
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
      <span class="scope-stat__value">约 94,215 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">packages/playground/package.json</code></li><li><code class="path-chip">site/package.json</code></li><li><code class="path-chip">package.json</code></li><li><code class="path-chip">packages/core/package.json</code></li><li><code class="path-chip">packages/corpus-us-federal/package.json</code></li><li><code class="path-chip">packages/compose/package.json</code></li><li><code class="path-chip">.github/workflows/pr-title.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">packages/mcp/src/index.ts</code></li><li><code class="path-chip">packages/solve/src/index.ts</code></li><li><code class="path-chip">packages/core/src/index.ts</code></li><li><code class="path-chip">packages/compose/src/index.ts</code></li><li><code class="path-chip">packages/corpus-us-federal/src/index.ts</code></li><li><code class="path-chip">packages/cli/src/index.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>在 AI 代理生成税务建议或计算时，模型常因训练数据过时而产出错误数字，且无可靠验证手段；现有税务软件多为黑箱，无法审计。开发者与合规部门需一个精确、可追踪、可独立核验的税务计算源。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">工程采用 monorepo 结构，核心 package &quot;@invaro/opentax-core&quot; 定义领域无关的规则引擎，规则以纯数据接口 Rule 定义（<code class="code-ref">packages/core/src/rule.ts</code>），包含引用、有效期、公式表达式；引擎使用 bigint 分进行精确运算（<code class="code-ref">packages/core/src/money.js</code>）。税收语料封装于 @invaro/opentax-corpus-us-federal，由数百条规则组成，通过内容寻址的 Merkle 根（<code class="code-ref">packages/core/src/hash.ts</code> 中的 merkleRoot 函数）固定版本。计算时生成完整推导证明树（DerivationNode，<code class="code-ref">packages/core/src/proof.ts</code>），证明文件可独立验证（<code class="code-ref">packages/core/src/verify.ts</code> 导出 verifyProof）。CLI 与 MCP 服务器均基于此引擎，提供 eval、check、verify 等命令，且包含求解模块（<code class="code-ref">packages/solve/src/sweep.ts</code>）进行扫掠、边际、悬崖分析。CI 工作流包含构建、测试、生成物同步检查（<code class="code-ref">.github/workflows/ci.yml</code>）。</p>
<p class="audit-callout audit-callout--highlight">领域无关引擎 + 法律数据分离，使税法变更仅需更新规则数据，引擎逻辑可复用（<code class="code-ref">packages/core/src/rule.ts</code> 与 <code class="code-ref">packages/corpus-us-federal/src/index.ts</code> 的规则聚合）。</p>
<p class="audit-callout audit-callout--highlight">完整的可验证证明体系，计算答案与语料哈希绑定，任何一方篡改均可检测（<code class="code-ref">packages/core/src/proof.ts</code> 与 <code class="code-ref">packages/core/src/hash.ts</code>），且证明格式公开（<code class="code-ref">docs/PROOF-FORMAT.md</code>），支持第三方实现独立校验。</p>
<p class="audit-callout audit-callout--doubt">核心 evaluate 模块未在本次审查中提供（<code class="code-ref">packages/core/src/evaluate.ts</code> 未包含在 code_bundle 中），规则选择、版本匹配、错误传播的具体实现无法验证，可能存在未发现的设计缺陷。</p>
<p class="audit-callout audit-callout--doubt">测试仅见少量 JSON fixture（如 <code class="code-ref">packages/corpus-us-federal/test/fixtures/08_missing_filing_status.js</code>on），未见测试运行器与断言逻辑，无法评估覆盖率及边界条件。</p>
<p>立即补充 evaluate 模块文档与单元测试，重点覆盖多规则版本、嵌套依赖、错误枚举等路径；在 MCP 服务器中增加请求审计日志以符合企业环境要求；持续扩展州税法语料并建立社区贡献流程。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>规则仅覆盖 2025-2026 联邦及部分州，维护成本高，扩展进度影响实用性。</li><li>核心评估器闭源可能隐藏逻辑错误，依赖方无法自行审查法律解读合理性。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可嵌入 AI 税务助手、财税 SaaS 或内部合规工具，作为确定性后端避免模型幻觉；AGPL 强制开源但提供商业许可，已在 TaxCalcBench 达 96% 准确率，有望替代传统税务引擎。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">66</div>
  <div class="score-bar"><span style="width:66%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.0</span>
  </div>
</div>
</section>