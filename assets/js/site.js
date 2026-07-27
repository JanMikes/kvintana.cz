/* Kvintána — front-end behaviour
   Vanilla, no dependencies. Everything degrades to a working page without it. */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Sticky header ---------------------------------------------------- */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* --- Mega panel (Nabídka) --------------------------------------------- */
  var megaBtn = document.querySelector('[data-mega-toggle]');
  var mega = document.querySelector('[data-mega]');
  if (megaBtn && mega) {
    var closeMega = function () {
      mega.classList.remove('is-open');
      megaBtn.setAttribute('aria-expanded', 'false');
    };
    megaBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = mega.classList.toggle('is-open');
      megaBtn.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function (e) {
      if (!mega.contains(e.target) && e.target !== megaBtn) closeMega();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMega();
    });
    header.addEventListener('mouseleave', closeMega);
  }

  /* --- Mobile drawer ----------------------------------------------------- */
  var burger = document.querySelector('[data-burger]');
  var drawer = document.querySelector('[data-drawer]');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('is-locked', open);
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        drawer.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('is-locked');
      }
    });
  }

  /* --- Reveal on scroll -------------------------------------------------- */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    if (reduced || !('IntersectionObserver' in window)) {
      revealables.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      revealables.forEach(function (el) { io.observe(el); });
    }
  }

  /* --- Lightbox ----------------------------------------------------------- */
  var lbox = document.querySelector('[data-lightbox]');
  if (lbox) {
    var lImg = lbox.querySelector('[data-lb-img]');
    var lCap = lbox.querySelector('[data-lb-cap]');
    var lCount = lbox.querySelector('[data-lb-count]');
    var items = [];
    var idx = 0;
    var lastFocus = null;

    var collect = function (group) {
      items = Array.prototype.slice.call(
        document.querySelectorAll('[data-lb][data-lb-group="' + group + '"]')
      );
    };

    var render = function () {
      var el = items[idx];
      if (!el) return;
      lImg.src = el.getAttribute('data-lb');
      lImg.alt = el.getAttribute('data-lb-cap') || '';
      lCap.textContent = el.getAttribute('data-lb-cap') || '';
      lCount.textContent = (idx + 1) + ' / ' + items.length;
    };

    var open = function (el) {
      collect(el.getAttribute('data-lb-group') || 'all');
      idx = items.indexOf(el);
      if (idx < 0) idx = 0;
      lastFocus = el;
      render();
      lbox.classList.add('is-open');
      lbox.setAttribute('aria-hidden', 'false');
      document.body.classList.add('is-locked');
      lbox.querySelector('.lbox__close').focus();
    };

    var close = function () {
      lbox.classList.remove('is-open');
      lbox.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('is-locked');
      if (lastFocus) lastFocus.focus();
    };

    var step = function (n) {
      idx = (idx + n + items.length) % items.length;
      render();
    };

    document.addEventListener('click', function (e) {
      var trigger = e.target.closest('[data-lb]');
      if (trigger) { e.preventDefault(); open(trigger); }
    });

    lbox.addEventListener('click', function (e) {
      if (e.target.closest('[data-lb-prev]')) return step(-1);
      if (e.target.closest('[data-lb-next]')) return step(1);
      if (e.target.closest('[data-lb-close]') || e.target === lbox) return close();
    });

    document.addEventListener('keydown', function (e) {
      if (!lbox.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });

    /* swipe */
    var sx = 0;
    lbox.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lbox.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 55) step(dx < 0 ? 1 : -1);
    }, { passive: true });
  }

  /* --- Gallery album filter ---------------------------------------------- */
  var filterBar = document.querySelector('[data-filter]');
  if (filterBar) {
    var tiles = document.querySelectorAll('[data-album]');
    filterBar.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-filter-val]');
      if (!btn) return;
      var val = btn.getAttribute('data-filter-val');
      filterBar.querySelectorAll('[data-filter-val]').forEach(function (b) {
        b.classList.toggle('is-current', b === btn);
        b.setAttribute('aria-pressed', String(b === btn));
      });
      tiles.forEach(function (t) {
        var show = val === 'all' || t.getAttribute('data-album') === val;
        t.style.display = show ? '' : 'none';
      });
    });
  }

  /* --- Inquiry form -> Formspree ----------------------------------------- */
  var form = document.querySelector('[data-form]');
  if (form) {
    var ok = form.querySelector('[data-form-ok]');
    var err = form.querySelector('[data-form-err]');
    var submit = form.querySelector('button[type="submit"]');

    var show = function (el) {
      [ok, err].forEach(function (b) { if (b) b.classList.remove('is-shown'); });
      if (!el) return;
      el.classList.add('is-shown');
      el.setAttribute('role', 'status');
      el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
    };

    form.addEventListener('submit', function (e) {
      if (!form.reportValidity()) { e.preventDefault(); return; }
      /* Let the browser do a normal POST if fetch is unavailable — Formspree
         renders its own thank-you page in that case. */
      if (!window.fetch) return;

      e.preventDefault();
      show(null);
      var label = submit ? submit.innerHTML : '';
      if (submit) { submit.disabled = true; submit.textContent = 'Odesílám…'; }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          show(ok);
        })
        .catch(function () { show(err); })
        .then(function () {
          if (submit) { submit.disabled = false; submit.innerHTML = label; }
        });
    });
  }

  /* --- Prefill inquiry subject from ?show= --------------------------------- */
  var params = new URLSearchParams(window.location.search);
  var show = params.get('show');
  if (show) {
    var sel = document.querySelector('[data-form] select[name="program"]');
    if (sel) {
      Array.prototype.forEach.call(sel.options, function (o) {
        if (o.value === show) sel.value = show;
      });
    }
  }
})();
