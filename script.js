// Mobile nav toggle
(function () {
  var toggle = document.getElementById('nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  nav.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', function () {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
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
        status.textContent = "Thanks — we've got your request and will be in touch shortly.";
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
