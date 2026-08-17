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
- **Pubblicazione:** GitHub Pages (vedi "Da fare" se non ancora attivo)

## Flusso di lavoro (IMPORTANTE)
1. **Modifico i dati o i file**
2. `python3 tools/build.py` per rigenerare le pagine
3. L'utente controlla su **http://localhost:8010** e ricarica con Cmd+R
4. Solo quando è soddisfatto → **push** (lo faccio io)
5. Il push richiede `dangerouslyDisableSandbox: true` (serve il portachiavi macOS)

> L'utente NON usa git da riga di comando. Pubblico io. Non è tecnico:
> spiegare i passaggi senza dare per scontato git/CSS.

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
- **Motivi ricorrenti:** tacche d'angolo tipo mirino (`.ticks`); miniature
  leggermente graduate a riposo che vanno a pieno colore all'hover (come un
  color grading); rapporti d'aspetto reali (16:9 video, 3:2 foto).
- **Griglia foto:** dentro una riga le misure sono **uguali**. Le foto sono
  tutte 3:2, quindi larghezze diverse darebbero altezze diverse e buchi. Il
  ritmo lo fa il numero di foto per riga (`RITMO` in build.py).
- **Griglia film in home:** zigzag 7/5 → 5/7 → 6/6 con `align-items: end`, così
  lo scarto di altezza diventa aria in alto e le didascalie si allineano.
- **Selezione home:** solo film la cui anteprima YouTube è un **fotogramma
  pulito**. Diverse anteprime hanno titoli e loghi stampati sopra (una ha
  "3000 STEPS!!" con l'emoji): a grande dimensione fanno sembrare la pagina una
  griglia di YouTube. Sulla pagina Film ci sono tutte, ma più piccole.
- **Hero:** locandina fotografica + loop muto dello showreel da YouTube che
  parte dopo il primo disegno, solo su schermi ≥60rem e senza reduced-motion.
- **Video:** 22 iframe insieme affosserebbero la pagina. Anteprime locali,
  iframe creato **solo al click**, e svuotato alla chiusura per fermare l'audio.

## Trappole già incontrate (non ripeterle)
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
- [ ] **Repo GitHub + Pages non ancora creati.** Serve l'utente per creare il
      repo; poi Settings → Pages → branch `main`, e `CNAME` è già pronto.
- [ ] **DNS ancora su Squarespace.** Va spostato al registrar: `CNAME www` →
      `<utente>.github.io` e i 4 record A di GitHub Pages per il dominio nudo.
      Finché non si sposta, il sito live resta quello vecchio.
- [ ] **Manca un ritratto di lui.** La pagina Info usa `people-09` (una figura
      in muta di spalle), che non dichiara di essere lui. Se ne fornisce uno, va
      sostituito in `pagina_info()`.
- [ ] **Cliente non dichiarato** per "The Hyper Contrast Capsule": lasciato in
      bianco di proposito invece di indovinare. Chiederglielo.
- [ ] Valutare una pagina privacy: l'hero carica YouTube (in modalità
      nocookie) in automatico su desktop.
- [ ] Le foto vengono dal CDN di Squarespace, quindi già compresse da loro. Se
      vuole, si rifanno dagli originali in `~/Desktop/FOTO`.

## Note di stile comunicazione
Rispondere in **italiano**, tono pratico e chiaro. Procedere una modifica alla
volta e far verificare su localhost prima di pubblicare.
