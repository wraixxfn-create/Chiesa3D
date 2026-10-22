# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (1.561 oggetti, 18 materiali PBR con texture incorporate) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 900×1050) |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprima e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia di riferimento |

## Dimensioni

**~90 m di larghezza × ~104 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~34,5 m).

## Versione 1.3 — 3 miglioramenti di fedeltà all'originale

1. **Partizione gotica reale del registro superiore e dei torrioni angolari**
   - **Cornice quadrata gotica dell'oculo di Camaino**: sostituita la corona circolare sospesa sul muro vuoto con il vero grande tabernacolo quadrato fra i pilastri centrali, dotato di apertura strombata passante, **vetrata con griglia metallica 5×4**, pennacchi angolari con i **Quattro Evangelisti**, **36 edicole gotiche cuspidate** coi busti di Patriarchi e Profeti disposte sui quattro lati del quadrato e statua della **Madonna col Bambino** al centro inferiore.
   - **Inversione corretta fra settori laterali e torrioni angolari + pilastri centrali continui**: i pilastri centrali salgono ora continui fino alle guglie coronate da statue; le **loggette gotiche a 5 archetti acuti su colonnine binate** con le **cuspidi dorate** tornano all'interno in asse coi portali laterali, mentre i **torrioni gotici angolari a due campate** tornano all'esterno con finestre bicrome, tabernacoli statuari, doccioni sporgenti e **lanterna ottagonale a gradoni** più alta delle cuspidi laterali (errore RMS del profilo sommitale ridotto da **3,64 m** a **2,04 m**, −44%).

2. **Ordine inferiore di Giovanni Pisano a tre grandi portali contigui e specchiature bicrome**
   - Eliminato il cornicione passante a quota 8,1 m che tagliava a metà le lunette e sostituito con la vera **trabeazione scolpita d'imposta** sotto gli archi (`z = 8,35 m`).
   - **Tre grandi portali strombati contigui** con **5 ordini concentrici di archivolti bianchi e rosa** su fasci di colonne ritorte e scanalate che si toccano sui piloni comuni, **lunetta centrale a raggiera bicroma** col Sole raggiante di San Bernardino, **ghimberghe ripide** svettanti oltre il cornicione della galleria e **specchiature in marmo verde-nero di Prato con rosoni scolpiti** nei timpani triangolari.

3. **Mosaici figurati reali, policromia marmorea PBR e inquadratura/luce da Piazza del Duomo**
   - Sostituiti i dischi piatti blu/rossi con **texture ad alta risoluzione dei veri mosaici dorati** (*Incoronazione della Vergine*, *Presentazione al Tempio*, *Natività*), dei portoni in bronzo/noce e della vetrata, incorporate direttamente (`pack()`) nel `.blend` e nel `.glb`, abbinate a texture PBR venate per marmo avorio/rosa senese e serpentino verde-nero di Prato.
   - **Camera frontale simmetrica dal basso** su Piazza del Duomo (gradinata orizzontale) e **luce solare tardo-pomeridiana radente da destra** su cielo azzurro senese con denoising Cycles (errore quadratico medio RGB sull'intera immagine ridotto del **30%** e correlazione diretta con la foto aumentata da `0,04` a `0,42`).

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
