Du erhältst einen Geschäftsprozess als Mermaid-Diagramm. Analysiere ihn auf Prozessdefekte.

## Analysekategorien

### 1. Strukturelle Probleme
- Dead Ends (Knoten ohne ausgehende Kante, die kein End-Event sind)
- Endlosschleifen (Zyklen ohne Exit-Bedingung)
- Fehlende Pfade (Entscheidungen mit weniger Ausgängen als erwartet)
- Unerreichbare Knoten
- Gateway-Typ-Fehler (AND-Split ohne AND-Join, XOR statt AND, etc.)
- Fehlende oder falsche Event-Typen
- Message Flows ohne Empfänger

### 2. Organisatorische Probleme
- Bottlenecks (ein Akteur/Lane, durch den zu viele Pfade laufen)
- Unklare Verantwortlichkeiten (Subgraphs ohne Aktivitäten oder ohne Label)
- Überlastung (zu viele Aufgaben in einer Lane)
- Unterauslastung (Lane mit nur einer optionalen Aufgabe)

### 3. Effizienz-Probleme
- Unnötige Schleifen oder Redundanzen
- Ping-Pong (Aufgaben die zwischen Akteuren hin- und herwandern)
- Sequenzielle Schritte, die parallelisiert werden könnten
- Fehlende Automatisierungspotenziale

## Output-Format

Für jedes Finding:
- **ID**: F1, F2, F3, ...
- **Kategorie**: structural | organizational | efficiency
- **Schwere**: high | medium | low
- **Betroffene Elemente**: Konkrete Node-IDs oder Labels aus dem Mermaid
- **Titel**: Einzeilige Zusammenfassung
- **Beschreibung**: 2-3 Sätze mit Erklärung und Konsequenz

Wenn keine Probleme gefunden: explizit sagen "Keine Probleme identifiziert".
