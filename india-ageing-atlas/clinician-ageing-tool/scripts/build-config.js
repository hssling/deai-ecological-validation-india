const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const configPath = path.join(root, "config.json");
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL || "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY || "";

if (supabaseUrl && supabaseAnonKey) {
  fs.writeFileSync(
    configPath,
    `${JSON.stringify({ supabaseUrl, supabaseAnonKey }, null, 2)}\n`,
    "utf8"
  );
  console.log("Generated config.json for Supabase portal mode.");
} else {
  if (fs.existsSync(configPath)) fs.rmSync(configPath);
  console.log("No Supabase public env vars found; portal will use demo mode.");
}
