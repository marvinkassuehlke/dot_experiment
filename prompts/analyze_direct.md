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
