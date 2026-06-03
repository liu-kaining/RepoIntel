---
title: '[Score: 79.65] duncatzat/vigils'
date: '2026-06-03T10:53:56Z'
categories:
- AI Agent Security Control Plane
tags:
- Rust
- Tauri
- MCP
- sandbox
- audit-ledger
- Chrome-extension
intel_score: 79.65
repo_name: duncatzat/vigils
repo_link: https://github.com/duncatzat/vigils
summary: 本地优先的 AI Agent 控制面，用 Rust 构建带审计账本、策略防火墙和 PII 脱敏的 MCP 网关，适合重度使用 Claude Code/Cursor
  等工具的开发者管控 Agent 行为。
code_source: git
code_files_reviewed:
- crates/vigil-browser/Cargo.toml
- crates/vigil-types/Cargo.toml
- crates/vigil-policy/Cargo.toml
- crates/vigil-http-auth/Cargo.toml
- crates/vigil-ui-protocol/Cargo.toml
- apps/native-host/Cargo.toml
- .github/workflows/docs.yml
- .github/workflows/ci.yml
- .github/workflows/release.yml
- apps/vigil-hub-cli/src/lib.rs
- crates/vigil-policy/src/lib.rs
- crates/vigil-mcp/src/lib.rs
- crates/vigil-http-transport/src/lib.rs
- crates/vigil-runner-types/src/lib.rs
- crates/vigil-types/src/lib.rs
- crates/vigil-lease/src/lib.rs
- apps/desktop/src/lib.rs
- crates/vigil-browser/src/lib.rs
- apps/desktop/tauri.conf.json
- crates/vigil-runner-types/README.md
- apps/desktop/build.rs
- crates/vigil-sdk/README.md
- apps/desktop/README.md
- crates/vigil-audit/tests/print_hash_vectors.rs
- crates/vigil-mcp/tests/upstream_non_exhaustive.rs
- crates/vigil-audit/tests/hash_chain_vectors.rs
- crates/vigil-http-auth/tests/audit_strings_golden.rs
- crates/vigil-runner/tests/audit_strings_golden.rs
- apps/desktop/tests/embed_hub_skeleton.rs
- crates/vigil-browser/tests/audit_strings_golden.rs
- apps/vigil-hub-cli/tests/cli_add_remote.rs
- apps/desktop/ui/postcss.config.js
- apps/desktop/icons/README.md
- apps/desktop/ui/tsconfig.json
- apps/desktop/ui/tailwind.config.js
- crates/vigil-types/src/invocation.rs
- apps/desktop/ui/vite.config.ts
- apps/desktop/src/render.rs
- crates/vigil-types/src/decision.rs
- crates/vigil-types/src/audit.rs
- crates/vigil-http-auth/src/types.rs
- crates/vigil-types/src/session.rs
- crates/vigil-types/src/principal.rs
- crates/vigil-types/src/server.rs
- apps/desktop/capabilities/default.json
- crates/vigil-ui-protocol/src/error.rs
- crates/vigil-redaction/benches/scrub.rs
- crates/vigil-audit/src/error.rs
code_chars_analyzed: 74707
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
      <span class="scope-stat__value">约 74,707 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crates/vigil-browser/Cargo.toml</code></li><li><code class="path-chip">crates/vigil-types/Cargo.toml</code></li><li><code class="path-chip">crates/vigil-policy/Cargo.toml</code></li><li><code class="path-chip">crates/vigil-http-auth/Cargo.toml</code></li><li><code class="path-chip">crates/vigil-ui-protocol/Cargo.toml</code></li><li><code class="path-chip">apps/native-host/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/docs.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">apps/vigil-hub-cli/src/lib.rs</code></li><li><code class="path-chip">crates/vigil-policy/src/lib.rs</code></li><li><code class="path-chip">crates/vigil-mcp/src/lib.rs</code></li><li><code class="path-chip">crates/vigil-http-transport/src/lib.rs</code></li><li><code class="path-chip">crates/vigil-runner-types/src/lib.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在 Cursor、Claude Code 等 AI 工具中授权 Agent 读写文件、调 API、访问密钥，但无法事后审计 Agent 做了什么、无法在高危操作前拦截，也无法防止 prompt/日志泄露 API Key 和 PII。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整体是一个 Rust workspace，以 <code class="code-ref">vigil-mcp</code>（MCP Hub）为中央网关，拦截所有 <code class="code-ref">tools/call</code> 请求，经过 Policy 引擎裁决→必要时等待人工审批→Runner 沙箱执行→审计账本记录。前端分桌面端（Tauri 2 + Vue 3）和 Chrome MV3 扩展两条通道。</p>
