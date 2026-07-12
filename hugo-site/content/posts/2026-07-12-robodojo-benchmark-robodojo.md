---
title: '[Score: 77.2] RoboDojo-Benchmark/RoboDojo'
date: '2026-07-12T05:54:50Z'
categories:
- Robotics Benchmark
tags:
- robotics
- benchmark
- simulation
- manipulation
- IsaacSim
- real-robot
intel_score: 77.2
repo_name: RoboDojo-Benchmark/RoboDojo
repo_link: https://github.com/RoboDojo-Benchmark/RoboDojo
summary: 面向通用机器人操作策略的 sim-and-real 统一基准，42个仿真任务+18个真机任务，集成XPolicyLab多策略评估，支持异构并行仿真与崩溃恢复。
code_source: git
code_files_reviewed:
- scripts/requirements.txt
- pyproject.toml
- Dockerfile
- src/__init__.py
- env/environment/isaac/__init__.py
- src/eval_client/main.py
- src/eval_client/physx_warning_monitor.py
- src/eval_client/eval_env.py
- env_cfg/robot/_robot_info.json
- env_cfg/sim/sim_config.yml
- scripts/internal/prepare_policy_server.sh
- task/RoboDojo/config/stack_bowls.yml
- task/RoboDojo/config/fold_clothes.yml
- env_cfg/arx_x5.yml
- docker/entrypoint.sh
- task/RoboDojo/config/stack_blocks_by_language.yml
- env_cfg/robot/dual_x5.yml
- env/global_configs.py
- task/RoboDojo/config/swap_T.yml
- task/RoboDojo/config/plug_in_charger.yml
- .pre-commit-config.yaml
- task/RoboDojo/config/push_T.yml
- task/RoboDojo/config/align_blocks.yml
- task/RoboDojo/config/insert_key.yml
- task/RoboDojo/config/fold_clothes_random.yml
- task/RoboDojo/config/stack_blocks.yml
- task/RoboDojo/config/insert_tubes.yml
- env_cfg/robot/dual_x5_and_franka_competition.yml
- task/RoboDojo/config/hang_mugs.yml
- task/RoboDojo/task_registry.py
- env_cfg/camera/camera_config.yml
- env_cfg/camera/template.py
- utils/ensure_usd_path.py
- task/RoboDojo/config/fill_egg_holder.yml
- task/RoboDojo/tasks/general_pickup.py
- task/RoboDojo/config/put_bottles_into_dustbin.yml
- task/RoboDojo/config/stack_bowls_random.yml
- env_cfg/scene/conveyor.yml
- task/RoboDojo/config/deposit_coin.yml
- task/RoboDojo/config/stack_blocks_random.yml
- env/environment/isaac/direct_rl_env.py
- task/RoboDojo/config/sweep_blocks.yml
- task/RoboDojo/tasks/match_and_pick_from_conveyor.py
- task/RoboDojo/config/hang_mugs_random.yml
- task/RoboDojo/config/pour_balls_into_vase.yml
- task/RoboDojo/config/play_Xylophone.yml
- env_cfg/scene/default.yml
code_chars_analyzed: 141829
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
      <span class="scope-stat__value">47 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 141,829 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">scripts/requirements.txt</code></li><li><code class="path-chip">pyproject.toml</code></li><li><code class="path-chip">Dockerfile</code></li><li><code class="path-chip">src/__init__.py</code></li><li><code class="path-chip">env/environment/isaac/__init__.py</code></li><li><code class="path-chip">src/eval_client/main.py</code></li><li><code class="path-chip">src/eval_client/physx_warning_monitor.py</code></li><li><code class="path-chip">src/eval_client/eval_env.py</code></li><li><code class="path-chip">env_cfg/robot/_robot_info.json</code></li><li><code class="path-chip">env_cfg/sim/sim_config.yml</code></li><li><code class="path-chip">scripts/internal/prepare_policy_server.sh</code></li><li><code class="path-chip">task/RoboDojo/config/stack_bowls.yml</code></li><li><code class="path-chip">task/RoboDojo/config/fold_clothes.yml</code></li><li><code class="path-chip">env_cfg/arx_x5.yml</code></li><li class="path-more">另有 33 个文件未展示</li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>机器人学家缺乏能统一评估通用操作策略的标准化基准，现有仿真任务太简单且无法可靠对应真实世界表现，导致策略对比困难。</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">入口 <code class="code-ref">src/eval_client/main.py</code> 解析命令行参数，启动 Isaac Sim App，动态加载任务注册表 (<code class="code-ref">task/RoboDojo/task_registry.py</code>)，构建 <code class="code-ref">EvalEnv</code>（<code class="code-ref">src/eval_client/eval_env.py</code> 中的工厂方法 <code class="code-ref">create_eval_env</code>）。每个 episode 通过 WebSocket 调用外部策略服务 (<code class="code-ref">XPolicyLab</code>)，支持单环境顺序或批量并行评估。核心亮点是 <code class="code-ref">src/eval_client/physx_warning_monitor.py</code> 实现的 PhysX 异常监控与恢复体系：通过 <code class="code-ref">dup2</code> 重定向 stdout/stderr 到管道，多线程扫描 &#x27;Invalid PhysX transform&#x27; 日志（<code class="code-ref">_reader_loop</code>），识别错误环境；结合尾随线程（<code class="code-ref">_tail_loop</code>）和镜像文件（<code class="code-ref">/dev/shm</code>）形成冗余检测。main.py 的 <code class="code-ref">_restart_or_exit</code> 利用 os.execv 实现进程级自恢复，并持久化进度到 <code class="code-ref">_resume_&lt;run_id&gt;.json</code>。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/eval_client/physx_warning_monitor.py</code> 的 <code class="code-ref">start()</code> 方法在 AppLauncher 之前重定向 fd，确保 Carb 日志不丢失；<code class="code-ref">_ThrottleState</code> 限流机制防止日志风暴卡死管道，同时保证检测不丢行；<code class="code-ref">_fatal_watchdog_loop</code> 在 CUDA 错误 700 时直接 os._exit(99) 避免主线程死锁。</p>
