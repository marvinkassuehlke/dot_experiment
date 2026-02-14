# Expected Findings — Rechnungsfreigabe (02_medium)

## Seeded Defect
- **Typ:** Fehlender Pfad an XOR-Gateway
- **Location:** XOR Gateway "Betrag < 1000?"
- **Beschreibung:** Das XOR-Gateway hat nur einen Ausgang ("ja" -> Automatische Freigabe). Der "nein"-Pfad für manuelle Prüfung bei Beträgen >= 1000 fehlt. Rechnungen über 1000 Euro haben keinen definierten Prozessweg.
- **Erwartete Erkennung:** LLM sollte erkennen, dass ein XOR-Gateway mindestens 2 Ausgänge braucht und der "nein"-Pfad fehlt.
