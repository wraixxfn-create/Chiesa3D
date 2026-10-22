# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (834 oggetti, 17 materiali) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima (Cycles CPU, 900×1050) |
| `genera_facciata.py` | Script procedurale che rigenera modello, anteprima e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia di riferimento |

## Dimensioni

**~96 m di larghezza × ~101 m di altezza all'angelo** (gradinata compresa: 108 m di larghezza), in unità metriche.
Rispetto alla versione precedente (~32 × ~34 m) il modello è stato **ingrandito di 3× in modo uniforme**: coordinate, quote, luci e camera sono scalate dal parametro `scala_globale` in `config_facciata.json` (valore `3.0`; mettendolo a `1.0` si riottengono le dimensioni originali).

## Cosa contiene il modello

- Gradinata del sagrato e basamento in pietra
- **Tre portali pisani** (Giovanni Pisano, 1284–1297): strombo a colonne ritorte con capitelli a fogliame, archivolti ritorti con chiave a testa di satiro, lunette e porte (bronzo al centro, legno ai lati)
- **Tre ghimberghe cuspidate** con foglie rampanti, medaglione con busto e statua di coronamento (Vergine al centro, Angeli ai lati)
- **Oculo centrale** (Camaino di Crescentino, 1299–1317) con vetrata, incorniciato dalla corona di **34 nicchie gotiche** con i mezzi busti degli antenati di Gesù e la Madonna col Bambino in quella sommitale
- Due ordini di loggette ad archetti nei settori laterali, galleria di nicchie con statue
- **Silhouette tricuspidale**: grande timpano centrale con mosaico dorato dell'Incoronazione e angelo apicale, due sottilissime guglie ai lati del timpano, due cuspidi laterali dorate con mosaici (Presentazione al Tempio / Natività) e due torrioni laterali tozzi con edicole cuspidate
- Fasce bicrome bianco/verde, pannelli a losanghe, gargolle sporgenti
- Materiali: marmo bianco, marmo rosa, verde serpentino, oro, bronzo, legno, vetro
- Camera frontale, sole e luce di riempimento già impostati come nella foto

Gli oggetti sono organizzati nelle collezioni `01_Struttura`, `02_Portali`, `03_Rosone_e_logge`, `04_Guglie_e_pinnacoli`, `05_Statue`, `06_Dettagli`.

È una ricostruzione stilizzata da singola foto (non un rilievo fotogrammetrico): proporzioni e partitura decorativa seguono la facciata reale, i dettagli minuti (statue, mosaici figurati) sono semplificati.

## Versione 1.2 — cosa è cambiato

Tre miglioramenti di fedeltà alla facciata reale, più l'ingrandimento 3×:

1. **Dal rosone gotico all'oculo di Camaino.** Il rosone a raggiera è stato sostituito dal grande oculo circolare realmente presente (con la vetrata cinquecentesca di Pastorino dei Pastorini), circondato dalla corona di 34 nicchie con gli antenati di Cristo e dalla Madonna col Bambino.
2. **Silhouette tricuspidale corretta.** Le guglie sottili sono state spostate a ridosso del timpano centrale, le cuspidi laterali dorate sono state alzate a coronare i due ordini di loggette e i torrioni laterali sono diventati tozzi, come nella fotografia: la differenza media dal profilo sommitale della foto passa da 4,5 m a 3,2 m.
3. **Portali di Giovanni Pisano.** Colonne ritorte, archivolti ritorti con chiavi a testa di satiro e ghimberghe cuspidate con foglie rampanti e statue.

## Rigenerare il modello

Con Blender installato:

```bash
blender --background --python genera_facciata.py
```

oppure con il modulo Python `bpy` (`pip install bpy==4.2.0`):

```bash
python genera_facciata.py
```

Lo script sovrascrive `Facciata_Duomo_Siena.blend`, `anteprima_facciata.png` e `Facciata_Duomo_Siena.glb`.
