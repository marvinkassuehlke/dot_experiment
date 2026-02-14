# DOT Translation Study — Ergebnisse

## Hypothese

GraphViz DOT taugt als Zwischenformat, um Business-Diagramme (Flowcharts, BPMN, Orgcharts, Swimlanes) für LLM-Analyse zugänglich zu machen.

Getestet werden zwei Dimensionen:
1. **Übersetzungsqualität** — Wie genau bildet die LLM-Übersetzung (Bild→DOT, XML→DOT) die Struktur des Originals ab?
2. **Analytisches Potenzial** — Kann ein LLM auf Basis des übersetzten DOT Prozessdefekte erkennen?

## Methodik

- **Ground Truth First**: DOT-Dateien manuell erstellt → PNG gerendert → XML exportiert → LLM-Rückübersetzung
- **4 Diagrammtypen × 3 Komplexitätsstufen** = 12 Testfälle
- **21 Übersetzungen** (Orgcharts haben kein XML-Quellformat)
- **8 geseedete Defekte** in medium/complex Cases
- **14 Defekt-Analysen** auf den übersetzten DOT-Dateien
- **Automatisierter Graph-Diff** via `compare.py` (ID-basiert + label-basiert mit Normalisierung)

## 1. Übersetzungsqualität (Label-basiert, normalisiert)

### Ergebnis-Matrix

| Typ | Case | Quelle | Node P | Node R | Edge P | Edge R | SG Match |
|-----|------|--------|--------|--------|--------|--------|----------|
| Flowchart | 01_simple | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Flowchart | 01_simple | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Flowchart | 02_medium | image | 1.000 | 1.000 | 0.917 | 1.000 | 1.000 |
| Flowchart | 02_medium | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Flowchart | 03_complex | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Flowchart | 03_complex | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| BPMN | 01_simple | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| BPMN | 01_simple | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| BPMN | 02_medium | image | 0.833 | 0.909 | 1.000 | 1.000 | 0.000 |
| BPMN | 02_medium | xml | 0.750 | 0.818 | 0.800 | 0.800 | 0.000 |
| BPMN | 03_complex | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| BPMN | 03_complex | xml | 0.846 | 0.917 | 0.429 | 0.462 | 1.000 |
| Orgchart | 01_simple | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Orgchart | 02_medium | image | 1.000 | 1.000 | 1.000 | 0.750 | 1.000 |
| Orgchart | 03_complex | image | 0.538 | 0.500 | 0.080 | 0.077 | 0.000 |
| Swimlane | 01_simple | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Swimlane | 01_simple | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Swimlane | 02_medium | image | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Swimlane | 02_medium | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Swimlane | 03_complex | image | 1.000 | 1.000 | 1.000 | 1.000 | 0.750 |
| Swimlane | 03_complex | xml | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

### Durchschnitte nach Diagrammtyp

| Typ | Ø Node Recall | Ø Edge Recall | Ø SG Match | n |
|-----|---------------|---------------|------------|---|
| Flowchart | 1.000 | 1.000 | 1.000 | 6 |
| BPMN | 0.941 | 0.877 | 0.667 | 6 |
| Orgchart | 0.833 | 0.609 | 0.667 | 3 |
| Swimlane | 1.000 | 1.000 | 0.958 | 6 |

### Durchschnitte nach Quelle

| Quelle | Ø Node Recall | Ø Edge Recall | Ø SG Match | n |
|--------|---------------|---------------|------------|---|
| Image | 0.951 | 0.923 | 0.812 | 12 |
| XML | 0.971 | 0.918 | 0.889 | 9 |

### Interpretation

**Flowcharts** und **Swimlanes** werden nahezu perfekt übersetzt — sowohl von Bild als auch von XML. Das sind die einfachsten Topologien (lineare Flows mit Verzweigungen).

**BPMN** zeigt Schwächen bei XML-Übersetzung (02_medium und 03_complex). Die Bildübersetzung ist hier oft besser, weil das LLM die visuelle Struktur direkt interpretiert statt XML-Elemente zu mappen.

