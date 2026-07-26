---
title: '[Score: 75.75] OpenBMB/StaffDeck'
date: '2026-07-26T02:30:49Z'
categories:
- Enterprise AI Agent Platform
tags:
- digital-employee
- state-machine-sop
- knowledge-retrieval
- fastapi
- react
intel_score: 75.75
repo_name: OpenBMB/StaffDeck
repo_link: https://github.com/OpenBMB/StaffDeck
summary: 将个人工作流与领域知识沉淀为可复用数字员工的平台，集成状态机SOP、文档结构感知检索与多渠道交互。
code_source: git
code_files_reviewed:
- frontend-enterprise/package.json
- backend/pyproject.toml
- .github/workflows/codeql.yml
- .github/workflows/release.yml
- backend/app/api/__init__.py
- backend/app/security/__init__.py
- backend/app/session/__init__.py
- backend/app/__init__.py
- backend/app/core/__init__.py
- backend/app/memory/__init__.py
- backend/app/observability/__init__.py
- backend/app/tools/__init__.py
- backend/app/knowledge/__init__.py
- backend/tests/test_paths.py
- backend/tests/test_resource_paths.py
- backend/tests/test_timezone_data.py
- backend/tests/test_runner_bash_guard.py
- backend/tests/test_channel_crypto.py
- backend/tests/test_mock_auth.py
- backend/tests/test_skill_stream_job_permissions.py
- backend/tests/test_runner_stream_windows.py
- frontend-enterprise/src/vite-env.d.ts
- package-lock.json
- frontend-enterprise/src/lib/utils.ts
- backend/app/llm/prompts/step_agent_awaiting_input_rules.md
- backend/app/llm/prompts/step_agent_knowledge_rules.md
- frontend-enterprise/src/components/ui/skeleton.tsx
- backend/app/llm/prompts/step_agent_repair_rules.md
- backend/app/llm/prompts/step_agent_tool_rules.md
- frontend-enterprise/src/main.tsx
- backend/app/skills/llm_limits.py
- backend/app/security/tenant.py
- backend/app/llm/prompts/step_agent_tool_continuation_rules.md
- frontend-enterprise/README.md
- backend/app/channels/service_durable_inbox.py
- frontend-enterprise/components.json
- scripts/dev_up.sh
- scripts/dev_down.sh
- scripts/dev_status.sh
- backend/app/llm/prompts/knowledge_document_route_prompt.md
- frontend-enterprise/src/hooks/use-mobile.ts
- frontend-enterprise/src/components/ui/label.tsx
- frontend-enterprise/tsconfig.json
- backend/app/llm/prompts/step_agent_general_skill_rules.md
- frontend-enterprise/src/enums/routes.ts
- backend/mock_servers/README.md
- backend/app/llm/prompts/knowledge_search_prompt.md
- frontend-enterprise/src/components/ui/separator.tsx
code_chars_analyzed: 31272
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
      <span class="scope-stat__value">约 31,272 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">frontend-enterprise/package.json</code></li><li><code class="path-chip">backend/pyproject.toml</code></li><li><code class="path-chip">.github/workflows/codeql.yml</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">backend/app/api/__init__.py</code></li><li><code class="path-chip">backend/app/security/__init__.py</code></li><li><code class="path-chip">backend/app/session/__init__.py</code></li><li><code class="path-chip">backend/app/__init__.py</code></li><li><code class="path-chip">backend/app/core/__init__.py</code></li><li><code class="path-chip">backend/app/memory/__init__.py</code></li><li><code class="path-chip">backend/app/observability/__init__.py</code></li><li><code class="path-chip">backend/app/tools/__init__.py</code></li><li><code class="path-chip">backend/app/knowledge/__init__.py</code></li><li><code class="path-chip">backend/tests/test_paths.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>企业内大量重复性任务（如工单处理、政策查询）依赖人工记忆与操作，个人经验难留存为组织资产，员工离职即流失。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">后端基于FastAPI分层设计，core/agent_loop（<code class="code-ref">见backend/app/core/__init__.py:1</code>）为核心调度器，memory、knowledge、tools等模块通过Service层暴露能力。前端为Vite+React单页应用，路由划分企业级管理路径（<code class="code-ref">frontend-enterprise/src/enums/routes.ts:1</code>）。</p>
<p class="audit-callout audit-callout--highlight">精细的多步Agent规则体系，通过独立的prompt文件（<code class="code-ref">如backend/app/llm/prompts/step_agent_tool_rules.md:1</code>）定义了工具调用、知识检索、修复等场景的约束，避免LLM幻觉。</p>
<p class="audit-callout audit-callout--highlight">工程交付成熟度高，<code class="code-ref">.github/workflows/release.yml:1</code>实现了macOS/Windows/Linux多平台PyInstaller打包、代码签名及Windows端烟测试，CI流程完备。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">未审阅到core/agent_loop.py</code>等核心实现文件，无法评估状态机执行、多轮对话管理的实际质量，仅凭__init__.py导出难以判断完整性。</p>
<p class="audit-callout audit-callout--doubt">知识检索模块仅见prompt文件（<code class="code-ref">backend/app/llm/prompts/knowledge_search_prompt.md:1</code>），未提供KnowledgeService的向量索引或检索逻辑源码，文档结构感知能力存疑。</p>
<p>优先在内部快速部署测试知识检索与SOP执行链路，关注长上下文窗口下的token消耗；桌面端跨平台构建已就绪，可立即分发试用。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>项目仅创建12天，API与功能可能快速迭代，早期采用者需面对向后不兼容风险。</li><li>依赖OpenAI兼容模型服务，企业数据安全与合规需自行审查，知识库可能泄露敏感信息。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>瞄准企业“数字员工”赛道，通过组织级知识沉淀与流程自动化，降低人力成本，可与飞书/企微等办公平台集成，有较大变现空间。</p>
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
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.75</span>
  </div>
</div>
</section>