# Expected Findings — Onboarding (03_complex)

## Seeded Defect
- **Typ:** Bottleneck
- **Location:** Node "Teamlead-Freigabe"
- **Beschreibung:** Alle drei parallelen Onboarding-Pfade (IT, HR, Fachbereich) müssen durch einen einzigen Knoten "Teamlead-Freigabe" laufen. Dies ist ein offensichtlicher Engpass — der Teamlead muss 3 unabhängige Prozesse einzeln freigeben, was den gesamten Onboarding-Prozess verzögert.
- **Erwartete Erkennung:** LLM sollte den Bottleneck bei "Teamlead-Freigabe" identifizieren (3 eingehende Kanten aus verschiedenen Bereichen, 1 Person).
