import { readdir, readFile, stat } from "node:fs/promises";
import { extname, join, relative, sep } from "node:path";

/*
 * ドキュメントのリンク検証。
 * 1. Markdown/MDX 内の相対 .md リンクを禁止し、Blume のルート形式を強制する。
 * 2. ビルド済み HTML の内部リンクが実在するページまたは静的ファイルへ解決できるか確認する。
 */
const siteOrigin = "https://docs.example.internal";
const docsDir = "docs";
const distDir = "dist/client";
const ignoredSchemes = /^(mailto|tel|javascript|data):/i;

const errors = [];

// 指定ディレクトリ配下のファイルを再帰的に収集する共通処理。
async function walkFiles(root, predicate) {
  const files = [];

  async function walk(current) {
    const entries = await readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const path = join(current, entry.name);
      if (entry.isDirectory()) {
        await walk(path);
      } else if (!predicate || predicate(path)) {
        files.push(path);
      }
    }
  }

  await walk(root);
  return files;
}

// OS 依存の区切り文字を URL 用の / に揃える。
function toPosix(path) {
  return path.split(sep).join("/");
}

// dist/client 内の HTML ファイルパスから、実サイト上のルートを復元する。
function pageUrlForHtml(htmlPath) {
  const rel = toPosix(relative(distDir, htmlPath));
  if (rel === "index.html") return "/";
  if (rel.endsWith("/index.html")) return `/${rel.slice(0, -"/index.html".length)}`;
  return `/${rel.slice(0, -".html".length)}`;
}

async function pathExists(path) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

// 生成済み HTML と静的ファイルをもとに、有効な内部ルート一覧を作る。
async function buildRouteSet() {
  const routes = new Set(["/"]);
  const files = await walkFiles(distDir);

  for (const file of files) {
    const rel = `/${toPosix(relative(distDir, file))}`;
    routes.add(rel);

    if (rel.endsWith("/index.html")) {
      const route = rel.slice(0, -"/index.html".length) || "/";
      routes.add(route);
      routes.add(`${route}/`);
      continue;
    }

    if (rel.endsWith(".html")) {
      routes.add(rel.slice(0, -".html".length));
    }
  }

  return routes;
}

// HTML から href 属性だけを抽出する。リンク検証用途なので HTML パーサまでは使わない。
function extractHrefs(html) {
  const hrefs = [];
  const pattern = /\bhref=(["'])(.*?)\1/gis;
  let match;
  while ((match = pattern.exec(html)) !== null) {
    hrefs.push(match[2].trim());
  }
  return hrefs;
}

// 執筆時に壊れやすい相対 Markdown リンクを禁止する。
async function validateMarkdownLinks() {
  const contentFiles = await walkFiles(docsDir, (path) =>
    [".md", ".mdx"].includes(extname(path)),
  );
  const relativeMarkdownLink = /\[[^\]]+\]\((?!https?:\/\/|#|\/|mailto:|tel:)([^)\s]+\.md(?:#[^)]+)?)\)/g;

  for (const file of contentFiles) {
    const text = await readFile(file, "utf8");
    let match;
    while ((match = relativeMarkdownLink.exec(text)) !== null) {
      errors.push(
        `${file}: relative Markdown link "${match[1]}" is not allowed. Use a Blume route such as /procedures/deploy-application.`,
      );
    }
  }
}

// ビルド後の HTML に含まれる内部リンク切れを検出する。
async function validateRenderedHtmlLinks(routes) {
  const htmlFiles = await walkFiles(distDir, (path) => extname(path) === ".html");

  for (const file of htmlFiles) {
    const html = await readFile(file, "utf8");
    const pageUrl = new URL(pageUrlForHtml(file), siteOrigin);

    for (const href of extractHrefs(html)) {
      if (!href || href.startsWith("#") || ignoredSchemes.test(href)) continue;

      let url;
      try {
        url = new URL(href, pageUrl);
      } catch {
        errors.push(`${file}: invalid href "${href}"`);
        continue;
      }

      if (url.origin !== siteOrigin) continue;
      if (routes.has(url.pathname)) continue;

      const staticPath = join(distDir, decodeURIComponent(url.pathname.slice(1)));
      if (await pathExists(staticPath)) continue;

      errors.push(
        `${file}: href "${href}" resolves to missing internal path "${url.pathname}"`,
      );
    }
  }
}

await validateMarkdownLinks();
await validateRenderedHtmlLinks(await buildRouteSet());

if (errors.length > 0) {
  console.error(`Found ${errors.length} link validation error(s):`);
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log("link validation passed");
