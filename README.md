# Chiesa3D — Facciata del Duomo di Siena

Modello 3D (`.blend`) della **sola facciata ovest del Duomo di Siena**, ricostruita in modo procedurale a partire dalla fotografia `riferimento_facciata.jpg`. Nessun interno, nessuna navata, nessun edificio laterale: solo il fronte, con spessore ridotto (~7,8 m) e retro piatto.

## File

| File | Descrizione |
|---|---|
| `Facciata_Duomo_Siena.blend` | Modello Blender 4.2+ pronto da aprire, con rosone, sculture e frontoni dei mosaici v2.9 e materiali PBR a texture incorporate |
| `Facciata_Duomo_Siena.glb` | Esportazione glTF 2.0 per visualizzatori web / game engine |
| `anteprima_facciata.png` | Render frontale di anteprima con denoising (Cycles CPU, 64 campioni, 900×1050) |
| `anteprima_apice.png` | Render ravvicinato della cuspide centrale, delle **due torri-pinnacolo** e dell'angelo (Cycles CPU, 64 campioni, 900×1022) |
| `anteprima_torri.png` | Panoramica delle due torri-pinnacolo con i registri di lancette, i doccioni e i coronamenti (Cycles CPU, 64 campioni, 1500×820) |
| `confronto_torri.png` | Confronto fotografia / v3.2 di ciascuna torre: fusto, registro delle lancette, coronamento, guglia e statua |
| `anteprima_rosone.png` | Il rosone e tutte le statue che lo circondano, inquadrati come nella fotografia di dettaglio (Cycles CPU, 48 campioni, 1453×1582) |
| `confronto_rosone.png` | Confronto fotografia / versione 2.6 / versione 2.7 del rosone, della vetrata e delle sculture |
| `anteprima_cuspidi.png` | Il rosone al centro e i due frontoni dei mosaici ai lati, nello stesso taglio panoramico del nuovo riferimento (Cycles CPU, 64 campioni, 1800×660) |
| `confronto_cuspidi.png` | Confronto fotografia / versione 2.9 dei due frontoni: Presentazione a sinistra, Natività a destra |
| `anteprima_galleria.png` | Dettaglio panoramico v2.5 sul taglio della fotografia: fregio di cherubini, trabeazione a scacchiera, 15 edicole con profeti in altorilievo, pennacchi e sommità del rosone (Cycles CPU, 1600×520) |
| `confronto_galleria.png` | Confronto fotografia di riferimento / versione 2.4 / versione 2.5 della galleria dei Profeti |
| `genera_facciata.py` | Script procedurale che rigenera modello, texture, anteprime e GLB da zero |
| `crea_confronto_torri.py` | Compone `confronto_torri.png` affiancando i ritagli della fotografia ai render `model_sx.png` / `model_dx.png` |
| `model_sx.png`, `model_dx.png` | Render laterali di ciascuna torre usati dal confronto (Cycles CPU, 48 campioni, 340×1240) |
| `config_facciata.json` | Tutti i parametri (dimensioni, materiali PBR, luci, camera, render, export) |
| `riferimento_facciata.jpg` | Fotografia d'insieme di riferimento |
| `riferimento_apice.jpg` | Fotografia ravvicinata ad alta risoluzione (2176×2472) usata per calibrare l'intera zona superiore centrale |
| `riferimento_galleria.jpg` | Fotografia di dettaglio (1866×619) della galleria dei Profeti e dei pennacchi del rosone, riferimento della versione 2.3 |
| `riferimento_vetrata.jpg` | Fotografia di dettaglio (1453×1582) del rosone, delle nicchie laterali e dei pennacchi, riferimento della versione 2.6 |
| `riferimento_cuspidi.jpg` | Nuovo dettaglio frontale (3120×1146) dei due frontoni con la Presentazione e la Natività, riferimento della versione 2.9 |

## Dimensioni

**~90 m di larghezza × ~111 m di altezza all'angelo** (gradinata compresa: 126 m di larghezza), in unità metriche.
Il modello mantiene il fattore `scala_globale: 3.0` in `config_facciata.json` (impostandolo a `1.0` si ottengono le dimensioni in scala 1:1 di ~30 × ~37 m).

