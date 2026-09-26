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
