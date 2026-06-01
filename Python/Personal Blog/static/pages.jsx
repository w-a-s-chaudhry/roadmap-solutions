// Pages: HomePage, ArticlePage, Dashboard, EditorPage
// All shared via window globals so other Babel scripts can use them.

const { useState, useMemo, useEffect } = React;

// ─── Topbar ───────────────────────────────────────────────────────
function Topbar({ route, navigate, mode, dark, onToggleDark }) {
  return (
    <header className="topbar">
      <div className="container topbar-inner">
        <a
          className="brand"
          href="#/"
          onClick={(e) => { e.preventDefault(); navigate({ name: "home" }); }}
        >
          <span className="brand-mark">F</span>
          <span className="brand-name">Field Notes</span>
          <span className="brand-tag">/ a personal blog</span>
        </a>
        <nav className="topnav">
          <button
            className={route.name === "home" ? "active" : ""}
            onClick={() => navigate({ name: "home" })}
          >Writing</button>
          <button onClick={() => alert("About — placeholder")}>About</button>
          <button onClick={() => alert("RSS — placeholder")}>RSS</button>
          <span style={{ width: 8 }} />
          <button
            className={mode === "admin" ? "active" : ""}
            onClick={() => { window.location.href = "/admin"; }}
            title="Admin"
          >Admin →</button>
          <ThemeToggle dark={dark} onToggle={onToggleDark} />
        </nav>
      </div>
    </header>
  );
}

// ─── Theme toggle ─────────────────────────────────────────────────
// Single-button light/dark switch. Shows the icon of the theme
// you'd switch TO, so clicking it always feels predictable.
function ThemeToggle({ dark, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      title={dark ? "Switch to light mode" : "Switch to dark mode"}
      aria-label="Toggle dark mode"
      style={{ display: "inline-flex", alignItems: "center", padding: "6px 8px" }}
    >
      {dark ? (
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
          <circle cx="8" cy="8" r="3"
                  stroke="currentColor" strokeWidth="1.5" />
          <path d="M8 1.5v1.5M8 13v1.5M1.5 8h1.5M13 8h1.5
                   M3 3l1 1M12 12l1 1
                   M13 3l-1 1M4 12l-1 1"
                stroke="currentColor" strokeWidth="1.5"
                strokeLinecap="round" />
        </svg>
      ) : (
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
          <path d="M13 9.5A5.5 5.5 0 1 1 6.5 3
                   a4.5 4.5 0 0 0 6.5 6.5Z"
                fill="currentColor" />
        </svg>
      )}
    </button>
  );
}

// ─── Footer ───────────────────────────────────────────────────────
function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-inner">
        <span>© 2026 — Field Notes</span>
        <span>Built with HTML &amp; patience</span>
      </div>
    </footer>
  );
}

