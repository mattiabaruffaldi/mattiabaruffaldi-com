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
- **Repo:** https://github.com/mattiabaruffaldi/mattiabaruffaldi-com — **PUBBLICO**, branch `main`.
  Spostato sul suo account personale (ago 2026): quel punto in sospeso e' chiuso.
  **Pubblico vuol dire che qualunque cosa committata e' leggibile da chiunque,
  per sempre, anche se poi la togli.** Niente tariffe, niente preventivi, niente
  link di preventivo dentro i file del repository.
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
img/photo/<set>/   90 foto a 1800px + `thumb/` a 800px
img/bts/           6 foto dietro le quinte (pagina Info)
originali/         file sorgente pesanti, ESCLUSI da git (.gitignore)
index.html film/ photo/ lifetalks/ info/   generati
studio/index.html  compilatore preventivi (SCRITTO A MANO, non generato)
quote/index.html   lettore di UN preventivo   (SCRITTO A MANO)
quotes/index.html  indice di PIU' preventivi  (SCRITTO A MANO)
css/quote.css js/quote.js               motore preventivi
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
- **Pagina Info: biografia a colonna singola, poi la griglia del dietro le
  quinte** (`img/bts/`, sei foto recuperate dal vecchio About di Squarespace,
  che gli piaceva). Niente contatti (ci sono gia' nel piede) e niente ritratto
  grande accanto al testo: la foto di Genova e' la prima della griglia.
- **Menu da telefono:** sotto 48rem la nav sparisce e compare un pulsante a
  due linee che apre un `<dialog>` a tutto schermo. **Il `<dialog>` va incluso
  nella regola che azzera `margin` e `max-height`** (`.player, .viewer, .menu`),
  altrimenti il margine di default del browser gli impedisce di coprire lo
  schermo.
- **I link di sezione in home sono pulsanti** (`.btn`), non testine: quelli
  piccoli non li notava. E senza numeri: "See all films", non "All 20 films".
- **SEO:** ogni pagina ha titolo e descrizione propri, canonical, anteprima
  social dedicata in `img/og/`, e un blocco JSON-LD (`Person` + `WebSite`,
  piu' `ImageGallery` su Photo e `ProfilePage` su Info) generato da
  `dati_strutturati()`. Sitemap e robots.txt aggiornati dal build.
- **Le foto in home non sono cliccabili** (scelta sua, ago 2026): niente link
  e niente reazione all'hover, che suggerirebbe un collegamento inesistente.
  Alla galleria ci si va col link sotto la griglia.
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
  alto. L'altezza e' `var(--vh)`, che il JS scrive con `window.innerHeight`
  vero e aggiorna a ogni resize, orientamento e `fullscreenchange`.
  **Non tornare a `100svh` da solo:** `svh` e' l'altezza minima (tutte le
  barre aperte), quindi a schermo intero sotto restava una striscia nera. Ha
  segnalato il problema tre volte. Verificato a 1440x900, 1512x1400,
  1100x1500 e 390x844: zero bande sopra e sotto.
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

## Preventivi — `/studio/` e `/quote/`
Strumento suo per fare preventivi, nato ad agosto 2026 dal preventivo VVENA.
**Queste due pagine sono scritte a mano, non le genera `build.py`.**

- `/studio/` — dove compila. I blocchi stanno **a fisarmonica, uno aperto
  alla volta** (sua richiesta): si riempie e si preme "Avanti". Anteprima del
  documento a fianco, che si compone mentre scrive.
- **Una sola troupe di default**, chiamata "Production crew": la seconda si
  ottiene col pulsante "+ duplica blocco". Non rimettere Crew A / Crew B nel
  catalogo. Vale anche per le trasferte.
- I titoli dei blocchi si riscrivono; "+ voce" aggiunge righe non previste,
  "+ duplica blocco" e "Elimina blocco" gestiscono i blocchi.
- **La spunta di una voce comanda su tutto** (`v.on`). Prima l'attivazione si
  deduceva dal prezzo: una voce spuntata ma ancora senza cifra si rispuntava
  da sola al primo ridisegno, e sembrava che le spunte non funzionassero.
  Togliendo la spunta prezzo e dicitura NON si azzerano: se la rimette, li
  ritrova.
- **Ogni pulsante nuovo dentro i blocchi va aggiunto al `closest()`** del
  gestore dei click, altrimenti non scatta e basta (successo con `data-del`).
- Intestazione a scelta fra lui e Unreal Srl (`PREVENTIVO.intestazioni`).
- **Giornate di produzione una volta sola**, in cima. Le voci con `dd` diverso
  da 0 le seguono; `ddx` segna quelle con giornate proprie (il drone che ne fa
  4 mentre la troupe ne fa 11). Svuotando il campo giorni si torna a seguire
  il valore globale. Nel link le giornate viaggiano gia' risolte, cosi'
  `/quote/` non deve sapere nulla di questo meccanismo.
- **Maggiorazioni multiple** (`d.mag`, elenco di `{l, p}`): rivalsa, IVA e
  agency fee possono stare **insieme**, non si escludono. Si applicano **a
  cascata**: l'agency fee sul budget, l'IVA su budget + agency fee. I pulsanti
  aggiungono quelle pronte, la × le toglie.
- **Lo studio e' a tutta pagina** con l'anteprima a scomparsa (pulsante
  "Anteprima"): a lui interessa vedere i campi, non il layout. Le righe sono
  una tabella: voce · nota · giorni · q.ta' · dicitura · prezzo · totale · ×.
  **Il nome di ogni voce e' modificabile**, e ogni voce si elimina con la ×.
- `/quote/` — quello che vede il cliente, e da cui si stampa il PDF.
- **I dati del preventivo NON stanno sul sito**: viaggiano nel link dopo il
  cancelletto (`/quote/#z...`). Quella parte il browser non la manda mai al
  server, quindi non finisce nei log ne' nel repository. E' sicuro quanto
  mandare un PDF allegato: chi ha il link vede, nessun altro.
- Il link e' compresso con `CompressionStream` (prefisso `z`; `p` se il
  browser non ce l'ha). Senza compressione superava i 4.000 caratteri e
  certi programmi di posta spezzano i link lunghi.
- **NON scrivere le sue tariffe in `js/quote.js`:** il repository e' pubblico,
  sarebbe come pubblicare il listino. Nel catalogo i prezzi stanno a zero.
- **Le tariffe NON si ereditano** da un preventivo all'altro (sua richiesta,
  ago 2026): "le metto io ogni volta". `PREVENTIVO.vuoto()` non prende piu' il
  preventivo precedente. Le tariffe dei lavori gia' fatti restano dentro i
  preventivi salvati in Archivio, da dove si riaprono o si duplicano.
- **Blocchi di default** (ordine deciso da lui, ago 2026): Script, storyboard
  & development · Pre-production · Production crew · Equipment · Post
  production · Travel & accommodation · Miscellaneous. Un solo blocco trasferte
  (prima erano due, "Travel" e "Travel & accommodation"). I nomi nel catalogo
  sono in inglese corretto perche' finiscono nel PDF che legge il cliente.
- Le pagine sono `noindex` e non sono linkate da nessuna parte, ne' stanno
  nella sitemap. **Non metterle in `robots.txt`**: elencarle la' significa
  rivelarne l'indirizzo a chiunque legga quel file.

### Lucchetto su `/studio/` (ago 2026)
`CHIAVE_HASH` in `studio/index.html` contiene l'**impronta SHA-256** della
password, mai la password: il repository e' pubblico e chiunque legge quel
file. Vuota = studio aperto senza chiedere niente.

- **Per impostarla:** lui apre `/studio/#password`, scrive la password che
  vuole, e manda il codice che compare. La password non esce dal suo
  computer e non deve mai finire in una conversazione o in un commit.
- Lo sblocco sta in `sessionStorage`: non richiede finche' non chiude il
  browser, e non resta in giro dopo.
- **Non e' sicurezza, e non va raccontata come tale.** Il controllo sta nel
  browser di chi guarda: chi apre gli strumenti da sviluppatore entra
  comunque, e i preventivi nel `localStorage` si leggono lo stesso. Tiene
  fuori chi capita sull'indirizzo o chi si siede al suo computer.
- Se un domani servisse protezione vera servirebbe un servizio esterno
  (stessa conversazione dei link corti), oppure cifrare l'archivio con la
  password — che pero' vuol dire perdere tutto se la dimentica.

### Un preventivo nuovo parte VUOTO (ago 2026)
Nel catalogo ogni voce ha `on: false`: **niente e' spuntato di partenza**,
lui accende quello che serve. Prima l'attivazione si deduceva dal prezzo o
dalla dicitura, e mezze voci (Make-up "By client", Canon "Included", Travel
"TBD") comparivano da sole nel documento del cliente.

- **Scrivere una cifra accende la riga da sola**, se no sarebbe un click in
  piu' per ogni voce. Togliere la spunta resta un gesto suo, e il prezzo non
  lo disfa.
- Diciture tolte dai predefiniti: "By client" su make-up e stylist,
  "Included" su Canon e Photo editing. Restano i "TBD" su trasferte e
  Miscellaneous, che lui non ha chiesto di togliere.
- Voci tolte dal catalogo: Leica Q, Drone travel, Mileage, On-site expenses,
  Set materials.
- Il catalogo NON e' versionato e non viaggia nei link: si puo' cambiare
  liberamente. Le **consegne** invece sono nei testi standard, e per quelle
  serve una versione nuova (vedi qui sotto).

### Consegne da spuntare (ago 2026)
Le Deliverables non erano modificabili: arrivavano fisse dai testi standard.
Ora sono una sezione dello studio, con la stessa riga delle voci ma senza
prezzi: spunta · nome · formato · quantita' · elimina.

- `d.dl` e' l'elenco **completo**, con `on: false` su quelle disponibili ma
  non usate in quel preventivo. Nel link e nel documento vanno **solo le
  spuntate**, senza la spunta (`PREVENTIVO.consegneAttive`).
- La quantita' e' testo, non numero: certe consegne si scrivono "@50".
- La sezione nello studio si chiama **Delivery** (sua parola). Nel documento
  del cliente il titolo resta **Deliverables**.
- **Testi standard alla versione 3** (`PREVENTIVO.DV = 3`). La 1 e la 2 non
  si toccano: i tre VVENA hanno `dv: 1` e continuano a mostrare le consegne
  di allora. Verificato dopo ogni cambio.
  E' esattamente il motivo per cui quel meccanismo esiste: **quando cambi
  un testo standard aggiungi una versione, non modifichi quella vecchia.**
  - v1: consegne originali (Main campaign film, Social contents, ...)
  - v2: primo elenco da spuntare, con Teaser e Behind the scenes
  - v3: elenco corto (Main video, Social video contents, Retouched still
    images) e niente spuntato di partenza

### Il PDF deve stare in 3 pagine (ago 2026)
Ogni `.q-sheet` deve entrare in **una** pagina A4. Prima non ci entrava: i
fogli venivano 302-369mm contro i 297 disponibili, quindi ognuno si portava
dietro una seconda pagina quasi vuota e il PDF usciva di 6 pagine invece di 3.

- Il margine del foglio (`--q-pad`) e' **14mm**, non 18. Le spaziature del
  documento sono **misurate**, non scelte a occhio: coi tre preventivi VVENA
  i fogli vengono 247-285mm, cioe' 12-50mm di margine.
- **Le stesse misure valgono a schermo e in stampa**: l'anteprima e' il PDF.
  Non rimettere le spaziature dentro `@media print` soltanto.
- **Se tocchi una spaziatura del documento, rimisura**, e misura come misura
  la stampa:
  - **contando i margini**, non solo `getBoundingClientRect().height`. La
    prima volta li avevo esclusi: a schermo tornava, in PDF no.
  - con `?x=<timestamp>` **prima** del cancelletto nell'indirizzo
    dell'iframe, se no il browser serve la pagina e il CSS dalla cache e si
    misura la versione vecchia senza accorgersene.
- **`.q-sheet + .q-sheet` (due classi) batte `.q-sheet` (una) anche dentro
  `@media print`.** Il `margin: 0` del blocco di stampa non azzerava il
  `margin-top: 10mm` fra i fogli: in stampa i fogli 2 e 3 partivano 10mm
  piu' in basso e sforavano di un pelo. Un pelo costa **una pagina intera**,
  perche' la coda va sulla pagina dopo e il salto forzato ne apre un'altra.
  Nel blocco di stampa vanno nominati **tutti e due** i selettori.
- Margine di sicurezza attuale: 14mm nel caso peggiore (Origin). Sotto i
  10mm conviene tagliare qualcosa.
- Nello studio, accanto al totale, c'e' **quante pagine viene il PDF**
  (`contaPagine()`): disegna il documento fuori campo e lo misura. Diventa
  ambra quando un foglio non ci sta in una pagina sola. Serve a non dover
  stampare per scoprirlo.
- Per i preventivi davvero lunghi il dettaglio continua sulla pagina dopo:
  e' giusto. Le regole di stampa tengono interi totali, firme e condizioni,
  e non lasciano l'intestazione di un blocco da sola in fondo alla pagina.

### `/quotes/` — piu' preventivi in un link solo (ago 2026)
Pagina con una casella per preventivo (numero, titolo, sottotitolo, scope,
totale, "Open quotation"); ogni casella apre `/quote/` col suo preventivo.
Si genera dallo studio: filtra per cliente e premi **"Link con questi N"**.

- **Perche' non una pagina committata con dentro i link:** il repository e'
  pubblico, quindi ci finirebbero le sue tariffe per sempre. Qui nel repo c'e'
  solo il guscio; i dati stanno nel link dopo il cancelletto, come per `/quote/`.
- **I preventivi si comprimono INSIEME**, non uno per uno: condividono
  condizioni, consegne e diritti d'uso, quindi tre uniti fanno ~2.000 caratteri
  contro i ~4.700 di tre link separati. Serve `PREVENTIVO.impacchetta` /
  `spacchetta`, che a differenza di `codifica` non passano da `compatta`.
- L'ordine delle caselle e' per numero: prima i numerici in ordine, poi gli
  altri in ordine alfabetico (per VVENA viene 1, 2, Origin).
- La formattazione dei numeri e' scritta a mano, non con `Intl`: in alcuni
  browser la localizzazione italiana e' incompleta e sparisce il punto delle
  migliaia (5500 invece di 5.500).

### Archivio dei preventivi — FATTO (ago 2026)
`/studio/` e' un **gestionale a due viste** in un solo file: `#v-home`
(l'archivio, dove si arriva) e `#v-edit` (il compilatore). Le viste si
scambiano con `#app[data-vista]`, non con un modale.

- **L'archivio e' la home** (sua richiesta): aprendo `/studio/` si vede
  l'elenco, e da li' si sceglie se riprendere un preventivo o farne uno nuovo.
- **Indirizzi veri:** `/studio/` = archivio, `/studio/#p=<id>` = quel
  preventivo aperto. Il tasto Indietro del browser funziona (`hashchange`, con
  la sentinella `saltoInterno` per non rimbalzare sui salti fatti da noi).
- **Era un `<dialog>` modale: non lo e' piu'.** Un modale non si linka, non
  regge densita' e non e' una schermata di lavoro. Non tornare indietro.
- **Colonna clienti + tabella**, non riquadri: un preventivo e' una riga di
  dati (titolo, n., data, importo, stato) e la tabella li fa confrontare.
  Sotto 62rem la colonna diventa una striscia di pastiglie scorrevole; sotto
  52rem la tabella si impila e le colonne numeriche lasciano il posto a
  `.meta-m` (una riga sola "n. · data · importo").
- **Stati: Bozza / Inviato / Accettato / Perso** (`d.st`, e `stato` nella voce
  d'archivio). Sono un `<select>` vero, non un aggeggio inventato; il colore
  non e' mai l'unico segnale, la parola c'e' sempre. Filtri per stato in cima.
- **Annullare invece di confermare**: eliminare un preventivo o un blocco non
  chiede conferma, lo toglie e offre "Annulla" per 7 secondi.
- **Rinomina in linea** (Invio conferma, Esc annulla), non `prompt()`.
- Scorciatoie: `/` porta sulla ricerca, `Esc` la svuota.

**Vincolo che ha deciso tutto:** il repository e' pubblico, quindi i preventivi
non si possono committare. L'archivio sta **nel browser**, chiave
`mb-archivio`: un elenco di `{id, cliente, titolo, n, agg, tot, dati}`
(`agg` = data ultimo salvataggio). `mb-preventivo` resta la bozza aperta.

- **Le "cartelle" sono il campo Cliente**, raggruppato al momento del disegno:
  non c'e' nessuna struttura separata da tenere allineata, e cambiare cliente a
  un preventivo lo sposta di cartella da solo. Le cartelle sono in ordine
  alfabetico, "Senza cliente" sempre in fondo; dentro, il piu' recente in cima.
- **Si archivia da solo quando la bozza ha un titolo** (senza titolo non c'e'
  niente da ritrovare). Salvataggio ritardato di 700 ms per non scrivere a ogni
  tasto, piu' un `beforeunload` per chi chiude la scheda a meta' parola.
- Per riga: **apri · duplica · rinomina · elimina**. La matita accanto al nome
  della cartella **rinomina il cliente su tutti** i suoi preventivi insieme.
  "Duplica" apre subito la copia, pronta da modificare.
- **Esporta / Importa** un file `.json`: e' il **vero backup**, e va detto
  chiaro. L'importazione unisce per `id` e tiene la versione con `agg` piu'
  recente, quindi reimportare lo stesso file due volte non crea doppioni.
- **`id` non finisce nel link del cliente** (`PREVENTIVO.compatta` lo salta):
  serve solo all'archivio, al cliente non dice nulla.
- La finestra e' un `<dialog>`: **nessun `display` su `.arc`** (vedi la
  trappola piu' sotto), l'impaginazione a colonna sta su `.arc__box`. E
  `showModal()` va chiamato solo se non e' gia' aperto, altrimenti e' un errore.

**Da ripetergli:** se svuota i dati del browser o cambia computer, l'archivio
sparisce. Il backup e' **Esporta**. Non promettergli una sincronia che un sito
statico non puo' dare: se un domani vuole l'archivio condiviso fra dispositivi
serve un servizio esterno (Cloudflare Pages + KV, o simili), che e' un cambio di
categoria, non un'aggiunta.

## Skill installate su questa macchina
Le skill che lui installa nell'app Claude **non si vedono da Claude Code**:
stanno sul suo account, non sul disco. Claude Code le legge da
`~/.claude/skills/`, e ci si mettono a mano (il comando `/plugin` qui non
c'e'). Installate ad ago 2026, dopo aver letto cosa contenevano:

- **impeccable** (v3.5.0) — design di interfacce. E' quella con cui e' stato
  costruito il gestionale: conosce gia' le scelte di questo progetto.
- **ui-ux-pro-max** — stesso mestiere di impeccable, ma con dati consultabili
  (palette, abbinamenti di font, linee guida UX) e script Python locali.
  Utile per **cercare un dato**, non per rifare le scelte gia' prese.
- **stop-slop** — toglie i tic di scrittura AI dai testi. Da usare sui testi
  inglesi del sito e sulle mail ai clienti.

Sovrapposizione: impeccable e ui-ux-pro-max fanno la stessa cosa. Per questo
progetto **comanda impeccable**, che ha in testa le decisioni gia' prese
(grafite e ambra, griglie uniformi, niente desaturazione); ui-ux-pro-max si
interroga quando serve un riferimento concreto.

Non installata: `Agent-Skills-for-Context-Engineering`, 17 skill su come si
costruiscono i sistemi ad agenti. Non c'entra col sito e riempirebbe l'elenco.

## Trappole già incontrate (non ripeterle)
- **L'archivio dei preventivi e' legato all'indirizzo del sito.** `localhost:8010`
  e `mattiabaruffaldi.com` sono due origini diverse per il browser, quindi due
  `localStorage` separati che non si vedono fra loro. Un preventivo creato in
  locale NON compare online e viceversa: si passa da **Esporta / Importa**.
  Successo ad ago 2026: gli avevo creato tre preventivi su localhost e lui li
  cercava sul sito pubblicato. Prima di dire "e' fatto", guardare su quale
  indirizzo sta lavorando lui.
- **`/studio/` e `/quote/` non le genera `build.py`**, quindi non prendevano la
  firma anti-cache e il browser serviva `quote.css`/`quote.js` vecchi: le
  modifiche sembravano non arrivate. Ora `timbra_a_mano()` in `build.py`
  aggiorna solo il `?v=` di quei due indirizzi senza riscrivere le pagine.
  **Lanciare `python3 tools/build.py` anche quando si toccano solo quei file.**
- **Il tuo strumento Write puo' scrivere byte NUL** al posto di uno spazio
  dentro una stringa (successo ad ago 2026 in `studio/index.html`: `' '`
  diventato `"\0"`). I sintomi: `grep` smette di rispondere sul file perche' lo
  considera binario, `Edit` non trova righe che invece esistono, e il confronto
  in JS fallisce senza errore. Si trova con
  `perl -ne 'print "$.\n" if /\0/' <file>` e si aggiusta con `perl -i`.
- **Non provare l'archivio sul suo browser vero senza mettere via i suoi dati.**
  Il salvataggio automatico scatta anche su `beforeunload`, quindi rimettere a
  posto `localStorage` e poi ricaricare **non serve a niente**: alla chiusura la
  pagina riscrive tutto dai dati che ha in memoria. Per ripulire davvero si
  passa **dai campi dell'interfaccia** (svuotare il Titolo basta a fermare
  l'archiviazione), non da `localStorage`. Successo ad agosto 2026: la bozza che
  aveva aperta e' stata sovrascritta con dati di prova.
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
- [x] "The Hyper Contrast Capsule" e' **Unreal × Odlo** (confermato da lui).
- [x] **RAM non passa da Unreal**: il credito e' solo "RAM". Tutti gli altri
      film con brand sono Unreal, confermato.
- [x] "RGB Films" e' scritto giusto.
- [ ] Valutare una pagina privacy: l'hero carica YouTube (in modalità
      nocookie) in automatico su desktop.
- [ ] Le foto vengono dal CDN di Squarespace, quindi già compresse da loro. Se
      vuole, si rifanno dagli originali in `~/Desktop/FOTO`.

## Note di stile comunicazione
Rispondere in **italiano**, tono pratico e chiaro. Procedere una modifica alla
volta e far verificare su localhost prima di pubblicare.
