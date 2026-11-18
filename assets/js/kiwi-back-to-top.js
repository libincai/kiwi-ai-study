(function () {
  "use strict";
  const isFoundationL4 = !!document.querySelector(".foundation-level4");
  const isThinkingL4 = !!document.querySelector(
    ".kiwi-learning-layout .kiwi-topic-article",
  );
  if (!isFoundationL4 && !isThinkingL4) return;

  const main = document.querySelector("main");
  if (!main) return;
  if (!main.id) main.id = "kiwi-page-top";
  if (!main.hasAttribute("tabindex")) main.setAttribute("tabindex", "-1");

  const sentinel = document.createElement("div");
  sentinel.className = "kiwi-back-to-top-sentinel";
  sentinel.setAttribute("aria-hidden", "true");
  sentinel.style.cssText =
    "width:1px;height:1px;margin:0;padding:0;border:0;pointer-events:none";

  const topChromeEnd =
    main.querySelector(".kiwi-grade-strip-wrap") ||
    main.querySelector(".topic-banner, .nf-hero.topic-banner") ||
    main.querySelector(".foundation-level4") ||
    main.querySelector(".kiwi-learning-layout");
  if (topChromeEnd && topChromeEnd.parentNode) {
    topChromeEnd.parentNode.insertBefore(sentinel, topChromeEnd.nextSibling);
  } else {
    document.body.insertBefore(sentinel, document.body.firstChild);
  }

  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "kiwi-back-to-top";
  btn.setAttribute("aria-label", "Back to top");
  btn.setAttribute("data-en", "↑ Top");
  btn.setAttribute("data-zh", "↑ 回到顶部");
  btn.textContent = "↑ Top";
  btn.hidden = true;
  btn.classList.add("kiwi-back-to-top--article");
  document.body.appendChild(btn);

  const article =
    document.querySelector(".foundation-level4 .mf-article.mf-chapter") ||
    document.querySelector(".foundation-level4 .mf-article") ||
    document.querySelector(".kiwi-topic-article");
  const gapOutside = 12;
  const minEdge = 16;
  const placeButton = () => {
    if (!article) return;
    const openCard =
      document.querySelector(
        ".foundation-level4 .mf-article details.lesson-card[open]",
      ) ||
      document.querySelector(".kiwi-topic-article details.lesson-card[open]");
    const anchor = openCard || article;
    const anchorRight = anchor.getBoundingClientRect().right;
    const width = btn.offsetWidth || 72;
    let left = anchorRight + gapOutside;
    const maxLeft = window.innerWidth - width - minEdge;
    if (left > maxLeft) left = maxLeft;
    btn.style.left = `${Math.max(minEdge, left)}px`;
    btn.style.right = "auto";
  };
  placeButton();
  window.addEventListener("resize", placeButton, { passive: true });
  window.addEventListener("scroll", placeButton, { passive: true });

  const isZh = () =>
    /^zh/i.test(document.documentElement.lang || "") ||
    document.documentElement.getAttribute("data-language") === "zh";

  const syncLanguage = () => {
    const zh = isZh();
    btn.textContent = btn.getAttribute(zh ? "data-zh" : "data-en");
    btn.setAttribute("aria-label", zh ? "回到顶部" : "Back to top");
  };
  syncLanguage();
  new MutationObserver(syncLanguage).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["lang", "data-language"],
  });

  const scrollY = () =>
    window.scrollY ||
    document.documentElement.scrollTop ||
    document.body.scrollTop ||
    0;

  const MIN_VIEWPORTS = 2;
  const MIN_SCROLL_PX = 320;
  const SHOW_DELAY_MS = 120;

  const pageIsLong = () => {
    const docH = Math.max(
      document.documentElement.scrollHeight,
      document.body.scrollHeight,
    );
    return docH > window.innerHeight * MIN_VIEWPORTS;
  };

  const setVisible = (visible) => {
    btn.hidden = !visible;
  };

  let sentinelInView = true;
  let showTimer = null;

  const applyShowIntent = (wantShow) => {
    if (!pageIsLong() || scrollY() < 1) {
      if (showTimer) clearTimeout(showTimer);
      showTimer = null;
      setVisible(false);
      return;
    }
    if (!wantShow) {
      if (showTimer) clearTimeout(showTimer);
      showTimer = null;
      setVisible(false);
      return;
    }
    if (showTimer) return;
    showTimer = setTimeout(() => {
      showTimer = null;
      if (
        pageIsLong() &&
        scrollY() >= MIN_SCROLL_PX &&
        !sentinelInView
      ) {
        setVisible(true);
      }
    }, SHOW_DELAY_MS);
  };

  const evaluateVisibility = () => {
    const wantShow =
      pageIsLong() && scrollY() >= MIN_SCROLL_PX && !sentinelInView;
    applyShowIntent(wantShow);
  };

  const fallbackCheck = () => {
    const rect = sentinel.getBoundingClientRect();
    sentinelInView = rect.top > -8;
    evaluateVisibility();
  };

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        const e = entries[0];
        if (!e) return;
        sentinelInView = e.isIntersecting;
        evaluateVisibility();
      },
      { root: null, rootMargin: "-8px 0px 0px 0px", threshold: 0 },
    );
    io.observe(sentinel);
    window.addEventListener("scroll", evaluateVisibility, { passive: true });
    window.addEventListener("resize", () => {
      evaluateVisibility();
    }, { passive: true });
    evaluateVisibility();
  } else {
    window.addEventListener("scroll", fallbackCheck, { passive: true });
    window.addEventListener("resize", fallbackCheck, { passive: true });
    fallbackCheck();
  }

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    main.focus({ preventScroll: true });
  });
})();