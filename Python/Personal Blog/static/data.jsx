// Article formatting helpers shared across pages. The article data
// itself lives on the backend (see /api/articles in app.py) and is
// loaded by app.jsx via fetch() — no seed lives in the frontend.

// Format an ISO date (YYYY-MM-DD) for display.
//   "long"  -> "May 12, 2026"
//   "short" -> "May 12, 2026"  (same shape, kept for API symmetry)
//   "iso"   -> the input unchanged
function formatDate(iso, style = "long") {
  const d = new Date(iso + "T00:00:00");
  if (style === "iso") return iso;
  if (style === "short") {
    return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
}

// Total word count across all body blocks (strings + heading objs).
function wordCount(article) {
  return article.body.reduce((n, b) => {
    const s = typeof b === "string" ? b : b.text;
    return n + s.split(/\s+/).filter(Boolean).length;
  }, 0);
}

// Estimated reading time in minutes (220 wpm, minimum 1).
function readingTime(article) {
  return Math.max(1, Math.round(wordCount(article) / 220));
}

// Short preview text for index views: the lede if present, else
// the first paragraph/heading of the body.
function excerptOf(article) {
  return article.lede || (typeof article.body[0] === "string" ? article.body[0] : article.body[0].text);
}

// Render a body array back into editable Markdown for the editor.
function bodyToMarkdown(body) {
  return body.map(b => typeof b === "string" ? b : `## ${b.text}`).join("\n\n");
}

// Parse Markdown from the editor back into a body array of
// strings and h2 heading objects.
function markdownToBody(md) {
  return md.split(/\n\s*\n/).map(chunk => {
    const trimmed = chunk.trim();
    if (trimmed.startsWith("## ")) return { type: "h2", text: trimmed.slice(3).trim() };
    if (trimmed.startsWith("# "))  return { type: "h2", text: trimmed.slice(2).trim() };
    return trimmed;
  }).filter(Boolean);
}

Object.assign(window, {
  formatDate, wordCount, readingTime, excerptOf,
  bodyToMarkdown, markdownToBody,
});
