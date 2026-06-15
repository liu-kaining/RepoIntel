---
title: '[Score: 75.05] tmchow/illo-skill'
date: '2026-06-15T23:01:23Z'
categories:
- AI Agent Skill — Editorial Illustration Engine
tags:
- image-generation
- prompt-engineering
- agent-skill
- OpenRouter
- character-consistency
- risograph
intel_score: 75.05
repo_name: tmchow/illo-skill
repo_link: https://github.com/tmchow/illo-skill
summary: 面向 AI Agent 运行时的编辑插画技能，通过结构化 prompt 配方与参考图锁定实现角色一致性，适配 Claude Code / Codex
  / Gemini CLI 等多平台，适合技术博客作者为文章生成风格统一的配图。
code_source: git
code_files_reviewed:
- .github/workflows/version-sync.yml
- .github/workflows/asset-checksums.yml
- .github/workflows/publish-clawhub.yml
- CLAUDE.md
- .agents/plugins/marketplace.json
- gemini-extension.json
- .codex-plugin/plugin.json
- .claude-plugin/marketplace.json
- .cursor-plugin/plugin.json
- .claude-plugin/plugin.json
- .github/scripts/skill_frontmatter_version.py
- .github/scripts/clawhub_version_state.py
- skills/illo/scripts/repair-hermes-assets.sh
- skills/illo/references/styles/woodcut.md
- .github/scripts/sync_plugin_versions.py
- .github/scripts/regen_asset_checksums.py
- skills/illo/references/styles/chalk.md
- skills/illo/references/styles/pixel.md
- skills/illo/references/styles/blueprint.md
- skills/illo/references/styles/phosphor.md
- skills/illo/references/styles/gouache.md
- skills/illo/references/styles/manila.md
- skills/illo/references/visual-style.md
- skills/illo/references/styles/clay.md
- skills/illo/references/models.md
- skills/illo/references/styles/enamel.md
- README.md
- skills/illo/references/palettes.md
- skills/illo/references/pack-sharing.md
- skills/illo/references/styles/felt.md
- skills/illo/references/backends.md
- skills/illo/references/quality-bar.md
- skills/illo/references/character.md
- skills/illo/references/prompt-recipe.md
- skills/illo/references/character-builder.md
- skills/illo/README.md
- AGENTS.md
- skills/illo/references/composition.md
- skills/illo/SKILL.md
code_chars_analyzed: 198437
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
      <span class="scope-stat__value">39 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 198,437 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.github/workflows/version-sync.yml</code></li><li><code class="path-chip">.github/workflows/asset-checksums.yml</code></li><li><code class="path-chip">.github/workflows/publish-clawhub.yml</code></li><li><code class="path-chip">CLAUDE.md</code></li><li><code class="path-chip">.agents/plugins/marketplace.json</code></li><li><code class="path-chip">gemini-extension.json</code></li><li><code class="path-chip">.codex-plugin/plugin.json</code></li><li><code class="path-chip">.claude-plugin/marketplace.json</code></li><li><code class="path-chip">.cursor-plugin/plugin.json</code></li><li><code class="path-chip">.claude-plugin/plugin.json</code></li><li><code class="path-chip">.github/scripts/skill_frontmatter_version.py</code></li><li><code class="path-chip">.github/scripts/clawhub_version_state.py</code></li><li><code class="path-chip">skills/illo/scripts/repair-hermes-assets.sh</code></li><li><code class="path-chip">skills/illo/references/styles/woodcut.md</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>技术博主写完文章后需要一张风格统一的编辑配图，手动找插画师成本高、周期长，用通用图像生成器则角色不一致、风格漂移、每次生成都像随机抽取，且不同文章/平台的配图缺乏品牌辨识度。illo 试图用结构化 prompt 模板 + 参考图条件锁定 + 调色板系统解决这个一致性问题。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整个技能是一个 Agent Skill（SKILL.md 格式），核心是一个纯 Python stdlib 脚本 <code class="code-ref">skills/illo/scripts/illo.py</code>（未在 code_bundle 中提供源码，本次结论不覆盖其内部逻辑）。用户侧调用链为：SKILL.md 定义工作流步骤 → 引用 <code class="code-ref">references/</code> 下的十余个 Markdown 参考文件构建 prompt → 通过 <code class="code-ref">illo.py generate</code> 命令调用 Codex CLI 或 OpenRouter API 生成图片。技能本身无复杂运行时依赖，但 prompt 模板工程量很大。</p>
