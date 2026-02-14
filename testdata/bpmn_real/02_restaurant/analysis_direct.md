# Prozessanalyse: Restaurant-Bestellprozess (Fast-Food / Counter-Service)

## Prozessbeschreibung

Das BPMN-Diagramm modelliert einen Restaurant-Bestellprozess im Counter-/Fast-Food-Stil mit drei Pools:

- **Gast (Nahrungsaufnahme)**: Restaurant betreten, Gericht auswaehlen, Bestellung aufgeben, Betrag bezahlen, Pieper entgegennehmen, warten auf Signal "Essen abholbereit", Essen abholen, Mahlzeit verzehren.
- **Angestellter (Bestellungsbearbeitung)**: Bestellung erhalten (Message Start), Bestellung eingeben, Geld kassieren (Kassensystem), Pieper einstellen, Pieper uebergeben, Koch informieren, warten auf "Essen fertig" (Message Event), Pieper ausloesen, dann entweder Kunde erscheint oder nach 5-Minuten-Timer Kunden ausrufen, Essen uebergeben, Ende "Bestellung bearbeitet".
- **Koch (Mahlzeitzubereitung)**: Message Start "Mahlzeit zuzubereiten", Mahlzeit zubereiten, Essen in Durchreiche stellen, Angestellten informieren, Ende "Mahlzeit zubereitet".

---

## 1. Strukturelle Probleme

### S1: Fehlender Fehler-/Abbruchpfad bei Nicht-Erscheinen des Kunden

**Betroffene Elemente:** Timer-Event "5 Minuten", Task "Kunden ausrufen", Event "Kunde erscheint"

**Beschreibung:** Nach dem Ausloesen des Piepers wartet der Prozess auf das Ereignis "Kunde erscheint". Falls der Kunde nicht erscheint, wird nach 5 Minuten der Kunde ausgerufen. Danach fuehrt der Pfad zurueck zum Event-Gateway (implizit: erneutes Warten). Es gibt jedoch keinen definierten Abbruchpfad -- was passiert, wenn der Kunde auch nach dem Ausrufen nicht erscheint? Der Prozess koennte theoretisch endlos zwischen "5 Minuten warten" und "Kunden ausrufen" pendeln.

**Schwere:** HOCH -- Potenzielle Endlosschleife ohne definierten Abbruch. In der Realitaet wuerde das Essen irgendwann entsorgt, aber das Diagramm bildet diesen Fall nicht ab.

---

### S2: Fehlende Synchronisation zwischen Gast und Angestelltem beim Bezahlen

**Betroffene Elemente:** "Betrag bezahlen" (Gast), "Geld kassieren" (Angestellter)

**Beschreibung:** Der Gast fuehrt "Betrag bezahlen" aus, und der Angestellte fuehrt "Geld kassieren" aus. Diese Aktivitaeten sind ueber Message Flows (gestrichelte Linien) verbunden, aber die Synchronisation ist unvollstaendig modelliert. Der Angestellte beginnt mit "Geld kassieren" direkt nach "Bestellung eingeben" -- es gibt kein explizites Warten darauf, dass der Gast tatsaechlich bezahlt. In einem korrekten BPMN-Modell muesste hier ein empfangendes Message-Event die Zahlung des Gastes abwarten.

**Schwere:** MITTEL -- Die Reihenfolge ist durch den Message Flow implizit angedeutet, aber BPMN-konform nicht sauber modelliert. Koennte bei automatisierter Ausfuehrung zu Timing-Problemen fuehren.

---

### S3: Kein Rueckkanal bei Problemen in der Kueche

**Betroffene Elemente:** Koch-Pool komplett, Angestellter-Pool

**Beschreibung:** Der Koch-Prozess ist strikt linear: Nachricht empfangen, zubereiten, in Durchreiche stellen, Angestellten informieren. Es gibt keinen modellierten Pfad fuer den Fall, dass eine Zutat fehlt, das Gericht nicht zubereitet werden kann, oder ein Fehler bei der Zubereitung passiert. Der Gast und der Angestellte wuerden endlos auf "Essen fertig" warten.

**Schwere:** HOCH -- Fehlende Fehlerbehandlung in einem kritischen Teilprozess. Dead End fuer den Gesamtprozess bei Kuechenproblemen.

---

