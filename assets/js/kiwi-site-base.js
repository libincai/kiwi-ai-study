(function () {
  "use strict";

  var REPO_PREFIX = "kiwi-ai-study";
  /* KIWI_GITHUB_SLUG_DEST_BEGIN */
  window.KIWI_GITHUB_SLUG_DEST={"algebraic-strategies": "/math/thinking-algebraic-strategies.html", "books-advanced": "/books/books-advanced.html", "books-foundations": "/books/books-foundations.html", "books-speedy": "/books/books-speedy.html", "by-grade": "/math/by-grade.html", "by-ontario-course": "/math/by-ontario-course.html", "car-journey": "/math/car-journey.html", "car-journey-advanced": "/math/thinking-car-journey-advanced.html", "chance-and-probability": "/math/thinking-chance-and-probability.html", "data-and-graphs": "/math/thinking-data-and-graphs.html", "episode-01": "/ai/episode-01.html", "episode-02": "/ai/episode-02.html", "episode-03": "/ai/episode-03.html", "episode-04": "/ai/episode-04.html", "episode-05": "/ai/episode-05.html", "episode-06": "/ai/episode-06.html", "episode-07": "/ai/episode-07.html", "episode-08": "/ai/episode-08.html", "episode-09": "/ai/episode-09.html", "episode-10": "/ai/episode-10.html", "episode-11": "/ai/episode-11.html", "episode-12": "/ai/episode-12.html", "episode-13": "/ai/episode-13.html", "episode-14": "/ai/episode-14.html", "episode-15": "/ai/episode-15.html", "episode-special-learning": "/ai/episode-special-learning.html", "foundation-algebra-language-and-patterns": "/math/foundation-algebra-language-and-patterns.html", "foundation-algebraic-strategies": "/math/foundation-algebraic-strategies.html", "foundation-angles-and-trigonometric-ratios": "/math/foundation-angles-and-trigonometric-ratios.html", "foundation-angles-in-standard-position": "/math/foundation-angles-in-standard-position.html", "foundation-basic-geometry-words": "/math/foundation-basic-geometry-words.html", "foundation-chance-and-probability": "/math/foundation-chance-and-probability.html", "foundation-choosing-trigonometry-laws": "/math/foundation-choosing-trigonometry-laws.html", "foundation-data-and-graphs": "/math/foundation-data-and-graphs.html", "foundation-decimal": "/math/foundation-decimal.html", "foundation-decimal-to-fraction": "/math/foundation-decimal-to-fraction.html", "foundation-division-rules-2-9": "/math/foundation-division-rules-2-9.html", "foundation-exact-trigonometric-values": "/math/foundation-exact-trigonometric-values.html", "foundation-exponents": "/math/foundation-exponents.html", "foundation-function-transformations": "/math/foundation-function-transformations.html", "foundation-functions-and-their-inverses": "/math/foundation-functions-and-their-inverses.html", "foundation-geometric-strategies": "/math/foundation-geometric-strategies.html", "foundation-greatest-common-factor-gcf": "/math/foundation-greatest-common-factor-gcf.html", "foundation-law-of-cosines": "/math/foundation-law-of-cosines.html", "foundation-linear-vs-non-linear-functions": "/math/foundation-linear-vs-non-linear-functions.html", "foundation-math-operation-signs-and": "/math/foundation-math-operation-signs-and.html", "foundation-measures-of-center": "/math/foundation-measures-of-center.html", "foundation-number-families": "/math/foundation-number-families.html", "foundation-number-strategies": "/math/foundation-number-strategies.html", "foundation-oblique-triangles-and-triangle-laws": "/math/foundation-oblique-triangles-and-triangle-laws.html", "foundation-proving-trigonometric-identities": "/math/foundation-proving-trigonometric-identities.html", "foundation-pythagorean-identity": "/math/foundation-pythagorean-identity.html", "foundation-quotient-identities": "/math/foundation-quotient-identities.html", "foundation-rational-exponents": "/math/foundation-rational-exponents.html", "foundation-reciprocal-identities": "/math/foundation-reciprocal-identities.html", "foundation-reciprocal-trigonometric-ratios": "/math/foundation-reciprocal-trigonometric-ratios.html", "foundation-related-and-coterminal-angles": "/math/foundation-related-and-coterminal-angles.html", "foundation-result-signs-and": "/math/foundation-result-signs-and.html", "foundation-roots": "/math/foundation-roots.html", "foundation-rotation-transformation": "/math/foundation-rotation-transformation.html", "foundation-sine-law": "/math/foundation-sine-law.html", "foundation-six-trigonometric-functions-unit-circle": "/math/foundation-six-trigonometric-functions-unit-circle.html", "foundation-special-right-triangles": "/math/foundation-special-right-triangles.html", "foundation-ssa-ambiguous-case": "/math/foundation-ssa-ambiguous-case.html", "foundation-step-pattern-and-first-differences-y": "/math/foundation-step-pattern-and-first-differences-y.html", "foundation-the-four-basic-trigonometric-ratios": "/math/foundation-the-four-basic-trigonometric-ratios.html", "foundation-the-three-sides-of-a-right-triangle": "/math/foundation-the-three-sides-of-a-right-triangle.html", "foundation-trigonometric-identities": "/math/foundation-trigonometric-identities.html", "foundation-trigonometric-identities-quick-checks": "/math/foundation-trigonometric-identities-quick-checks.html", "foundation-trigonometric-ratios-beyond-90": "/math/foundation-trigonometric-ratios-beyond-90.html", "foundation-trigonometry-3d-applications": "/math/foundation-trigonometry-3d-applications.html", "foundation-trigonometry-fundamentals": "/math/foundation-trigonometry-fundamentals.html", "foundation-understanding-functions": "/math/foundation-understanding-functions.html", "foundation-understanding-the-placeholder-in-f-x": "/math/foundation-understanding-the-placeholder-in-f-x.html", "foundation-understanding-trigonometry": "/math/foundation-understanding-trigonometry.html", "foundation-unit-conversions-and-rates": "/math/foundation-unit-conversions-and-rates.html", "foundation-what-is-trigonometric-identity": "/math/foundation-what-is-trigonometric-identity.html", "foundation-why-simplified-calculation": "/math/foundation-why-simplified-calculation.html", "foundation-word-problems": "/math/foundation-word-problems.html", "gcf": "/math/thinking-greatest-common-factor-gcf.html", "geometric-strategies": "/math/thinking-geometric-strategies.html", "grade-10": "/math/grade-10.html", "grade-11": "/math/grade-11.html", "grade-3": "/math/grade-3.html", "grade-4": "/math/grade-4.html", "grade-5": "/math/grade-5.html", "grade-6": "/math/grade-6.html", "grade-7": "/math/grade-7.html", "grade-8": "/math/grade-8.html", "grade-9": "/math/grade-9.html", "in-class-learning": "/math/in-class-learning.html", "math-foundations": "/math/math-foundations.html", "math-real-life": "/math/math-real-life.html", "mathematical-thinking": "/math/mathematical-thinking.html", "measures-of-center": "/math/thinking-measures-of-center.html", "mental-squaring-and-square-rooting": "/math/thinking-mental-squaring-and-square-rooting.html", "number-families": "/math/foundation-number-families.html", "number-shape-thinking": "/math/thinking-number-shape-thinking.html", "number-strategies": "/math/thinking-number-strategies.html", "recovering-function-rule": "/math/thinking-recovering-function-rule.html", "rotation-transformation": "/math/thinking-rotation-transformation.html", "skateboard-ramp": "/math/skateboard-ramp.html", "special-right-triangles": "/math/thinking-special-right-triangles.html", "speedy-playful-math-magic": "/books/speedy-playful-math-magic.html", "thinking-algebraic-strategies": "/math/thinking-algebraic-strategies.html", "thinking-car-journey-advanced": "/math/thinking-car-journey-advanced.html", "thinking-chance-and-probability": "/math/thinking-chance-and-probability.html", "thinking-data-and-graphs": "/math/thinking-data-and-graphs.html", "thinking-discovering-pythagorean-triples": "/math/thinking-discovering-pythagorean-triples.html", "thinking-geometric-strategies": "/math/thinking-geometric-strategies.html", "thinking-greatest-common-factor-gcf": "/math/thinking-greatest-common-factor-gcf.html", "thinking-imaginary-complex-numbers": "/math/thinking-imaginary-complex-numbers.html", "thinking-measures-of-center": "/math/thinking-measures-of-center.html", "thinking-mental-squaring-and-square-rooting": "/math/thinking-mental-squaring-and-square-rooting.html", "thinking-number-shape-thinking": "/math/thinking-number-shape-thinking.html", "thinking-number-strategies": "/math/thinking-number-strategies.html", "thinking-recovering-function-rule": "/math/thinking-recovering-function-rule.html", "thinking-rotation-transformation": "/math/thinking-rotation-transformation.html", "thinking-special-right-triangles": "/math/thinking-special-right-triangles.html", "thinking-unit-conversions-and-rates": "/math/thinking-unit-conversions-and-rates.html", "thinking-why-simplified-calculation": "/math/thinking-why-simplified-calculation.html", "thinking-word-problems": "/math/thinking-word-problems.html", "unit-conversions-and-rates": "/math/thinking-unit-conversions-and-rates.html", "visual-math-patterns": "/math/visual-math-patterns.html", "why-simplified-calculation": "/math/thinking-why-simplified-calculation.html", "word-problems": "/math/thinking-word-problems.html"};
  /* KIWI_GITHUB_SLUG_DEST_END */

  function hostLower() {
    return (location.hostname || "").toLowerCase();
  }

  function isGithubProjectHost() {
    return hostLower().slice(-".github.io".length) === ".github.io";
  }

  function isLocalDev() {
    var h = hostLower();
    return h === "localhost" || h === "127.0.0.1";
  }

  function resolvePublishedDirectHref(href) {
    if (isLocalDev()) return null;
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
    var basePath = isGithubProjectHost() ? "/" + REPO_PREFIX : "";
    return basePath + dest + suffix;
  }

  function detectSiteBase() {
    if (isLocalDev()) return "/" + REPO_PREFIX;
    /* github.io project URL keeps /kiwi-ai-study; custom domain is repo root. */
    if (isGithubProjectHost()) return "/" + REPO_PREFIX;
    return "";
  }

  function stripWrongRepoPrefix(href) {
    if (!href || href.charAt(0) !== "/") return href;
    var prefix = "/" + REPO_PREFIX;
    if (base !== "" || isGithubProjectHost() || isLocalDev()) return href;
    if (href.indexOf(prefix + "/") === 0) return href.slice(prefix.length);
    if (href === prefix) return "/";
    return href;
  }

  var base = detectSiteBase();
  window.KIWI_SITE_BASE = base;

  function kiwiRootHref(href) {
    if (!href || typeof href !== "string") return href;
    if (href.charAt(0) !== "/" || href.indexOf("//") === 0) return href;
    href = stripWrongRepoPrefix(href);
    var direct = resolvePublishedDirectHref(href);
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
        var direct = resolvePublishedDirectHref(h);
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