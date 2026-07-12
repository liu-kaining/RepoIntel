---
title: '[Score: 79.3] pengchujin/jzsub'
date: '2026-07-12T15:56:57Z'
categories:
- Video Processing
tags:
- yt-dlp
- Subtitles
- AI Translation
- Codex Skill
- Bilingual
- FFmpeg
intel_score: 79.3
repo_name: pengchujin/jzsub
repo_link: https://github.com/pengchujin/jzsub
summary: 输入视频链接，全自动下载最高画质、生成 GPT 双语字幕并烧录为 MP4，适合外语内容消费。
code_source: git
code_files_reviewed:
- skills/jzsub/tests/test_verify_delivery.py
- skills/jzsub/tests/test_burn_subtitles.py
- skills/jzsub/tests/test_subtitle_pipeline.py
- skills/jzsub/agents/openai.yaml
- TODO.md
- skills/jzsub/references/translation-contract.md
- skills/jzsub/references/chrome-auth.md
- skills/jzsub/references/platform-notes.md
- README.md
- skills/jzsub/scripts/verify_delivery.py
- skills/jzsub/SKILL.md
- skills/jzsub/scripts/burn_subtitles.py
code_chars_analyzed: 89578
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
      <span class="scope-stat__value">12 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 89,578 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">skills/jzsub/tests/test_verify_delivery.py</code></li><li><code class="path-chip">skills/jzsub/tests/test_burn_subtitles.py</code></li><li><code class="path-chip">skills/jzsub/tests/test_subtitle_pipeline.py</code></li><li><code class="path-chip">skills/jzsub/agents/openai.yaml</code></li><li><code class="path-chip">TODO.md</code></li><li><code class="path-chip">skills/jzsub/references/translation-contract.md</code></li><li><code class="path-chip">skills/jzsub/references/chrome-auth.md</code></li><li><code class="path-chip">skills/jzsub/references/platform-notes.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">skills/jzsub/scripts/verify_delivery.py</code></li><li><code class="path-chip">skills/jzsub/SKILL.md</code></li><li><code class="path-chip">skills/jzsub/scripts/burn_subtitles.py</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>学习外语视频时需手动下载、提取字幕、翻译并重新嵌入，步骤繁琐且易出错。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">JZSub 形成一个完整的视频处理流水线：fetch_video.py 下载视频、封面和字幕（未审阅源码，但通过测试和文档推断其行为），subtitle_pipeline.py 将字幕分批供会话模型翻译并生成 ASS 双语字幕，burn_subtitles.py 烧录最终 MP4，最后 verify_delivery.py 验证各环节完成情况。模块间通过 JSON 清单传递状态，实现断点续做。</p>
<p class="audit-callout audit-callout--highlight">烧录脚本 <code class="code-ref">skills/jzsub/scripts/burn_subtitles.py</code> 的 <code class="code-ref">_verify_output</code> 函数对输出进行严格验证，检查容器格式、时长（允许 1% 或 0.5s 偏差）、分辨率是否匹配、帧率漂移不超过 0.5%，并确保音频轨道存在（引用了 <code class="code-ref">_verify_output</code> 内的 <code class="code-ref">abs(output_duration - input_duration) &gt; duration_tolerance</code> 等逻辑）。</p>
<p class="audit-callout audit-callout--highlight">字幕管线通过紧凑分批、原文锁定和翻译合约保证安全，测试文件 <code class="code-ref">skills/jzsub/tests/test_subtitle_pipeline.py</code> 中的 <code class="code-ref">test_ass_malicious_text_is_losslessly_escaped</code> 验证了对 ASS 特殊字符的转义，防止注入；<code class="code-ref">test_translation_contract_rejects_missing_duplicate_and_hash_mismatch</code> 展示了哈希校验和防止原文篡改。</p>
<p class="audit-callout audit-callout--doubt">未审阅到 <code class="code-ref">fetch_video.py</code> 和 <code class="code-ref">subtitle_pipeline.py</code> 的完整实现，无法确认下载器对反爬、登录失败、网络异常的处理细节；依赖 <code class="code-ref">test_subtitle_pipeline.py</code> 通过 importlib 加载推断接口，实际鲁棒性待验证。</p>
<p class="audit-callout audit-callout--doubt">项目重度依赖外部二进制（yt-dlp、带 libass 的 FFmpeg、MiSans 字体），且字体需手动从指定链接下载安装，增加了用户环境配置门槛；虽然 <code class="code-ref">burn_subtitles.py</code> 具备字体缺失警告和回退，但未提供 Docker 等容器化方案。</p>
<p>适合作为本地脚本或 Codex Skill 集成，处理个人外语视频库。建议提供 Docker 镜像、完善 Windows 支持（见 TODO.md），并持续跟进 yt-dlp 版本以应对平台接口变更。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>依赖的外部工具（yt-dlp、FFmpeg）若版本不兼容或平台提取器失效，可能导致完全不可用。</li><li>字体 MiSans 需手动下载安装，且 Windows 下登录态下载尚未解决，限制了部分用户群体。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>展示了 AI Agent 执行端到端视频本地化的能力，可应用于内容出海、教育素材制作，但工具属性大于产品属性，难以独立盈利。</p>
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
  <div class="score-item__value">88</div>
  <div class="score-bar"><span style="width:88%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">79.3</span>
  </div>
</div>
</section>