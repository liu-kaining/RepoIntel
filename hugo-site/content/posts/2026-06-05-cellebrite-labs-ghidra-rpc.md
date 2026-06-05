---
title: '[Score: 76.3] cellebrite-labs/ghidra-rpc'
date: '2026-06-05T19:51:14Z'
categories:
- AI-Powered Reverse Engineering Tool
tags:
- Ghidra
- reverse-engineering
- CLI
- Unix-socket
- PyGhidra
- binary-analysis
intel_score: 76.3
repo_name: cellebrite-labs/ghidra-rpc
repo_link: https://github.com/cellebrite-labs/ghidra-rpc
summary: 将 Ghidra 逆向工程能力通过 Unix Socket JSON-RPC 暴露给 LLM Agent 的 CLI 守护进程，让 AI 助手可自主完成反编译、调用图追踪与符号标注。
code_source: git
code_files_reviewed:
- package.json
- pyproject.toml
- ghidra_rpc/server/__init__.py
- ghidra_rpc/__init__.py
- ghidra_rpc/server/tools/__init__.py
- ghidra_rpc/server/main.py
- tests/test_tools.py
- ghidra_rpc/server/tools/navigation.py
- docs/flows/binary-audit.md
- docs/install.md
- docs/flows/vulnerability-research.md
- ghidra_rpc/server/_gui_launcher.py
- .pi/prompts/process-feedback.md
- ghidra_rpc/server/launcher.py
- ghidra_rpc/server/tools/decompiler.py
- docs/quickstart.md
- README.md
- ghidra_rpc/session.py
- tests/test_protocol.py
- ghidra_rpc/daemon.py
- ghidra_rpc/server/tools/xrefs.py
- docs/flows/patch-analysis.md
- ghidra_rpc/client.py
- tests/test_client.py
- ghidra_rpc/server/tools/tags.py
- ghidra_rpc/server/tools/search.py
- docs/troubleshooting.md
- ghidra_rpc/server/tools/processor_context.py
- docs/internals.md
- ghidra_rpc/server/tools/bookmarks.py
- ghidra_rpc/server/tools/memory.py
- ghidra_rpc/server/tools/cfg.py
- ghidra_rpc/server/tools/disassembly.py
- ghidra_rpc/server/tools/analysis.py
- AGENTS.md
- ghidra_rpc/server/tools/version_tracking.py
- ghidra_rpc/server/context.py
- SKILL.md
- ghidra_rpc/server/tools/data_types.py
code_chars_analyzed: 298392
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
      <span class="scope-stat__value">39 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 298,392 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">package.json</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">ghidra_rpc/server/__init__.py</code></li><li><code class="path-chip">ghidra_rpc/__init__.py</code></li><li><code class="path-chip">ghidra_rpc/server/tools/__init__.py</code></li><li><code class="path-chip">ghidra_rpc/server/main.py</code></li><li><code class="path-chip">tests/test_tools.py</code></li><li><code class="path-chip">ghidra_rpc/server/tools/navigation.py</code></li><li><code class="path-chip">docs/flows/binary-audit.md</code></li><li><code class="path-chip">docs/install.md</code></li><li><code class="path-chip">docs/flows/vulnerability-research.md</code></li><li><code class="path-chip">ghidra_rpc/server/_gui_launcher.py</code></li><li><code class="path-chip">.pi/prompts/process-feedback.md</code></li><li><code class="path-chip">ghidra_rpc/server/launcher.py</code></li><li class="path-more">另有 25 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>安全研究员在分析二进制时需要反复手动操作 Ghidra GUI：反编译、交叉引用查找、重命名函数、标注漏洞——每个二进制平均耗费数小时重复性鼠标点击；LLM 虽能推理代码语义但缺少访问 Ghidra API 的标准化管道。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">ghidra-rpc 采用守护进程 + CLI 客户端的双进程架构。CLI（<code class="code-ref">ghidra_rpc/cli.py</code>，未审阅到源码）通过 <code class="code-ref">ghidra_rpc/client.py:47</code> 的 <code class="code-ref">send_request</code> 发送 newline-delimited JSON 到 Unix domain socket；服务端 <code class="code-ref">ghidra_rpc/server/main.py:46</code> 的 <code class="code-ref">_handle_connection</code> 解析请求并由全局 <code class="code-ref">_HANDLER_LOCK</code> 串行化所有 handler 调用，避免 Ghidra 事务冲突。<code class="code-ref">ghidra_rpc/server/tools/__init__.py:6</code> 的 <code class="code-ref">register_all_tools()</code> 在启动时注册 14 个工具模块，覆盖反编译、交叉引用、搜索、内存读写、CFG/P-code、版本追踪等能力。<code class="code-ref">ghidra_rpc/server/context.py:44</code> 的 <code class="code-ref">HeadlessContext</code> 管理项目生命周期和 <code class="code-ref">ProgramInfo</code> 数据，<code class="code-ref">context.py:60</code> 的 <code class="code-ref">DecompilerPool</code> 提供线程安全的反编译器实例池。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">ghidra_rpc/server/context.py:88</code> 的 <code class="code-ref">DecompilerPool.acquire()</code> 采用「容量检查持锁、创建放锁」模式避免初始化期间死锁，与 <code class="code-ref">LifoQueue</code> 组合实现池化复用，设计合理。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">ghidra_rpc/server/tools/version_tracking.py:40</code> 的 <code class="code-ref">_open_vt_programs</code> 为版本追踪操作临时释放守护进程的排他写锁再重开引用，处理了 Ghidra VTSessionDB 与 GhidraProject 互斥锁冲突这一棘手边界，最终通过 <code class="code-ref">_restore_daemon_programs</code> 恢复状态。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">tests/test_tools.py:10</code> 所有集成测试被硬编码 <code class="code-ref">skip</code>，实际覆盖率为零——没有任何测试验证工具 handler 的返回值正确性。<code class="code-ref">test_protocol.py</code> 和 <code class="code-ref">test_client.py</code> 仅覆盖协议层与客户端逻辑，不涉及 Ghidra API 调用。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">ghidra_rpc/server/main.py:46</code> 的 <code class="code-ref">_handle_connection</code> 使用 <code class="code-ref">conn.recv(65536)</code> 读取请求但没有长度前缀或消息边界保护——如果客户端发送的数据恰好不含换行符（例如超大 JSON），handler 会阻塞在 <code class="code-ref">while b&quot;\n&quot; not in buf</code> 循环中直到连接超时或 OOM，缺少最大缓冲区大小限制。</p>
