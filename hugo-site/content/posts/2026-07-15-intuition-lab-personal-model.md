---
title: '[Score: 83.2] Intuition-Lab/personal-model'
date: '2026-07-15T13:37:40Z'
categories:
- AI Agent Runtime
tags:
- macOS
- MCP
- privacy
- screen-context
- memory
- local-first
intel_score: 83.2
repo_name: Intuition-Lab/personal-model
repo_link: https://github.com/Intuition-Lab/personal-model
summary: Persome 是一个本地优先的 macOS 运行时，通过可访问性 API 捕获屏幕活动构建带证据链的个人记忆模型，并为 MCP 客户端提供个性化上下文。
code_source: git
code_files_reviewed:
- clients/persome-companion/package.json
- pyproject.toml
- .github/workflows/publish-mcp.yml
- .github/workflows/ci.yml
- .github/workflows/release.yml
- src/persome/store/__init__.py
- src/persome/mcp/__init__.py
- src/persome/security/__init__.py
- src/persome/capture/__init__.py
- src/persome/retrieval/__init__.py
- src/persome/__init__.py
- src/persome/writer/__init__.py
- src/persome/trace.py
- src/persome/__main__.py
- src/persome/ocr_setup.py
- src/persome/vectors_tick.py
- src/persome/logger.py
- src/persome/llm_setup.py
- src/persome/env_file.py
- src/persome/launchagent.py
- src/persome/source_import.py
- src/persome/index_health.py
- src/persome/doctor.py
- src/persome/paths.py
- src/persome/providers.py
- src/persome/runtime_pid.py
- src/persome/evidence.py
- src/persome/daemon.py
- src/persome/config.py
- src/persome/updater.py
- connectors/apple-health/Tests/PersomeAppleHealthTests/RelayEnvelopeCodecTests.swift
- clients/persome-companion/Tests/PersomeCompanionCoreTests/SyncEngineTests.swift
- clients/persome-companion/Bridge/test/server.test.js
- clients/persome-companion/Tests/PersomeCompanionCoreTests/PairingTests.swift
- connectors/apple-health/Tests/PersomeAppleHealthTests/RelayCredentialStoreTests.swift
- clients/persome-companion/Tests/PersomeCompanionCoreTests/MobileEventTests.swift
- clients/persome-companion/Bridge/test/store.test.js
- connectors/apple-health/Tests/PersomeAppleHealthTests/HealthEventTests.swift
- src/persome/prompts/timeline_block.user.md
- src/persome/prompts/session_reduce.window.md
- src/persome/prompts/memory_decay.md
- src/persome/prompts/contradiction_check.md
- src/persome/prompts/compact.md
- src/persome/evomem/_json.py
- src/persome/api/onboarding_view.py
- src/persome/writer/cost.py
code_chars_analyzed: 325993
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
      <span class="scope-stat__value">46 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 325,993 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">clients/persome-companion/package.json</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/publish-mcp.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">src/persome/store/__init__.py</code></li><li><code class="path-chip">src/persome/mcp/__init__.py</code></li><li><code class="path-chip">src/persome/security/__init__.py</code></li><li><code class="path-chip">src/persome/capture/__init__.py</code></li><li><code class="path-chip">src/persome/retrieval/__init__.py</code></li><li><code class="path-chip">src/persome/__init__.py</code></li><li><code class="path-chip">src/persome/writer/__init__.py</code></li><li><code class="path-chip">src/persome/trace.py</code></li><li><code class="path-chip">src/persome/__main__.py</code></li><li class="path-more">另有 32 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>AI 编码代理缺乏对用户历史工作模式、优先级和决策风格的了解，导致输出与个人实际需求脱节，无法在长周期开发中积累有效上下文。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">源码层次清晰，src/persome 下划分 capture、store、writer、mcp 等模块。daemon.py 通过 TaskDefinition 注册可插拔的异步任务（如 capture、session、reducer-retry、mcp 等），并利用 asyncio 进行协同调度（<code class="code-ref">src/persome/daemon.py:228</code>）。捕获模块通过 macOS Accessibility API 获取窗口信息和文本，由 timeline 聚合为 1 分钟块，writer 的 S2 缩减器在会话结束时进行压缩和模式检测。存储基于 SQLite FTS5 实现全文搜索和向量队列，证据模块 support 引用追溯。</p>
<p class="audit-callout audit-callout--highlight">安全边界实现细致。env_file.py 中 write_env_values 使用临时文件 + os.fchmod(0600) + Atomic 替换（<code class="code-ref">src/persome/env_file.py:120</code>），确保密钥文件权限严格且无竞态。paths.py 同样强制所有数据目录和文件为 owner-only（0700/0600），并通过 ensure_private_file 防止符号链接和硬链接（<code class="code-ref">src/persome/paths.py:220</code>）。</p>
<p class="audit-callout audit-callout--highlight">配置与提供者解析设计灵活。config.py 使用层次化 dataclass 完全映射 TOML 配置，providers.py 解耦模型端点、凭证发现和协议适配（<code class="code-ref">src/persome/providers.py:1</code>），支持 20+ 种 LLM 后端（包括本地 Ollama、vLLM）的自动探测与回退。</p>
<p class="audit-callout audit-callout--doubt">未审阅到针对模型推理质量（如分类、减少、记忆Delta）的系统性测试。CI 仅执行 pytest -m &quot;not macos and not integration&quot;（<code class="code-ref">.github/workflows/ci.yml:104</code>），主要覆盖离线单元，无法保证核心建模逻辑的正确性。</p>
<p class="audit-callout audit-callout--doubt">OCR 依赖 paddleocr==3.7.0（pyproject.toml:62），仅在 arm64 macOS 上可用，且附加大体积的 PaddlePaddle 运行时，显著增加了安装复杂度和初始资源占用，对 Intel Mac 用户需回退到系统 Vision OCR，体验割裂。</p>
<p>短期可补充一套最小 synthetic 数据集上的模型输出基准测试，确保链路演进不被破坏；长期考虑将 OCR 依赖做成可选插件，降低非 Apple Silicon 用户的入门门槛。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅支持 macOS 13+，用户群体受限，无法覆盖 Linux/Windows 开发者。</li><li>项目仅创建 4 天，Stars 快速增长但缺乏社区贡献历史和长久维护保证。</li><li>LLM 调用费用完全由用户承担，长时间运行可能产生显著成本。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>为 AI 编码代理和助手提供持久的用户专属记忆，构建个人工作的“数字图层”，在 MCP 生态中具备差异化潜力，但依赖上游客户端采纳。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">83.2</span>
  </div>
</div>
</section>