### S4: Kein Gateway nach Pieper-Ausloesen -- Event-Based Gateway implizit

**Betroffene Elemente:** "Pieper ausloesen" -> Event-Gateway -> "Kunde erscheint" / "5 Minuten"

**Beschreibung:** Nach "Pieper ausloesen" folgt ein Event-based Gateway, das korrekt zwischen "Kunde erscheint" und dem Timer "5 Minuten" unterscheidet. Das ist grundsaetzlich korrekt modelliert. Jedoch: Nach "Kunden ausrufen" fuehrt der Pfad zurueck zu demselben Gateway. Das bedeutet, der Pieper wuerde nicht erneut ausgeloest -- der Prozess wartet nur passiv. Es ist unklar, ob der Ruecksprung zum Gateway BPMN-konform ist, da Event-based Gateways normalerweise nicht als Schleifenziel dienen.

**Schwere:** MITTEL -- Semantisch fragwuerdig, ob das Event-based Gateway als Schleifenruecksprungziel valide ist.

---

### S5: Fehlende Eskalation / Timeout auf Gast-Seite

**Betroffene Elemente:** Message Intermediate Catch Event "Essen abholbereit" (Gast-Lane)

**Beschreibung:** Der Gast wartet nach "Pieper entgegennehmen" auf das Signal "Essen abholbereit". Es gibt keinen Timer oder Abbruchpfad auf Gast-Seite. Falls das Essen nie fertig wird (Kuechenproblem, Systemfehler), wartet der Gast-Prozess endlos.

**Schwere:** MITTEL -- Fehlende Timeout-Behandlung, aber in der Praxis wuerde der Gast selbst eskalieren.

---

## 2. Organisatorische Probleme

### O1: Angestellter als Single Point of Failure / Bottleneck

**Betroffene Elemente:** Gesamte Angestellter-Lane

**Beschreibung:** Der Angestellte ist fuer den kompletten Bestellprozess verantwortlich: Bestellung aufnehmen, kassieren, Pieper programmieren und uebergeben, Koch informieren, auf fertiges Essen warten, Pieper ausloesen, ggf. Kunden ausrufen, und Essen uebergeben. Das sind 8+ Aufgaben in einem einzigen Prozessdurchlauf. Bei mehreren gleichzeitigen Bestellungen wird dieser Mitarbeiter zum Flaschenhals, da er den gesamten Lebenszyklus einer Bestellung begleitet.

**Schwere:** HOCH -- In Stosszeiten kritischer Engpass. Keine Aufgabenteilung zwischen Kassierer und Ausgabe.

---

### O2: Keine Rolle fuer Qualitaetskontrolle

**Betroffene Elemente:** Uebergang Koch -> Angestellter -> Gast

**Beschreibung:** Zwischen "Essen in Durchreiche stellen" und "Essen uebergeben" gibt es keine Qualitaetspruefung. Niemand kontrolliert, ob die richtige Bestellung dem richtigen Kunden zugeordnet wird. Das Kassensystem wird nur beim Kassieren referenziert, nicht bei der Ausgabe.

**Schwere:** MITTEL -- Verwechslungsgefahr bei Bestellungen, besonders bei hohem Aufkommen.

---

### O3: Koch erhaelt keine Bestelldetails

**Betroffene Elemente:** "Koch informieren" (Angestellter), "Mahlzeit zuzubereiten" (Koch, Message Start)

**Beschreibung:** Der Koch erhaelt eine Nachricht "Mahlzeit zuzubereiten", aber es ist nicht modelliert, wie die konkreten Bestelldetails (welches Gericht, Sonderwuensche) uebermittelt werden. Die Nachricht allein reicht nicht -- es braucht einen Datenobjekt-Bezug oder eine Referenz auf die Bestellung.

**Schwere:** NIEDRIG -- Eher ein Modellierungsdefizit als ein Prozessfehler; in der Praxis existiert ein Bestellzettel oder Display.

---

## 3. Effizienz-Probleme

### E1: Fehlende Parallelisierung von Kassieren und Koch-Informieren

**Betroffene Elemente:** "Geld kassieren" -> "Pieper einstellen" -> "Pieper uebergeben" -> "Koch informieren"

