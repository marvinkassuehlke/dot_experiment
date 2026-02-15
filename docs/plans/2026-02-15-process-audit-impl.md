# Process Audit Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a `/process_audit` Claude Code Skill that analyzes process diagrams (BPMN, Flowcharts, Swimlanes) via dual-perspective analysis (direct + structural) and outputs YAML + Markdown findings.

**Architecture:** The skill is a SKILL.md file that orchestrates 6 prompt templates. Input: process diagram(s) as image and/or XML. Pipeline: translate → analyze (2 perspectives) → synthesize → output. Multi-artifact mode adds cross-artifact consistency checks.

**Tech Stack:** Claude Code Skill (SKILL.md), Mermaid (intermediate format), YAML + Markdown (output)

**Design doc:** `docs/plans/2026-02-15-process-audit-design.md`

---

### Task 1: Translation Prompts (Bild→Mermaid, XML→Mermaid)

**Context:** The existing `prompts/translate_image.md` and `prompts/translate_xml.md` target DOT format. We need Mermaid equivalents. The study (Section 7) shows Mermaid reduces image translation errors significantly.

**Files:**
- Create: `prompts/translate_image_to_mermaid.md`
- Create: `prompts/translate_xml_to_mermaid.md`
- Reference: `prompts/translate_image.md` (existing DOT version)
- Reference: `prompts/translate_xml.md` (existing DOT version)

**Step 1: Create `prompts/translate_image_to_mermaid.md`**

```markdown
Du erhältst ein Prozessdiagramm als Bild. Übersetze es in Mermaid-Syntax.

Regeln:
- Diagrammtyp: `flowchart TD` (top-down) oder `flowchart LR` (left-right), je nach Layout des Originals
- Jeden sichtbaren Knoten als Node mit eindeutiger ID und Label in Anführungszeichen
- Shapes: `["Label"]` = Aktivität/Task, `{"Label"}` = Entscheidung/Gateway, `(["Label"])` = Start/End Event, `[/"Label"/]` = Daten/Dokument
- Jede Verbindung als Edge mit `-->` (Sequence Flow) oder `-.->` (Message Flow / gestrichelt)
- Edge-Labels mit `-->|"Label"|` Syntax
- `subgraph` für Pools, Lanes, Gruppierungen — mit Label in Anführungszeichen
- Labels exakt vom Bild übernehmen, nicht umformulieren
- Nur valides Mermaid ausgeben, keine Erklärung, kein Markdown-Codeblock

Beispiel-Syntax:
```
flowchart TD
    subgraph pool1["Gast"]
        A(["Hunger festgestellt"]) --> B["Restaurant betreten"]
        B --> C["Gericht auswählen"]
        C --> D{"Gericht verfügbar?"}
        D -->|"Ja"| E["Bestellen"]
        D -->|"Nein"| C
    end
```
```

**Step 2: Create `prompts/translate_xml_to_mermaid.md`**

```markdown
Du erhältst ein Prozessdiagramm als XML (BPMN 2.0 oder draw.io Format). Übersetze die Struktur in Mermaid-Syntax.

Regeln:
- Ignoriere Layout-Metadaten (Koordinaten, Größen, Farben, Positionen)
- Extrahiere nur Topologie: Knoten, Kanten, Gruppierungen
- Diagrammtyp: `flowchart TD` (top-down) oder `flowchart LR` (left-right)
- Shapes: `["Label"]` = Task/Aktivität, `{"Label"}` = Gateway/Entscheidung, `(["Label"])` = Start/End Event
- `subgraph` für Pools, Lanes, Gruppierungen — mit Label in Anführungszeichen
- Edge-Labels mit `-->|"Label"|` Syntax
- `-->` für Sequence Flows, `-.->` für Message Flows
- Labels exakt aus dem XML übernehmen
- Gateway-Typ im Label vermerken, z.B. `{"AND (Split)"}`, `{"XOR: Sonderversand?"}`, `{"OR (Join)"}`
- Nur valides Mermaid ausgeben, keine Erklärung, kein Markdown-Codeblock
```

**Step 3: Validate both prompts**

Test `translate_image_to_mermaid.md` mentally against `testdata/bpmn_real/01_warenversand/bpmn_rendered.png` — verify the prompt instructions would produce a correct Mermaid translation for this 3-lane BPMN.

Test `translate_xml_to_mermaid.md` mentally against `testdata/bpmn_real/01_warenversand/Warenversand.bpmn` — verify the XML rules cover BPMN namespace handling.

