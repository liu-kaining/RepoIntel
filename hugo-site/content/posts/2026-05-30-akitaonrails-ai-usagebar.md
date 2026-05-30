---
title: '[Score: 76.8] akitaonrails/ai-usagebar'
date: '2026-05-30T02:49:50Z'
categories:
- Developer Tools
tags:
- Waybar
- Rust
- CLI
- TUI
- OAuth
- Linux Desktop
intel_score: 76.8
repo_name: akitaonrails/ai-usagebar
repo_link: https://github.com/akitaonrails/ai-usagebar
summary: 将 Claudebar 的 Bash 脚本用 Rust 重写并扩展至四家 AI 供应商，面向 Linux 桌面 Waybar 用户的计划用量监控小部件。
code_source: git
code_files_reviewed:
- Makefile
- Cargo.toml
- .github/workflows/release.yml
- src/tui/mod.rs
- src/openrouter/mod.rs
- src/zai/mod.rs
- src/openai/mod.rs
- src/anthropic/mod.rs
- src/widget/mod.rs
- src/lib.rs
- src/vendor.rs
- src/countdown.rs
- src/error.rs
- src/active.rs
- src/waybar.rs
- src/format.rs
- src/tooltip.rs
- src/pango.rs
- src/usage.rs
- src/theme.rs
- src/pacing.rs
- src/config.rs
- src/cache.rs
- src/bin/ai-usagebar.rs
- src/tui/view.rs
- src/openrouter/types.rs
- src/openai/oauth.rs
- src/widget/pretty.rs
- src/openai/creds.rs
- src/anthropic/types.rs
- src/bin/ai-usagebar-tui.rs
- src/zai/fetch.rs
- src/zai/types.rs
- src/tui/app.rs
- src/anthropic/oauth.rs
- src/anthropic/creds.rs
- src/widget/cli.rs
- src/openai/types.rs
- src/openrouter/fetch.rs
- src/zai/vendor.rs
- src/openai/fetch.rs
- src/openrouter/vendor.rs
- src/widget/run.rs
- src/openai/vendor.rs
- src/anthropic/fetch.rs
- src/tui/panels.rs
- src/widget/render.rs
- src/tui/settings.rs
code_chars_analyzed: 348767
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
      <span class="scope-stat__value">约 348,767 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/tui/mod.rs</code></li><li><code class="path-chip">src/openrouter/mod.rs</code></li><li><code class="path-chip">src/zai/mod.rs</code></li><li><code class="path-chip">src/openai/mod.rs</code></li><li><code class="path-chip">src/anthropic/mod.rs</code></li><li><code class="path-chip">src/widget/mod.rs</code></li><li><code class="path-chip">src/lib.rs</code></li><li><code class="path-chip">src/vendor.rs</code></li><li><code class="path-chip">src/countdown.rs</code></li><li><code class="path-chip">src/error.rs</code></li><li><code class="path-chip">src/active.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>使用 Claude Pro/Max、ChatGPT Plus、Z.AI 或 OpenRouter 的开发者无法在桌面状态栏一眼看到各供应商的会话/周额度消耗率、倒计时和配额余额，只能手动打开网页或 CLI 查看；多供应商用户更需要一个统一视图以免在不同工具间切换。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">库按供应商分为 <code class="code-ref">src/anthropic/</code>、<code class="code-ref">src/openai/</code>、<code class="code-ref">src/zai/</code>、<code class="code-ref">src/openrouter/</code> 四个子模块，每个模块遵循「creds → maybe-refresh → fetch → cache → render」的统一流水线，由 <code class="code-ref">src/vendor.rs:11</code> 的 <code class="code-ref">VendorId</code> 枚举驱动分发。两个二进制入口 <code class="code-ref">src/bin/ai-usagebar.rs</code> 和 <code class="code-ref">src/bin/ai-usagebar-tui.rs</code> 均为薄壳：前者通过 <code class="code-ref">src/widget/run.rs:13</code> 的 <code class="code-ref">run()</code> 走 tokio current_thread 后必定 <code class="code-ref">exit(0)</code>，保证 Waybar 永远不会隐藏模块；后者通过 <code class="code-ref">src/bin/ai-usagebar-tui.rs:58</code> 的 <code class="code-ref">event_loop</code> 用 <code class="code-ref">tokio::select!</code> 并行处理键盘事件、定时刷新和后台 fetch 结果。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/cache.rs:76</code> 的 <code class="code-ref">write_payload</code> 使用 <code class="code-ref">tempfile::persist</code>（POSIX rename）实现原子写入，配合 <code class="code-ref">src/cache.rs:110</code> 的 <code class="code-ref">acquire_lock</code>（flock + 50ms 轮询 + 可配置超时），让多显示器 Waybar 实例不会并发打 API——工程上比 Shell 版的 <code class="code-ref">exec 9&gt;&quot;$_lockfile&quot;</code> 更可靠。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/error.rs:1</code> 的 <code class="code-ref">AppError</code> 枚举把网络层（<code class="code-ref">Transport</code>）、协议层（<code class="code-ref">Http</code>）、语义层（<code class="code-ref">Schema</code>）、本地 I/O（<code class="code-ref">Io</code>）分离为不同变体，<code class="code-ref">is_transient()</code> 只对 <code class="code-ref">Transport</code> 返回 true，使得 <code class="code-ref">src/anthropic/fetch.rs:90</code> 的 fallback 逻辑可以区分「静默降级到缓存」和「标记 stale 并写 <code class="code-ref">.last_error</code>」两条路径。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/openrouter/fetch.rs:75</code> 的 <code class="code-ref">reuse_cache</code> 用手写 JSON 字段访问（<code class="code-ref">s[&quot;label&quot;].as_str()</code>）反序列化缓存，而同模块的 <code class="code-ref">fetch_snapshot</code> 用 <code class="code-ref">serde_json::from_slice</code> 反序列化 API 响应——两条路径的 schema 容错度不一致，若缓存格式升级时容易出现静默丢失字段。</p>
<p class="audit-callout audit-callout--doubt">四个供应商的 renderer（如 <code class="code-ref">src/zai/vendor.rs</code>、<code class="code-ref">src/openrouter/vendor.rs</code>）各自独立实现 tooltip 渲染，~200 行 <code class="code-ref">push_window</code> + <code class="code-ref">render_bordered</code> 调用高度重复；若新增供应商或调整 tooltip 布局，需要在多处同步修改。</p>
<p>该项目面向已使用 Waybar 的 Linux 桌面用户，开箱即可 <code class="code-ref">cargo install</code> 并用默认 config 运行 Anthropic 供应商；如需其他供应商则需配置 API key。建议先用 <code class="code-ref">--pretty</code> 或 TUI 验证各供应商端点可达性，再配置 Waybar 模块。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>四个供应商端点均未文档化（README 明确提及 &quot;undocumented endpoint&quot;），API schema 任何变更都会导致功能静默失效，需持续维护 smoke 测试。</li><li>项目仅 6 天历史、9 次 commit，维护者单一（AkitaOnRails），长期维护和社区贡献的可持续性未经验证。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Waybar 生态中唯一覆盖四家 AI 计划供应商的用量监控小部件，对重度使用多家 AI 编码助手的 Linux 桌面用户有明确价值；但 Waybar 用户基数本身较小，且项目依赖未文档化的 API 端点，商业扩展空间有限。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.8</span>
  </div>
</div>
</section>