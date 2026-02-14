# Prozessanalyse: Regressnahme (Participant 2)

## 1. Strukturelle Probleme

### 1.1 Fehlende Sequence-Flow-Referenzen (4 Defekte)

**sequenceFlow sid-3821CAD9: kein sourceRef**
Der Sequence Flow zum Timer-Event "30 Tage" hat im XML kein `sourceRef`-Attribut. Aus dem Diagramm-Layout ergibt sich, dass dieser Flow vermutlich vom Event-Based Gateway ausgehen sollte. Ohne sourceRef ist der Timer "30 Tage" de facto unerreichbar -- der Pfad zur "Wiedervorlage Zahlungsanforderung bearbeiten" wird nie ausgeloest.

**sequenceFlow sid-2EDECBB4: kein targetRef**
Der ausgehende Flow von "Zahlungseingang verbuchen" hat kein Ziel. Der Knoten "Zahlungseingang verbuchen" ist damit ein **Dead End**: nach der Verbuchung endet der Prozess undefiniert, ohne ein End-Event zu erreichen. Aus dem Diagramm-Layout (Waypoints enden bei x=1211, y=245, nahe dem XOR-Merge-Gateway) laesst sich vermuten, dass der Flow zum Merge-Gateway vor "Regress beendet" fuehren sollte.

**sequenceFlow sid-0DF52C12 ("nein"): kein targetRef**
Der "nein"-Ausgang des XOR-Gateways nach "Widerspruch gerechtfertigt" hat kein Ziel. Das bedeutet: Wenn ein Widerspruch als nicht gerechtfertigt bewertet wird, ist unklar was passiert. Aus dem Layout (Waypoints enden bei x=1198, y=470, nahe dem XOR-Merge vor Inkasso) laesst sich vermuten, dass bei ungerechtfertigtem Widerspruch der Inkasso-Pfad eingeschlagen werden sollte.

**sequenceFlow sid-6EFCA0DD ("ja"): kein targetRef**
Der "ja"-Ausgang desselben XOR-Gateways hat ebenfalls kein Ziel. Wenn der Widerspruch als gerechtfertigt bewertet wird, ist der weitere Prozessverlauf undefiniert. Aus dem Layout (Waypoints enden bei x=1219, y=284, nahe dem XOR-Merge-Gateway vor End-Event) laesst sich vermuten, dass bei gerechtfertigtem Widerspruch der Regress beendet werden sollte.

### 1.2 Dead Ends

- **"Zahlungseingang verbuchen"**: Ausgehender Flow hat kein targetRef -- Prozess endet undefiniert.
- **XOR-Gateway nach "Widerspruch gerechtfertigt"**: Beide Ausgaenge (ja/nein) haben kein targetRef -- alle Pfade durch dieses Gateway enden undefiniert.

### 1.3 Unerreichbarer Knoten

- **Timer "30 Tage"**: Der eingehende Sequence Flow hat kein sourceRef. Damit ist der gesamte Pfad Timer -> "Wiedervorlage Zahlungsanforderung bearbeiten" -> XOR-Merge -> "Auftrag an Inkasso erstellen" -> End "Inkassostelle platziert" potenziell unerreichbar (abhaengig davon, ob die Laufzeitumgebung den fehlenden sourceRef kompensiert).

### 1.4 Event-Based Gateway mit falschem Event-Typ

Das Event-Based Gateway (`ebg_nach_zahlung`) hat zwei ausgehende Pfade:
- "Vn widerspricht" (Message Intermediate Catch Event) -- korrekt fuer Event-Based Gateway
- Conditional Intermediate Catch Event (ohne Label) -- korrekt fuer Event-Based Gateway

Zusaetzlich sollte laut Diagramm-Layout auch der Timer "30 Tage" vom Event-Based Gateway ausgehen (3 Alternativen). Aber der zugehoerige Sequence Flow ist defekt (kein sourceRef). Wenn man diesen Defekt gedanklich korrigiert, haette das Event-Based Gateway drei ausgehende Pfade (Message, Timer, Conditional), was semantisch valide waere.

