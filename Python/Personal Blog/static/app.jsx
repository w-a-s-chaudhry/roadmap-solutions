// Main app: routing + state + API client.

const { useState: useStateA, useEffect: useEffectA } = React;

// Hardcoded look-and-feel for everything except dark mode (which
// is user-toggleable from the topbar and persisted to localStorage).
const DEFAULTS = {
  cardLayout: "rows",
};

// Read the initial theme: saved preference wins; otherwise fall
// back to the OS-level prefers-color-scheme. Matches the inline
// <head> script in index.html so React picks up the same value
// the page already painted with.
function initialDark() {
  const stored = localStorage.getItem("fn-theme");
  if (stored) return stored === "dark";
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

// --- Hash routing ---

function parseHash() {
  const h = (location.hash || "#/").replace(/^#/, "");
  const parts = h.split("/").filter(Boolean);
  if (parts.length === 0)                    return { name: "home" };
  if (parts[0] === "article" && parts[1])    return { name: "article", id: parts[1] };
  if (parts[0] === "admin")                  return { name: "dashboard" };
  if (parts[0] === "add")                    return { name: "add" };
  if (parts[0] === "edit" && parts[1])       return { name: "edit", id: parts[1] };
  return { name: "home" };
}

function routeToHash(r) {
  switch (r.name) {
    case "home":      return "#/";
    case "article":   return `#/article/${r.id}`;
    case "dashboard": return "#/admin";
    case "add":       return "#/add";
    case "edit":      return `#/edit/${r.id}`;
    default:          return "#/";
  }
}

// --- API client ---
// Tiny wrapper around fetch() that handles JSON + error responses
// uniformly so the views can stay sync-style.

async function api(method, path, body) {
  const res = await fetch(path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body:    body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;  // DELETE returns no body
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `${method} ${path} failed`);
  return data;
}

// --- App ---

function App() {
  const [route, setRoute]       = useStateA(parseHash());
  const [articles, setArticles] = useStateA([]);
  const [loading, setLoading]   = useStateA(true);
  const [dark, setDark]         = useStateA(initialDark);

  // Apply the theme to <html> and persist it whenever it changes.
  // CSS handles every color via the [data-theme="dark"] block —
  // we only flip the attribute and let cascade do the rest.
  useEffectA(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    localStorage.setItem("fn-theme", dark ? "dark" : "light");
  }, [dark]);

  // Load articles from the backend on mount.
  useEffectA(() => {
    api("GET", "/api/articles")
      .then(setArticles)
      .catch((err) => alert(`Could not load articles: ${err.message}`))
      .finally(() => setLoading(false));
  }, []);

  // Hash routing.
  useEffectA(() => {
    const onHash = () => setRoute(parseHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);

  function navigate(r) {
    const h = routeToHash(r);
    if (location.hash !== h) location.hash = h;
    else setRoute(r);
    window.scrollTo({ top: 0, behavior: "instant" });
  }

  // Save: POST for new, PUT for existing. Server returns the
  // saved article (with its assigned id for new ones); we splice
  // that into local state to stay in sync.
  async function handleSave(payload) {
    try {
      const isUpdate = payload.id && articles.find((a) => a.id === payload.id);
      const saved = isUpdate
        ? await api("PUT",  `/api/articles/${payload.id}`, payload)
        : await api("POST", "/api/articles",               payload);

      if (isUpdate) {
        setArticles(articles.map((a) => (a.id === saved.id ? saved : a)));
      } else {
        setArticles([saved, ...articles]);
      }
      navigate({ name: "dashboard" });
    } catch (err) {
      alert(`Could not save: ${err.message}`);
    }
  }

  async function handleDelete(id) {
    try {
      await api("DELETE", `/api/articles/${id}`);
      setArticles(articles.filter((a) => a.id !== id));
      navigate({ name: "dashboard" });
    } catch (err) {
      alert(`Could not delete: ${err.message}`);
    }
  }

  const isAdmin = ["dashboard", "add", "edit"].includes(route.name);

  // Avoid rendering pages that read articles[0] before fetch lands.
  if (loading) {
    return (
      <div className="app">
        <Topbar route={route} navigate={navigate} mode={isAdmin ? "admin" : "guest"} dark={dark} onToggleDark={() => setDark((d) => !d)} />
        <div className="container" style={{ padding: "60px 0", color: "var(--text-3)" }}>
          Loading…
        </div>
        <Footer />
      </div>
    );
  }

  let body;
  if (route.name === "home") {
    body = <HomePage articles={articles} navigate={navigate} cardLayout={DEFAULTS.cardLayout} />;
  } else if (route.name === "article") {
    body = <ArticlePage articles={articles} articleId={route.id} navigate={navigate} />;
  } else if (route.name === "dashboard") {
    body = <Dashboard articles={articles} navigate={navigate} onDelete={handleDelete} />;
  } else if (route.name === "add") {
    body = <EditorPage mode="add" navigate={navigate} onSave={handleSave} />;
  } else if (route.name === "edit") {
    const article = articles.find((a) => a.id === route.id);
    body = <EditorPage mode="edit" article={article} navigate={navigate} onSave={handleSave} onDelete={handleDelete} />;
  }

  return (
    <div className="app">
      <Topbar route={route} navigate={navigate} mode={isAdmin ? "admin" : "guest"} dark={dark} onToggleDark={() => setDark((d) => !d)} />
      {body}
      <Footer />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
