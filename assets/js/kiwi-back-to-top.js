(function () {
  "use strict";
  if (!document.querySelector(".foundation-level4")) return;

  const main = document.querySelector("main");
  if (!main) return;
  if (!main.id) main.id = "kiwi-page-top";
  if (!main.hasAttribute("tabindex")) main.setAttribute("tabindex", "-1");

  const sentinel = document.createElement("div");
  sentinel.className = "kiwi-back-to-top-sentinel";
  sentinel.setAttribute("aria-hidden", "true");
  sentinel.style.cssText =
    "width:1px;height:1px;margin:0;padding:0;border:0;pointer-events:none";
  document.body.insertBefore(sentinel, document.body.firstChild);

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
    document.querySelector(".foundation-level4 .mf-article");
  const gapOutside = 12;
  const minEdge = 16;
  const placeButton = () => {
    if (!article) return;
    const openCard = document.querySelector(
      ".foundation-level4 .mf-article details.lesson-card[open]",
    );
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

  const showAt = 120;
  const setVisible = (visible) => {
    btn.hidden = !visible;
  };

  const fallbackCheck = () => setVisible(scrollY() >= showAt);

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        const e = entries[0];
        if (!e) return;
        setVisible(!e.isIntersecting || scrollY() >= showAt);
      },
      { root: null, rootMargin: "0px 0px 0px 0px", threshold: 0 },
    );
    io.observe(sentinel);
    window.addEventListener("scroll", fallbackCheck, { passive: true });
    fallbackCheck();
  } else {
    window.addEventListener("scroll", fallbackCheck, { passive: true });
    fallbackCheck();
  }

  btn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    main.focus({ preventScroll: true });
  });
})();