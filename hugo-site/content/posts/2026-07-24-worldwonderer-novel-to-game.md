---
title: '[Score: 76.25] worldwonderer/novel-to-game'
date: '2026-07-24T13:38:02Z'
categories:
- AI-Assisted Game Development
tags:
- agent-skills
- game-design
- novel-adaptation
- claude-code
- web-game
- pipeline
intel_score: 76.25
repo_name: worldwonderer/novel-to-game
repo_link: https://github.com/worldwonderer/novel-to-game
summary: NovelToGame 通过七步技能管线将小说转化为可玩网页游戏，锁定产品框架后依次完成拆解、概念、设计、构建与证据化验证，避免 AI 直接生成换皮作品。
code_source: git
code_files_reviewed:
- .github/workflows/validate.yml
- .github/workflows/deploy.yml
- skills/novel-to-game/agents/openai.yaml
- skills/game-qa/agents/openai.yaml
- skills/game-build/agents/openai.yaml
- skills/game-concept/agents/openai.yaml
- skills/game-world-design/agents/openai.yaml
- skills/novel-game-analyze/agents/openai.yaml
- skills/game-art-direction/agents/openai.yaml
- kimi.plugin.json
- .claude-plugin/marketplace.json
- .claude-plugin/plugin.json
- examples/journey-to-the-west/_progress.md
- skills/game-build/references/build-brief-contract.md
- examples/journey-to-the-west/source/SOURCE.md
- .codex-plugin/plugin.json
- examples/jin-ping-mei/_progress.md
- examples/journey-to-the-west/PRODUCT_BRIEF.md
- AGENTS.md
- examples/jin-ping-mei/PRODUCT_BRIEF.md
- skills/game-art-direction/SKILL.md
- skills/game-qa/SKILL.md
- skills/game-art-direction/references/art-direction-method.md
- skills/game-world-design/SKILL.md
- skills/game-build/SKILL.md
- skills/game-world-design/references/world-design-method.md
- skills/game-build/references/production-techniques.md
- examples/jin-ping-mei/source/SOURCE.md
- skills/novel-to-game/SKILL.md
- skills/novel-to-game/references/pipeline-contract.md
- skills/game-concept/references/concept-method.md
- skills/novel-game-analyze/SKILL.md
- skills/game-qa/references/qa-contract.md
- skills/game-concept/SKILL.md
- skills/game-world-design/references/game-writing-craft.md
- skills/novel-to-game/references/intake-method.md
- tests/test_validate_repo.py
- README.md
- skills/novel-game-analyze/references/gameability-protocol.md
- README_EN.md
- examples/jin-ping-mei/source/expurgate.py
- examples/journey-to-the-west/analysis/SOURCE_BIBLE.md
- skills/novel-to-game/references/intake-engine-reference.md
- examples/jin-ping-mei/design/ART_DIRECTION.md
- skills/novel-to-game/references/intake-benchmark-reference.md
- examples/jin-ping-mei/concepts/CONCEPT.md
- examples/journey-to-the-west/concepts/CONCEPT.md
- scripts/validate_repo.py
code_chars_analyzed: 110856
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
      <span class="scope-stat__value">约 110,856 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/validate.yml</code></li><li><code class="path-chip">.github/workflows/deploy.yml</code></li><li><code class="path-chip">skills/novel-to-game/agents/openai.yaml</code></li><li><code class="path-chip">skills/game-qa/agents/openai.yaml</code></li><li><code class="path-chip">skills/game-build/agents/openai.yaml</code></li><li><code class="path-chip">skills/game-concept/agents/openai.yaml</code></li><li><code class="path-chip">skills/game-world-design/agents/openai.yaml</code></li><li><code class="path-chip">skills/novel-game-analyze/agents/openai.yaml</code></li><li><code class="path-chip">skills/game-art-direction/agents/openai.yaml</code></li><li><code class="path-chip">kimi.plugin.json</code></li><li><code class="path-chip">.claude-plugin/marketplace.json</code></li><li><code class="path-chip">.claude-plugin/plugin.json</code></li><li><code class="path-chip">examples/journey-to-the-west/_progress.md</code></li><li><code class="path-chip">skills/game-build/references/build-brief-contract.md</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>创作者将小说直接抛给语言模型做游戏，得到的往往是通用玩法换皮。NovelToGame 解决的难题是将原著独特的世界规则、角色关系与情绪转化为可玩动词与核心循环，产出忠于原著的独特体验。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">总入口 <code class="code-ref">skills/novel-to-game/SKILL.md</code> 先执行需求 intake（<code class="code-ref">skills/novel-to-game/references/intake-method.md</code>），生成 PRODUCT_BRIEF 锁定九大产品维度；随后串行调用六个子技能：novel-game-analyze 拆解全书提取可玩事实并保证覆盖门禁（<code class="code-ref">skills/novel-game-analyze/SKILL.md</code>），game-concept 基于事实生成三个真正不同的方案并淘汰硬否决项（<code class="code-ref">skills/game-concept/SKILL.md</code>），game-world-design 把概念收束为包含核心循环、关卡节拍与系统预算的游戏设计文档（<code class="code-ref">skills/game-world-design/SKILL.md</code>），game-art-direction 定义视觉原则、镜头与签名画面（<code class="code-ref">skills/game-art-direction/SKILL.md</code>），game-build 将设计压缩为 BUILD_BRIEF 交由编码模型实现原型（<code class="code-ref">skills/game-build/SKILL.md</code>），最后 game-qa 以独立证据验证启动、渲染、输入、状态变化与重开（<code class="code-ref">skills/game-qa/SKILL.md</code>）。每一阶段的出入库契约由 pipeline-contract.md 强制，不允许下游静默改写上游事实。仓库结构由 <code class="code-ref">scripts/validate_repo.py</code> 与测试套件 <code class="code-ref">tests/test_validate_repo.py</code> 统一验证，确保技能、示例与清单一致性。</p>
