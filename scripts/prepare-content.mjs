import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";

/*
 * Blume に渡す前処理。
 * docs 配下の Markdown/MDX を blume-docs へコピーし、Blume が扱う frontmatter を
 * title と description に絞る。既存ページの H1 と Blume のページタイトルが重複表示
 * されないよう、frontmatter の title と同じ先頭 H1 も取り除く。
 */
const repoRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
const sourceDir = join(repoRoot, "docs");
const outputDir = join(repoRoot, "blume-docs");

const frontmatterValue = (frontmatter, key) => {
  const match = frontmatter.match(new RegExp(`^${key}:\\s*(.+)$`, "m"));
  return match?.[1]?.trim() ?? "";
};

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

const removeDuplicateTitleHeading = (body, title) => {
  if (!title) {
    return body;
  }
  const pattern = new RegExp(`^\\s*#\\s+${escapeRegExp(title)}\\s*\\n+`);
  return body.replace(pattern, "");
};

// docs 配下の .md と .mdx を再帰的に収集する。
const contentFiles = async (dir) => {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await contentFiles(path)));
    } else if (
      entry.isFile() &&
      (entry.name.endsWith(".md") || entry.name.endsWith(".mdx"))
    ) {
      files.push(path);
    }
  }

  return files;
};

// frontmatter を Blume 用に正規化し、重複する先頭 H1 を削除する。
const sanitizeMarkdown = (text) => {
  if (!text.startsWith("---\n")) {
    return text;
  }

  const end = text.indexOf("\n---\n", 4);
  if (end === -1) {
    return text;
  }

  const frontmatter = text.slice(4, end);
  const body = text.slice(end + "\n---\n".length);
  const title = frontmatterValue(frontmatter, "title");
  const description = frontmatterValue(frontmatter, "description");

  const lines = ["---"];
  if (title) {
    lines.push(`title: ${title}`);
  }
  if (description) {
    lines.push(`description: ${description}`);
  }
  lines.push("---", "");

  return `${lines.join("\n")}${removeDuplicateTitleHeading(body, title)}`;
};

// blume-docs は生成物なので、毎回作り直して古いページが残らないようにする。
await rm(outputDir, { force: true, recursive: true });

for (const sourcePath of await contentFiles(sourceDir)) {
  const filePath = relative(sourceDir, sourcePath);
  const outputPath = join(outputDir, filePath);
  const text = await readFile(sourcePath, "utf8");
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, sanitizeMarkdown(text), "utf8");
  console.log(`prepared ${relative(repoRoot, outputPath)}`);
}
