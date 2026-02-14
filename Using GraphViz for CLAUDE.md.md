# Using GraphViz for CLAUDE.md — Artikelzusammenfassung

**Quelle:** https://blog.fsck.com/2025/09/29/using-graphviz-for-claudemd/
**Autor:** Jesse Vincent (fsck.com)
**Kernidee:** CLAUDE.md-Regeln nicht als Prosa/Markdown, sondern als DOT (GraphViz) formulieren — strukturierter, weniger mehrdeutig, maschinenlesbarer.

---

## Motivation

- Der Autor hatte eine umfangreiche CLAUDE.md mit Prozessregeln (TDD, Git-Disziplin, Debugging etc.)
- Hypothese: DOT als Spezifikationsformat reduziert die Ambiguität natürlicher Sprache
- Claude versteht DOT-Syntax und kann danach handeln

## Experiment-Verlauf (v1–v5)

| Version | Ergebnis |
|---------|----------|
| v1 | Zu komplex, zu viele Verbindungen — unpraktisch für Claude |
| v2 | Rule #1 überall eingebettet, aber zu akademisch |
| v3 | Unified Workflow — unbefriedigende Abstraktionen |
| v4 | Vereinfacht, aber zu viel Prozessdetail verloren |
| v5 | Finale Version: 7 Layer als Subgraphs (Request-Analyse, TDD, Debugging, Testing, Git, Completion) |

**Wichtig:** ~12 Iterationsrunden waren nötig. Das ist kein einfaches Format-Konvertieren — es erfordert ein Neudenken der Prozessstruktur.

## Was funktioniert hat

- Claude **versteht DOT und handelt danach** — keine spezielle Erklärung nötig
- In direkten Vergleichstests: DOT-Version produzierte **besseres Output** als Markdown-Version
- Prozess-Inkonsistenzen werden im Graph **sofort sichtbar** (Markdown versteckt sie)
- Visuelle Darstellung deckt problematische Workflows auf

## Semantische Shape-Konventionen

```
diamond    → Entscheidungen (ja/nein)
octagon    → Absolute Verbote (filled, rot/orange)
box        → Standard-Prozessschritte
ellipse    → Entry/Exit-Punkte
doublecircle → Finale Zustände
plaintext  → Konkrete Shell-Commands
subgraph   → Thematische Gruppierung (cluster_tdd, cluster_debug, etc.)
dotted edges → Bedingte/optionale Flows
```

## Probleme & Einschränkungen

- **Halluzinationen:** Bei der Aufforderung "mach es 100x besser" erfand Claude Sci-Fi-Features
- **Komplexität:** Zu detaillierte Graphen sind kontraproduktiv — Claude verliert den Überblick
- **Unicode:** Rendert nicht korrekt in GraphViz-Output
- **Sweet Spot unklar:** Optimale Granularität zwischen "zu simpel" und "zu komplex" ist schwer zu treffen

## Zentrale Erkenntnisse

1. **DOT ist ein valides Format für CLAUDE.md** — Claude parsed und befolgt es
2. **Struktur erzwingt Klarheit:** Man muss Prozesse als echte Zustandsmaschinen denken, nicht als Prosa-Listen
3. **Subgraphs als Organisationsprinzip:** Jeder Workflow (TDD, Debugging, Git) wird ein eigener Cluster
4. **Shapes als semantische Marker:** Nicht nur Dekoration — sie signalisieren Claude die Art des Knotens
5. **Weniger ist mehr:** Kompakte Graphen mit klaren Pfaden > erschöpfende Dokumentation
6. **Cross-Cluster-Edges:** Verbindungen zwischen Subgraphs modellieren reale Workflow-Übergänge (z.B. Test failed → Debugging-Subgraph)

---

## Relevanz für unser Experiment

Marvins globale CLAUDE.md nutzt bereits genau dieses Pattern (DOT-Digraph mit Subgraphs, semantischen Shapes, Cluster-Organisation). Die Frage ist nun: **Wie kann man diesen Ansatz systematisch weiterentwickeln und validieren?**