**Orgcharts** brechen bei hoher Komplexität ein (03_complex: 50% Node Recall, 8% Edge Recall). Das Holding-Diagramm mit 28 Knoten und 3 Tochtergesellschaften übersteigt die Kapazität der Bildübersetzung. Edge Recall bei 02_medium liegt bei 75% — die fehlenden 25% sind Matrix-Beziehungen, die im Bild schwer erkennbar sind.

**Beobachtung: ID-basierte vs. Label-basierte Metriken**
compare.py musste um label-basierte Vergleiche erweitert werden, weil Ground Truth und LLM-Übersetzung unterschiedliche Node-IDs verwenden (z.B. `gf` vs. `susanne_engel`). Die ID-basierten Metriken waren für BPMN und Orgchart durchgehend 0.0. Zusätzlich war Label-Normalisierung (`\n` → Leerzeichen) nötig, da Ground Truth Zeilenumbrüche in Labels nutzt, die XML-Übersetzung aber nicht.

## 2. Defekt-Erkennung (Detection Rate)

### Seeded Defects — Ergebnisse

| # | Case | Defekt | from_image | from_xml | Erkannt? |
|---|------|--------|------------|----------|----------|
| 1 | Flowchart 02 | Dead End (Eskalation) | NICHT erkannt | ERKANNT | Teilweise |
| 2 | Flowchart 03 | Endlosschleife (review_check) | ERKANNT | ERKANNT | Ja |
| 3 | BPMN 02 | XOR-Gateway 1 Ausgang | ERKANNT | ERKANNT | Ja |
| 4 | BPMN 03 | Bottleneck (Teamlead-Freigabe) | ERKANNT | ERKANNT | Ja |
| 5 | Orgchart 02 | 12 Direct Reports | ERKANNT | — | Ja |
| 6 | Orgchart 03 | Verwaiste Tochter C | NICHT erkannt | — | Nein |
| 7 | Swimlane 02 | Ping-Pong (3× Bug-Fix) | ERKANNT | ERKANNT | Ja |
| 8 | Swimlane 03 | Leere Lane (Recht) | Nicht übertragbar* | ERKANNT | Teilweise |

*\*Swimlane 03 from_image: Die Bildübersetzung enthielt die Recht-Lane gar nicht, daher konnte der Defekt nicht erkannt werden.*

### Detection Rate

| Metrik | Wert |
|--------|------|
| **Gesamt (pro Analyse-Instanz)** | 11 / 14 = **78.6%** |
| **Gesamt (pro Defekt, mindestens 1 Treffer)** | 7 / 8 = **87.5%** |
| **Flowchart** | 3 / 4 = 75% |
| **BPMN** | 4 / 4 = 100% |
| **Orgchart** | 1 / 2 = 50% |
| **Swimlane** | 3 / 4 = 75% |

### Detail-Analyse der Fehlschläge

**Flowchart 02 — Dead End nicht aus Bild erkannt:**
Die Bildübersetzung hat den Escalation-Knoten korrekt mit einer ausgehenden Kante übersetzt (die im Ground Truth als Dead End geseedet war). Das LLM hat bei der Bildübersetzung den Defekt "repariert" — es hat eine logische Kante hinzugefügt, die im Ground Truth fehlte. Die XML-Übersetzung hingegen hat die Struktur exakt übernommen und der Dead End wurde korrekt erkannt.

**Orgchart 03 — Verwaiste Tochter C nicht erkannt:**
Die Bildübersetzung für diesen Case war generell sehr ungenau (50% Node Recall, 8% Edge Recall). Die Analyse identifizierte andere reale Probleme (fehlende GF in Tochter B, isolierte CFO/CTO), aber der spezifisch geseedete Defekt (Tochter C ohne Reporting-Linie) ging in der fehlerhaften Übersetzung unter.

**Swimlane 03 — Leere Lane nicht aus Bild erkannt:**
Die Bildübersetzung enthielt die Recht-Lane nicht. Da die Lane im gerenderten PNG leer war (keine Aktivitäten), hat das LLM sie bei der Bildinterpretation übersprungen. Aus der XML-Quelle wurde die leere Lane korrekt übersetzt und als Defekt erkannt.

