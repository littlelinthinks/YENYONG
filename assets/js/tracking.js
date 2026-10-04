/*
 * YENYONG conversion event tracking (GA4)
 * Loaded with `defer` so DOM is parsed before binding.
 * All events are prefixed and use the global `gtag` already defined by the GA4 snippet.
 */
(function () {
  "use strict";

  function fire(name, params) {
    if (typeof window.gtag === "function") {
      window.gtag("event", name, params || {});
    }
  }

  function paramsFor(el, extra) {
    var p = {};
    if (el.textContent) {
      var t = el.textContent.replace(/\s+/g, " ").trim();
      if (t) p.link_text = t.slice(0, 60);
    }
    if (typeof extra === "function") {
      var e = extra(el);
      if (e) for (var k in e) p[k] = e[k];
    }
    return p;
  }

  function bind(selector, event, name, extra) {
    var nodes = document.querySelectorAll(selector);
    for (var i = 0; i < nodes.length; i++) {
      (function (el) {
        el.addEventListener(event, function () {
          fire(name, paramsFor(el, extra));
        });
      })(nodes[i]);
    }
  }

  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  ready(function () {
    // WhatsApp tap
    bind('a[href*="wa.me"], a[href*="whatsapp"]', "click", "whatsapp_click", function (el) {
      return { destination: el.getAttribute("href") };
    });

    // Email tap
    bind('a[href^="mailto:"]', "click", "email_click", function (el) {
      var href = el.getAttribute("href") || "";
      var email = href.replace(/^mailto:/, "").split("?")[0];
      var subject = "";
      var m = href.match(/[?&]subject=([^&]+)/);
      if (m) {
        try { subject = decodeURIComponent(m[1]); } catch (e) { subject = m[1]; }
      }
      return { email: email, subject: subject };
    });

    // Phone tap (no tel: links today, but safe for future)
    bind('a[href^="tel:"]', "click", "phone_click", function (el) {
      return { phone: (el.getAttribute("href") || "").replace(/^tel:/, "") };
    });

    // Catalog / document download intent
    bind('a[href$=".pdf"]', "click", "catalog_download", function (el) {
      return { file: el.getAttribute("href") };
    });

    // Inquiry / quote / contact CTA (anything pointing at #contact)
    bind('a[href*="#contact"]', "click", "contact_cta_click");

    // Inquiry form submission
    var forms = document.querySelectorAll("form");
    for (var i = 0; i < forms.length; i++) {
      (function (form) {
        form.addEventListener("submit", function () {
          fire("inquiry_submit", {
            form_id: form.id || form.getAttribute("name") || "unnamed"
          });
        });
      })(forms[i]);
    }
  });
})();

/* ===== yy-nav-behavior 统一导航行为：滚动反色 + 当前页高亮 + Sustainability 项 ===== */
(function () {
  "use strict";
  var nav = document.querySelector("nav.nav");
  var sn = document.querySelector(".site-nav");
  if (!nav && !sn) return;
  function tick() {
    var s = window.scrollY > 80;
    if (nav) nav.classList.toggle("scrolled", s);
    if (sn) sn.classList.toggle("scrolled", s);
  }
  window.addEventListener("scroll", tick, { passive: true });
  tick();

  if (!nav) return; /* site-nav 变体模板无 .links 结构，跳过插入/高亮 */
  var links = nav.querySelectorAll(".links a");
  if (!links.length) return;
  var path = location.pathname.replace(/\/index\.html$/, "/");
  var langM = path.match(/^\/(de|fr|ru|zh)\//);
  var lang = langM ? langM[1] : "";
  var pre = lang ? "/" + lang + "/" : "/";
  var susLabel = { de: "Nachhaltigkeit", fr: "Durabilite", ru: "Устойчивое развитие", zh: "可持续发展" }[lang] || "Sustainability";

  // 1) 导航缺少 Sustainability 项时，插入到 Contact 按钮之前
  var hasSus = Array.prototype.some.call(links, function (a) {
    return (a.getAttribute("href") || "") === pre + "sustainability.html";
  });
  var cta = nav.querySelector(".links a.cta");
  if (!hasSus && cta) {
    var el = document.createElement("a");
    el.href = pre + "sustainability.html";
    el.textContent = susLabel;
    cta.parentNode.insertBefore(el, cta);
    links = nav.querySelectorAll(".links a");
  }

  // 2) 当前页高亮：精确匹配 > 博客文章→Insights > 产品页→Products
  function norm(u) {
    try { return new URL(u, location.origin).pathname.replace(/\/index\.html$/, "/"); }
    catch (e) { return u || ""; }
  }
  var best = null;
  Array.prototype.forEach.call(links, function (a) {
    a.classList.remove("act");
    if (norm(a.getAttribute("href")) === path) best = a;
  });
  if (!best && path.indexOf("/blog/") > -1) {
    best = Array.prototype.find.call(links, function (a) {
      return /insights\.html$/.test(norm(a.getAttribute("href")) || "");
    });
  }
  if (!best) {
    var prods = ["spc-rigid-core-flooring","spc-wall-panel","wpc-wall-panel","pvc-wall-panel","acoustic-panel",
      "aluminium-composite-panel","aluminium-honeycomb-panel","bamboo-crystal-panel","carbon-crystal-panel",
      "ceramic-porcelain-tile","colour-library","flexible-stone-panel","hpl-compact-laminate","ar-preview",
      "material-calculator","pricing-calculator","product-comparison","sample-order"];
    var isProd = prods.some(function (s) { return path.indexOf("/" + s + ".html") > -1; });
    if (isProd) {
      best = Array.prototype.find.call(links, function (a) {
        return (a.getAttribute("href") || "").indexOf("#products") > -1;
      });
    }
  }
  if (best && !best.classList.contains("cta")) best.classList.add("act");
})();
