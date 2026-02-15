Du erhältst ein Prozessdiagramm als XML (BPMN 2.0 oder draw.io Format). Übersetze die Struktur in Mermaid-Syntax.

Regeln:
- Ignoriere Layout-Metadaten (Koordinaten, Größen, Farben, Positionen)
- Extrahiere nur Topologie: Knoten, Kanten, Gruppierungen
- Diagrammtyp: `flowchart TD` (top-down) oder `flowchart LR` (left-right)
- Shapes: `["Label"]` = Task/Aktivität, `{Label}` = Gateway/Entscheidung, `(["Label"])` = Start/End Event
- `subgraph` für Pools, Lanes, Gruppierungen — mit Label in Anführungszeichen
- Edge-Labels mit `-->|Label|` Syntax
- `-->` für Sequence Flows, `-.->` für Message Flows
- Labels exakt aus dem XML übernehmen
- Gateway-Typ im Label vermerken, z.B. `{AND (Split)}`, `{XOR: Sonderversand?}`, `{OR (Join)}`
- Nur valides Mermaid ausgeben, keine Erklärung, kein Markdown-Codeblock
