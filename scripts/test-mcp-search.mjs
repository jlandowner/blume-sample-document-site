import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";

/*
 * Blume の MCP search 動作確認。
 * ビルド済みの Node server を一時起動し、/mcp の search_docs が日本語クエリで
 * 期待する代表ページを返すことを確認する。
 */
const endpoint = "http://127.0.0.1:4321/mcp";
const cases = [
  { query: "本番", expectedRoute: "/environments/production" },
  { query: "デプロイ", expectedRoute: "/procedures/deploy-application" },
  { query: "命名", expectedRoute: "/constraints/naming-conventions" },
  { query: "ロールバック", expectedRoute: "/procedures/rollback" },
];

let output = "";

// テスト専用にローカルホストへ Blume server を起動する。
const server = spawn("node", ["dist/server/entry.mjs"], {
  env: { ...process.env, HOST: "127.0.0.1", PORT: "4321" },
  stdio: ["ignore", "pipe", "pipe"],
});

server.stdout.on("data", (chunk) => {
  output += chunk;
});
server.stderr.on("data", (chunk) => {
  output += chunk;
});

// MCP endpoint が応答可能になるまで短時間ポーリングする。
async function waitForMcp() {
  for (let i = 0; i < 60; i += 1) {
    try {
      await callSearch("疎通確認");
      return;
    } catch {
      await delay(500);
    }
  }

  throw new Error(`MCP endpoint did not become ready.\n${output}`);
}

// MCP の search_docs tool を JSON-RPC over HTTP で呼び出す。
async function callSearch(query) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      id: 1,
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        name: "search_docs",
        arguments: { query, limit: 5 },
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`search_docs failed for "${query}": HTTP ${response.status}`);
  }

  const body = await response.json();
  const text = body.result?.content?.[0]?.text;
  if (!text) {
    throw new Error(`search_docs returned no text content for "${query}"`);
  }

  return JSON.parse(text);
}

try {
  await waitForMcp();

  // 各クエリで代表ルートが検索結果に含まれることを確認する。
  const results = [];
  for (const testCase of cases) {
    const hits = await callSearch(testCase.query);
    const routes = hits.map((hit) => hit.route);
    if (!routes.includes(testCase.expectedRoute)) {
      throw new Error(
        [
          `search_docs("${testCase.query}") did not include ${testCase.expectedRoute}.`,
          `Actual routes: ${routes.join(", ") || "(none)"}`,
        ].join("\n"),
      );
    }
    results.push({ query: testCase.query, routes });
  }

  console.log(JSON.stringify({ status: "ok", results }, null, 2));
} finally {
  // テスト用 server は成功・失敗にかかわらず停止する。
  server.kill("SIGTERM");
  await delay(200);
  if (!server.killed) {
    server.kill("SIGKILL");
  }
}
