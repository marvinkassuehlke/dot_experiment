# Prozessanalyse: Selbstbedienungsrestaurant

Analysiert auf Basis der DOT-Datei `from_xml.dot`. Der Prozess modelliert eine Collaboration mit drei Pools: **Gast** (Nahrungsaufnahme), **Angestellter** (Bestellungsbearbeitung), **Koch** (Mahlzeitzubereitung).

---

## 1. Strukturelle Probleme

### 1.1 Endlosschleife ohne garantierte Terminierung (Angestellter-Pool)

Im Angestellter-Pool existiert ein Zyklus:

```
EventBasedGateway -> "5 Minuten" -> "Kunden ausrufen" -> EventBasedGateway
```

Das Event-Based Gateway wartet auf eines von zwei Ereignissen: "Kunde erscheint" (Message Event) oder "5 Minuten" (Timer Event). Falls der Timer-Pfad genommen wird, wird "Kunden ausrufen" ausgefuehrt und der Fluss kehrt zurueck zum Gateway.

**Problem:** Es gibt keine explizite Exit-Bedingung fuer diesen Zyklus. Wenn der Kunde nie erscheint (z.B. das Restaurant verlaesst, den Pieper nicht hoert), dreht die Schleife unbegrenzt: alle 5 Minuten wird der Kunde ausgerufen, ohne dass ein Abbruch modelliert ist. Es fehlt ein Timeout-Ende (z.B. "nach 3 Versuchen Bestellung stornieren").

### 1.2 Fehlende Fehlerbehandlung im Gast-Pool

Der Gast-Prozess ist ein reiner Happy Path: `Hunger festgestellt -> Restaurant betreten -> Gericht auswaehlen -> an der Reihe -> Bestellung aufgeben -> Betrag bezahlen -> Pieper entgegennehmen -> Essen abholbereit -> Essen abholen -> Mahlzeit verzehren -> Hunger gestillt`.

Es gibt keine Entscheidungen (kein Gateway, kein XOR-Split). Szenarien wie "gewuenschtes Gericht nicht verfuegbar", "Bezahlung scheitert" oder "Wartezeit zu lang, Gast verlässt Restaurant" sind nicht modelliert.

### 1.3 Message Flow "Kunden ausrufen" hat kein definiertes Ziel im Gast-Pool

Der Message Flow von "Kunden ausrufen" (Angestellter) zeigt im BPMN-XML auf den Participant `Gast` insgesamt (nicht auf ein spezifisches Catch-Event oder einen Task). Im Gast-Pool gibt es keinen korrespondierenden Empfangsknoten fuer diesen Ausruf. Der Gast-Prozess reagiert an keiner Stelle darauf. Das bedeutet: Der Ausruf verpufft prozessual -- der Gast hat keinen modellierten Empfang fuer diese Nachricht.

### 1.4 Bidirektionaler Message Flow zwischen "Betrag bezahlen" und "Geld kassieren"

Zwischen `Task_12h2fs9` ("Betrag bezahlen", Gast) und `Task_1ng51gy` ("Geld kassieren", Angestellter) existieren zwei Message Flows in entgegengesetzter Richtung. Das impliziert einen synchronen Austausch waehrend beider Tasks gleichzeitig aktiv sind. In BPMN ist das zulaessig, aber es erzeugt eine implizite Synchronisierungsabhaengigkeit, die nicht ueber Sequence Flows modelliert ist -- der Gast muss bei "Betrag bezahlen" warten, bis der Angestellte bei "Geld kassieren" angekommen ist, und umgekehrt.

---

## 2. Organisatorische Probleme

### 2.1 Bottleneck: Angestellter als zentraler Engpass

Der Angestellter-Pool hat mit 14 Knoten (8 Tasks, 1 Gateway, 3 Intermediate Events, 1 Start Event, 1 End Event) deutlich mehr Aktivitaeten als Koch (3 Tasks) oder Gast (7 Tasks). Der Angestellte muss:
- Bestellung entgegennehmen und eingeben
- Geld kassieren
- Pieper einstellen und uebergeben
- Koch informieren
- Auf Fertigmeldung warten
- Pieper ausloesen
- Ggf. wiederholt Kunden ausrufen
- Essen uebergeben

