# mattiabaruffaldi.com — sito personale di Mattia Baruffaldi

Memoria di progetto. Leggere all'inizio di ogni sessione. (L'utente parla italiano.)

## Cos'è
Sito **statico** (HTML/CSS/JS puro, nessun framework) di **Mattia Baruffaldi**,
filmmaker e fotografo. Nato in Valtellina (provincia di Sondrio), vive a Milano.
Freelance con case di produzione: Lamborghini, Ducati, Moncler, Kappa.
**Il sito è in inglese** (come il precedente).

Sostituisce il vecchio sito Squarespace su **www.mattiabaruffaldi.com**.

- **Cartella:** `~/Desktop/WWW/mattiabaruffaldi-com`
- **Anteprima locale:** `python3 -m http.server 8010` → http://localhost:8010
- **Repo:** https://github.com/hellonorthsidecc-ai/mattiabaruffaldi-com — **privato**, branch `main`
- **Pubblicazione:** GitHub Pages (vedi "Da fare" se non ancora attivo)

## Flusso di lavoro (IMPORTANTE)
1. **Modifico i dati o i file**
2. `python3 tools/build.py` per rigenerare le pagine
3. L'utente controlla su **http://localhost:8010** con un normale Cmd+R:
   `build.py` appende una firma del contenuto agli indirizzi di CSS e JS
   (`site.css?v=9a8ad6f9`), quindi le modifiche arrivano subito. Non serve
   piu' il refresh forzato, e vale anche per i visitatori dopo un aggiornamento.
4. Quando è soddisfatto: committo io, **ma il push lo fa lui**

> ⚠️ **Non posso fare push su questo repo.** Il token nel portachiavi è quello
> fine-grained di NSCC, autorizzato solo su quel repository: qui torna
> `403 Write access to repository not granted`. Quindi: io committo in locale,
> poi lui clicca **"Push origin"** in GitHub Desktop. Se un giorno aggiunge
> questo repo ai permessi del token, il push torna a farlo Claude
> (con `dangerouslyDisableSandbox: true`, serve il portachiavi macOS).

> L'utente NON usa git da riga di comando. Non è tecnico: spiegare i passaggi
> senza dare per scontato git/CSS.

## Come è fatto
`tools/build.py` è il **generatore**: contiene tutti i contenuti (video, testi,
descrizioni delle foto) e sputa fuori HTML statico. **Non modificare a mano gli
`.html` generati**: si sovrascrivono al build successivo. Per cambiare un titolo,
aggiungere un video o una foto, si modifica `build.py` e si rilancia.

```
tools/build.py     generatore + TUTTI i contenuti
css/site.css       sistema visivo completo (token, componenti, movimento)
js/site.js         testata, rivelazioni, lettore video, visore foto
fonts/             Archivo variabile ospitato qui (2 file woff2, 176 KB)
img/hero.jpg       fotogramma dell'hero (Lamborghini, 2500px)
img/video/<id>.jpg 22 anteprime YouTube scaricate in locale
img/photo/<set>/   88 foto a 1800px + `thumb/` a 800px
index.html film/ photo/ lifetalks/ info/   generati
about/ contatti/ portfolio-video/ photo/*/ ponti dai vecchi indirizzi Squarespace
```

Pagine con URL puliti tramite cartelle (`film/index.html` → `/film/`), così
localhost e GitHub Pages si comportano identici.

## Decisioni di design prese
- **Lane:** camera oscura / sala di montaggio. Non il "black minimal" da template.
- **Colore:** superficie grafite quasi-nera `oklch(0.145 0.004 260)`. UI
  **monocromatica** di proposito: il colore lo portano le fotografie. Un solo
  accento, **ambra** `oklch(0.795 0.155 68)` ("luce di sicurezza"), usato solo
  per hover, focus e stati. Non aggiungere altri colori.
- **Font: Archivo variabile**, una sola famiglia sfruttata ai due estremi
  dell'asse larghezza (`wdth`): **82 condensato** per wordmark ed etichette
  (coerente col suo logo esistente), **118 espanso peso 700** per i titoli
  display. Ospitato in locale: nessuna chiamata a Google, nessun cookie terzo.
- **Logo:** wordmark spaziato `img/logo-2c.png` (suo), reso bianco in
  `img/wordmark.png`. Sostituisce monogramma + nome scritto.
- **Pagina Info:** la foto sta in griglia col testo e si allunga fino a dove
  finisce la biografia (`align-items: stretch`, niente proporzione fissa da
  56rem in su). I contatti stanno **sotto**, a tutta larghezza su quattro
  colonne. `object-position: 50% 32%` tiene il viso dentro quando il taglio
  si fa basso.
