# Defekt-Analyse: swimlane/02_medium/from_xml.dot

## 1. Strukturelle Probleme

### Fehlende Pfade bei Entscheidungen

- **"Tests durchfuehren"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (1. Runde)"`. Es fehlt der Pfad fuer den Fall, dass die Tests beim ersten Durchlauf bestanden werden (z.B. "OK" --> "Tests bestanden"). Der Knoten ist als `shape=box` modelliert, obwohl hier eine Verzweigung stattfinden muesste.

- **"Retest (1. Runde)"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (2. Runde)"`. Es fehlt der "OK"-Pfad, der direkt zu `"Tests bestanden"` fuehren muesste.

- **"Retest (2. Runde)"** hat nur eine ausgehende Kante mit Label `"Bug gefunden"` zu `"Bug fixen (3. Runde)"`. Auch hier fehlt der "OK"-Pfad zu `"Tests bestanden"`.

- **"Retest (3. Runde)"** hat nur eine ausgehende Kante `"OK"` zu `"Tests bestanden"`. Es fehlt der Pfad fuer den Fall, dass auch in der 3. Runde noch Bugs gefunden werden (Eskalation, Abbruch, oder weitere Runde).

### Fehlende Entscheidungsknoten

Saemtliche Test-/Retest-Schritte sind als `shape=box` (Aktivitaet) modelliert, obwohl sie implizit Entscheidungen treffen ("Bug gefunden" vs. "OK"). Korrekt waeren explizite Entscheidungsknoten (`shape=diamond`) nach jedem Test-Schritt.

## 2. Organisatorische Probleme

### Ping-Pong zwischen Dev und QA

Der Prozess wechselt sechsmal in Folge zwischen den Lanes "Dev" und "QA":
1. `"Tests durchfuehren"` (QA) --> `"Bug fixen (1. Runde)"` (Dev) --> `"Retest (1. Runde)"` (QA)
2. `"Retest (1. Runde)"` (QA) --> `"Bug fixen (2. Runde)"` (Dev) --> `"Retest (2. Runde)"` (QA)
3. `"Retest (2. Runde)"` (QA) --> `"Bug fixen (3. Runde)"` (Dev) --> `"Retest (3. Runde)"` (QA)

Dieses Ping-Pong ist ein klassisches Effizienzproblem. Ein einzelner Zyklus mit Schleifenkante wuerde denselben Sachverhalt kompakter und flexibler abbilden.

### Management-Lane duenn besetzt

Die Lane "Management" enthaelt nur `"Start"`, `"Release freigeben"` und `"Ende"`. Da `"Start"` und `"Ende"` reine Steuerknoten sind, hat Management effektiv nur eine einzige Aktivitaet (`"Release freigeben"`). Die Daseinsberechtigung einer eigenen Lane dafuer ist fragwuerdig.

## 3. Effizienz-Probleme

### Unnoetig hartcodierte Schleifen statt dynamischer Zyklen

Der Bug-Fix-Retest-Zyklus ist dreimal als separate Knoten-Paare ausmodelliert:
- `"Bug fixen (1. Runde)"` + `"Retest (1. Runde)"`
- `"Bug fixen (2. Runde)"` + `"Retest (2. Runde)"`
- `"Bug fixen (3. Runde)"` + `"Retest (3. Runde)"`

Das sind 6 redundante Knoten, die als 2 Knoten mit Rueckkante modelliert werden koennten. Die Hartcodierung auf genau 3 Runden ist starr und bildet die Realitaet nicht flexibel ab.

### Linearer Zwangspfad

Weil die "OK"-Pfade an `"Tests durchfuehren"`, `"Retest (1. Runde)"` und `"Retest (2. Runde)"` fehlen, gibt es keinen Weg zu `"Tests bestanden"`, ohne alle drei Bug-Fix-Runden zu durchlaufen. Der Prozess erzwingt immer den laengsten Pfad -- ein klarer Modellierungsfehler.

## Hinweis

Die Dateien `from_image.dot` und `from_xml.dot` sind fuer diesen Case strukturell identisch. Alle oben genannten Defekte gelten fuer beide Varianten gleichermassen.
