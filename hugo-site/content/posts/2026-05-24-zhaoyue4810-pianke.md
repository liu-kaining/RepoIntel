---
title: '[Score: 76.35] zhaoyue4810/pianke'
date: '2026-05-24T04:56:29Z'
categories:
- 本地摄影选片工具
tags:
- Python
- Flask
- DINOv2
- InsightFace
- RAW处理
- 摄影工作流
intel_score: 76.35
repo_name: zhaoyue4810/pianke
repo_link: https://github.com/zhaoyue4810/pianke
summary: 面向摄影师的本地 AI 选片工具，融合 DINOv2/InsightFace/EXIF 多信号分组与擂台式 A/B PK，支持 RAW+JPG 及
  LLM 远程初筛三种模式。
code_source: git
code_files_reviewed:
- requirements.txt
- tests/conftest.py
- scripts/run.sh
- tests/test_quality.py
- scripts/compress_images_target.py
- tests/test_prescreen_session.py
- scripts/diagnose_grouping.py
- README.md
- pic_selecter/vision.py
- scripts/launcher.py
- pic_selecter/fast_clustering.py
- pic_selecter/clustering.py
- pic_selecter/quality.py
- pic_selecter/fast_quality.py
- pic_selecter/llm_judge.py
- pic_selecter/grouper.py
- pic_selecter/watermark.py
code_chars_analyzed: 236134
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
      <span class="scope-stat__value">17 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 236,134 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">requirements.txt</code></li><li><code class="path-chip">tests/conftest.py</code></li><li><code class="path-chip">scripts/run.sh</code></li><li><code class="path-chip">tests/test_quality.py</code></li><li><code class="path-chip">scripts/compress_images_target.py</code></li><li><code class="path-chip">tests/test_prescreen_session.py</code></li><li><code class="path-chip">scripts/diagnose_grouping.py</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">pic_selecter/vision.py</code></li><li><code class="path-chip">scripts/launcher.py</code></li><li><code class="path-chip">pic_selecter/fast_clustering.py</code></li><li><code class="path-chip">pic_selecter/clustering.py</code></li><li><code class="path-chip">pic_selecter/quality.py</code></li><li><code class="path-chip">pic_selecter/fast_quality.py</code></li><li class="path-more">另有 3 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>婚礼/活动摄影师一次拍摄数百张连拍，人工逐张比对耗时 1-2 小时且容易错过最佳表情帧，需要一个能在本地离线完成废片剔除、相似帧归组和快速 A/B 筛选的工具，同时不能把客户照片上传到云端。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">整体采用 Flask 单页应用 + 后台线程池处理模式。入口 <code class="code-ref">app.py</code>（未审阅）负责路由与会话管理，核心分析管线在 <code class="code-ref">pic_selecter/grouper.py</code> 中 <code class="code-ref">compute_infos</code> 驱动：通过 <code class="code-ref">scan_folder</code> 递归收集文件并按 (目录, stem) 配对 RAW+JPG 伴随文件（<code class="code-ref">grouper.py:284</code>），然后用 <code class="code-ref">ThreadPoolExecutor</code> 并发调用 <code class="code-ref">_process_one</code>（<code class="code-ref">grouper.py:505</code>），每张图走 EXIF 解析 → 质量分析 → 视觉特征提取完整链路。分组由 <code class="code-ref">group_infos</code> 根据 engine 分发到 <code class="code-ref">clustering.cluster</code>（专家/土豪）或 <code class="code-ref">fast_clustering.cluster</code>（极速）。<code class="code-ref">clustering.py</code> 采用强制连拍检测（连号+时间差+phash 汉明距离）→ 时间硬切段 → DINOv2+人脸识别+EXIF 多信号加权 → complete linkage 聚类的四阶段流水线（<code class="code-ref">clustering.py:17-23</code>）。<code class="code-ref">quality.py</code> 的 <code class="code-ref">analyze_image</code> 实现了拉普拉斯方差模糊检测、曝光/对比度/熵分析、InsightFace 人脸锐度与 EAR 闭眼检测，以及 NIMA/MUSIQ/CLIP-IQA+ 三模型联合美学拒片（2-of-3 规则，<code class="code-ref">quality.py:228-240</code>）。LLM 初筛通过 <code class="code-ref">llm_judge.py</code> 调用火山引擎 Ark API，实现了自适应并发限速器 <code class="code-ref">_AdaptiveLimiter</code>（429 时减半、稳定后逐级回升，<code class="code-ref">llm_judge.py:100-155</code>）。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">fast_quality.py</code> 的极速模式质量评估实现了完整的纯传统 CV 链路——多锐度指标融合（拉普拉斯+Tenengrad+FFT 高频比+Marziliano 边宽）、FFT spectral residual saliency 显著性区域锐度、9 宫格局部分析、Hough 直线地平线检测，全部用 numpy+opencv 实现零模型依赖（<code class="code-ref">fast_quality.py:145-290</code>）。设计上通过 <code class="code-ref">_saliency_map</code> 自实现替代了 opencv-contrib 4.10+ 中被移除的 <code class="code-ref">cv2.saliency</code> 模块。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">clustering.py</code> 中人像场景的权重重分配逻辑——当两图都有人脸时自动切到 PORTRAIT 权重档（face ID 权重从 0.15 提升到 0.50，DINOv2 从 0.35 降到 0.20），解决了「同人不同背景该合的不合」和「不同人同背景错合」两个老问题（<code class="code-ref">clustering.py:40-50</code>）。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">requirements.txt</code> 注释详述了 opencv-python 与 opencv-contrib-python 共存导致 <code class="code-ref">cv2.saliency</code> 失效的问题，但 <code class="code-ref">grouper.py</code> 顶部直接 <code class="code-ref">import imagehash</code> 并依赖 <code class="code-ref">cv2</code>（通过 <code class="code-ref">_ensure_cv2</code>），而 <code class="code-ref">launcher.py</code> 中 <code class="code-ref">_ensure_opencv_single</code> 的清理逻辑依赖 <code class="code-ref">importlib.metadata</code> 在运行时检测冲突包（<code class="code-ref">launcher.py:228-258</code>）。如果用户通过 <code class="code-ref">pip install -r</code> 手动安装且 insightface 的传递依赖偷偷拉入 opencv-python，在 launcher 不介入的情况下 cv2 子模块会被覆盖，此场景目前仅靠注释文档提醒而非自动化防护。</p>
