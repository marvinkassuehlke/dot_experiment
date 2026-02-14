# Evaluation: 01_warenversand (Musterlösung)

## Übersetzung (XML → DOT)

| Metrik | Wert |
|--------|------|
| Nodes (XML → DOT) | 15 → 15 |
| Edges (XML → DOT) | 17 → 17 |
| Pools/Lanes | 1 Pool, 3 Lanes (korrekt) |
| Rendert fehlerfrei | Ja |

## Analyse

| Findings | Korrekt | Accuracy |
|----------|---------|----------|
| 6 Strukturell | 2/2 | 100% |
| 6 Organisatorisch | 3/3 | 100% |
| 6 Effizienz | 3/3 | 100% |
| **Gesamt** | **6/6** | **100%** |

## Highlight

AND-Split ohne AND-Join (Finding 1.1): Der Parallel Gateway splittet in "Versandart klären" und "Ware verpacken", aber der XOR-Gateway am Ende synchronisiert die Pfade nicht korrekt. Genau der Fehler, den diese Übungsaufgabe provozieren soll.
