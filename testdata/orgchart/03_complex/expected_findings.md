# Expected Findings — Konzernstruktur (03_complex)

## Seeded Defect
- **Typ:** Verwaiste Organisationseinheit
- **Location:** Subgraph "Tochter C — Digital"
- **Beschreibung:** Die Tochtergesellschaft "Digital" hat keine Reporting-Linie zur Holding. Während Tochter A (Manufacturing) und Tochter B (Services) an den Vorstand berichten, ist Tochter C komplett isoliert — keine Governance, keine Steuerung, kein Informationsfluss zur Konzernspitze.
- **Erwartete Erkennung:** LLM sollte erkennen, dass Tochter C keine Verbindung zur Holding hat und als verwaiste Einheit identifizieren.
