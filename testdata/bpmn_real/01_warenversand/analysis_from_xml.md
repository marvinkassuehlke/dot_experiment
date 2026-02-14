# Prozessanalyse: Warenversand Hardware-Händler

Quelle: `from_xml.dot` (übersetzt aus Camunda BPMN 2.0 XML)

---

## 1. Strukturelle Probleme

### 1.1 Fehlende Synchronisation der parallelen Pfade (schwerwiegend)

Der Prozess beginnt mit einem **AND-Split** (`ParallelGateway_02fgrfq`), der zwei parallele Pfade startet:

- **Pfad A (Sekretariat):** "Versandart klären" und nachfolgende Logik
- **Pfad B (Lagerarbeiter):** "Ware verpacken"

Diese beiden Pfade werden jedoch durch einen **XOR-Join** (`ExclusiveGateway_0z5sib0`, Label: "XOR") zusammengeführt — nicht durch einen AND-Join. Ein XOR-Gateway feuert, sobald **einer** der eingehenden Pfade eintrifft. Das bedeutet:

- Wenn "Ware verpacken" schneller abgeschlossen ist als die Versandorganisation, wird "Ware bereitstellen" ausgelöst, **bevor eine Versandart feststeht** oder ein Spediteur beauftragt ist.
- Wenn umgekehrt die Versandart zuerst geklärt wird, wird die Ware bereitgestellt, **bevor sie verpackt ist**.

**Korrekte Lösung:** `ExclusiveGateway_0z5sib0` müsste ein **Parallel Gateway (AND-Join)** sein, damit beide Pfade abgeschlossen sein müssen, bevor "Ware bereitstellen" beginnt.

### 1.2 Fehlender Pfad: Normalversand ohne Versicherung

Der Inclusive-OR-Split (`InclusiveGateway_0p2e5vq`) hat zwei ausgehende Kanten:

- "Versicherung erforderlich" → "Versicherung abschließen"
- "immer" → "Paketschein ausfüllen"

Die Bezeichnung "immer" suggeriert, dass "Paketschein ausfüllen" in jedem Fall ausgeführt wird, während "Versicherung abschließen" nur bei Bedarf. Das ist als Inclusive-OR korrekt modelliert. Allerdings fehlt eine explizite Default-Bedingung — es ist nur durch das Label "immer" implizit klar, dass mindestens ein Pfad aktiv ist. In einer Prozess-Engine könnte eine fehlende Bedingungsdefinition zu einem Laufzeitfehler führen.

---

## 2. Organisatorische Probleme

### 2.1 Unterauslastung: Leiter Logistik

Die Lane "Leiter Logistik" enthält **nur eine einzige Aufgabe**: "Versicherung abschließen". Diese wird zudem nur **bedingt** ausgeführt (nur wenn "Versicherung erforderlich" gilt). Das wirft Fragen auf:

- Ist eine eigene Lane/Rolle für eine einzelne, optionale Aufgabe gerechtfertigt?
- Kann die Aufgabe an das Sekretariat delegiert werden, das ohnehin den gesamten administrativen Pfad steuert?

### 2.2 Überlastung: Sekretariat

Die Lane "Sekretariat" enthält **10 Flow-Knoten** (3 Tasks, 4 Gateways, 1 Start-Event, 2 weitere Gateways für Zusammenführung). Das Sekretariat ist für die gesamte Versandlogik verantwortlich:

- Versandart klären
- Angebote einholen (bei Sonderversand)
- Spediteur beauftragen
- Paketschein ausfüllen

Das macht das Sekretariat zum **zentralen Bottleneck** des Prozesses. Alle Entscheidungs- und Organisationsschritte laufen ausschließlich durch diese Lane.

### 2.3 Lagerarbeiter erst spät aktiv

Der Lagerarbeiter hat zwei Aufgaben ("Ware verpacken" und "Ware bereitstellen"), wobei "Ware bereitstellen" erst nach dem fehlerhaften XOR-Join kommt. Faktisch wartet der Lagerarbeiter nach dem Verpacken auf das Sekretariat — ohne dass dies explizit modelliert ist (kein Wartezustand, kein Message-Event).

---

## 3. Effizienz-Probleme

### 3.1 Sequenzielles Einholen von 3 Angeboten

Die Aufgabe "Angebote von 3 Spediteuren einholen" ist als einzelner Task modelliert. In der Realität könnten die drei Angebotsanfragen **parallel** gesendet werden. Die sequenzielle Modellierung als ein Block ist akzeptabel (Abstraktion), aber bei der Prozessoptimierung ein Ansatzpunkt.

### 3.2 Kein Feedback-Loop bei Angebotsprüfung

Nach "Angebote von 3 Spediteuren einholen" folgt direkt "Spediteur beauftragen" — ohne eine explizite Entscheidung, welcher Spediteur den Zuschlag erhält, oder eine Prüfung, ob die Angebote akzeptabel sind. Es fehlt ein Entscheidungs-Gateway zwischen diesen beiden Tasks.

### 3.3 Redundanter XOR-Join (ExclusiveGateway_1ouv9kf)

Der XOR-Join `ExclusiveGateway_1ouv9kf` führt zwei Pfade zusammen:

- Sonderversand-Pfad (über "Spediteur beauftragen")
- Normalversand-Pfad (über OR-Join `InclusiveGateway_1dgb4sg`)

Da diese beiden Pfade aus einer XOR-Entscheidung (`Sonderversand?`) stammen, ist der XOR-Join hier korrekt. Allerdings erzeugt die Kette `InclusiveGateway_1dgb4sg` → `ExclusiveGateway_1ouv9kf` eine zusätzliche Indirektion, die den Prozess schwerer lesbar macht.

---

## Zusammenfassung

| # | Kategorie | Problem | Schwere |
|---|-----------|---------|---------|
| 1.1 | Strukturell | AND-Split ohne AND-Join — XOR-Join bei `ExclusiveGateway_0z5sib0` synchronisiert parallele Pfade nicht | Hoch |
| 1.2 | Strukturell | Fehlende explizite Default-Bedingung am OR-Split | Mittel |
| 2.1 | Organisatorisch | Lane "Leiter Logistik" mit nur einer optionalen Aufgabe | Niedrig |
| 2.2 | Organisatorisch | Sekretariat als zentrales Bottleneck (10 Knoten) | Mittel |
| 2.3 | Organisatorisch | Implizites Warten des Lagerarbeiters nicht modelliert | Niedrig |
| 3.1 | Effizienz | Sequenzielle Angebotseinholung statt parallel | Niedrig |
| 3.2 | Effizienz | Fehlende Angebotsprüfung vor Beauftragung | Mittel |
| 3.3 | Effizienz | Redundante Gateway-Kette erschwert Lesbarkeit | Niedrig |
