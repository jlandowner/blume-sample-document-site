# MCP tools

`docs.search` はpage単位の検索に使います。検索結果には `page_id`、page metadata、`matched_sections` が含まれます。

`docs.get_page` は `page_id` を指定してMarkdown正本を取得するために使います。

MCP serverの内部実装は `/ai/docs-index.json`、`/ai/chunks.jsonl`、`/ai/source/docs/*.md` を読みます。
