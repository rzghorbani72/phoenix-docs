/* Phoenix product docs — chapter sidebar, scroll-spy, theme and BLAME toggles.
   Inlined at the end of <body> by apply_theme.py. Storage is a convenience only. */
(function () {
  var root = document.documentElement;
  var body = document.body;
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  var theme = load("phx-theme");
  if (theme === "light" || theme === "dark") root.setAttribute("data-theme", theme);

  var hasBlame = !!document.querySelector(".who");
  if (hasBlame && load("phx-blame") !== "show") body.classList.add("hide-blame");

  /* every h2 gets an id so it can be linked and listed */
  [].forEach.call(document.querySelectorAll("h2:not([id])"), function (h, i) { h.id = "sec-" + (i + 1); });

  /* sidebar from part dividers + h2[id] */
  var heads = [].slice.call(document.querySelectorAll("section.part, h2[id]"))
    .filter(function (el) { return el.id !== "toc"; });
  if (heads.filter(function (el) { return el.tagName === "H2"; }).length > 3) {
    var nav = document.createElement("nav");
    nav.id = "side";
    nav.setAttribute("aria-label", "فهرست فصل‌ها");
    var h1 = document.querySelector("h1");
    var docT = document.createElement("div");
    docT.className = "doc";
    docT.textContent = h1 ? h1.textContent.trim() : document.title;
    nav.appendChild(docT);
    var list = document.createElement("ol");
    nav.appendChild(list);
    var links = [];
    heads.forEach(function (el) {
      if (el.tagName !== "H2") {
        var t = el.querySelector(".ttl");
        var g = document.createElement("li");
        g.className = "grp";
        g.textContent = t ? t.textContent.trim() : "";
        list.appendChild(g);
        return;
      }
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + el.id;
      var label = el.cloneNode(true);
      [].forEach.call(label.querySelectorAll(".ab"), function (n) { n.remove(); });
      a.textContent = label.textContent.replace(/\s+/g, " ").trim();
      a.title = a.textContent;
      li.appendChild(a);
      list.appendChild(li);
      links.push({ a: a, el: el });
    });
    body.insertBefore(nav, body.firstChild);

    if ("IntersectionObserver" in window) {
      var current = null;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (l) {
            var on = l.el === e.target;
            l.a.classList.toggle("on", on);
            if (on && l.a !== current) {
              current = l.a;
              var r = l.a.getBoundingClientRect(), n = nav.getBoundingClientRect();
              if (r.top < n.top || r.bottom > n.bottom) l.a.scrollIntoView({ block: "nearest" });
            }
          });
        });
      }, { rootMargin: "0px 0px -75% 0px" });
      links.forEach(function (l) { io.observe(l.el); });
    }
  }

  /* toolbar */
  var bar = document.createElement("div");
  bar.className = "toolbar";
  function btn(label, title, fn) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.title = title;
    b.addEventListener("click", function () { fn(b); });
    bar.appendChild(b);
    return b;
  }
  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return true;
  }
  var tb = btn(isDark() ? "☀ روشن" : "☾ تیره", "تغییر تم", function (b) {
    var next = isDark() ? "light" : "dark";
    root.setAttribute("data-theme", next);
    save("phx-theme", next);
    b.textContent = next === "dark" ? "☀ روشن" : "☾ تیره";
  });
  if (hasBlame) {
    var bb = btn("BLAME", "نمایش یا پنهان کردن خطوط Git Blame", function (b) {
      var hidden = body.classList.toggle("hide-blame");
      b.setAttribute("aria-pressed", String(!hidden));
      save("phx-blame", hidden ? "hide" : "show");
    });
    bb.setAttribute("aria-pressed", String(!body.classList.contains("hide-blame")));
  }
  btn("↑", "بالای صفحه", function () { window.scrollTo({ top: 0 }); });
  body.appendChild(bar);
})();
