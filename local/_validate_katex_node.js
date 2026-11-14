const katex = require("katex");
const fs = require("fs");
const html = fs.readFileSync("../math/thinking-mental-squaring-and-square-rooting.html", "utf8");
const re = /<annotation encoding="application\/x-tex">([\s\S]*?)<\/annotation>/g;
let m;
let fails = 0;
let total = 0;
while ((m = re.exec(html))) {
  total++;
  let t = m[1]
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"');
  const display = /\\begin\{aligned\}|\\\\/.test(t);
  const out = katex.renderToString(t, {
    throwOnError: false,
    displayMode: display,
    strict: "ignore",
  });
  if (out.includes("katex-error")) {
    fails++;
    console.log(t.slice(0, 220).replace(/\n/g, " "));
    console.log("---");
  }
}
console.log("total", total, "fails", fails);