<p class="audit-callout audit-callout--highlight">需求 intake 与上游事实保护。<code class="code-ref">skills/novel-to-game/SKILL.md</code> 规定用户首次给出小说时必须先框定产品框架，锁进 PRODUCT_BRIEF，并由 pipeline-contract.md 确保下游各阶段（概念、美术、构建）必须继承而非重猜，有效防止需求偏移。</p>
<p class="audit-callout audit-callout--highlight">全书覆盖与独立审计验证。<code class="code-ref">tests/test_validate_repo.py</code> 中 test_example_source_bible_accounts_for_every_source_chapter 强制要求 SOURCE_BIBLE.md 的“全书覆盖”章节引用全部章节，保证游戏化拆解没有遗漏。金瓶梅示例的 expurgate.py 引入 FILTER_LEXICON 与 AUDIT_LEXICON 两个独立词表，避免循环论证，并通过独立审计词表判定退出码，防范删节残留。</p>
<p class="audit-callout audit-callout--doubt">构建与 QA 阶段高度依赖外部模型，技能自身不包含任何可本地执行的游戏代码生成或独立测试逻辑；若外部 CLI 代理不可用，流水线终止在 BUILD_BRIEF，无法产出实际可运行原型。</p>
<p class="audit-callout audit-callout--doubt">未审阅到针对生成游戏的自动化独立 QA 工具源码。game-qa 契约强调“自检不能自证”，但仓库未提供类似 expurgate.py 的独立检查脚本用于验收生成游戏的规则正确性，示例中提及的 battle.mjs 和 ledger.mjs 测试文件不在代码包内，无法评估覆盖质量。</p>
<p>优先为构建阶段提供最小化本地 mock 执行器，使流水线在没有外部模型时仍能输出框架性网页骨架；同时为 QA 阶段提供独立验证脚本模板，降低验收门槛，避免仅依赖生成模型的自检断言。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>技能强依赖 Claude Code / Codex / Kimi Code 等特定 CLI 代理，迁移到其他代理需重写适配层。</li><li>生成游戏的版权与原著 IP 授权需使用者自行审查，仓库示例仅选用公版作品，不可直接用于非公版小说的商业改编。</li><li>输出游戏的质量严重依赖底层语言模型能力，可能出现玩法不平衡或满篇 AI 腔文本，需要人工二次打磨，项目不提供后期精修支持。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>该项目作为开源技能集，能大幅降低从小说到可玩游戏原型的转换成本，尤其适合独立开发者、互动小说作者利用 AI 生成独特玩法，但自身不具备收费能力，不构成独立商业产品。</p>
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
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.25</span>
  </div>
</div>
</section>