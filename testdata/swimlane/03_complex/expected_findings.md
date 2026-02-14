# Expected Findings — Reklamation (03_complex)

## Seeded Defect
- **Typ:** Leere Lane / Fehlende Verantwortlichkeit
- **Location:** Subgraph "Recht" (cluster_recht)
- **Beschreibung:** Die Lane "Recht" existiert in der Prozessdefinition, enthält aber keine einzige Aktivität. Bei einem Reklamationsprozess wäre die Rechtsabteilung typischerweise bei Gewährleistungsfragen, Haftungsprüfungen oder Eskalationen involviert. Die leere Lane deutet auf einen unvollständigen Prozessentwurf hin.
- **Erwartete Erkennung:** LLM sollte die leere Lane identifizieren und als unvollständigen Prozessentwurf bemängeln.
