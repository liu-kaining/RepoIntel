---
title: '[Score: 75.15] XYZ-AI-Lab/AxisAgentic'
date: '2026-07-26T08:33:17Z'
categories:
- AI Agent Framework
tags:
- trajectory-collection
- sft-export
- multi-turn-agents
- long-horizon-tasks
- python
- openai-tools
intel_score: 75.15
repo_name: XYZ-AI-Lab/AxisAgentic
repo_link: https://github.com/XYZ-AI-Lab/AxisAgentic
summary: 面向长期智能体的可扩展运行时与轨迹收集框架，输出忠实于状态的交互记录，供模型训练与评测复现。
code_source: git
code_files_reviewed:
- setup.py
- pyproject.toml
- .github/workflows/ci.yml
- recipe/wide_search/__init__.py
- recipe/wide_search/agent/__init__.py
- recipe/wide_search/eval/__init__.py
- recipe/wide_search/runners/__init__.py
- recipe/__init__.py
- recipe/web_search/__init__.py
- recipe/dashboard/__init__.py
- recipe/web_search/runners/__init__.py
- recipe/web_search/agent/__init__.py
- tests/conftest.py
- recipe/common/log_processing/append_run_log.py
- .pre-commit-config.yaml
- .github/ISSUE_TEMPLATE/config.yml
- .github/PULL_REQUEST_TEMPLATE.md
- recipe/dashboard/tool_call_tab.py
- recipe/common/README.md
- agentic/config/io.py
- recipe/dashboard/constants.py
- .github/ISSUE_TEMPLATE/feature_request.yml
- recipe/dashboard/live_results.py
- recipe/dashboard/metrics.py
- SECURITY.md
- agentic/config/runtime_template.yaml
- CHANGELOG.md
- recipe/README.md
- docs/README.zh-CN.md
- agentic/orchestration/orchestrator_tool.py
- recipe/wide_search/eval/primary_key_preprocess.py
- setup_env.sh
- docs/README.md
- recipe/dashboard/README.md
- recipe/common/log_processing/trace_refs.py
- .github/ISSUE_TEMPLATE/bug_report.yml
- recipe/wide_search/eval/preprocess.py
- agentic/model_clients/gpu_utils.py
- agentic/datasets/base.py
- agentic/evaluation/verifier.py
- recipe/wide_search/agent/runtime.py
- tests/test_web_search_prompt_date.py
- agentic/rl/facade.py
- agentic/tools/web_search/_utils.py
- agentic/model_assets/chat_template_compat.py
- recipe/common/io_timing.py
- recipe/wide_search/eval/llm_judge_column.py
- agentic/model_clients/errors.py
code_chars_analyzed: 57084
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
      <span class="scope-stat__value">约 57,084 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">setup.py</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">recipe/wide_search/__init__.py</code></li><li><code class="path-chip">recipe/wide_search/agent/__init__.py</code></li><li><code class="path-chip">recipe/wide_search/eval/__init__.py</code></li><li><code class="path-chip">recipe/wide_search/runners/__init__.py</code></li><li><code class="path-chip">recipe/__init__.py</code></li><li><code class="path-chip">recipe/web_search/__init__.py</code></li><li><code class="path-chip">recipe/dashboard/__init__.py</code></li><li><code class="path-chip">recipe/web_search/runners/__init__.py</code></li><li><code class="path-chip">recipe/web_search/agent/__init__.py</code></li><li><code class="path-chip">tests/conftest.py</code></li><li><code class="path-chip">recipe/common/log_processing/append_run_log.py</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>多步推理中，上下文膨胀、回滚与恢复复杂，且常用轨迹记录丢失隐藏状态，导致 SFT 数据无法反映模型真实所见。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">基于 agentic 核心包，通过 Orchestrator 驱动工具调用与模型交互；recipe 实现具体任务（web_search、wide_search）。<code class="code-ref">agentic/rl/facade.py</code> 暴露 RL 接口，支持策略执行（RLPolicyFacade.act）和环境步进（RLEnvironmentFacade.step），与 OrchestratorTool (<code class="code-ref">agentic/orchestration/orchestrator_tool.py</code>) 结合实现递归子任务编排。配置通过 <code class="code-ref">agentic/config/io.py</code> 的 YAML 加载，轨迹输出与仪表板由 recipe/common 支持。</p>
<p class="audit-callout audit-callout--highlight">递归编排与工具代理。<code class="code-ref">agentic/orchestration/orchestrator_tool.py</code> 的 OrchestratorTool 将整个编排器包装为可调用工具，使模型能在运行中触发子任务，实现层次化规划。</p>
<p class="audit-callout audit-callout--highlight">运行时期重写与容错。<code class="code-ref">recipe/wide_search/agent/runtime.py</code> 的 WideSearchConversationRuntime._extract_direct_final_answer 识别 Markdown 表格并提前结束对话，避免无效轮次，体现 Recipe 对运行时的灵活定制。</p>
<p class="audit-callout audit-callout--doubt">核心运行时代码缺失。未审阅到 <code class="code-ref">agentic/orchestration/task_orchestrator.py</code> 等关键文件，无法评估追加式轨迹（append‑only trace）的实际实现，工程可靠性存疑。</p>
<p class="audit-callout audit-callout--doubt">测试覆盖严重不足。仅见 <code class="code-ref">tests/test_web_search_prompt_date.py</code> 一个测试文件且为 prompts 单元测试，缺少集成与轨迹一致性测试；CI 仅运行 lint 与 pytest，质量门槛低。</p>
<p>立刻补充核心运行时单元测试与轨迹序列化测试；增加 CI 中端到端搜索任务回归，确保轨迹可重放；文档中明确声明当前 API 稳定性保证期限。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>基准结果声明非受控比较，实际性能因工具与裁判不同难以复现。</li><li>发布仅3天，commit极少，API 可能频繁变动，生产集成风险高。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>若持续集成 Hugging Face 数据集与训练管线，可成为智能体训练数据飞轮的关键中间件，但目前仍需大量工程投入。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">75.15</span>
  </div>
</div>
</section>