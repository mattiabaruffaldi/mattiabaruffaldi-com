#!/usr/bin/env python3
"""
Genera le pagine statiche di mattiabaruffaldi.com.

I contenuti (video, foto, testi) stanno tutti qui sotto in CONTENUTI.
Per aggiornare il sito: modifica i dati, poi `python3 tools/build.py`.
L'output e' HTML statico puro: funziona anche senza JavaScript.
"""

import hashlib
import html

import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.mattiabaruffaldi.com"
ANNO = date.today().year

# ============================================================================
# CONTENUTI
# ============================================================================

CONTATTI = {
    "email": "info@mattiabaruffaldi.com",
    "tel": "+393464755599",
    "tel_display": "(+39) 346 475 5599",
    "instagram": "https://www.instagram.com/mattiabaruffaldi/",
    "linkedin": "https://www.linkedin.com/in/mattia-baruffaldi-a734831a5/",
    "youtube": "https://www.youtube.com/@mattiabaruffaldi_film",
}

# id YouTube, titolo mostrato, credito (produzione × cliente; vuoto = non dichiarato).
# Unreal Media House e' la casa di produzione con cui lavora da sempre.
FILM = {
    "reel": [
        ("9daFPeNSXGo", "Showreel", ""),
    ],
    "automotive": [
        ("GVQPl1QtQQ4", "Esperienza Giro USA", "Unreal × Lamborghini"),
        ("oxBlVDnw5Lo", "From the Alps to the Sea", "Unreal × Lamborghini"),
        ("8vc4HPQ3ycY", "Multistrada V4 Pikes Peak", "Unreal × Ducati"),
        ("T-nkJv4oWhI", "Multistrada V4 · Expand Your Limits", "Unreal × Ducati"),
        ("QROt4ap1GjY", "Hypermotard V2 · Never So Hyper", "Unreal × Ducati"),
        ("YKYowJ4TOcA", "Streetfighter V4", "Unreal × Ducati"),
        ("I-xkV-nLD5g", "Multistrada V2", "Unreal × Ducati"),
        ("YHMMSysS0Yo", "#BACK2BACKgnaia", "Unreal × Ducati Corse"),
        ("-3H7_iYdI9I", "The Red from Borgo Panigale Enters Motocross", "Unreal × Ducati"),
        ("KORLNLzHhwU", "Motocross · Coming 2024", "Unreal × Ducati"),
        ("ng4vK723AS8", "1500 TRX Lunar Edition", "Unreal × RAM"),
    ],
    "apparel": [
        ("CF3su928_Bc", "Kappa × Ducati", "Unreal × Kappa"),
        ("p5ZqRwjilKg", "Winter Collection", "Unreal × Kappa"),
        ("qqoSzrGkyf8", "US Ski Team", "Unreal × Kappa"),
        ("BFilRFo1Yiw", "The Hyper Contrast Capsule", ""),
        ("BPCioSdPk-U", "Powerstage RR Limited Edition", "Unreal × Ducati"),
        ("tDmiGfRRpRU", "Lords of Tram", "Lorenzo Casati"),
        ("puQ4XR38yc8", "The Fastest Urban Downhill", ""),
        ("6BfEIhr-aY4", "Mountain Calls · Jonny", ""),
    ],
}

GRUPPI_FILM = [
    ("automotive", "Automotive and motorsport"),
    ("apparel", "Sport and apparel"),
]

LIFETALKS = [
    ("UggHyqDGgGQ", "Grazia Robustellini", "Episode 1",
     "My grandmother. Grazia is a sprightly 88-year-old from Tirano, in the "
     "Valtellina valley. I hope her stories land with you the way they landed "
     "with me."),
    ("KnBHJpXhq3Q", "Michelangelo &ldquo;Puki&rdquo; Pochettino", "Episode 2",
     "Puki is one of the significant figures of the vintage motorcycle world in "
     "Italy. Former motocross racer, distributor for Montesa and importer of CZ, "
     "he keeps one of the most varied collections in the country."),
]

