// Mickey Salim · Level Up Circle — small, framework-free interactions.
(function () {
  document.documentElement.classList.remove('no-js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scroll reveal
  var revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); ro.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) { ro.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  // About slideshow: changes every 3 seconds, dots jump to a photo
  var show = document.querySelector('[data-slideshow]');
  if (show) {
    var imgs = show.querySelectorAll('.slideshow__frame img');
    var dots = show.querySelectorAll('.slideshow__dot');
    var caption = show.querySelector('.slideshow__caption');
    var current = 0, timer = null;
    function go(i) {
      current = (i + imgs.length) % imgs.length;
      imgs.forEach(function (img, n) { img.classList.toggle('is-active', n === current); });
      dots.forEach(function (d, n) { d.setAttribute('aria-current', n === current ? 'true' : 'false'); });
      if (caption) caption.textContent = imgs[current].getAttribute('data-caption') || '';
    }
    function start() { stop(); timer = setInterval(function () { go(current + 1); }, 3000); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    dots.forEach(function (d, n) { d.addEventListener('click', function () { go(n); start(); }); });
    document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
    go(0);
    start();
  }

  // "Read more" links on phones: reveal the collapsed block they point to
  document.querySelectorAll('[data-expand]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-expand'));
      if (target) target.classList.add('is-expanded');
      btn.setAttribute('aria-expanded', 'true');
    });
  });

  // Product page: sticky buy bar appears once the main buy button scrolls away
  var bar = document.querySelector('[data-buybar]');
  var anchor = document.querySelector('[data-buy-anchor]');
  if (bar && anchor && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      var out = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
      bar.classList.toggle('is-visible', out);
      bar.inert = !out;
    }).observe(anchor);
  }
})();
