/**
 * Global Pagefind search — classic script (works on file:// for UI; search needs http(s) or localhost).
 */
(function () {
  "use strict";

  const COPY = {
    en: {
      open: "Search site",
      title: "Search Kiwi 爱AI Study",
      placeholder: "Topics, lessons, episodes, keywords…",
      empty: "No results. Try another keyword or switch language.",
      offline:
        "Full search needs the site opened over http(s)—for example GitHub Pages or a local server (npx serve). The search index cannot load from a file:// tab.",
      hint: "Ctrl+K or / to open",
      scopeMath: "Search in Math",
      scopeAll: "All sections",
      close: "Close",
    },
    zh: {
      open: "搜索本站",
      title: "搜索 Kiwi 爱AI Study",
      placeholder: "主题、课程、集数、关键词…",
      empty: "没有匹配结果，请换关键词或切换语言后再试。",
      offline:
        "完整搜索需要在 http(s) 下打开网站，例如 GitHub Pages 或本地服务器（npx serve）。file:// 标签页无法加载搜索索引。",
      hint: "Ctrl+K 或 / 打开",
      scopeMath: "搜索数学内容",
      scopeAll: "全站",
      close: "关闭",
    },
  };

  function lang() {
    return (document.documentElement.lang || "").toLowerCase().startsWith("zh") ? "zh" : "en";
  }

  function cleanExcerpt(excerpt) {
    let s = excerpt || "";
    s = s.replace(/<math\b[\s\S]*?<\/math>/gi, " ");
    s = s.replace(/&lt;math\b[\s\S]*?&lt;\/math&gt;/gi, " ");
    s = s.replace(/<[^>]+>/g, " ");
    s = s.replace(/&lt;[^&]+&gt;/g, " ");
    s = s.replace(/\s+/g, " ").trim();
    if (s.length > 220) s = s.slice(0, 217) + "…";
    return s;
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function truncatePlain(text, maxLen) {
    const s = String(text || "").trim();
    if (s.length <= maxLen) return s;
    return s.slice(0, maxLen - 1).trim() + "…";
  }

  function highlightQuery(text, query) {
    const q = (query || activeQuery || "").trim();
    const plain = escapeHtml(text);
    if (!q) return plain;
    try {
      if (isMathAbbrev(q)) {
        const u = q.toUpperCase();
        return plain.replace(new RegExp("(?<![A-Za-z])" + u + "(?![A-Za-z])", "gi"), function (m) {
          return "<mark>" + m + "</mark>";
        });
      }
      const esc = q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return plain.replace(new RegExp(esc, "gi"), function (m) {
        return "<mark>" + m + "</mark>";
      });
    } catch (_) {
      return plain;
    }
  }

  function sanitizePagefindExcerpt(excerpt) {
    let s = String(excerpt || "");
    s = s.replace(/<math\b[\s\S]*?<\/math>/gi, " ");
    s = s.replace(/&lt;math\b[\s\S]*?&lt;\/math&gt;/gi, " ");
    s = s.replace(/<span class="pagefind__highlight">(.*?)<\/span>/gi, "<mark>$1</mark>");
    s = s.replace(/<(?!\/?mark\b)[^>]+>/gi, " ");
    s = s.replace(/&lt;[^&]+&gt;/g, " ");
    s = s.replace(/\s+/g, " ").trim();
    const plainLen = s.replace(/<\/?mark>/gi, "").length;
    if (plainLen > 220) {
      const plain = cleanExcerpt(s);
      return highlightQuery(truncatePlain(plain, 220), activeQuery);
    }
    return s;
  }

  function excerptIsReadable(excerpt, query) {
    const q = (query || activeQuery || "").trim();
    if (isMathAbbrev(q)) {
      if (!excerpt) return true;
      return !/xmlns|semantics|annotation encoding/i.test(excerpt);
    }
    if (!excerpt) return false;
    if (/xmlns|semantics|<mrow|&lt;mrow|annotation encoding/i.test(excerpt)) return false;
    const plain = cleanExcerpt(excerpt);
    return plain.length >= 6;
  }

  function metaHaystack(meta, excerpt) {
    return (
      cleanExcerpt(excerpt) +
      " " +
      (meta.excerpt_zh || "") +
      " " +
      (meta.title_en || "") +
      " " +
      (meta.title_zh || "") +
      " " +
      (meta.breadcrumb || "") +
      " " +
      (meta.breadcrumb_zh || "")
    );
  }

  function excerptLang(excerpt) {
    const plain = cleanExcerpt(excerpt);
    const cjk = (plain.match(/[\u4e00-\u9fff]/g) || []).length;
    const latin = (plain.match(/[a-zA-Z]/g) || []).length;
    if (cjk >= 4 && cjk >= latin) return "zh";
    if (latin >= 4) return "en";
    return cjk > latin ? "zh" : "en";
  }

  let activeQuery = "";

  const MATH_ABBREVS = new Set(["asa", "aas", "ssa", "sas", "sss", "gcf"]);

  function isMathAbbrev(term) {
    return MATH_ABBREVS.has((term || "").trim().toLowerCase());
  }

  function hitIsMathSection(meta, url) {
    const section = String(meta.section || "").toLowerCase();
    if (section === "math") return true;
    const u = String(url || "").toLowerCase();
    return u.includes("/math/") || /^\/math[-/]/.test(u);
  }

  function mathAbbrevInText(text, term) {
    const u = (term || "").trim().toUpperCase();
    if (!/^[A-Z]{2,4}$/.test(u)) return false;
    const s = String(text || "").toUpperCase();
    let i = 0;
    while ((i = s.indexOf(u, i)) !== -1) {
      const before = i > 0 ? s[i - 1] : "";
      const after = i + u.length < s.length ? s[i + u.length] : "";
      if (!/[A-Z]/.test(before) && !/[A-Z]/.test(after)) return true;
      i += 1;
    }
    return false;
  }

  function hitMatchesActiveLang(excerpt, meta, query) {
    const q = (query || activeQuery || "").trim();
    if (isMathAbbrev(q)) {
      const hay = metaHaystack(meta, excerpt);
      if (!mathAbbrevInText(hay, q)) return false;
      if (lang() === "zh") {
        return !!(meta.title_zh || meta.breadcrumb_zh || meta.excerpt_zh);
      }
      return !!(meta.title_en || meta.title || meta.breadcrumb);
    }
    return excerptLang(excerpt) === lang();
  }

  function hasCjk(text) {
    return /[\u4e00-\u9fff]/.test(text || "");
  }

  function lastCrumbSegment(crumb) {
    if (!crumb) return "";
    const parts = crumb.split("›");
    return (parts[parts.length - 1] || "").trim();
  }

  function displayTitle(meta, excerpt, url) {
    if (lang() === "zh") {
      return meta.title_zh || lastCrumbSegment(meta.breadcrumb_zh) || meta.title || url;
    }
    let title = meta.title_en || meta.title || "";
    if (!title || hasCjk(title)) {
      const fromCrumb = lastCrumbSegment(meta.breadcrumb);
      if (fromCrumb && !hasCjk(fromCrumb)) title = fromCrumb;
    }
    if (!title || hasCjk(title)) title = url;
    return title;
  }

  function displayCrumb(meta) {
    if (lang() === "zh") {
      const crumb = meta.breadcrumb_zh || "";
      return hasCjk(crumb) ? crumb : "";
    }
    const crumb = meta.breadcrumb || "";
    return hasCjk(crumb) ? "" : crumb;
  }

  function displayExcerpt(meta, excerpt, query) {
    const q = (query || activeQuery || "").trim();
    if (isMathAbbrev(q)) {
      const src =
        lang() === "zh" && meta.excerpt_zh && mathAbbrevInText(meta.excerpt_zh, q)
          ? meta.excerpt_zh
          : cleanExcerpt(excerpt);
      return highlightQuery(truncatePlain(src, 220), q);
    }
    if (lang() === "zh" && meta.excerpt_zh) {
      const raw = cleanExcerpt(excerpt);
      if (excerptLang(excerpt) === "en" || !hasCjk(raw)) {
        return highlightQuery(truncatePlain(meta.excerpt_zh, 220), q);
      }
    }
    if (/<mark\b/i.test(excerpt) || /pagefind__highlight/i.test(excerpt)) {
      return sanitizePagefindExcerpt(excerpt);
    }
    return highlightQuery(truncatePlain(cleanExcerpt(excerpt), 220), q);
  }

  function t(key) {
    return COPY[lang()][key] || COPY.en[key];
  }

  function getSiteBaseUrl() {
    const s = document.querySelector('script[src*="kiwi-site-search.js"]');
    if (!s || !s.src) {
      return new URL("./", window.location.href);
    }
    return new URL("../../", s.src);
  }

  function useCleanPublicUrls() {
    const path = window.location.pathname || "";
    if (/\.html?$/i.test(path)) return false;
    const host = (window.location.hostname || "").toLowerCase();
    return host === "localhost" || host === "127.0.0.1";
  }

  /** GitHub project Pages prefix (e.g. kiwi-ai-study), empty at domain root or localhost. */
  function sitePathPrefix() {
    const p = getSiteBaseUrl().pathname.replace(/\/$/, "");
    if (!p || p === "/") return "";
    return p.replace(/^\//, "");
  }

  function stripSitePathPrefix(relPath) {
    let p = String(relPath || "").replace(/^\/+/, "");
    const prefix = sitePathPrefix();
    if (!prefix) return p;
    if (p === prefix) return "";
    if (p.startsWith(prefix + "/")) return p.slice(prefix.length + 1);
    return p;
  }

  function canonicalFilePath(rawPath) {
    let path = String(rawPath || "")
      .trim()
      .replace(/[#?].*$/, "")
      .replace(/^\/+/, "");
    if (!path) return "index.html";
    if (/^https?:\/\//i.test(rawPath)) {
      try {
        path = new URL(rawPath).pathname.replace(/^\/+/, "");
      } catch (_) {
        /* keep path */
      }
    }
    path = stripSitePathPrefix(path);
    if (!/\.html?$/i.test(path)) {
      if (!path.includes("/")) {
        if (/^episode-\d+$/i.test(path)) path = "ai/" + path;
        else if (/^(about|contact|books)$/i.test(path)) path = path + "/index";
        else if (path === "index") path = "index";
        else if (path === "ai") path = "ai/index";
        else if (path === "math") path = "math/index";
        else path = "math/" + path;
      }
      if (!/\.html?$/i.test(path)) path += ".html";
    }
    return path.replace(/^\/+/, "");
  }

  function publicHrefFromFile(filePath) {
    const base = getSiteBaseUrl();
    const rel = stripSitePathPrefix(filePath);
    if (useCleanPublicUrls()) {
      if (rel.startsWith("math/") && rel.endsWith(".html")) {
        const slug = rel.slice(5, -5);
        if (slug === "index") return new URL("/math", base).pathname;
        return new URL("/" + slug, base).pathname;
      }
      if (rel.startsWith("ai/episode-") && rel.endsWith(".html")) {
        return new URL("/" + rel.slice(3, -5), base).pathname;
      }
      if (rel === "ai/index.html") return new URL("/ai", base).pathname;
      if (rel === "index.html") return new URL("/", base).pathname;
      const hub = rel.match(/^(about|contact|books)\/index\.html$/);
      if (hub) return new URL("/" + hub[1], base).pathname;
    }
    try {
      return new URL(rel, base).pathname;
    } catch (_) {
      return "/" + rel;
    }
  }

  function resolveSearchHref(rawUrl) {
    if (!rawUrl) return rawUrl;
    if (/^https?:\/\//i.test(rawUrl)) {
      try {
        const u = new URL(rawUrl);
        const tail = u.search + u.hash;
        return publicHrefFromFile(canonicalFilePath(u.pathname)) + tail;
      } catch (_) {
        return rawUrl;
      }
    }
    const hash = (String(rawUrl).match(/#.*$/) || [""])[0];
    const search = (String(rawUrl).match(/\?.*$/) || [""])[0];
    return publicHrefFromFile(canonicalFilePath(rawUrl)) + search + hash;
  }

  let pagefindApi = null;
  let initPromise = null;
  let pagefindUnavailable = false;

  async function getPagefind() {
    if (pagefindUnavailable) return null;
    if (pagefindApi) return pagefindApi;
    if (!initPromise) {
      initPromise = (async () => {
        try {
          const base = getSiteBaseUrl();
          const modUrl = new URL("pagefind/pagefind.js", base);
          const mod = await import(modUrl.href);
          const basePath = base.pathname.endsWith("/") ? base.pathname : base.pathname + "/";
          await mod.init({ basePath: basePath });
          pagefindApi = mod;
          return mod;
        } catch (err) {
          pagefindUnavailable = true;
          console.warn("Kiwi search: Pagefind unavailable", err);
          return null;
        }
      })();
    }
    return initPromise;
  }

  function updateHeaderOffset() {
    const hdr = document.querySelector(".site-header");
    if (!hdr) {
      document.documentElement.style.setProperty("--kiwi-header-height", "73px");
      return;
    }
    const rect = hdr.getBoundingClientRect();
    const bottom = Math.max(Math.ceil(rect.bottom), Math.ceil(rect.height), 73);
    document.documentElement.style.setProperty("--kiwi-header-height", bottom + "px");
  }

  function watchHeaderResize() {
    const hdr = document.querySelector(".site-header");
    if (!hdr || typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(function () {
      updateHeaderOffset();
    });
    ro.observe(hdr);
  }

  function getSearchRoot() {
    return document.getElementById("kiwi-search-root");
  }

  function isSearchOpen() {
    const root = getSearchRoot();
    return root && !root.hidden;
  }

  function closeSearch() {
    const root = getSearchRoot();
    if (!root || root.hidden) return;
    root.hidden = true;
    const input = root.querySelector("[data-kiwi-search-input]");
    if (input) input.value = "";
    root.querySelector("[data-kiwi-search-results]").innerHTML = "";
    const off = root.querySelector("[data-kiwi-search-offline]");
    if (off) off.hidden = true;
    document.body.classList.remove("kiwi-search-open");
  }

  function createModal() {
    if (getSearchRoot()) return;
    const root = document.createElement("div");
    root.id = "kiwi-search-root";
    root.className = "kiwi-search-root";
    root.hidden = true;
    root.innerHTML =
      '<div class="kiwi-search-scrim" data-kiwi-search-backdrop aria-hidden="true"></div>' +
      '<div class="kiwi-search-panel" role="dialog" aria-modal="true" aria-labelledby="kiwi-search-title-id">' +
      '<form class="kiwi-search-form" role="search" onsubmit="return false">' +
      '<header class="kiwi-search-header">' +
      '<h2 class="kiwi-search-title" id="kiwi-search-title-id" data-kiwi-search-title></h2>' +
      '<button type="button" class="kiwi-search-close" data-kiwi-search-close aria-label="">×</button>' +
      "</header>" +
      '<div class="kiwi-search-scope-row" data-kiwi-search-scope-row hidden>' +
      '<span data-kiwi-search-scope-label></span>' +
      '<button type="button" class="kiwi-search-scope-clear" data-kiwi-search-scope-clear></button>' +
      "</div>" +
      '<input type="search" class="kiwi-search-input" data-kiwi-search-input autocomplete="off" spellcheck="false" />' +
      '<p class="kiwi-search-hint" data-kiwi-search-hint></p>' +
      '<p class="kiwi-search-offline" data-kiwi-search-offline hidden></p>' +
      '<ul class="kiwi-search-results" data-kiwi-search-results role="listbox" aria-live="polite"></ul>' +
      "</form></div>";
    document.body.appendChild(root);
    root.querySelector("[data-kiwi-search-backdrop]")?.addEventListener("click", closeSearch);
    root.querySelector("[data-kiwi-search-close]")?.addEventListener("click", closeSearch);
  }

  function ensureHeaderButton() {
    const nav = document.querySelector(".site-nav");
    const flags = nav && nav.querySelector(".flags");
    if (!nav || !flags) return;
    let btn = nav.querySelector(".kiwi-search-open");
    if (!btn) {
      btn = document.createElement("button");
      btn.type = "button";
      btn.className = "kiwi-search-open";
      btn.setAttribute("data-kiwi-search-trigger", "");
      nav.insertBefore(btn, flags);
    }
    btn.setAttribute("aria-label", t("open"));
    btn.innerHTML =
      '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/><path d="M20 20l-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
    if (!btn.dataset.kiwiBound) {
      btn.dataset.kiwiBound = "1";
      btn.addEventListener("click", () => openSearch({ scope: null }));
    }
  }

  let activeScope = null;

  function syncModalCopy() {
    const root = getSearchRoot();
    if (!root) return;
    root.querySelector("[data-kiwi-search-title]").textContent = t("title");
    root.querySelector("[data-kiwi-search-input]").placeholder = t("placeholder");
    root.querySelector("[data-kiwi-search-hint]").textContent = t("hint");
    root.querySelector("[data-kiwi-search-close]").setAttribute("aria-label", t("close"));
    const scopeRow = root.querySelector("[data-kiwi-search-scope-row]");
    const scopeLabel = root.querySelector("[data-kiwi-search-scope-label]");
    const clearBtn = root.querySelector("[data-kiwi-search-scope-clear]");
    if (activeScope === "math") {
      scopeRow.hidden = false;
      scopeLabel.textContent = t("scopeMath");
      clearBtn.textContent = t("scopeAll");
    } else {
      scopeRow.hidden = true;
    }
    ensureHeaderButton();
  }

  function openSearch(opts) {
    opts = opts || {};
    activeScope = opts.scope || null;
    createModal();
    if (window.scrollY > 0) {
      window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
    }
    updateHeaderOffset();
    syncModalCopy();
    const root = getSearchRoot();
    root.hidden = false;
    document.body.classList.add("kiwi-search-open");
    requestAnimationFrame(function () {
      updateHeaderOffset();
      requestAnimationFrame(updateHeaderOffset);
    });
    const input = root.querySelector("[data-kiwi-search-input]");
    input.value = opts.initialQuery || "";
    input.focus();
    runSearch(input.value);
  }

  async function runSearch(query) {
    const root = getSearchRoot();
    if (!root) return;
    const list = root.querySelector("[data-kiwi-search-results]");
    const offlineEl = root.querySelector("[data-kiwi-search-offline]");
    const q = (query || "").trim();
    activeQuery = q;
    if (!q) {
      list.innerHTML = "";
      if (offlineEl) offlineEl.hidden = true;
      return;
    }

    const pf = await getPagefind();
    if (!pf) {
      if (offlineEl) {
        offlineEl.textContent = t("offline");
        offlineEl.hidden = false;
      }
      list.innerHTML = "";
      return;
    }
    if (offlineEl) offlineEl.hidden = true;

    try {
      let response;
      if (isMathAbbrev(q)) {
        const loose = { filters: { section: activeScope || "math" } };
        response = await pf.search(q, loose);
      } else {
        const options = { filters: { lang: lang() } };
        if (activeScope) options.filters.section = activeScope;
        response = await pf.search(q, options);
      }
      const items = response.results.slice(0, 24);
      if (!items.length) {
        list.innerHTML = '<li class="kiwi-search-empty">' + t("empty") + "</li>";
        return;
      }
      const rows = await Promise.all(
        items.map(async (r) => {
          const data = await r.data();
          const meta = data.meta || {};
          const excerpt = data.excerpt || "";
          if (!excerptIsReadable(excerpt, q)) return null;
          if (isMathAbbrev(q) && !hitIsMathSection(meta, data.url)) return null;
          if (!hitMatchesActiveLang(excerpt, meta, q)) return null;
          const title = displayTitle(meta, excerpt, data.url);
          return {
            url: resolveSearchHref(data.url),
            title: highlightQuery(title, q),
            crumb: escapeHtml(displayCrumb(meta)),
            excerpt: displayExcerpt(meta, excerpt, q),
          };
        }),
      );
      const visible = rows.filter(Boolean).slice(0, 12);
      if (!visible.length) {
        list.innerHTML = '<li class="kiwi-search-empty">' + t("empty") + "</li>";
        return;
      }
      list.innerHTML = visible
        .map(function (row) {
          return (
            '<li class="kiwi-search-hit"><a href="' +
            row.url +
            '"><span class="kiwi-search-hit-title">' +
            row.title +
            "</span>" +
            (row.crumb ? '<span class="kiwi-search-hit-crumb">' + row.crumb + "</span>" : "") +
            (row.excerpt ? '<span class="kiwi-search-hit-excerpt">' + row.excerpt + "</span>" : "") +
            "</a></li>"
          );
        })
        .join("");
    } catch (err) {
      list.innerHTML = '<li class="kiwi-search-empty">' + t("empty") + "</li>";
      console.warn("Kiwi search:", err);
    }
  }

  function bindKeys() {
    document.addEventListener("keydown", function (e) {
      const tag = e.target && e.target.tagName;
      const inField = tag && /input|textarea|select/i.test(tag);
      if (e.key === "Escape" && isSearchOpen()) {
        e.preventDefault();
        closeSearch();
        return;
      }
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (isSearchOpen()) closeSearch();
        else openSearch({ scope: activeScope });
        return;
      }
      if (e.key === "/" && !inField && !isSearchOpen()) {
        e.preventDefault();
        openSearch({ scope: null });
      }
    });
    window.addEventListener("resize", updateHeaderOffset);
  }

  function bindDialogSearch() {
    const root = getSearchRoot();
    if (!root) return;
    const input = root.querySelector("[data-kiwi-search-input]");
    let timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        runSearch(input.value);
      }, 120);
    });
    root.querySelector("[data-kiwi-search-scope-clear]")?.addEventListener("click", function () {
      activeScope = null;
      syncModalCopy();
      runSearch(input.value);
    });
  }

  function watchLanguage() {
    new MutationObserver(function () {
      syncModalCopy();
      pagefindApi = null;
      initPromise = null;
      const root = getSearchRoot();
      if (!root || root.hidden) return;
      const input = root.querySelector("[data-kiwi-search-input]");
      if (input) runSearch(input.value);
    }).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["lang"],
    });
  }

  function init() {
    createModal();
    ensureHeaderButton();
    updateHeaderOffset();
    watchHeaderResize();
    bindKeys();
    bindDialogSearch();
    watchLanguage();
    syncModalCopy();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();