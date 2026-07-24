---
title: '[Score: 76.35] Icex0/wp2shell-poc'
date: '2026-07-24T11:01:17Z'
categories:
- Security Exploitation Tools
tags:
- wordpress
- sql-injection
- rce
- exploit
- penetration-testing
- python
intel_score: 76.35
repo_name: Icex0/wp2shell-poc
repo_link: https://github.com/Icex0/wp2shell-poc
summary: 针对 WordPress REST 路由混淆漏洞的完整利用链，从预认证 SQL 注入到 RCE 一键化，服务于安全测试场景。
code_source: git
code_files_reviewed:
- pyproject.toml
- wp2shell/__init__.py
- wp2shell/__main__.py
- wp2shell.py
- wp2shell/version.py
- wp2shell/shell.py
- wp2shell/client.py
- README.md
- wp2shell/sqli.py
- wp2shell/exploit.py
- wp2shell/cli.py
code_chars_analyzed: 79273
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
      <span class="scope-stat__value">11 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 79,273 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">wp2shell/__init__.py</code></li><li><code class="path-chip">wp2shell/__main__.py</code></li><li><code class="path-chip">wp2shell.py</code></li><li><code class="path-chip">wp2shell/version.py</code></li><li><code class="path-chip">wp2shell/shell.py</code></li><li><code class="path-chip">wp2shell/client.py</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">wp2shell/sqli.py</code></li><li><code class="path-chip">wp2shell/exploit.py</code></li><li><code class="path-chip">wp2shell/cli.py</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>渗透测试人员需手动变造多层 batch 请求、提取数据、构造提权序列，操作复杂且易因环境差异失败，缺乏稳定的自动化工具。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">核心路由混淆在 <code class="code-ref">wp2shell/client.py</code> 实现：BatchClient 使用 _DESYNC_PRIMER（<code class="code-ref">///</code>）制造路由数组偏移，外层将 POST /wp/v2/posts 请求送至 batch 处理器，内层将 GET /wp/v2/posts/999999 的 author_exclude 注入 WP_Query，形成 SQL 注入。数据读取由 <code class="code-ref">wp2shell/sqli.py</code> 的三种提取器完成：盲注通过 X-WP-Total 响应头做布尔二分搜索，错误注入利用 EXTRACTVALUE 反射，UnionSQLi 伪造 23 列 WP_Post 实现单次请求带内读取。<code class="code-ref">wp2shell/exploit.py</code> 的 PreAuthAdminCreator 将 UNION 注入产品化：先寻找可嵌入链接，渲染 oEmbed 缓存 post，再计算这些缓存 ID 构造 changeset 和导航项触发用户创建。<code class="code-ref">wp2shell/shell.py</code> 的 AdminSession 执行认证后 plugin upload，上传随机路径 webshell 执行命令。命令行接口在 <code class="code-ref">wp2shell/cli.py</code> 组装为 check/read/shell 子命令，提供通用超时、代理和版本检测。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">wp2shell/sqli.py</code> 的 UnionSQLi 利用 <code class="code-ref">orderby=none</code> 取消全局 ORDER BY，并设 <code class="code-ref">per_page=500</code> 保持全行模式，使 UNION SELECT 的伪造行成功渲染为 REST 响应，从响应体直接解析 HEX 包裹的标题，实现单请求读取任意 SQL 表达式，极大降低数据提取延迟。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">wp2shell/exploit.py</code> 的 PreAuthAdminCreator 通过 <code class="code-ref">wp_posts_tuple</code> 动态构造伪造行，配合恢复的 oEmbed 缓存 ID，在一个请求体中同时渲染 changeset、导航项和请求钩子形状，最终在同一个 batch 内调用用户创建端点，整个提权步骤无需外部交互。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 tests/ 目录或任何 <code class="code-ref">*_test.py</code> 文件，所有功能模块仅靠 README 示例验证，缺乏自动化测试覆盖，无法保证在不同 WordPress 配置或网络环境下的稳定性和健壮性。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">wp2shell/shell.py</code> 的 webshell 虽用随机 slug 和 token 保护，但 <code class="code-ref">run()</code> 方法无频率限制或一次性令牌，且 <code class="code-ref">cleanup()</code> 依赖 rm -rf 执行，若进程异常或连接中断可能导致 shell 残留并形成永久后门。</p>
<p>用于授权测试时，务必在测试后运行 <code class="code-ref">shell</code> 的子命令清理账户和文件；开发者应加入单元测试与 payload 定制化测试；增加 shell 心跳检测与强制删除逻辑。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>仅对 WordPress 6.9.0-6.9.4 及 7.0.0-7.0.1 有效，修复后完全失效。</li><li>需要目标站点存在至少一个已发布文章/页面以完成 oEmbed 缓存毒化，否则提权步骤不可用。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>安全厂商可集成此利用链到自动化扫描器，提升漏洞验证与演示效率，但因依赖特定版本，生命周期仅存于受影响站点。</p>
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
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">75</div>
  <div class="score-bar"><span style="width:75%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.35</span>
  </div>
</div>
</section>