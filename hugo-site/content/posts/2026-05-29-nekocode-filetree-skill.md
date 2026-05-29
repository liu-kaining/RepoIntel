---
title: '[Score: 75.9] nekocode/filetree-skill'
date: '2026-05-29T02:56:26Z'
categories:
- Developer Tools
tags:
- Claude Code Plugin
- Git
- Python
- LLM Context
- CLI
intel_score: 75.9
repo_name: nekocode/filetree-skill
repo_link: https://github.com/nekocode/filetree-skill
summary: Claude Code 插件，为仓库维护一行一文件的 FILETREE.md 索引并带内容 hash 检测漂移，帮助 LLM 在每次会话开始时跳过重复的文件发现开销。
code_source: git
code_files_reviewed:
- .claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- tests/conftest.py
- commands/lint.md
- commands/update.md
- README.zh.md
- README.md
- commands/init.md
- skills/filetree/SKILL.md
- skills/filetree/scripts/filetree.py
- tests/test_filetree.py
code_chars_analyzed: 96108
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
      <span class="scope-stat__value">11 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 96,108 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">.claude-plugin/plugin.json</code></li><li><code class="path-chip">.claude-plugin/marketplace.json</code></li><li><code class="path-chip">tests/conftest.py</code></li><li><code class="path-chip">commands/lint.md</code></li><li><code class="path-chip">commands/update.md</code></li><li><code class="path-chip">README.zh.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">commands/init.md</code></li><li><code class="path-chip">skills/filetree/SKILL.md</code></li><li><code class="path-chip">skills/filetree/scripts/filetree.py</code></li><li><code class="path-chip">tests/test_filetree.py</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>使用 Claude Code 的开发者每次新开会话时，Agent 都要重新执行 ls/grep/cat 探索仓库结构，花费大量 token 且不可跨会话复用；手动维护的摘要文档容易静默过期，团队协作时尤其无法察觉。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整个插件由单个 Python 脚本 <code class="code-ref">skills/filetree/scripts/filetree.py</code>（~580 行）承担全部确定性操作，通过 argparse 提供 <code class="code-ref">todo</code>/<code class="code-ref">lint</code>/<code class="code-ref">apply</code>/<code class="code-ref">wire-target</code> 四个子命令。<code class="code-ref">todo</code> 命令调用 <code class="code-ref">list_current_files()</code> 合并 <code class="code-ref">git ls-files -z</code>（已跟踪）和 <code class="code-ref">git ls-files --others --exclude-standard -z</code>（未跟踪未忽略），同时过滤 mode 160000 的 submodule gitlink（<code class="code-ref">skills/filetree/scripts/filetree.py:68-78</code>），防止 <code class="code-ref">git hash-object</code> 遇到 gitlink 时 exit 128 崩溃。<code class="code-ref">cmd_apply</code> 是核心写入路径：它从 payload 只接收 <code class="code-ref">{path, summary}</code> 对，所有 hash 从磁盘实时计算（<code class="code-ref">skills/filetree/scripts/filetree.py:280</code>），rename/removed 从 repo state 重新推导（<code class="code-ref">skills/filetree/scripts/filetree.py:263-267</code>），彻底杜绝 LLM 传回脏数据污染 manifest。写入使用 tmp + <code class="code-ref">os.replace</code> 原子操作（<code class="code-ref">skills/filetree/scripts/filetree.py:188-190</code>）。</p>
<p class="audit-callout audit-callout--highlight">symlink 处理严谨 — <code class="code-ref">hash_files</code> 对普通文件用 <code class="code-ref">--stdin-paths</code> 批量哈希绕过 ARG_MAX，对 symlink 单独用 <code class="code-ref">os.readlink</code> 获取 raw bytes 后通过 <code class="code-ref">--stdin</code> 哈希（<code class="code-ref">skills/filetree/scripts/filetree.py:105-120</code>），避免了 <code class="code-ref">--stdin-paths</code> 追踪链接内容并遇坏链接 exit 128 的问题，且 bytes 而非 str 处理 non-UTF-8 链接目标。</p>
<p class="audit-callout audit-callout--highlight">UNCHANGED bias 设计精巧 — <code class="code-ref">cmd_apply</code> 中对 summary 等于 <code class="code-ref">UNCHANGED</code> 的条目只刷新 hash 保留旧摘要（<code class="code-ref">skills/filetree/scripts/filetree.py:295-303</code>），且对无 prior entry 的 UNCHANGED 调用会报 <code class="code-ref">skipped_unchanged_new</code> 而非静默丢弃（<code class="code-ref">skills/filetree/scripts/filetree.py:300-303</code>），配合 <code class="code-ref">merge_payloads</code> 的 last-writer-wins 去重（<code class="code-ref">skills/filetree/scripts/filetree.py:231-240</code>），让并行 sub-agent 场景下不会因重试产生假计数。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">_unquote_git_path</code> 的 C-style 转义解析器（<code class="code-ref">skills/filetree/scripts/filetree.py:131-151</code>）手动实现了八进制和简单转义字符的解码，但注释提到这是「migration hook」，未审阅到任何自动化迁移流程或对旧 manifest 的主动扫描。如果团队中有人用旧版本生成了 manifest，新版本只能在逐条 parse 时被动解码，不会一次性修正文件中的 quoted-octal 原文，这意味着 git diff 中仍会看到 legacy 格式的条目。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">list_current_files</code> 未对 <code class="code-ref">git ls-files</code> 的输出做任何异常处理 — 若 git 命令因权限或 corrupt index 失败，<code class="code-ref">subprocess.check_output</code> 会抛 <code class="code-ref">CalledProcessError</code>，但外层 <code class="code-ref">cmd_todo</code> 和 <code class="code-ref">cmd_apply</code> 均未 catch 并给出友好提示，只在 <code class="code-ref">require_git</code> 中做了基本的 repo 存在性检查。</p>
<p>纯 Python stdlib 零依赖、单文件部署是极大的加分项，适合在任何有 git 的项目中试用。建议先用 <code class="code-ref">/filetree:init</code> 在一个中型 repo 上跑一次，观察 token 节省效果；CI 接入 <code class="code-ref">lint</code> 可直接在 pre-commit 或 GitHub Actions 中加一行。注意该插件深度绑定 Claude Code plugin 格式，不能用于 Cursor/Copilot 等其他 AI 编码工具。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目创建仅 2 天、14 次 commit、无 CI 配置文件，维护者单人，长期可维护性未验证。</li><li>深度绑定 Claude Code plugin 协议（<code class="code-ref">plugin.json/marketplace.js</code>on/skills/），README 未提及任何其他 AI 编码工具的兼容路径，生态迁移成本高。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Claude Code 生态中的上下文管理工具，解决了 Agent 定位仓库结构的高频痛点；若 Claude Code 市场生态扩大，这类「减少 token 浪费」的插件有望成为标配。但其价值上限取决于 Claude Code 的市场渗透率，且核心功能单一、护城河有限。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">52</div>
  <div class="score-bar"><span style="width:52%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.9</span>
  </div>
</div>
</section>