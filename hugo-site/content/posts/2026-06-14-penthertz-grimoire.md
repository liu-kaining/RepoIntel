---
title: '[Score: 76.4] PentHertz/grimoire'
date: '2026-06-14T13:57:10Z'
categories:
- Pentest Documentation Aggregator
tags:
- offline-search
- SQLite-FTS5
- MCP
- security-ops
- Python
- pentest-tooling
intel_score: 76.4
repo_name: PentHertz/grimoire
repo_link: https://github.com/PentHertz/grimoire
summary: 将 20+ 安全知识库（HackTricks、OWASP、LOTL 等）克隆后用 SQLite FTS5 建统一索引，提供 Web 搜索和 MCP
  接口供 AI 模型调用，适合离线渗透测试场景使用。
code_source: git
code_files_reviewed:
- requirements.txt
- pyproject.toml
- grimoire_app/__init__.py
- data/index_state.json
- grimoire_app/__main__.py
- custom/example.md
- context.example.yaml
- grimoire.py
- docs/QUICKSTART.md
- grimoire_app/context.py
- grimoire_app/config.py
- docs/SECURITY.md
- grimoire_app/view.py
- README.md
- docs/MCP_TUTORIAL.md
- grimoire_app/controller.py
- grimoire_app/runner.py
- grimoire_app/model.py
- grimoire_app/mcp.py
- test_grimoire.py
- sources.yaml
- grimoire_app/sources.default.yaml
code_chars_analyzed: 199120
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
      <span class="scope-stat__value">22 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 199,120 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">requirements.txt</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">grimoire_app/__init__.py</code></li><li><code class="path-chip">data/index_state.json</code></li><li><code class="path-chip">grimoire_app/__main__.py</code></li><li><code class="path-chip">custom/example.md</code></li><li><code class="path-chip">context.example.yaml</code></li><li><code class="path-chip">grimoire.py</code></li><li><code class="path-chip">docs/QUICKSTART.md</code></li><li><code class="path-chip">grimoire_app/context.py</code></li><li><code class="path-chip">grimoire_app/config.py</code></li><li><code class="path-chip">docs/SECURITY.md</code></li><li><code class="path-chip">grimoire_app/view.py</code></li><li><code class="path-chip">README.md</code></li><li class="path-more">另有 8 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>渗透测试人员在无网络的隔离环境中需要同时查阅 HackTricks、PayloadsAllTheThings、GTFOBins、OWASP WSTG 等数十个分散的 playbook，手动翻找耗时且容易遗漏；Grimoire 把这些源统一索引，一个搜索框即可跨源定位。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">项目采用 MVC 分层，<code class="code-ref">grimoire_app/__init__.py:17</code> 明确声明 config / model / view / controller / mcp 五个模块。主入口 grimoire.py:35 调用 controller.main()，CLI 解析在 <code class="code-ref">grimoire_app/controller.py:155</code>-185，子命令 fetch/index/serve/mcp 各自路由到 model 或 mcp 层。数据流：fetch 从 sources.yaml 读取仓库列表，model.cmd_fetch 逐个 shallow clone 到 data/sources/；index 通过 model.Index 类（<code class="code-ref">grimoire_app/model.py:199</code>-240）将所有 .md/.yml/.ipynb/.pdf 文件写入 SQLite FTS5 表；serve 启动 ThreadingHTTPServer（<code class="code-ref">grimoire_app/controller.py:31</code>），REST 端点路由到 model.search + view 渲染；mcp 启动 stdio JSON-RPC 循环（<code class="code-ref">grimoire_app/mcp.py:285</code>-307）暴露 search/fetch_doc/checklist 等工具。</p>
<p class="audit-callout audit-callout--highlight">SQL 注入防御设计扎实。<code class="code-ref">grimoire_app/model.py:231</code>-240 的 Index.search 方法所有 SQL 均使用参数绑定，同时 model.py:242-244 的 _fts_query 将用户输入过滤为纯字母数字的前缀 token 再拼入 MATCH 表达式，双层防护。test_grimoire.py:47-55 验证了 FTS5 元字符被剥离、分词后只剩 &quot;token&quot;* 形式。测试套件中 test_sqli_query_is_safe、test_search_category_injection_is_parameterized、test_search_match_injection_is_neutralized 覆盖了多种注入向量。</p>
<p class="audit-callout audit-callout--highlight">MCP 执行模式分层控制清晰。<code class="code-ref">grimoire_app/mcp.py:20</code>-22 定义 MODE 全局变量，active_tools()（mcp.py:157-161）在 read 模式下完全不暴露 install/run 工具，模型甚至无法尝试调用。<code class="code-ref">grimoire_app/runner.py:52</code>-64 的 _TOOL_RE 正则拒绝含 shell 元字符的工具名，防止命令注入。test_grimoire.py:289-310 覆盖了 mode 门控、注入拒绝、scope 执行拦截。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">grimoire_app/model.py:105</code>-127 的 cmd_fetch 使用 subprocess.Popen 调用 git clone，但 _safe_repo_url（model.py:20-28）仅校验 URL scheme，对已知恶意仓库（如供应链投毒的第三方仓库）无签名/哈希校验。SECURITY.md:24 明确声明「indexed sources are untrusted」，但 fetch 阶段本身即会执行 git 操作，且 <code class="code-ref">grimoire_app/model.py:89</code>-99 的 _fetch_org 会遍历 GitHub org 的全部公开仓库——一个被接管的 org 下新建的恶意仓库会被自动 clone。</p>
<p class="audit-callout audit-callout--doubt">web UI 无认证机制。<code class="code-ref">grimoire_app/controller.py:31</code> 的 ThreadingHTTPServer 绑定 127.0.0.1:8000，SECURITY.md 和 <code class="code-ref">docs/SECURITY.md:43</code> 均提醒需要自行添加 VPN/反代认证，但默认代码中无任何 access control。若用户以 --host 0.0.0.0 暴露，任何人可搜索并触发 /api/update（<code class="code-ref">grimoire_app/controller.py:76</code>-83 仅检查 X-Requested-With 自定义 header，不检查 Origin/Referer）。</p>
<p>对渗透测试团队而言，当前版本（1.0.0、创建仅 1 天）适合在受控环境中快速试用。建议：(1) 在隔离网络先验证 sources.yaml 中仓库的完整性再部署到生产隔离环境；(2) MCP 执行模式仅在实验性场景使用 assist/auto，正式评估中坚持 read 模式；(3) 若需在团队共享场景使用 serve，务必前置认证网关。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>sources.yaml 中 HackTricks 等条目硬编码 type:local 且 path 为 /tmp/gt/ht（<code class="code-ref">grimoire_app/sources.default.yaml</code>），pip 安装后该路径不存在，用户需手动修正</li><li>创建仅 1 天、0 open issues、仅 11 commits，社区未经过实际使用验证，稳定性存疑</li><li>_fetch_org 会自动 clone 某 GitHub org 下所有公开仓库，被投毒的 org 新建仓库会被静默索引</li><li>serve 无认证，暴露到非本地网络后任何人均可触发 /api/update 触发后台 git clone 操作</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>Grimoire 作为 RF-Swift 工具链的文档层，填补了离线渗透测试场景中安全知识统一检索的空白；MCP 接口使其成为 AI 辅助安全评估工作流中的自然组件，有潜力被安全咨询团队和 CTF 社区采纳为标准离线参考工具。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">80</div>
  <div class="score-bar"><span style="width:80%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.4</span>
  </div>
</div>
</section>