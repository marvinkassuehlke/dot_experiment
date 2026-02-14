# Evaluation: 03_regressnahme_p1 (Teilnehmer)

## Übersetzung (XML → DOT)

| Metrik | Wert |
|--------|------|
| Nodes (XML → DOT) | 16 → 16 |
| Edges (XML → DOT) | 18 → 18 |
| Pools/Lanes | Keine (korrekt — Quelle hatte auch keine) |
| Rendert fehlerfrei | Ja |

## Vergleich mit Referenzlösung (Label-basiert)

| Metrik | Wert |
|--------|------|
| Node Recall | 31.2% |
| Edge Recall | 11.1% |
| Subgraph Match | 0.0% |

Niedrige Werte erwartet — andere Namenskonventionen, keine Pools/Lanes.

## Analyse

| Findings | Korrekt | Accuracy |
|----------|---------|----------|
| 4 Strukturell | 4/4 | 100% |
| 2 Organisatorisch | 2/2 | 100% |
| 4 Effizienz | 4/4 | 100% |
| **Gesamt** | **10/10** | **100%** |

## Highlight

Fehlende Lanes/Pools (Finding 2.1): Grundlegender Modellierungsmangel für eine Trainingsübung. End Event mit Aktivitäts-Semantik (1.2) zeigt BPMN-Best-Practice-Wissen.