# Testi alternativi scritti guardando ogni foto: servono a chi usa
# uno screen reader e a Google.
ALT = {
    "automotive": [
        "A rider in leathers holding a helmet beside his bike at the track",
        "A MotoGP rider in red leathers crouched low over the bike on the tarmac",
        "A race bike blurred to a streak along a circuit straight",
        "A lone motorcycle on the pit straight below the empty grandstands",
        "A Ducati MotoGP bike leaning through a corner over heat-hazed asphalt",
        "A MotoGP Ducati at full lean past the trackside boards",
        "A race bike panned past the grandstands at speed",
        "A circuit seen wide, pit lane and paddock below",
        "A MotoGP rider tipping into the red and white kerbs",
        "A Lamborghini running a mountain road at dusk",
        "A BMW M4 GT race car emerging from smoke in a dark studio",
        "A car bursting through a wall of orange sand",
        "Empty desert ridges under a pale sky",
        "A vintage pickup parked on a dune crest in the desert",
        "Two figures silhouetted on a ridge in fog",
        "The rear haunch of a black Lamborghini on the move",
        "A blue Lamborghini on a forest mountain road with a second car behind",
        "An orange sports car panned along a tree-lined road",
        "A motorcycle silhouetted against a bright horizon",
        "A naked motorcycle parked against a coastal sunset",
        "A car under a white cover in a bright studio",
        "The rear deck of a Ferrari under pastel light",
        "A motocross rider deep in a dirt rut, sun flaring behind",
        "A motocross rider throwing a roost of dirt, black and white",
        "A motorcycle silhouetted on a hill crest against the low sun",
        "A blue Ferrari Spider on a coast road above the sea",
        "A white Abarth 695 cornering on a circuit",
        "A Jeep Grand Cherokee parked in snow below dolomite peaks",
        "A Jeep Renegade on a road through autumn woods",
        "A Jeep Grand Cherokee crossing a snow-covered pass",
    ],
    "action-sports": [
        "Paragliders over a wooded valley",
        "A kite high against an overcast sky",
        "A snowboarder inverted mid-air against the clouds",
        "A downhill skier panned against blue safety netting",
        "A goggle and helmet resting in low light",
        "A mountain biker dropping into a dark forest trail",
        "A mountain biker on a fire road through alpine woods",
        "A rider in a full-face helmet backlit in the trees",
        "Water beading on a cycling shoe, close up",
        "A downhill rider mid-jump against a dark treeline",
        "A mountain biker rolling a berm in the woods",
        "A bike wheel and the rider's foot on loose rock",
        "A rider carving a dusty hillside trail",
        "A mountain biker hopping across a rocky alpine slope",
        "A downhill racer at speed, the background stretched by the pan",
        "A mud-covered rider cornering hard",
        "A cyclist riding through the arches of a mountain gallery",
        "A rider's shoulder with the trees blurred behind",
        "A road cyclist climbing through a snow gallery",
        "A pass road seen through a helmet vent",
        "A road bike's shadow cast across white road markings",
        "A cyclist riding out of a lit tunnel",
        "A cyclist on a pass road cut into the rock face",
        "Two riders on a sunlit forest road, panned",
        "A cyclist pushing into a whiteout",
        "A snowboarder small against a dark slope",
        "A skater on the poolside coping at sunset",
        "A concrete skate bowl at dusk with palms behind",
        "A skater dropping into the bowl",
        "A skater riding out of a trick with both arms up",
        "A snowboarder throwing powder toward the camera",
        "A kitesurfer suspended under the kite against deep blue sky",
        "A kite and rider far off against a pale sky",
        "A snowboarder cutting a line down a wind-rippled face",
        "A snowboarder on a summit ridge with the sun flaring",
        "A rider in a hoodie blurred through the pines",
        "Mountain bikers descending a trail in a spruce forest",
        "Looking up at the treetops from under a jump",
    ],
    "people": [
        "A kitesurfer holding up a competition trophy on the beach",
        "A kiter walking the shoreline past rigged kites",
        "A woman in sunglasses, blurred by the pan",
        "A rider on a BMW motorcycle dragged by a slow shutter",
        "A racer in red leathers standing over the bike on a wet track",
        "A rider holding his helmet, sea and sky behind",
        "A figure at a concrete lookout fence",
        "A racer in red leathers on the number 93 bike, seen from behind",
        "A wetsuited figure standing on a flat, empty beach",
        "A kitesurfer laughing in a helmet on the beach",
        "A kiter standing in front of a painted mural wall",
        "Bare feet on a table in front of a Harlem scoreboard",
        "A close, half-lit profile of a face",
        "A woman in a water helmet looking into the lens",
        "Two mirrored portraits of a young man with headphones",
        "A young man leaning against a white wall, arms crossed",
        "A studio portrait of a young man wearing over-ear headphones",
        "A young man against a dark ridged wall",
        "A hand raised against a bright white ground",
        "A cyclist in a white helmet and shield glasses",
    ],
}

