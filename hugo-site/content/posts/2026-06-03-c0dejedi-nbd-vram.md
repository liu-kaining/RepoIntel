---
title: '[Score: 79.8] c0deJedi/nbd-vram'
date: '2026-06-03T10:53:56Z'
categories:
- System Tools
tags:
- Linux
- CUDA
- swap
- NBD
- GPU
- shell
intel_score: 79.8
repo_name: c0deJedi/nbd-vram
repo_link: https://github.com/c0deJedi/nbd-vram
summary: 通过 NBD 协议将闲置 NVIDIA GPU 显存映射为 Linux swap 分区，适用于焊死内存的混合显卡笔记本用户扩展可用内存。
code_source: git
code_files_reviewed:
- Makefile
- .github/FUNDING.yml
- nbd-vram-disconnect.sh
- nbd-vram-connect.sh
- uninstall.sh
- test-fill.sh
- nbd-vram-power-check.sh
- test-nbd.sh
- benchmarks/bench-latency.sh
- benchmarks/bench-throughput.sh
- install.sh
- benchmarks/bench-iops.sh
- README.md
- nbd-vram.c
code_chars_analyzed: 50827
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
      <span class="scope-stat__value">14 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 50,827 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">Makefile</code></li><li><code class="path-chip">.github/FUNDING.yml</code></li><li><code class="path-chip">nbd-vram-disconnect.sh</code></li><li><code class="path-chip">nbd-vram-connect.sh</code></li><li><code class="path-chip">uninstall.sh</code></li><li><code class="path-chip">test-fill.sh</code></li><li><code class="path-chip">nbd-vram-power-check.sh</code></li><li><code class="path-chip">test-nbd.sh</code></li><li><code class="path-chip">benchmarks/bench-latency.sh</code></li><li><code class="path-chip">benchmarks/bench-throughput.sh</code></li><li><code class="path-chip">install.sh</code></li><li><code class="path-chip">benchmarks/bench-iops.sh</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">nbd-vram.c</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>焊死内存的混合显卡笔记本（如 AMD 集显 + RTX 独显）用户面临 RAM 不足、频繁换页到 SSD 的高延迟问题，而独显的 8 GB VRAM 长期闲置却无法被操作系统利用为扩展内存。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">daemon 在用户态通过 dlopen 加载 libcuda.so.1（<code class="code-ref">nbd-vram.c:78</code> 的 <code class="code-ref">load_libcuda</code>），用 cuMemAlloc 分配 VRAM，然后实现完整的 NBD fixed-newstyle 协议，通过 Unix socket（<code class="code-ref">SOCK_PATH = /run/nbd-vram.sock</code>）向内核 nbd 驱动暴露块设备。Shell 脚本层负责 mkswap/swapon 生命周期、systemd 服务编排和电源管理。</p>
<p class="audit-callout audit-callout--highlight">VRAM 分配采用渐进退避策略（<code class="code-ref">nbd-vram.c:307-318</code>），从请求大小开始每次减 512 MiB 重试，直到 ≥1024 MiB，能自适应显示合成器已占用部分显存的场景，无需用户精确估算。</p>
<p class="audit-callout audit-callout--highlight">断开脚本 <code class="code-ref">nbd-vram-disconnect.sh:9-12</code> 在 swapoff 失败时主动 abort 并拒绝断开 NBD 连接，注释明确指出「Disconnecting NBD with active swap pages mapped causes a kernel panic」，这是生产级的故障防护意识。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">nbd-vram.c:195</code> 的 NBD 传输循环是单线程串行处理——每个 READ/WRITE 请求阻塞在 cuMemcpyHtoD/DtoH + cuCtxSynchronize 上，高 iodepth 下无法并发。README 中 fio 基准测试（VRAM 28.7k IOPS vs NVMe 45.4k IOPS）已暴露此瓶颈，但代码中无任何并发/多线程改造计划或 TODO 注释。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 systemd unit 文件（<code class="code-ref">systemd/vram-swap-nbd.service</code>、<code class="code-ref">systemd/nbd-vram-power-check.service</code> 等）和 <code class="code-ref">nbd-vram.conf</code> 配置模板的源码，本次结论不覆盖服务编排细节。这些文件在 <code class="code-ref">install.sh:49-55</code> 被引用安装但未出现在 code_bundle 中。</p>
<p>当前适合在个人笔记本上作为实验性扩展内存方案使用。若要提升至生产可靠性，建议：(1) 为传输循环引入线程池处理并发 I/O，(2) 添加 CUDA OOM 时的 graceful fallback（当前 cuMemcpy 失败直接返回 EIO 给内核，可能触发 swap storm），(3) 补充 GPU 挂掉时的 watchdog 与自动恢复逻辑。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>cuMemcpy 是同步拷贝（PCIe 往返），GPU 重负载（如训练/推理）时 swap 延迟可能骤升数倍，README 未提及此干扰场景。</li><li>fork_star_ratio 仅 1.67%（240 star / 4 fork），围观远大于参与，且仓库仅 3 天历史、8 次提交，长期维护可持续性存疑。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为开源工具直接面向痛点明确的小众群体（焊死内存的笔记本 Linux 用户），社区传播潜力可观，但商业变现路径不明确，适合作为个人技术品牌项目。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">78</div>
  <div class="score-bar"><span style="width:78%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.8</span>
  </div>
</div>
</section>