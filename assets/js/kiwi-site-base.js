(function () {
  "use strict";

  var REPO_PREFIX = "kiwi-ai-study";
  /* KIWI_GITHUB_SLUG_DEST_BEGIN */
  window.KIWI_GITHUB_SLUG_DEST={"algebraic-strategies": "/kiwi-ai-study/math/thinking-algebraic-strategies.html", "books-advanced": "/kiwi-ai-study/books/books-advanced.html", "books-foundations": "/kiwi-ai-study/books/books-foundations.html", "books-speedy": "/kiwi-ai-study/books/books-speedy.html", "by-grade": "/kiwi-ai-study/math/by-grade.html", "by-ontario-course": "/kiwi-ai-study/math/by-ontario-course.html", "car-journey": "/kiwi-ai-study/math/car-journey.html", "car-journey-advanced": "/kiwi-ai-study/math/thinking-car-journey-advanced.html", "chance-and-probability": "/kiwi-ai-study/math/thinking-chance-and-probability.html", "data-and-graphs": "/kiwi-ai-study/math/thinking-data-and-graphs.html", "episode-01": "/kiwi-ai-study/ai/episode-01.html", "episode-02": "/kiwi-ai-study/ai/episode-02.html", "episode-03": "/kiwi-ai-study/ai/episode-03.html", "episode-04": "/kiwi-ai-study/ai/episode-04.html", "episode-05": "/kiwi-ai-study/ai/episode-05.html", "episode-06": "/kiwi-ai-study/ai/episode-06.html", "episode-07": "/kiwi-ai-study/ai/episode-07.html", "episode-08": "/kiwi-ai-study/ai/episode-08.html", "episode-09": "/kiwi-ai-study/ai/episode-09.html", "episode-10": "/kiwi-ai-study/ai/episode-10.html", "episode-11": "/kiwi-ai-study/ai/episode-11.html", "episode-12": "/kiwi-ai-study/ai/episode-12.html", "episode-13": "/kiwi-ai-study/ai/episode-13.html", "episode-14": "/kiwi-ai-study/ai/episode-14.html", "episode-15": "/kiwi-ai-study/ai/episode-15.html", "episode-special-learning": "/kiwi-ai-study/ai/episode-special-learning.html", "foundation-algebra-language-and-patterns": "/kiwi-ai-study/math/foundation-algebra-language-and-patterns.html", "foundation-algebraic-strategies": "/kiwi-ai-study/math/foundation-algebraic-strategies.html", "foundation-angles-and-trigonometric-ratios": "/kiwi-ai-study/math/foundation-angles-and-trigonometric-ratios.html", "foundation-angles-in-standard-position": "/kiwi-ai-study/math/foundation-angles-in-standard-position.html", "foundation-basic-geometry-words": "/kiwi-ai-study/math/foundation-basic-geometry-words.html", "foundation-chance-and-probability": "/kiwi-ai-study/math/foundation-chance-and-probability.html", "foundation-choosing-trigonometry-laws": "/kiwi-ai-study/math/foundation-choosing-trigonometry-laws.html", "foundation-data-and-graphs": "/kiwi-ai-study/math/foundation-data-and-graphs.html", "foundation-decimal": "/kiwi-ai-study/math/foundation-decimal.html", "foundation-decimal-to-fraction": "/kiwi-ai-study/math/foundation-decimal-to-fraction.html", "foundation-division-rules-2-9": "/kiwi-ai-study/math/foundation-division-rules-2-9.html", "foundation-exact-trigonometric-values": "/kiwi-ai-study/math/foundation-exact-trigonometric-values.html", "foundation-exponents": "/kiwi-ai-study/math/foundation-exponents.html", "foundation-function-transformations": "/kiwi-ai-study/math/foundation-function-transformations.html", "foundation-functions-and-their-inverses": "/kiwi-ai-study/math/foundation-functions-and-their-inverses.html", "foundation-geometric-strategies": "/kiwi-ai-study/math/foundation-geometric-strategies.html", "foundation-greatest-common-factor-gcf": "/kiwi-ai-study/math/foundation-greatest-common-factor-gcf.html", "foundation-law-of-cosines": "/kiwi-ai-study/math/foundation-law-of-cosines.html", "foundation-linear-vs-non-linear-functions": "/kiwi-ai-study/math/foundation-linear-vs-non-linear-functions.html", "foundation-math-operation-signs-and": "/kiwi-ai-study/math/foundation-math-operation-signs-and.html", "foundation-measures-of-center": "/kiwi-ai-study/math/foundation-measures-of-center.html", "foundation-number-families": "/kiwi-ai-study/math/foundation-number-families.html", "foundation-number-strategies": "/kiwi-ai-study/math/foundation-number-strategies.html", "foundation-oblique-triangles-and-triangle-laws": "/kiwi-ai-study/math/foundation-oblique-triangles-and-triangle-laws.html", "foundation-proving-trigonometric-identities": "/kiwi-ai-study/math/foundation-proving-trigonometric-identities.html", "foundation-pythagorean-identity": "/kiwi-ai-study/math/foundation-pythagorean-identity.html", "foundation-quotient-identities": "/kiwi-ai-study/math/foundation-quotient-identities.html", "foundation-rational-exponents": "/kiwi-ai-study/math/foundation-rational-exponents.html", "foundation-reciprocal-identities": "/kiwi-ai-study/math/foundation-reciprocal-identities.html", "foundation-reciprocal-trigonometric-ratios": "/kiwi-ai-study/math/foundation-reciprocal-trigonometric-ratios.html", "foundation-related-and-coterminal-angles": "/kiwi-ai-study/math/foundation-related-and-coterminal-angles.html", "foundation-result-signs-and": "/kiwi-ai-study/math/foundation-result-signs-and.html", "foundation-roots": "/kiwi-ai-study/math/foundation-roots.html", "foundation-rotation-transformation": "/kiwi-ai-study/math/foundation-rotation-transformation.html", "foundation-sine-law": "/kiwi-ai-study/math/foundation-sine-law.html", "foundation-six-trigonometric-functions-unit-circle": "/kiwi-ai-study/math/foundation-six-trigonometric-functions-unit-circle.html", "foundation-special-right-triangles": "/kiwi-ai-study/math/foundation-special-right-triangles.html", "foundation-ssa-ambiguous-case": "/kiwi-ai-study/math/foundation-ssa-ambiguous-case.html", "foundation-step-pattern-and-first-differences-y": "/kiwi-ai-study/math/foundation-step-pattern-and-first-differences-y.html", "foundation-the-four-basic-trigonometric-ratios": "/kiwi-ai-study/math/foundation-the-four-basic-trigonometric-ratios.html", "foundation-the-three-sides-of-a-right-triangle": "/kiwi-ai-study/math/foundation-the-three-sides-of-a-right-triangle.html", "foundation-trigonometric-identities": "/kiwi-ai-study/math/foundation-trigonometric-identities.html", "foundation-trigonometric-identities-quick-checks": "/kiwi-ai-study/math/foundation-trigonometric-identities-quick-checks.html", "foundation-trigonometric-ratios-beyond-90": "/kiwi-ai-study/math/foundation-trigonometric-ratios-beyond-90.html", "foundation-trigonometry-3d-applications": "/kiwi-ai-study/math/foundation-trigonometry-3d-applications.html", "foundation-trigonometry-fundamentals": "/kiwi-ai-study/math/foundation-trigonometry-fundamentals.html", "foundation-understanding-functions": "/kiwi-ai-study/math/foundation-understanding-functions.html", "foundation-understanding-the-placeholder-in-f-x": "/kiwi-ai-study/math/foundation-understanding-the-placeholder-in-f-x.html", "foundation-understanding-trigonometry": "/kiwi-ai-study/math/foundation-understanding-trigonometry.html", "foundation-unit-conversions-and-rates": "/kiwi-ai-study/math/foundation-unit-conversions-and-rates.html", "foundation-what-is-trigonometric-identity": "/kiwi-ai-study/math/foundation-what-is-trigonometric-identity.html", "foundation-why-simplified-calculation": "/kiwi-ai-study/math/foundation-why-simplified-calculation.html", "foundation-word-problems": "/kiwi-ai-study/math/foundation-word-problems.html", "gcf": "/kiwi-ai-study/math/thinking-greatest-common-factor-gcf.html", "geometric-strategies": "/kiwi-ai-study/math/thinking-geometric-strategies.html", "grade-10": "/kiwi-ai-study/math/grade-10.html", "grade-11": "/kiwi-ai-study/math/grade-11.html", "grade-3": "/kiwi-ai-study/math/grade-3.html", "grade-4": "/kiwi-ai-study/math/grade-4.html", "grade-5": "/kiwi-ai-study/math/grade-5.html", "grade-6": "/kiwi-ai-study/math/grade-6.html", "grade-7": "/kiwi-ai-study/math/grade-7.html", "grade-8": "/kiwi-ai-study/math/grade-8.html", "grade-9": "/kiwi-ai-study/math/grade-9.html", "in-class-learning": "/kiwi-ai-study/math/in-class-learning.html", "math-foundations": "/kiwi-ai-study/math/math-foundations.html", "math-real-life": "/kiwi-ai-study/math/math-real-life.html", "mathematical-thinking": "/kiwi-ai-study/math/mathematical-thinking.html", "measures-of-center": "/kiwi-ai-study/math/thinking-measures-of-center.html", "mental-squaring-and-square-rooting": "/kiwi-ai-study/math/thinking-mental-squaring-and-square-rooting.html", "number-families": "/kiwi-ai-study/math/foundation-number-families.html", "number-shape-thinking": "/kiwi-ai-study/math/thinking-number-shape-thinking.html", "number-strategies": "/kiwi-ai-study/math/thinking-number-strategies.html", "recovering-function-rule": "/kiwi-ai-study/math/thinking-recovering-function-rule.html", "rotation-transformation": "/kiwi-ai-study/math/thinking-rotation-transformation.html", "skateboard-ramp": "/kiwi-ai-study/math/skateboard-ramp.html", "special-right-triangles": "/kiwi-ai-study/math/thinking-special-right-triangles.html", "speedy-playful-math-magic": "/kiwi-ai-study/books/speedy-playful-math-magic.html", "thinking-algebraic-strategies": "/kiwi-ai-study/math/thinking-algebraic-strategies.html", "thinking-car-journey-advanced": "/kiwi-ai-study/math/thinking-car-journey-advanced.html", "thinking-chance-and-probability": "/kiwi-ai-study/math/thinking-chance-and-probability.html", "thinking-data-and-graphs": "/kiwi-ai-study/math/thinking-data-and-graphs.html", "thinking-geometric-strategies": "/kiwi-ai-study/math/thinking-geometric-strategies.html", "thinking-greatest-common-factor-gcf": "/kiwi-ai-study/math/thinking-greatest-common-factor-gcf.html", "thinking-imaginary-complex-numbers": "/kiwi-ai-study/math/thinking-imaginary-complex-numbers.html", "thinking-measures-of-center": "/kiwi-ai-study/math/thinking-measures-of-center.html", "thinking-mental-squaring-and-square-rooting": "/kiwi-ai-study/math/thinking-mental-squaring-and-square-rooting.html", "thinking-number-shape-thinking": "/kiwi-ai-study/math/thinking-number-shape-thinking.html", "thinking-number-strategies": "/kiwi-ai-study/math/thinking-number-strategies.html", "thinking-recovering-function-rule": "/kiwi-ai-study/math/thinking-recovering-function-rule.html", "thinking-rotation-transformation": "/kiwi-ai-study/math/thinking-rotation-transformation.html", "thinking-special-right-triangles": "/kiwi-ai-study/math/thinking-special-right-triangles.html", "thinking-unit-conversions-and-rates": "/kiwi-ai-study/math/thinking-unit-conversions-and-rates.html", "thinking-why-simplified-calculation": "/kiwi-ai-study/math/thinking-why-simplified-calculation.html", "thinking-word-problems": "/kiwi-ai-study/math/thinking-word-problems.html", "unit-conversions-and-rates": "/kiwi-ai-study/math/thinking-unit-conversions-and-rates.html", "visual-math-patterns": "/kiwi-ai-study/math/visual-math-patterns.html", "why-simplified-calculation": "/kiwi-ai-study/math/thinking-why-simplified-calculation.html", "word-problems": "/kiwi-ai-study/math/thinking-word-problems.html"};
  /* KIWI_GITHUB_SLUG_DEST_END */

  function isGithubPages() {
    return (
      (location.hostname || "").toLowerCase().slice(-".github.io".length) ===
      ".github.io"
    );
  }

  function resolveGithubDirectHref(href) {
    if (!isGithubPages()) return null;
    var map = window.KIWI_GITHUB_SLUG_DEST;
    if (!map || typeof map !== "object") return null;
    if (!href || href.charAt(0) !== "/" || href.indexOf("//") === 0) return null;

    var hashIdx = href.indexOf("#");
    var queryIdx = href.indexOf("?");
    var end = href.length;
    if (queryIdx >= 0) end = queryIdx;
    else if (hashIdx >= 0) end = hashIdx;
    var pathOnly = href.slice(0, end);
    var suffix = href.slice(end);

    var slug = pathOnly.slice(1);
    if (slug.indexOf(REPO_PREFIX + "/") === 0) {
      slug = slug.slice(REPO_PREFIX.length + 1);
    } else if (slug === REPO_PREFIX) {
      return null;
    }
    if (!slug || slug.indexOf("/") >= 0) return null;

    var dest = map[slug];
    if (!dest) return null;
    return dest + suffix;
  }

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
    var direct = resolveGithubDirectHref(href);
    if (direct) return direct;
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
        var direct = resolveGithubDirectHref(h);
        if (direct) {
          a.setAttribute("href", direct);
          return;
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