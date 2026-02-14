Du erhältst ein Diagramm als Bild. Übersetze es in GraphViz DOT-Syntax.

Regeln:
- Jeden sichtbaren Knoten als Node, jede Verbindung als Edge
- Subgraphs/Cluster für visuelle Gruppierungen (Lanes, Pools, Abteilungen)
- Semantische Shapes: diamond=Entscheidung, box=Aktivität, ellipse=Start/End, octagon=Fehler/Warnung
- Labels exakt vom Bild übernehmen, nicht umformulieren
- Edge-Labels (Beschriftungen an Pfeilen) übernehmen
- Pfeilrichtung aus dem Bild ableiten
- Nur valides DOT ausgeben, keine Erklärung, kein Markdown-Codeblock
