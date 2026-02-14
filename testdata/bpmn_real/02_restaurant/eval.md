# Evaluation: 02_restaurant (Musterlösung)

## Übersetzung (XML → DOT)

| Metrik | Wert |
|--------|------|
| Nodes (XML → DOT) | 30 → 30 |
| Edges (XML → DOT) | 28 Seq + 10 MF → 34 + 10 MF |
| Pools | 3 (Gast, Angestellter, Koch) |
| Message Flows | 10 (dashed, blue, labeled) |
| Rendert fehlerfrei | Ja |

## Analyse

| Findings | Korrekt | Accuracy |
|----------|---------|----------|
| 4 Strukturell | 4/4 | 100% |
| 3 Organisatorisch | 3/3 | 100% |
| 4 Effizienz | 4/4 | 100% |
| **Gesamt** | **11/11** | **100%** |

## Highlight

Endlosschleife (Finding 1.1): Timer → "Kunden ausrufen" → EventBasedGateway → Timer bildet eine Schleife ohne Exit-Bedingung. Wenn der Kunde nie erscheint, dreht die Schleife ewig. Koch-Information erst nach Pieper-Übergabe (3.4) ist ein konkreter Optimierungsvorschlag.
