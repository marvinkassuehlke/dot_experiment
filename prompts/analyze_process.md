Du erhältst einen Geschäftsprozess als GraphViz DOT. Analysiere ihn auf:

1. **Strukturelle Probleme:**
   - Dead Ends (Knoten ohne ausgehende Kante, die kein End-Knoten sind)
   - Endlosschleifen (Zyklen ohne Exit-Bedingung)
   - Fehlende Pfade (Entscheidungen mit weniger Ausgängen als erwartet)
   - Unerreichbare Knoten

2. **Organisatorische Probleme:**
   - Bottlenecks (ein Knoten/Akteur, durch den zu viele Pfade laufen)
   - Unklare Verantwortlichkeiten (Lanes/Cluster ohne Aktivitäten)
   - Überlastung (zu viele Direct Reports, zu viele Aufgaben in einer Lane)

3. **Effizienz-Probleme:**
   - Unnötige Schleifen
   - Ping-Pong (Aufgaben die mehrfach zwischen Akteuren hin- und herwandern)
   - Redundante Schritte

Benenne jedes gefundene Problem konkret mit Bezug auf die Node-Labels aus dem DOT.
Wenn keine Probleme gefunden: explizit sagen "Keine Probleme identifiziert".
