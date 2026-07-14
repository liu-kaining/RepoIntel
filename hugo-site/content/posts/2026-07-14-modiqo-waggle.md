---
title: '[Score: 84.3] modiqo/waggle'
date: '2026-07-14T16:11:26Z'
categories:
- AI Agent Coordination
tags:
- agent-handoffs
- context-references
- MCP
- Rust
- attribution
- event-log
intel_score: 84.3
repo_name: modiqo/waggle
repo_link: https://github.com/modiqo/waggle
summary: ～30字节属性化引用替代多智能体上下文复制，通过解析时变体投射、只记事件和行级遥测减少令牌开销与失败率。
code_source: git
code_files_reviewed:
- xtask/Cargo.toml
- bench/Cargo.toml
- Makefile
- crates/waggle-ops/Cargo.toml
- crates/waggle-agent/Cargo.toml
- crates/waggle/Cargo.toml
- .github/workflows/pages.yml
- .github/workflows/publish-crates.yml
- .github/workflows/ci.yml
- .github/workflows/paper.yml
- crates/waggle-agent/src/lib.rs
- crates/waggle-store-cloudflare/src/lib.rs
- crates/waggle/src/lib.rs
- crates/waggle-social/src/lib.rs
- crates/waggle-store-sqlite/src/lib.rs
- crates/waggle-mcp/src/lib.rs
- edge-worker/src/lib.rs
- crates/waggle-tree/src/lib.rs
- crates/waggle-store/src/lib.rs
- crates/waggle-store-sqlite/build.rs
- crates/waggle-store-sqlite/tests/loom_cache.rs
- crates/waggle-cli/tests/daemon_purge.rs
- crates/waggle-store-fs-jsonl/tests/conformance.rs
- crates/waggle-core/tests/spec_vectors.rs
- crates/waggle-mcp/tests/gap_fixes.rs
- crates/waggle-mcp/tests/envelope_contract.rs
- crates/waggle-mcp/tests/media_e2e.rs
- crates/waggle-cli/tests/daemon_mgmt.rs
- crates/waggle-tmux/src/error.rs
- crates/waggle-mcp/benches/query_paths.rs
- crates/waggle-core/src/entropy.rs
- crates/waggle-store-sqlite/src/cache.rs
- crates/waggle-core/src/time.rs
- crates/waggle-lens-code/benches/extract.rs
- crates/waggle-store/src/error.rs
- crates/waggle-social/src/og.rs
- crates/waggle-store-cloudflare/src/storage.rs
- crates/waggle-store-sqlite/benches/store_paths.rs
- crates/waggle-store-sqlite/src/schema.rs
- crates/waggle-social/src/qr.rs
- crates/waggle-cli/src/health.rs
- crates/waggle-cli/src/identity.rs
- crates/waggle-mcp/src/record.rs
- crates/waggle-social/src/package.rs
- crates/waggle-store/src/types.rs
- crates/waggle-mcp/src/discovery.rs
- crates/waggle-store/src/traits.rs
- crates/waggle-social/src/channels.rs
code_chars_analyzed: 109825
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
      <span class="scope-stat__value">约 109,825 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">xtask/Cargo.toml</code></li><li><code class="path-chip">bench/Cargo.toml</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">crates/waggle-ops/Cargo.toml</code></li><li><code class="path-chip">crates/waggle-agent/Cargo.toml</code></li><li><code class="path-chip">crates/waggle/Cargo.toml</code></li><li><code class="path-chip">.github/workflows/pages.yml</code></li><li><code class="path-chip">.github/workflows/publish-crates.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/paper.yml</code></li><li><code class="path-chip">crates/waggle-agent/src/lib.rs</code></li><li><code class="path-chip">crates/waggle-store-cloudflare/src/lib.rs</code></li><li><code class="path-chip">crates/waggle/src/lib.rs</code></li><li><code class="path-chip">crates/waggle-social/src/lib.rs</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>多智能体编排中每个子代理需重复发送完整工件上下文，造成15倍以上令牌开销且37%失败源于交接信息丢失。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">系统分为钱包核心（<code class="code-ref">crates/waggle-core</code>）、操作目录（<code class="code-ref">crates/waggle-ops</code>）、MCP工具层（<code class="code-ref">crates/waggle-mcp</code>）、可插拔存储（<code class="code-ref">crates/waggle-store</code>契约，SQLite与Cloudflare后端），以及社交渲染、代码透镜、目录树搜索等辅助模块。核心流程为<code class="code-ref">mint</code>创建令牌（含不可变清单、变体、签名），消费者调用<code class="code-ref">resolve</code>根据自身上下文获得适配视图，<code class="code-ref">record</code>/<code class="code-ref">funnel</code>记录无载荷事件，<code class="code-ref">search</code>/<code class="code-ref">read</code>基于内容寻址进行范围限取。存储层通过<code class="code-ref">ReadStore</code>/<code class="code-ref">AppendStore</code>特质分离读写，并强制<code class="code-ref">?Send</code>以兼容Workers；SQLite后端使用WAL+FULL同步模式保障持久性与并发读<code class="code-ref">crates/waggle-store-sqlite/src/schema.rs:14-16</code>。MCP服务器通过<code class="code-ref">Handler</code>泛型化存储和Blob侧车<code class="code-ref">crates/waggle-mcp/src/lib.rs:1-14</code>，工具模式由操作目录驱动以保证MCP表面不漂移。</p>
<p class="audit-callout audit-callout--highlight">写入契约以类型边界强制只读路径无法追加—<code class="code-ref">ReadStore</code>不含<code class="code-ref">append</code>方法，<code class="code-ref">Store</code>的read-only消费者因<code class="code-ref">compile_fail</code>文档测试而编译期验证<code class="code-ref">crates/waggle-store/src/lib.rs:25-29</code>。</p>
<p class="audit-callout audit-callout--highlight">变体选择依据已发布规范向量进行严格测试<code class="code-ref">crates/waggle-core/tests/spec_vectors.rs:1-45</code>，确保密封匹配器在所有索引上稳定，支撑跨实现互操作。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">waggle-agent</code>模块仅为桩<code class="code-ref">crates/waggle-agent/src/lib.rs:1-13</code>，其声明的<code class="code-ref">ResolverContext</code>提取逻辑尚未落地，当前依赖匿名代理上下文，可能影响高级交互间的身份注入。</p>
<p class="audit-callout audit-callout--doubt">性能基准中的熵源使用确定性计数器<code class="code-ref">crates/waggle-mcp/tests/envelope_contract.rs:26-31</code>，虽利于可重复性但无法探测真实随机条件下的行为，不过生产熵源已通过特质注入隔离。</p>
<p>可直接作为MCP服务器嵌入Claude Code等现有编排器进行试点，初期聚焦本地文件交接的<code class="code-ref">mint --snapshot</code>和<code class="code-ref">funnel</code>审计，逐步扩展到跨容器和边缘解析。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅发布6天，生产部署案例空缺，API稳定性待观察。</li><li>重依赖Edge Workers作为分布式组件，可能形成供应商锁定。</li><li>令牌的变体选择和契约仍较早期，复杂多代理交互策略未经大规模验证。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为多智能体生态提供标准化的工件引用和审计原语，可降低编排层的大量上下文复制成本并提高交接可靠性，具备成为Agent-to-Agent协议参考层的潜力。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">90</div>
  <div class="score-bar"><span style="width:90%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">84.3</span>
  </div>
</div>
</section>