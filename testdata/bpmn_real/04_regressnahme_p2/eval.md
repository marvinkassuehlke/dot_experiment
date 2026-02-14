# Evaluation: 04_regressnahme_p2 (Teilnehmer)

## Übersetzung (XML → DOT)

| Metrik | Wert |
|--------|------|
| Nodes (XML → DOT) | ~17 → 21* |
| Edges (XML → DOT) | ~19 → 19 |
| Pools/Lanes | 1 Pool "Sachbearbeiter" (korrekt) |
| Rendert fehlerfrei | Ja |

*4 zusätzliche rote Placeholder-Knoten für fehlende sourceRef/targetRef in XML.

## Vergleich mit Referenzlösung (Label-basiert)

| Metrik | Wert |
|--------|------|
| Node Recall | 6.2% |
| Edge Recall | 0.0% |
| Subgraph Match | 0.0% |

Maximale Divergenz — defektes XML + völlig andere Labels.

## Analyse

| Findings | Korrekt | Accuracy |
|----------|---------|----------|
| 5 Strukturell | 5/5 | 100% |
| 2 Organisatorisch | 2/2 | 100% |
| 3 Effizienz | 3/3 | 100% |
| **Gesamt** | **10/10** | **100%** |

## Highlight

Herausragend: 4 defekte XML-Referenzen gefunden UND deren Konsequenzen (Dead Ends, unerreichbare Knoten) abgeleitet. Die wahrscheinlich beabsichtigte Struktur wurde aus Waypoint-Koordinaten rekonstruiert. Das DOT visualisiert defekte Flows als rote Placeholder-Knoten — konstruktive Fehlerbehandlung.