## Versione 3.2 — le due torri-pinnacolo ai lati della cuspide

Intervento dedicato alle **due torri che affiancano la cuspide centrale**
(quelle con la statua in cima, |x| ≈ 5,35 m). Nella v3.1 erano un prisma
con cinque costoloni piatti, due stecche sporgenti al posto dei doccioni,
un tabernacolo a cono e una figurina tozza: da vicino non reggevano il
confronto con `riferimento_apice.jpg`, e da lontano leggevano come due pali.

- **Fusto polistilo vero.** Cinque colonnine scanalate con basi attiche,
  entasi e capitelli a due ordini di foglie (Marmo_Bianco), colonnine
  d'angolo più grosse che arrotondano lo spigolo del torrione, e
  specchiature in **marmo rigato rosa senese** con filletti di serpentino.
- **Due registri di lancette cieche.** Quattro archi a sesto acuto per
  registro (z ≈ 20,0–21,4 m e 22,4–23,9 m) con buio sottile dentro una
  ghiera bianca a due fili, montanti, ghimberghe crochettate e bottone:
  sono gli archi che nella fotografia danno il ritmo verticale al fusto.
- **Fasce di carellature.** Tre fasce continue a z ≈ 21,5 / 24,3 / 26,2 m
  formate ciascuna da due file sfalsate di archetti lapidei, con filo di
  serpentino in ombra davanti alle colonnine: è il contrasto chiaro/scuro
  a leggere da lontano, come nella fotografia.
- **Doccioni zoomorfi scolpiti.** Due coppie alla quota delle fasce
  (z ≈ 21,2 e 24,0 m): mensola fogliata d'innesto, corpo accovacciato,
  collo teso, fauci spalancate, orecchie, ali ripiegate, zampe artigliate
  e coda arricciata — non più semplici coni protesi nel vuoto. Usano la
  stessa `gargolla()` dei contrafforti, con il mostro di profilo.
- **Cornice a tre fili** con dentelli e perline d'angolo, che chiude il
  fusto a z = 27,30 m.
- **Coronamento a grappolo.** Plinto ottagonale con specchiatura rosa,
  **otto pinnacoli** di due misure (quattro grandi sugli assi, quattro
  minori in diagonale) con nicchie cieche, guglia a sezione a otto punti,
  gattoni sugli spigoli e bottone; **lanterna traforata** a quattro archi
  con ghimberghe e la **statuetta del santo all'interno**; **guglia
  crochettata** con nodo a metà altezza e fiorone; **grande statua
  sommitale** (1,24 m) su dado ottagonale fogliato.
- **Nucleo strutturale abbassato** a 27,12 m: prima il vecchio prisma
  arrivava a 28,42 m e «inghiottiva» tutto il coronamento, che spariva
  dentro il muro.
- **Nessun elemento decorativo duplicato.** Le vecchie funzioni
  (`Guglia_Gotica_Marmo`, tabernacolo a cono, statuine sovrapposte) sono
  sostituite da `_torre_pinnacolo`, che scrive quattro oggetti per lato:
  marmo, pietra scolpita, serpentino e marmo rigato.
- Nuove anteprime `anteprima_torri.png` e `confronto_torri.png`; il render
  `anteprima_apice.png` ora inquadra anche i due coronamenti completi.
- `config_facciata.json` passa alla versione **3.2**.

## Versione 3.1 — i due triangoli dei mosaici staccati dal corpo centrale

Quarto passaggio sui **due triangoli laterali con i mosaici**, nato dalla
segnalazione che nella v3.0 erano **staccati dalla parte centrale
dell'edificio**: fra il frontone e il pilastro polistilo restava cielo.

- **Triangoli attaccati alla muratura.** Il muro di spalla laterale
  (`Corpo_Settore_Lat`) è più largo (5,70 m) e più alto, e arriva fino al
  retro piatto; il frontone (`larghezza_cuspidi_mosaico` 4,02 m,
  `altezza_cuspidi_mosaico` 3,53 m) siede sul suo interasse ±8,01 m.
