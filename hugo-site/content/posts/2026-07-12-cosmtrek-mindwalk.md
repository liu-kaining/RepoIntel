---
title: '[Score: 82.45] cosmtrek/mindwalk'
date: '2026-07-12T19:01:05Z'
categories:
- AI Agent Debugging
tags:
- coding-agent
- visualization
- claude-code
- codex
- go
- three.js
intel_score: 82.45
repo_name: cosmtrek/mindwalk
repo_link: https://github.com/cosmtrek/mindwalk
summary: 一个本地优先的 3D 可视化工具，将 Claude Code/Codex 会话回放为代码库的发光地图，帮助开发者审查智能体的足迹与决策路径。
code_source: git
code_files_reviewed:
- go.mod
- Makefile
- web/package.json
- .github/workflows/release.yml
- cmd/mindwalk/main.go
- cmd/mindwalk/main_test.go
- internal/model/stats.go
- internal/model/stats_test.go
- internal/citymap/builder_test.go
- internal/model/model.go
- internal/adapter/adapter_test.go
- internal/citymap/builder.go
- internal/server/server.go
- internal/server/server_test.go
- internal/adapter/adapter.go
- internal/adapter/claudecode/adapter_test.go
- internal/adapter/claudecode/adapter.go
- internal/adapter/codex/adapter.go
- internal/adapter/codex/adapter_test.go
- CLAUDE.md
- .claude/launch.json
- web/src/ui/shortcuts.ts
- web/src/main.tsx
- web/tsconfig.json
- .goreleaser.yaml
- web/vite.config.ts
- web/src/state/filters.ts
- web/src/api/client.ts
- web/src/ui/LogoMark.tsx
- scripts/install.sh
- .claude/skills/verify/SKILL.md
- AGENTS.md
- web/src/scene/textures.ts
- schema/citymap.schema.json
- .impeccable.md
- web/src/state/store.ts
- web/src/ui/Inspector.tsx
- web/src/scene/trail.ts
- web/src/types.ts
- web/src/playback/reducer.ts
- README.md
- web/src/scene/dirLabels.ts
- web/src/scene/treeLayout.ts
- web/src/playback/recorder.ts
- web/src/scene/sceneUtils.ts
- schema/trace.schema.json
- web/src/ui/SessionRail.tsx
- web/src/ui/Timeline.tsx
code_chars_analyzed: 255771
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
      <span class="scope-stat__value">约 255,771 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">go.mod</code></li><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">web/package.json</code></li><li><code class="path-chip">.github/workflows/release.yml</code></li><li><code class="path-chip">cmd/mindwalk/main.go</code></li><li><code class="path-chip">cmd/mindwalk/main_test.go</code></li><li><code class="path-chip">internal/model/stats.go</code></li><li><code class="path-chip">internal/model/stats_test.go</code></li><li><code class="path-chip">internal/citymap/builder_test.go</code></li><li><code class="path-chip">internal/model/model.go</code></li><li><code class="path-chip">internal/adapter/adapter_test.go</code></li><li><code class="path-chip">internal/citymap/builder.go</code></li><li><code class="path-chip">internal/server/server.go</code></li><li><code class="path-chip">internal/server/server_test.go</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>使用编码智能体的工程师只能查看原始 JSONL 日志，却无法直观理解智能体如何‘理解’仓库、在哪里探索、操作是否合理，导致会话审查耗时且不完整。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目清晰分层：适配器（<code class="code-ref">internal/adapter/adapter.go</code> 定义 Source 接口）将 Claude 和 Codex 日志归一化为 Trace；citymap 构建器（<code class="code-ref">internal/citymap/builder.go</code>）生成确定性布局；服务端（<code class="code-ref">internal/server/server.go</code>）聚合数据并缓存；前端 Three.js/React 渲染 3D 场景与回放控制。</p>
<p class="audit-callout audit-callout--highlight">确定性仓库地图：<code class="code-ref">internal/citymap/builder.go</code> 使用 git ls-files 获取文件列表，按路径排序后分配 ID，并用 squarified treemap 算法布局，权重为 sqrt(max(lines, bytes/4096, 16))，且内边距与纵横比限制确保可视性。builder_test.go 中的 TestBuildIsDeterministic 多次构建结果一致，TestSquarifiedLayoutAvoidsExtremeAspectRatios 验证避免极端比例。</p>
<p class="audit-callout audit-callout--highlight">命令语义分类：adapter.BuildEvent（<code class="code-ref">internal/adapter/adapter.go</code>）能将 Bash/exec_command 等工具调用精确归类为 search/read/verify/exec，通过解析命令字符串和已知模式（如 searchCommand、readCommand），并标记 inferred（weak）目标。adapter_test.go 中大量用例验证了对 sed、grep、Promise.all 等复杂模式的处理，确保事件归类准确。</p>
<p class="audit-callout audit-callout--doubt">未审阅到前端自动化测试代码。<code class="code-ref">web/package.js</code>on 中虽有 Playwright 依赖，但源码中未提供任何前端测试文件（如 *.spec.ts），仅有一份操作技能文档（<code class="code-ref">.claude/skills/verify/SKILL.md</code>），这会增加视觉与交互回归风险。</p>
<p class="audit-callout audit-callout--doubt">Citymap 构建器的非 Git 回退路径（filepath.WalkDir）未被测试覆盖。builder.go 中 listFiles 在 git ls-files 失败时采用 WalkDir，并硬编码排除 node_modules 等目录，但 builder_test.go 中所有测试均基于 git 仓库，未验证无 git 环境的行为，可能隐藏边界问题。</p>
<p>该工具已可自用或小团队试运行；若想扩大受众，应补充前端自动化测试套件，并增加对更多智能体格式（如 Aider、Cursa）的适配器，同时加入沙箱保护以抵御恶意会话日志。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>单开发者维护，仓库仅 3 天历史，长期可持续性存疑</li><li>前端缺少自动化测试，3D 场景更新易引入视觉回归</li><li>Codex 会话的错误观测性为推断值，误差率数据可能误导</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>精准切入 AI 编码辅助工具的审计需求，随着编码智能体普及，有望成为开发者日常审查工具，具备社区插件化扩展潜力。</p>
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
  <div class="score-item__value">83</div>
  <div class="score-bar"><span style="width:83%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">87</div>
  <div class="score-bar"><span style="width:87%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">82.45</span>
  </div>
</div>
</section>