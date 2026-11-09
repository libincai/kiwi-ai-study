(function () {
  "use strict";
  const pages = {
    "about/index.html": { en:"About", zh:"关于我们", parent:"" },
    "contact/index.html": { en:"Contact Us", zh:"联系我们", parent:"" },
    "legal/privacy.html": { en:"Privacy Policy", zh:"隐私政策", parent:"" },
    "legal/terms.html": { en:"Copyright & Content Usage Policy", zh:"版权与内容使用政策", parent:"" },

    "math/index.html": { en:"Math Education", zh:"数学教育", parent:"" },
    "math/math-foundations.html": { en:"Math Foundations", zh:"数学基础", parent:"math/index.html" },
    "math/math-real-life.html": { en:"Math in Real Life", zh:"生活中的数学", parent:"math/index.html" },
    "math/visual-math-patterns.html": { en:"Visual Math & Patterns", zh:"视觉数学与规律", parent:"math/index.html" },
    "math/gcf.html": { en:"Greatest Common Factor (GCF)", zh:"Greatest Common Factor (GCF)", parent:"math/mathematical-thinking.html" },
    "math/unit-conversions-and-rates.html": { en:"Unit Conversions and Rates", zh:"Unit Conversions and Rates", parent:"math/mathematical-thinking.html" },
    "math/mental-squaring-and-square-rooting.html": { en:"Mental Squaring and Square Rooting", zh:"Mental Squaring and Square Rooting", parent:"math/mathematical-thinking.html" },
    "math/recovering-function-rule.html": { en:"Recovering a Function Rule from Function Notation", zh:"Recovering a Function Rule from Function Notation", parent:"math/mathematical-thinking.html" },
    "math/car-journey-advanced.html": { en:"Function in Real Life: A Car\u2019s Journey", zh:"Function in Real Life: A Car\u2019s Journey", parent:"math/mathematical-thinking.html" },
    "math/rotation-transformation.html": { en:"Rotation Transformation", zh:"Rotation Transformation", parent:"math/mathematical-thinking.html" },
    "math/special-right-triangles.html": { en:"Special Right Triangles", zh:"Special Right Triangles", parent:"math/mathematical-thinking.html" },
    "math/data-and-graphs.html": { en:"Data and Graphs", zh:"Data and Graphs", parent:"math/mathematical-thinking.html" },
    "math/measures-of-center.html": { en:"Measures of Center", zh:"Measures of Center", parent:"math/mathematical-thinking.html" },
    "math/chance-and-probability.html": { en:"Chance and Probability", zh:"Chance and Probability", parent:"math/mathematical-thinking.html" },
    "math/why-simplified-calculation.html": { en:"Why Simplified Calculation", zh:"Why Simplified Calculation", parent:"math/mathematical-thinking.html" },
    "math/number-strategies.html": { en:"Number Strategies", zh:"Number Strategies", parent:"math/mathematical-thinking.html" },
    "math/algebraic-strategies.html": { en:"Algebraic Strategies", zh:"Algebraic Strategies", parent:"math/mathematical-thinking.html" },
    "math/geometric-strategies.html": { en:"Geometric Strategies", zh:"Geometric Strategies", parent:"math/mathematical-thinking.html" },
    "math/number-shape-thinking.html": { en:"Number\u2013Shape Thinking", zh:"Number\u2013Shape Thinking", parent:"math/mathematical-thinking.html" },
    "math/word-problems.html": { en:"Word Problems", zh:"Word Problems", parent:"math/mathematical-thinking.html" },
    "math/mathematical-thinking.html": { en:"Mathematical Thinking", zh:"数学思维", parent:"math/index.html" },
    "math/in-class-learning.html": { en:"In-Class Learning", zh:"课堂学习", parent:"math/index.html" },
    "math/number-families.html": { en:"Number Families", zh:"数的分类", parent:"math/math-foundations.html" },
    "math/car-journey.html": { en:"A Car’s Journey", zh:"汽车的旅程", parent:"math/math-real-life.html" },
    "math/skateboard-ramp.html": { en:"Skateboard Ramp", zh:"滑板坡道", parent:"math/visual-math-patterns.html" },

    "ai/index.html": { en:"AI Education", zh:"人工智能教育", parent:"" },
    "ai/episode-01.html": { en:"Episode 1: What Is AI?", zh:"第 1 集：什么是人工智能？", parent:"ai/index.html" },
    "ai/episode-02.html": { en:"Episode 2: Traditional AI vs. Generative AI", zh:"第 2 集：传统 AI 与生成式 AI", parent:"ai/index.html" },
    "ai/episode-03.html": { en:"Episode 3: AI Learning", zh:"第 3 集：AI 学习", parent:"ai/index.html" },
    "ai/episode-04.html": { en:"Episode 4: Who Creates AI?", zh:"第 4 集：谁创造了 AI？", parent:"ai/index.html" },
    "ai/episode-05.html": { en:"Episode 5: Invisible and Visible AI", zh:"第 5 集：看不见的 AI 和看得见的 AI", parent:"ai/index.html" },
    "ai/episode-06.html": { en:"Episode 6: Review", zh:"第 6 集：知识回顾", parent:"ai/index.html" },
    "ai/episode-07.html": { en:"Episode 7: The AI Concept Map", zh:"第 7 集：AI 的一张概念地图", parent:"ai/index.html" },
    "ai/episode-08.html": { en:"Episode 8: Prompt", zh:"第 8 集：提示词", parent:"ai/index.html" },
    "ai/episode-09.html": { en:"Episode 9: Focused Prompts", zh:"第 9 集：聚焦式提示词", parent:"ai/index.html" },
    "ai/episode-10.html": { en:"Episode 10: How Does an AI Agent Work?", zh:"第 10 集：AI Agent 如何工作？", parent:"ai/index.html" },
    "ai/episode-special-learning.html": { en:"Special (Ep 7): AI Is Powerful", zh:"第 7 集特别篇：AI 这么厉害", parent:"ai/index.html" },

    "books/index.html": { en:"Books & Learning Resources", zh:"书籍与学习资源", parent:"" },
    "books/books-speedy.html": { en:"Speedy & Playful Math Magic", zh:"Speedy & Playful Math Magic", parent:"books/index.html" },
    "books/books-foundations.html": { en:"Math Quick Reference Library", zh:"Math Quick Reference Library", parent:"books/index.html" },
    "books/books-advanced.html": { en:"Math Quick Reference Library – Advanced", zh:"Math Quick Reference Library – Advanced", parent:"books/index.html" },
    "books/speedy-playful-math-magic.html": { en:"Where to Buy", zh:"购买渠道", parent:"books/books-speedy.html" }
  };

  const path = location.pathname.replace(/\/+/g, "/").replace(/^\/+|\/+$/g, "");
  // Support both domain-root hosting and deployments inside a subfolder.
  const key = Object.keys(pages).find(page => path === page || path.endsWith("/" + page)) || "";
  const current = pages[key];
  if (!current) return;

  const isZh = () => /^zh/i.test(document.documentElement.lang || "") ||
    document.documentElement.getAttribute("data-language") === "zh";
  const label = item => isZh() ? item.zh : item.en;
  const urlFor = itemKey => {
    const from = key.split("/").slice(0, -1);
    const to = itemKey.split("/");
    let common = 0;
    while (common < from.length && common < to.length && from[common] === to[common]) common++;
    return "../".repeat(from.length - common) + to.slice(common).join("/");
  };

  const chain = [];
  let cursor = key;
  while (cursor && pages[cursor]) {
    chain.unshift({ key:cursor, item:pages[cursor] });
    cursor = pages[cursor].parent;
  }
  chain.unshift({ key:"index.html", item:{ en:"Home", zh:"首页" } });

  const childrenOf = parentKey => Object.keys(pages)
    .filter(k => pages[k].parent === parentKey)
    .map(k => ({ key:k, item:pages[k] }));

  const nav = document.createElement("nav");
  nav.className = "drive-breadcrumb";
  nav.setAttribute("aria-label", isZh() ? "页面路径" : "Breadcrumb");
  nav.innerHTML = chain.map((entry, index) => {
    const isCurrent = index === chain.length - 1;
    const children = isCurrent ? childrenOf(entry.key) : [];
    const text = isCurrent
      ? `<span class="drive-crumb-current" aria-current="page">${label(entry.item)}</span>`
      : `<a class="drive-crumb-link" href="${urlFor(entry.key)}">${label(entry.item)}</a>`;
    const dropdown = children.length
      ? `<span class="drive-crumb-menu-wrap">
           <button class="drive-crumb-menu-button" type="button" aria-label="${isZh() ? "展开" : "Open"} ${label(entry.item)}" aria-expanded="false">
             <svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>
           </button>
           <span class="drive-crumb-menu" hidden>
             ${children.map(child => `<a href="${urlFor(child.key)}">${label(child.item)}</a>`).join("")}
           </span>
         </span>` : "";
    const separator = isCurrent ? "" : `<svg class="drive-crumb-separator" viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>`;
    return `<span class="drive-crumb-part">${text}${isCurrent ? dropdown : ""}${separator}</span>`;
  }).join("");

  nav.addEventListener("click", event => {
    const button = event.target.closest(".drive-crumb-menu-button");
    if (button) {
      const menu = button.nextElementSibling;
      const open = button.getAttribute("aria-expanded") === "true";
      nav.querySelectorAll(".drive-crumb-menu").forEach(m => m.hidden = true);
      nav.querySelectorAll(".drive-crumb-menu-button").forEach(b => b.setAttribute("aria-expanded", "false"));
      if (!open) {
        menu.hidden = false;
        button.setAttribute("aria-expanded", "true");
      }
      event.stopPropagation();
      return;
    }
    if (!event.target.closest(".drive-crumb-menu-wrap")) {
      nav.querySelectorAll(".drive-crumb-menu").forEach(m => m.hidden = true);
      nav.querySelectorAll(".drive-crumb-menu-button").forEach(b => b.setAttribute("aria-expanded", "false"));
    }
  });
  document.addEventListener("click", () => {
    nav.querySelectorAll(".drive-crumb-menu").forEach(m => m.hidden = true);
    nav.querySelectorAll(".drive-crumb-menu-button").forEach(b => b.setAttribute("aria-expanded", "false"));
  });

  const main = document.querySelector("main");
  if (!main) return;
  main.querySelectorAll(":scope > .page-back-wrap, :scope > .edu-back, :scope > .ai-back").forEach(el => el.remove());
  main.insertBefore(nav, main.firstChild);

  const refreshBreadcrumbLanguage = () => {
    nav.setAttribute("aria-label", isZh() ? "页面路径" : "Breadcrumb");
    nav.querySelectorAll(".drive-crumb-link").forEach((el, i) => {
      const entry = chain[i];
      if (entry) el.textContent = label(entry.item);
    });
    const currentEl = nav.querySelector(".drive-crumb-current");
    if (currentEl) currentEl.textContent = label(chain[chain.length - 1].item);
    const menuLinks = nav.querySelectorAll(".drive-crumb-menu a");
    const currentChildren = childrenOf(chain[chain.length - 1].key);
    menuLinks.forEach((el, i) => {
      if (currentChildren[i]) el.textContent = label(currentChildren[i].item);
    });
    nav.querySelectorAll(".drive-crumb-menu-button").forEach(button => {
      const wrap = button.closest(".drive-crumb-menu-wrap");
      const crumbLabel = wrap && wrap.parentElement.querySelector(".drive-crumb-current, .drive-crumb-link");
      button.setAttribute("aria-label", `${isZh() ? "展开" : "Open"} ${crumbLabel ? crumbLabel.textContent : ""}`);
    });
  };
  new MutationObserver(refreshBreadcrumbLanguage).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["lang", "data-language"]
  });
})();