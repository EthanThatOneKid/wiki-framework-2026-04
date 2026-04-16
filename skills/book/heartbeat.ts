import { parse } from "https://deno.land/std@0.224.0/datetime/mod.ts";

const date = new Date().toISOString().split("T")[0];
const path = `./wiki/daily-${date}.md`;

console.log(`💓 Pulsing Daily Heartbeat for ${date}...`);

const template = await Deno.readTextFile("./skills/book/daily/template.md");
const content = template.replace(/{{date}}/g, date);

try {
  await Deno.writeTextFile(path, content, { createNew: true });
  console.log(`✅ ${path} created!`);
} catch (e) {
  console.log(`ℹ️ ${path} already exists. Skipping.`);
}

console.log("--- Done Pulsing ---");
