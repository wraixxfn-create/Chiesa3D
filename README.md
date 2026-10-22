# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (~4.000 oggetti, 23 materiali PBR con texture incorporate) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 900×1050) |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprima e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia d'insieme di riferimento |
| `riferimento_apice.jpg` | Fotografia ravvicinata dell'apice (usata per cuspide, mosaico e angelo) |

## Dimensioni

**~90 m di larghezza × ~111 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~37 m).

## Versione 1.6 — apice centrale ricostruito sulla fotografia ravvicinata

Intervento limitato alla **punta centrale della facciata** (cuspide, mosaico
dell'Incoronazione e angelo apicale), con proporzioni misurate su
`riferimento_apice.jpg`:

| Elemento | Quota nel modello | Fonte |
|---|---|---|
| Cuspide | 10,30 m di base × 7,72 m di altezza | 4,91 × 3,68 m a scala 1:1 |
| Mosaico | 6,69 m di base × 5,01 m di altezza | base 0,59 m sopra la trabeazione |
| Fascia ornamentale | ~1,80 m per lato | misurata fra bordo e mosaico |
| Edicola + angelo | 0,42 m + 2,55 m | angelo 1,52 m in scala 1:1 |

Cosa è stato rifatto:

1. **Cornici degli spioventi** — dall'esterno verso l'interno: crockets a foglie
   d'acanto (modellate, non più coni), grosso filo arrotondato, nastrino, filo
   di perle su fondo in ombra, gola, fascia di fogliame a cubetti d'acanto,
   quadretti, toro e fregio di cherubini alati. Le modanature si fermano prima
   dell'apice per non incrociarsi sotto il cappuccio.
2. **Mosaico** — la texture dell'Incoronazione è ora ritagliata dalla foto
   ravvicinata a 1024 px (prima 512 px dalla foto d'insieme), con la stessa
   rettifica baricentrica sul triangolo. Il fregio di base ha cherubini
   policromi alternati a tralci, gola, astragalo e filo di perle.
3. **Apice** — raccordo con feritoie a quatrifoglio, grappe in ferro, cherubino
   di chiave e ciuffo di foglie d'acanto.
4. **Angelo apicale** — statua modellata con veste a pieghe, manto, braccio
   alzato con asta, basamento a foglie; ali a ventaglio di 12 penne lanceolate
   in rame ossidato (prima erano 2 coni per lato che leggevano come una stella).
   Nuovi materiali `Bronzo_Angelico` (dorato) e `Bronzo_Verde` (rame ossidato).

L'altezza totale passa da ~104 m a ~111 m (scala globale 3.0) perché la cuspide
centrale è stata riportata alle proporzioni reali. Camera, luci, portali,
oculo, logge, torrioni e gradinata sono invariati.

## Prova rapida del render

Lo script legge quattro variabili d'ambiente opzionali, utili per iterare senza
toccare `config_facciata.json`:

```bash
CHIESA_SAMPLES=16 CHIESA_RES_X=450 CHIESA_RES_Y=600 CHIESA_NO_GLB=1 python genera_facciata.py
CHIESA_NO_RENDER=1 python genera_facciata.py       # solo .blend, senza render
```

## Rigenerare il modello

Con Blender 4.2+:

```bash
blender --background --python genera_facciata.py
```

oppure con il modulo Python `bpy` (`pip install bpy==4.2.0`):

```bash
python genera_facciata.py
```

Lo script sovrascrive `Facciata_Duomo_Siena.blend`, `anteprima_facciata.png` e `Facciata_Duomo_Siena.glb`.