SET_FOTO = [
    ("automotive", "Automotive"),
    ("action-sports", "Action sports"),
    ("people", "People"),
]

# Anteprima foto in home: tre scatti fermi, uno per insieme, poi il link alla
# pagina completa. Niente striscia che scorre di lato.
ANTEPRIMA_FOTO = [
    ("automotive", 12), ("action-sports", 3), ("people", 1),
    ("automotive", 23), ("action-sports", 32), ("people", 17),
    ("automotive", 16), ("action-sports", 35), ("people", 14),
]

# Selezione film in home. Scelti fra quelli la cui anteprima YouTube e' un
# fotogramma pulito: diverse altre hanno titoli e loghi stampati sopra, che a
# grande dimensione fanno sembrare la pagina una griglia di YouTube.
HOME_FILM = [
    "oxBlVDnw5Lo",   # From the Alps to the Sea
    "CF3su928_Bc",   # Kappa × Ducati
    "8vc4HPQ3ycY",   # Multistrada V4 Pikes Peak
    "-3H7_iYdI9I",   # The Red from Borgo Panigale Enters Motocross
]

# L'anteprima YouTube dello showreel e' una schiacciata nera col solo titolo.
# Al suo posto una sua fotografia, dichiarata come locandina nel testo alternativo.
POSTER = {
    "9daFPeNSXGo": ("/img/hero.jpg", 2500, 1667,
                    "Showreel poster: a Lamborghini on a mountain road at dusk"),
}

# La griglia foto e' uniforme (3 per riga da CSS): nessun mosaico. Le misure
# diverse creavano buchi e i riquadri grandi mostravano la grana degli scatti.


# ============================================================================
# COSTRUZIONE
# ============================================================================

TUTTI_FILM = {v[0]: v for gruppo in FILM.values() for v in gruppo}
for _ep in LIFETALKS:                       # gli episodi usano le stesse miniature
    TUTTI_FILM[_ep[0]] = (_ep[0], _ep[1], _ep[2])
N_FILM = sum(len(g) for g in FILM.values())
N_FOTO = sum(len(ALT[k]) for k, _ in SET_FOTO)

RE_ENTITA = re.compile(r"&(?![a-zA-Z]+;|#\d+;)")


def firma(percorso):
    """Firma breve del contenuto del file, da appendere all'indirizzo.

    Serve a far arrivare subito le modifiche: senza, browser e GitHub Pages
    tengono in cache la versione vecchia di CSS e JS e le correzioni sembrano
    non essere state fatte.
    """
    intero = os.path.join(ROOT, percorso.lstrip("/"))
    try:
        with open(intero, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:8]
    except OSError:
        return "0"


def e(s):
    """Escape per il testo, lasciando passare le entita' scritte a mano."""
    return RE_ENTITA.sub("&amp;", s).replace("<", "&lt;").replace(">", "&gt;")


def attr(s):
    """Escape per un attributo: le entita' non servono, il testo va in chiaro."""
    pulito = re.sub(r"&[a-zA-Z]+;", "'", s)
    return html.escape(pulito, quote=True)


def shell(*, slug, title, desc, body, og_image="/og.png", extra_head=""):
    """Guscio comune: head, testata, corpo, piede, finestre modali."""
    url = SITE + ("/" if slug == "" else "/%s/" % slug)
    nav = [("film", "Film"), ("photo", "Photo"), ("lifetalks", "LifeTalks"), ("info", "Info")]
    voci = "".join(
        '<li><a href="/%s/"%s>%s</a></li>' % (
            s, ' aria-current="page"' if s == slug else "", n)
        for s, n in nav)

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
<meta name="theme-color" content="#121214">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Mattia Baruffaldi">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(site)s%(og)s?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/site.css?v=%(vcss)s">
%(extra)s</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <a class="brand" href="/" aria-label="Mattia Baruffaldi, home">
    <img src="/img/wordmark.png" alt="Mattia Baruffaldi" width="640" height="30">
  </a>
  <nav class="site-nav" aria-label="Sections">
    <ul>%(voci)s</ul>
  </nav>
</header>

<main id="main">
%(body)s
</main>

