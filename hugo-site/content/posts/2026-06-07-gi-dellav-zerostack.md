---
title: '[Score: 78.25] gi-dellav/zerostack'
date: '2026-06-07T03:37:10Z'
categories:
- AI Coding Agent Runtime
tags:
- Rust
- CLI
- coding-agent
- terminal-ui
- multi-provider
- MCP
intel_score: 78.25
repo_name: gi-dellav/zerostack
repo_link: https://github.com/gi-dellav/zerostack
summary: Rust 编写的轻量级终端编码 Agent，17k 行代码、16MB 内存，支持多 LLM 供应商、权限系统和会话管理，适合资源敏感环境下的开发者日常编码辅助。
code_source: git
code_files_reviewed:
- Cargo.toml
- .github/workflows/ci.yml
- .github/workflows/update-models.yml
- .github/workflows/release.yml
- src/agent/mod.rs
- src/extras/mod.rs
- src/tests/mod.rs
- src/extras/subagents/mod.rs
- src/extras/mcp/mod.rs
- src/extras/loop/mod.rs
- src/ui/pickers/mod.rs
- src/extras/archmd/mod.rs
- src/session/mod.rs
- src/pricing.rs
- src/fs.rs
- src/docs.rs
- src/event.rs
- src/models_catalog.rs
- src/sandbox.rs
- src/auth.rs
- src/cli.rs
- src/provider.rs
- src/permission/ask.rs
- src/extras/truncate.rs
- src/context/prompts.rs
- src/session/chat_history.rs
- src/ui/terminal.rs
- src/context/themes.rs
- src/context/resources.rs
- src/permission/pattern.rs
- src/config/types.rs
- src/extras/status_signals.rs
- src/ui/permission_handler.rs
- src/ui/status.rs
- src/session/storage.rs
- src/ui/utils.rs
- src/agent/prompt.rs
- src/ui/events.rs
- src/config/load.rs
- src/agent/builder.rs
- src/permission/checker.rs
- src/agent/runner.rs
- src/ui/event_handler.rs
- src/ui/markdown.rs
- src/ui/renderer.rs
- src/tests/crc_tests.rs
- src/tests/slash_init_tests.rs
- src/tests/slash_add_tests.rs
code_chars_analyzed: 245005
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
      <span class="scope-stat__value">约 245,005 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Cargo.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/update-models.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/agent/mod.rs</code></li><li><code class="path-chip">src/extras/mod.rs</code></li><li><code class="path-chip">src/tests/mod.rs</code></li><li><code class="path-chip">src/extras/subagents/mod.rs</code></li><li><code class="path-chip">src/extras/mcp/mod.rs</code></li><li><code class="path-chip">src/extras/loop/mod.rs</code></li><li><code class="path-chip">src/ui/pickers/mod.rs</code></li><li><code class="path-chip">src/extras/archmd/mod.rs</code></li><li><code class="path-chip">src/session/mod.rs</code></li><li><code class="path-chip">src/pricing.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>Node.js/Python 实现的编码 Agent（如 opencode）在闲置时占用 ~300MB RAM、CPU ~2%，对老旧开发机或远程服务器资源消耗过大；开发者需要一个可在 SSH 终端里低开销运行、具备完整权限控制和多模型切换的编码助手。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 rig（Rust agent framework）作为底层 LLM 抽象层，通过 <code class="code-ref">src/provider.rs</code> 中的 <code class="code-ref">AnyClient</code> / <code class="code-ref">AnyModel</code> / <code class="code-ref">AnyAgent</code> 三层枚举统一 OpenRouter、OpenAI（含 Responses / Completions 双 API 风格）、Anthropic、Gemini、Ollama 五种供应商。Agent 构建在 <code class="code-ref">src/agent/builder.rs</code> 的 <code class="code-ref">build_agent_inner</code> 中完成：preamble 由系统提示 + AGENTS.md + ARCHITECTURE.md + 活跃 prompt 模式 + 工作目录拼接，工具列表通过 <code class="code-ref">SmallVec&lt;[Box&lt;dyn ToolDyn&gt;; 8]&gt;</code> 收集读/写/编辑/bash/grep/find/list/todo 八个核心工具，再条件编译追加 subagent task、memory、MCP 工具。流式执行在 <code class="code-ref">src/agent/runner.rs:spawn_agent</code> 中通过 <code class="code-ref">tokio::spawn</code> 驱动 rig 的 <code class="code-ref">stream_chat</code> 多轮循环，事件经 <code class="code-ref">mpsc::channel(32)</code> 推送至 TUI 层。TUI 渲染由 <code class="code-ref">src/ui/renderer.rs</code> 实现基于 crossterm 的滚动视口，支持鼠标选择、Markdown 渲染（<code class="code-ref">src/ui/markdown.rs</code> 用 pulldown_cmark 解析）、CJK 宽度感知。权限系统在 <code class="code-ref">src/permission/checker.rs</code> 中实现五种安全模式（Restrictive/ReadOnly/Guarded/Standard/Yolo），支持 glob + regex 双层规则匹配、session allowlist、doom-loop 检测（连续 3 次相同调用触发 coaching 或拦截）。会话压缩在 <code class="code-ref">src/provider.rs:compress_messages</code> 中调用 LLM 总结历史并替换消息，<code class="code-ref">src/session/mod.rs:compact</code> 管理 token 预算。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/sandbox.rs</code> 提供 bwrap 和 zerobox 双后端沙箱隔离，bwrap 模式通过 <code class="code-ref">--clearenv</code> + 白名单环境变量 + namespace 隔离（IPC/PID/UTS/cgroup）实现，这是编码 Agent 中少见的进程级防护设计。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/permission/checker.rs:doom_loop_check</code> 实现了重复调用检测（16 个最近调用的 VecDeque），当同一 tool+input 连续调用 ≥3 次时触发 coaching 提示或拦截，有效防止 Agent 陷入死循环浪费 token。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/extras/subagents/mod.rs</code> 中 <code class="code-ref">CONFIG</code> 和 <code class="code-ref">SUBAGENT_EVENT_TX</code> 使用 <code class="code-ref">std::sync::Mutex</code> 全局静态变量，且 <code class="code-ref">init()</code> 不是幂等的——多次调用会覆盖配置。在多线程场景下（<code class="code-ref">multithread</code> feature），<code class="code-ref">SUBAGENT_EVENT_TX</code> 的 <code class="code-ref">lock().unwrap_or_else</code> 模式虽处理了 poison，但全局 Mutex 可能成为并发瓶颈。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/ui/event_handler.rs:handle_agent_done</code> 函数签名有 22 个参数（含多个 <code class="code-ref">#[cfg(feature)]</code> 条件参数），这是典型的「上帝函数」模式，可维护性堪忧。未审阅到 <code class="code-ref">src/config/mod.rs</code> 完整定义，无法确认 <code class="code-ref">Config</code> 结构体的所有默认值和验证逻辑。</p>
<p>适合需要在低配服务器或 SSH 环境运行编码 Agent 的开发者试用；建议先在 sandbox 模式下验证安全性；MCP 和 ACP 为可选编译特性，需按需启用；关注 rig 框架升级对 AnyClient 枚举的维护成本。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>CI 仅 <code class="code-ref">cargo build --release</code> 无测试步骤，<code class="code-ref">cargo test</code> 未在 CI 中执行，代码质量保障依赖本地开发者自觉</li><li>README 声称 Windows 支持未经测试，且 <code class="code-ref">src/session/storage.rs:dirs_path</code> 依赖 <code class="code-ref">dirs::data_dir()</code> 在 Windows 路径下的行为未验证</li><li><code class="code-ref">src/provider.rs</code> 中 <code class="code-ref">AnyClient</code> 枚举随 rig 版本升级需手动适配每个供应商，技术债会随 rig 上游变更累积</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>对资源敏感的开发团队（远程服务器、CI 环境、老旧硬件）有明确价值，16MB 内存占用是硬指标差异；GPL-3.0 许可证限制商业集成，但作为独立工具具备社区增长潜力。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">71</div>
  <div class="score-bar"><span style="width:71%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.25</span>
  </div>
</div>
</section>