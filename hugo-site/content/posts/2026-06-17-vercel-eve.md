---
title: '[Score: 76.0] vercel/eve'
date: '2026-06-17T15:20:57Z'
categories:
- AI Agent Framework
tags:
- TypeScript
- Agent Framework
- Vercel
- Durable Workflows
- Sandbox
- CLI
intel_score: 76.0
repo_name: vercel/eve
repo_link: https://github.com/vercel/eve
summary: Vercel 出品的文件系统优先 AI Agent 框架，将指令、工具、技能等以约定目录结构组织，面向需要快速搭建并部署到 Vercel 的 TypeScript
  开发者。
code_source: git
code_files_reviewed:
- apps/fixtures/weather-agent/package.json
- e2e/fixtures/agent-subagents-hitl/package.json
- apps/frameworks/nuxt/package.json
- apps/fixtures/agent-tui-client/package.json
- e2e/fixtures/agent-tools/package.json
- e2e/fixtures/agent-skills/package.json
- .github/workflows/release.yml
- .github/workflows/e2e-local.yml
- .github/workflows/e2e-vercel.yml
- .github/workflows/ci.yml
- packages/eve/src/index.ts
- packages/eve/src/public/nuxt/index.ts
- packages/eve/src/evals/loaders/index.ts
- packages/eve/src/public/tools/approval/index.ts
- packages/eve/src/public/schedules/index.ts
- packages/eve/src/evals/reporters/index.ts
- packages/eve/src/internal/workflow/index.ts
- packages/eve/src/public/instructions/index.ts
- packages/eve/src/public/hooks/index.ts
- packages/eve-catalog/CHANGELOG.md
- apps/docs/CHANGELOG.md
- packages/eve/turbo.json
- packages/eve/tsconfig.tui.json
- packages/eve-catalog/tsconfig.build.json
- packages/eve-catalog/vitest.config.ts
- packages/eve/tsconfig.dev.json
- apps/docs/turbo.json
- apps/docs/vercel.json
- apps/docs/next-env.d.ts
- apps/templates/README.md
- packages/eve-catalog/tsconfig.json
- packages/eve/tsconfig.build.json
- apps/frameworks/README.md
- apps/docs/components.json
- apps/fixtures/README.md
- packages/eve/tsconfig.json
- apps/docs/proxy.ts
- packages/eve/vitest.dev-server.config.ts
- apps/docs/tsconfig.json
- packages/eve/vitest.vercel.config.ts
- packages/eve/vitest.scenario.config.ts
- packages/eve/vitest.unit.config.ts
- packages/eve/vitest.integration.config.ts
- apps/docs/next.config.ts
- packages/eve/CHANGELOG.md
- apps/docs/source.config.ts
- apps/docs/geistdocs.tsx
- packages/eve/README.md
code_chars_analyzed: 48567
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
      <span class="scope-stat__value">约 48,567 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">apps/fixtures/weather-agent/package.json</code></li><li><code class="path-chip">e2e/fixtures/agent-subagents-hitl/package.json</code></li><li><code class="path-chip">apps/frameworks/nuxt/package.json</code></li><li><code class="path-chip">apps/fixtures/agent-tui-client/package.json</code></li><li><code class="path-chip">e2e/fixtures/agent-tools/package.json</code></li><li><code class="path-chip">e2e/fixtures/agent-skills/package.json</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">.github/workflows/e2e-local.yml</code></li><li><code class="path-chip">.github/workflows/e2e-vercel.yml</code></li><li><code class="path-chip">.github/workflows/ci.yml</code></li><li><code class="path-chip">packages/eve/src/index.ts</code></li><li><code class="path-chip">packages/eve/src/public/nuxt/index.ts</code></li><li><code class="path-chip">packages/eve/src/evals/loaders/index.ts</code></li><li><code class="path-chip">packages/eve/src/public/tools/approval/index.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>构建 AI Agent 时，开发者常把系统提示、工具定义、调度逻辑散落在代码各处，改一处要翻多个文件；部署到生产环境还需自建状态持久化、沙箱隔离和审批流水线，迭代成本高。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">eve 将 Agent 划分为 channel（入站规范化）、harness（单轮 AI 推理）、runtime（状态持久化与流式事件）三层，以 <code class="code-ref">.eve/</code> 编译产物为边界。<code class="code-ref">packages/eve/src/index.ts</code> 仅做 re-export，实际逻辑分散在 <code class="code-ref">src/public/</code> 下按约定目录组织的子模块中。运行时基于 Nitro + Vercel Workflows，通过 <code class="code-ref">continuationToken</code> 与 <code class="code-ref">sessionId</code> 两个标识将通道与运行时解耦。</p>
<p class="audit-callout audit-callout--highlight">四层测试分层设计清晰。<code class="code-ref">vitest.unit.config.ts</code> 通过 <code class="code-ref">src/internal/testing/unit-guard.ts</code> 阻止单元测试触碰真实文件系统和网络，<code class="code-ref">vitest.integration.config.ts</code> 引入 workflow vitest 插件在内存中跑集成，<code class="code-ref">vitest.scenario.config.ts</code> 隔离子进程级场景测试，<code class="code-ref">vitest.vercel.config.ts</code> 将部署测试与凭证绑定且关闭并发，分层粒度在开源 Agent 框架中少见。</p>
<p class="audit-callout audit-callout--highlight">CI 配置对 changeset 发布流程有防御性处理。<code class="code-ref">.github/workflows/release.yml:36</code> 在发布前显式清理 <code class="code-ref">.git/objects/pack/.tmp-*</code> 临时包文件，并在注释中详细解释 isomorphic-git 的 packfile 解析失败路径，说明团队踩过坑并记录了根因。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">packages/eve/src/internal/workflow/index.ts:6</code> 的 <code class="code-ref">fetch</code> wrapper 标注了 <code class="code-ref">&quot;use step&quot;</code> 字符串指令，但 code_bundle 中未提供 workflow 编译器源码，无法验证该指令是否被编译器正确识别和转换为持久化步骤点，也无从评估其对 fetch 错误的重试/超时语义。未审阅到 workflow 编译器实现，本次结论不覆盖。</p>
<p class="audit-callout audit-callout--doubt">48 个源码文件中绝大部分是 manifest、CI、配置和入口 re-export，核心运行时（harness 推理循环、sandbox 管理、state 持久化、channel 路由）的实现文件均未包含在 code_bundle 中，无法评估关键链路的错误传播、并发模型和资源清理逻辑。工程分因可观测性不足而保守打分。</p>
<p>若要在生产中使用 eve，应重点审计以下未审阅区域：（1）sandbox 模板失败后的自动重建路径是否存在竞态；（2）HITL 审批 gate 超时后 session 状态是否正确清理；（3）<code class="code-ref">continuationToken</code> 的生成与校验是否存在枚举或重放风险。建议在本地用 <code class="code-ref">eve eval --strict</code> 跑完 e2e fixtures 后再做部署决策。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心运行时源码未包含在本次审阅包中，harness/sandbox/state 持久化链路的安全性无法独立验证。</li><li>README 明确声明处于 beta 阶段，API 与行为可能在 GA 前发生破坏性变更，生产依赖需谨慎。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为 Vercel 官方 Agent 框架，eve 直接绑定 Vercel 部署与 Workflows 基础设施，为 Vercel 带来 Agent 工作负载的平台锁定，同时降低了 TypeScript 开发者进入 Agent 赛道的门槛。</p>
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
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.0</span>
  </div>
</div>
</section>