<footer class="site-foot">
  <div class="wrap site-foot__top">
    <div>
      <h2>Let&rsquo;s talk.</h2>
      <a class="site-foot__mail" href="mailto:%(email)s">%(email)s</a>
      <a class="site-foot__tel" href="tel:%(tel)s">%(tel_d)s</a>
    </div>
    <div>
      <p class="meta" style="margin-bottom:var(--s-4)">Milan, Italy</p>
      <ul class="site-foot__links">
        <li><a class="link" href="%(ig)s" rel="me noopener" target="_blank">Instagram</a></li>
        <li><a class="link" href="%(yt)s" rel="me noopener" target="_blank">YouTube</a></li>
        <li><a class="link" href="%(li)s" rel="me noopener" target="_blank">LinkedIn</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap site-foot__bar">
    <p class="meta">&copy; %(anno)s Mattia Baruffaldi</p>
    <p class="meta">Film and photography</p>
  </div>
</footer>

<script src="/js/site.js?v=%(vjs)s" defer></script>
</body>
</html>
""" % {
        "title": title, "desc": desc, "url": url, "site": SITE, "og": og_image,
        "extra": extra_head, "voci": voci, "body": body, "anno": ANNO,
        "vcss": firma("css/site.css"), "vjs": firma("js/site.js"),
        "email": CONTATTI["email"], "tel": CONTATTI["tel"],
        "tel_d": CONTATTI["tel_display"], "ig": CONTATTI["instagram"],
        "yt": CONTATTI["youtube"], "li": CONTATTI["linkedin"],
    }


DIALOG_PLAYER = """
<dialog class="player" id="player" aria-label="Video player">
  <div class="player__inner">
    <div class="player__frame"></div>
    <div class="player__bar">
      <p class="player__title"></p>
      <button class="player__close" type="button">Close &times;</button>
    </div>
  </div>
</dialog>
"""

DIALOG_VIEWER = """
<dialog class="viewer" id="viewer" aria-label="Photograph">
  <div class="viewer__stage"><img alt=""></div>
  <div class="viewer__bar">
    <p class="meta viewer__count"></p>
    <div class="viewer__nav">
      <button class="viewer__btn" type="button" data-dir="prev" aria-label="Previous photograph">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
      </button>
      <button class="viewer__btn" type="button" data-dir="next" aria-label="Next photograph">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
      </button>
    </div>
    <button class="viewer__close meta" type="button" style="color:var(--paper)">Close &times;</button>
  </div>
</dialog>
"""


def film_item(vid, span_class="", stagger=0, level=3, eager=False, caption=True,
              cliente_visibile=True):
    """Una miniatura video: bottone che apre il lettore, link a YouTube senza JS.

    caption=False dove il titolo e' gia' scritto accanto (pagina LifeTalks):
    ripeterlo sotto la miniatura lo mostrerebbe due volte.
    """
    _, titolo, cliente = TUTTI_FILM[vid]
    riga = ('<p class="meta film__client">%s</p>' % e(cliente)) \
        if (cliente and cliente_visibile) else ""
    classi = " ".join(x for x in ["film", span_class, "reveal"] if x)
    poster, pw, ph, palt = POSTER.get(
        vid, ("/img/video/%s.jpg" % vid, 1280, 720, "Still from %s" % attr(titolo)))
    blocco_did = "" if not caption else """
    <figcaption class="film__caption">
      <h%(lv)d class="film__title">%(t)s</h%(lv)d>
      %(cl)s
    </figcaption>""" % {"lv": level, "t": e(titolo), "cl": riga}
    return """<figure class="%(cls)s" data-stagger="%(st)d">
  <a class="film__btn" href="https://www.youtube.com/watch?v=%(id)s" data-video="%(id)s"
     data-title="%(t_attr)s" target="_blank" rel="noopener">
    <span class="film__frame">
      <img src="%(poster)s" alt="%(palt)s" width="%(pw)d" height="%(ph)d"
           %(load)s decoding="async">
      <span class="film__cue" aria-hidden="true"></span>
    </span>%(did)s
  </a>
