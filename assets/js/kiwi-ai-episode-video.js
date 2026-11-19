(() => {
  const DATA_URL = (() => {
    const base = document.querySelector('script[src*="kiwi-ai-episode-video"]');
    const fallback = "../data/ai-episode-videos.json";
    if (!base || !base.src) return fallback;
    try {
      const u = new URL(base.src);
      const fromAssetsJs = new URL("../../data/ai-episode-videos.json", u).pathname;
      if (/\/data\/ai-episode-videos\.json$/i.test(fromAssetsJs)) return fromAssetsJs;
    } catch (_e) {
      /* use fallback */
    }
    const kbase =
      typeof window.KIWI_SITE_BASE === "string" && window.KIWI_SITE_BASE
        ? window.KIWI_SITE_BASE.replace(/\/?$/, "/")
        : "";
    return (kbase + "data/ai-episode-videos.json").replace(/\/{2,}/g, "/");
  })();

  const COPY = {
    en: {
      watchTitle: "Watch this episode",
      watchYouTube: "Watch on YouTube",
      watchRednote: "Watch on Rednote (小红书)",
      cardPlay: "Video available"
    },
    zh: {
      watchTitle: "观看本集视频",
      watchYouTube: "在 YouTube 观看",
      watchRednote: "在小红书观看",
      cardPlay: "有视频版"
    }
  };

  let catalog = null;
  let catalogPromise = null;

  function currentLang() {
    try {
      return localStorage.getItem("kiwi-site-language") === "zh" ? "zh" : "en";
    } catch (_e) {
      return "en";
    }
  }

  function loadCatalog() {
    if (catalog) return Promise.resolve(catalog);
    if (!catalogPromise) {
      catalogPromise = fetch(DATA_URL + "?v=20261118-rednote-discovery")
        .then((r) => (r.ok ? r.json() : {}))
        .catch(() => ({}))
        .then((data) => {
          catalog = data && typeof data === "object" ? data : {};
          return catalog;
        });
    }
    return catalogPromise;
  }

  function episodeIdFromHref(href) {
    if (!href) return null;
    const base = String(href).split("?")[0].split("#")[0];
    const m = base.match(/episode-(\d{2})(?:\.html)?$/i);
    if (m) return m[1];
    if (/episode-special-learning(?:\.html)?$/i.test(base)) return "special-learning";
    return null;
  }

  function episodeIdFromPath() {
    const parts = location.pathname.split("/").filter(Boolean);
    let name = (parts.pop() || "").toLowerCase();
    if (name === "index.html" || name === "") {
      name = (parts.pop() || "").toLowerCase();
    }
    if (!name || name === "ai" || name === "kiwi-ai-study") return null;
    return episodeIdFromHref(name);
  }

  function videoUrlForEpisode(entry, lang) {
    if (!entry) return null;
    return lang === "zh" ? entry.rednote || null : entry.youtube || null;
  }

  function platformForLang(lang) {
    return lang === "zh" ? "rednote" : "youtube";
  }

  function iconSrc(platform, transparent) {
    const root = "../assets/social/";
    if (transparent) {
      return platform === "rednote"
        ? root + "xiaohongshu-watch-d-trim.webp"
        : root + "youtube-watch-icon.svg";
    }
    return platform === "rednote"
      ? root + "Xiaohongshu-reference.webp"
      : root + "YouTube-reference.webp";
  }

  function applyWatchBlock(wrap, entry) {
    const lang = currentLang();
    const c = COPY[lang];
    const platform = platformForLang(lang);
    const url = videoUrlForEpisode(entry, lang);
    const btn = wrap.querySelector(".kiwi-episode-watch-btn");
    if (!btn) return;
    if (!url) {
      wrap.hidden = true;
      const off = wrap.closest(".topic-banner");
      if (off) off.classList.remove("topic-banner--has-video");
      return;
    }
    wrap.hidden = false;
    const banner = wrap.closest(".topic-banner");
    if (banner) banner.classList.add("topic-banner--has-video");
    btn.href = url;
    btn.target = "_blank";
    btn.rel = "noopener noreferrer";
    btn.classList.toggle("kiwi-episode-watch-btn--rednote", platform === "rednote");
    const img = btn.querySelector("img");
    if (img) {
      const transparent = wrap.classList.contains("kiwi-episode-watch--banner");
      img.src = iconSrc(platform, transparent);
      img.alt = "";
    }
    const ep = wrap.dataset.kiwiEpisodeId || "";
    btn.setAttribute(
      "aria-label",
      (platform === "rednote" ? c.watchRednote : c.watchYouTube) + (ep ? ` (${ep})` : "")
    );
  }

  function ensureEpisodeWatchStrip(entry, episodeId) {
    const banner = document.querySelector(".topic-banner, .nf-hero.topic-banner");
    if (!banner) return;
    const legacy = document.querySelector(
      "[data-kiwi-episode-watch]:not(.kiwi-episode-watch--banner)"
    );
    if (legacy) legacy.remove();
    let wrap = banner.querySelector("[data-kiwi-episode-watch]");
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "kiwi-episode-watch kiwi-episode-watch--banner";
      wrap.dataset.kiwiEpisodeWatch = "1";
      wrap.dataset.kiwiEpisodeId = episodeId;
      wrap.innerHTML =
        '<a class="kiwi-episode-watch-btn" href="#">' +
        '<img width="72" height="40" alt="" decoding="async"></a>';
      banner.appendChild(wrap);
    }
    applyWatchBlock(wrap, entry);
  }

  function refreshAllWatchBlocks() {
    document.querySelectorAll("[data-kiwi-episode-watch]").forEach((wrap) => {
      const id = wrap.dataset.kiwiEpisodeId;
      if (id && catalog && catalog[id]) applyWatchBlock(wrap, catalog[id]);
    });
  }

  function decorateHubCards() {
    const grid = document.getElementById("ai-episode-grid");
    if (!grid || !catalog) return;
    const lang = currentLang();
    const c = COPY[lang];
    grid.querySelectorAll("a.ai-episode[href]").forEach((card) => {
      const id = episodeIdFromHref(card.getAttribute("href"));
      if (!id || !catalog[id]) return;
      const entry = catalog[id];
      const url = videoUrlForEpisode(entry, lang);
      if (!url) return;
      card.classList.add("ai-episode-has-video");
      card.dataset.kiwiEpisodeId = id;
      let art = card.querySelector(".ai-episode-art");
      if (!art) return;
      if (!art.querySelector(".kiwi-episode-card-play")) {
        const badge = document.createElement("span");
        badge.className = "kiwi-episode-card-play";
        badge.setAttribute("aria-hidden", "true");
        badge.textContent = "▶";
        art.appendChild(badge);
      }
      let hint = card.querySelector(".kiwi-episode-watch-hint");
      if (!hint) {
        hint = document.createElement("p");
        hint.className = "kiwi-episode-watch-hint";
        hint.textContent = c.cardPlay;
        const body = card.querySelector(".ai-episode-body");
        if (body) body.appendChild(hint);
      } else {
        hint.textContent = c.cardPlay;
      }
    });
  }

  function bindLanguageRefresh() {
    document.querySelectorAll(".flag[data-language]").forEach((btn) => {
      btn.addEventListener("click", () => {
        setTimeout(() => {
          refreshAllWatchBlocks();
          decorateHubCards();
        }, 0);
      });
    });
    window.addEventListener("pageshow", () => {
      refreshAllWatchBlocks();
      decorateHubCards();
    });
  }

  function init() {
    loadCatalog().then((data) => {
      const onEpisode = episodeIdFromPath();
      if (onEpisode && data[onEpisode]) {
        ensureEpisodeWatchStrip(data[onEpisode], onEpisode);
      }
      if (document.getElementById("ai-episode-grid")) {
        decorateHubCards();
      }
      bindLanguageRefresh();
    });
  }

  window.kiwiAiEpisodeVideo = {
    refresh: () => {
      refreshAllWatchBlocks();
      decorateHubCards();
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();