- **Pilastri polistili ricostruiti.** Il fusto visibile del pilastro centrale
  va da |x| ≈ 4,7 m a 6,0 m, con costoloni bianchi scoperti, il registro di
  ghimberghe e archetti acuti sotto la cuspide, marcapiani sagomati e il
  cornicione poligonale che si salda allo spigolo interno del frontone.
- **Edicola d'angolo della galleria dei Profeti** tra il fregio di quatrifogli e
  il pilastro, come nella fotografia.
- **Mosaici ricampionati** sui nuovi punti di riferimento misurati su
  `riferimento_cuspidi.jpg` (filo interno del campo aureo). La Presentazione
  conserva il velo bianco di Anna e le figure staccate; la Natività recupera
  l'oro pieno. Colori delle vesti più saturi, meno ingiallimento dal gain sul blu.
- **Materiali**: mosaici con roughness 0,36 e metallic 0,08; marmo delle
  cuspidi più chiaro (`Marmo_Cuspidi_Chiaro`, AO 0,40).
- `config_facciata.json` passa alla versione **3.1** con le nuove dimensioni.
- Bugfix: lo script cercava le chiavi `x_pilastri_centrali`, `x_settori_laterali`
  e `base_cuspidi_laterali`, che nel JSON non esistevano, quindi i valori
  `interasse_*` e `quota_*` del file di configurazione venivano ignorati.
  Ora lo script legge le chiavi del JSON, con fallback coerenti.

**Limiti noti:** `anteprima_cuspidi.png` è stata rigenerata con
`CHIESA_SOLO_CUSPIDI=1` (64 campioni). Le altre anteprime
(`anteprima_facciata.png`, `anteprima_apice.png`, `anteprima_galleria.png`,
`anteprima_rosone.png`) e i `confronto_*.png` non sono state rigenerate e
riflettono ancora la v3.0: per allinearle eseguire `genera_facciata.py` completo.

## Versione 3.0 — i due triangoli dei mosaici, terzo passaggio

Terzo intervento dedicato ai **due triangoli laterali con i mosaici**
(Presentazione a sinistra, Natività a destra), calibrato sul confronto
diretto fra `confronto_cuspidi.png` v2.9 e la fotografia: nella v2.9 i
mosaici uscivano slavati, i gattoni leggevano come piccole colombe
bianche, la cornice era un nastro piatto e le statue apicali poggiavano
su un dado a torretta che in foto non esiste.

- **Mosaici de-velati e saturi.** Nuova estrazione
  `_extract_mosaic_laterale_v30`: il fondo della Presentazione, bruciato
  dal sole nella foto, torna bianco-oro senza annegare le figure (il
  sacerdote scuro riacquista il suo nero-blu); la Natività ritrova l'oro
  pieno. Saturazione da cartone musivo (1,24–1,34), albedo scurito per
  il sole diretto di Cycles, grana delle tessere anche nel colore e
  bump delle fughe più profondo. Via l'emissione (0,18) che slavava
  entrambe le scene e il metallic che le spegneva.
- **Gattoni a giglio senese.** `_bm_gattone_cuspide` è ora un fiore di
  giglio scolpito — petalo centrale carnoso, due petali laterali
  arcuati, sepali ricadenti e bottone alla base — in otto esemplari per
  falda, larghi circa 0,27 m come in fotografia.
- **Cornice con ombre vere.** Dieci modanature a mitra con gole di
  patina fra i fili, banda a **ovoli e dardi** scolpita lungo gli
  spioventi (gusci, ovoli a tutto tondo e dardi appuntiti) e
  perlinatura più grande sul campo aureo. I marmi delle cuspidi
  riacquistano AO e pointiness (`ao_strength` 0,48–0,62, niente
  emissione): le modanature si leggono anche in pieno sole.
- **Apice come in foto.** Eliminato il dado a torretta con specchiatura
  rosa: lastra bassa (0,15 m in tutto), capitello di foglie d'acanto e
  **statue femminili velate di 1,52 m**, mano al petto a sinistra e
  mano alzata a destra.
- **Base completata.** Fregio a ovoli e dardi a tutto tondo, perle e
  dentelli, e sotto la cornice la **fascia scura di serpentino** della
  fotografia; il grande pannello rosa piatto sotto i frontoni è
  ridotto a una sottile lastra chiara.
