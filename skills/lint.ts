import { parse } from "https://deno.land/std@0.224.0/front_matter/yaml.ts";
import { walk } from "https://deno.land/std@0.224.0/fs/walk.ts";

console.log("🔍 Linting Zowiki for semantic integrity...");

let errors = 0;

for await (
  const entry of walk("./wiki", { includeDirs: false, exts: [".md"] })
) {
  if (entry.name === "log.md" || entry.name === "index.md") continue;

  const content = await Deno.readTextFile(entry.path);
  try {
    const { data } = parse(content);
    if (!data.id || !data.type) {
      console.error(`❌ ${entry.path}: Missing 'id' or 'type' in frontmatter.`);
      errors++;
    }
  } catch (e) {
    console.error(`❌ ${entry.path}: Failed to parse frontmatter.`);
    errors++;
  }
}

if (errors > 0) {
  console.log(`\n⚠️ Found ${errors} semantic errors.`);
  Deno.exit(1);
} else {
  console.log("\n✅ Semantic check passed!");
}
