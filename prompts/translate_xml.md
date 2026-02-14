Du erhältst ein Prozessdiagramm als XML (BPMN 2.0 oder draw.io Format). Übersetze die Struktur in GraphViz DOT-Syntax.

Regeln:
- Ignoriere Layout-Metadaten (Koordinaten, Größen, Farben, Positionen)
- Extrahiere nur Topologie: Knoten, Kanten, Gruppierungen
- Subgraphs/Cluster für Pools, Lanes, Gruppierungen
- Semantische Shapes: diamond=Entscheidung/Gateway, box=Aktivität/Task, ellipse=Start/End Event
- Labels exakt aus dem XML übernehmen
- Pfeilrichtung aus sequenceFlow/Verbindungen ableiten
- Nur valides DOT ausgeben, keine Erklärung, kein Markdown-Codeblock
