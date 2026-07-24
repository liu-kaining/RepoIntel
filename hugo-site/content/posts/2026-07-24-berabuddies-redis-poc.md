---
title: '[Score: 79.15] berabuddies/redis-poc'
date: '2026-07-24T08:22:49Z'
categories:
- Security Exploit
tags:
- Redis
- RCE
- Exploit
- Heap Bug
- Patch Bypass
intel_score: 79.15
repo_name: berabuddies/redis-poc
repo_link: https://github.com/berabuddies/redis-poc
summary: 针对Redis多版本漏洞的完整RCE利用链集，包含堆布局操控与无痕恢复，面向授权安全测试。
code_source: git
code_files_reviewed:
- crc64.h
- P86_run.sh
- P74_loop.sh
- calibrate.sh
- crcspeed.h
- HARDENING.md
- A_lib.py
- P88W_lib.py
- README.md
- P74_g2.py
- P88W_corrupt.py
- crc64.c
- crcspeed.c
- P88W_exploit.py
- G2_arbread.py
- P74_exploit.py
- T88_exploit.py
- P86_exploit.py
- A_exploit_stock.py
code_chars_analyzed: 135227
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
      <span class="scope-stat__value">19 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 135,227 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">crc64.h</code></li><li><code class="path-chip">P86_run.sh</code></li><li><code class="path-chip">P74_loop.sh</code></li><li><code class="path-chip">calibrate.sh</code></li><li><code class="path-chip">crcspeed.h</code></li><li><code class="path-chip">HARDENING.md</code></li><li><code class="path-chip">A_lib.py</code></li><li><code class="path-chip">P88W_lib.py</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">P74_g2.py</code></li><li><code class="path-chip">P88W_corrupt.py</code></li><li><code class="path-chip">crc64.c</code></li><li><code class="path-chip">crcspeed.c</code></li><li><code class="path-chip">P88W_exploit.py</code></li><li class="path-more">另有 5 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>红队和安全研究者在评估Redis服务器安全性时，缺乏可直接验证高危漏洞的可靠利用工具，且需避免服务崩溃和残留污染。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">利用两种核心漏洞（stream NACK double free 和 RedisBloom 模块堆溢出），构建从任意读原语到 RCE 的完整链。A_lib.py 提供 RESP 通信、CRC64 计算及 payload 构建；G2_arbread.py 实现基于 UAF 的平滑任意读；各版本独立脚本调用共享模块并组合成最终利用。例如 A_exploit_stock.py 的 <code class="code-ref">stage4</code> 通过伪造 dict-&gt;type 植入 system 函数指针，RCE 后立即恢复原指针（A_exploit_stock.py: <code class="code-ref">stage4</code> 中的恢复写入 <code class="code-ref">fe.write(D1 + 1, struct.pack(&#x27;&lt;Q&#x27;, orig_type)[1:8])</code>），确保服务器正常运行。</p>
<p class="audit-callout audit-callout--highlight">非破坏性设计贯穿全链，A_exploit_stock.py 的 <code class="code-ref">cleanup</code> 函数删除临时键并恢复 save/slowlog 配置，配合 HARDENING.md 详述的残留处理，使目标在利用后功能无损（A_exploit_stock.py: <code class="code-ref">cleanup</code> 中重置 <code class="code-ref">CONFIG SET save</code>）。</p>
<p class="audit-callout audit-callout--highlight">在 7.4/8.6 版本中，通过 P74_g2.py 的 <code class="code-ref">reclaim_echo</code> 利用 XINFO FULL 无损检测堆布局（P74_g2.py: 函数 <code class="code-ref">xinfo_count</code> 读取 delivery_count 判断状态），避免依赖 DEBUG 命令，提升了实战隐蔽性。</p>
<p class="audit-callout audit-callout--doubt">利用脚本硬编码大量二进制偏移（如 A_exploit_stock.py 中的 <code class="code-ref">STR_FORMAT_OFF = 0x11fc20</code>），尽管可通过命令行覆盖，但未提供自动化偏移提取逻辑，换用非官方镜像时易失败。</p>
<p class="audit-callout audit-callout--doubt">项目未包含任何自动化测试或 CI 流程，README 中列出的可靠性数字（如“6.2.22 10/10”）均为手工验证，缺乏回归保护；核心利用函数中大量 <code class="code-ref">assert</code> 可用于调试，但缺少异常捕获下的优雅降级处理。</p>
<p>可补充 Dockerized 测试套件，自动复现多版本利用并通过 CI 持续验证；将偏移配置外置为 YAML 文件，降低人为误配风险。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>目标必须是官方编译的特定 Redis 二进制，非标准构建需手动校准，否则可能无效或诱发守护进程崩溃。</li><li>利用高度依赖 jemalloc 分配器布局，内存碎片或并发请求会显著降低成功率，生产环境复现难度大。</li><li>README 明确要求使用全新实例，已负载的服务器上触发易失败，限制了真实渗透场景的适用面。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>可直接集成至红队工具集或安全评估平台，缩短漏洞验证时间，降低因误操作导致服务中断的风险。</p>
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
  <div class="score-item__value">85</div>
  <div class="score-bar"><span style="width:85%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">65</div>
  <div class="score-bar"><span style="width:65%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.15</span>
  </div>
</div>
</section>