</figure>""" % {"cls": classi, "st": stagger, "id": vid,
                "t_attr": attr(titolo), "did": blocco_did,
                "poster": poster, "pw": pw, "ph": ph, "palt": palt,
                "load": 'fetchpriority="high"' if eager else 'loading="lazy"'}


def griglia_foto(chiave):
    """Griglia uniforme: tutte le foto della stessa misura, 3 per riga."""
    alts = ALT[chiave]
    nome_set = next(t for k, t in SET_FOTO if k == chiave)
    fuori = []
    for i, testo in enumerate(alts):
        n = i + 1
        # E' un <a> verso il file grande, non un <button>: senza JavaScript
        # la foto si apre comunque a piena risoluzione.
        fuori.append("""<figure class="shot reveal" data-stagger="%(st)d">
  <a href="/img/photo/%(k)s/%(k)s-%(nn)02d.jpg" data-full="/img/photo/%(k)s/%(k)s-%(nn)02d.jpg"
     data-alt="%(alt_a)s" data-set="%(setn)s" data-idx="%(nn)d" data-count="%(tot)d"
     aria-label="Open: %(alt_a)s">
    <img src="/img/photo/%(k)s/thumb/%(k)s-%(nn)02d.jpg" alt="%(alt)s"
         width="800" height="533" loading="lazy" decoding="async">
  </a>
</figure>""" % {"st": i % 3, "k": chiave, "nn": n,
                "alt": e(testo), "alt_a": attr(testo), "tot": len(alts),
                "setn": nome_set})
    return "\n".join(fuori)


# ---------------------------------------------------------------- home
def pagina_home():
    reel = FILM["reel"][0][0]

    selezione = "\n".join(
        film_item(vid, "", i, cliente_visibile=False)
        for i, vid in enumerate(HOME_FILM))

    anteprima = "\n".join(
        """<figure class="peek reveal" data-stagger="%(i)d">
  <a href="/photo/#%(k)s">
    <img src="/img/photo/%(k)s/thumb/%(k)s-%(nn)02d.jpg" alt="%(alt)s"
         width="800" height="533" loading="lazy" decoding="async">
  </a>
</figure>""" % {"i": i, "k": k, "nn": n, "alt": e(ALT[k][n - 1])}
        for i, (k, n) in enumerate(ANTEPRIMA_FOTO))

    body = """
<section class="hero">
  <!-- Video ospitato qui, non YouTube: parte all'istante, senza comandi
       sopra e senza una fotografia d'attesa. La locandina è il primo
       fotogramma del video stesso, così non si vede alcun cambio. -->
  <div class="hero__media">
    <video class="hero__video" poster="/img/showreel-poster.jpg"
           muted loop playsinline autoplay preload="auto"
           aria-hidden="true" tabindex="-1" width="1920" height="1080">
      <source src="/img/showreel-loop.mp4" type="video/mp4">
    </video>
  </div>
  <div class="hero__inner">
    <!-- Il titolo resta per Google e per chi usa uno screen reader, ma non si
         vede: sull'hero deve esserci solo il video. -->
    <h1 class="visually-hidden">Mattia Baruffaldi, film and photography</h1>
    <div class="hero__actions">
      <a class="link link--big" href="/film/">Portfolio</a>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="sec-head reveal">
    <h2 class="display">Selected film</h2>
  </div>
  <div class="films">
%(selezione)s
  </div>
  <p class="sec-more reveal"><a class="link" href="/film/">All %(nfilm)d films</a></p>
</section>

<section class="section wrap">
  <div class="sec-head reveal">
    <h2 class="display">Photography</h2>
  </div>
  <div class="peeks">
%(anteprima)s
  </div>
  <p class="sec-more reveal"><a class="link" href="/photo/">All %(nfoto)d photographs</a></p>
</section>

<div class="wrap"><hr class="rule"></div>

<section class="section wrap">
  <div class="slab reveal">
    <div class="slab__media">
      <img src="/img/video/UggHyqDGgGQ.jpg" alt="Grazia Robustellini at home in Tirano, from LifeTalks episode one"
           width="1280" height="720" loading="lazy" decoding="async">
    </div>
    <div class="slab__body">
      <h2 class="display">LifeTalks</h2>
      <p>A project of my own: the lives of ordinary people with an uncommon story.
         Two episodes so far, my grandmother Grazia and Puki, who keeps one of the
         best vintage motorcycle collections in Italy.</p>
      <a class="link" href="/lifetalks/">Watch the episodes</a>
    </div>
  </div>
