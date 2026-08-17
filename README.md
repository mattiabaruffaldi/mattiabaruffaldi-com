# mattiabaruffaldi.com

Sito personale di Mattia Baruffaldi, filmmaker e fotografo. HTML/CSS/JS statico,
nessun framework, nessuna dipendenza.

## Anteprima in locale

```bash
python3 -m http.server 8010
```

Poi apri http://localhost:8010

## Rigenerare le pagine

I contenuti (video, testi, descrizioni delle foto) stanno tutti in
`tools/build.py`. Le pagine `.html` sono **generate**: non modificarle a mano.

```bash
python3 tools/build.py
```

## Struttura

| Percorso | Cosa contiene |
|---|---|
| `tools/build.py` | Generatore e tutti i contenuti |
| `css/site.css` | Sistema visivo: token, componenti, movimento |
| `js/site.js` | Testata, rivelazioni, lettore video, visore foto |
| `fonts/` | Archivo variabile, ospitato qui (176 KB) |
| `img/photo/` | 88 fotografie a 1800px, più `thumb/` a 800px |
| `img/video/` | 22 anteprime dei video |

## Pubblicazione

GitHub Pages dal branch `main`. Il file `CNAME` punta a `www.mattiabaruffaldi.com`.
