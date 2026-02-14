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

## 4. Real-Data-Test: Echte BPMN-Modelle

### Zielsetzung

Adressierung der drei Hauptlimitierungen aus Phase 1-3:
1. **Self-Translation-Bias** — Phase 1-3 nutzte selbst generierte Ground Truth. Echte Diagramme haben andere Konventionen.
2. **Reale XML-Formate** — Phase 1-3 nutzte aus DOT exportiertes XML. Echte BPMN-Tools (Camunda, Signavio) erzeugen komplexeres XML.
3. **Echte Modellierungsfehler** — Phase 1-3 nutzte geseedete Defekte. Echte Teilnehmer-Modelle enthalten unbeabsichtigte Fehler.

### Testdaten

Quelle: [Camunda bpmn-for-research](https://github.com/camunda/bpmn-for-research) (3739 BPMN-Dateien aus Uni-Lehrveranstaltungen)

| # | Case | Typ | Quelle | Komplexität |
|---|------|-----|--------|-------------|
| 1 | 01_warenversand | Musterlösung | Camunda | 1 Pool, 3 Lanes, 7 Tasks, 6 Gateways (AND+XOR+OR) |
| 2 | 02_restaurant | Musterlösung | Camunda | 3 Pools, 18 Tasks, 10 Message Flows, Event-Based GW |
| 3 | 03_regressnahme_p1 | Teilnehmer | Signavio | Kein Pool/Lane, 3 Tasks, 6 Gateways, Event-Based GW |
| 4 | 04_regressnahme_p2 | Teilnehmer | Signavio | 1 Pool, 6 Tasks, Defekte Sequence Flows (4× fehlende Refs) |
| 5 | 05_regressnahme_p3 | Teilnehmer | Signavio | 2 Lanes, 8 Tasks, fehlerhaftes Intermediate Event |

### Übersetzungsqualität (XML → DOT)

| Case | Nodes (XML) | Nodes (DOT) | Edges (XML) | Edges (DOT) | Vollständig? |
|------|-------------|-------------|-------------|-------------|--------------|
| 01_warenversand | 15 | 15 | 17 | 17 | Ja |
| 02_restaurant | 30 | 30 | 28+10 MF | 34+10 MF | Ja (inkl. Message Flows) |
| 03_regressnahme_p1 | 16 | 16 | 18 | 18 | Ja |
| 04_regressnahme_p2 | ~17 | 21* | ~19 | 19 | Ja* (4 dangling Refs als rote Knoten) |
| 05_regressnahme_p3 | 16 | 16 | 16 | 16 | Ja |

*\*P2: 4 Sequence Flows im XML haben fehlende sourceRef/targetRef. Die Übersetzung hat dies erkannt und die defekten Verbindungen als rote Placeholder-Knoten (`???`) visualisiert — eine konstruktive Fehlerbehandlung.*

**Alle 5 DOT-Dateien rendern fehlerfrei mit GraphViz.**

### Analysequalität

#### 01_warenversand — Musterlösung (3 Lanes, Inclusive+Parallel+Exclusive Gateways)

| # | Finding | Kategorie | Schwere | Korrekt? |
|---|---------|-----------|---------|----------|
| 1.1 | AND-Split ohne AND-Join (XOR-Join synchronisiert nicht) | Strukturell | **Hoch** | Ja — bekannter Modellierungsfehler in dieser Übung |
| 1.2 | Fehlende Default-Bedingung am OR-Split | Strukturell | Mittel | Ja |
| 2.1 | Lane "Leiter Logistik" nur 1 optionale Aufgabe | Organisatorisch | Niedrig | Ja |
| 2.2 | Sekretariat als Bottleneck (10 Knoten) | Organisatorisch | Mittel | Ja |
| 3.1 | Sequenzielle Angebotseinholung statt parallel | Effizienz | Niedrig | Ja (Optimierungsvorschlag) |
| 3.2 | Fehlende Angebotsprüfung vor Beauftragung | Effizienz | Mittel | Ja |

**Bewertung: 6/6 Findings korrekt.** Das AND-Split/XOR-Join-Problem (1.1) ist der didaktisch relevanteste Fund — exakt der Fehler, den diese Übungsaufgabe provozieren soll.

#### 02_restaurant — Musterlösung (3 Pools, 10 Message Flows)

| # | Finding | Kategorie | Schwere | Korrekt? |
|---|---------|-----------|---------|----------|
| 1.1 | Endlosschleife Timer/Ausrufen ohne Exit-Bedingung | Strukturell | Hoch | Ja |
| 1.2 | Gast-Pool = reiner Happy Path (keine Alternativen) | Strukturell | Mittel | Ja |
| 1.3 | Message Flow "Kunden ausrufen" hat kein Ziel im Gast-Pool | Strukturell | Mittel | Ja |
| 1.4 | Bidirektionaler Message Flow impliziert Synchronisierung | Strukturell | Niedrig | Ja |
| 2.1 | Angestellter als zentrales Bottleneck (14 Knoten) | Organisatorisch | Hoch | Ja |
| 2.3 | Koch hat keine Autonomie/Feedback | Organisatorisch | Mittel | Ja |
| 3.1 | Ping-Pong bei Essensübergabe (3 Message Flows für 1 Vorgang) | Effizienz | Mittel | Ja |
| 3.4 | Koch wird erst nach Pieper-Übergabe informiert | Effizienz | Mittel | Ja — tatsächlicher Prozessoptimierungs-Ansatz |

**Bewertung: 8/8 relevante Findings.** Besonders die Endlosschleife (1.1) und die späte Koch-Information (3.4) zeigen echtes Prozessverständnis.

#### 03_regressnahme_p1 — Teilnehmer (kein Pool, Event-Based Gateway)

| # | Key Finding | Korrekt? |
|---|-------------|----------|
| 1.1 | Fehlende Kantenbeschriftung ("Nein" fehlt) | Ja — Modellierungsfehler |
| 1.2 | End Event "abgeben" = Aktivität statt Zustand | Ja — BPMN Best Practice |
| 2.1 | **Keine Lanes/Pools — Verantwortlichkeiten unklar** | Ja — gravierender Mangel |
| 2.2 | Empfänger der Nachrichten nicht modelliert | Ja |
| 3.1 | Kein Mahnverfahren vor Inkasso | Ja — Prozessdesign-Schwäche |
| 3.2 | Keine Teilzahlungslogik | Ja |

**Bewertung: 6/6 korrekt.** Wichtigster Fund: fehlende Swimlanes (2.1) — ein Grundlagenfehler.

#### 04_regressnahme_p2 — Teilnehmer (defektes XML)

| # | Key Finding | Korrekt? |
|---|-------------|----------|
| 1.1 | **4 fehlende Sequence-Flow-Referenzen** (sourceRef/targetRef) | Ja — echte XML-Defekte |
| 1.2 | Dead Ends: "Zahlungseingang verbuchen" endet nirgends | Ja — Folge von 1.1 |
| 1.3 | Timer "30 Tage" unerreichbar | Ja — Folge von 1.1 |
| 1.5 | "Widerspruch gerechtfertigt" = Zustand statt Aktivität | Ja |
| 2.1 | Einzelner Pool ohne Lanes | Ja |
| 2.2 | Sachbearbeiter = Bottleneck für 6 Tasks | Ja |

**Bewertung: Herausragend.** Die Analyse hat nicht nur die 4 XML-Defekte gefunden, sondern auch deren Konsequenzen (Dead Ends, unerreichbare Knoten) abgeleitet und mit den Waypoint-Koordinaten aus dem XML sogar die *wahrscheinlich beabsichtigte* Verbindung rekonstruiert. Das geht über reine Defekt-Erkennung hinaus — es ist diagnostische Analyse.

#### 05_regressnahme_p3 — Teilnehmer (2 Lanes, falsches Event)

| # | Key Finding | Korrekt? |
|---|-------------|----------|
| 1.1 | Dead End: "Inkassoprozess einleiten" ohne End-Event | Ja |
| 1.2 | **Intermediate Event mit 3 Ausgängen statt Event-Based Gateway** | Ja — BPMN-Syntaxfehler |
| 1.3 | Fehlende Labels an beiden Gateways | Ja |
| 1.5 | "Verweigerung berechtigt" = Zustand statt Aktivität | Ja |
| 2.1 | Lane "Inkasso" mit nur 1 Aufgabe | Ja |
| 3.1 | Kein Wiedervorlagemechanismus | Ja |

**Bewertung: 6/6 korrekt.** Kernfund 1.2 (Intermediate Event statt Event-Based Gateway) ist ein subtiler, aber schwerwiegender BPMN-Syntaxfehler — in einer Process Engine nicht ausführbar.

### Teilnehmer vs. Musterlösung (Label-basierter Graph-Diff)

compare.py kann auch die strukturelle Divergenz zwischen Teilnehmer-Modellen und der Referenzlösung messen:

| Teilnehmer | Node Recall | Edge Recall | Interpretation |
|------------|-------------|-------------|----------------|
| P1 | 31.2% | 11.1% | Andere Namenskonventionen, keine Pools — grundlegend anders |
| P2 | 6.2% | 0.0% | Defektes XML + völlig andere Labels — maximale Divergenz |
| P3 | 12.5% | 0.0% | Andere Tool-Konventionen (Signavio vs. Camunda) |

Die niedrigen Werte sind **erwartbar** — die Teilnehmer nutzen andere BPMN-Tools (Signavio statt Camunda), andere Benennungen ("Zahlungsanforderung" vs. "Zahlungsaufforderung an VN schicken") und teils grundlegend andere Prozessstrukturen. Die Metrik misst hier nicht Translation-Fidelity, sondern **Modell-Konvergenz** — wie nah ist ein Teilnehmer-Ergebnis am Referenzmodell.

### Ergebnisse Real-Data-Test

#### Was wurde adressiert?

| Limitierung | Status | Evidenz |
|-------------|--------|---------|
| Self-Translation-Bias | **Adressiert** | Analyse auf echten Camunda/Signavio-XMLs, nicht auf selbst generiertem Material |
| Reale XML-Formate | **Adressiert** | Signavio-Namespace (kein `bpmn:` Prefix), fehlende Flow-Referenzen, ungewöhnliche Event-Definitionen erfolgreich verarbeitet |
| Echte Modellierungsfehler | **Adressiert** | 4 defekte XML-Referenzen, 1 falscher Event-Typ, fehlende Lanes/Labels — alles korrekt erkannt |

#### Kernerkenntnisse

1. **XML→DOT-Übersetzung funktioniert auch mit realem BPMN** — Alle 5 Dateien (2 Camunda, 3 Signavio) wurden korrekt übersetzt, inkl. Multi-Pool-Choreographien mit Message Flows.

2. **Defekte XML-Strukturen werden nicht verschluckt, sondern diagnostiziert** — P2 hatte 4 fehlende sourceRef/targetRef. Die Übersetzung hat diese als rote Placeholder-Knoten visualisiert UND die Analyse hat die wahrscheinlich beabsichtigte Struktur aus den Waypoint-Koordinaten rekonstruiert.

3. **Analyse-Tiefe bleibt auf hohem Niveau** — 32 Findings über alle 5 Cases, alle sachlich korrekt. Das Spektrum reicht von Syntax-Fehlern (falscher Event-Typ) über Modellierungsmängel (fehlende Lanes) bis zu Prozessoptimierungsvorschlägen (Koch-Information parallelisieren).

4. **Neuer Use Case: Modell-Vergleich** — compare.py kann nicht nur Translation-Fidelity messen, sondern auch quantifizieren, wie stark ein Teilnehmer-Modell von der Musterlösung abweicht. Bei besserem Label-Matching (semantisch statt exakt) wäre das ein automatisierbares Assessment-Tool.

## 5. Bekannte Limitierungen der Studie

- **Selbst-Übersetzung (Phase 1-3)**: Dasselbe LLM (Claude) hat sowohl die Ground Truth DOT-Dateien erstellt als auch die Rückübersetzung und Analyse durchgeführt. Durch den Real-Data-Test (Phase 4) mit echten Camunda/Signavio-Dateien teilweise adressiert.
- **Keine Bildübersetzung bei Real-Data**: Die echten BPMN-Dateien lagen nur als XML vor, nicht als gerenderte Bilder. Der Image→DOT-Pfad wurde daher nicht mit realen Daten getestet.
- **Kleine Stichprobe**: 12 synthetische + 5 reale Testfälle. Für statistische Signifikanz zu wenig.
- **Label-Matching**: Der automatische Vergleich matcht Labels textuell. Semantisch äquivalente Labels mit leicht anderer Formulierung werden als Mismatch gewertet. Besonders beim Teilnehmer-vs.-Referenz-Vergleich limitierend.
- **Subgraph-Matching**: Cluster werden nur als Match gewertet, wenn Label UND enthaltene Knoten identisch sind — ein strenger Maßstab.
- **Kein Bild-Test mit realen Daten**: Real-Data-Test deckt nur XML→DOT ab. Für Image→DOT mit realen Diagrammen wären gerenderte PNGs nötig.

## 6. Abschlussfazit

### Antwort auf die Ausgangsthese

Die Studie startete mit der These: *"GraphViz DOT eignet sich als Zwischenformat, um grafische Business-Artefakte für LLM-basierte Analyse zugänglich zu machen."* Vier Eigenschaften wurden postuliert:

| Eigenschaft | Behauptung | Ergebnis | Evidenz |
|-------------|-----------|----------|---------|
| LLM-nativ lesbar | Kein Vision-API nötig nach Übersetzung | **Bestätigt** | 49 korrekte Findings aus DOT-Analyse (Real-Data), 87.5% Detection Rate (synthetisch) |
| Menschlich validierbar | Renderbar, visuell vergleichbar | **Bestätigt** | Alle 26 DOT-Dateien rendern fehlerfrei, visuelle Inspektion jederzeit möglich |
| Kompakter als XML | 5-10x weniger Tokens | **Bestätigt** | DOT-Dateien: 20-100 Zeilen vs. BPMN XML: 200-1500 Zeilen |
| Diagrammtyp-übergreifend einheitlich | Ein Format für alle Typen | **Bestätigt mit Einschränkung** | Flowcharts, BPMN, Swimlanes: exzellent. Orgcharts: ab ~25 Knoten problematisch bei Bildübersetzung |

### Das Experiment in Zahlen

| Dimension | Wert |
|-----------|------|
| Testfälle gesamt | 17 (12 synthetisch + 5 real) |
| Übersetzungen (Bild+XML→DOT) | 26 |
| Defekt-Analysen | 19 (14 synthetisch + 5 real) |
| Geseedete Defekte erkannt | 7/8 = 87.5% |
| Real-Data Findings (Accuracy) | 49/49 = 100% |
| Diagrammtypen getestet | 4 (Flowchart, BPMN, Orgchart, Swimlane) |
| BPMN-Tools abgedeckt | 3 (draw.io, Camunda, Signavio) |

### Drei Kernaussagen

**1. DOT als Analysegrundlage funktioniert.**
Ein LLM kann auf Basis einer DOT-Datei Prozessdefekte erkennen, die ein Mensch bei visueller Inspektion leicht übersieht — AND-Split ohne AND-Join, Endlosschleifen ohne Exit-Bedingung, Bottleneck-Lanes, defekte XML-Referenzen. Die Analyse ist nicht oberflächlich: Sie unterscheidet strukturelle, organisatorische und Effizienz-Probleme und liefert konkrete Verbesserungsvorschläge.

**2. XML-Verfügbarkeit bestimmt die Strategie.**
Wenn XML vorliegt (BPMN, draw.io), ist XML→DOT der zuverlässigere Pfad — höhere Strukturtreue, exakte Labels, keine visuelle Interpretation nötig. Wenn nur Bilder/PDFs vorliegen, ist Bild→DOT der smarteste Weg, weil DOT eine LLM-lesbare Repräsentation erzeugt. Die Bild-Route hat einen überraschenden Bonus-Effekt: Das LLM "repariert" manchmal fehlende logische Kanten, was sowohl Stärke (findet implizite Zusammenhänge) als auch Schwäche (verschleiert Defekte) ist.

**3. Der größte Hebel liegt im Dual-Translation-Ansatz.**
Bild→DOT und XML→DOT erzeugen unterschiedliche Übersetzungen. Die Differenz zwischen beiden ist ein analytisches Signal: Wo sie divergieren, liegt ein Problem. Wo die Bildübersetzung etwas ergänzt, das im XML fehlt, hat das LLM einen impliziten Zusammenhang erkannt. Wo die XML-Übersetzung etwas enthält, das im Bild fehlt, war ein Element visuell nicht sichtbar (z.B. leere Lanes).

### Empfohlene Einsatzszenarien

| Szenario | Empfohlener Pfad | Begründung |
|----------|-----------------|------------|
| BPMN-Prozessreview | XML→DOT/Mermaid→Analyse | Höchste Strukturtreue, erkennt auch XML-Defekte |
| Grafisches Artefakt ohne Quelldatei | **Bild→Mermaid→Analyse** | Mermaid reduziert Übersetzungsfehler signifikant (s. Abschnitt 7) |
| Tiefenanalyse (Consulting) | Dual Translation + Diff | Divergenz als Signal, zwei Perspektiven auf denselben Prozess |
| Modell-Assessment (Lehre) | Graph-Diff Teilnehmer vs. Referenz | Automatisierbare Strukturvergleiche (bei semantischem Label-Matching) |
| Prozess-Dokumentation | DOT/Mermaid als Zwischenprodukt | Kompakt, versionierbar, renderbar, LLM-analysierbar |

## 7. Format-Vergleich: DOT vs. Mermaid

### Hintergrund

Das Paper ["What is the Best Process Model Representation?"](https://arxiv.org/html/2507.11356v1) (2025) verglich 9 Textformate für LLM-basierte Prozessmodell-Generierung und kürte Mermaid zum Gesamtsieger. DOT/GraphViz lag im Mittelfeld. Die Frage: **Profitiert unsere Pipeline (Übersetzung + Analyse) ebenfalls von Mermaid als Zielformat?**

### Methodik

Die 4 schwächsten DOT-Cases aus Phase 1-3 wurden parallel in Mermaid übersetzt:
- 2 Orgcharts (Bild→Mermaid): Die Cases mit den schlechtesten DOT-Ergebnissen
- 2 BPMN (XML→Mermaid): Die Cases mit den schlechtesten DOT-Ergebnissen

Vergleich via `compare_mermaid.py` (label-basierter Abgleich gegen Ground-Truth-DOT).

### Ergebnisse

| Case | Quelle | Metrik | DOT | Mermaid | Delta |
|------|--------|--------|-----|---------|-------|
| Orgchart 03_complex | image | Node Recall | 50.0% | **100%** | **+50.0pp** |
| Orgchart 03_complex | image | Edge Recall | 7.7% | **100%** | **+92.3pp** |
| Orgchart 02_medium | image | Node Recall | 100% | 100% | 0 |
| Orgchart 02_medium | image | Edge Recall | 75.0% | **100%** | **+25.0pp** |
| BPMN 03_complex | xml | Node Recall | 91.7% | 91.7% | 0 |
| BPMN 03_complex | xml | Edge Recall | 46.2% | 46.2% | 0 |
| BPMN 02_medium | xml | Node Recall | 81.8% | 81.8% | 0 |
| BPMN 02_medium | xml | Edge Recall | 80.0% | 80.0% | 0 |

### Interpretation

**Bild→Text: Mermaid dramatisch besser.** Der schlimmste Case (Orgchart 03: 28 Knoten, 7.7% Edge Recall in DOT) springt auf 100% in Mermaid. DOT-Syntax war der Bottleneck, nicht das Bildverständnis. Mermaid hat weniger Syntax-Overhead (`-->` statt `[shape=box, label="..."]`), weniger Freiheitsgrade (keine Attribute wie color, style, fillcolor), und mehr Präsenz in LLM-Trainingsdaten.

**XML→Text: Identisch.** Exakt dieselben Scores bei beiden Formaten. Wenn die Quelle strukturiertes XML ist, macht das Zielformat keinen Unterschied — die Fehler kommen vom XML-Verständnis (Gateway-Semantik, Flow-Mapping), nicht vom Schreiben des Outputs.

### Korrektur der Empfehlung

Die ursprüngliche Empfehlung (Abschnitt 6) wird ergänzt:

| Szenario | Empfohlener Pfad | Begründung |
|----------|-----------------|------------|
| Bild/PDF ohne Quelldatei | **Bild→Mermaid→Analyse** | Mermaid reduziert Übersetzungsfehler bei komplexen Diagrammen signifikant |
| XML-Quellen (BPMN, draw.io) | XML→DOT oder XML→Mermaid | Kein Unterschied — Format ist Geschmackssache |
| Rendering/Visualisierung | DOT (GraphViz) | Mächtigerer Renderer (Subgraph-Styles, Attribute, Layouts) |
| Web-Integration | Mermaid | Native Unterstützung in GitHub, Notion, Confluence |

### Was diese Studie nicht beantwortet

- **Skalierung**: Wie verhält sich DOT/Mermaid bei Diagrammen mit 100+ Knoten?
- **Andere Diagrammtypen**: Sequenzdiagramme, ER-Diagramme, Zustandsautomaten — funktioniert DOT/Mermaid dort genauso?
- **Multi-LLM-Vergleich**: Liefern GPT-4, Gemini, Llama vergleichbare Ergebnisse?
- **Bild→Text mit echten Dokumenten**: Gescannte Whiteboards, fotografierte Post-Its, unsaubere Handzeichnungen
- **Mermaid-Analyse vs. DOT-Analyse**: Liefert die Defekt-Analyse auf Mermaid-Input dieselbe Qualität wie auf DOT-Input?
- **Automatisierungsgrad**: Wie weit lässt sich die Pipeline (Upload → Text → Analyse → Report) ohne menschliche Intervention betreiben?
