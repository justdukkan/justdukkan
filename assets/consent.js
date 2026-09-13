(function () {
  var GA_ID = 'G-C8T8T596HD';
  var KEY = 'jd-consent';
  var lang = document.documentElement.lang === 'tr' ? 'tr' : 'en';
  var T = {
    en: { text: 'We use Google Analytics to understand how the site is used. It only runs if you accept.', link: 'Privacy', href: '/privacy/', decline: 'Decline', accept: 'Accept' },
    tr: { text: 'Sitenin nasıl kullanıldığını anlamak için Google Analytics kullanıyoruz. Yalnızca kabul ederseniz çalışır.', link: 'Gizlilik', href: '/tr/gizlilik/', decline: 'Reddet', accept: 'Kabul et' }
  }[lang];

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function loadGA() {
    if (window.gtag) return;
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', GA_ID);
  }

  function close() { var el = document.querySelector('.consent'); if (el) el.remove(); }

  function open() {
    if (document.querySelector('.consent')) return;
    var el = document.createElement('div');
    el.className = 'consent'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Cookie consent');
    el.innerHTML = '<p>' + T.text + ' <a href="' + T.href + '">' + T.link + '</a></p>' +
      '<div class="consent-actions"><button type="button" class="btn btn-ghost btn-sm" data-c="denied">' + T.decline + '</button>' +
      '<button type="button" class="btn btn-primary btn-sm" data-c="granted">' + T.accept + '</button></div>';
    el.addEventListener('click', function (e) {
      var c = e.target.getAttribute('data-c'); if (!c) return;
      set(c); close(); if (c === 'granted') loadGA(); else window['ga-disable-' + GA_ID] = true;
    });
    document.body.appendChild(el);
  }

  window.jdConsent = { open: function () { try { localStorage.removeItem(KEY); } catch (e) {} open(); } };

  var c = get();
  if (c === 'granted') loadGA(); else if (c !== 'denied') open();
})();