- `confronto_cuspidi.png` rigenerato (fotografia / v3.0); per le prove
  rapide resta `CHIESA_SOLO_CUSPIDI=1`.

## Versione 2.9 — i due frontoni dei mosaici riletti sul nuovo dettaglio

Secondo intervento dedicato ai **due triangoli laterali con i mosaici**, questa
volta calibrato sul riferimento frontale `riferimento_cuspidi.jpg` (3120×1146).
La v2.9 sostituisce proporzioni, texture e apparato decorativo della v2.8.

- **Proporzioni corrette.** Il rapporto altezza/larghezza è ora circa **0,93**:
  i frontoni non sono più schiacciati. Il campo musivo occupa circa il 78%
  della larghezza esterna e il corpo nascosto è stato assottigliato per
  eliminare il grande fianco grigio visibile in prospettiva.
- **Mosaici puliti a 1536 px.** Presentazione e Natività sono campionate sul
  filo interno corretto del nuovo ritaglio. È eliminata la banda bianca del
  mosaico destro; niente più bilanciamento sulla mediana o bordi dorati
  disegnati sopra le figure. Un micro-rilievo separato suggerisce le fughe
  fra le tessere senza coprire il dettaglio fotografico.
- **Otto modanature continue a mitra.** Fili esterni, gole, dentelli, tori,
  perlinatura lapidea e nastro a foglie/dardi hanno profondità coordinate.
  I materiali dedicati `Marmo_Cuspidi_Chiaro` e `Pietra_Cuspidi_Rilievi`
  mantengono le ombre sottili e leggibili invece di creare fasce nere.
- **Gattoni trilobati.** Nove elementi carnosi per falda, con lobo centrale,
  due lobi laterali e ricciolo, sostituiscono le piccole spine e i gambi
  cilindrici. La dimensione digrada verso l'apice.
- **Base completata.** Ovoli/foglie, dentelli e perline collegano la soglia
  del mosaico al cornicione. Eliminate le quattro ghimberghe duplicate che
  formavano una fila di “V” non presente nella fotografia.
- **Apice integrato.** Fiore fogliato, volute, dado basso scanalato con
  specchiatura rosa e statue a figura intera con plinto ridotto; la statua
  sinistra ha una posa raccolta al petto, quella destra regge il libro.
- **Nuove anteprime.** `anteprima_cuspidi.png` è ora 1800×660 e segue il taglio
  del riferimento; `confronto_cuspidi.png` affianca foto e modello dei soli
  due frontoni. Per le prove: `CHIESA_SOLO_CUSPIDI=1`.

## Versione 2.8 — le due cuspidi dei mosaici (Presentazione e Natività)

Intervento dedicato ai **due timpani laterali che affiancano il rosone**, quelli
con il mosaico su fondo aureo: nella v2.7 erano triangoli troppo acuti, con una
cornice fatta di due scatole ruotate e un mosaico da 256 px che a distanza
leggeva come una macchia slavata.

- **Proporzioni misurate sulla fotografia.** I due timpani non sono equilateri
  né acuti: sono **larghi e bassi** (H/W ≈ 0,68, apice a ~61°), centrati sui
  settori di ±8,05 m e appoggiati sul cornicione della loggia, con l'apice che
  resta libero fra i due pilastri polistili.
- **Cornice modanata a mitra.** Via le due scatole ruotate che si incrociavano
  sull'apice lasciando un vuoto nero: la cuspide ha ora sei modanature continue
  tagliate a mitra sull'asse — filo esterno in pieno sole, canalino dei
  dentelli, toro con perline, gola, secondo toro dentellato e battuta d'ombra
  sul campo aureo — ciascuna con il proprio filo frontale e la propria
  profondità.
- **Gattoni rampanti veri** (`_bm_gattone_cuspide`): sedici per falda, sono
  foglie carnose lobate che si arricciano verso l'esterno con perla terminale
  e seconda fogliolina alla base, rastremate verso la punta; prima erano
  cilindri con una sfera in cima.
