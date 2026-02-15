# Process Audit Report: Selbstbedienungsrestaurant

## Übersicht

| | High | Medium | Low | Gesamt |
|---|---|---|---|---|
| **Structural** | 3 | 4 | 3 | 10 |
| **Organizational** | 1 | 2 | 1 | 4 |
| **Efficiency** | 0 | 2 | 3 | 5 |
| **Gesamt** | **4** | **8** | **7** | **19** |

---

## Strukturelle Probleme

### F1 — Endlosschleife im Ausruf-Zyklus ohne Exit-Bedingung (HIGH)
**Elemente:** EventBasedGateway_1qyi8l9, IntermediateCatchEvent_0nhl104, Task_0rpvccw

Wenn der Gast nicht auf den Pieper reagiert und auch nicht auf Ausrufen erscheint, gibt es keinen Abbruchpfad. Der Prozess pendelt endlos zwischen 5-Minuten-Timer und Kunden ausrufen.

### F2 — Fehlender Pfad fuer nicht verfuegbare Gerichte oder Bestellaenderungen (HIGH)
**Elemente:** Gericht auswaehlen, Bestellung aufgeben

Kein Prozessweg vorgesehen, wenn ein Gericht nicht verfuegbar ist oder der Gast die Bestellung aendern moechte. Der Prozess geht linear zur Bezahlung.

### F6 — Inkonsistente Synchronisation beim Essen-Abholen mit zirkulaerer Abhaengigkeit (HIGH)
**Elemente:** IntermediateCatchEvent_1r5wlb4, Task_0o0pue9, IntermediateCatchEvent_1rch6yh, Task_1a48xz1

Der Gast muss abholen damit der Angestellte bemerkt dass er da ist, aber der Angestellte muss das Essen uebergeben damit der Gast es abholen kann. Zirkulaere Message-Flow-Abhaengigkeit.

### F3 — Kein Fehlerpfad bei Zahlungsproblemen (MEDIUM)
**Elemente:** Betrag bezahlen, Geld kassieren

Keine Modellierung fuer gescheiterte Kartenzahlung, unzureichendes Bargeld oder technische Probleme am Kassensystem.

### F4 — Message Flow 'Kunden ausrufen' ohne konkreten Empfaenger im Gast-Pool (MEDIUM)
**Elemente:** Task_0rpvccw, Pool_Gast

Der Message Flow zeigt auf den gesamten Gast-Pool statt auf einen konkreten Catch-Event. Der Gast hat keinen modellierten Reaktionspfad auf das Ausrufen.

### F5 — Bidirektionaler Message Flow zwischen Bezahlung und Kassieren semantisch fragwuerdig (MEDIUM)
**Elemente:** Task_1ng51gy, Task_12h2fs9

Hin- und Rueck-Message-Flow zwischen diesen Tasks suggeriert synchrone Interaktion, die ueber getrennte Send/Receive-Events sauberer modelliert waere.

### F7 — Kein Rueckkanal vom Koch bei Zubereitungsproblemen (MEDIUM)
**Elemente:** Koch informieren, Mahlzeit zubereiten

Koch-Pool hat keine Moeglichkeit, Probleme waehrend der Zubereitung zurueckzumelden (z.B. Zutaten fehlen, Geraeteausfall).

### F8 — Kein Abbruchpfad fuer vorzeitiges Verlassen des Restaurants (MEDIUM)
**Elemente:** Gast Pool gesamt

Der Gast kann den Prozess nicht vorzeitig abbrechen. Fuehrt bei Abbruch zu inkonsistentem Zustand im Angestellten-Pool.

### F9 — Intermediate Catch Event 'an der Reihe' ohne korrespondierenden Message Flow (LOW)
**Elemente:** IntermediateCatchEvent_1nu2fvu

Das Event hat keinen eingehenden Message Flow. Unklar, wer dem Gast signalisiert, dass er an der Reihe ist.

### F10 — Kein Fehlerbehandlungspfad im gesamten Prozess (LOW)
**Elemente:** Pool_Gast, Pool_Angestellter, Pool_Koch

