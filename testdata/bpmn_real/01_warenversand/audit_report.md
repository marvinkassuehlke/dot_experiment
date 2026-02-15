# Process Audit Report: Warenversand Hardware-Händler

**Artefakt:** warenversand (bpmn_rendered.png + source.xml)
**Typ:** BPMN 2.0
**Analyse-Modus:** Dual-Input (Bild + XML)

---

## Übersicht

| | High | Medium | Low | Gesamt |
|---|---|---|---|---|
| **Strukturell** | 2 | 2 | 0 | 4 |
| **Organisatorisch** | 0 | 1 | 2 | 3 |
| **Effizienz** | 1 | 1 | 3 | 5 |
| **Gesamt** | **3** | **4** | **5** | **12** |

**Overlap-Rate:** 42% (5 von 12 Findings wurden von beiden Perspektiven identifiziert)

---

## Strukturelle Probleme

### F1 — AND-Split ohne AND-Join (HIGH) `source: structural`

**Betroffene Elemente:** ParallelGateway (AND-Split), ExclusiveGateway_0z5sib0 (XOR-Join)

Der Prozess beginnt mit einem AND-Split, der in "Versandart klären" (Sekretariat) und "Ware verpacken" (Lagerarbeiter) forkt. Diese parallelen Pfade werden durch einen XOR-Join zusammengeführt, der bereits beim ersten eintreffenden Token feuert. Dadurch kann "Ware bereitstellen" starten, bevor beide Pfade abgeschlossen sind — z.B. Ware bereitgestellt ohne geklärte Versandart oder ohne Verpackung.

### F2 — Inklusives Gateway ohne explizite Default-Bedingung (MEDIUM) `source: both`

**Betroffene Elemente:** InclusiveGateway_0p2e5vq (OR-Split)

Das inklusive OR-Gateway nach "Sonderversand? = nein" hat Pfade "immer" und "Versicherung erforderlich". Der Pfad "immer" suggeriert ständige Ausführung, aber es fehlt eine formale Default-Bedingung. In einer Prozess-Engine könnte dies zu Laufzeitfehlern führen.

### F3 — Kein Fehlerbehandlungspfad (HIGH) `source: direct`

**Betroffene Elemente:** Gesamter Prozess

Es gibt keinen Fehler- oder Eskalationspfad. Was passiert bei: Spediteur nicht verfügbar, Versicherung abgelehnt, Ware defekt/fehlend? Ein Warenversandprozess ohne Ausnahmebehandlung ist in der Praxis nicht robust.

### F4 — Sonderversand umgeht Paketschein/Versicherungslogik (MEDIUM) `source: both`

**Betroffene Elemente:** XOR Sonderversand, Angebote einholen, Spediteur beauftragen, OR-Split

Bei "Sonderversand = ja" führt der Pfad direkt zu Angebotseinholung und Spediteurbeauftragung, wobei Paketschein und Versicherungsprüfung komplett übersprungen werden. Möglicherweise beabsichtigt, aber nicht dokumentiert.

---

## Organisatorische Probleme

### F5 — Sekretariat als zentrales Bottleneck (MEDIUM) `source: both`

**Betroffene Elemente:** Lane Sekretariat (Versandart klären, Angebote einholen, Spediteur beauftragen, Paketschein ausfüllen)

Das Sekretariat führt 5 von 7 operativen Aktivitäten aus und enthält 8 der Flow-Knoten. Es verantwortet alle Entscheidungs- und Organisationsschritte. Bei hohem Versandvolumen wird es zum Engpass.

### F6 — Leiter Logistik unterausgelastet (LOW) `source: both`

**Betroffene Elemente:** Lane Leiter Logistik, Versicherung abschließen

Die Lane "Leiter Logistik" enthält nur eine einzige Aufgabe ("Versicherung abschließen"), die zudem nur bedingt ausgeführt wird. Eine eigene Lane/Rolle für eine optionale Aufgabe ist organisatorisch fragwürdig.

### F7 — Keine Freigabe bei Spediteur-Beauftragung (LOW) `source: direct`

**Betroffene Elemente:** Spediteur beauftragen

Die Beauftragung eines Spediteurs erfolgt direkt durch das Sekretariat ohne Freigabe durch den Leiter Logistik oder eine andere Instanz. Bei hohen Versandkosten fehlt ein Vier-Augen-Prinzip.

---

## Effizienz-Probleme

### F8 — Sequenzielle Angebotseinholung als Blocker (HIGH) `source: both`

**Betroffene Elemente:** Angebote von 3 Spediteuren einholen

Das Einholen von drei Spediteursangeboten ist als einzelner sequenzieller Task modelliert und liegt auf dem kritischen Pfad. Die Anfragen könnten parallel gesendet werden. Zudem suggeriert der Prozess, dass bei jedem Sonderversand von Null begonnen wird — keine Rahmenverträge.

### F9 — Parallelisierung birgt Verpackungsrisiko (MEDIUM) `source: direct`

**Betroffene Elemente:** AND-Split, Ware verpacken, Versandart klären

Die parallele Ausführung von "Ware verpacken" und "Versandart klären" ist effizient, aber die Verpackungsart könnte von der Versandart abhängen (z.B. Palettierung). Der Lagerarbeiter verpackt möglicherweise falsch.

### F10 — Fehlende Automatisierungspotenziale (LOW) `source: direct`

**Betroffene Elemente:** Paketschein ausfüllen, Versandart klären

Beide Tasks sind als manuelle Aktivitäten modelliert. In modernen Logistikprozessen werden Paketscheine automatisch aus dem ERP generiert und die Versandart regelbasiert bestimmt.

### F11 — Kein expliziter Angebotsvergleich vor Beauftragung (LOW) `source: direct`

**Betroffene Elemente:** Angebote einholen, Spediteur beauftragen

Zwischen Angebotseinholung und Beauftragung fehlt ein expliziter Vergleichs- und Entscheidungsschritt. Die Spediteurauswahl geschieht implizit.

### F12 — Redundante Gateway-Kette (LOW) `source: structural`

**Betroffene Elemente:** InclusiveGateway_1dgb4sg (OR-Join), ExclusiveGateway_1ouv9kf (XOR-Join)

Die Kette aus Inclusive-OR-Join zu XOR-Join erzeugt eine zusätzliche Indirektion, die den Prozess schwerer lesbar macht, ohne fachlichen Mehrwert zu bieten.

---

## Methodik

Dieser Audit verwendet einen **Dual-Perspective-Ansatz**:

1. **Direkte Analyse**: Das originale BPMN-Diagramm (PNG) wurde visuell analysiert wie durch einen Prozessberater — Fokus auf Business-Logik, Governance, Szenarien und organisatorische Schwächen.

2. **Strukturelle Analyse**: Das BPMN-XML wurde in ein Mermaid-Zwischenformat übersetzt und graph-basiert analysiert — Fokus auf Gateway-Typen, Topologie, Synchronisationsfehler und Erreichbarkeit.

3. **Synthese**: Findings beider Perspektiven wurden zusammengeführt, dedupliziert und mit Quellenangabe versehen. Die **Overlap-Rate von 42%** zeigt, dass beide Perspektiven substantiell unterschiedliche Aspekte aufdecken. Insbesondere wurde der kritische Gateway-Typ-Fehler (F1: AND-Split ohne AND-Join) ausschließlich durch die strukturelle Analyse erkannt, während Governance-Lücken (F3, F7) und Automatisierungspotenziale (F10) nur durch die direkte Analyse sichtbar wurden.

Da nur ein einzelnes Artefakt analysiert wurde, entfällt die Cross-Artefakt-Konsistenzprüfung.
