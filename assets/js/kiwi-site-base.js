(function () {
  "use strict";

  var REPO_PREFIX = "kiwi-ai-study";

  function detectSiteBase() {
    var host = (location.hostname || "").toLowerCase();
    if (host === "localhost" || host === "127.0.0.1") {
      return "/" + REPO_PREFIX;
    }
    /* GitHub project Pages: always /{repo}/… — root-relative /grade-3 must not escape. */
    if (host.slice(-".github.io".length) === ".github.io") {
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
    root.querySelectorAll("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (!h || h.indexOf("://") >= 0 || h.indexOf("//") === 0) return;
      if (h.charAt(0) === "/") {
        if (/^\/[a-z0-9][\w.-]*\.html$/i.test(h)) {
          h = h.replace(/\.html$/i, "");
        }
        var fixed = kiwiRootHref(h);
        if (fixed !== a.getAttribute("href")) a.setAttribute("href", fixed);
        return;
      }
      var qIdx = h.indexOf("?");
      var pathOnly = qIdx >= 0 ? h.slice(0, qIdx) : h;
      var query = qIdx >= 0 ? h.slice(qIdx) : "";
      var hashIdx = pathOnly.indexOf("#");
      if (hashIdx > 0) {
        var pathPart = pathOnly.slice(0, hashIdx);
        var frag = pathOnly.slice(hashIdx) + query;
        if (pathPart.indexOf("/") < 0 && /\.html$/i.test(pathPart)) {
          a.setAttribute(
            "href",
            kiwiRootHref("/" + pathPart.replace(/\.html$/i, "") + frag),
          );
          return;
        }
      }
      if (pathOnly.indexOf("/") >= 0 || pathOnly.indexOf("#") === 0) {
        if (query && pathOnly.indexOf("/") < 0 && /\.html$/i.test(pathOnly)) {
          a.setAttribute(
            "href",
            kiwiRootHref("/" + pathOnly.replace(/\.html$/i, "") + query),
          );
        }
        return;
      }
      if (/^[a-z0-9][\w.-]*\.html$/i.test(pathOnly)) {
        a.setAttribute(
          "href",
          kiwiRootHref("/" + pathOnly.replace(/\.html$/i, "") + query),
        );
        return;
      }
      if (h === "index.html") {
        a.setAttribute("href", kiwiRootHref("/math"));
      }
    });
  }

  function install() {
    patchRootLinks(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install);
  } else {
    install();
  }

  new MutationObserver(function () {
    install();
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["lang", "data-language"],
  });
})();