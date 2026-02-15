# Process Audit Skill — Design

## Ziel

Ein Claude-Code-Skill (`/process_audit`), der visuelle Prozessbeschreibungen (BPMN, Flowcharts, Swimlanes) systematisch auf strukturelle, organisatorische und Effizienz-Probleme prüft. Basiert auf den Erkenntnissen der dot_experiment-Studie.

Lebt innerhalb des `dot_experiment`-Projekts. Primärer Zweck: Referenz-Implementation als Begleitung zu einem Blogpost.

## Kernidee: Drei Analyse-Perspektiven

Die Studie (Section 8) zeigt: Direkte Bildanalyse und Zwischenformat-basierte Analyse haben ~55% Overlap, aber jede Perspektive findet Dinge, die die andere übersieht. Der Skill kombiniert beide.

```
Input(s)                    Analyse-Pipeline                    Output
─────────                   ──────────────                     ──────
                            ┌─────────────────┐
  Bild(er) ───────────────→ │ Direkte Analyse  │──→ findings_direct
                            └─────────────────┘
                            ┌─────────────────┐
  Bild(er) ──→ Mermaid ──→ │ Strukturanalyse  │──→ findings_structural
  XML(s)   ──→ Mermaid ──→ │ (auf Mermaid)    │
                            └─────────────────┘
                            ┌─────────────────┐
  findings_direct ─────────→│ Synthese +       │──→ audit_findings.yaml
  findings_structural ─────→│ Cross-Artefakt   │    audit_report.md
  (Mermaid-Dateien) ───────→│                  │
                            └─────────────────┘
```

### Warum Mermaid statt DOT?

Bei Bild-Quellen: Mermaid macht signifikant weniger Übersetzungsfehler (Section 7: Edge Recall 8%→100% bei komplexen Diagrammen). Bei XML-Quellen: kein Unterschied. Mermaid ist der sichere Default.

### Warum beide Perspektiven?

| Dimension | Strukturanalyse (Mermaid) | Direkte Analyse (Bild) |
|-----------|--------------------------|----------------------|
| BPMN-Syntax | Gateway-Typen, Event-Semantik, Message-Flow-Ziele | Weniger präzise |
| Graph-Topologie | Synchronisationsfehler, Schleifen, Dead Ends | Findet Schleifen, übersieht Gateway-Mismatches |
| Business-Logik | Grundlegend | **Deutlich stärker** — Governance, Eskalation |
| Organisatorisches | Bottlenecks, Unterauslastung | + Kompetenzfragen, Vier-Augen |

Kritischstes Beispiel: AND-Split→XOR-Join-Bug im Warenversand — nur von der Mermaid-basierten Analyse gefunden.

## Eingabeformate

| Format | Behandlung |
|--------|-----------|
| PNG/PDF/SVG (Bild) | Bild→Mermaid + Bild→Direkte Analyse |
| .bpmn/.xml (XML) | XML→Mermaid + (falls Bild vorhanden) Bild→Direkte Analyse |
| Bild + XML (beides) | Dual: XML→Mermaid für Struktur, Bild→Direkte Analyse für Business-Kontext |

## Prozesstypen

- BPMN (mit/ohne Pools, Lanes, Message Flows)
- Flowcharts (Entscheidungsbäume, Ablaufdiagramme)
- Swimlane-Diagramme (rollenbasierte Prozesse)

Explizit ausgeschlossen: Organigramme (keine Prozesse, schwache Studienergebnisse bei Bildübersetzung).

## Multi-Artefakt-Modus

Wenn mehrere Artefakte übergeben werden:

1. Jedes Artefakt wird einzeln übersetzt (→ je eine Mermaid-Datei)
2. Jedes Artefakt wird einzeln analysiert (direkt + strukturell)
3. **Cross-Artefakt-Synthese** auf den Mermaid-Dateien:
   - **Schnittstellen-Check**: Enden von Teilprozessen matchen mit Starts anderer Teilprozesse?
   - **Noun/Verb-Konsistenz**: Gleiche Aktivitäten gleich benannt über Artefakte hinweg?
   - **Vollständigkeit**: Referenzierte Teilprozesse, die nicht als Artefakt vorliegen?

### Vorteil des Zwischenformats bei Multi-Artefakt

In Mermaid sind Labels normalisierte Strings. "Antrag prüfen" in Prozess A und "Antragsprüfung" in Prozess B sind als Text vergleichbar — in Bildern nicht. Die Mermaid-Übersetzung erzwingt eine kanonische Textform, die Cross-Referenzierung ermöglicht.

## Output-Artefakte

### `audit_findings.yaml` — Maschinenlesbar

