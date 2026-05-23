from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

import yaml

from .config import Settings
from .models import RepoAudit


class ContentGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def publish(self, audits: list[RepoAudit], *, now: datetime | None = None) -> list[RepoAudit]:
        now = now or datetime.now(UTC)
        publishable = self.select_publishable(audits)
        self.settings.hugo_content_dir.mkdir(parents=True, exist_ok=True)
        self.settings.output_dir.mkdir(parents=True, exist_ok=True)
        for audit in publishable:
            self.write_hugo_post(audit, now)
        self.write_wechat_digest(publishable, now)
        return publishable

    def select_publishable(self, audits: list[RepoAudit]) -> list[RepoAudit]:
        return [
            audit
            for audit in sorted(audits, key=lambda item: item.total_score, reverse=True)
            if audit.total_score >= self.settings.score_threshold
        ][: self.settings.final_publish_limit]

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

## 一句话情报

{audit.summary}

## 解决的工程痛点

{audit.pain_point}

## CTO 级技术审计

{audit.technical_review}

## 隐藏风险与雷点

{_bullet_list(audit.hidden_risks)}

## 生态与商业价值

{audit.commercial_value}

## 四维评分

| 维度 | 分数 |
| --- | ---: |
| 创新度 | {audit.scores.innovation} |
| 实用性 | {audit.scores.utility} |
| 工程质量 | {audit.scores.engineering} |
| 社区健康度 | {audit.scores.health} |
| **RepoIntel 总分** | **{audit.total_score}** |

## 项目链接

[{audit.repo_name}]({audit.repo_link})
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