Das ist ein Single Point of Failure: Ein einzelner Angestellter bearbeitet den gesamten Bestellzyklus von Anfang bis Ende. Bei hohem Aufkommen staut sich alles bei diesem Akteur.

### 2.2 Keine Parallelisierung im Angestellter-Pool

Alle Tasks im Angestellter-Pool sind strikt sequentiell. Es gibt keinen Parallel Gateway. Beispielsweise koennten "Pieper einstellen" und "Koch informieren" theoretisch parallel laufen, sind aber sequentiell modelliert (`Pieper einstellen -> Pieper uebergeben -> Koch informieren`).

### 2.3 Koch hat keine Autonomie

Der Koch-Pool wird ausschliesslich durch eine Message von "Koch informieren" (Angestellter) gestartet und hat einen rein linearen Ablauf mit nur 3 Tasks. Der Koch hat keinen Einfluss auf Priorisierung, keine Rueckmeldung bei Problemen (fehlende Zutaten, Geraeteausfall) und keinen Feedback-Kanal zurueck zum Gast.

---

## 3. Effizienz-Probleme

### 3.1 Ping-Pong zwischen Gast und Angestellter bei der Essensuebergabe

Die Essensabholung erfordert mehrere Pool-uebergreifende Interaktionen in kurzer Folge:
1. "Pieper ausloesen" (Angestellter) -> "Essen abholbereit" (Gast) -- Signal
2. "Essen abholen" (Gast) -> "Kunde erscheint" (Angestellter) -- Ankunft
3. "Essen uebergeben" (Angestellter) -> "Essen abholen" (Gast) -- Essen

Das sind 3 Message Flows fuer einen einzigen logischen Vorgang (Essen uebergeben). Insbesondere der bidirektionale Flow zwischen "Essen abholen" und "Essen uebergeben" / "Kunde erscheint" ist redundant: Der Gast muss physisch zum Tresen kommen (Message "Ankunft"), dann bekommt er das Essen (Message "Essen"), das er aber im selben Task "Essen abholen" empfaengt, den er schon begonnen hat. Hier wuerde ein einfacheres Rendezvous-Muster genuegen.

### 3.2 Pieper-Handling ist aufwendig modelliert

Der Pieper durchlaeuft 4 Tasks ueber 2 Pools:
1. "Pieper einstellen" (Angestellter)
2. "Pieper uebergeben" (Angestellter) -> "Pieper entgegennehmen" (Gast)
3. "Pieper ausloesen" (Angestellter) -> "Essen abholbereit" (Gast)

Das Einstellen und Uebergeben des Piepers sind zwei separate Tasks, die in der Praxis ein einziger Handgriff sind. Die Granularitaet ist hier unnoetig hoch.

### 3.3 Unnoetige Wartezeit: "an der Reihe" ohne Parallelarbeit

Das Intermediate Event "an der Reihe" im Gast-Pool modelliert das Warten in einer Schlange. Waehrend dieser Wartezeit passiert prozessual nichts -- der Gast hat sein Gericht bereits ausgewaehlt. In der Realitaet koennten andere Prozessinstanzen (andere Gaeste) parallel bedient werden, was im BPMN-Modell nicht sichtbar ist. Das Event selbst ist korrekt, aber es fehlt die explizite Modellierung, dass der Angestellter-Pool mehrere Instanzen parallel abarbeitet.

### 3.4 Koch wird erst nach Pieper-Uebergabe informiert

Die Sequenz im Angestellter-Pool ist: `Geld kassieren -> Pieper einstellen -> Pieper uebergeben -> Koch informieren`. Der Koch beginnt erst mit der Zubereitung, nachdem der Pieper bereits an den Gast uebergeben wurde. Effizienter waere es, den Koch parallel zum Pieper-Handling zu informieren (oder sogar schon bei der Bestellungseingabe), um die Wartezeit des Gastes zu reduzieren.
