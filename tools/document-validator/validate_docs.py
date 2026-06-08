from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_MKDOCS_CONFIG = REPO_ROOT / "mkdocs.yml"

REQUIRED_FRONTMATTER = {
    "id",
    "title",
    "description",
    "type",
    "owner",
    "status",
    "review_cycle",
    "last_reviewed",
    "platform_versions",
    "audience",
    "tags",
    "canonical_url",
}
ALLOWED_TYPES = {
    "overview",
    "environment",
    "constraint",
    "procedure",
    "api-reference",
    "tool-reference",
    "checklist",
    "runbook",
    "changelog",
}
ALLOWED_STATUSES = {"draft", "reviewed", "deprecated"}
ALLOWED_REVIEW_CYCLES = {
    "monthly": {"max_age_days": 31},
    "quarterly": {"max_age_days": 92},
    "release": {"max_age_days": None},
}
ALLOWED_OWNERS = {
    "platform-team",
    "security-team",
    "sre-team",
    "developer-experience",
}
REQUIRED_LIST_FIELDS = {"platform_versions", "audience", "tags"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
CANONICAL_URL_PATTERN = re.compile(r"^/")
CHECKLIST_REFERENCE_PREFIXES = (
    "../constraints/",
    "../procedures/",
    "../environments/",
    "../api-reference/",
    "../tools/",
    "../runbooks/",
)


@dataclass(frozen=True)
class Page:
    path: Path
    relative_path: Path
    metadata: dict[str, Any]
    body: str


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def split_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter blockがありません")
    try:
        _, raw_frontmatter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError("frontmatter blockが閉じられていません") from exc

    metadata = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(metadata, dict):
        raise ValueError("frontmatterはmappingである必要があります")
    return metadata, body


def load_pages(docs_dir: Path) -> list[Page]:
    pages: list[Page] = []
    for path in sorted(docs_dir.rglob("*.md")):
        metadata, body = split_frontmatter(path)
        pages.append(
            Page(
                path=path,
                relative_path=path.relative_to(docs_dir),
                metadata=metadata,
                body=body,
            )
        )
    return pages


def expected_canonical_url(relative_path: Path) -> str:
    if relative_path.as_posix() == "index.md":
        return "/"
    if relative_path.name == "index.md":
        return f"/{relative_path.parent.as_posix()}/"
    return f"/{relative_path.with_suffix('').as_posix()}/"


def expected_id(relative_path: Path) -> str:
    if relative_path.as_posix() == "index.md":
        return "home"
    if relative_path.name == "index.md":
        return f"{relative_path.parent.as_posix().replace('/', '.')}.index"
    return relative_path.with_suffix("").as_posix().replace("/", ".")


def flatten_nav(items: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(items, list):
        for item in items:
            paths.update(flatten_nav(item))
    elif isinstance(items, dict):
        for value in items.values():
            paths.update(flatten_nav(value))
    elif isinstance(items, str):
        paths.add(items)
    return paths


def markdown_links(body: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", body)


def is_external_or_anchor(link: str) -> bool:
    return (
        link.startswith("http://")
        or link.startswith("https://")
        or link.startswith("mailto:")
        or link.startswith("#")
    )


def validate_page(
    page: Page,
    today: date,
    nav_paths: set[str],
) -> list[str]:
    errors: list[str] = []
    metadata = page.metadata
    path_label = page.path.as_posix()

    missing = sorted(REQUIRED_FRONTMATTER - set(metadata))
    for field in missing:
        errors.append(f"{path_label}: frontmatter.{field} がありません")

    if missing:
        return errors

    doc_id = str(metadata["id"])
    if not ID_PATTERN.match(doc_id):
        errors.append(f"{path_label}: id '{doc_id}' がpattern {ID_PATTERN.pattern} に一致しません")

    expected_doc_id = expected_id(page.relative_path)
    if doc_id != expected_doc_id:
        errors.append(f"{path_label}: idは '{expected_doc_id}' にしてください")

    title = metadata["title"]
    if not isinstance(title, str) or not title.strip():
        errors.append(f"{path_label}: titleは空でない文字列にしてください")

    description = metadata["description"]
    if not isinstance(description, str) or len(description.strip()) < 10:
        errors.append(f"{path_label}: descriptionは10文字以上の説明文にしてください")

    doc_type = metadata["type"]
    if doc_type not in ALLOWED_TYPES:
        errors.append(f"{path_label}: type '{doc_type}' は許可されていません")

    owner = metadata["owner"]
    if owner not in ALLOWED_OWNERS:
        errors.append(f"{path_label}: owner '{owner}' はvalidatorに定義されていません")

    status = metadata["status"]
    if status not in ALLOWED_STATUSES:
        errors.append(f"{path_label}: status '{status}' は許可されていません")

    review_cycle = metadata["review_cycle"]
    if review_cycle not in ALLOWED_REVIEW_CYCLES:
        errors.append(f"{path_label}: review_cycle '{review_cycle}' は許可されていません")
    else:
        errors.extend(validate_review_date(path_label, metadata["last_reviewed"], ALLOWED_REVIEW_CYCLES[review_cycle], today))

    for field in REQUIRED_LIST_FIELDS:
        value = metadata[field]
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
            errors.append(f"{path_label}: {field} は空でない文字列listにしてください")

    canonical_url = metadata["canonical_url"]
    if not isinstance(canonical_url, str) or not CANONICAL_URL_PATTERN.match(canonical_url):
        errors.append(f"{path_label}: canonical_urlは '/' で始めてください")

    expected_url = expected_canonical_url(page.relative_path)
    if canonical_url != expected_url:
        errors.append(f"{path_label}: canonical_urlは '{expected_url}' にしてください")

    if status == "deprecated" and not metadata.get("replaced_by"):
        errors.append(f"{path_label}: deprecated pageには replaced_by を指定してください")

    if page.relative_path.as_posix() not in nav_paths:
        errors.append(f"{path_label}: mkdocs.yml の nav に含まれていません")

    h1_matches = re.findall(r"^#\s+(.+)$", page.body, flags=re.MULTILINE)
    if len(h1_matches) != 1:
        errors.append(f"{path_label}: H1は1つだけにしてください")
    elif h1_matches[0].strip() != title.strip():
        errors.append(f"{path_label}: H1 '{h1_matches[0].strip()}' と title '{title.strip()}' を一致させてください")

    if page.relative_path.name != "index.md" and doc_type == "checklist":
        errors.extend(validate_checklist_references(page))

    errors.extend(validate_internal_markdown_links(page))
    return errors


def validate_review_date(path_label: str, raw_date: Any, cycle_rule: dict[str, Any], today: date) -> list[str]:
    errors: list[str] = []
    if isinstance(raw_date, date):
        reviewed = raw_date
    else:
        try:
            reviewed = datetime.strptime(str(raw_date), "%Y-%m-%d").date()
        except ValueError:
            return [f"{path_label}: last_reviewedはYYYY-MM-DD形式にしてください"]

    if reviewed > today:
        errors.append(f"{path_label}: last_reviewedが未来日です")

    max_age_days = cycle_rule.get("max_age_days")
    if max_age_days is not None and (today - reviewed).days > int(max_age_days):
        errors.append(f"{path_label}: last_reviewedがreview_cycleの期限を超えています")

    return errors


def validate_checklist_references(page: Page) -> list[str]:
    errors: list[str] = []
    table_rows = [
        line
        for line in page.body.splitlines()
        if line.startswith("|") and "---" not in line and "チェック" not in line and "Check" not in line
    ]

    for row in table_rows:
        links = markdown_links(row)
        if not links:
            errors.append(f"{page.path.as_posix()}: checklist rowに正本ドキュメントへのlinkがありません: {row}")
            continue
        if not any(link.startswith(CHECKLIST_REFERENCE_PREFIXES) for link in links):
            errors.append(f"{page.path.as_posix()}: checklist rowのlinkは正本カテゴリを参照してください: {row}")

    return errors


def validate_internal_markdown_links(page: Page) -> list[str]:
    errors: list[str] = []
    for link in markdown_links(page.body):
        target = link.split("#", 1)[0]
        if not target or is_external_or_anchor(target):
            continue
        if target.startswith("/"):
            continue
        if not target.endswith(".md"):
            continue
        resolved = (page.path.parent / target).resolve()
        try:
            resolved.relative_to(DEFAULT_DOCS_DIR.resolve())
        except ValueError:
            errors.append(f"{page.path.as_posix()}: docs外へのlinkです: {link}")
            continue
        if not resolved.exists():
            errors.append(f"{page.path.as_posix()}: link先が存在しません: {link}")
    return errors


def validate_uniqueness(pages: list[Page]) -> list[str]:
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}
    seen_urls: dict[str, Path] = {}

    for page in pages:
        doc_id = str(page.metadata.get("id", ""))
        canonical_url = str(page.metadata.get("canonical_url", ""))

        if doc_id in seen_ids:
            errors.append(f"{page.path.as_posix()}: id '{doc_id}' が {seen_ids[doc_id].as_posix()} と重複しています")
        seen_ids[doc_id] = page.path

        if canonical_url in seen_urls:
            errors.append(f"{page.path.as_posix()}: canonical_url '{canonical_url}' が {seen_urls[canonical_url].as_posix()} と重複しています")
        seen_urls[canonical_url] = page.path

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate platform documentation rules.")
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--mkdocs-config", type=Path, default=DEFAULT_MKDOCS_CONFIG)
    parser.add_argument("--today", default=date.today().isoformat(), help="YYYY-MM-DD. CIで検証日を固定したい場合に使う。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mkdocs_config = load_yaml(args.mkdocs_config)
    nav_paths = flatten_nav(mkdocs_config.get("nav", []))
    today = datetime.strptime(args.today, "%Y-%m-%d").date()

    errors: list[str] = []
    try:
        pages = load_pages(args.docs_dir)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for page in pages:
        errors.extend(validate_page(page, today, nav_paths))
    errors.extend(validate_uniqueness(pages))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"document validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(f"document validation passed: {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
