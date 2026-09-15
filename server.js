const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { z } = require("zod");
const { DatabaseSync } = require("node:sqlite");

const db = new DatabaseSync("data/quran.db");

const server = new McpServer({
  name: "quran-morphology",
  version: "1.0.0"
});

server.tool(
  "cari_kata_by_root",
  { root: z.string().describe("Akar kata Arab, misal: عمل") },
  async ({ root }) => {
    const rows = db.prepare(
      "SELECT surah, ayah, word, arabic, pos, lemma FROM morphology WHERE root = ? LIMIT 50"
    ).all(root);
    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }]
    };
  }
);

server.tool(
  "lihat_ayat",
  {
    surah: z.number().describe("Nomor surah"),
    ayah: z.number().describe("Nomor ayat")
  },
  async ({ surah, ayah }) => {
    const rows = db.prepare(
      "SELECT word, segment, arabic, pos, root, lemma, features FROM morphology WHERE surah = ? AND ayah = ? ORDER BY word, segment"
    ).all(surah, ayah);
    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }]
    };
  }
);

const transport = new StdioServerTransport();
server.connect(transport);