### 1.5 Task-Benennung als Zustand statt Aktivitaet

Der Knoten **"Widerspruch gerechtfertigt"** ist als Task modelliert, liest sich aber wie ein Zustand oder eine Entscheidung, nicht wie eine Taetigkeit. Ein Task sollte eine ausfuehrbare Aktivitaet beschreiben (z.B. "Widerspruch pruefen"), waehrend die Entscheidung ob er gerechtfertigt ist, im nachfolgenden XOR-Gateway getroffen werden sollte.

## 2. Organisatorische Probleme

### 2.1 Einzelner Pool ohne Lanes

Der gesamte Prozess laeuft in einem einzigen Pool "Sachbearbeiter" ohne weitere Lane-Unterteilung. Bei einem Regressnahme-Prozess waere zu erwarten, dass weitere Akteure beteiligt sind:
- Der **Versicherungsnehmer (VN)** empfaengt die Zahlungsaufforderung und kann widersprechen
- Die **Inkassostelle** empfaengt den Auftrag
- Ggf. eine **Rechtsabteilung** fuer die Pruefung des Widerspruchs

Das Fehlen dieser Akteure als eigene Pools/Lanes macht Verantwortlichkeiten und Schnittstellen unklar.

### 2.2 Bottleneck "Sachbearbeiter"

Alle 6 Tasks liegen beim gleichen Akteur. Der Sachbearbeiter ist fuer Pruefung, Zahlungsaufforderung, Zahlungsverbuchung, Wiedervorlage, Widerspruchsbewertung UND Inkasso-Beauftragung zustaendig. Das ist eine sehr breite Aufgabenpalette, die in der Praxis vermutlich auf verschiedene Rollen verteilt ist.

## 3. Effizienz-Probleme

### 3.1 Fehlende Eskalation bei Wiedervorlage

Der Pfad ueber "Wiedervorlage Zahlungsanforderung bearbeiten" fuehrt (ueber den XOR-Merge) direkt zu "Auftrag an Inkasso erstellen". Es fehlt eine Schleife zurueck zur Zahlungsaufforderung -- d.h. nach einer Wiedervorlage wird sofort eskaliert (Inkasso), ohne dem VN eine zweite Chance zur Zahlung zu geben. Das kann gewollt sein, wirkt aber im Vergleich zu typischen Mahnprozessen (mit mehreren Mahnstufen) ungewoehnlich.

### 3.2 Conditional Event ohne Label

Das Conditional Intermediate Catch Event (nach dem Event-Based Gateway) hat kein Label. Es ist unklar, welche Bedingung hier ueberwacht wird. Vermutlich handelt es sich um den Zahlungseingang. Ohne Label ist der Prozess fuer Dritte nicht nachvollziehbar.

### 3.3 Kein Default-Pfad am XOR "Regress noetig?"

Das Gateway "Regress noetig?" hat zwei benannte Ausgaenge (ja/nein). Fuer ein exklusives Gateway ist das grundsaetzlich korrekt, aber es fehlt eine Markierung des Default-Pfads. Bei einer technischen Implementierung (z.B. Camunda) kann das zu Problemen fuehren, wenn keine der Bedingungen zutrifft.

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturelle Probleme | 5 | Kritisch -- 4 fehlende Flow-Referenzen machen wesentliche Prozesspfade unvollstaendig |
| Organisatorische Probleme | 2 | Mittel -- fehlende Akteure und Rollenverteilung |
| Effizienz-Probleme | 3 | Niedrig bis Mittel -- betreffen Verstaendlichkeit und Prozessoptimierung |

Die gravierendsten Defekte sind die 4 fehlenden Sequence-Flow-Referenzen (sourceRef/targetRef). Diese fuehren dazu, dass von den 3 moeglichen Prozesspfaden nach dem Event-Based Gateway keiner ein definiertes Ende erreicht. Der Prozess ist in seiner aktuellen XML-Form nicht ausfuehrbar.