- **In home nessun credito cliente** sotto i video: "Unreal × …" si vede solo
  nella pagina Film. In home i link "All N films" / "All N photographs" stanno
  **sotto** la griglia, non accanto al titolo (accanto non li notava).
- **Niente descrizioni sotto i titoli di sezione**, ne' conteggi tipo
  "30 frames": le ha fatte togliere tutte (ago 2026). Titolo e basta.
- **Due soli gruppi di film**: Automotive and motorsport, Sport and apparel.
  La sezione Documentary e' stata eliminata, quei film stanno in Sport and
  apparel insieme a Powerstage RR.
- **TUTTE le griglie sono uniformi.** Feedback esplicito suo (ago 2026): non
  gli piacciono foto e video distribuiti a misure diverse, li vuole "puliti e
  minimal". Film 2 per riga, foto 3 per riga, nessuna eccezione, nessun
  mosaico, nessun riquadro grande in cima. **Non riproporre layout a mosaico
  o a zigzag.** I riquadri grandi mostravano anche la grana degli scatti.
- **Niente tacche d'angolo.** C'erano dei segni tipo mirino agli angoli delle
  immagini: gliele ho tolte perche' non gli piacevano. Non rimetterle.
- **Nessuna desaturazione, mai.** Feedback suo (ago 2026): non gli piaceva che
  foto e video fossero smorti finche' non ci passavi sopra col mouse. Le
  immagini vanno mostrate **coi colori naturali**, sono gia' graduate da lui.
  All'hover si muove solo la scala. Non reintrodurre `filter: saturate(...)`
  o `brightness(...)` sulle immagini.
- **Hero senza scritte.** Niente nome, niente sottotitolo, niente pulsanti:
  solo il video a tutto schermo e un unico link **Portfolio** in basso a
  sinistra che porta a `/film/`. Il tag `<h1>` resta ma `visually-hidden`,
  serve a Google e agli screen reader. Le due sfumature sull'hero servono
  solo a leggere logo/menu in alto e ad agganciare la pagina nera in basso.
