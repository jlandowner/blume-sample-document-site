import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const rootConfigPath = resolve(process.argv[2] || "blume.config.ts");
const outputConfigPath = resolve(process.argv[3] || "blume.config.js");
const siteUrl =
  process.env.BLUME_SITE_URL || "https://sample-document-site.pages.dev";

const tempDir = await mkdtemp(join(tmpdir(), "blume-pages-config-"));
const tempConfigPath = join(tempDir, basename(rootConfigPath).replace(/\.ts$/, ".mjs"));

try {
  const rootConfigSource = await readFile(rootConfigPath, "utf8");
  const importFreeConfigSource = rootConfigSource.replace(
    /^\s*import\s+\{\s*defineConfig\s*\}\s+from\s+["']blume["'];\s*/m,
    "const defineConfig = (config) => config;\n",
  );

  await writeFile(tempConfigPath, importFreeConfigSource);
  const rootConfigModule = await import(pathToFileURL(tempConfigPath));
  const rootConfig = rootConfigModule.default;

  if (!rootConfig || typeof rootConfig !== "object") {
    throw new Error(`${rootConfigPath} must export a Blume config object.`);
  }

  const pagesConfig = {
    ...rootConfig,
    deployment: {
      ...rootConfig.deployment,
      adapter: undefined,
      output: "static",
      site: siteUrl,
    },
    ai: {
      ...rootConfig.ai,
      mcp: {
        ...rootConfig.ai?.mcp,
        enabled: false,
      },
    },
  };

  await writeFile(
    outputConfigPath,
    [
      'import { defineConfig } from "blume";',
      "",
      "export default defineConfig(",
      `${JSON.stringify(pagesConfig, null, 2)}`,
      ");",
      "",
    ].join("\n"),
  );
} finally {
  await rm(tempDir, { force: true, recursive: true });
}
