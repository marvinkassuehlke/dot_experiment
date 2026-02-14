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
