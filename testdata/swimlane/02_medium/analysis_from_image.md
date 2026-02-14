# Defekt-Analyse: swimlane/02_medium/from_image.dot

## 1. Strukturelle Probleme

### Fehlende Pfade bei Entscheidungen

- **"Tests durchfuehren"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (1. Runde)"`. Es fehlt der Pfad fuer den Fall, dass die Tests beim ersten Durchlauf bestanden werden (z.B. "OK" --> "Tests bestanden"). Der Knoten ist de facto kein Entscheidungsknoten (shape=box statt diamond), obwohl hier eine Verzweigung stattfinden muesste.

- **"Retest (1. Runde)"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (2. Runde)"`. Es fehlt der "OK"-Pfad, der direkt zu `"Tests bestanden"` fuehren muesste.

- **"Retest (2. Runde)"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (3. Runde)"`. Auch hier fehlt der "OK"-Pfad zu `"Tests bestanden"`.

- **"Retest (3. Runde)"** hat nur eine ausgehende Kante `"OK"` zu `"Tests bestanden"`. Es fehlt der Pfad fuer den Fall, dass auch in der 3. Runde noch Bugs gefunden werden. Der Prozess modelliert keinen Eskalations- oder Abbruchpfad.

### Fehlende Entscheidungsknoten

Saemtliche Test-/Retest-Schritte sind als `shape=box` (Aktivitaet) modelliert, obwohl sie implizit Entscheidungen beinhalten ("Bug gefunden" vs. "OK"). Es fehlen explizite Entscheidungsknoten (`shape=diamond`), die die Verzweigung sauber abbilden.

## 2. Organisatorische Probleme

### Ping-Pong zwischen Dev und QA

Der Prozess wandert dreimal zwischen den Lanes "Dev" und "QA" hin und her:
1. `"Tests durchfuehren"` (QA) --> `"Bug fixen (1. Runde)"` (Dev) --> `"Retest (1. Runde)"` (QA)
2. `"Retest (1. Runde)"` (QA) --> `"Bug fixen (2. Runde)"` (Dev) --> `"Retest (2. Runde)"` (QA)
3. `"Retest (2. Runde)"` (QA) --> `"Bug fixen (3. Runde)"` (Dev) --> `"Retest (3. Runde)"` (QA)

Das sind 6 Lane-Wechsel in Folge. In der Realitaet wuerde man das als einen einzigen Bug-Fix-Zyklus mit Schleife modellieren, nicht als drei fest verdrahtete Runden.

### Management-Lane duenn besetzt

Die Lane "Management" enthaelt nur `"Start"`, `"Release freigeben"` und `"Ende"`. Die Start/Ende-Knoten sind reine Steuerelemente. Die einzige echte Aktivitaet ist `"Release freigeben"` -- ob das eine eigene Lane rechtfertigt, ist fragwuerdig.

## 3. Effizienz-Probleme

### Unnoetig hartcodierte Schleifen statt dynamischer Zyklen

Der Bug-Fix-Retest-Zyklus ist dreimal als separate Knoten ausmodelliert (`"Bug fixen (1./2./3. Runde)"` und `"Retest (1./2./3. Runde)"`), anstatt als eine Schleife mit Zaehler oder Exit-Bedingung. Das fuehrt zu:
- **Redundanten Schritten**: 6 Knoten (3x Bug fixen + 3x Retest) statt 2 Knoten mit Rueckkante.
- **Starrheit**: Der Prozess kann genau 3 Runden abbilden -- weder weniger (ohne fehlende OK-Pfade, s.o.) noch mehr.

### Linearer Zwangspfad

Da die "OK"-Pfade an `"Tests durchfuehren"`, `"Retest (1. Runde)"` und `"Retest (2. Runde)"` fehlen, muss der Prozess immer alle 3 Bug-Fix-Runden durchlaufen, bevor er bei `"Tests bestanden"` ankommen kann. Das ist offensichtlich nicht intendiert.