<p class="audit-callout audit-callout--doubt"><code class="code-ref">clustering.py</code> 中 <code class="code-ref">_pair_similarity</code> 对 DINOv2 缺失时直接 <code class="code-ref">raise RuntimeError</code>（<code class="code-ref">clustering.py:161</code>），但 <code class="code-ref">grouper.py</code> 的 <code class="code-ref">_process_one</code> 在 expert 分支中对 DINOv2 调用没有 try-except 保护（<code class="code-ref">grouper.py:410</code>），DINOv2 如果在单张图上返回零向量（已在 <code class="code-ref">vision.py:97</code> 有检查），异常会直接透传到 worker 的 <code class="code-ref">except Exception</code>，被归为「未知原因」跳过而非给出明确错误。此外，<code class="code-ref">app.py</code> 和前端代码未审阅，无法验证会话管理、CSRF 防护和路由设计。</p>
<p>对于婚礼/活动工作室场景，建议使用专家模式（人像分组精度最高），但首次需下载约 600MB 模型且首次启动需 10-30 秒预热。RAW+JPG 双拍用户可直接使用，纯 RAW 用户需确保安装 rawpy。注意 opencv 冲突问题，推荐使用一键启动器而非手动 pip install。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>app.py 和前端代码未审阅，无法验证 CSRF/Origin 校验是否真正生效，局域网暴露风险不确定。</li><li>依赖链极重（torch+transformers+insightface+pyiqa 约 2-3GB），opencv 三个包共存冲突靠注释文档而非强制约束，手动安装用户极易踩坑。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>面向中国摄影工作室的实用工具，解决婚纱/活动选片的高频痛点，纯本地模式天然满足客户隐私要求。三模式梯度设计（免费极速/本地 AI/LLM 远程）为商业化留有空间，土豪模式可作为 API 付费入口。</p>
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
  <div class="score-item__value">74</div>
  <div class="score-bar"><span style="width:74%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">实用性</div>
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">81</div>
  <div class="score-bar"><span style="width:81%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">62</div>
  <div class="score-bar"><span style="width:62%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.35</span>
  </div>
</div>
</section>