<p class="audit-callout audit-callout--highlight">审计账本设计扎实。<code class="code-ref">crates/vigil-audit/tests/hash_chain_vectors.rs</code> 钉死了 SHA-256 hash chain 的四条测试向量（TV1-TV3 + domain constant 契约），使用 JCS（JSON Canonicalization Scheme）确保 key 乱序不影响 hash，<code class="code-ref">crates/vigil-audit/src/error.rs:HardSecretDetected</code> 在 <code class="code-ref">append_event</code> 入口做 fail-closed 硬指纹检测，拒绝含原始 secret 的 payload 写入——这是一条主动防御而非被动清理。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">#[non_exhaustive]</code> + golden test 策略覆盖多个 crate。<code class="code-ref">crates/vigil-mcp/tests/upstream_non_exhaustive.rs</code> 从消费者 integration test 视角验证 <code class="code-ref">UpstreamError</code> 的 <code class="code-ref">_ =&gt;</code> 兜底编译约束；<code class="code-ref">crates/vigil-runner/tests/audit_strings_golden.rs</code> 用 <code class="code-ref">ALL_KNOWN</code> 双向校验枚举变体与 golden 字符串，确保新增 variant 不漏同步。跨 crate ABI 稳定性守门做得比一般开源项目严谨。</p>
<p class="audit-callout audit-callout--doubt">代码包中未提供 <code class="code-ref">vigil-runner</code>（含 <code class="code-ref">WasmRunner</code>/<code class="code-ref">spawn_native</code>）、<code class="code-ref">vigil-redaction</code>（含 <code class="code-ref">scrub_text</code>/ML ensemble）、<code class="code-ref">vigil-firewall</code>、<code class="code-ref">vigil-audit</code>（完整源码）、<code class="code-ref">vigil-sandbox-linux</code>（Landlock）、<code class="code-ref">vigil-hub-cli/src/serve.rs</code> 等核心实现文件，仅见到 manifest 和少量 <code class="code-ref">tests/lib.rs</code>。sandbox 的 fail-closed 行为、redaction 的 ML ensemble 质量、firewall 的策略引擎细节均无法验证，本次工程评分不覆盖这些模块。</p>
<p class="audit-callout audit-callout--doubt">项目仅 2 天历史、9 次提交，核心 crate 源码大面积缺失于 code_bundle 中。README 声称 743+ 测试，但仓库 root 的 <code class="code-ref">tests/</code> 目录和多数 crate 的 <code class="code-ref">src/</code> 未收录，无法独立确认测试覆盖率。<code class="code-ref">apps/desktop/build.rs:include!(&quot;src/commands.rs&quot;)</code> 的 SSOT 跨文件 include 模式虽然精巧，但耦合度高，若 <code class="code-ref">commands.rs</code> 有 <code class="code-ref">#[cfg(test)]</code> 以外的顶层副作用会影响 build script 行为。</p>
<p>对 MCP 重度用户（每天 10+ 次 Claude Code tool call），可先用 CLI 模式 <code class="code-ref">vigil-hub serve --stdio</code> 接入现有工作流，验证审计账本和 policy 规则的实际拦截效果。Desktop GUI 尚在 α1 阶段（icon 占位、<code class="code-ref">tauri build</code> 会失败），短期内不宜作为主要使用方式。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>README 声称 743+ 测试但核心 crate 源码未全部开源，无法独立审计 sandbox/redaction 实现的健壮性。</li><li>Desktop GUI 处于 α1 阶段：icon 占位文件缺失导致 <code class="code-ref">tauri build</code> 失败，发布产物不可用；OTA 更新依赖未签名的 Ed25519 密钥配置。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若 MCP 生态持续扩张，Agent 行为审计和 secret 防泄漏将成为合规刚需；Vigils 的 local-first 定位避免了将敏感 prompt 经第三方中转，对企业安全团队有吸引力，但作为 2 天项目，商业化路径和社区生态建设尚远。</p>
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
  <div class="score-item__value">84</div>
  <div class="score-bar"><span style="width:84%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">87</div>
  <div class="score-bar"><span style="width:87%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.65</span>
  </div>
</div>
</section>