</section>
%(dialog)s
""" % {"reel": reel, "selezione": selezione, "anteprima": anteprima,
       "nfilm": N_FILM, "nfoto": N_FOTO, "dialog": DIALOG_PLAYER}

    return shell(
        slug="", title="Mattia Baruffaldi — Film and photography",
        desc="Filmmaker and photographer based in Milan, from the Italian Alps. "
             "Commercials, brand films and stills for Lamborghini, Ducati, Kappa and others.",
        body=body)


# ---------------------------------------------------------------- film
def pagina_film():
    salti = " ".join(
        '<a class="link" href="#%s">%s</a>' % (k, t) for k, t in GRUPPI_FILM)

    sezioni = [
        """<section class="section--tight wrap">
  <div class="films">%s</div>
</section>""" % film_item(FILM["reel"][0][0], "", 0, level=2, eager=True)
    ]

    for chiave, titolo in GRUPPI_FILM:
        elementi = "\n".join(
            film_item(v[0], "", i) for i, v in enumerate(FILM[chiave]))
        sezioni.append("""<section class="section wrap" id="%(k)s">
  <div class="sec-head reveal">
    <h2 class="display">%(t)s</h2>
  </div>
  <div class="films">
%(el)s
  </div>
</section>""" % {"k": chiave, "t": e(titolo), "el": elementi})

    body = """
<div class="wrap page-head">
  <h1>Film</h1>
  <p>Commercials, launch films and documentary work, made freelance with
     production companies. Click any frame to watch it here.</p>
</div>
<div class="wrap"><nav class="jump" aria-label="Jump to a group">%(salti)s</nav></div>
%(sez)s
%(dialog)s
""" % {"salti": salti, "sez": "\n".join(sezioni), "dialog": DIALOG_PLAYER}

    return shell(slug="film", title="Film — Mattia Baruffaldi",
                 desc="Commercials, launch films and documentary work for Lamborghini, "
                      "Ducati, Kappa, RAM and others.",
                 body=body, og_image="/og.png")


# ---------------------------------------------------------------- photo
def pagina_photo():
    salti = " ".join(
        '<a class="link" href="#%s">%s</a>' % (k, t) for k, t in SET_FOTO)

    sezioni = []
    for chiave, titolo in SET_FOTO:
        sezioni.append("""<section class="section wrap" id="%(k)s">
  <div class="sec-head reveal">
    <h2 class="display">%(t)s</h2>
  </div>
  <div class="sheet">
%(g)s
  </div>
</section>""" % {"k": chiave, "t": e(titolo), "g": griglia_foto(chiave)})

    body = """
<div class="wrap page-head">
  <h1>Photography</h1>
</div>
<div class="wrap"><nav class="jump" aria-label="Jump to a set">%(salti)s</nav></div>
%(sez)s
%(dialog)s
""" % {"salti": salti, "sez": "\n".join(sezioni), "dialog": DIALOG_VIEWER}

    return shell(slug="photo", title="Photography — Mattia Baruffaldi",
                 desc="Automotive, action sports and portrait photography by "
                      "Mattia Baruffaldi.",
                 body=body)


# ---------------------------------------------------------------- lifetalks
def pagina_lifetalks():
    ep = []
    for i, (vid, nome, numero, testo) in enumerate(LIFETALKS):
        ep.append("""<article class="episode">
  <div>%(media)s</div>
  <div class="episode__body reveal">
    <span class="episode__no">%(no)s</span>
    <h3>%(nome)s</h3>
    <p>%(testo)s</p>
  </div>
</article>""" % {"media": film_item(vid, "", i, eager=(i == 0), caption=False),
                 "no": e(numero), "nome": e(nome), "testo": e(testo)})

    body = """
<div class="wrap page-head">
  <h1>LifeTalks</h1>
  <p>A project of my own, outside of client work: telling the lives of ordinary
     people who turn out to have an uncommon story. Shot when I have the time,
     which is why there are two.</p>
</div>
<div class="wrap section--tight">
%(ep)s
</div>
%(dialog)s
""" % {"ep": "\n".join(ep), "dialog": DIALOG_PLAYER}

    return shell(slug="lifetalks", title="LifeTalks — Mattia Baruffaldi",
                 desc="A personal documentary project: the lives of ordinary people "
                      "with an uncommon story.",
                 body=body, og_image="/og.png")


# ---------------------------------------------------------------- info
def pagina_info():
    body = """
<div class="wrap page-head">
  <h1>Info</h1>
