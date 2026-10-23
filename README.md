# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2 pronto da aprire (2.748 oggetti mesh, 28 materiali PBR con texture incorporate) |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 64 campioni, 900×1050) |
| `anteprima_apice.png` | Render ravvicinato della cuspide centrale e dei pinnacoli (Cycles CPU, 64 campioni, 900×1022) |
| `anteprima_galleria.png` | Dettaglio panoramico della fascia richiesta: edicole, frontoni a chevron, profeti e sommità del rosone (Cycles CPU, 1200×400) |
| `confronto_galleria.png` | Confronto affiancato fotografia di riferimento / versione 2.1 / versione 2.2 della galleria dei Profeti |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprime e GLB da zero |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia d'insieme di riferimento |
| `riferimento_apice.jpg` | Fotografia ravvicinata ad alta risoluzione (2176×2472) usata per calibrare l'intera zona superiore centrale |

## Dimensioni

**~90 m di larghezza × ~111 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~37 m).

## Versione 2.2 — galleria dei Profeti ricostruita da zero

Intervento integralmente dedicato alla fascia **sopra lo specchio del rosone e
sotto il triangolo centrale** (`Nicchia_Sup_00` … `Nicchia_Sup_13`), rifatta
sulla fotografia di dettaglio fornita. Il resto della facciata resta invariato.

- **Nicchie incassate, non pannelli.** Ogni campata ha ora un vero vano a tutto
  sesto con catino, spallette strombate e fondale in **marmo rigato rosa**
  (nuova texture `Tex_Marmo_Rigato`): l'ombra nasce dalla geometria.
- **Arcata doppia.** Arco bianco esterno, arco in marmo rosa arretrato e
  perlinatura fitta sull'intradosso, con capitelli fogliati e colonnine binate
  scanalate; cornice d'imposta continua su tutta la galleria (prima gli archi
  «galleggiavano» sulla fascia rosa).
- **Frontone a chevron.** Gli spioventi sono molto meno inclinati e composti da
  quattro fasce modanate parallele (bianco → gola in ombra → filo bianco →
  filetto rosa → cornice bianca), tagliate a mitra sull'asse di ogni campata,
  con gattoni rampanti digradanti e fiorone. È il motivo a zig-zag continuo
  del coronamento senese, prima assente.
- **Tabernacoli fra i frontoni.** Sull'asse di ogni piedritto compare un
  tabernacolo gotico con statuina, ghimberga, gattoni e fiorone; i piedritti
  hanno parasta, montanti scanalati e pannello con quatrifoglio a rilievo.
- **Fascia cosmatesca azzurra** dietro frontoni e pinnacoli (nuova texture
  `Tex_Cosmatesco`), come nel fondo della fotografia.
- **14 profeti rifatti** come mezzi busti in altorilievo: panneggio scanalato
  che appoggia sul davanzale, braccia raccolte, libro/rotolo/tavola, volto con
  naso, sopraccigli, occhi, bocca, barba e nimbo ad anello; gesti, barbe e
  copricapi (capelli, berretta, cappuccio, mitra, corona) differenziati.
- Corretto il difetto della versione 2.1 per cui i busti restavano schiacciati
  in basso e i frontoni tagliavano i copricapi.

## Versione 2.1 — galleria dei Profeti, fregio e angeli del rosone

Intervento mirato alla fascia **sopra l'oculo e sotto il timpano centrale**,
ricostruita sul dettaglio fotografico fornito. Il resto della facciata resta
invariato.

- Le `14` campate superiori sono ora edicole gotiche individuali più leggibili:
  colonnine scanalate con capitelli fogliati, archi acuti strombati, doppie
  ghimberghe, gattoni rampanti e finiali scolpiti.
- I `14` profeti hanno silhouette e gesti differenziati (libro, cartiglio,
  tavola, mano alzata), con panneggio, barbe, copricapi e volti modellati in
  altorilievo; il fondo rosato e le nicchie ombreggiate danno profondità alla
  galleria.
- I due rilievi ai lati dell'arco sono stati rifatti come angeli alati
  speculari, con nimbo, piume separate, panneggio e braccio rivolto verso il
  rosone.
- La trabeazione sotto il mosaico aggiunge una sequenza scolpita di cherubini e
  gigli; il fregio alla base del mosaico passa da `6` a `10` testine, alternate
  a palmette.
- `anteprima_galleria.png` mostra il dettaglio aggiornato con un'inquadratura
  ravvicinata e panoramica.

## Versione 2.0 — ricostruzione integrale della zona centrale superiore

Rifacimento completo, calibrato millimetricamente sulla fotografia ad alta
risoluzione `riferimento_apice.jpg` (`2176×2472 px`), di tutta la parte
superiore centrale del Duomo di Siena — angelo apicale, cuspide musiva,
contrafforti centrali con tabernacoli gotici, trabeazione e galleria superiore
dei profeti — con rigenerazione integrale di `Facciata_Duomo_Siena.blend`,
`Facciata_Duomo_Siena.glb`, `anteprima_apice.png` e `anteprima_facciata.png`:

1. **Angelo apicale e capitello pensile (`statua_angelo_apicale`, `ala_angelo`)**:
   - Ali in bronzo/rame ossidato verderame (`Rame_Verde` + `Patina_Bronzo`) a
     10 larghe remiganti spatolate sovrapposte senza fessure interne, costolone
     carpale arcuato e tre ordini embricati di copritrici sbalzate.
   - Statua marmorea in contrapposto classico-gotico con braccio destro alzato
     che impugna la lancia bronzea, tunica e manto drappeggiati con sottosquadri
     patinati (`Patina_Scolpita`), cuscino a foglie d'acanto e grande capitello
     corinzio pensile coronato da abaco aggettante.
