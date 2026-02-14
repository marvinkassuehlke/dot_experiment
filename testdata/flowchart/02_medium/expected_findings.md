# Expected Findings — Support-Ticket (02_medium)

## Seeded Defect
- **Typ:** Dead End
- **Location:** Node "Eskalation an Entwicklung" (escalate)
- **Beschreibung:** Der Knoten "escalate" hat keine ausgehende Kante. Tickets mit Schweregrad "hoch" werden eskaliert, aber der Prozess endet dort ohne Auflösung.
- **Erwartete Erkennung:** LLM sollte identifizieren, dass "escalate" ein Dead End ist — kein Pfad zurück zum Hauptflow oder zu einem End-Knoten.
