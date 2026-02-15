# CLAUDE.md — dot_experiment

## Project Overview

Study: DOT (GraphViz) als Zwischenformat für Business-Diagramme (Flowcharts, BPMN, Orgcharts, Swimlanes). Testet Übersetzungsqualität (Bild/XML → DOT) und analytisches Potenzial (Defekt-Erkennung auf DOT-Basis).

## Commands

```bash
dot -Tpng input.dot -o output.png    # DOT → PNG rendern
python eval/compare.py                # Graph-Diff Ground Truth vs. Ergebnis
```

## Key Directories

- `testdata/<type>/<complexity>/` — Ground Truth DOT, gerenderte PNGs, XML-Quellen, LLM-Ergebnisse
- `prompts/` — Standardisierte Prompts für Übersetzung und Analyse
- `eval/` — Vergleichsskript + Gesamtauswertung

## Conventions

- Ground Truth Dateien: `ground_truth.dot`
- LLM-Ergebnisse: `from_image.dot`, `from_xml.dot`
- Analysen: `analysis_from_image.md`, `analysis_from_xml.md`
- Auswertungen: `eval.md` pro Case, `eval/summary.md` gesamt
- Alle DOT-Dateien nutzen semantische Shapes (diamond=Entscheidung, box=Aktivität, ellipse=Start/End, octagon=Fehler)

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

- Skill-Definition: `.claude/skills/process_audit/SKILL.md`
- Prompt-Templates: `prompts/translate_*_to_mermaid.md`, `prompts/analyze_*.md`, `prompts/synthesize_findings.md`, `prompts/cross_artifact_check.md`
- Output: `audit_findings.yaml` + `audit_report.md` im Arbeitsverzeichnis
