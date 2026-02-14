# Design: DOT als Zwischenformat für Business-Diagramme

**Datum:** 2026-02-14
**Status:** Approved

## These

GraphViz DOT eignet sich als Zwischenformat, um grafische Business-Artefakte (Flowcharts, BPMN, Orgcharts, Swimlanes) für LLM-basierte Analyse zugänglich zu machen. DOT ist:
1. LLM-nativ lesbar (kein Vision-API nötig nach Übersetzung)
2. Menschlich validierbar (renderbar, visuell vergleichbar)
3. Kompakter als XML-Formate (5-10x weniger Tokens)
4. Diagrammtyp-übergreifend einheitlich

## Ansatz: Ground Truth First

Wir erzeugen Testdaten als DOT (= Ground Truth), rendern sie als Bilder, erzeugen XML-Varianten. Dann testen wir die Rückübersetzung und Analysefähigkeit.

## Diagrammtypen & Testcases

### Flowchart (3 Cases)
- `01_simple`: Kundenbestellung — linear, eine Entscheidung
- `02_medium`: Support-Ticket — Eskalationsstufen, Schleife. **Defekt: Dead End nach Eskalation**
- `03_complex`: Kreditantrag — parallele Prüfungen. **Defekt: Endlosschleife ohne Exit**

### BPMN (3 Cases)
- `01_simple`: Urlaubsantrag — 3 Lanes, linearer Flow
- `02_medium`: Rechnungsfreigabe — XOR/Parallel Gateway. **Defekt: XOR mit nur einem Ausgang**
- `03_complex`: Onboarding — 3 Bereiche parallel. **Defekt: Bottleneck, alles durch eine Person**

### Orgchart (3 Cases)
- `01_simple`: Kleine Firma — GF + 3 Abteilungen + Mitarbeiter
- `02_medium`: Matrixorganisation — Doppel-Reporting. **Defekt: 12 Direct Reports**
- `03_complex`: Konzernstruktur — Holding + Töchter. **Defekt: Verwaiste Einheit**

### Swimlane (3 Cases)
- `01_simple`: Bestellprozess — 3 Lanes
- `02_medium`: Softwarerelease — 4 Lanes, Rückschleifen. **Defekt: Ping-Pong Dev↔QA**
- `03_complex`: Reklamation — 4 Lanes, Eskalation. **Defekt: Lane ohne Aktivitäten**

## DOT-Limitationen (bewusst akzeptiert)

- BPMN-Gateways → `shape=diamond` mit Label (XOR/AND/OR)
- Swimlanes → `subgraph cluster_*` + `rank=same` (kein echtes Lane-Konzept)
- Orgchart hat kein Standard-XML → nur Bild-Pfad, kein XML-Vergleich

## Input-Formate

| Typ | Bild → DOT | XML → DOT | XML-Format |
|-----|-----------|-----------|------------|
| Flowchart | Ja | Ja | draw.io XML |
| BPMN | Ja | Ja | BPMN 2.0 XML |
| Orgchart | Ja | Nein | — |
| Swimlane | Ja | Ja | draw.io XML |

**Gesamt: 21 Übersetzungen, 8 Defekt-Analysen**

## Evaluation

### Übersetzungsqualität (automatisiert via compare.py)

| Metrik | Beschreibung |
|--------|-------------|
| Node Recall | Gefundene / erwartete Knoten |
| Node Precision | Korrekte / erzeugte Knoten |
| Edge Recall | Gefundene / erwartete Kanten |
| Edge Precision | Korrekte / erzeugte Kanten |
| Subgraph Match | Korrekte / erwartete Cluster |
| Semantic Fidelity | Manuell, 1-5 (nur bei Ausreißern) |

### Analysefähigkeit (semi-automatisiert)

| Bewertung | Bedeutung |
|-----------|-----------|
| Found | Defekt exakt identifiziert |
| Partial | Problem-Gebiet erkannt, unscharf |
| Missed | Nicht erkannt |
| False Positive | Falsches Problem gemeldet |

Detection Rate = Found / Seeded Defects

### Ergebnis-Matrix

```
                    Bild → DOT    XML → DOT
Flowchart              ?              ?
BPMN                   ?              ?
Orgchart               ?              —
Swimlane               ?              ?
```

## Prompts (standardisiert, in prompts/)

1. `translate_image.md` — Bild → DOT (nur Struktur, Labels exakt übernehmen)
2. `translate_xml.md` — XML → DOT (Layout-Metadaten ignorieren, nur Topologie)
3. `analyze_process.md` — DOT → Prozessanalyse (Strukturelle, organisatorische, Effizienz-Probleme)

## Ausführungsflow

1. **Phase 1 — Testdaten:** Ground Truth DOT schreiben, rendern, XML erzeugen, Expected Findings dokumentieren
2. **Phase 2 — Übersetzungen:** LLM übersetzt Bilder und XMLs zu DOT (frischer Kontext pro Case)
3. **Phase 3 — Analyse:** LLM analysiert DOT-Ergebnisse auf Defekte
4. **Phase 4 — Evaluation:** compare.py + Detection Rate berechnen
5. **Phase 5 — Validierung:** Mensch prüft Ausreißer, bewertet Semantic Fidelity, schreibt Fazit
