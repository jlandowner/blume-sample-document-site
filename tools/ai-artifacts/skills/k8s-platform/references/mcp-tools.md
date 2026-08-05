# MCP tools

`search_docs` はpage単位の検索に使います。検索結果には `route`、`title`、`excerpt`、`url` が含まれます。

`get_page` は `route` を指定してMarkdown正本を取得するために使います。

MCP serverはBlume内蔵MCP serverを使います。ブラウザ検索と同じBlumeのOrama検索を使うため、日本語検索には `blume.config.ts` の `i18n.defaultLocale: "ja"` が必要です。