- **Mosaici ad alta risoluzione.** Texture da **1024 px** (prima 256) lette
  quasi per intero dal triangolo reale, con i bordi lapidei sostituiti da
  tessere d'oro, contrasto e saturazione riportati e calibrazione fotometrica
  ambrata: sotto il sole diretto l'oro resta oro e le figure conservano i rossi,
  i blu e i verdi dei cartoni ottocenteschi.
- **Campo aureo arretrato di 0,17 m** rispetto alla cornice: il risalto delle
  modanature nasce dalla profondità e il bordo del mosaico non scompare più
  dietro la ghiera (nella v2.7 il mosaico sporgeva e la cornice interna
  spariva).
- **Base e apice ridisegnati.** Base d'imposta a tre fili sottili con dentelli
  e perline a sbalzo; dado apicale con gola fogliata e statua a figura intera
  di 0,33 h (`statua_gotica_v26`), al posto della figurina di 1,25 m su un
  piedistallo troppo pesante. Nessun pinnacolo sull'apice, come in fotografia.
- **Nuova inquadratura `anteprima_cuspidi.png`** (1600×700) che riprende
  esattamente il taglio della fotografia d'insieme: rosone al centro, i due
  timpani ai lati, e `confronto_cuspidi.png` con foto e modello affiancati.

## Versione 2.7 — vetrata e sculture del rosone, secondo passaggio profondo

Intervento concentrato sulla fotografia `riferimento_vetrata.jpg`: non si
limita ai materiali, ma corregge geometria, proporzioni, pose e inquadratura.

- **Rosone circolare.** L'apertura e tutti gli ordini concentrici della ghiera
  usano ora lo stesso raggio orizzontale e verticale; il pannello dei
  pennacchi è stato riportato alla larghezza misurata sulla fotografia.
- **Vetro fotografico pulito, non quattro campioni ripetuti.** Una texture da
  **1536×1536 px** rilegge l'intera vetrata e conserva le differenze fra le
  diciotto lastre, i graffi, le nuvolature e le bollicine. Montanti e
  Redentore presenti nella foto sono rimossi per campionamento locale: il
  reticolo e la statua sono soltanto geometria 3D, mai ombre stampate.
- **Materiale del vetro più credibile.** Emissione bilanciata per evitare sia
  il disco nero sia il pannello piatto, micro-bump, ondulazione millimetrica
  della lastra e riflesso controllato. La piombatura è davanti al vetro, con
  due montanti, cinque traversi e filo perimetrale a sezione sottile.
- **Ghiera scolpita sul telaio corretto.** Eliminate le scaglie disposte sul
  piano sbagliato: **288 foglie d'acanto lobate** con costa centrale,
  **180 dentelli**, perlinatura, volute, corda e mosaico seguono ora la
  circonferenza con profondità frontale coerente.
- **Quattro profeti a figura intera.** I busti dei pennacchi sono sostituiti
  da figure complete in contrapposto: tunica continua, manto a doppia
  superficie con orli, piedi separati, maniche raccordate e mani articolate.
  I superiori indicano e parlano verso l'oculo; gli inferiori reggono rotolo
  e libro. Sono avanzati e spostati quanto basta per non nascondere i gesti
  dietro la ghiera.
- **Otto nicchie laterali abitate.** Ogni edicola ha fondo chiaro, catino
  concavo con costole, triplice arco, capitelli, ghimberga, mensola e
  cosmatesco. I busti sono più grandi e alternano lettura, pensiero, rotolo,
  preghiera e gesto parlante; la fascia esterna ha sedici quatrifogli per lato.
- **Redentore rifatto nella posa e nella scala.** Figura raccolta con mano al
  petto, capelli lunghi e manto continuo; l'altezza e il piedistallo sono
  calibrati sul rapporto fra testa, bordo inferiore del vetro e ghimberga.
- **Nuovo render 1453×1582** con tutte le sculture nel campo e
  `confronto_rosone.png` aggiornato a fotografia / v2.6 / v2.7.

## Versione 2.6 — il rosone e le statue che lo circondano

