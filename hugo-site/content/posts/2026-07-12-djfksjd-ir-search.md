---
title: '[Score: 76.5] djfksjd/ir-search'
date: '2026-07-12T13:13:28Z'
categories:
- Developer Tools / Government Tech
tags:
- python
- crawler
- claude-code
- startup
- korea
- government-grants
intel_score: 76.5
repo_name: djfksjd/ir-search
repo_link: https://github.com/djfksjd/ir-search
summary: 한국 정부 지원사업을 전수 크롤링하여 Claude Code가 프로젝트에 맞춰 A/B/C 3단계로 분류·보고하는 스킬. 키워드 검색의
  사각지대를 해소하며, 재조사 시 diff 모드로 증분 보고해 반복 작업 피로를 낮춘다.
code_source: git
code_files_reviewed:
- scripts/diff_surveys.py
- references/sources.md
- README.md
- README.en.md
- scripts/kstartup_crawl.py
- SKILL.md
- scripts/sources_crawl.py
code_chars_analyzed: 43876
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
      <span class="scope-stat__value">7 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 43,876 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  <ul class="path-list"><li><code class="path-chip">scripts/diff_surveys.py</code></li><li><code class="path-chip">references/sources.md</code></li><li><code class="path-chip">README.md</code></li><li><code class="path-chip">README.en.md</code></li><li><code class="path-chip">scripts/kstartup_crawl.py</code></li><li><code class="path-chip">SKILL.md</code></li><li><code class="path-chip">scripts/sources_crawl.py</code></li></ul>
</div>
</section>

<section class="content-panel content-panel--pain" id="pain">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◎</span>
  <h2 class="panel-title">解决的工程痛点</h2>
</header>
<div class="panel-body prose">
<p>한국 예비·초기 창업자가 K-Startup·기업마당 등에 산재한 수백 건의 공고를 수작업으로 찾고, “AI 스타트업”이 지원할 수 있는 콘텐츠·사회서비스 분야 숨은 기회를 놓치며, 자격요건 검증에 실패하는 문제.</p>
</div>
</section>

<section class="content-panel content-panel--audit" id="audit">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚙</span>
  <h2 class="panel-title">CTO 级技术审计</h2>
</header>
<div class="panel-body prose">
<p class="audit-callout audit-callout--intro">SKILL.md에 정의된 워크플로를 따라 scripts/의 크롤러가 공고를 수집하고, Claude가 전체 목록을 읽어 프로필과 매칭·분류한 뒤 상세검증을 거쳐 보고서를 생성한다. 재조사 시 <code class="code-ref">scripts/diff_surveys.py:20</code>-35의 load_dir이 이전/현재 jsonl을 (source, id)로 비교해 신규·마감·변경만 추출, 나머지는 판정을 승계한다.</p>
<p class="audit-callout audit-callout--highlight">TLS 지문 차단을 우회하기 위한 이중 fetch 백엔드 – <code class="code-ref">scripts/kstartup_crawl.py:21</code>-50의 make_fetcher()가 curl_cffi(Safari impersonate)를 우선 사용하고, 미설치 시 urllib로 폴백하며 차단 시 힌트를 출력한다.</p>
<p class="audit-callout audit-callout--highlight">비정규 키워드 매칭 문제를 해결한 전수 검토 접근 – SKILL.md:54-62에서 “AI 스타트업”이 콘텐츠 제작지원·예술×기술 입주 등 키워드로 잡히지 않는 사각지대를 언급하며, 크롤링 후 LLM이 전체 제목을 직접 읽어 변형 가능성까지 포착하도록 설계했다.</p>
<p class="audit-callout audit-callout--doubt">모든 파서가 정규표현식과 HTML 구조에 의존함 – <code class="code-ref">scripts/kstartup_crawl.py:94</code>-130의 parse_list는 &lt;li class=&quot;notice&quot;&gt; 등 마크업에 강하게 결합되어 있고, <code class="code-ref">scripts/sources_crawl.py:170</code>의 page_smtech 등도 유사하여 사이트 개편 시 즉시 파손될 위험이 크다.</p>
<p class="audit-callout audit-callout--doubt">테스트 코드 및 CI 구성이 전무함 – code_bundle에 tests/ 디렉터리나 *_test.py 파일이 존재하지 않으며, <code class="code-ref">scripts/diff_surveys.py:38</code>의 load_dir에서 json decode 실패를 continue로 넘기는 등 경계 조건 검증이 부족하다.</p>
<p>크롤러의 지속적 작동을 위해 주요 사이트 HTML 변경을 감지하는 스모크 테스트를 도입하고, 공고 데이터를 로컬 DB에 저장해 오프라인 검색·통계 기능을 추가하면 실용성이 높아진다.</p>
</div>
</section>

<section class="content-panel content-panel--risk" id="risk">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⚠</span>
  <h2 class="panel-title">隐藏风险与雷点</h2>
</header>
<div class="panel-body prose">
<ul class="risk-list"><li>대상 사이트의 robots.txt 및 이용약관 준수 의무; 공격적 크롤링 시 법적 분쟁 가능</li><li>curl_cffi 미설치 시 urllib fallback이 TLS 차단에 취약해 크롤링 실패 가능</li><li>LLM 분류 오류로 인한 부적격 공고 추천 시 사용자 신뢰 손상</li><li>summary 过长，可能含废话</li></ul>
</div>
</section>

<section class="content-panel content-panel--value" id="value">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">◈</span>
  <h2 class="panel-title">生态与商业价值</h2>
</header>
<div class="panel-body prose">
<p>정부 지원사업 탐색 대행/컨설팅 업체의 내부 도구로 활용 가능하며, 스타트업 액셀러레이터의 멤버십 부가 서비스로 공급할 수 있는 실용적 가치.</p>
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
  <div class="score-item__value">72</div>
  <div class="score-bar"><span style="width:72%"></span></div>
</div>
    <div class="score-item">
  <div class="score-item__label">社区健康度</div>
  <div class="score-item__value">70</div>
  <div class="score-bar"><span style="width:70%"></span></div>
</div>
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">76.5</span>
  </div>
</div>
</section>