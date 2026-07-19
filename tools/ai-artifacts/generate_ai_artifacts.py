from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "ai"
DEFAULT_SKILLS_DIR = Path(__file__).resolve().parent / "skills"
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Page:
    path: Path
    relative_path: Path
    metadata: dict[str, Any]
    body: str


def split_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    _, raw_frontmatter, body = text.split("---\n", 2)
    metadata = yaml.safe_load(raw_frontmatter) or {}
    return metadata, body.strip() + "\n"


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


def anchorize(text: str) -> str:
    value = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    value = re.sub(r"\s+", "-", value.strip())
    return value or "section"


def extract_headings(body: str) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for match in HEADING_PATTERN.finditer(body):
        text = match.group(2).strip()
        headings.append(
            {
                "level": len(match.group(1)),
                "text": text,
                "anchor": anchorize(text),
            }
        )
    return headings


def page_record(page: Page) -> dict[str, Any]:
    data = page.metadata
    source_path = f"docs/{page.relative_path.as_posix()}"
    return {
        "id": data["id"],
        "title": data["title"],
        "description": data["description"],
        "type": data["type"],
        "source_path": source_path,
        "source_url": f"/ai/source/{source_path}",
        "canonical_url": data["canonical_url"],
        "owner": data["owner"],
        "status": data["status"],
        "review_cycle": data["review_cycle"],
        "last_reviewed": str(data["last_reviewed"]),
        "platform_versions": data["platform_versions"],
        "audience": data["audience"],
        "tags": data["tags"],
        "headings": extract_headings(page.body),
        "mcp_resource": f"docs://page/{data['id']}",
    }


def section_chunks(page: Page) -> list[dict[str, Any]]:
    data = page.metadata
    matches = list(HEADING_PATTERN.finditer(page.body))
    if not matches:
        return []

    chunks: list[dict[str, Any]] = []
    heading_stack: list[tuple[int, str]] = []
    used_chunk_ids: dict[str, int] = {}

    for index, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(2).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(page.body)
        text = page.body[start:end].strip()

        heading_stack = [(stack_level, stack_heading) for stack_level, stack_heading in heading_stack if stack_level < level]
        heading_stack.append((level, heading))
        heading_path = [stack_heading for _, stack_heading in heading_stack]

        anchor = anchorize(heading)
        base_chunk_id = f"{data['id']}#{anchor}"
        duplicate_count = used_chunk_ids.get(base_chunk_id, 0)
        used_chunk_ids[base_chunk_id] = duplicate_count + 1
        chunk_id = base_chunk_id if duplicate_count == 0 else f"{base_chunk_id}-{duplicate_count + 1}"

        chunks.append(
            {
                "page_id": data["id"],
                "chunk_id": chunk_id,
                "title": data["title"],
                "heading_path": heading_path,
                "text": text,
                "type": data["type"],
                "owner": data["owner"],
                "status": data["status"],
                "audience": data["audience"],
                "tags": data["tags"],
                "source_path": f"docs/{page.relative_path.as_posix()}",
                "canonical_url": f"{data['canonical_url'].rstrip('/')}/#{anchor}",
            }
        )
    return chunks


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def write_llms_txt(output_dir: Path, pages: list[Page]) -> None:
    lines = [
        "# K8sプラットフォームドキュメント",
        "",
        "社内Kubernetesプラットフォームの環境、制約、手順、API、ツール、チェックリスト、ランブックをまとめたドキュメントです。",
        "AIエージェントは必要に応じてMCP toolsを使い、該当pageを検索・取得してください。",
        "",
    ]

    pages_by_type: dict[str, list[Page]] = {}
    for page in pages:
        pages_by_type.setdefault(page.metadata["type"], []).append(page)

    for page_type in sorted(pages_by_type):
        lines.append(f"## {page_type}")
        lines.append("")
        for page in pages_by_type[page_type]:
            data = page.metadata
            lines.append(f"- [{data['title']}]({data['canonical_url']}): {data['description']} (`docs://page/{data['id']}`)")
        lines.append("")

    (output_dir / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def write_llms_full_txt(output_dir: Path, pages: list[Page]) -> None:
    parts = ["# K8sプラットフォームドキュメント全文", ""]
    for page in pages:
        data = page.metadata
        parts.append(f"<!-- source: docs/{page.relative_path.as_posix()} id: {data['id']} resource: docs://page/{data['id']} -->")
        parts.append(page.body.strip())
        parts.append("")
    (output_dir / "llms-full.txt").write_text("\n".join(parts), encoding="utf-8")


def write_source_docs(output_dir: Path, docs_dir: Path) -> None:
    source_docs_dir = output_dir / "source" / "docs"
    shutil.copytree(docs_dir, source_docs_dir)


def copy_skills(output_dir: Path, skills_dir: Path) -> None:
    shutil.copytree(skills_dir, output_dir / "skills")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate AI artifacts from platform docs.")
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--skills-dir", type=Path, default=DEFAULT_SKILLS_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True)

    pages = load_pages(args.docs_dir)
    index = [page_record(page) for page in pages]
    chunks = [chunk for page in pages for chunk in section_chunks(page)]

    write_json(args.output_dir / "docs-index.json", index)
    write_jsonl(args.output_dir / "chunks.jsonl", chunks)
    write_source_docs(args.output_dir, args.docs_dir)
    write_llms_txt(args.output_dir, pages)
    write_llms_full_txt(args.output_dir, pages)
    copy_skills(args.output_dir, args.skills_dir)

    print(f"generated AI artifacts: {len(index)} pages, {len(chunks)} chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