```yaml
audit:
  artifacts:
    - id: hauptprozess
      source: hauptprozess.png
      type: bpmn
  findings:
    - id: F1
      category: structural     # structural | organizational | efficiency
      severity: high            # high | medium | low
      source: structural        # structural | direct | both
      elements: ["Gateway_X", "Task_Y"]
      title: "AND-Split ohne AND-Join"
      description: "Der parallele Gateway wird durch einen exklusiven Gateway synchronisiert..."
      artifact: hauptprozess
  cross_artifact_findings:      # nur bei Multi-Artefakt
    - id: CF1
      category: structural
      severity: medium
      title: "Inkonsistente Benennung zwischen Haupt- und Teilprozess"
      artifacts: [hauptprozess, teilprozess_a]
      description: "..."
  summary:
    total: 12
    by_category: {structural: 5, organizational: 4, efficiency: 3}
    by_severity: {high: 3, medium: 5, low: 4}
    overlap_rate: 0.55          # Anteil Findings, die beide Perspektiven gefunden haben
```

### `audit_report.md` — Menschenlesbar

Strukturierter Markdown-Report:
- Zusammenfassungstabelle (Kategorie × Severity)
- Findings nach Kategorie gruppiert, mit Severity-Tag und betroffenen Elementen
- Bei Multi-Artefakt: eigener Abschnitt für Cross-Artefakt-Findings
- Abschnitt "Methodik" mit Hinweis auf Dual-Analyse-Ansatz

## Skill-Workflow

```
/process_audit <pfad(e) zu Diagramm(en)>
```

### Schritte

1. **Input erkennen**: Dateityp(en) bestimmen, Artefakt-Liste aufbauen
2. **Übersetzen**: Jedes Artefakt → Mermaid (Bild→Mermaid oder XML→Mermaid)
3. **Direkte Analyse**: Jedes Bild-Artefakt direkt analysieren (ohne Zwischenformat)
4. **Strukturelle Analyse**: Jede Mermaid-Datei auf Prozessdefekte analysieren
5. **Synthese**: Findings zusammenführen, deduplizieren, Overlap-Rate berechnen
6. **Cross-Artefakt-Check** (bei Multi): Schnittstellen, Konsistenz, Vollständigkeit
7. **Output schreiben**: `audit_findings.yaml` + `audit_report.md` im Arbeitsverzeichnis

### Sonderfälle

- **Nur XML, kein Bild**: Kein direkter Analyse-Schritt. Nur strukturelle Analyse auf Mermaid.
- **Nur Bild, kein XML**: Beide Perspektiven (direkt + Mermaid), aber Mermaid aus Bild übersetzt (fehleranfälliger).
- **Einzelnes Artefakt**: Kein Cross-Artefakt-Schritt.

## File Layout

```
dot_experiment/
├── skills/
│   └── process_audit/
│       └── SKILL.md                  # Skill-Definition
├── prompts/
│   ├── translate_image_to_mermaid.md # Bild → Mermaid (NEU, basiert auf translate_image.md)
│   ├── translate_xml_to_mermaid.md   # XML → Mermaid (NEU, basiert auf translate_xml.md)
│   ├── analyze_structural.md         # Analyse auf Mermaid-Basis (NEU, basiert auf analyze_process.md)
│   ├── analyze_direct.md             # Direkte Bildanalyse (NEU)
│   ├── synthesize_findings.md        # Findings-Synthese + Deduplizierung (NEU)
│   └── cross_artifact_check.md       # Cross-Artefakt-Konsistenz (NEU)
│   ├── translate_image.md            # (Original, bleibt)
│   ├── translate_xml.md              # (Original, bleibt)
│   └── analyze_process.md            # (Original, bleibt)
├── eval/                             # (unverändert)
└── testdata/                         # (unverändert)
```

## Abgrenzung

- **Kein Rendering**: Der Skill rendert keine Mermaid-Diagramme. Die Mermaid-Dateien sind Zwischenprodukte für die Analyse, nicht für visuelle Ausgabe.
- **Kein Vergleich gegen Referenz**: compare.py / compare_mermaid.py sind Studien-Tools, nicht Teil des Audit-Workflows.
- **Kein Fix-Vorschlag**: Der Skill identifiziert Probleme, schlägt aber keine korrigierten Diagramme vor.
- **Keine Engine-Validierung**: Keine BPMN-Schema-Validierung oder Executable-Check. Rein analytisch.

## Validierung

Der Skill kann gegen die bestehenden Testdaten validiert werden:
- `testdata/bpmn_real/01_warenversand/` — bekannte Findings aus Section 4+8
- `testdata/bpmn_real/02_restaurant/` — bekannte Findings
- `testdata/bpmn_real/03_regressnahme_p1/` — bekannte Findings

Erwartung: Der Skill sollte mindestens die Findings reproduzieren, die in Section 8 als "gemeinsam" (Overlap) identifiziert wurden.
