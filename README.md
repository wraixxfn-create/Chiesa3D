# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (3.194 oggetti, 19 materiali PBR con texture incorporate) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 900×1050) |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprima e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia di riferimento |

## Dimensioni

**~90 m di larghezza × ~104 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~34,5 m).

## Versione 1.5 — tre miglioramenti di fedeltà all'originale

Confronto con la fotografia `riferimento_facciata.jpg`, limitato a **tre interventi**:

1. **Portali scolpiti** — archivolti avanzati rispetto al fondo triangolare per evitare che la ghimberga li nasconda, due fasce di rosette a cinque petali per portale, tralci a bassorilievo e listello interno sugli spioventi. Conservati porte, dimensioni e medaglioni.
2. **Torrioni gotici laterali** — vani e modanature delle sei finestre portati davanti alla muratura, marcapiani e cornicioni meno spessi e aggettanti; coronamenti a doppia ghimberga con foglie rampanti, colonnine e piccoli pinnacoli. Conservata l'asimmetria dei due torrioni.
3. **Cornice scolpita dell'oculo** — quattro anelli concentrici resi visibili davanti alla lastra, perlinatura interna e ovuli esterni; pennacchi in marmo chiaro con rosette e rilievi degli Evangelisti più sporgenti. Conservati diametro, vetrata e corona quadrata di nicchie.

Nessuna modifica a camera, illuminazione, scala, mosaici, gradinata o impostazioni di render/export. Modello `.blend` e anteprima rigenerati con Blender 4.2 / Cycles CPU; GLB generato ma escluso da Git secondo `.gitignore`.

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
