# Expected Findings — Kreditantrag (03_complex)

## Seeded Defect
- **Typ:** Endlosschleife
- **Location:** Nodes "review" → "review_check" → "review"
- **Beschreibung:** Nach Ablehnung wird der Antrag nochmal geprüft (review). Der Entscheidungsknoten "review_check" hat nur einen Ausgang ("nein" → zurück zu review). Es gibt keinen "ja"-Pfad, der die Schleife verlässt.
- **Erwartete Erkennung:** LLM sollte die Endlosschleife identifizieren und das Fehlen eines Exit-Pfads aus "review_check" benennen.

## Sekundärer Befund (optional)
- Node "done_no" (Abgelehnt) ist unerreichbar — kein Pfad führt dorthin, da "reject" direkt zu "review" geht statt zu "done_no".
