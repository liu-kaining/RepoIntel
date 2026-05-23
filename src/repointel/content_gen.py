from __future__ import annotations

import html
import logging
import re
from datetime import UTC, datetime
from pathlib import Path

import yaml

from .config import Settings
from .legacy_guard import is_blocked_repo_name
from .models import RepoAudit

LOGGER = logging.getLogger(__name__)

_FILE_EXTENSIONS = r"(?:rs|py|go|ts|tsx|js|java|toml|yaml|yml|md|json|mod)"
_AUDIT_HEADER_RE = re.compile(
    r"(?:^|\n)\s*(?:【|\*\*)?"
    r"(架构与核心链路|亮点\s*\d*|亮点|疑点\s*\d*|疑点|雷点\s*\d*|雷点|疑点/雷点|落地建议|不足与限制)"
    r"(?:\*\*|】)?\s*[：:]\s*",
    re.IGNORECASE,
)
_CODE_REF_RE = re.compile(
    rf"`([^`]+)`"
    rf"|((?:[\w.-]+/)+[\w.-]+\.{_FILE_EXTENSIONS}|cmd/[\w./-]+\.{_FILE_EXTENSIONS})"
    rf"(?:\s*[:：]\s*(\d+))?",
)


class ContentGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish(self, audits: list[RepoAudit], *, now: datetime | None = None) -> list[RepoAudit]:
        now = now or datetime.now(UTC)
        publishable = self.select_publishable(audits)
        LOGGER.info(
            "Content generation selected %d publishable entries from %d audits",
            len(publishable),
            len(audits),
        )
        self.settings.hugo_content_dir.mkdir(parents=True, exist_ok=True)
        self.settings.output_dir.mkdir(parents=True, exist_ok=True)
        for audit in publishable:
            post_path = self.write_hugo_post(audit, now)
            LOGGER.info("Wrote Hugo post %s -> score=%s", post_path.name, audit.total_score)
        digest_path = self.write_wechat_digest(publishable, now)
        LOGGER.info("Wrote WeChat digest -> %s with %d entries", digest_path, len(publishable))
        return publishable

    def select_publishable(self, audits: list[RepoAudit]) -> list[RepoAudit]:
        publishable: list[RepoAudit] = []
        for audit in sorted(audits, key=lambda item: item.total_score, reverse=True):
            if is_blocked_repo_name(audit.repo_name):
                LOGGER.warning("Skipping blocklisted repo %s", audit.repo_name)
                continue
            if audit.total_score < self.settings.score_threshold:
                continue
            publishable.append(audit)
            if len(publishable) >= self.settings.final_publish_limit:
                break
        return publishable

    def write_hugo_post(self, audit: RepoAudit, published_at: datetime) -> Path:
        slug = _slugify(audit.repo_name)
        date_prefix = published_at.date().isoformat()
        path = self.settings.hugo_content_dir / f"{date_prefix}-{slug}.md"
        front_matter = yaml.safe_dump(
            audit.to_front_matter(published_at),
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        ).strip()
        body = _render_post_body(audit)
        path.write_text(f"---\n{front_matter}\n---\n\n{body}", encoding="utf-8")
        return path

    def write_wechat_digest(self, audits: list[RepoAudit], published_at: datetime) -> Path:
        path = self.settings.output_dir / "wechat_digest.txt"
        if not audits:
            content = (
                f"RepoIntel 开源情报局 · {published_at.date().isoformat()}\n\n"
                "今日没有项目通过 75 分源码审计线。宁缺毋滥，明天再看。\n"
            )
            path.write_text(content, encoding="utf-8")
            return path

        lines = [
            f"RepoIntel 开源情报局 · {published_at.date().isoformat()}",
            "",
            "今日原则：宁缺毋滥，去伪存真。以下项目通过硬指标过滤与读码架构审计。",
            "",
        ]
        for index, audit in enumerate(audits, start=1):
            lines.extend(
                [
                    f"{index}. {audit.repo_name}",
                    f"RepoIntel 总分：{audit.total_score}",
                    f"分类：{audit.category}",
                    f"标签：{', '.join(audit.tags)}",
                    f"一句话：{audit.summary}",
                    f"痛点：{audit.pain_point}",
                    "毒舌审计：",
                    audit.technical_review,
                    "隐藏风险：",
                    *[f"- {risk}" for risk in audit.hidden_risks],
                    f"链接：{audit.repo_link}",
                    "",
                    "---",
                    "",
                ]
            )
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        return path


def _render_post_body(audit: RepoAudit) -> str:
    sections = [
        _scope_panel(audit),
        _panel("pain", "解决的工程痛点", _format_prose(audit.pain_point)),
        _panel("audit", "CTO 级技术审计", _format_prose(audit.technical_review, rich=True)),
        _panel("risk", "隐藏风险与雷点", _risk_list(audit.hidden_risks)),
        _panel("value", "生态与商业价值", _format_prose(audit.commercial_value)),
        _scores_panel(audit),
    ]
    return "\n\n".join(sections)


def _panel(panel_id: str, title: str, inner_html: str) -> str:
    icon = _PANEL_ICONS.get(panel_id, "◆")
    return f"""<section class="content-panel content-panel--{panel_id}" id="{panel_id}">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">{icon}</span>
  <h2 class="panel-title">{html.escape(title)}</h2>
</header>
<div class="panel-body prose">
{inner_html}
</div>
</section>"""


_PANEL_ICONS = {
    "scope": "⌁",
    "pain": "◎",
    "audit": "⚙",
    "risk": "⚠",
    "value": "◈",
    "scores": "▣",
}


