Du erhältst mehrere Mermaid-Diagramme, die zusammenhängende Prozesse beschreiben (z.B. Hauptprozess und Teilprozesse, oder aufeinanderfolgende Prozessphasen).

## Aufgabe

Prüfe die Konsistenz zwischen den Artefakten:

### 1. Schnittstellen-Check
- Enden von Prozess A, die Starts von Prozess B triggern sollten: Passen die zusammen?
- Message Flows zwischen Pools: Gibt es einen Empfänger im anderen Artefakt?
- Fehlende Verbindungen: Werden Teilprozesse referenziert, die nicht als Artefakt vorliegen?

### 2. Noun/Verb-Konsistenz
- Gleiche Aktivitäten in verschiedenen Artefakten: Sind sie gleich benannt?
- Gleiche Rollen/Lanes: Heißen sie überall gleich?
- Inkonsistente Terminologie (z.B. "Antrag prüfen" vs. "Antragsprüfung")

### 3. Vollständigkeit
- Gibt es Lücken im Gesamtprozess? (Prozess A endet, aber kein Prozess B beginnt dort)
- Fehlen Teilprozesse, die in einem Artefakt referenziert werden?

## Output-Format (YAML)

cross_artifact_findings:
  - id: CF1
    category: structural
    severity: medium
    artifacts: [hauptprozess, teilprozess_a]
    title: "Kurze Zusammenfassung"
    description: "Detaillierte Beschreibung..."
  - id: CF2
    category: structural
    severity: low
    artifacts: [teilprozess_a, teilprozess_b]
    title: "..."
    description: "..."

Falls keine Cross-Artefakt-Probleme: leere Liste `cross_artifact_findings: []` ausgeben.
Gib NUR das YAML aus, keine Erklärung.