**Step 4: Commit**

```bash
git add prompts/translate_image_to_mermaid.md prompts/translate_xml_to_mermaid.md
git commit -m "feat(process_audit): add Mermaid translation prompt templates"
```

---

### Task 2: Analysis Prompts (Structural + Direct)

**Context:** The existing `prompts/analyze_process.md` targets DOT input. We need a Mermaid-adapted version for structural analysis, plus a new prompt for direct image analysis (no intermediate format). Both prompts must produce findings in a consistent format so the synthesis step can merge them.

**Files:**
- Create: `prompts/analyze_structural.md`
- Create: `prompts/analyze_direct.md`
- Reference: `prompts/analyze_process.md` (existing DOT version)

**Step 1: Create `prompts/analyze_structural.md`**

```markdown
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
```

**Step 2: Create `prompts/analyze_direct.md`**

```markdown
Du erhältst ein Prozessdiagramm als Bild. Analysiere den dargestellten Prozess auf Probleme — OHNE ihn vorher in ein Textformat zu übersetzen.

Betrachte das Diagramm so, wie ein Prozessberater es tun würde: Lies den Ablauf, verstehe die Rollen, erkenne die Schwächen.

## Analysekategorien

### 1. Strukturelle Probleme
- Fehlende Pfade (z.B. kein "Nein"-Pfad bei Entscheidungen)
- Endlosschleifen ohne Abbruchbedingung
- Fehlende Fehlerbehandlung / Eskalationspfade
- Synchronisationsprobleme bei parallelen Abläufen

### 2. Organisatorische Probleme
- Bottlenecks (eine Rolle trägt zu viel Verantwortung)
- Fehlende Rollen oder Verantwortlichkeiten
- Governance-Lücken (fehlende Freigaben, Vier-Augen-Prinzip)
- Kompetenzfragen (wer darf/kann bestimmte Entscheidungen treffen?)

### 3. Effizienz-Probleme
- Vermeidbare Wartezeiten
- Fehlende Automatisierungspotenziale
- Unnötig komplexe Teilprozesse
- Fehlende Parallelisierung

## Output-Format

Für jedes Finding:
- **ID**: F1, F2, F3, ...
- **Kategorie**: structural | organizational | efficiency
- **Schwere**: high | medium | low
- **Betroffene Elemente**: Konkrete Bezeichnungen aus dem Diagramm
- **Titel**: Einzeilige Zusammenfassung
- **Beschreibung**: 2-3 Sätze mit Erklärung und Konsequenz

Wenn keine Probleme gefunden: explizit sagen "Keine Probleme identifiziert".
```

**Step 3: Verify consistency**

Both prompts use the same Output-Format (ID, Kategorie, Schwere, Elemente, Titel, Beschreibung) and the same Kategorie-Werte (structural, organizational, efficiency). This is critical for the synthesis step.

**Step 4: Commit**

```bash
git add prompts/analyze_structural.md prompts/analyze_direct.md
git commit -m "feat(process_audit): add structural and direct analysis prompts"
```

---

### Task 3: Synthesis + Cross-Artifact Prompts

**Context:** The synthesis prompt merges findings from both analysis perspectives (direct + structural), deduplicates overlapping findings, and computes the overlap rate. The cross-artifact prompt checks consistency across multiple diagrams. Both produce YAML output.

**Files:**
- Create: `prompts/synthesize_findings.md`
- Create: `prompts/cross_artifact_check.md`

**Step 1: Create `prompts/synthesize_findings.md`**

```markdown
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

```yaml
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
```

Gib NUR das YAML aus, keine Erklärung.
```

**Step 2: Create `prompts/cross_artifact_check.md`**

```markdown
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

```yaml
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
```

Falls keine Cross-Artefakt-Probleme: leere Liste `cross_artifact_findings: []` ausgeben.
Gib NUR das YAML aus, keine Erklärung.
```

**Step 3: Commit**

```bash
git add prompts/synthesize_findings.md prompts/cross_artifact_check.md
git commit -m "feat(process_audit): add synthesis and cross-artifact prompts"
```

---

### Task 4: SKILL.md erstellen

**Context:** Das Herzstück. SKILL.md definiert den Workflow, den Claude Code ausführt, wenn `/process_audit` aufgerufen wird. Es orchestriert die Prompt-Templates aus Task 1-3.

**Files:**
- Create: `skills/process_audit/SKILL.md`