<p class="audit-callout audit-callout--highlight">风格系统的设计很有层次感。十种 look（riso、blueprint、woodcut、pixel、clay 等）各自在 <code class="code-ref">references/styles/&lt;name&gt;.md</code> 中定义 prompt blocks、palette mapping、character treatment 和 QA deltas，每个文件约 3KB，职责单一。以 <code class="code-ref">skills/illo/references/styles/clay.md</code> 为例，它明确记录了已知失败模式（平面素材穿帮到 clay 场景中），并在 CHARACTER forcing line 中强制要求 re-roll——这种「已知缺陷 + 强制校验」的文档模式值得参考。</p>
<p class="audit-callout audit-callout--highlight">版本管理与发布管线设计精细。<code class="code-ref">.github/scripts/sync_plugin_versions.py</code> 以 <code class="code-ref">skills/illo/SKILL.md</code> frontmatter 的 version 字段为单一事实来源，自动同步到 5 个插件 manifest（<code class="code-ref">.claude-plugin/plugin.json</code>、<code class="code-ref">.codex-plugin/plugin.json</code>、<code class="code-ref">.cursor-plugin/plugin.json</code>、<code class="code-ref">gemini-extension.json</code>、<code class="code-ref">.claude-plugin/marketplace.json</code>）。<code class="code-ref">.github/workflows/version-sync.yml</code> 在 PR 上自动提交同步、在 main 上验证一致性。<code class="code-ref">.github/workflows/publish-clawhub.yml</code> 在 version 为新时自动发布到 ClawHub 并创建 git tag——这套 CI 管线对一个 3 天的仓库来说工程意识很强。</p>
<p class="audit-callout audit-callout--doubt">核心引擎 <code class="code-ref">scripts/illo.py</code> 的源码未在 code_bundle 中提供。该文件是所有生成逻辑的承载点（双后端选择、OpenRouter API 调用、Codex CLI subprocess 调用、JSON 输出、manifest 写入），但本次无法审阅其错误处理、重试逻辑、超时机制、并发行为和安全实现。AGENTS.md 中大量安全规则（不读 env 变量、config 文件 mode 600、仅通过 getpass 收集 key）若没有源码佐证，无法确认 <code class="code-ref">illo.py</code> 实际遵守。降低 engineering 分数。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">skills/illo/scripts/repair-hermes-assets.sh</code> 是一个针对 Hermes 运行时已知 bug 的 workaround（<code class="code-ref">repair-hermes-assets.sh:10-13</code> 注释说明了 Hermes 将二进制文件按文本解码导致损坏）。这个修复脚本依赖 <code class="code-ref">assets/checksums.txt</code> 中的 SHA256 + pin-commit 体系，<code class="code-ref">regen_asset_checksums.py</code> 负责生成该 manifest。逻辑自洽，但整个 Hermes 兼容层是临时方案，README 和 AGENTS.md 均注明「Remove once Hermes ships its installer fix」——这增加了维护负担，且没有自动检测 Hermes 是否已修复的机制。</p>
<p>需要实际审阅 <code class="code-ref">scripts/illo.py</code> 的源码才能给出完整工程评估。当前 repo 的 prompt 参考文档质量极高（每个 style 文件都有已知失败模式、QA delta、calibration example URL），但缺少自动化测试——未见到任何 <code class="code-ref">tests/</code> 目录或 <code class="code-ref">*_test.*</code> 文件，所有质量保证完全依赖文档化的 QA checklist 和人工 re-roll。对于一个 3 天的仓库，文档密度与 CI 完善度超出预期，但核心引擎和测试覆盖是明显的空白。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心引擎 <code class="code-ref">scripts/illo.py</code> 源码未在本次 code_bundle 中提供，所有关于安全实现、错误处理、后端切换的判断均基于文档而非代码，存在声明与实现不一致的风险。</li><li>Fork/Star 比仅 1.5%（2 forks / 131 stars），repo 仅 3 天、8 次 commit，社区采用证据极薄；131 stars 可能反映的是作者个人影响力而非实际用户验证。</li><li>风格系统依赖十余个 Markdown prompt 模板，无自动化测试验证 prompt 拼装正确性或生成质量回归，所有质量保证靠人工 QA checklist 和 re-roll。</li><li>OpenRouter 后端的默认模型 Grok Imagine 不在公开模型列表中，README 和 models.md 均注明「works for accounts with access」，用户首次使用可能遇到 404。</li><li>Hermes 兼容层（repair-hermes-assets.sh）是临时 workaround，依赖外部仓库 raw URL 下载修复文件，无自动检测 Hermes 是否已修好的退出机制。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>illo 定位为技术写作配图的垂直工具，通过多平台 Agent Skill 生态（Claude Code、Codex、Gemini CLI、Copilot、Hermes、OpenClaw）分发，ClawHub 发布管线已通。若 Agent Skill 生态起量，作为头部创意类技能有先发价值；但核心依赖 OpenRouter 图像 API 的定价和可用性，且没有自建模型壁垒。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">71</div>
  <div class="score-bar"><span style="width:71%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.05</span>
  </div>
</div>
</section>