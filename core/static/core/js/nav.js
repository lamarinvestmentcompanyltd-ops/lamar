document.addEventListener("DOMContentLoaded", function () {
  // Home page: header floats transparent over the hero, then turns solid once you scroll.
  var siteHeader = document.querySelector(".site-header");
  if (siteHeader && document.body.classList.contains("home-page")) {
    var syncHeader = function () { siteHeader.classList.toggle("is-scrolled", window.scrollY > 40); };
    syncHeader();
    window.addEventListener("scroll", syncHeader, { passive: true });
  }

  var toggle = document.getElementById("menuToggle");
  var nav = document.getElementById("mainNav");
  if (!toggle || !nav) return;

  var MOBILE_MAX = 860; // keep in sync with the @media (max-width: 860px) breakpoint in style.css

  function closeMenu() {
    nav.classList.remove("mobile-open");
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    document.body.classList.remove("menu-open");
  }

  toggle.addEventListener("click", function () {
    var isOpen = nav.classList.toggle("mobile-open");
    toggle.classList.toggle("open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    toggle.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
    document.body.classList.toggle("menu-open", isOpen);
  });

  nav.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      // On touch tablets the dropdown trigger only opens its menu (handled below)
      if (link.classList.contains("nav-dropdown-trigger") && window.innerWidth > MOBILE_MAX) return;
      closeMenu();
    });
  });

  // Close the mobile menu with Escape, a tap outside it, or when the screen grows to desktop size
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
  });
  document.addEventListener("click", function (e) {
    if (nav.classList.contains("mobile-open") && !nav.contains(e.target) && !toggle.contains(e.target)) {
      closeMenu();
    }
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > MOBILE_MAX) closeMenu();
  });

  // Dropdowns ("About Us", "Our Work"): hover on desktop, tap on tablets.
  // On a touch screen wider than the mobile breakpoint there is no hover, so the first
  // tap on the trigger opens the menu and a second tap follows the link.
  var isTouch = window.matchMedia("(hover: none)").matches;

  document.querySelectorAll(".nav-dropdown").forEach(function (dd) {
    var trigger = dd.querySelector(".nav-dropdown-trigger");
    if (!trigger) return;

    function setExpanded(state) {
      trigger.setAttribute("aria-expanded", state ? "true" : "false");
    }

    dd.addEventListener("mouseenter", function () { setExpanded(true); });
    dd.addEventListener("mouseleave", function () { setExpanded(false); });
    dd.addEventListener("focusin", function () { setExpanded(true); });
    dd.addEventListener("focusout", function () {
      if (!dd.contains(document.activeElement)) setExpanded(false);
    });

    if (isTouch) {
      trigger.addEventListener("click", function (e) {
        if (window.innerWidth <= MOBILE_MAX) return; // phones: menu is already flattened inline
        if (!dd.classList.contains("open")) {
          e.preventDefault();
          document.querySelectorAll(".nav-dropdown.open").forEach(function (o) { o.classList.remove("open"); });
          dd.classList.add("open");
          setExpanded(true);
        }
      });
    }
  });

  if (isTouch) {
    document.addEventListener("click", function (e) {
      document.querySelectorAll(".nav-dropdown.open").forEach(function (dd) {
        if (!dd.contains(e.target)) {
          dd.classList.remove("open");
          var t = dd.querySelector(".nav-dropdown-trigger");
          if (t) t.setAttribute("aria-expanded", "false");
        }
      });
    });
  }
});
