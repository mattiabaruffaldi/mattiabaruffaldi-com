/* Preventivi — motore condiviso fra /studio/ (compilazione) e /quote/ (lettura).

   I dati del preventivo NON stanno sul server: viaggiano nel link, dopo il
   cancelletto. Quella parte il browser non la invia mai, quindi non finisce
   nei log del server ne' nel repository. Chi ha il link vede, nessun altro. */
(function (globale) {
  'use strict';

  var PREVENTIVO = {};

  /* ------------------------------------------------------------------
     Intestazione: i suoi dati
     ------------------------------------------------------------------ */
  PREVENTIVO.intestazione = {
    nome: 'Mattia Baruffaldi',
    ruolo: 'Director / DOP',
    righe: [
      'Via Vallarsa 11, 20139 Milano',
      'info.mattiabaruffaldi@gmail.com',
      '+39 346 475 5599',
      'IBAN IT67G0306952290100000005478'
    ]
  };

  /* ------------------------------------------------------------------
     Catalogo: tutte le voci gia' pronte, lui mette solo i numeri.
     dd = giorni, u = unita', p = prezzo unitario, f = dicitura al posto
     del prezzo ("Included", "By client", "TBD").

     I PREZZI QUI SONO A ZERO DI PROPOSITO. Questo file sta in un repository
     pubblico: scriverci le sue tariffe significherebbe pubblicare il suo
     listino. Li digita lui la prima volta e il browser se li ricorda; il
     pulsante "Ricomincia" li conserva.
     ------------------------------------------------------------------ */
  PREVENTIVO.catalogo = [
    { t: 'Project management', i: [
      { d: 'Pre-production & logistics', n: 'Shotlist, call sheet, permits', dd: 0, u: 1, p: 0 },
      { d: 'Location scouting', n: '', dd: 0, u: 1, p: 0, f: 'TBD' }
    ]},
    { t: 'Production crew', i: [
      { d: 'Photographer', n: 'Mattia Baruffaldi', dd: 1, u: 1, p: 0 },
      { d: 'Camera operator', n: '', dd: 1, u: 1, p: 0 },
      { d: 'Director of photography', n: '', dd: 0, u: 1, p: 0, f: '' },
      { d: 'Assistant', n: '', dd: 0, u: 1, p: 0, f: '' },
      { d: 'Drone operator', n: 'EASA certified', dd: 0, u: 1, p: 0, f: '' },
      { d: 'Talent', n: '', dd: 1, u: 1, p: 0 },
      { d: 'Make-up & hair', n: '', dd: 1, u: 1, p: 0, f: 'By client' },
      { d: 'Stylist', n: '', dd: 1, u: 1, p: 0, f: 'By client' }
    ]},
    { t: 'Equipment', i: [
      { d: 'Camera & lens package', n: 'Canon EOS R5 + RF, Leica Q, cinema camera + cinema lenses', dd: 1, u: 1, p: 0, f: 'Included' },
      { d: 'Lighting & grip kit', n: '', dd: 1, u: 1, p: 0, f: 'Included' },
      { d: 'Drone', n: 'DJI', dd: 0, u: 1, p: 0, f: '' },
      { d: 'Hard drives', n: '1 master + 1 backup', dd: 0, u: 2, p: 0 }
    ]},
    { t: 'Post production', i: [
      { d: 'Photo editing', n: 'Selected images', dd: 0, u: 1, p: 0, f: 'Included' },
      { d: 'Main film', n: '16:9 · 1’30” · 4K', dd: 0, u: 1, p: 0 },
      { d: 'Social contents', n: '9:16 · 15/30” · 1080p', dd: 0, u: 3, p: 0 },
      { d: 'Color correction', n: '', dd: 0, u: 1, p: 0, f: 'Included' },
      { d: 'Sound design & mix', n: '', dd: 0, u: 1, p: 0, f: '' },
      { d: 'Music licence', n: '', dd: 0, u: 1, p: 0, f: '' }
    ]},
    { t: 'Travel & accommodation', i: [
      { d: 'Travel', n: '', dd: 0, u: 1, p: 0, f: 'TBD' },
      { d: 'Accommodation', n: '', dd: 0, u: 1, p: 0, f: 'TBD' }
    ]}
  ];

  PREVENTIVO.vuoto = function (precedente) {
    var oggi = new Date();
    // Le tariffe si ereditano dal preventivo precedente: non stanno nel
    // codice, quindi l'unico posto dove vivono e' il suo browser.
    var catalogo = JSON.parse(JSON.stringify(PREVENTIVO.catalogo));
    if (precedente && precedente.g) {
      catalogo.forEach(function (g) {
        var vecchio = precedente.g.find(function (x) { return x.t === g.t; });
        if (!vecchio) return;
        g.i.forEach(function (v) {
          var w = (vecchio.i || []).find(function (x) { return x.d === v.d; });
          if (w && w.p) v.p = w.p;
        });
      });
    }
    var mesi = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December'];
    return {
      n: '1',
      dt: mesi[oggi.getMonth()] + ' ' + oggi.getFullYear(),
      t: '',
      s: '',
      sc: '',
      g: catalogo,
      dl: [
        { d: 'Main campaign film', n: '16:9 · 1’30” · 4K', q: '1' },
        { d: 'Social contents', n: '9:16 · 15/30” · 1080p', q: '3' },
        { d: 'Retouched still images', n: '', q: '@50' },
        { d: 'Reworks per produced video', n: '', q: '3' }
      ],
      inc: [
        'Full camera, lens and lighting package',
        'Editing and retouch of selected images',
        'Color correction on film and social contents'
      ],
      exc: [
        'Location and permits',
        'Make-up, hair and styling',
        'Shooting days beyond those estimated',
        'Travel and accommodation'
      ],
      ur: [
        { b: 'Web', t: 'websites and company digital channels' },
        { b: 'BTL materials', t: 'brochures, flyers, catalogues, presentations' },
        { b: 'Print', t: 'magazines and printed editorial or promotional media' }
      ],
      urn: 'TV advertising, billboards, OOH and sponsored social media are not included and will be quoted separately.',
      rv: 4,
      rvl: 'Rivalsa INPS 4%',
      vl: '10 days from presentation.',
      iv: '30% on acceptance, 70% on delivery.',
      pg: 'Bank transfer, 60 days end of month.',
      wd: 'Documented expenses and lost profit, set at 60% of the agreed fee.',
      nt: 'Operazione senza applicazione dell’IVA ai sensi dell’art. 1, commi 54-89, L. 190/2014.'
    };
  };

  /* ------------------------------------------------------------------
     Conti
     ------------------------------------------------------------------ */
  function totaleVoce(v) {
    if (!v.p) return 0;
    return v.p * (v.u || 1) * (v.dd && v.dd > 0 ? v.dd : 1);
  }
  function totaleGruppo(g) {
    return (g.i || []).reduce(function (s, v) { return s + totaleVoce(v); }, 0);
  }
  PREVENTIVO.totaleVoce = totaleVoce;
  PREVENTIVO.totaleGruppo = totaleGruppo;

  PREVENTIVO.conti = function (d) {
    var attivi = (d.g || []).filter(function (g) { return totaleGruppo(g) > 0; });
    var fee = attivi.reduce(function (s, g) { return s + totaleGruppo(g); }, 0);
    var riv = Math.round(fee * (Number(d.rv) || 0)) / 100;
    return { attivi: attivi, fee: fee, riv: riv, tot: fee + riv };
  };

  // Formattazione scritta a mano invece di Intl: in alcuni browser la
  // localizzazione italiana non e' completa e il punto delle migliaia sparisce.
  PREVENTIVO.euro = function (n, simbolo) {
    var v = Math.round((Number(n) || 0) * 100) / 100;
    var segno = v < 0 ? '-' : '';
    v = Math.abs(v);
    var intero = String(Math.floor(v));
    var dec = String(Math.round((v - Math.floor(v)) * 100)).padStart(2, '0');
    var gruppi = intero.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return segno + gruppi + ',' + dec + (simbolo ? ' €' : '');
  };

  /* ------------------------------------------------------------------
     Il preventivo dentro il link
     ------------------------------------------------------------------ */
  // Nel link va solo quello che si vede: le voci del catalogo non usate
  // resterebbero a gonfiare l'indirizzo per niente.
  PREVENTIVO.compatta = function (d) {
    var c = {};
    Object.keys(d).forEach(function (k) {
      var v = d[k];
      if (v === '' || v == null) return;
      if (Array.isArray(v) && !v.length) return;
      c[k] = v;
    });
    c.g = (d.g || []).map(function (g) {
      return { t: g.t, i: (g.i || []).filter(function (v) {
        return PREVENTIVO.totaleVoce(v) > 0 || v.f;
      }).map(function (v) {
        var o = { d: v.d };
        if (v.n) o.n = v.n;
        if (v.dd) o.dd = v.dd;
        if (v.u && v.u !== 1) o.u = v.u;
        if (v.p) o.p = v.p;
        if (v.f) o.f = v.f;
        return o;
      }) };
    }).filter(function (g) { return g.i.length; });
    return c;
  };

  function base64url(byte) {
    var bin = '';
    for (var i = 0; i < byte.length; i++) bin += String.fromCharCode(byte[i]);
    return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }
  function daBase64url(s) {
    var b64 = s.replace(/-/g, '+').replace(/_/g, '/');
    while (b64.length % 4) b64 += '=';
    var bin = atob(b64);
    var byte = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) byte[i] = bin.charCodeAt(i);
    return byte;
  }
  async function passa(byte, flusso) {
    var s = new Blob([byte]).stream().pipeThrough(flusso);
    return new Uint8Array(await new Response(s).arrayBuffer());
  }

  // Il primo carattere dice come e' fatto il resto: "z" compresso, "p" no.
  // La compressione taglia il link di circa due terzi; se il browser non ce
  // l'ha si ripiega sul semplice, e la lettura riconosce entrambi.
  PREVENTIVO.codifica = async function (d) {
    var byte = new TextEncoder().encode(JSON.stringify(PREVENTIVO.compatta(d)));
    if (typeof CompressionStream === 'function') {
      try { return 'z' + base64url(await passa(byte, new CompressionStream('gzip'))); }
      catch (e) { /* si ripiega */ }
    }
    return 'p' + base64url(byte);
  };

  PREVENTIVO.decodifica = async function (s) {
    var tipo = s[0], resto = s.slice(1);
    var byte = daBase64url(resto);
    if (tipo === 'z') byte = await passa(byte, new DecompressionStream('gzip'));
    else if (tipo !== 'p') byte = daBase64url(s);   // formato vecchio, senza sigla
    return JSON.parse(new TextDecoder().decode(byte));
  };

  /* ------------------------------------------------------------------
     Disegno del documento
     ------------------------------------------------------------------ */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function riga(v) {
    var q = v.dd && v.dd > 0 ? v.dd : '—';
    var val = v.p ? PREVENTIVO.euro(totaleVoce(v)) :
      '<span class="q-flag">' + esc(v.f || '—') + '</span>';
    return '<tr><td>' + esc(v.d) +
      (v.n ? '<span class="q-it__n">' + esc(v.n) + '</span>' : '') +
      '</td><td class="q-num-cell">' + q +
      '</td><td class="q-num-cell">' + esc(v.u || 1) +
      '</td><td class="q-num-cell">' + (v.p ? PREVENTIVO.euro(v.p) : '—') +
      '</td><td class="q-num-cell">' + val + '</td></tr>';
  }

  PREVENTIVO.disegna = function (d) {
    var c = PREVENTIVO.conti(d);
    var h = PREVENTIVO.intestazione;
    var contatti = h.righe.map(function (r) { return '<div>' + esc(r) + '</div>'; }).join('');

    /* ---- foglio 1: copertina e riepilogo ---- */
    var riepilogo = c.attivi.map(function (g) {
      var note = (g.i || []).filter(function (v) { return totaleVoce(v) > 0; })
        .map(function (v) { return v.d; }).join(', ');
      return '<div class="q-sum__row"><div><div class="q-sum__t">' + esc(g.t) + '</div>' +
        (note ? '<div class="q-sum__n">' + esc(note) + '</div>' : '') +
        '</div><div class="q-sum__v">' + PREVENTIVO.euro(totaleGruppo(g)) + '</div></div>';
    }).join('');

    var uno = '<section class="q-sheet"><div class="q-head">' +
      '<div><h1 class="q-name">' + esc(h.nome) + '</h1>' +
      '<p class="q-role">' + esc(h.ruolo) + '</p></div>' +
      '<div class="q-contact">' + contatti + '</div></div>' +
      '<div class="q-section"><p class="q-meta">Quotation ' + esc(d.n) +
      ' · ' + esc(d.dt) + '</p>' +
      '<h2 class="q-title">' + esc(d.t || 'Untitled') + '</h2>' +
      (d.s ? '<p class="q-sub">' + esc(d.s) + '</p>' : '') + '</div>' +
      (d.sc ? '<div class="q-section"><h3 class="q-h2">Scope</h3>' +
        '<p class="q-text">' + esc(d.sc) + '</p></div>' : '') +
      '<div class="q-section"><h3 class="q-h2">Budget</h3>' +
      '<div class="q-sum">' + riepilogo + '</div>' +
      '<div class="q-tot">' +
      '<div class="q-tot__row"><span class="q-tot__l">Fee</span>' +
      '<span class="q-tot__v">' + PREVENTIVO.euro(c.fee, 1) + '</span></div>' +
      (c.riv ? '<div class="q-tot__row"><span class="q-tot__l">' + esc(d.rvl || 'Rivalsa') +
        '</span><span class="q-tot__v">' + PREVENTIVO.euro(c.riv, 1) + '</span></div>' : '') +
      '<div class="q-grand"><span>Total</span><strong>' +
      PREVENTIVO.euro(c.tot, 1) + '</strong></div></div>' +
      (d.nt ? '<p class="q-note">' + esc(d.nt) + '</p>' : '') +
      '</div><div class="q-num">1 / 3</div></section>';

    /* ---- foglio 2: dettaglio ---- */
    var corpo = c.attivi.map(function (g, i) {
      var voci = (g.i || []).filter(function (v) { return totaleVoce(v) > 0 || v.f; });
      return '<tr class="q-grp"><td colspan="5"><span class="q-grp__n">' +
        ('0' + (i + 1)).slice(-2) + '</span><span class="q-grp__t">' + esc(g.t) +
        '</span></td></tr>' + voci.map(riga).join('') +
        '<tr class="q-sub-row"><td colspan="4">Subtotal</td><td class="q-num-cell">' +
        PREVENTIVO.euro(totaleGruppo(g)) + '</td></tr>';
    }).join('');

    var due = '<section class="q-sheet">' +
      '<div class="q-runhead"><span>' + esc(h.nome) + '</span><span>Budget detail</span></div>' +
      '<table class="q-table"><thead><tr><th>Description</th><th>Days</th>' +
      '<th>Units</th><th>Unit price</th><th>Total</th></tr></thead><tbody>' +
      corpo + '</tbody></table>' +
      '<div class="q-tot">' +
      '<div class="q-tot__row"><span class="q-tot__l">Fee</span>' +
      '<span class="q-tot__v">' + PREVENTIVO.euro(c.fee, 1) + '</span></div>' +
      (c.riv ? '<div class="q-tot__row"><span class="q-tot__l">' + esc(d.rvl || 'Rivalsa') +
        '</span><span class="q-tot__v">' + PREVENTIVO.euro(c.riv, 1) + '</span></div>' : '') +
      '<div class="q-tot__row" style="border-top:1.5px solid var(--q-rule);padding-top:4mm">' +
      '<span class="q-tot__l" style="color:var(--q-ink)">Total</span>' +
      '<span class="q-sum__v">' + PREVENTIVO.euro(c.tot, 1) + '</span></div></div>' +
      '<div class="q-num">2 / 3</div></section>';

    /* ---- foglio 3: consegne e condizioni ---- */
    var consegne = (d.dl || []).map(function (x) {
      return '<li><span><b>' + esc(x.d) + '</b>' +
        (x.n ? '<span class="q-it__n">' + esc(x.n) + '</span>' : '') +
        '</span><span class="q-qty">' + esc(x.q) + '</span></li>';
    }).join('');
    var elenco = function (a) {
      return (a || []).map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
    };
    var diritti = (d.ur || []).map(function (x) {
      return '<li><span><b>' + esc(x.b) + '</b> — ' + esc(x.t) + '</span></li>';
    }).join('');
    var condizione = function (l, v) {
      return v ? '<div class="q-term"><p class="q-term__l">' + esc(l) + '</p><p>' +
        esc(v) + '</p></div>' : '';
    };

    var tre = '<section class="q-sheet">' +
      '<div class="q-runhead"><span>' + esc(h.nome) + '</span><span>Deliverables &amp; terms</span></div>' +
      (consegne ? '<div class="q-section"><h3 class="q-h2">Deliverables</h3>' +
        '<ul class="q-list">' + consegne + '</ul></div>' : '') +
      '<div class="q-cols">' +
      '<div><h4 class="q-h3">Included</h4><ul class="q-bul">' + elenco(d.inc) + '</ul></div>' +
      '<div><h4 class="q-h3">Excluded</h4><ul class="q-bul">' + elenco(d.exc) + '</ul></div>' +
      '</div>' +
      (diritti ? '<div class="q-section"><h3 class="q-h2">Usage rights</h3>' +
        '<ul class="q-bul" style="margin-top:4mm">' + diritti + '</ul>' +
        (d.urn ? '<p class="q-note">' + esc(d.urn) + '</p>' : '') + '</div>' : '') +
      '<div class="q-section"><h3 class="q-h2">Terms</h3><div class="q-terms">' +
      condizione('Validity', d.vl) +
      condizione('Fee', PREVENTIVO.euro(c.fee, 1) + (c.riv ? ' plus ' + (d.rv || 0) + '% INPS contribution.' : '')) +
      condizione('Invoicing', d.iv) +
      condizione('Payment', d.pg) +
      condizione('Withdrawal', d.wd) +
      '</div></div>' +
      '<div class="q-sign">' +
      '<div><p class="q-sign__l">Accepted and agreed' +
      (d.cl ? ' — ' + esc(d.cl) : '') + '</p>' +
      '<div class="q-sign__line"></div><p class="q-sign__c">Date and signature</p></div>' +
      '<div><p class="q-sign__l">' + esc(h.nome) + '</p>' +
      '<div class="q-sign__line"></div><p class="q-sign__c">Signature</p></div>' +
      '</div><div class="q-num">3 / 3</div></section>';

    return uno + due + tre;
  };

  globale.PREVENTIVO = PREVENTIVO;
})(window);
