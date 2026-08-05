import { defineConfig } from "blume";

const siteUrl =
  process.env.BLUME_SITE_URL || "https://sample-document-site.pages.dev";

export default defineConfig({
  title: "K8sプラットフォームドキュメント",
  description:
    "アプリケーションチームとAIエージェント向けのKubernetesプラットフォームドキュメント。",
  feedback: false,
  i18n: {
    defaultLocale: "ja",
    locales: [{ code: "ja", label: "日本語" }],
  },
  content: {
    root: "blume-docs",
  },
  deployment: {
    output: "static",
    site: siteUrl,
  },
  ai: {
    llmsTxt: true,
    mcp: {
      enabled: false,
    },
  },
  navigation: {
    sidebar: [
      "/",
      {
        label: "概要",
        items: ["/overview/platform-summary", "/overview/audience-and-scope"],
      },
      {
        label: "環境",
        items: [
          "/environments",
          "/environments/dev",
          "/environments/production",
          "/environments/network",
        ],
      },
      {
        label: "制約",
        items: [
          "/constraints",
          "/constraints/platform-limits",
          "/constraints/security-policy",
          "/constraints/naming-conventions",
        ],
      },
      {
        label: "作業手順",
        items: [
          "/procedures",
          "/procedures/deploy-application",
          "/procedures/rollback",
          "/procedures/secrets",
        ],
      },
      {
        label: "API仕様",
        items: [
          "/api-reference",
          "/api-reference/platform-api",
          "/api-reference/crds",
        ],
      },
      {
        label: "ツール",
        items: ["/tools", "/tools/cli", "/tools/ci-templates"],
      },
      {
        label: "アプリチェックリスト",
        items: [
          "/app-checklists",
          "/app-checklists/production-readiness",
          "/app-checklists/deployment-review",
        ],
      },
      {
        label: "ランブック",
        items: ["/runbooks", "/runbooks/common-failures"],
      },
      {
        label: "運用",
        items: ["/operations/document-operations"],
      },
      {
        label: "設計",
        items: [
          "/design/requirements-and-architecture",
          "/design/ai-agent-access-plan",
        ],
      },
      {
        label: "執筆",
        items: ["/authoring/page-template", "/authoring/markdown-syntax-test"],
      },
    ],
  },
  search: {
    provider: "orama",
  },
  analytics: {
    scripts: [
      {
        src: "/clipboard-fallback.js",
        strategy: "defer",
      },
    ],
  },
});
