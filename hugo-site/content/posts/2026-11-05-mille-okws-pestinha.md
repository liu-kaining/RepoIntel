---
title: '[Score: 76.0] mille-okws/pestinha'
date: '2026-11-05T19:27:48Z'
categories:
- Desktop Companion
tags:
- Python
- PySide6
- Spiking Neural Network
- Cross-platform
- Local-first
- Desktop Automation
intel_score: 76.0
repo_name: mille-okws/pestinha
repo_link: https://github.com/mille-okws/pestinha
summary: 基于脉冲神经网络与本地学习的桌面虚拟宠物，可感知窗口活动并随交互演化情绪。
code_source: git
code_files_reviewed:
- pyproject.toml
- requirements.txt
- .github/workflows/testes.yml
- .github/workflows/executaveis.yml
- pestinha/controle/__init__.py
- pestinha/__init__.py
- pestinha/plataforma/__init__.py
- assets/comum/programas.json
- pestinha/mathutil.py
- pestinha/sense/README.md
- executáveis/windows/pets/bryan.json
- pets/bryan.json
- tests/test_carinho.py
- pestinha/controle/README.md
- pestinha/world/README.md
- executáveis/README.md
- docs/README.md
- pestinha/body/README.md
- pestinha/ui/README.md
- tests/test_homeostase.py
- conftest.py
- pestinha/plataforma/README.md
- pestinha/mind/README.md
- pestinha/plataforma/_comum.py
- docs/auditorias/README.md
- pestinha/core/README.md
- executáveis/windows/pets/jorge.json
- pets/jorge.json
- ferramentas/README.md
- tests/test_robustez.py
- tests/test_mesa.py
- pestinha/settings_store.py
- tests/test_paineis.py
- tests/test_festa.py
- tests/test_bolinha.py
- tests/test_atividade.py
- pestinha/mind/festa.py
- pestinha/ui/rotulos.py
- tests/test_castigo_integracao.py
- pestinha/log.py
- tests/test_castigo_bugs_rede.py
- tests/test_pedido.py
code_chars_analyzed: 49456
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
      <span class="scope-stat__value">42 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 49,456 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">requirements.txt</code></li><li><code class="path-chip">.github/workflows/testes.yml</code></li><li><code class="path-chip">.github/workflows/executaveis.yml</code></li><li><code class="path-chip">pestinha/controle/__init__.py</code></li><li><code class="path-chip">pestinha/__init__.py</code></li><li><code class="path-chip">pestinha/plataforma/__init__.py</code></li><li><code class="path-chip">assets/comum/programas.json</code></li><li><code class="path-chip">pestinha/mathutil.py</code></li><li><code class="path-chip">pestinha/sense/README.md</code></li><li><code class="path-chip">executáveis/windows/pets/bryan.json</code></li><li><code class="path-chip">pets/bryan.json</code></li><li><code class="path-chip">tests/test_carinho.py</code></li><li><code class="path-chip">pestinha/controle/README.md</code></li><li class="path-more">另有 28 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>开发者在长时间编码时缺乏轻量陪伴反馈，现有桌面宠物多为预设动画，无法根据用户行为和环境变化调整行为。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro"><code class="code-ref">pestinha/plataforma/__init__.py</code> 按 sys.platform 动态选择 windows/macos/linux 后端，统一暴露进程名、窗口几何、空闲时长等接口；上层分为 core、sense、body、mind、world、ui、controle，<code class="code-ref">tests/test_arquitetura.py</code>（README 提及）强制依赖边界。采集数据经 <code class="code-ref">pestinha/sense/senses.py</code> 的活动分类（<code class="code-ref">tests/test_atividade.py</code> 验证 code.exe→PROGRAMMING）输入脉冲网络，再由 motor 神经活动驱动身体状态和行为控制器，形成闭环。</p>
<p class="audit-callout audit-callout--highlight">跨平台抽象清晰，<code class="code-ref">pestinha/plataforma/_comum.py</code> 的 <code class="code-ref">rodar</code> 对 subprocess 超时和失败统一返回 None，<code class="code-ref">pestinha/settings_store.py</code> 的 save/panic 捕获 OSError 保证会话不崩。</p>
<p class="audit-callout audit-callout--highlight">人格参数与网络结构解耦，<code class="code-ref">pets/bryan.json</code> 和 <code class="code-ref">pets/jorge.json</code> 通过 temperamento 权重调整 DISMISS-&gt;FRUSTRATION、TOY_TAKEN-&gt;GLOOM 等映射，<code class="code-ref">pestinha/ui/rotulos.py</code> 定义了 20+ 感官/运动通道名，证明同一网络可配置不同行为风格。</p>
<p class="audit-callout audit-callout--doubt">核心网络实现 <code class="code-ref">pestinha/core/nervous_system.py</code>、<code class="code-ref">pestinha/core/homeostasis.py</code> 未在 bundle 中，仅从 <code class="code-ref">tests/test_homeostase.py</code> 的 <code class="code-ref">Drives.update</code> 调用推断存在，无法验证 LIF 积分、突触权重、防 NaN 等细节，工程评分已下调。</p>
<p class="audit-callout audit-callout--doubt">版本号不一致，<code class="code-ref">pyproject.toml</code> 声明 0.8.0，但 <code class="code-ref">pestinha/__init__.py</code> 为 0.7.0；<code class="code-ref">pestinha/mind/festa.py</code> 的 euforia 累积参数硬编码，调整需改源码。</p>
<p>尽快补齐核心模块的单元测试覆盖（尤其 NaN 边界，参照 <code class="code-ref">docs/auditorias/README.md</code> 的审计历史），统一版本号，并将 FestaController 参数迁移至 JSON 配置以支持外部调整。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>核心神经网络源码未审阅，LIF 稳定性与学习算法无法确认，谨慎用于严肃场景。</li><li>项目仅 4 天、5 次 commit，行为可能频繁变更，不宜作为稳定依赖。</li><li>Windows/macOS 可执行文件未签名，用户需手动处理系统安全警告。</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>作为本地陪伴/娱乐工具，具备小众市场潜力，可通过个性化角色包或赞助获得收入；但娱乐属性强，商业天花板有限。</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.0</span>
  </div>
</div>
</section>