### Bonus-Befunde (nicht geseedet, aber erkannt)

Das LLM hat über die geseedeten Defekte hinaus weitere berechtigte Prozessprobleme identifiziert:

- **Flowchart 02:** Bottleneck bei "Ticket klassifizieren", fehlender Abbruch-Pfad
- **Flowchart 03:** Unerreichbarer Knoten "Abgelehnt", fehlende Synchronisations-Semantik
- **BPMN 02:** Leere Lanes (Abteilungsleiter, Geschäftsführung), Überlastung Buchhaltung
- **BPMN 03:** Fehlendes AND-Join-Gateway, unklare Lane-Zuordnung Teamlead
- **Orgchart 02:** Fehlende Matrix-Verbindungen, verwaiste Projektleitung Beta
- **Orgchart 03:** Fehlende GF in Tochter B, isolierte CFO/CTO-Positionen
- **Swimlane 02:** Fehlende OK-Pfade, hartcodierte Schleifen statt dynamischer Zyklen
- **Swimlane 03:** Fehlende Kundenentscheidung, kein Feedback-Kanal

Diese Bonus-Befunde zeigen, dass DOT-basierte Analyse nicht nur geseedete Defekte findet, sondern echten analytischen Mehrwert liefert.

## 3. Gesamtfazit

### DOT taugt als Zwischenformat — mit Einschränkungen

**Stärken:**
- Flowcharts und Swimlanes werden exzellent übersetzt (100% Node/Edge Recall)
- Defekt-Erkennung funktioniert zuverlässig (87.5% Detection Rate)
- LLM produziert über geseedete Defekte hinaus wertvolle analytische Befunde
- XML→DOT liefert konsistent gute Ergebnisse
- Label-Normalisierung macht den Vergleich robust gegen Formatierungsunterschiede

**Schwächen:**
- Komplexe Orgcharts (>25 Knoten) übersteigen die Kapazität der Bildübersetzung
- BPMN-spezifische Semantik (Gateways, Pools) geht bei XML-Übersetzung teilweise verloren
- Bild→DOT kann Defekte "reparieren" (LLM ergänzt fehlende logische Kanten)
- Leere visuelle Elemente (Lanes ohne Aktivitäten) werden im Bild ignoriert

### Empfehlungen

1. **XML als bevorzugte Quelle** — höhere Strukturtreue als Bildübersetzung
2. **Komplexitäts-Limit** — Orgcharts/Konzernstrukturen ab ~25 Knoten manuell vorstrukturieren
3. **Dual-Translation** — Sowohl Bild als auch XML übersetzen und Ergebnisse vergleichen (Bild findet andere Dinge als XML)
4. **DOT für Analyse, nicht als Single Source of Truth** — DOT eignet sich hervorragend als Input für LLM-Analyse, ist aber kein verlustfreies Austauschformat

## 4. Bekannte Limitierungen der Studie

- **Selbst-Übersetzung**: Dasselbe LLM (Claude) hat sowohl die Ground Truth DOT-Dateien erstellt als auch die Rückübersetzung und Analyse durchgeführt. Ein Bias zugunsten eigener Konventionen ist wahrscheinlich.
- **Keine echten Quell-Diagramme**: Die PNGs und XMLs wurden aus den Ground-Truth-DOTs erzeugt, nicht aus realen Business-Dokumenten. Reale Diagramme haben mehr visuelle Noise, inkonsistente Formatierung und Tool-spezifische Artefakte.
- **Kleine Stichprobe**: 12 Testfälle × 2 Quellen = 21 Datenpunkte. Für statistische Signifikanz zu wenig.
- **Label-Matching**: Der automatische Vergleich matcht Labels textuell. Semantisch äquivalente Labels mit leicht anderer Formulierung werden als Mismatch gewertet.
- **Subgraph-Matching**: Cluster werden nur als Match gewertet, wenn Label UND enthaltene Knoten identisch sind — ein strenger Maßstab.