**Step 1: Create directory**

```bash
mkdir -p skills/process_audit
```

**Step 2: Create `skills/process_audit/SKILL.md`**

```markdown
---
name: process_audit
description: Analysiert Prozessdiagramme (BPMN, Flowcharts, Swimlanes) auf strukturelle, organisatorische und Effizienz-Probleme via Dual-Perspective-Analyse.
---

# Process Audit

Systematische Prozessanalyse durch Kombination zweier Perspektiven:
- **Strukturelle Analyse**: Übersetzung in Mermaid → Graph-basierte Defekterkennung (Gateway-Typen, Topologie, Synchronisation)
- **Direkte Analyse**: Bildbasierte Prozessbewertung (Business-Logik, Governance, Szenarien)

Beide Perspektiven haben ~55% Overlap. Die Differenz ist das Signal: Was nur eine Perspektive findet, ist oft der wertvollste Fund.

## Aufruf

```
/process_audit <pfad(e) zu Diagramm(en)>
```

Unterstützte Formate:
- **Bilder**: PNG, PDF, SVG — werden direkt analysiert UND nach Mermaid übersetzt
- **XML**: .bpmn, .xml — werden nach Mermaid übersetzt (keine direkte Analyse möglich)
- **Beides**: Bild + XML zum selben Prozess — Dual-Input, beste Abdeckung

Mehrere Pfade = Multi-Artefakt-Modus (Cross-Artefakt-Konsistenzprüfung).

## Workflow

### Schritt 1: Input erkennen

Für jeden übergebenen Pfad bestimmen:
- Dateityp (Bild vs. XML)
- Artefakt-ID ableiten (Dateiname ohne Extension)
- Bei Bild+XML zum selben Prozess: als ein Artefakt mit zwei Quellen behandeln

### Schritt 2: Übersetzen → Mermaid

Für jedes Artefakt:
- **Bild-Quelle**: Prompt `prompts/translate_image_to_mermaid.md` anwenden. Output als `<artefakt_id>.mmd` speichern.
- **XML-Quelle**: Prompt `prompts/translate_xml_to_mermaid.md` anwenden. Output als `<artefakt_id>.mmd` speichern.
- Bei beiden Quellen: XML bevorzugen (höhere Strukturtreue laut Studie Section 7).

### Schritt 3: Direkte Analyse

Für jedes Artefakt mit Bild-Quelle:
- Prompt `prompts/analyze_direct.md` auf das Originalbild anwenden.
- Output intern als `findings_direct` halten.

Falls nur XML (kein Bild): Diesen Schritt überspringen. Die Synthese arbeitet dann nur mit strukturellen Findings.

### Schritt 4: Strukturelle Analyse

Für jedes Artefakt:
- Prompt `prompts/analyze_structural.md` auf die Mermaid-Datei aus Schritt 2 anwenden.
- Output intern als `findings_structural` halten.

### Schritt 5: Synthese

Prompt `prompts/synthesize_findings.md` anwenden mit:
- `findings_direct` (aus Schritt 3)
- `findings_structural` (aus Schritt 4)

Output: zusammengeführte Findings mit Deduplizierung und Overlap-Rate.

Falls nur eine Perspektive vorhanden (nur XML, kein Bild): Synthese überspringen, strukturelle Findings direkt als Ergebnis übernehmen. Alle Findings bekommen `source: structural`.

### Schritt 6: Cross-Artefakt-Check (nur bei Multi-Artefakt)

Nur wenn mehr als ein Artefakt übergeben wurde:
- Alle Mermaid-Dateien aus Schritt 2 zusammen an Prompt `prompts/cross_artifact_check.md` übergeben.
- Output: `cross_artifact_findings` Liste.

Bei Einzel-Artefakt: Diesen Schritt überspringen.

### Schritt 7: Output schreiben

Zwei Dateien im aktuellen Arbeitsverzeichnis erstellen:

**`audit_findings.yaml`**: Maschinenlesbares YAML mit:
- `audit.artifacts`: Liste der analysierten Artefakte (ID, Quelle, Typ)
- `audit.findings`: Alle Findings aus der Synthese
- `audit.cross_artifact_findings`: Nur bei Multi-Artefakt
- `audit.summary`: Aggregation (Anzahl nach Kategorie, Severity, Source, Overlap-Rate)

**`audit_report.md`**: Menschenlesbarer Markdown-Report mit:
- Übersichtstabelle (Kategorie × Severity)
- Findings gruppiert nach Kategorie, jeweils mit Severity, betroffenen Elementen, Beschreibung
- Bei Multi-Artefakt: eigener Abschnitt "Cross-Artefakt-Findings"
- Abschnitt "Methodik" (kurzer Hinweis auf Dual-Analyse-Ansatz und Overlap-Rate)

## Wichtige Hinweise

- **Mermaid als Zwischenformat**: Die .mmd-Dateien werden nicht gerendert. Sie dienen nur als strukturierte Eingabe für die Analyse.
- **Gateway-Typen im Label**: Die Mermaid-Übersetzung soll Gateway-Typen explizit im Label vermerken (z.B. `{"XOR: Sonderversand?"}`). Das ist der Hauptvorteil gegenüber reiner Bildanalyse.
- **Keine Fixes**: Der Skill identifiziert Probleme, schlägt aber keine korrigierten Diagramme vor.
- **Overlap-Rate**: Typischer Wert laut Studie: ~55%. Deutlich höher = ein Artefakt ist sehr klar modelliert. Deutlich niedriger = die Perspektiven sehen sehr unterschiedliche Dinge (genauer hinschauen!).
```

