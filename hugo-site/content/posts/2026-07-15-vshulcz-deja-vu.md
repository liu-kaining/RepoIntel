---
title: '[Score: 78.3] vshulcz/deja-vu'
date: '2026-07-15T21:57:16Z'
categories:
- AI Agent Memory
tags:
- agent-memory
- cli
- search
- indexing
- mcp
- go
intel_score: 78.3
repo_name: vshulcz/deja-vu
repo_link: https://github.com/vshulcz/deja-vu
summary: deja-vu 为编码代理提供本地持久记忆：搜索、MCP 召回、自动上下文，一零依赖二进制跨 Claude Code/Codex/opencode
  索引会话日志。
code_source: git
code_files_reviewed:
- go.mod
- Makefile
- npm/package.json
- .github/workflows/codeql.yml
- .github/workflows/lint.yml
- .github/workflows/scorecard.yml
- .github/workflows/release.yml
- cmd/deja/main.go
- internal/index/lock_unix.go
- internal/model/model.go
- internal/sources/name_test.go
- cmd/deja/sync.go
- internal/index/lock_windows.go
- internal/index/heal_test.go
- cmd/deja/hook_context.go
- internal/redact/redact_test.go
- internal/sources/codex.go
- internal/index/ord_churn_test.go
- internal/sources/util.go
- internal/redact/redact.go
- cmd/deja/sync_ssh.go
- cmd/deja/sync_ssh_test.go
- internal/sources/claude.go
- internal/sources/opencode.go
- cmd/deja/share.go
- internal/index/sync_persist_test.go
- cmd/deja/mcp.go
- internal/search/search_test.go
- internal/index/sync.go
- cmd/deja/stats.go
- internal/sources/sources_test.go
- cmd/deja/install.go
- internal/search/search.go
- cmd/deja/main_test.go
- internal/index/index_test.go
- internal/index/index.go
- .github/PULL_REQUEST_TEMPLATE.md
- .github/dependabot.yml
- .github/ISSUE_TEMPLATE/feature_request.md
- npm/README.md
- .github/ISSUE_TEMPLATE/bug_report.md
- .golangci.yml
- CONTRIBUTING.md
- fixtures/synthetic/make_opencode_db.sh
- .goreleaser.yaml
- install.sh
- scripts/e2e.sh
- CHANGELOG.md
code_chars_analyzed: 234743
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
      <span class="scope-stat__value">约 234,743 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">npm/package.json</code></li><li><code class="path-chip">.github/workflows/codeql.yml</code></li><li><code class="path-chip">.github/workflows/lint.yml</code></li><li><code class="path-chip">.github/workflows/scorecard.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">cmd/deja/main.go</code></li><li><code class="path-chip">internal/index/lock_unix.go</code></li><li><code class="path-chip">internal/model/model.go</code></li><li><code class="path-chip">internal/sources/name_test.go</code></li><li><code class="path-chip">cmd/deja/sync.go</code></li><li><code class="path-chip">internal/index/lock_windows.go</code></li><li><code class="path-chip">internal/index/heal_test.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>编码代理在多次会话中重复调试相同问题，以往的历史日志闲置在本地无法检索，deja 将其转为可搜索、可回忆的记忆层。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口 <code class="code-ref">cmd/deja/main.go</code> 解析子命令，路由到索引构建 (internal/index)、搜索 (internal/search) 等功能。main.go 中 <code class="code-ref">loadAll</code> 函数聚合三个代理源，<code class="code-ref">index.Ensure</code> 检查/创建倒排索引桶 (<code class="code-ref">buckets/*.bin</code>) 和记录文件 (<code class="code-ref">records.bin</code>)。搜索时 <code class="code-ref">index.Search</code> 通过 <code class="code-ref">intersectPostings</code> 或 <code class="code-ref">intersectSubstringPostings</code> 获取候选偏移，<code class="code-ref">scanRecords</code> 组装结果，支持正则和分词匹配。增量更新由 <code class="code-ref">updateIndex</code> 处理，仅重索引变动的文件。</p>
<p class="audit-callout audit-callout--highlight">增量索引逻辑精细，<code class="code-ref">internal/index/index.go</code> 的 <code class="code-ref">canAppendIncremental</code> 判断文件仅尾部追加时，调用 <code class="code-ref">appendIncremental</code> 直接追加新记录到 <code class="code-ref">records.bin</code> 并更新桶，避免全量重建（<code class="code-ref">index_test.go:TestIncrementalOnlyReingestsChangedFile</code> 验证仅变动的文件被重新摄入）。</p>
<p class="audit-callout audit-callout--highlight">摄入时秘密信息编辑，<code class="code-ref">internal/redact/redact.go</code> 用正则匹配 AWS 密钥、JWT、GitHub Token 等，在 <code class="code-ref">redactForIngest</code> 中过滤，使可搜索文本不含明文秘密（<code class="code-ref">index_test.go:TestRedactsSecretsAtIngest</code> 确认搜索不到密钥）。</p>
<p class="audit-callout audit-callout--doubt">索引格式依赖 gob 编码（manifest.gob, sessions.gob），虽然 current version=9 但未见版本迁移代码，未来 schema 变更可能导致索引不可读。</p>
<p class="audit-callout audit-callout--doubt">opencode 源通过 <code class="code-ref">exec.Command(&quot;sqlite3&quot;, ...)</code> 查询，依赖系统 sqlite3 CLI（见 <code class="code-ref">internal/sources/opencode.go</code>），若缺失则静默忽略，缺失诊断在 <code class="code-ref">sources 子命令</code> 中有提示但无自动安装。</p>
<p>适合同时使用 Claude Code、Codex 或 opencode 的开发者，通过 brew/install.sh 部署，配合 <code class="code-ref">deja install --auto</code> 启用自动回忆，注意定期 <code class="code-ref">deja warmup</code> 保持索引最新。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持三种代理，新增代理需手动扩展 sources 解析。</li><li>索引无自动清理，长期使用可能膨胀，需手动 <code class="code-ref">--rebuild</code>。</li><li>单维护者，社区贡献度待验证。</li><li>同步传输无加密/签名，依赖系统 ssh/scp，敏感元数据可能泄漏。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>在代理工作流中作为记忆中间件，可能成为 IDE/终端代理生态的标配组件，但暂无直接商业化路径。</p>
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
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.3</span>
  </div>
</div>
</section>