---
title: '[Score: 78.55] gajus/zod-compiler'
date: '2026-06-12T14:53:04Z'
categories:
- Build-time Schema Compiler
tags:
- zod
- validation
- build-time-compilation
- unplugin
- typescript
- codegen
intel_score: 78.55
repo_name: gajus/zod-compiler
repo_link: https://github.com/gajus/zod-compiler
summary: 将 Zod schema 在构建期编译为零开销验证函数的 unplugin 工具，适用于已有大量 Zod 验证、关注运行时性能的 TypeScript
  全栈项目。
code_source: git
code_files_reviewed:
- apps/rspack/package.json
- benchmarks/package.json
- apps/hono/package.json
- apps/viteplus/package.json
- apps/nextjs/package.json
- apps/trpc/package.json
- .github/workflows/feature.yaml
- .github/workflows/main.yaml
- benchmarks/fixtures/schemas/effects/index.ts
- benchmarks/fixtures/schemas/real-world/index.ts
- benchmarks/fixtures/schemas/collections/index.ts
- benchmarks/fixtures/schemas/objects/index.ts
- benchmarks/fixtures/schemas/primitives/index.ts
- benchmarks/fixtures/schemas/recursive/index.ts
- benchmarks/fixtures/schemas/unions/index.ts
- benchmarks/fixtures/schemas/index.ts
- src/index.ts
- src/discovery.ts
- src/loader.ts
- src/static-filter.ts
- src/unplugin/bun.ts
- src/unplugin/farm.ts
- src/unplugin/vite.ts
- src/unplugin/rollup.ts
- src/unplugin/rspack.ts
- src/unplugin/esbuild.ts
- src/unplugin/webpack.ts
- src/unplugin/rolldown.ts
- src/cli/errors.ts
- apps/hono/vitest.config.ts
- apps/viteplus/tsconfig.json
- apps/trpc/tsconfig.json
- apps/rspack/tsconfig.json
- apps/hono/tsconfig.json
- apps/trpc/vitest.config.ts
- apps/hono/build.ts
- apps/nextjs/next-env.d.ts
- apps/nextjs/next.config.ts
- apps/trpc/tsdown.config.ts
- apps/viteplus/vite.config.ts
- apps/nextjs/tsconfig.json
- src/cli/logger.ts
- src/unplugin/edits.ts
- src/core/compile.ts
- src/cli/emitter.ts
- src/unplugin/virtual.ts
- src/core/pipeline.ts
- src/unplugin/hoist-compile.ts
code_chars_analyzed: 60311
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
      <span class="scope-stat__value">约 60,311 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">apps/rspack/package.json</code></li><li><code class="path-chip">benchmarks/package.json</code></li><li><code class="path-chip">apps/hono/package.json</code></li><li><code class="path-chip">apps/viteplus/package.json</code></li><li><code class="path-chip">apps/nextjs/package.json</code></li><li><code class="path-chip">apps/trpc/package.json</code></li><li><code class="path-chip">.github/workflows/feature.yaml</code></li><li><code class="path-chip">.github/workflows/main.yaml</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/effects/index.ts</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/real-world/index.ts</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/collections/index.ts</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/objects/index.ts</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/primitives/index.ts</code></li><li><code class="path-chip">benchmarks/fixtures/schemas/recursive/index.ts</code></li><li class="path-more">另有 34 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>使用 Zod 的大型项目中，每次请求都经历 schema 运行时解析与验证，对象分配和递归遍历在热路径上造成可测量延迟；typia 等替代方案需要迁移全量代码。zod-compiler 让开发者保留现有 Zod schema 不动，仅通过构建插件获得 2-75 倍验证加速。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整个编译流水线分为「发现 → 提取 IR → 代码生成 → 文本替换」四段。发现阶段由 <code class="code-ref">src/discovery.ts</code> 执行用户源文件并扫描导出，通过 <code class="code-ref">_zod.def</code> 鸭子类型识别 Zod schema（<code class="code-ref">src/discovery.ts:18</code> 的 <code class="code-ref">isZodSchema</code>）。<code class="code-ref">src/static-filter.ts</code> 的 <code class="code-ref">mayExportSchemas</code> 用 acorn 解析 jiti 转译后的 CJS，对每个顶层导出做保守分类（函数/类/字面量 → safe，其余 → candidate），避免对纯组件/工具文件做无意义执行。核心编译由 <code class="code-ref">src/core/pipeline.ts:36</code> 的 <code class="code-ref">compileSchemas</code> 驱动，两遍处理：第一遍 <code class="code-ref">extractSchema</code> 生成 IR，第二遍 <code class="code-ref">generateValidator</code> 产出优化代码；跨 schema 的结构重复通过 <code class="code-ref">createSharedSchemaPlan</code> 做文件级去重。unplugin 入口见 <code class="code-ref">src/unplugin/vite.ts</code> 等单行 re-export，实际逻辑应在未提供的 <code class="code-ref">src/unplugin/index.ts</code> 中。构建产物通过虚拟模块 <code class="code-ref">virtual:zod-compiler/runtime</code>（<code class="code-ref">src/unplugin/virtual.ts</code>）注入共享 helper，bundler tree-shake 未使用的导出。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/static-filter.ts</code> 的整套保守静态分类器设计精巧——用 acorn walk 分析转译后 CJS 的绑定链与导出目标，能将 <code class="code-ref">export function Foo() {}</code> 等纯函数文件在不执行任何依赖的情况下排除，显著减少构建时需要加载的文件数量。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/loader.ts</code> 的运行时适配与缓存策略——Node 走共享 jiti 实例（按 tsconfig alias 缓存，<code class="code-ref">src/loader.ts:52</code> 的 <code class="code-ref">jitiInstances</code>），Bun/Deno 走原生 import；HMR 时 <code class="code-ref">invalidateModuleCache</code> 精准清除一方代码缓存而保留 node_modules 热缓存（<code class="code-ref">src/loader.ts:82</code>），避免每次文件变更都重新执行 zod 本身。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">src/core/extract/</code> 和 <code class="code-ref">src/core/codegen/</code> 的实际源码，IR 提取与代码生成的质量、边界覆盖（recursive schema、z.lazy、z.preprocess 等）无法从已提供文件中验证，这些是决定编译正确性的核心。engineering 分因此保守。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">src/unplugin/hoist-compile.ts:74</code> 的 <code class="code-ref">compileOne</code> 使用 <code class="code-ref">new Function(...)</code> 求值提升后的 schema 表达式——虽然受限于 zod-specifier 检查，但若用户项目中有 <code class="code-ref">const x = z.number;</code> 再 <code class="code-ref">export const s = x();</code>，free identifier 分析会将其归为 zod 绑定，<code class="code-ref">new Function</code> 的执行上下文与用户源码的模块作用域不同，可能在边界情况下产生不同结果。</p>
<p>接入前先在项目里跑 <code class="code-ref">zod-compiler check</code> 看有多少 schema 能被正确编译；对包含 z.preprocess / z.lazy 循环引用的 schema 重点做 safeParse 回归测试；HMR 场景需关注 <code class="code-ref">src/loader.ts</code> 的 <code class="code-ref">cacheGeneration</code> 在多入口构建中的正确性。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仓库仅 2 天历史、8 次 commit，核心 extract/codegen 模块未审阅，生产就绪度存疑。</li><li>Zod v4 尚未稳定，编译器对 v4 内部 <code class="code-ref">_zod.def</code> 结构的依赖意味着 Zod 版本升级可能破坏编译。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>Zod 在 TypeScript 生态已有大量存量代码，zod-compiler 零迁移成本的 build plugin 模式使其在性能敏感的 API 服务（tRPC/Hono）和 Next.js Server Actions 场景下有明确商业价值；若 benchmark 数据可复现，对 typia/ajv 的差异化竞争空间真实存在。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">55</div>
  <div class="score-bar"><span style="width:55%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">78.55</span>
  </div>
</div>
</section>