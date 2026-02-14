# Defekt-Analyse: Onboarding (from_image.dot)

## 1. Strukturelle Probleme

### Fehlendes Parallel-Gateway (AND-Split)
Der Startknoten **"Neuer\nMitarbeiter"** verzweigt direkt auf drei Aktivitaeten in drei Lanes: **"Laptop\nbereitstellen"**, **"Vertrag\nfinalisieren"** und **"Einarbeitungsplan\nerstellen"**. Ein explizites AND-Split-Gateway fehlt. In BPMN ist ein paralleles Gateway notwendig, um die Semantik "alle Pfade werden gleichzeitig gestartet" korrekt auszudruecken. Ohne dieses Gateway ist die Parallelitaet nur implizit und koennte auch als alternative Pfade (XOR) interpretiert werden.

### Fehlendes Parallel-Gateway (AND-Join)
Entsprechend fehlt vor **"Teamlead-\nFreigabe"** ein explizites AND-Join-Gateway. Drei eingehende Kanten (von **"Software\ninstallieren"**, **"Willkommenspaket"**, **"Erste Aufgaben\ndefinieren"**) muenden direkt in den Aktivitaetsknoten. Es ist strukturell nicht modelliert, ob alle drei Pfade abgeschlossen sein muessen, bevor die Freigabe erfolgt.

## 2. Organisatorische Probleme

### Bottleneck: Teamlead-Freigabe
Der Knoten **"Teamlead-\nFreigabe"** ist ein Bottleneck: Alle drei parallelen Pfade (IT, HR, Fachbereich) konvergieren dort. Wenn der Teamlead nicht verfuegbar ist, blockiert der gesamte Onboarding-Prozess.

### Unklare Verantwortlichkeit: Teamlead-Freigabe
**"Teamlead-\nFreigabe"** liegt ausserhalb aller definierten Cluster (IT, HR, Fachbereich). Es gibt keinen eigenen Cluster fuer den Teamlead und der Knoten ist keiner Lane zugeordnet. Die organisatorische Zustaendigkeit fuer diesen Prozessschritt ist damit unklar.

## 3. Effizienz-Probleme

Keine Effizienz-Probleme identifiziert. Die drei parallelen Straenge (IT, HR, Fachbereich) sind sinnvoll aufgeteilt, und innerhalb jedes Strangs gibt es eine logische Reihenfolge ohne Redundanzen oder unnoetige Schleifen.

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturell | 2 | Mittel (fehlendes AND-Split), Mittel (fehlendes AND-Join) |
| Organisatorisch | 2 | Mittel (Bottleneck Teamlead), Niedrig (unklare Lane-Zuordnung) |
| Effizienz | 0 | -- |

Die Hauptdefekte sind die fehlenden parallelen Gateways: Ohne expliziten AND-Split und AND-Join ist die Synchronisationssemantik der drei Pfade ambig. Zudem ist die organisatorische Einordnung der Teamlead-Freigabe nicht modelliert.