Intervento dedicato alla **vetrata, alla ghiera e alle sculture che la
circondano**, riletti sulla nuova fotografia di dettaglio
`riferimento_vetrata.jpg` (1453×1582). Il resto della facciata è invariato.

- **Vetrata cattedrale vera.** Il vetro non è più un disco scuro con un
  ritaglio stirato: è un disco con UV proprie, la cui texture è composta da
  **quattro riquadri puliti letti dalla fotografia** (azzurro-verde
  lattiginoso, nuvolature, bollicine) disposti 2×2 senza specchiature, quindi
  senza ripetizioni visibili. Dietro il vetro c'è un fondo opaco: niente più
  cielo che filtra dalle fughe.
- **Piombatura sottile**: due montanti verticali a un terzo del raggio, cinque
  traversi e filo perimetrale, a sezione piatta di ferro — non più tubi neri
  spessi e non più il reticolo dorato che girava *dentro* il vetro.
- **Ghiera rifatta come nell'intaglio originale**: orlo modanato doppio, gola
  in ombra, **perlinatura fitta (196 perle)**, **due ordini di fogliame
  d'acanto che corrono lungo l'arco** — ogni foglia è orientata da un telaio
  locale tangente all'ellisse, quindi giace *sulla* fascia invece di sporgere
  a raggiera — **corda intrecciata oro/avorio** a due capi, occhi di voluta e
  **mosaico aureo a tessere** sul bordo del vetro.
- **Strombatura troncoconica in ombra** fra il filo della ghiera e il vetro:
  la profondità del rosone nasce dalla geometria.
- **Quattro profeti sui pennacchi** (prima due): i due superiori sdraiati in
  diagonale con il braccio teso verso l'oculo, i due inferiori ritti e rivolti
  al centro, su pannelli di marmo rigato con cornice.
- **Nicchie laterali rifatte** (`edicola_v26`): incasso in marmo rigato,
  pilastrini con capitello, doppia ghiera, ghimberga a gattoni e fiorone,
  **quattro per lato con statue a figura intera**. Le vecchie nicchiette
  lasciavano intravedere lastre nere: eliminate.
- **Statue a figura intera nuove** (`statua_gotica_v26`): corpo a sezioni con
  pieghe lunghe e scanalate, pieghe-cordone del manto, cintola annodata,
  spalle raccordate, mani articolate con polsino, volto di
  `_bm_testa_profeta24`. Pose differenziate (libro, lettura, croce, petto,
  benedizione).
- **Il Redentore al centro**, a figura intera e benedicente, si staglia
  davanti al vetro del rosone come in fotografia (prima era una statuina di
  sfere e coni).
- Nuova inquadratura `anteprima_rosone.png`, nuovo `confronto_rosone.png`
  (foto / 2.5 / 2.6) e variabile `CHIESA_SOLO_ROSone=1` per renderizzare solo
  questo settore durante le prove.

## Versione 2.5 — la fascia sopra lo specchio riletta sulla fotografia

Terzo passaggio sulla fascia **sopra lo specchio del rosone e sotto il
triangolo centrale**, questa volta per chiudere i conti con il dettaglio
fotografico `riferimento_galleria.jpg`: non cambiano le 15 campate né le
pose, ma sfondi, trabeazione, pennacchi e corona dell'oculo.

- **Via la banda grigio-azzurra.** Nella 2.4 dietro le punte dei frontoni
  restava un campo azzurro che nel render leggeva come una striscia di
  cielo. Ora il marmo rosa rigato sale continuo fino al filetto verde
  sotto la trabeazione (chiusa anche la fessura da cui il cielo
  traspariva), e i pannellini cosmateschi nella V fra i frontoni sono
  più ampi e incorniciati, quindi il mosaico si legge fra le punte.
- **Frontoni più fitti e più bassi:** chevron ribassato, una seconda
  cornice a chevron in rilievo e un'**ogivetta con giglio senese,
  rosetta e volute** al posto del motivo precedente (che a distanza
  leggeva come una “X”); sei gattoni uncinati per falda invece di quattro.
