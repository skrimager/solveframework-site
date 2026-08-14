// Mobile nav toggle
(function () {
  var toggle = document.getElementById('nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.querySelectorAll('.nav-dropdown a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
  nav.querySelectorAll('.main-nav > a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// Nav dropdowns: click-to-toggle (mobile accordion + keyboard/click support on desktop)
(function () {
  var items = document.querySelectorAll('.nav-item');
  if (!items.length) return;
  items.forEach(function (item) {
    var trigger = item.querySelector('.nav-trigger');
    if (!trigger) return;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var willOpen = !item.classList.contains('open');
      items.forEach(function (other) {
        other.classList.remove('open');
        var t = other.querySelector('.nav-trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
      if (willOpen) {
        item.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav-item')) {
      items.forEach(function (item) {
        item.classList.remove('open');
        var t = item.querySelector('.nav-trigger');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });
})();

// Compact-on-scroll header: add a subtle shrink + shadow once past the top
(function () {
  var header = document.getElementById('site-header');
  if (!header) return;
  var ticking = false;
  function apply() {
    header.classList.toggle('site-header--scrolled', window.scrollY > 40);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(apply);
      ticking = true;
    }
  }, { passive: true });
  apply();
})();

// Scroll reveal
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || !items.length) {
    items.forEach(function (el) { el.classList.add('in-view'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();

// Footer year
(function () {
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

// ROI calculator: how many months of the dashboard does one extra sale cover?
// Reference rate is the Office tier at today's locked rate ($583.50/mo), the tier
// most teams land in. Copy/display only — no billing logic.
(function () {
  var input = document.getElementById('roi-deal');
  var result = document.getElementById('roi-result');
  if (!input || !result) return;

  var DASHBOARD_MONTHLY = 583.50;
  var DEFAULT_MSG = 'One extra sale covers months of your dashboard, then keeps paying.';

  function update() {
    var deal = parseFloat(input.value);
    if (!deal || deal <= 0) {
      result.textContent = DEFAULT_MSG;
      return;
    }
    var months = deal / DASHBOARD_MONTHLY;
    var dealText = '$' + Math.round(deal).toLocaleString('en-US');
    if (months >= 12) {
      result.textContent = 'One ' + dealText + ' sale covers more than a full year of the Office dashboard at today’s locked rate ($583.50/mo). The math already made the decision.';
    } else {
      var rounded = Math.round(months * 10) / 10;
      result.textContent = 'One ' + dealText + ' sale covers about ' + rounded + ' month' + (rounded === 1 ? '' : 's') + ' of the Office dashboard at today’s locked rate ($583.50/mo).';
    }
  }

  input.addEventListener('input', update);
})();

// Request Access lead form: open modal, submit to the training platform API,
// show inline success/error without a page reload.
(function () {
  var modal = document.getElementById('lead-modal');
  var form = document.getElementById('lead-form');
  var status = document.getElementById('lead-status');
  if (!modal || !form) return;

  var API_BASE = window.__SOLVE_API_BASE || 'https://training.solveframework.com';
  var currentSource = '';

  function open(source) {
    currentSource = source || '';
    status.textContent = '';
    status.className = 'lead-status';
    form.reset();
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    var first = form.querySelector('input[name="name"]');
    if (first) first.focus();
  }

  function close() {
    modal.hidden = true;
    document.body.style.overflow = '';
  }

  document.querySelectorAll('[data-lead-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      open(btn.getAttribute('data-lead-source') || '');
    });
  });

  modal.querySelectorAll('[data-lead-close]').forEach(function (el) {
    el.addEventListener('click', close);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) close();
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var name = (data.get('name') || '').toString().trim();
    var email = (data.get('email') || '').toString().trim();
    if (!name || !email) {
      status.textContent = 'Please enter your name and email.';
      status.className = 'lead-status lead-status-error';
      return;
    }

    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;
    status.textContent = 'Sending…';
    status.className = 'lead-status';

    fetch(API_BASE + '/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name,
        email: email,
        company: (data.get('company') || '').toString().trim(),
        referredBy: (data.get('referredBy') || '').toString().trim(),
        message: (data.get('message') || '').toString().trim(),
        source: currentSource
      })
    })
      .then(function (res) {
        if (!res.ok) throw new Error('bad status ' + res.status);
        return res.json();
      })
      .then(function () {
        form.reset();
        status.textContent = "Thanks, we've got your request and will be in touch shortly.";
        status.className = 'lead-status lead-status-ok';
      })
      .catch(function () {
        status.textContent = 'Something went wrong. Please email hello@solveframework.com or try again.';
        status.className = 'lead-status lead-status-error';
      })
      .finally(function () {
        if (submitBtn) submitBtn.disabled = false;
      });
  });
})();

// Hero "Get More Information" box: lightweight name+email capture,
// posts to the same /api/leads endpoint with its own source tag.
(function () {
  var form = document.getElementById('hero-info-form');
  var status = document.getElementById('hero-info-status');
  if (!form || !status) return;

  var API_BASE = window.__SOLVE_API_BASE || 'https://training.solveframework.com';

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var name = (data.get('name') || '').toString().trim();
    var email = (data.get('email') || '').toString().trim();
    if (!name || !email) {
      status.textContent = 'Please enter your name and email.';
      status.className = 'hero-info-status hero-info-status-error';
      return;
    }

    var submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;
    status.textContent = 'Sending…';
    status.className = 'hero-info-status';

    fetch(API_BASE + '/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name,
        email: email,
        company: '',
        message: '',
        source: 'hero-info-box'
      })
    })
      .then(function (res) {
        if (!res.ok) throw new Error('bad status ' + res.status);
        return res.json();
      })
      .then(function () {
        form.reset();
        status.textContent = "Thanks, check your inbox soon.";
        status.className = 'hero-info-status hero-info-status-ok';
      })
      .catch(function () {
        status.textContent = 'Something went wrong. Please try again.';
        status.className = 'hero-info-status hero-info-status-error';
      })
      .finally(function () {
        if (submitBtn) submitBtn.disabled = false;
      });
  });
})();
