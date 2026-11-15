(function () {
  "use strict";

  var REPO_PREFIX = "kiwi-ai-study";

  function detectSiteBase() {
    var host = (location.hostname || "").toLowerCase();
    if (host === "localhost" || host === "127.0.0.1") {
      return "/" + REPO_PREFIX;
    }
    var path = location.pathname || "";
    if (path === "/" + REPO_PREFIX || path.indexOf("/" + REPO_PREFIX + "/") === 0) {
      return "/" + REPO_PREFIX;
    }
    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
      var src = scripts[i].src;
      if (!src || src.indexOf("assets/js/") === -1) continue;
      try {
        var u = new URL(src, location.href);
        var m = u.pathname.match(new RegExp("^/(?:" + REPO_PREFIX + ")/"));
        if (m) return "/" + REPO_PREFIX;
      } catch (_) {
        /* ignore */
      }
    }
    return "";
  }

  var base = detectSiteBase();
  window.KIWI_SITE_BASE = base;

  function kiwiRootHref(href) {
    if (!href || typeof href !== "string") return href;
    if (href.charAt(0) !== "/" || href.indexOf("//") === 0) return href;
    if (!base) return href;
    if (href === base || href.indexOf(base + "/") === 0) return href;
    return base + href;
  }
  window.kiwiRootHref = kiwiRootHref;

  function patchRootLinks(root) {
    root.querySelectorAll('a[href^="/"]').forEach(function (a) {
      var h = a.getAttribute("href");
      if (!h || h.indexOf("//") === 0) return;
      var fixed = kiwiRootHref(h);
      if (fixed !== h) a.setAttribute("href", fixed);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      patchRootLinks(document);
    });
  } else {
    patchRootLinks(document);
  }
})();