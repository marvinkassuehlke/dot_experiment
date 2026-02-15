Du erhältst ein Prozessdiagramm als Bild. Übersetze es in Mermaid-Syntax.

Regeln:
- Diagrammtyp: `flowchart TD` (top-down) oder `flowchart LR` (left-right), je nach Layout des Originals
- Jeden sichtbaren Knoten als Node mit eindeutiger ID und Label in Anführungszeichen
- Shapes: `["Label"]` = Aktivität/Task, `{"Label"}` = Entscheidung/Gateway, `(["Label"])` = Start/End Event, `[/"Label"/]` = Daten/Dokument
- Jede Verbindung als Edge mit `-->` (Sequence Flow) oder `-.->` (Message Flow / gestrichelt)
- Edge-Labels mit `-->|"Label"|` Syntax
- `subgraph` für Pools, Lanes, Gruppierungen — mit Label in Anführungszeichen
- Labels exakt vom Bild übernehmen, nicht umformulieren
- Nur valides Mermaid ausgeben, keine Erklärung, kein Markdown-Codeblock

Beispiel-Syntax:

flowchart TD
    subgraph pool1["Gast"]
        A(["Hunger festgestellt"]) --> B["Restaurant betreten"]
        B --> C["Gericht auswählen"]
        C --> D{"Gericht verfügbar?"}
        D -->|"Ja"| E["Bestellen"]
        D -->|"Nein"| C
    end
