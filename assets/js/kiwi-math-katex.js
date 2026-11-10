/**
 * Sitewide math rendering (KaTeX): explicit data-tex blocks + MathML tex annotations.
 * See DESIGN_STANDARDS.md — Display Formula / unit \cancel / upright \text{units}.
 */
(function () {
  const KATEX_OPTS = {
    throwOnError: false,
    strict: "ignore",
    trust: false,
  };

  const UNIT_WORDS =
    "lb|gal|km|cm|mm|ml|L|g|kg|h|hr|s|m|ft|in|mph|kph|oz|pt|qt|yr|min|sec";

  function currentLang() {
    const lang = (document.documentElement.lang || "en").toLowerCase();
    return lang.startsWith("zh") ? "zh" : "en";
  }

  function normalizeTex(tex, displayMode) {
    if (!tex) return tex;
    let t = tex.trim();
    if (displayMode) {
      t = t.replace(/\\frac\b/g, "\\dfrac");
    }
    t = t.replace(/\\boxed\{\\text\{([^}]+)\}\}/g, "\\cancel{\\text{$1}}");
    if (!/\\text\{/.test(t)) {
      t = t.replace(
        new RegExp(`\\{(${UNIT_WORDS})\\}`, "gi"),
        (_, u) => `{\\text{${u}}}`,
      );
      t = t.replace(
        new RegExp(`(\\d)\\s*\\\\,?\\s*(${UNIT_WORDS})\\b`, "gi"),
        (_, n, u) => `${n}\\,\\text{${u}}`,
      );
    }
  t = wrapTeachingLabels(t);
    return t;
  }

  /** Word-export tex like "Value = Rate \times Quantity" → upright labels */
  function wrapTeachingLabels(tex) {
    if (!tex || /\\text\{/.test(tex)) return tex;
    let t = tex.replace(/Conversion\\ Factor/g, "Conversion Factor");
    if (!/\b(Value|Rate|Quantity)\b/.test(t)) return t;
    t = t.replace(/\bValue\b/g, "\\text{Value}");
    t = t.replace(/\bRate\b/g, "\\text{Rate}");
    t = t.replace(/\bQuantity\b/g, "\\text{Quantity}");
    t = t.replace(
      /Conversion Factor/g,
      "\\text{Conversion}\\,\\text{Factor}",
    );
    return t;
  }

  function isDisplayMath(mathEl) {
    const display = (mathEl.getAttribute("display") || "").toLowerCase();
    if (display === "inline") return false;
    if (display === "block") return true;
    if (mathEl.classList.contains("kiwi-display-math")) return true;
    if (mathEl.classList.contains("math-display")) return true;
    const parent = mathEl.parentElement;
    if (
      parent &&
      parent.children.length === 1 &&
      parent.children[0] === mathEl &&
      (parent.tagName === "P" || parent.classList.contains("kiwi-math-block"))
    ) {
      return true;
    }
    return false;
  }

  function renderLatexBlock(el) {
    if (typeof katex === "undefined") return;
    const lang = currentLang();
    const tex =
      el.getAttribute(lang === "zh" ? "data-tex-zh" : "data-tex-en") ||
      el.getAttribute("data-tex-en");
    if (!tex) return;
    const display =
      el.getAttribute("data-display") === "block" ||
      (!el.classList.contains("kiwi-katex-inline") &&
        !!el.closest(".kiwi-math-block"));
    try {
      katex.render(normalizeTex(tex, display), el, {
        ...KATEX_OPTS,
        displayMode: display,
      });
    } catch (err) {
      /* ignore */
    }
  }

  function renderMathFromAnnotation(mathEl) {
    if (typeof katex === "undefined") return;
    if (mathEl.closest(".kiwi-math-latex")) return;
    const ann = mathEl.querySelector(
      'annotation[encoding="application/x-tex"]',
    );
    if (!ann) return;
    const display = isDisplayMath(mathEl);
    const raw = ann.textContent;
  if (raw == null) return;
    const tex = normalizeTex(raw, display);
    if (!tex) return;
    const holder = document.createElement(display ? "div" : "span");
    holder.className = display ? "kiwi-katex-display" : "kiwi-katex-inline";
    holder.setAttribute("role", "math");
    holder.setAttribute("aria-label", tex);
    try {
      katex.render(tex, holder, { ...KATEX_OPTS, displayMode: display });
    } catch (err) {
      return;
    }
    mathEl.replaceWith(holder);
    if (display) {
      const parent = holder.parentElement;
      if (
        parent &&
        (parent.tagName === "P" || parent.tagName === "DIV") &&
        !parent.classList.contains("kiwi-math-block")
      ) {
        if (
          parent.childNodes.length === 1 ||
          (parent.children.length === 1 && parent.children[0] === holder)
        ) {
          parent.classList.add("kiwi-math-block");
        }
      }
    }
  }

  function kiwiRenderMathLatex(root) {
    const scope = root && root.querySelectorAll ? root : document;
    scope.querySelectorAll(".kiwi-math-latex").forEach(renderLatexBlock);
  }

  function kiwiRenderMathAnnotations(root) {
    const scope = root && root.querySelectorAll ? root : document;
    scope.querySelectorAll("math").forEach(renderMathFromAnnotation);
  }

  function kiwiRenderAllMath(root) {
    kiwiRenderMathLatex(root);
    kiwiRenderMathAnnotations(root);
  }

  window.kiwiRenderMathLatex = kiwiRenderMathLatex;
  window.kiwiRenderMathAnnotations = kiwiRenderMathAnnotations;
  window.kiwiRenderAllMath = kiwiRenderAllMath;

  function onReady() {
    if (typeof katex === "undefined") return false;
    kiwiRenderAllMath();
    return true;
  }

  function scheduleRender() {
    if (onReady()) return;
    let attempts = 0;
    const retry = () => {
      if (onReady()) return;
      if (++attempts > 200) return;
      window.requestAnimationFrame(retry);
    };
    window.addEventListener("load", () => onReady(), { once: true });
    window.requestAnimationFrame(retry);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scheduleRender);
  } else {
    scheduleRender();
  }
})();
