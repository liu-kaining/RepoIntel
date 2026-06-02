---
title: '[Score: 75.5] S-Sigdel/vimhjkl'
date: '2026-06-02T23:00:42Z'
categories:
- Developer Tools
tags:
- vim
- terminal
- spaced-repetition
- python
- TUI
- keystroke-grading
intel_score: 75.5
repo_name: S-Sigdel/vimhjkl
repo_link: https://github.com/S-Sigdel/vimhjkl
summary: 在终端内启动真实 vim/nvim 做 Vim 高级技巧的间隔重复训练器，以击键效率评分并用 Leitner 分级管理掌握度，适合已过 vimtutor
  的中级 Vim 用户。
code_source: git
code_files_reviewed:
- pyproject.toml
- .github/workflows/aur-publish.yml
- .github/workflows/homebrew-bump.yml
- src/vimhjkl/__init__.py
- src/vimhjkl/__main__.py
- src/vimhjkl/keys.py
- src/vimhjkl/store.py
- src/vimhjkl/challenge.py
- src/vimhjkl/tui.py
- src/vimhjkl/engine.py
- src/vimhjkl/grader.py
- src/vimhjkl/cli.py
- packaging/homebrew/vimhjkl.rb
- README.md
- CONTRIBUTING.md
- tests/test_engine.py
- tests/test_grader.py
code_chars_analyzed: 127071
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
      <span class="scope-stat__value">17 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 127,071 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/aur-publish.yml</code></li><li><code class="path-chip">.github/workflows/homebrew-bump.yml</code></li><li><code class="path-chip">src/vimhjkl/__init__.py</code></li><li><code class="path-chip">src/vimhjkl/__main__.py</code></li><li><code class="path-chip">src/vimhjkl/keys.py</code></li><li><code class="path-chip">src/vimhjkl/store.py</code></li><li><code class="path-chip">src/vimhjkl/challenge.py</code></li><li><code class="path-chip">src/vimhjkl/tui.py</code></li><li><code class="path-chip">src/vimhjkl/engine.py</code></li><li><code class="path-chip">src/vimhjkl/grader.py</code></li><li><code class="path-chip">src/vimhjkl/cli.py</code></li><li><code class="path-chip">packaging/homebrew/vimhjkl.rb</code></li><li><code class="path-chip">README.md</code></li><li class="path-more">另有 3 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Vim 用户过完 vimtutor 后缺少结构化练习——dot command、text object、macro、:g/:s 等进阶技巧只能靠日常碰运气。记笔记、看视频都无法验证你「真的用对了最少键」，也没有间隔复习机制把刚学会的招式固化成长期肌肉记忆。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">CLI 入口 <code class="code-ref">src/vimhjkl/cli.py:main</code> 加载技能数据（<code class="code-ref">store.load_skills</code>）和玩家进度（<code class="code-ref">store.load_progress</code>），通过 <code class="code-ref">engine.py:select_due_skills</code> 基于 Leitner 分级 + difficulty gate 筛选待练习技能，再由 <code class="code-ref">engine.py:DrillSession.run</code> 依次调用 <code class="code-ref">grader.py:run_attempt</code>——该函数以 <code class="code-ref">vim -u NONE -W scriptout</code> 启动真实 vim，回读 buffer/cursor/scriptout 文件后走 <code class="code-ref">_score</code> 评分。整个调度层（engine.py）与 vim 交互层（grader.py）分离清晰，engine 对 vim 一无所知。数据模型在 <code class="code-ref">challenge.py:Skill</code>/<code class="code-ref">Challenge</code> 中，通过 <code class="code-ref">CATEGORIES</code> 注册表将 grading kind（buffer vs cursor）与是否需要 ex command 分类，新增技巧只改 JSON 不动引擎。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">grader.py:_tokenize</code> 对 scriptout 做多字节分词（nvim 0x80 三字节序列、ANSI 箭头转义），<code class="code-ref">_normalize_tokens</code> 消除 Backspace 对前一按键的撤销并合并连续 Esc，从而让 efficiency 评分惩罚退格和误触，而不是简单按字节计数——这在 <code class="code-ref">tests/test_grader.py:unit_checks</code> 中以 <code class="code-ref">count_keystrokes(b&quot;ciwHELLO\x1b:wq\r&quot;) == 9</code> 等断言验证。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">engine.py:select_due_skills</code> 用 Efraimidis–Spirakis 加权无放回采样实现「弱技能优先但每次顺序不同」的调度，同时将新技能与 box-maxed review 技能交错（<code class="code-ref">_interleave</code>），避免大堆已掌握技能占满 session 挤掉新内容——<code class="code-ref">tests/test_engine.py</code> 专门对此有 <code class="code-ref">session blends new + old practice</code> 回归测试。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">grader.py:_goal_window_script</code> 中 <code class="code-ref">cnoreabbrev &lt;expr&gt; q</code> 将 <code class="code-ref">q</code> 重映射为 <code class="code-ref">qall</code>，但注释说只匹配「整个命令行恰好是 q」。若用户输入 <code class="code-ref">:q</code> 后面带空格（<code class="code-ref">:q </code>），<code class="code-ref">getcmdline()</code> 返回 <code class="code-ref">q </code> 不匹配 <code class="code-ref">^q$</code>，缩写不生效，只剩一个窗口关闭——这在双窗布局下会导致 vim 不退出而用户以为已退出。<code class="code-ref">_build_argv</code> 行 154 附近缺少对此边界的防御。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">tests/</code> 目录只有 <code class="code-ref">test_engine.py</code> 和 <code class="code-ref">test_grader.py</code>，无 <code class="code-ref">test_store.py</code>/<code class="code-ref">test_tui.py</code>/<code class="code-ref">test_cli.py</code>。<code class="code-ref">store.py:_atomic_write</code> 使用 <code class="code-ref">.tmp</code> 后缀 + <code class="code-ref">os.replace</code> 实现原子写，但 progress.json 被 <code class="code-ref">cli.py</code> 的 KeyboardInterrupt handler 在任意位置调用 <code class="code-ref">store.save_progress</code>（<code class="code-ref">cli.py:main</code> 末尾），此时 progress dict 可能处于半更新状态——没有锁或写时复制。且 <code class="code-ref">store.py:SKILLS_PATH</code> 指向包内 <code class="code-ref">data/skills.json</code>，<code class="code-ref">save_skills</code> 也会写入该路径，如果用户以 wheel 安装则 site-packages 只读，调用会抛 <code class="code-ref">PermissionError</code>。</p>
<p>加一个 <code class="code-ref">test_store.py</code> 覆盖原子写入和 progress 并发场景；给 <code class="code-ref">save_skills</code> 加 <code class="code-ref">if not _is_source_checkout(): raise RuntimeError</code> 保护；<code class="code-ref">_goal_window_script</code> 中 <code class="code-ref">q</code> 的映射改为 <code class="code-ref">&#x27;^q\s*$&#x27;</code> 以匹配尾部空格。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>进度文件 progress.json 无并发锁，多终端同时运行或 Ctrl-C 时机不当可能导致数据丢失</li><li>wheel 安装后 save_skills 写 site-packages 会抛 PermissionError，当前无防护</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为纯 stdlib Python 包可通过 Homebrew/AUR 一键安装零依赖，适合写进 Vim 教程或搭配 dotfiles 仓库分享；但受众仅限认真学 Vim 的终端用户，难以延伸到企业场景。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.5</span>
  </div>
</div>
</section>