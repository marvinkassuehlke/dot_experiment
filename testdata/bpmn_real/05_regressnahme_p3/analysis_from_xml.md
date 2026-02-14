# Prozessanalyse: Regressnahme (Participant 3)

Quelle: `from_xml.dot` (übersetzt aus Signavio BPMN 2.0 XML)

---

## 1. Strukturelle Probleme

### 1.1 Dead End: "Inkassoprozess einleiten" hat keinen Ausgang
Der Knoten `inkassoprozess_einleiten` ("Inkassoprozess einleiten") hat eine eingehende Kante von `weiterleitung_inkasso`, aber keine ausgehende Kante und kein End-Event. Der Prozess endet hier ohne explizites Ende. Im BPMN fehlt ein End-Event in der Lane "Inkasso" nach dieser Aufgabe.

### 1.2 Zwischenereignis mit drei ausgehenden Kanten ohne Gateway-Semantik
Der Knoten `zwischenereignis` ("Zwischenereignis") hat drei ausgehende Kanten:
- → `zahlungsverweigerung`
- → `zahlungseingang`
- → `timer`

Im BPMN-Quell-XML ist dieses Element als `intermediateCatchEvent` modelliert und enthält gleichzeitig eine `cancelEventDefinition` und eine `terminateEventDefinition`. Das ist semantisch fehlerhaft: Ein Intermediate Catch Event kann nicht gleichzeitig auf Cancel und Terminate warten und dabei drei alternative Pfade eröffnen. Korrekt wäre hier ein **Event-Based Gateway** (eventBasedGateway), das auf drei mögliche Ereignisse wartet (Zahlungseingang, Zahlungsverweigerung, Fristablauf). Stattdessen wurde ein einzelnes Zwischenereignis mit drei Ausgängen modelliert, was in BPMN 2.0 ungültig ist.

### 1.3 Fehlende Labels an Gateways
- `gw1` (erster Exclusive Gateway): Nur ein Ausgang ist beschriftet ("nein"). Der zweite Ausgang (→ Zahlungsanforderung) hat kein Label. Bei einem Exclusive Gateway sollten alle Ausgänge beschriftet sein, damit die Entscheidungslogik nachvollziehbar ist. Es fehlt zudem ein Default-Flow.
- `gw2` (zweiter Exclusive Gateway): Beide Ausgänge (→ Ende, → Weiterleitung an Inkasso) sind unbeschriftet. Die Entscheidungskriterien sind völlig unklar.

### 1.4 Fehlende Gateway-Frage am ersten Gateway
Der erste Gateway folgt auf "Fall prüfen", aber es ist nicht erkennbar, welche Frage entschieden wird. Vermutlich: "Ist Regress berechtigt?" — aber die Benennung fehlt. Die Kante "nein" führt zum Ende, der Ja-Fall hat kein Label.

### 1.5 Task "Verweigerung berechtigt" ist keine Aktivität
Der Knoten `verweigerung_berechtigt` ("Verweigerung berechtigt") klingt nach einem Prüfergebnis/Zustand, nicht nach einer Tätigkeit. Im BPMN ist es als generischer Task modelliert. Besser wäre z.B. "Berechtigung der Verweigerung prüfen" als Aktivitätsname, und das Ergebnis über das folgende Gateway abgebildet.

---

## 2. Organisatorische Probleme

### 2.1 Lane "Inkasso" enthält nur eine einzige Aufgabe
Die Lane `cluster_inkasso` ("Inkasso") enthält ausschließlich den Knoten `inkassoprozess_einleiten`. Das deutet auf eine unvollständige Modellierung hin: Entweder gehört der Inkasso-Prozess in einen separaten (Sub-)Prozess und sollte als Call Activity referenziert werden, oder die Lane benötigt weitere Schritte und ein End-Event.

### 2.2 Regressstelle trägt die gesamte Prozesslast
Alle 8 Tasks, alle Gateways, alle Events (bis auf das Inkasso) liegen in der Lane "Regressstelle". Die Abteilung ist für Fallprüfung, Zahlungsanforderung, Zahlungseingang, Verbuchung, Verweigerungsprüfung und Weiterleitung zuständig. Es fehlt die Differenzierung, ob einzelne Aufgaben (z.B. "Zahlung verbuchen") nicht besser einer Buchhaltungs-Lane zugeordnet wären.

### 2.3 Keine Interaktion mit dem Gegner (Regressschuldner)
Der Prozess zeigt keine Message Flows oder Interaktionen mit der gegnerischen Partei. Die "Zahlungsanforderung" wird gesendet, aber es gibt keinen modellierten Empfänger. "Zahlungseingang" und "Zahlungsverweigerung" werden als Reaktion erwartet, aber die Kommunikation mit dem Schuldner ist nicht abgebildet.

---

## 3. Effizienz-Probleme

### 3.1 Kein Wiedervorlagemechanismus nach Zahlungsanforderung
Nach "Zahlungsanforderung" wird sofort auf ein Zwischenereignis gewartet. Im XML gibt es zwar ein Datenobjekt "Wiedervorlage" (dataObjectReference), aber es ist nur über eine DataOutputAssociation angebunden und hat keinen Einfluss auf den Kontrollfluss. Es fehlt ein Eskalationspfad oder eine Erinnerungsschleife (z.B. erneute Mahnung), bevor direkt an Inkasso übergeben wird.

### 3.2 Kein Rückweg nach Fristverstreichung (Timer)
Der Timer-Pfad (30 Tage) führt direkt zu "Weiterleitung an Inkasso", ohne dass zuvor eine erneute Kontaktaufnahme oder Mahnung stattfindet. In einem realen Regressprozess gibt es typischerweise Mahnstufen, bevor Inkasso eingeleitet wird.

### 3.3 Keine Teilzahlungsbehandlung
Der Prozess kennt nur "Zahlungseingang" (→ verbuchen → Ende) oder "Zahlungsverweigerung" (→ Berechtigung prüfen). Teilzahlungen, Ratenzahlungen oder Vergleichsangebote sind nicht modelliert. Der Prozess ist dadurch für reale Fälle zu vereinfacht.

### 3.4 Redundante Pfade zu "Weiterleitung an Inkasso"
Der Knoten `weiterleitung_inkasso` wird über zwei unabhängige Pfade erreicht:
1. `gw2` → `weiterleitung_inkasso` (Verweigerung nicht berechtigt)
2. `timer` → `weiterleitung_inkasso` (Fristablauf)

Das ist grundsätzlich korrekt modelliert (zwei Gründe für Inkasso-Übergabe). Allerdings fehlt ein zusammenführendes Gateway vor der Aufgabe, was in BPMN Best Practice wäre, um die Semantik explizit zu machen.

---

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturelle Probleme | 5 | hoch — insb. das falsche Zwischenereignis (1.2) und der Dead End (1.1) |
| Organisatorische Probleme | 3 | mittel — unvollständige Lane-Modellierung |
| Effizienz-Probleme | 4 | mittel — fehlende Eskalationsstufen und Sonderfälle |

Das schwerwiegendste Problem ist die Verwendung eines einzelnen Intermediate Catch Events mit drei Ausgängen statt eines Event-Based Gateways (1.2). Dies ist ein BPMN-Syntaxfehler, der in einer Process Engine nicht ausführbar wäre.
