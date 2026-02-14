# Prozessanalyse: Regressnahme (Teilnehmer P1)

## 1. Strukturelle Probleme

### 1.1 Fehlende Kantenbeschriftung am Gateway "Möglichkeit besteht?"
Die Entscheidung `Möglichkeit besteht?` hat zwei ausgehende Pfade: einer ist mit "Ja" beschriftet (führt zu `Zahlungsaufforderung senden`), der andere Pfad (führt direkt zu `gw_merge_vorgang` und dann zu `Vorgang schließen`) ist **unbeschriftet**. Bei einem Exclusive Gateway müssen alle ausgehenden Kanten eindeutig benannt sein, damit die Entscheidungslogik nachvollziehbar ist. Hier fehlt vermutlich das Label "Nein".

### 1.2 End Event mit Aktivitäts-Semantik: "An den Inkasso-Dienstleister abgeben"
Das End Event `An den Inkasso-Dienstleister abgeben` beschreibt eine Handlung ("abgeben"), nicht einen Endzustand. In BPMN sollte ein End Event einen Ergebniszustand ausdrücken (z.B. "Regress an Inkasso übergeben" oder "Inkassoverfahren eingeleitet"). Besser wäre es, die Übergabe als Task zu modellieren und das End Event als reinen Abschluss-Marker zu nutzen (z.B. "Inkassoverfahren eingeleitet"). Alternativ wäre ein Message End Event (Nachricht an Inkasso-Dienstleister) korrekt.

### 1.3 Kein Default-Pfad am Gateway "Gerechtfertigt?"
Die Entscheidung `Gerechtfertigt?` hat genau zwei Ausgänge: "Ja" und "Nein". Für den Modellierungsstandard wäre ein Default-Pfad empfehlenswert, falls die Prüfung keinen eindeutigen Entscheid ergibt (z.B. "Teilweise gerechtfertigt" oder "Klärung erforderlich"). In der aktuellen Modellierung gibt es keinen Pfad für unklare Fälle.

### 1.4 Keine Fehlerbehandlung
Der gesamte Prozess enthält keinerlei Error Events oder Kompensationsflüsse:
- Was passiert, wenn `Zahlungsaufforderung senden` fehlschlägt (ungültige Adresse, Zustellung scheitert)?
- Was passiert, wenn `Regress prüfen` nicht abschließbar ist (fehlende Unterlagen)?
- Die Intermediate Catch Events (`Geld eingegangen`, `Frist abgelaufen`, `Widerspruch eingegangen`) decken zwar drei Szenarien ab, aber es fehlt eine Eskalation für den Fall, dass keines der Ereignisse innerhalb eines Gesamtzeitrahmens eintritt.

## 2. Organisatorische Probleme

### 2.1 Keine Lanes/Pools — Verantwortlichkeiten vollständig unklar
Der Prozess enthält keinerlei Swimlanes oder Pools. Es ist nicht erkennbar:
- Wer `Regress prüfen` durchführt (Sachbearbeiter? Jurist? Automatisiert?)
- Wer `Widerspruch prüfen` durchführt (derselbe Sachbearbeiter? Eine andere Abteilung?)
- Wer `Vorgang auf "Wiedervorlage" setzen` ausführt
- An wen `Zahlungsaufforderung senden` gerichtet ist (an den Verursacher? An eine Versicherung?)

Für einen Trainings-Prozess ist dies ein wesentlicher Mangel, da die Organisationsstruktur ein Kernbestandteil der BPMN-Modellierung ist.

### 2.2 Keine Angabe des Empfängers bei Nachrichtenereignissen
`Zahlungsaufforderung senden` (Message Throw) und `Geld eingegangen` / `Widerspruch eingegangen` (Message Catch) implizieren Kommunikation mit einem externen Akteur (Schuldner, Gegner). Dieser Akteur ist nirgends als Pool oder Teilnehmer modelliert. Die Nachrichtenflüsse hängen damit "in der Luft".

## 3. Effizienz-Probleme

### 3.1 Kein Wiederholungsmechanismus nach Fristablauf
Wenn `Frist abgelaufen` eintritt, geht der Prozess direkt zu `An den Inkasso-Dienstleister abgeben`. In der Praxis wäre es üblich, mindestens eine Mahnung oder eine zweite Zahlungsaufforderung zu senden, bevor der Fall an den Inkasso-Dienstleister eskaliert wird. Der Prozess enthält keine Schleife für Mahnverfahren.

### 3.2 Keine Teilzahlungslogik
Nach dem Event-Based Gateway gibt es nur den binären Ausgang `Geld eingegangen` (alles bezahlt, Vorgang schließen). Es fehlt die Behandlung von Teilzahlungen: Was passiert, wenn nur ein Teil des Regressbetrags eingeht? Der Prozess müsste dann eine Restforderung berechnen und erneut in den Wartezyklus eintreten.

### 3.3 Redundanter Merge-Gateway `gw_merge_vorgang`
Der Merge-Gateway `gw_merge_vorgang` sammelt zwei Pfade: (1) den "Nein"-Pfad von `Möglichkeit besteht?` und (2) den Pfad nach `Geld eingegangen`. Beide führen zum selben Ziel (`Vorgang schließen`). Semantisch ist dies korrekt, aber die Benennung bzw. das Fehlen jeglicher Aktivität zwischen `Möglichkeit besteht? -> Nein` und dem End Event deutet darauf hin, dass kein expliziter Abschluss-Schritt (z.B. "Vorgang dokumentieren", "Akte schließen") modelliert wurde. In der Praxis dürfte auch der Abschluss eines geprüften-aber-abgelehnten Regressfalls eine dokumentierte Handlung erfordern.

### 3.4 Asymmetrische Behandlung der Widerspruchsprüfung
Wenn der Widerspruch gerechtfertigt ist (`Gerechtfertigt? -> Ja`), wird der Vorgang direkt geschlossen — ohne dass ein Rückzug der Forderung, eine Benachrichtigung des Schuldners oder eine Dokumentation der Entscheidung als Task modelliert ist. Der Nein-Pfad führt immerhin zum Inkasso, aber auch dort fehlt ein expliziter Übergabe-Task.

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturell | 4 | Mittel bis Hoch |
| Organisatorisch | 2 | Hoch |
| Effizienz | 4 | Mittel |

Die gravierendsten Mängel sind das vollständige Fehlen von Lanes/Pools (keine Verantwortlichkeiten erkennbar) und die fehlende Kantenbeschriftung am Gateway `Möglichkeit besteht?`. Für einen Trainings-Teilnehmer sind die fehlende Fehlerbehandlung und die fehlende Mahnlogik erwartbare Vereinfachungen, aber die fehlenden Lanes und unbeschrifteten Gateway-Ausgänge sind grundlegende Modellierungsfehler.
