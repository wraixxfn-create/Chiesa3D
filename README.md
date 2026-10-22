# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~2,6 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (555 oggetti, 18 materiali) |
| `anteprima_facciata.png` | Render frontale di anteprima (Cycles CPU) |
| `genera_facciata.py` | Script procedurale che rigenera modello e anteprima da zero |
| `riferimento_facciata.jpg` | Fotografia di riferimento |

## Cosa contiene il modello

- Gradinata del sagrato e basamento
- Tre portali con colonne, archivolti a conci bicromi bianco/verde, lunette (sole raggiante in quella centrale), porte laterali in legno e portale centrale in bronzo
- Tre ghimberghe (timpani triangolari) sopra i portali, con medaglioni
- Rosone centrale con anelli in marmo rosa/bianco, crociera, colonnine radiali e occhielli
- Loggette laterali ad archetti e galleria di nicchie con statue sopra il rosone
- Grande timpano centrale con mosaico dorato dell'Incoronazione e angelo apicale con ali
- Guglie centrali ed esterne con cuspidi, pinnacolini e finestre a lancetta
- Torri laterali con fasce bicrome bianco/verde e pannelli a losanghe in marmo rosa
- Statue stilizzate, gargolle sporgenti, materiali marmo bianco/rosa/verde serpentino, oro, bronzo, legno e vetro
- Camera frontale, sole e luce di riempimento già impostati come nella foto

Dimensioni: ~30 m di larghezza × ~34 m di altezza all'angelo (unità di misura: metri). Gli oggetti sono organizzati nelle collezioni `01_Struttura`, `02_Portali`, `03_Rosone_e_logge`, `04_Guglie_e_pinnacoli`, `05_Statue`, `06_Dettagli`.

È una ricostruzione stilizzata da singola foto (non un rilievo fotogrammetrico): proporzioni e partitura decorativa seguono la facciata reale, i dettagli minuti (statue, mosaici figurati) sono semplificati.

## Rigenerare il modello

Con Blender installato:

```bash
blender --background --python genera_facciata.py
```

oppure con il modulo Python `bpy` (`pip install bpy==4.2.0`):

```bash
python genera_facciata.py
```

Lo script sovrascrive `Facciata_Duomo_Siena.blend` e `anteprima_facciata.png`.