Durchgaengig fehlen Error-Events, Compensation-Handler oder Exception-Flows fuer unerwartete Situationen.

---

## Organisatorische Probleme

### F11 — Angestellter ist Bottleneck mit zu vielen sequenziellen Aufgaben (HIGH)
**Elemente:** Pool_Angestellter

15 Knoten bzw. 8 separate Taetigkeiten konzentriert in einem Pool. Bei mehreren gleichzeitigen Bestellungen wird der Angestellte zum systemischen Engpass.

### F12 — Koch-Pool stark untermodelliert ohne Fehlerhandling (MEDIUM)
**Elemente:** Pool_Koch

Rein linearer Ablauf ohne Entscheidungen, Parallelisierung oder Fehlerbehandlung. Keine Priorisierung bei Mehrfachbestellungen.

### F13 — Kassensystem-Ausfall nicht behandelt (MEDIUM)
**Elemente:** Kassensystem, Bestellung eingeben, Geld kassieren

Kein Fallback-Prozess bei technischen Problemen. Beide kritischen Aktivitaeten haengen vom Kassensystem ab.

### F14 — Keine Qualitaetskontrolle bei der Essensausgabe (LOW)
**Elemente:** Essen in Durchreiche stellen, Essen uebergeben

Kein Pruefschritt ob die richtige Bestellung dem richtigen Gast zugeordnet wird. Verwechslungsgefahr bei hohem Aufkommen.

---

## Effizienz-Probleme

### F15 — Fehlende Parallelisierung zwischen Pieper-Handling und Kuechen-Benachrichtigung (MEDIUM)
**Elemente:** Geld kassieren, Pieper einstellen, Pieper uebergeben, Koch informieren

Koch-Information koennte parallel zur Pieper-Ausgabe erfolgen statt sequenziell danach. Die Bestellung ist bereits im Kassensystem erfasst.

### F16 — Pieper-Handling verursacht manuellen Overhead (MEDIUM)
**Elemente:** Pieper einstellen, Pieper uebergeben, Pieper entgegennehmen

3 separate manuelle Prozessschritte fuer Pieper-Management. Digitale Benachrichtigung (App, Bildschirm) wuerde Durchlaufzeit und Handling-Aufwand reduzieren.

### F17 — Ping-Pong zwischen Koch und Angestelltem vermeidbar (LOW)
**Elemente:** Angestellten informieren, Pieper ausloesen

Koch informiert Angestellten manuell, der dann Pieper ausloest. Koennte durch direkten Sensor/Knopfdruck am Pieper-System ersetzt werden.

### F18 — Wartezeit passiv modelliert ohne Kapazitaetssteuerung (LOW)
**Elemente:** an der Reihe

Keine aktive Steuerung der Wartezeit oder Lastverteilung (z.B. zweite Kasse oeffnen bei Stosszeiten).

### F19 — Doppelter Uebergabeschritt zwischen Kueche und Ausgabe (LOW)
**Elemente:** Essen in Durchreiche stellen, Essen uebergeben

Bei Self-Service-Konzept koennte der Gast das Essen direkt an einer Ausgabetheke abholen, ohne den Angestellten als Mittelsmann.

---

## Methodik

Dieser Report wurde mit dem **Process Audit Skill** erstellt, der eine Dual-Perspective-Analyse durchführt:

1. **Strukturelle Analyse**: Übersetzung des BPMN-XML in Mermaid → Graph-basierte Defekterkennung (Gateway-Typen, Topologie, Message Flows, Synchronisation)
2. **Direkte Analyse**: Bildbasierte Prozessbewertung (Business-Logik, Governance, Szenarien, Organisationsdesign)
3. **Synthese**: Zusammenführung beider Perspektiven mit Deduplizierung

**Quellen**: bpmn_rendered.png, Selbstbedienungsrestaurant.bpmn (Dual-Input)

**Overlap-Rate**: 26% (5 von 19 Findings wurden von beiden Perspektiven gefunden). Der niedrige Overlap deutet darauf hin, dass die beiden Perspektiven stark komplementäre Erkenntnisse liefern — typisch für komplexe Multi-Pool-Prozesse mit vielen Message Flows.
