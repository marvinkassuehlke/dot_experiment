# Evaluation: 05_regressnahme_p3 (Teilnehmer)

## Übersetzung (XML → DOT)

| Metrik | Wert |
|--------|------|
| Nodes (XML → DOT) | 16 → 16 |
| Edges (XML → DOT) | 16 → 16 |
| Pools/Lanes | 1 Pool "Versicherung", 2 Lanes (Regressstelle, Inkasso) |
| Rendert fehlerfrei | Ja |

## Vergleich mit Referenzlösung (Label-basiert)

| Metrik | Wert |
|--------|------|
| Node Recall | 12.5% |
| Edge Recall | 0.0% |
| Subgraph Match | 0.0% |

Niedrige Werte — andere Tool-Konventionen (Signavio vs. Camunda).

## Analyse

| Findings | Korrekt | Accuracy |
|----------|---------|----------|
| 5 Strukturell | 5/5 | 100% |
| 3 Organisatorisch | 3/3 | 100% |
| 4 Effizienz | 4/4 | 100% |
| **Gesamt** | **12/12** | **100%** |

## Highlight

BPMN-Syntaxfehler erkannt (Finding 1.2): Intermediate Catch Event mit 3 Ausgängen statt Event-Based Gateway. Im XML enthält das Event gleichzeitig cancelEventDefinition und terminateEventDefinition — semantisch ungültig und in einer Process Engine nicht ausführbar.