**Beschreibung:** Der Koch wird erst informiert, NACHDEM der Pieper eingestellt und uebergeben wurde. Die Kuechenvorbereitung koennte bereits parallel zum Pieper-Handling beginnen. Die aktuelle sequenzielle Anordnung verzoegert die Essenszubereitung unnoetig.

**Schwere:** HOCH -- Direkte Auswirkung auf die Wartezeit des Kunden. Bei einer Zubereitungszeit von z.B. 10 Minuten koennten 2-3 Minuten gespart werden, wenn der Koch sofort nach Bestelleingang informiert wird.

---

### E2: Pieper-Handling ist ueberkomplex modelliert

**Betroffene Elemente:** "Pieper einstellen", "Pieper uebergeben", "Pieper entgegennehmen", "Pieper ausloesen"

**Beschreibung:** Der Pieper-Prozess umfasst vier separate Aktivitaeten/Events ueber zwei Lanes. In der Praxis ist "Pieper einstellen" und "Pieper uebergeben" oft ein einziger Handgriff. Die Granularitaet ist fuer ein Prozessmodell dieses Abstraktionsniveaus zu fein.

**Schwere:** NIEDRIG -- Kein funktionaler Fehler, aber unnoetige Komplexitaet im Modell, die die Lesbarkeit reduziert.

---

### E3: Gast wartet passiv ohne Statusinfo

**Betroffene Elemente:** Gast-Lane zwischen "Pieper entgegennehmen" und "Essen abholen"

**Beschreibung:** Der Gast hat keinerlei Interaktionsmoeglichkeit waehrend der Wartezeit. Es gibt kein zwischengeschaltetes Feedback (z.B. Bestellstatus-Anzeige, geschaetzte Wartezeit). Der Prozess modelliert nur das finale Signal "Essen abholbereit".

**Schwere:** NIEDRIG -- Eher ein UX-Problem als ein Prozessfehler, aber relevant fuer Kundenzufriedenheit.

---

### E4: Keine Batch-Verarbeitung / Parallelitaet bei Mehrfachbestellungen

**Betroffene Elemente:** Koch-Pool

**Beschreibung:** Der Koch-Prozess ist als einzelne Instanz modelliert (ein Start, ein Ende). Es gibt kein Multi-Instance-Pattern oder eine Warteschlange. Bei mehreren gleichzeitigen Bestellungen ist unklar, wie der Koch priorisiert oder parallelisiert.

**Schwere:** MITTEL -- In der Praxis arbeitet eine Kueche an mehreren Bestellungen gleichzeitig; das Modell bildet das nicht ab.

---

## Zusammenfassung

| Kategorie | ID | Problem | Schweregrad |
|---|---|---|---|
| Strukturell | S1 | Endlosschleife bei Nicht-Erscheinen des Kunden | HOCH |
| Strukturell | S2 | Unvollstaendige Synchronisation beim Bezahlen | MITTEL |
| Strukturell | S3 | Kein Fehlerbehandlungspfad in der Kueche | HOCH |
| Strukturell | S4 | Event-based Gateway als Schleifenziel fragwuerdig | MITTEL |
| Strukturell | S5 | Kein Timeout auf Gast-Seite beim Warten | MITTEL |
| Organisatorisch | O1 | Angestellter als Single Point of Failure | HOCH |
| Organisatorisch | O2 | Keine Qualitaetskontrolle bei Ausgabe | MITTEL |
| Organisatorisch | O3 | Fehlende Bestelldetails an Koch | NIEDRIG |
| Effizienz | E1 | Koch wird zu spaet informiert (keine Parallelisierung) | HOCH |
| Effizienz | E2 | Pieper-Handling uebergranular modelliert | NIEDRIG |
| Effizienz | E3 | Kein Statusfeedback fuer wartenden Gast | NIEDRIG |
| Effizienz | E4 | Keine Mehrfachbestellungs-Modellierung beim Koch | MITTEL |

| Kategorie | Anzahl | davon HOCH | davon MITTEL | davon NIEDRIG |
|---|---|---|---|---|
| Strukturell | 5 | 2 | 3 | 0 |
| Organisatorisch | 3 | 1 | 1 | 1 |
| Effizienz | 4 | 1 | 1 | 2 |
| **Gesamt** | **12** | **4** | **5** | **3** |

---

*Analyse erstellt auf Basis direkter Bildinterpretation des BPMN-Diagramms (bpmn_rendered.png) ohne Zwischenformat.*