- **Selezione home:** solo film la cui anteprima YouTube è un **fotogramma
  pulito**. Diverse anteprime hanno titoli e loghi stampati sopra (una ha
  "3000 STEPS!!" con l'emoji): a grande dimensione fanno sembrare la pagina una
  griglia di YouTube. Sulla pagina Film ci sono tutte, ma più piccole.
- **Hero a tutto schermo esatto.** `--head-h` (4.25rem) è l'altezza fissa
  della testata: l'hero la usa come margine negativo per partire dal bordo
  alto e ha `min-height: 100svh`, così arriva esatto in fondo senza avanzi.
  Se si cambia l'altezza della testata, si cambia solo quel token.
- **Hero: video del sito, NON YouTube.** `img/showreel-loop.mp4` (primi 24s
  dello showreel 2024, 1920×1080, muto, ~7 MB) in un `<video autoplay muted
  loop playsinline>`. La locandina è il primo fotogramma del video stesso
  (`img/showreel-poster.jpg`), così non si vede nessun cambio di immagine.
  Sorgente: `~/Desktop/FILM/SHOWREEL/2024/export/Showreel_2024_V2.mp4`,
  ricodificabile con ffmpeg (installato; yt-dlp no).
  **Motivo:** con l'embed YouTube comparivano i comandi del player sopra
  l'hero e si vedeva la fotografia d'attesa prima della partenza. Non
  tornare a YouTube per l'hero. Il lettore su click resta YouTube.
- **Video:** 22 iframe insieme affosserebbero la pagina. Anteprime locali,
  iframe creato **solo al click**, e svuotato alla chiusura per fermare l'audio.
- **Crediti film:** `Unreal × <cliente>`. Unreal Media House e' la casa di
  produzione con cui lavora da sempre; va nominata, non solo il brand.
- **Home:** niente sezione "Clients" (rimossa su sua richiesta) e niente
  striscia foto che scorre di lato: tre scatti fermi piu' il link.

## Trappole già incontrate (non ripeterle)
- **MAI mettere `display` su `.player` / `.viewer` senza `[open]`.** Il browser
  nasconde un `<dialog>` chiuso con `dialog:not([open]) { display: none }`, ma
  quella regola sta nel foglio del *browser* e qualunque `display` scritto nel
  CSS del sito la batte (l'origine autore vince sull'origine user-agent, la
  specificita' non conta). Con `display: grid` sulla classe nuda la finestra del
  lettore restava visibile sopra la pagina appena si apriva il sito. Bug vero,
  trovato da lui, che io avevo liquidato come artefatto delle catture.
- **Niente YouTube nell'hero.** Provato e scartato: con `loop=1&playlist=ID`
  YouTube disegna i pulsanti precedente/pausa/successivo sopra l'hero; con
  l'API IFrame e `host: youtube-nocookie` gli eventi non arrivano affatto; e
  in ogni caso prima della partenza si vedeva la locandina. Risolto ospitando
  il file video.
- **La finestra di Chrome guidata dall'automazione, se non e' in primo piano,
  congela paint e transizioni**: le catture escono nere o a metà animazione e i
  valori di `opacity`/`transform` restano bloccati. Misurare col DOM, e per le
  catture disattivare le transizioni con
  `*{transition:none !important;animation:none !important}`.
- **L'evento `close` del `<dialog>` non scatta** in alcuni browser. Non
  appoggiarsi a quello: `watchDialog()` in `site.js` osserva l'attributo `open`
  con un MutationObserver. Prima, chiudendo una foto, la pagina restava bloccata.
- **`.film__frame` è uno `<span>`**: senza `display: block` né `aspect-ratio`
  né `overflow: hidden` si applicano.
- **`<dialog>` modale nasce con `margin: auto`** e un `max-height` del browser:
  vanno azzerati o il contenuto sfonda il fondo dello schermo. E i limiti di
  altezza dell'immagine vanno in unità di viewport, non in percentuale (una
  percentuale su un elemento di griglia non risolve sempre).
- **L'anteprima YouTube dello showreel è una schiacciata nera** col solo titolo:
  sostituita da `img/hero.jpg` tramite il dizionario `POSTER`.
- Le **catture schermo di Chrome** in questo ambiente trascinano livelli
  fantasma quando ci sono iframe YouTube o `backdrop-filter`: non fidarsi dei
  pixel, misurare col DOM.
- Il resize della finestra non scende sotto ~864px: per provare il mobile,
  caricare il sito in un **iframe da 390px** (le media query rispondono al
  viewport dell'iframe) o misurare col DOM.

## Verifiche già passate
Struttura HTML valida su tutte le pagine, tutte le `img` con `alt` scritto a mano
guardando la foto, nessuna ancora orfana, nessuno sfondamento orizzontale a
390px. Contrasti: titoli 18,5:1 · corpo 8,4:1 · metadati 4,9:1 · ambra 10:1 ·
bordi dei controlli 3,1:1.

## Da fare / aperto
- [x] Repo creato e pubblicato (privato) su `hellonorthsidecc-ai`.
- [ ] **Pages da accendere**: Settings → Pages → Deploy from a branch →
      `main` / `(root)`. Il file `CNAME` è già nel repo, quindi GitHub imposterà
      da solo il dominio e mostrerà un avviso rosso sul DNS finché non si
      cambiano i record: è normale, sparisce dopo il passaggio.
- [ ] **Spostare il repo su un account personale suo.** Ha detto chiaramente
      (ago 2026) che non vuole il suo sito sotto l'account `hellonorthsidecc-ai`,
      ma ha scelto di pubblicare prima e spostare poi. Si fa con Settings →
      Transfer ownership: si tiene tutta la cronologia, cambia solo il record
      DNS del `www` verso `<nuovoutente>.github.io`. **Ricordarglielo.**
- [ ] **DNS ancora su Squarespace.** Va spostato al registrar: `CNAME www` →
      `<utente>.github.io` e i 4 record A di GitHub Pages per il dominio nudo.
      Finché non si sposta, il sito live resta quello vecchio.
      **Il registrar è GoDaddy.** Il DNS lo deve cambiare lui: non ho accesso
      al suo account e non devo inserire credenziali.
- [x] Ritratto: `img/portrait.jpg`, taglio 3:4 da
      `img/GS_240515_RBCA_Stunt_1897.jpg` (lui con la cinepresa, Genova dietro).
- [ ] **Cliente non dichiarato** per "The Hyper Contrast Capsule": lasciato in
      bianco di proposito invece di indovinare. Chiederglielo.
- [ ] **Verificare quali film NON sono Unreal.** Ho messo `Unreal × <cliente>`
      su tutti i film con brand; se qualcuno e' passato da un'altra produzione
      va corretto nel dizionario `FILM`.
- [ ] Valutare una pagina privacy: l'hero carica YouTube (in modalità
      nocookie) in automatico su desktop.
- [ ] Le foto vengono dal CDN di Squarespace, quindi già compresse da loro. Se
      vuole, si rifanno dagli originali in `~/Desktop/FOTO`.

## Note di stile comunicazione
Rispondere in **italiano**, tono pratico e chiaro. Procedere una modifica alla
volta e far verificare su localhost prima di pubblicare.
