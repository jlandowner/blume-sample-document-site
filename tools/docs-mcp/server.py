from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP


@dataclass
class Store:
    ai_dir: Path
    index: list[dict[str, Any]]
    chunks: list[dict[str, Any]]
    pages: dict[str, str]


def load_store(ai_dir: Path) -> Store:
    index = json.loads((ai_dir / "docs-index.json").read_text(encoding="utf-8"))
    chunks = [
        json.loads(line)
        for line in (ai_dir / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    pages: dict[str, str] = {}
    for page in index:
        source_path = ai_dir / "source" / page["source_path"]
        pages[page["id"]] = source_path.read_text(encoding="utf-8")
    return Store(ai_dir=ai_dir, index=index, chunks=chunks, pages=pages)


def normalize_terms(query: str) -> list[str]:
    return [term for term in re.split(r"\s+", query.lower().strip()) if term]


def score_text(terms: list[str], text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(term) for term in terms)


def excerpt_text(text: str, max_length: int = 240) -> str:
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= max_length:
        return normalized
    return normalized[: max_length - 3].rstrip() + "..."


def create_server(store: Store) -> FastMCP:
    mcp = FastMCP("k8s-platform-docs")

    @mcp.resource("docs://index")
    def docs_index() -> str:
        """page単位のmetadata indexを返します。"""
        return json.dumps(store.index, ensure_ascii=False, indent=2)

    @mcp.resource("docs://llms")
    def docs_llms() -> str:
        """LLM向けの軽量ドキュメント索引を返します。"""
        return (store.ai_dir / "llms.txt").read_text(encoding="utf-8")

    @mcp.resource("docs://skill/k8s-platform")
    def docs_skill() -> str:
        """K8s platform docs skillの入口を返します。"""
        return (store.ai_dir / "skills" / "k8s-platform" / "SKILL.md").read_text(encoding="utf-8")

    @mcp.resource("docs://page/{page_id}")
    def docs_page_resource(page_id: str) -> str:
        """page idを指定してMarkdown正本を返します。"""
        if page_id not in store.pages:
            raise ValueError(f"unknown page: {page_id}")
        return store.pages[page_id]

    @mcp.tool(name="docs.search")
    def docs_search(query: str, type: str | None = None, tags: list[str] | None = None, limit: int = 10) -> dict[str, Any]:
        """K8sプラットフォームドキュメントをpage単位でkeyword検索します。"""
        terms = normalize_terms(query)
        requested_tags = set(tags or [])
        pages_by_id = {page["id"]: page for page in store.index}
        results_by_page: dict[str, dict[str, Any]] = {}

        def result_for_page(page: dict[str, Any]) -> dict[str, Any]:
            return results_by_page.setdefault(
                page["id"],
                {
                    "page_id": page["id"],
                    "score": 0,
                    "metadata": page,
                    "matched_sections": [],
                },
            )

        for page in store.index:
            if type and page["type"] != type:
                continue
            if requested_tags and not requested_tags.issubset(set(page["tags"])):
                continue
            haystack = " ".join([page["title"], page["description"], page["type"], " ".join(page["tags"])])
            score = score_text(terms, haystack)
            if score:
                result = result_for_page(page)
                result["score"] += score
                result["matched_sections"].append(
                    {
                        "kind": "page_metadata",
                        "score": score,
                        "heading_path": [],
                        "excerpt": page["description"],
                        "canonical_url": page["canonical_url"],
                    }
                )

        for chunk in store.chunks:
            if type and chunk["type"] != type:
                continue
            if requested_tags and not requested_tags.issubset(set(chunk["tags"])):
                continue
            page = pages_by_id.get(chunk["page_id"])
            if page is None:
                continue
            haystack = " ".join([chunk["title"], " ".join(chunk["heading_path"]), chunk["text"], " ".join(chunk["tags"])])
            score = score_text(terms, haystack)
            if score:
                result = result_for_page(page)
                result["score"] += score
                result["matched_sections"].append(
                    {
                        "kind": "chunk",
                        "score": score,
                        "chunk_id": chunk["chunk_id"],
                        "heading_path": chunk["heading_path"],
                        "excerpt": excerpt_text(chunk["text"]),
                        "canonical_url": chunk["canonical_url"],
                    }
                )

        results = list(results_by_page.values())
        for result in results:
            result["matched_sections"].sort(key=lambda section: section["score"], reverse=True)
        results.sort(key=lambda result: result["score"], reverse=True)
        return {"query": query, "results": results[:limit]}

    @mcp.tool(name="docs.get_page")
    def docs_get_page(id: str) -> dict[str, Any]:
        """page idを指定してMarkdown正本を取得します。"""
        page = next((item for item in store.index if item["id"] == id), None)
        if page is None or id not in store.pages:
            raise ValueError(f"unknown page: {id}")
        return {"metadata": page, "markdown": store.pages[id]}

    return mcp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MCP server for K8s platform docs.")
    parser.add_argument("--ai-dir", type=Path, default=Path(os.environ.get("AI_DIR", "ai")))
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default=os.environ.get("MCP_TRANSPORT", "stdio"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store = load_store(args.ai_dir)
    server = create_server(store)
    server.run(transport=args.transport)


if __name__ == "__main__":
    main()