2. **Cuspide centrale e Mosaico dell'Incoronazione della Vergine (Sez. 6)**:
   - Triangoli esterni e interni ricalibrati a `61,05°` (`8,80 × 8,12 m`,
     incassati esattamente fra i due contrafforti centrali senza intersezioni).
   - Mosaico riestratto a `1536×1536 px` da `riferimento_apice.jpg` con restauro
     delle tessere auree perimetrali, shader metallico dorato e ghirlanda 3D ad
     altorilievo di cherubini alati, angeli d'angolo e gigli senesi lungo
     spioventi, base e lunetta apicale.
   - Gattoni rampanti a foglia d'acanto uncinata lungo gli spioventi e doppia
     fila di dentelli e mensole aggettanti illuminate dal sole sia lungo le
     cornici oblique sia lungo l'intera trabeazione orizzontale (`96` dentelli +
     `48` mensole).
3. **Contrafforti centrali e tabernacoli gotici (`pilastro_centrale_completo`)**:
   - Fusti a fascio in marmo bianco-crema e rosa di Siena con doppio ordine di
     ghimberghe acuminate, doccioni zoomorfi aggettanti e marcapiani patinati.
   - Eliminata la vecchia scatola nera `Luce_Guglia`: al suo posto veri
     tabernacoli gotici aperti su quattro lati con archetti trilobati, pinnacoli
     angolari, statua di santo scolpita all'interno, guglia a doppio ordine di
     gattoni, capitello fogliato e santo sommitale.
4. **Galleria superiore dei Patriarchi e Profeti (`edicola_gotica_busto`)**:
   - `14` edicole gotiche trilobate a tutta altezza fino alla trabeazione,
     arricchite da traforo gotico a lancette nei pennacchi e `14` busti scolpiti
     individuali (mitrie vescovili, cappucci, nimbi, cartigli e barbe).

## Versione 1.9 — angelo apicale e ali più fedeli alla fotografia

Intervento concentrato sulla statua al vertice: rispetto all'anteprima precedente,
la figura è più leggibile a distanza, con ali più ampie e slanciate verso l'alto,
una silhouette piumata più vicina all'angelo dell'originale. Le modifiche sono
nel generatore procedurale; per aggiornare il `.blend` e le anteprime occorre
rigenerare il progetto con Blender.

## Versione 1.8 — cuspide centrale rifinita sulla foto ravvicinata

L'intervento è concentrato sulla **parte alta al centro della facciata**. Il
resto del prospetto non cambia.

- Il mosaico dell'Incoronazione ora usa l'intero riquadro reale: sono stati
  corretti vertice e base del ritaglio, così la scena comprende anche gli angeli
  e il fregio inferiore invece di ingrandire soltanto le figure centrali.
- Il fregio alla base del mosaico è più fitto e segue meglio la sequenza di
  cherubini e palmette della fotografia.
- Due rilievi angelici completano la lunetta sopra il mosaico, attorno al
  cherubino di chiave.
- Il cappuccio acantiforme è stato alleggerito, con due ordini di foglie più
  leggibili; le penne delle ali dell'angelo sono ora modellate singolarmente,
  con asta apicale più slanciata.
- La rigenerazione produce ora anche `anteprima_apice.png`: un'inquadratura
  ravvicinata dedicata che mostra angelo, cuspide, mosaico e parte dei pinnacoli.
  `anteprima_facciata.png` resta invece la vista d'insieme.

## Versione 1.7 — ricostruzione iniziale dell'apice

Intervento concentrato sulla **punta centrale della facciata** (cuspide, mosaico
dell'Incoronazione, cornici degli spioventi, cappuccio e angelo apicale).
Il resto del prospetto è invariato.

| Elemento | Come è stato rifatto |
|---|---|
| Cornici degli spioventi | Modanature continue **tagliate a mitra** sull'asse: ogni fascia (lastra dei crockets, filo, perlinato, gola, fogliame, astragalo, toro, fregio) termina esattamente su x = 0 |
| Crockets | Foglie d'acanto piene (lobo centrale + due lobi laterali), orientate lungo la normale esterna e digradanti verso la punta |
| Fregio di cherubini | Testine a bassorilievo con fronte, naso, bocca, ciocche e ali di penne embricate, alternate a palmetti: sia lungo gli spioventi sia sulla base del mosaico (passo 1,62 m, testa 0,42 m come nell'originale) |
| Mosaico | Riestratto a 1024 px con stiramento dei livelli, contrasto locale e saturazione: l'oro torna pieno, le vesti rosse e blu leggibili |
| Fastigio apicale | Prisma traforato con feritoia a quatrifoglio, crockets, cherubino di chiave e grappe in ferro |
| Cappuccio | Calice pieno + tre ordini di foglie d'acanto sfalsate che coprono il taglio delle cornici |
| Angelo | Marmo bianco con ali in rame ossidato: figura snella panneggiata, braccio alzato con l'asta, ali a membrana con penne embricate e punte modellate |
| Ombreggiatura | Facce smooth con spigoli vivi oltre 32° (modanature tonde, cornici a spigolo) |
| Colore | View transform **Filmic** invece di AgX: i mosaici dorati non si desaturano |

Prima di questa versione le cornici erano scatole ruotate che si incrociavano
sotto l'apice lasciando vuoti neri, i crockets erano foglie sparse, i cherubini
sfere appoggiate e le ali dell'angelo 12 lame a raggiera.

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

Lo script sovrascrive `Facciata_Duomo_Siena.blend`, `anteprima_facciata.png`, `anteprima_apice.png` e `Facciata_Duomo_Siena.glb`.