- **Profeti più presenti ma più ariosi:** i busti sono un poco più
  stretti della luce (il fondale rosa si rivede ai lati, come in foto) e
  avanzati verso la ghiera, in vero altorilievo; i lembi dei manti
  scendono più lunghi sul parapetto e le specchiature cosmatesche di
  parapetto e piedritti sono più larghe.
- **Pennacchi del rosone finalmente protagonisti.** I due profeti ai
  lati dell'arco sono ora **mezze figure grandi sdraiate in diagonale**
  sui pannelli rosa (testa all'angolo alto esterno, corpo sporto in
  avanti, braccio teso verso il rosone a sinistra e mano alzata a
  destra). Nella 2.4, piccoli e verticali, restavano semisepolti
  dietro la ghiera: si vedevano quasi solo le teste.
- **Trabeazione completata:** sopra la galleria compaiono la
  **scacchiera cosmatesca a due ordini** bianco/verde sotto il fregio e
  la fascia a **ovoli e dardi** fra toro e dentelli; i cherubini del
  fregio sono più grandi, con le ali abbassate sulla soglia, e i gigli
  riempiono gli intervalli.
- **Sommità dell'oculo rifinita:** 172 dentelli fogliati e 172 perle
  (prima 112, che leggevano come borchie distanziate) e nuovo **anello
  a losanghe oro/verde** sullo sguincio interno. Ai lati del quadrato,
  le strisce con sfere diventano pannelli bianchi a quatrifogli con
  cornice in marmo verde.
- `anteprima_galleria.png` è ri-inquadrata sul taglio esatto della
  fotografia: dentro fregio, trabeazione, galleria e i due pennacchi
  per intero. `confronto_galleria.png` affianca foto / 2.4 / 2.5.

## Versione 2.4 — sculture e decori della fascia interamente rifiniti

Secondo intervento profondo sulla fascia **sopra lo specchio del rosone e sotto
il triangolo centrale**, concentrato questa volta sulla qualità scultorea e sulla
lettura d'insieme della fotografia. Le 15 campate e la Madonna sull'asse restano
al loro posto, ma le figure non sono più costruite come manichini.

- **Torso e manti sono superfici continue.** Il corpo ha spalle larghe, vita e
  ventre modellati, grandi pieghe a U e un manto diagonale che segue il volume.
  Maniche, polsi, dita e ciocche seguono curve continue invece di cilindri
  giuntati. Anche i lembi oltre il parapetto sono tessuto scolpito, senza
  l'effetto frangia della versione precedente.
- **Volti finalmente leggibili:** mascella, zigomi, mento, naso con narici,
  orbite, occhi, palpebre, sopracciglia, labbra e orecchie; barbe con massa e
  ciocche separate, capelli ondulati e copricapi differenti. Le mani hanno palmo,
  quattro dita e pollice, con gesti aperti, chiusi o in preghiera.
- **Pose più diverse e figure più presenti.** Il profeta sporgente è più grande
  e ruotato, il pensatore tocca il viso, il lettore regge un libro sottile con
  pagine separate, la Madonna sorregge un Bambino proporzionato. Le figure
  occupano meglio le nicchie grazie anche ai piedritti assottigliati.
- **Frontoni e fondo corretti:** gigli e rosette dentro i timpani, perlinatura
  più fitta, gattoni più contenuti e campo grigio-azzurro solo dietro la parte
  alta dei frontoni, non una fascia nera continua.
- **Sommità del rosone più fedele:** dentelli minuti con foglie, perline più
  fitte e pannelli in marmo rosa rigato. I due profeti dei pennacchi usano la
  stessa nuova scultura della galleria.
- **Un solo fregio di cherubini**, più grande e alternato a gigli sotto il
  mosaico; eliminate le sovrapposizioni fra i due fregi precedenti. Le mensole
  della trabeazione hanno ora una foglia scolpita sul fronte.
- `anteprima_galleria.png` usa una camera ricalibrata che comprende fregio,
  galleria, arco e profeti dei pennacchi nello stesso formato panoramico.

## Versione 2.3 — galleria dei Profeti rifatta sulla nuova fotografia

Nuovo intervento integrale sulla fascia **sopra lo specchio del rosone e sotto
il triangolo centrale** (`Nicchia_Sup_00` … `Nicchia_Sup_14`), ricostruita sulla
fotografia di dettaglio ad alta risoluzione `riferimento_galleria.jpg`.
Il resto della facciata resta invariato.