<p class="audit-callout audit-callout--highlight"><code class="code-ref">src/eval_client/eval_env.py</code> 的 <code class="code-ref">reset()</code> 中通过 <code class="code-ref">seed_manager</code> 管理种子排除已完成/放弃的布局，配合 <code class="code-ref">_align_layout_success</code> 跳过无效环境，实现精细化重试；视频流写入 <code class="code-ref">_stream_vision</code> 使用 ffmpeg 增量保存，避免内存缓冲，并在 episode 结束时永久化。</p>
<p class="audit-callout audit-callout--doubt">代码包中未见任何测试文件（<code class="code-ref">tests/</code> 目录或 <code class="code-ref">*_test.py</code>），核心评估循环的正确性依赖集成测试，可能存在回归风险；<code class="code-ref">src/eval_client/physx_warning_monitor.py</code> 的重连 (<code class="code-ref">_reattach</code>) 在 Kit 频繁更换 fd 时可能仍会漏报。</p>
<p class="audit-callout audit-callout--doubt">关键模块未审阅——实际任务逻辑（如 <code class="code-ref">general_pickup.py</code> 仅包含 reward 定义，本体在 <code class="code-ref">env/</code> 下的 <code class="code-ref">TaskEnv</code> 等未提供源码）导致无法评估任务难度、物理正确性及随机化覆盖；Docker 构建链繁重，依赖特定 CUDA 12.8 + Isaac Sim 5.1，环境一致性存疑。</p>
<p>作为评测工具，建议先在熟悉 Isaac Sim 的团队中试用仿真任务链，利用 <code class="code-ref">scripts/robodojo.sh</code> 快速集成一个已知策略，验证日志监控和恢复效果；真机部分需额外搭建 Piper/ARX 平台。</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>真机任务需特定机器人型号（Piper X, ARX X5），实验室若不采用则只能使用仿真部分。</li><li>仿真运行强依赖 Isaac Sim 和 CUDA 12.8，版本升级可能导致兼容性问题。</li><li>代码中未看到 anti-cheating 机制的具体实现，云评估管道未开源，公信力待验证。</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>有望成为机器人操作领域的“ImageNet”式基准，吸引策略开发者提交结果并竞争榜单，促进学术界与工业界通用策略研发；但依赖 NVIDIA 生态和特定硬件，商业推广受限。</p>
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
  <div class="score-item__value">82</div>
  <div class="score-bar"><span style="width:82%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">工程质量</div>
  <div class="score-item__value">76</div>
  <div class="score-bar"><span style="width:76%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">68</div>
  <div class="score-bar"><span style="width:68%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">77.2</span>
  </div>
</div>
</section>