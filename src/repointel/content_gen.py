from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from pathlib import Path

import yaml

from .config import Settings
from .legacy_guard import is_blocked_repo_name
from .models import RepoAudit

LOGGER = logging.getLogger(__name__)


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
        body = f"""---
{front_matter}
---

<div class="content-panel">

## 审读源码范围

- 代码来源：**{audit.code_source or "unknown"}**
- 审读文件数：**{len(audit.code_files_reviewed)}**（约 {audit.code_chars_analyzed} 字符）
- 主要路径：{", ".join(audit.code_files_reviewed[:12])}{" …" if len(audit.code_files_reviewed) > 12 else ""}

## 一句话情报

{audit.summary}

</div>

<div class="content-panel">

## 解决的工程痛点

{audit.pain_point}

</div>

<div class="content-panel">

## CTO 级技术审计

{audit.technical_review}

</div>

<div class="content-panel">

## 隐藏风险与雷点

{_bullet_list(audit.hidden_risks)}

</div>

<div class="content-panel">

## 生态与商业价值

{audit.commercial_value}

</div>

<div class="content-panel">

## 四维评分

<div class="score-grid">
  <div class="score-item">
    <div class="score-item__label">创新度</div>
    <div class="score-item__value">{audit.scores.innovation}</div>
    <div class="score-bar"><span style="width:{audit.scores.innovation}%"></span></div>
  </div>
  <div class="score-item">
    <div class="score-item__label">实用性</div>
    <div class="score-item__value">{audit.scores.utility}</div>
    <div class="score-bar"><span style="width:{audit.scores.utility}%"></span></div>
  </div>
  <div class="score-item">
    <div class="score-item__label">工程质量</div>
    <div class="score-item__value">{audit.scores.engineering}</div>
    <div class="score-bar"><span style="width:{audit.scores.engineering}%"></span></div>
  </div>
  <div class="score-item">
    <div class="score-item__label">社区健康度</div>
    <div class="score-item__value">{audit.scores.health}</div>
    <div class="score-bar"><span style="width:{audit.scores.health}%"></span></div>
  </div>
</div>

**RepoIntel 总分：{audit.total_score}**

</div>
"""
        path.write_text(body, encoding="utf-8")
        return path

    def write_wechat_digest(self, audits: list[RepoAudit], published_at: datetime) -> Path:
        path = self.settings.output_dir / "wechat_digest.txt"
        if not audits:
            content = (
                f"RepoIntel 开源情报局 · {published_at.date().isoformat()}\n\n"
                "今日没有项目通过 75 分硬核审计线。宁缺毋滥，明天再看。\n"
            )
            path.write_text(content, encoding="utf-8")
            return path

        lines = [
            f"RepoIntel 开源情报局 · {published_at.date().isoformat()}",
            "",
            "今日原则：宁缺毋滥，去伪存真。以下项目通过硬指标过滤与 AI 架构审计。",
            "",
            f"今日入选：{len(audits)} 个项目",
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


def _slugify(value: str) -> str:
    slug = value.lower().replace("/", "-")
    slug = re.sub(r"[^a-z0-9._-]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-._")
    return slug or "repo"


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "- 暂无明确风险，但仍建议人工复核。"
    return "\n".join(f"- {item}" for item in items)