- **Sono 15 campate, non 14.** Contando gli archi in fotografia: 7 profeti, la
  **Madonna col Bambino esattamente sull'asse** della facciata (con i due
  angiolini sdraiati sul frontone centrale), altri 7 profeti. Nella 2.2 l'asse
  cadeva fra due campate.
- **Busti grandi in altorilievo, mai più “pedine”.** La testa sale dentro la
  curva dell'arco e il torso è una massa organica di panneggio (ventre sulle
  ginocchia, petto, spalle) tagliata al parapetto; via la silhouette a cono del
  tornio, via il nimbo (in foto non c'è), via il colletto a piedistallo.
- **15 pose lette una per una dalla foto** (tabella `_POSE_PROFETI`): il grande
  profeta sporgente in diagonale col braccio oltre il davanzale, il pensatore
  con la mano alla guancia, l'orante a mani giunte, l'inchinato verso la
  Madonna, i lettori col libro aperto, il rotolo la cui punta scende sul
  parapetto… e i **lembi di manto appuntiti** che scendono davanti al parapetto
  cosmatesco dove la foto li mostra.
- **Frontone triangolare pieno.** Nella 2.2 era un doppio contorno di fasce
  vuoto; ora è un pannello pieno con doppia cornice modanata, triangolo
  inciso, losanga cosmatesca verso la punta, gattoni e fiorone. Fra i frontoni,
  pinnacolini bassi con statuina davanti a pannellini cosmatesci incassati.
- **Niente più banda nera.** La fascia cosmatesca alta un quarto della fascia
  (in foto non esiste: è solo un filetto di marmo verde sotto la trabeazione)
  è stata eliminata; il cosmatesco, con texture schiarita in toni caldi, vive
  dove sta davvero: specchiature verticali dei piedritti (con file di perle),
  parapetto sotto ogni campata, pannellini fra i frontoni.
- **Nicchie a tutto sesto poco profonde** con fondale rosa unico che riempie
  anche la lunetta dietro la testa e triplice ghiera concentrica perlinata;
  piedritti a parasta con capitello a fasce all'imposta.
- **Pennacchi del rosone corretti.** Ai piedi della galleria, ai lati
  dell'arco dell'oculo, non ci sono angeli alati con fiori (vecchia versione):
  sono i **due profeti a mezza figura sui pannelli di marmo rosa** con cornice
  verde — a sinistra indica il rosone col braccio teso, a destra parla con la
  mano alzata. Rimosse anche le rosette a fiore che li coprivano.
- `CHIESA_SOLO_GALLERIA=1` renderizza solo la vista della galleria (prove
  rapide); `anteprima_galleria.png` sale a 1600×520.

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

Lo script legge alcune variabili d'ambiente opzionali, utili per iterare senza
toccare `config_facciata.json`:

```bash
CHIESA_SAMPLES=16 CHIESA_RES_X=450 CHIESA_RES_Y=600 CHIESA_NO_GLB=1 python genera_facciata.py
CHIESA_NO_RENDER=1 python genera_facciata.py       # solo .blend, senza render
CHIESA_SOLO_ROSone=1 python genera_facciata.py     # solo la vista del rosone
CHIESA_SOLO_CUSPIDI=1 python genera_facciata.py    # solo i frontoni dei mosaici
CHIESA_SOLO_TORRI=1 python genera_facciata.py      # solo la panoramica delle due torri
CHIESA_SALTA_DETTAGLI_CENTRALI=1 python genera_facciata.py  # facciata + cuspidi
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

Lo script sovrascrive `Facciata_Duomo_Siena.blend`, `anteprima_facciata.png`, `anteprima_apice.png`, `anteprima_galleria.png`, `anteprima_rosone.png`, `anteprima_cuspidi.png`, `anteprima_torri.png` e, se abilitato, `Facciata_Duomo_Siena.glb`.

`confronto_torri.png` si rigenera a parte, dopo aver salvato i due render laterali:

```bash
python crea_confronto_torri.py
```