**Step 3: Commit**

```bash
git add skills/process_audit/SKILL.md
git commit -m "feat(process_audit): add SKILL.md with full audit workflow"
```

---

### Task 5: CLAUDE.md aktualisieren

**Context:** Das Projekt-CLAUDE.md muss den neuen Skill und die neuen Verzeichnisse dokumentieren.

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Append to CLAUDE.md**

Add after the existing `## Conventions` section:

```markdown

## Process Audit Skill

Skill: `/process_audit` — Analysiert Prozessdiagramme via Dual-Perspective-Analyse.

```bash
# Einzelnes Diagramm (Bild)
/process_audit testdata/bpmn_real/01_warenversand/bpmn_rendered.png

# Einzelnes Diagramm (XML)
/process_audit testdata/bpmn_real/01_warenversand/Warenversand.bpmn

# Multi-Artefakt
/process_audit prozess_a.png prozess_b.bpmn prozess_c.png
```

- Skill-Definition: `skills/process_audit/SKILL.md`
- Prompt-Templates: `prompts/translate_*_to_mermaid.md`, `prompts/analyze_*.md`, `prompts/synthesize_findings.md`, `prompts/cross_artifact_check.md`
- Output: `audit_findings.yaml` + `audit_report.md` im Arbeitsverzeichnis
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add process_audit skill to CLAUDE.md"
```

---

### Task 6: Validierung gegen Testdaten

**Context:** Den Skill gegen einen bekannten Case aus der Studie laufen lassen. Erwartung: Die Findings sollten mindestens den Overlap-Kern aus Section 8 reproduzieren.

**Files:**
- Reference: `testdata/bpmn_real/01_warenversand/bpmn_rendered.png`
- Reference: `testdata/bpmn_real/01_warenversand/Warenversand.bpmn`
- Reference: `testdata/bpmn_real/01_warenversand/analysis_from_xml.md` (bekannte DOT-Findings)
- Reference: `testdata/bpmn_real/01_warenversand/analysis_direct.md` (bekannte direkte Findings)

**Step 1: Run `/process_audit` on Warenversand**

```bash
# Im dot_experiment-Verzeichnis:
/process_audit testdata/bpmn_real/01_warenversand/bpmn_rendered.png testdata/bpmn_real/01_warenversand/Warenversand.bpmn
```

**Step 2: Verify output files exist**

Check that `audit_findings.yaml` and `audit_report.md` were created.

**Step 3: Compare against known findings**

Verify that the following known findings from Section 8 appear:
- AND-Split ohne AND-Join (structural, high) — aus struktureller Perspektive
- Sekretariat als Bottleneck (organizational, medium) — aus beiden Perspektiven
- Sequenzielle Angebotseinholung (efficiency) — aus beiden Perspektiven
- Keine Fehlerbehandlung (structural, high) — aus direkter Perspektive
- Leiter Logistik unterausgelastet (organizational, low) — aus beiden Perspektiven

**Step 4: Verify YAML is valid**

```bash
python -c "import yaml; yaml.safe_load(open('audit_findings.yaml'))"
```

**Step 5: Commit validation results**

```bash
git add audit_findings.yaml audit_report.md
git commit -m "test: validate process_audit against Warenversand case"
```

**Step 6: Push everything**

```bash
git push
```
