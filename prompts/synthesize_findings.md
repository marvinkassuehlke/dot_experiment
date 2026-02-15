Du erhältst zwei Listen von Prozess-Findings aus unterschiedlichen Analyse-Perspektiven:

1. **Strukturelle Analyse** (basierend auf einem Mermaid-Zwischenformat): Fokus auf Graph-Topologie, Gateway-Typen, Event-Semantik
2. **Direkte Analyse** (basierend auf dem Originalbild): Fokus auf Business-Logik, Governance, Szenarien

## Aufgabe

Führe die Findings zusammen:

1. **Identifiziere Overlap**: Findings, die inhaltlich dasselbe Problem beschreiben (auch wenn Wording/ID unterschiedlich). Markiere diese mit `source: both`.
2. **Behalte Unique Findings**: Findings, die nur in einer Perspektive auftauchen. Markiere mit `source: structural` oder `source: direct`.
3. **Dedupliziere**: Bei Overlap die präzisere/vollständigere Beschreibung übernehmen. Neue durchgehende IDs vergeben (F1, F2, ...).
4. **Berechne Overlap-Rate**: Anteil der Overlap-Findings an der Gesamtzahl.

## Output-Format (YAML)

findings:
  - id: F1
    category: structural
    severity: high
    source: both
    elements: ["Gateway_X", "Task_Y"]
    title: "Kurze Zusammenfassung"
    description: "Detaillierte Beschreibung..."
  - id: F2
    category: organizational
    severity: medium
    source: direct
    elements: ["Lane_Sekretariat"]
    title: "..."
    description: "..."
summary:
  total: 12
  by_category:
    structural: 5
    organizational: 4
    efficiency: 3
  by_severity:
    high: 3
    medium: 5
    low: 4
  by_source:
    both: 6
    structural: 3
    direct: 3
  overlap_rate: 0.50

Gib NUR das YAML aus, keine Erklärung.