</div>
<div class="wrap section--tight">
  <div class="info">
    <div class="info__bio">
      <p>I shoot film and stills for brands, mostly things that move fast.</p>
      <p>Born and raised in the Alps, in the province of Sondrio, and now based in
         Milan. I graduated in Public Relations and Business Communication at IULM.</p>
      <p>I started out as a photography assistant to Alberto Alquati, and came to
         moving images through Fabrizio Accettulli of RGB Films.</p>
      <p>I have worked with Unreal Media House since the beginning, and it is
         still where most of my work comes through: projects for Lamborghini,
         Ducati, Moncler and Kappa, among others.</p>
      <p>Between commissions I shoot LifeTalks, and I ride, ski and kite as much as
         the calendar allows, which is usually where the personal work comes from.</p>
    </div>
    <figure class="info__portrait reveal">
      <img src="/img/portrait.jpg" width="1800" height="1161" loading="lazy" decoding="async"
           alt="Mattia Baruffaldi holding a cinema camera, the rooftops of Genoa behind him">
    </figure>
  </div>

</div>
""" % {"email": CONTATTI["email"], "tel": CONTATTI["tel"],
       "tel_d": CONTATTI["tel_display"], "ig": CONTATTI["instagram"],
       "yt": CONTATTI["youtube"], "li": CONTATTI["linkedin"],
       "alt": e(ALT["people"][8])}

    return shell(slug="info", title="Info — Mattia Baruffaldi",
                 desc="Filmmaker and photographer from the Italian Alps, based in "
                      "Milan. Contact, bio and links.",
                 body=body)


# ---------------------------------------------------------------- 404
def pagina_404():
    body = """
<div class="wrap page-head" style="padding-block:var(--s-10)">
  <h1>Nothing here</h1>
  <p>That page moved when the site was rebuilt, or it never existed.</p>
  <p style="margin-top:var(--s-6);display:flex;flex-wrap:wrap;gap:var(--s-5)">
    <a class="link" href="/">Home</a>
    <a class="link" href="/film/">Film</a>
    <a class="link" href="/photo/">Photography</a>
    <a class="link" href="/info/">Info</a>
  </p>
</div>
"""
    return shell(slug="404", title="Page not found — Mattia Baruffaldi",
                 desc="Page not found.", body=body)


def redirect(dest):
    """Pagina ponte per i vecchi indirizzi di Squarespace."""
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved — Mattia Baruffaldi</title>
<link rel="canonical" href="%(site)s%(d)s">
<meta http-equiv="refresh" content="0; url=%(d)s">
<meta name="robots" content="noindex">
<style>body{background:#121214;color:#e8e8ea;font:16px/1.6 system-ui,sans-serif;padding:3rem}a{color:#f2b45c}</style>
</head>
<body><p>This page moved. <a href="%(d)s">Continue &rarr;</a></p></body>
</html>
""" % {"site": SITE, "d": dest}


def scrivi(percorso, testo):
    intero = os.path.join(ROOT, percorso)
    os.makedirs(os.path.dirname(intero), exist_ok=True)
    with open(intero, "w", encoding="utf-8") as f:
        f.write(testo)
    print("  %-42s %6.1f KB" % (percorso, len(testo.encode()) / 1024))


def main():
    print("Genero le pagine:")
    scrivi("index.html", pagina_home())
    scrivi("film/index.html", pagina_film())
    scrivi("photo/index.html", pagina_photo())
    scrivi("lifetalks/index.html", pagina_lifetalks())
    scrivi("info/index.html", pagina_info())
    scrivi("404.html", pagina_404())

    # Vecchi indirizzi Squarespace -> nuovi
    for vecchio, nuovo in [
        ("about", "/info/"),
        ("contatti", "/info/"),
        ("portfolio-video", "/film/"),
        ("photo/automotive", "/photo/#automotive"),
        ("photo/action-sports", "/photo/#action-sports"),
        ("photo/people", "/photo/#people"),
    ]:
        scrivi("%s/index.html" % vecchio, redirect(nuovo))

    pagine = ["/", "/film/", "/photo/", "/lifetalks/", "/info/"]
    oggi = date.today().isoformat()
    scrivi("sitemap.xml",
           '<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n'
                     % (SITE, p, oggi) for p in pagine)
           + "</urlset>\n")
    scrivi("robots.txt",
           "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    scrivi("CNAME", "www.mattiabaruffaldi.com\n")

    print("\n%d film, %d foto." % (N_FILM + len(LIFETALKS), N_FOTO))


if __name__ == "__main__":
    main()