// ─── HOME ─────────────────────────────────────────────────────────
function HomePage({ articles, navigate, cardLayout }) {
  const sorted = useMemo(() => [...articles].sort((a, b) => b.date.localeCompare(a.date)), [articles]);
  const featured = sorted[0];

  return (
    <>
      <section className="hero">
        <div className="container">
          <div className="hero-kicker">Field Notes — Est. 2025</div>
          <h1 className="hero-title">
            Slow writing about software, attention, and the texture of working in public.
          </h1>
          <p className="hero-sub">
            A small archive of essays. New posts arrive when they're ready, usually
            once a month. No newsletter, no analytics, no comments.
          </p>
          <div className="hero-meta">
            <span><b>{articles.length}</b>&nbsp;&nbsp;essays</span>
            <span>since&nbsp;&nbsp;<b>Dec 2025</b></span>
            {featured && (
              <span>latest&nbsp;&nbsp;<b>{formatDate(featured.date, "short")}</b></span>
            )}
          </div>
        </div>
      </section>

      <section className="list">
        <div className="container">
          <div className="list-head">
            <span>Index</span>
            <span className="count">{articles.length} / {articles.length}</span>
          </div>

          {cardLayout === "rows" && (
            <div className="row-list">
              {sorted.map((a, i) => (
                <article
                  key={a.id}
                  className="row"
                  onClick={() => navigate({ name: "article", id: a.id })}
                >
                  <div className="row-date">{formatDate(a.date, "short").toUpperCase()}</div>
                  <div>
                    <h2 className="row-title">{a.title}</h2>
                    <p className="row-excerpt">{excerptOf(a)}</p>
                  </div>
                  <div className="row-num">№ {String(sorted.length - i).padStart(3, "0")}</div>
                </article>
              ))}
            </div>
          )}

          {cardLayout === "table" && (
            <table className="tbl">
              <thead>
                <tr>
                  <th style={{ width: 130 }}>Date</th>
                  <th>Title</th>
                  <th style={{ width: 110, textAlign: "right" }}>Reading</th>
                </tr>
              </thead>
              <tbody>
                {sorted.map(a => (
                  <tr key={a.id} onClick={() => navigate({ name: "article", id: a.id })}>
                    <td className="tbl-date">{formatDate(a.date, "short")}</td>
                    <td className="tbl-title">{a.title}</td>
                    <td className="tbl-len">{readingTime(a)} min</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}

          {cardLayout === "cards" && (
            <div className="cards">
              {sorted.map(a => (
                <article
                  key={a.id}
                  className="card"
                  onClick={() => navigate({ name: "article", id: a.id })}
                >
                  <div className="card-meta">
                    <span>{formatDate(a.date, "short").toUpperCase()}</span>
                    <span>{readingTime(a)} min</span>
                  </div>
                  <h2 className="card-title">{a.title}</h2>
                  <p className="card-excerpt">{excerptOf(a)}</p>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  );
}

// ─── ARTICLE ──────────────────────────────────────────────────────
function ArticlePage({ articles, articleId, navigate }) {
  const sorted = useMemo(() => [...articles].sort((a, b) => b.date.localeCompare(a.date)), [articles]);
  const idx = sorted.findIndex(a => a.id === articleId);
  const article = sorted[idx];
  if (!article) {
    return (
      <div className="container">
        <div className="empty">Article not found. <a href="#/" onClick={(e) => { e.preventDefault(); navigate({ name: "home" }); }}>Back to index →</a></div>
      </div>
    );
  }
  const prev = sorted[idx + 1];
  const next = sorted[idx - 1];

  return (
    <article className="article container">
      <div className="article-meta">
        <span>{formatDate(article.date).toUpperCase()}</span>
        <span>·</span>
        <span>{readingTime(article)} MIN READ</span>
        <span>·</span>
        <span>{article.id.toUpperCase()}</span>
      </div>
      <h1>{article.title}</h1>
      <p className="article-lede">{article.lede}</p>

      <div className="article-body">
        {article.body.map((block, i) => {
          if (typeof block === "string") return <p key={i}>{block}</p>;
          if (block.type === "h2")       return <h2 key={i}>{block.text}</h2>;
          return null;
        })}
      </div>

      <div className="article-foot">
        <a
          href={prev ? `#/article/${prev.id}` : "#/"}
          onClick={(e) => {
            e.preventDefault();
            if (prev) navigate({ name: "article", id: prev.id });
            else navigate({ name: "home" });
          }}
        >
          {prev ? `← ${prev.title}` : "← Back to index"}
        </a>
        <a
          href={next ? `#/article/${next.id}` : "#/"}
          onClick={(e) => {
            e.preventDefault();
            if (next) navigate({ name: "article", id: next.id });
            else navigate({ name: "home" });
          }}
        >
          {next ? `${next.title} →` : "Index →"}
        </a>
      </div>
    </article>
  );
}

// ─── ADMIN: shared chrome ────────────────────────────────────────
function AdminBar({ section, navigate }) {
  return (
    <div className="admin-bar">
      <div className="container admin-bar-inner">
        <div className="admin-bar-l">
          <span className="dot" />
          <span>Admin · {section}</span>
        </div>
        <div className="admin-bar-l">
          <span>signed in as <b style={{ color: "var(--text-2)" }}>editor@fieldnotes</b></span>
          <button className="btn ghost sm" onClick={() => navigate({ name: "home" })}>Exit ↗</button>
        </div>
      </div>
    </div>
  );
}

// ─── DASHBOARD ────────────────────────────────────────────────────
function Dashboard({ articles, navigate, onDelete }) {
  const sorted = useMemo(() => [...articles].sort((a, b) => b.date.localeCompare(a.date)), [articles]);
  const totalWords = articles.reduce((n, a) => n + wordCount(a), 0);
  const lastDate = sorted[0]?.date;

  return (
    <>
      <AdminBar section="Dashboard" navigate={navigate} />
      <section className="container">
        <div className="dash-head">
          <div>
            <h1>Dashboard</h1>
            <p>Manage articles, drafts, and publishing.</p>
          </div>
          <button className="btn primary" onClick={() => navigate({ name: "add" })}>
            + New article
          </button>
        </div>

        <div className="dash-stats">
          <div className="stat">
            <div className="stat-label">Published</div>
            <div className="stat-val">{articles.length}</div>
          </div>
          <div className="stat">
            <div className="stat-label">Drafts</div>
            <div className="stat-val">0</div>
          </div>
          <div className="stat">
            <div className="stat-label">Total words</div>
            <div className="stat-val">{totalWords.toLocaleString()}</div>
          </div>
          <div className="stat">
            <div className="stat-label">Last published</div>
            <div className="stat-val mono" style={{ fontSize: 16, paddingTop: 4 }}>
              {lastDate ? formatDate(lastDate, "short") : "—"}
            </div>
          </div>
        </div>

        <div className="admin-tbl-wrap">
          <table className="admin-tbl">
            <thead>
              <tr>
                <th style={{ width: 80 }}>ID</th>
                <th>Title</th>
                <th style={{ width: 130 }}>Date</th>
                <th style={{ width: 110 }}>Status</th>
                <th style={{ width: 200, textAlign: "right" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {sorted.map(a => (
                <tr key={a.id}>
                  <td className="admin-id">{a.id}</td>
                  <td className="admin-title">{a.title}</td>
                  <td className="admin-date">{formatDate(a.date, "short")}</td>
                  <td><span className="admin-status published">Published</span></td>
                  <td>
                    <div className="admin-actions">
                      <button
                        className="btn ghost sm"
                        onClick={() => navigate({ name: "article", id: a.id })}
                      >View</button>
                      <button
                        className="btn sm"
                        onClick={() => navigate({ name: "edit", id: a.id })}
                      >Edit</button>
                      <button
                        className="btn danger sm"
                        onClick={() => {
                          if (confirm(`Delete "${a.title}"? This cannot be undone.`)) onDelete(a.id);
                        }}
                      >Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
              {sorted.length === 0 && (
                <tr>
                  <td colSpan="5" style={{ textAlign: "center", padding: 60, color: "var(--text-3)" }}>
                    No articles yet. <a href="#" onClick={(e) => { e.preventDefault(); navigate({ name: "add" }); }} style={{ color: "var(--accent)" }}>Write your first one →</a>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}

// ─── ADD / EDIT (shared editor) ──────────────────────────────────
function EditorPage({ mode, article, navigate, onSave, onDelete }) {
  const isEdit = mode === "edit";

  const [title,   setTitle]   = useState(article?.title || "");
  const [date,    setDate]    = useState(article?.date  || new Date().toISOString().slice(0, 10));
  const [lede,    setLede]    = useState(article?.lede  || "");
  const [content, setContent] = useState(article ? bodyToMarkdown(article.body) : "");

  const wc = content.split(/\s+/).filter(Boolean).length;
  const rt = Math.max(1, Math.round(wc / 220));

  function handleSave(e) {
    e?.preventDefault();
    if (!title.trim()) { alert("Title is required."); return; }
    onSave({
      id: article?.id,
      title: title.trim(),
      date,
      lede: lede.trim(),
      body: markdownToBody(content),
    });
  }

  return (
    <>
      <AdminBar
        section={isEdit ? `Edit · ${article?.id || ""}` : "New article"}
        navigate={navigate}
      />
      <form className="form container" onSubmit={handleSave}>
        <div className="form-head">
          <div>
            <span className="kicker">{isEdit ? "Editing article" : "New article"}</span>
            <h1>{isEdit ? article?.title || "Untitled" : "Write a new post"}</h1>
          </div>
          <button
            type="button"
            className="btn ghost"
            onClick={() => navigate({ name: "dashboard" })}
          >← Back to dashboard</button>
        </div>

        <div className="field">
          <label className="field-label">
            <span>Title</span>
            <span className="field-hint">{title.length} chars</span>
          </label>
          <input
            className="input title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="A working title…"
          />
        </div>

        <div className="row-2col">
          <div className="field">
            <label className="field-label">
              <span>Publication date</span>
            </label>
            <input
              className="input mono"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>
          <div className="field">
            <label className="field-label">
              <span>Slug / ID</span>
              <span className="field-hint">auto</span>
            </label>
            <input
              className="input mono"
              readOnly
              value={article?.id || `a-${String(Date.now()).slice(-3)}`}
              style={{ color: "var(--text-3)" }}
            />
          </div>
        </div>

        <div className="field">
          <label className="field-label">
            <span>Lede</span>
            <span className="field-hint">A short opening sentence shown in the index.</span>
          </label>
          <input
            className="input"
            value={lede}
            onChange={(e) => setLede(e.target.value)}
            placeholder="One sentence that invites the reader in…"
          />
        </div>

        <div className="field">
          <label className="field-label">
            <span>Content · Markdown</span>
            <span className="field-hint">{wc.toLocaleString()} words · {rt} min read</span>
          </label>
          <textarea
            className="textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={"Write here.\n\n## Use ## for subheadings\n\nSeparate paragraphs with blank lines."}
          />
        </div>

        <div className="form-actions">
          <div>
            {isEdit && (
              <button
                type="button"
                className="btn danger"
                onClick={() => {
                  if (confirm(`Delete "${article.title}"? This cannot be undone.`)) {
                    onDelete(article.id);
                  }
                }}
              >Delete article</button>
            )}
          </div>
          <div className="form-actions-r">
            <button
              type="button"
              className="btn"
              onClick={() => navigate({ name: "dashboard" })}
            >Cancel</button>
            <button type="submit" className="btn primary">
              {isEdit ? "Save changes" : "Publish"}
            </button>
          </div>
        </div>
      </form>
    </>
  );
}

Object.assign(window, {
  Topbar, Footer, HomePage, ArticlePage, Dashboard, EditorPage,
});