def _scope_panel(audit: RepoAudit) -> str:
    file_count = len(audit.code_files_reviewed)
    chars = audit.code_chars_analyzed
    chars_label = f"{chars:,}" if chars else "—"
    paths = _path_list(audit.code_files_reviewed)
    return f"""<section class="content-panel content-panel--scope" id="scope">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">⌁</span>
  <h2 class="panel-title">审读源码范围</h2>
</header>
<div class="panel-body">
  <div class="scope-stats">
    <div class="scope-stat">
      <span class="scope-stat__label">代码来源</span>
      <span class="scope-stat__value">{html.escape(audit.code_source or "unknown")}</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">审读文件</span>
      <span class="scope-stat__value">{file_count} 个</span>
    </div>
    <div class="scope-stat">
      <span class="scope-stat__label">采样体量</span>
      <span class="scope-stat__value">约 {chars_label} 字符</span>
    </div>
  </div>
  <p class="path-list-label">主要路径</p>
  {paths}
</div>
</section>"""


def _path_list(files: tuple[str, ...]) -> str:
    if not files:
        return '<p class="path-empty">本次未采集到有效源码路径。</p>'
    visible = list(files[:14])
    items = "".join(
        f'<li><code class="path-chip">{html.escape(path)}</code></li>' for path in visible
    )
    extra = ""
    if len(files) > len(visible):
        extra = f'<li class="path-more">另有 {len(files) - len(visible)} 个文件未展示</li>'
    return f'<ul class="path-list">{items}{extra}</ul>'


def _scores_panel(audit: RepoAudit) -> str:
    return f"""<section class="content-panel content-panel--scores" id="scores">
<header class="panel-head">
  <span class="panel-icon" aria-hidden="true">▣</span>
  <h2 class="panel-title">四维评分</h2>
</header>
<div class="panel-body">
  <div class="score-grid">
    {_score_item("创新度", audit.scores.innovation)}
    {_score_item("实用性", audit.scores.utility)}
    {_score_item("工程质量", audit.scores.engineering)}
    {_score_item("社区健康度", audit.scores.health)}
  </div>
  <div class="total-score-banner">
    <span class="total-score-banner__label">RepoIntel 总分</span>
    <span class="total-score-banner__value">{audit.total_score}</span>
  </div>
</div>
</section>"""


def _score_item(label: str, value: float) -> str:
    width = max(0, min(100, int(value)))
    return f"""<div class="score-item">
  <div class="score-item__label">{html.escape(label)}</div>
  <div class="score-item__value">{value}</div>
  <div class="score-bar"><span style="width:{width}%"></span></div>
</div>"""


def _risk_list(items: list[str]) -> str:
    if not items:
        return '<ul class="risk-list"><li>暂无明确风险，但仍建议人工复核。</li></ul>'
    rows = "".join(f"<li>{_inline_code(html.escape(item))}</li>" for item in items)
    return f'<ul class="risk-list">{rows}</ul>'


def _format_prose(text: str, *, rich: bool = False) -> str:
    cleaned = text.strip()
    if not cleaned:
        return "<p>暂无内容。</p>"
    if rich:
        return _format_audit_prose(cleaned)
    chunks = [part.strip() for part in re.split(r"\n\s*\n", cleaned) if part.strip()]
    if not chunks:
        chunks = [cleaned]
    return "\n".join(f"<p>{_inline_code(html.escape(chunk))}</p>" for chunk in chunks if chunk)


def _format_audit_prose(text: str) -> str:
    sections = _split_audit_sections(text)
    parts: list[str] = []
    for kind, body in sections:
        if not body:
            continue
        css = _callout_class(kind)
        escaped = html.escape(body)
        inner = _inline_code(escaped)
        if css:
            parts.append(f'<p class="{css}">{inner}</p>')
        else:
            parts.append(f"<p>{inner}</p>")
    return "\n".join(parts) if parts else "<p>暂无内容。</p>"


def _split_audit_sections(text: str) -> list[tuple[str, str]]:
    matches = list(_AUDIT_HEADER_RE.finditer(text))
    if not matches:
        return [("default", text)]

    sections: list[tuple[str, str]] = []
    cursor = 0
    for index, match in enumerate(matches):
        if match.start() > cursor:
            preamble = text[cursor : match.start()].strip()
            if preamble:
                kind = "intro" if index == 0 else "default"
                sections.append((kind, preamble))
        label = match.group(1)
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()
        if body:
            sections.append((_section_kind(label), body))
        cursor = body_end
    return sections or [("default", text)]


def _section_kind(label: str) -> str:
    normalized = re.sub(r"\s+", "", label.lower())
    if normalized.startswith("亮点") or normalized.startswith("highlight"):
        return "highlight"
    if any(normalized.startswith(prefix) for prefix in ("疑点", "雷点", "doubt", "风险")):
        return "doubt"
    if normalized.startswith("架构"):
        return "intro"
    return "default"


def _callout_class(kind: str) -> str:
    if kind == "highlight":
        return "audit-callout audit-callout--highlight"
    if kind == "doubt":
        return "audit-callout audit-callout--doubt"
    if kind == "intro":
        return "audit-callout audit-callout--intro"
    return ""


def _inline_code(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        if match.group(1):
            return f'<code class="code-ref">{match.group(1)}</code>'
        path = match.group(2)
        line = match.group(3)
        label = path if not line else f"{path}:{line}"
        return f'<code class="code-ref">{label}</code>'

    return _CODE_REF_RE.sub(repl, text)


def _slugify(value: str) -> str:
    slug = value.lower().replace("/", "-")
    slug = re.sub(r"[^a-z0-9._-]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "repo"
