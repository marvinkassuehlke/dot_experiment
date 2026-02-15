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

/process_audit <pfad(e) zu Diagramm(en)>

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
- **Gateway-Typen im Label**: Die Mermaid-Übersetzung soll Gateway-Typen explizit im Label vermerken (z.B. `{XOR: Sonderversand?}`). Das ist der Hauptvorteil gegenüber reiner Bildanalyse.
- **Keine Fixes**: Der Skill identifiziert Probleme, schlägt aber keine korrigierten Diagramme vor.
- **Overlap-Rate**: Typischer Wert laut Studie: ~55%. Deutlich höher = ein Artefakt ist sehr klar modelliert. Deutlich niedriger = die Perspektiven sehen sehr unterschiedliche Dinge (genauer hinschauen!).
