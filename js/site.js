/* mattiabaruffaldi.com — comportamenti del sito.
   Niente dipendenze. Tutto degrada: senza JS le pagine restano leggibili,
   i video si aprono su YouTube e le foto si aprono a tutta pagina. */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------------------------------------------------------------
     Testata: fondo opaco solo dopo che si è staccata dal bordo
     --------------------------------------------------------------- */
  var head = document.querySelector('.site-head');
  if (head) {
    var sentinel = document.createElement('div');
    sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:1px;pointer-events:none';
    document.body.prepend(sentinel);
    new IntersectionObserver(function (entries) {
      head.classList.toggle('is-stuck', !entries[0].isIntersecting);
    }, { rootMargin: '-8px 0px 0px 0px' }).observe(sentinel);
  }

  /* ---------------------------------------------------------------
     Rivelazioni allo scroll, con sfalsamento dentro un gruppo
     --------------------------------------------------------------- */
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.06 });

    reveals.forEach(function (el) {
      var i = Number(el.dataset.stagger || 0);
      if (i) el.style.setProperty('--d', Math.min(i, 6) * 70 + 'ms');
      io.observe(el);
    });
  }

  /* ---------------------------------------------------------------
     Hero: accende il titolo e, su schermi larghi, il loop di sfondo
     --------------------------------------------------------------- */
  var hero = document.querySelector('.hero');
  if (hero) {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add('is-lit'); });
    });

    var media = hero.querySelector('.hero__media');
    var loopId = media && media.dataset.loop;
    var wide = window.matchMedia('(min-width: 48rem)');

    if (loopId && wide.matches && !reduced.matches) {
      // Parte subito, non aspetta il `load` della pagina.
      //
      // Il loop NON usa `loop=1&playlist=ID`: quel parametro trasforma il video
      // in una playlist e YouTube mostra i pulsanti precedente/pausa/successivo
      // sopra l'immagine. Si usa invece l'API, che riavvolge a fine video
      // lasciando il fotogramma pulito.
      var host = document.createElement('div');
      host.setAttribute('aria-hidden', 'true');
      media.appendChild(host);

      // Il video si mostra solo quando sta DAVVERO suonando. Se l'autoplay
      // viene bloccato, o l'API non risponde, resta la fotografia: meglio una
      // locandina ferma che un rettangolo nero.
      function mostra() {
        var f = media.querySelector('iframe');
        if (!f) return false;
        f.setAttribute('tabindex', '-1');
        f.title = 'Showreel, riproduzione muta';
        f.classList.add('is-ready');
        return true;
      }

      window.onYouTubeIframeAPIReady = function () {
        // Host standard, non youtube-nocookie: con quello l'API non riesce a
        // parlare col player, quindi `onStateChange` non arriva e il loop muore.
        new YT.Player(host, {
          videoId: loopId,
          playerVars: {
            autoplay: 1, mute: 1, controls: 0, playsinline: 1,
            modestbranding: 1, rel: 0, disablekb: 1, fs: 0,
            iv_load_policy: 3
          },
          events: {
            onReady: function (ev) { ev.target.mute(); ev.target.playVideo(); },
            onStateChange: function (ev) {
              if (ev.data === YT.PlayerState.PLAYING) mostra();
              if (ev.data === YT.PlayerState.ENDED) {
                ev.target.seekTo(0);
                ev.target.playVideo();
              }
            }
          }
        });
      };

      var api = document.createElement('script');
      api.src = 'https://www.youtube.com/iframe_api';
      document.head.appendChild(api);
    }
  }

  /* ---------------------------------------------------------------
     Apertura e chiusura delle finestre modali

     Non ci si appoggia all'evento `close` del <dialog>: in alcuni browser
     non arriva, e la pagina resterebbe bloccata dopo la chiusura. Si osserva
     invece l'attributo `open`, che cambia sempre: con Esc, col pulsante,
     cliccando fuori o da codice.
     --------------------------------------------------------------- */
  function watchDialog(dlg, onOpen, onClose) {
    new MutationObserver(function () {
      if (dlg.open) { document.body.classList.add('is-locked'); onOpen(); }
      else { document.body.classList.remove('is-locked'); onClose(); }
    }).observe(dlg, { attributes: true, attributeFilter: ['open'] });
  }

  /* ---------------------------------------------------------------
     Lettore video: iframe creato solo al click (22 embed insieme
     affosserebbero la pagina)
     --------------------------------------------------------------- */
  var player = document.getElementById('player');
  if (player) {
    var pFrame = player.querySelector('.player__frame');
    var pTitle = player.querySelector('.player__title');
    var lastFocus = null;

    function openPlayer(id, title) {
      lastFocus = document.activeElement;
      pTitle.textContent = title;
      pFrame.innerHTML = '';
      var f = document.createElement('iframe');
      f.title = title;
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share';
      f.allowFullscreen = true;
      f.src = 'https://www.youtube-nocookie.com/embed/' + id +
        '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      pFrame.appendChild(f);
      player.showModal();
    }

    watchDialog(player, function () {}, function () {
      pFrame.innerHTML = '';                 // svuotare l'iframe ferma l'audio
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });

    document.querySelectorAll('[data-video]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        if (typeof player.showModal !== 'function') return;   // resta il link a YouTube
        e.preventDefault();
        openPlayer(btn.dataset.video, btn.dataset.title || 'Video');
      });
    });

    player.querySelector('.player__close').addEventListener('click', function () { player.close(); });
    // click fuori dal fotogramma = chiudi
    player.addEventListener('click', function (e) {
      if (!e.target.closest('.player__frame') && !e.target.closest('.player__bar')) player.close();
    });
  }

  /* ---------------------------------------------------------------
     Visore foto: frecce, swipe, precarica il vicino
     --------------------------------------------------------------- */
  var viewer = document.getElementById('viewer');
  if (viewer) {
    var shots = Array.prototype.slice.call(document.querySelectorAll('[data-full]'));
    var vImg = viewer.querySelector('.viewer__stage img');
    var vMeta = viewer.querySelector('.viewer__count');
    var vPrev = viewer.querySelector('[data-dir="prev"]');
    var vNext = viewer.querySelector('[data-dir="next"]');
    var current = 0;
    var vLastFocus = null;

    function show(i) {
      if (i < 0 || i >= shots.length) return;
      current = i;
      var btn = shots[i];
      vImg.src = btn.dataset.full;
      vImg.alt = btn.dataset.alt || '';
      // Il conteggio e' relativo all'insieme, non alle 88 foto totali,
      // anche se le frecce attraversano gli insiemi.
      vMeta.textContent = (btn.dataset.set || '') + ' · ' +
        btn.dataset.idx + '/' + btn.dataset.count;
      vPrev.disabled = i === 0;
      vNext.disabled = i === shots.length - 1;
      [i - 1, i + 1].forEach(function (j) {          // precarico i vicini
        if (shots[j]) { var p = new Image(); p.src = shots[j].dataset.full; }
      });
    }

    shots.forEach(function (btn, i) {
      btn.addEventListener('click', function (e) {
        // senza <dialog> il link porta comunque alla foto a piena risoluzione
        if (typeof viewer.showModal !== 'function') return;
        e.preventDefault();
        vLastFocus = document.activeElement;
        show(i);
        viewer.showModal();
      });
    });

    watchDialog(viewer, function () {}, function () {
      vImg.removeAttribute('src');
      if (vLastFocus && vLastFocus.focus) vLastFocus.focus();
    });

    vPrev.addEventListener('click', function () { show(current - 1); });
    vNext.addEventListener('click', function () { show(current + 1); });
    viewer.querySelector('.viewer__close').addEventListener('click', function () { viewer.close(); });

    viewer.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1); }
    });

    viewer.addEventListener('click', function (e) {
      if (e.target === viewer || e.target.closest('.viewer__stage')) viewer.close();
    });

    var x0 = null;
    viewer.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    viewer.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) show(current + (dx < 0 ? 1 : -1));
      x0 = null;
    }, { passive: true });
  }
})();