<p>补充可运行的 mock-Ghidra 集成测试（至少覆盖 load→decompile→rename 链路）；在 <code class="code-ref">_handle_connection</code> 中加入缓冲区大小上限（如 1MB）防止慢速客户端耗尽内存；对 <code class="code-ref">_HANDLER_LOCK</code> 的全局串行化考虑按 binary key 分片以提升并发吞吐。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>无 LICENSE 文件——仓库未声明许可证，商业化或二次分发存在法律灰区。</li><li>CLI 入口 <code class="code-ref">ghidra_rpc/cli.py</code> 未包含在审阅文件中，无法验证所有用户命令的参数校验与错误处理是否一致。</li><li>fork_star_ratio 仅 8.4%（119★/10F），commit 仅 1 次且仓库仅 1 天历史，社区健康度极低，项目存活前景不确定。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>Cellebrite 作为数字取证龙头推出的开源 Agent 技能，可为其商业 RE 平台培养生态用户；对独立安全团队而言，能将二进制审计从「人盯 GUI」变为「Agent 自动跑脚本 + 人复核」的半自动化工作流，但 Ghidra 的 AGPL 依赖和 JVM 环境限制了轻量化部署场景。</p>
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
  <div class="score-item__value">87</div>
  <div class="score-bar"><span style="width:87%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">42</div>
  <div class="score-bar"><span style="width:42%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.3</span>
  </div>
</div>
</section>