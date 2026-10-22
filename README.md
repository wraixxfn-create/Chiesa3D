# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (1.732 oggetti, 19 materiali PBR con texture incorporate) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 900×1050) |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprima e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia di riferimento |

## Dimensioni

**~90 m di larghezza × ~104 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~34,5 m).

## Versione 1.4 — altri 3 miglioramenti di fedeltà all'originale (e solo 3)

1. **Oculo circolare e cornice senza “buchi neri”** — l'oculo era un'ellisse (3,02 × 2,55 m): ora è un cerchio vero (Ø 5,60 m) con griglia della vetrata 3×3 a barre sottili. Le 36 edicole della cornice quadrata non sono più vani neri piatti (`Vano_Scuro`) ma incassi poco profondi in ombra calda (nuovo materiale `Vano_Nicchia`), con busti più grandi che riempiono la nicchia come gli altorilievi reali.
2. **Policromia marmorea attenuata** — ai contrafforti angolari la zebratura a bande nere spesse è sostituita da 5 fasce sottili di serpentino molto distanziate; fondo e specchiature fra le ghimberghe passano da lastre nere a “domino” a marmo chiaro/rosato con rosone fogliato e piccolo intarsio verde centrale; il campo rosa delle ghimberghe è ridotto a una cornice sottile in marmo rosato chiaro.
3. **Apparato scultoreo Giovanni Pisano** — le statue non sono più “pedine” (cono + sfera in pietra chiara), ma figure panneggiate con pieghe verticali, spalle, maniche cadenti e testa proporzionata, in pietra calda consumata più scura del marmo di fondo; i doccioni sono draghi orizzontali con testa, muso e ala (non più pioli conici) e l'angelo apicale ha 2 ali per lato (non la “stella” a 4 penne per lato).

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
