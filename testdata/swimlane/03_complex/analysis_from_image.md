# Defekt-Analyse: swimlane/03_complex/from_image.dot

## 1. Strukturelle Probleme

### Fehlender Pfad: Kundenentscheidung nach Kostenvoranschlag

Nach `"Kostenvoranschlag erstellen"` (Technik) geht der Prozess direkt zu `"Kostenvoranschlag erhalten"` (Kunde) und dann zu `"Ende"`. Es fehlt die Entscheidung des Kunden, ob er den Kostenvoranschlag annimmt oder ablehnt. In der Realitaet muesste hier eine Verzweigung folgen:
- **Annahme**: Reparatur beauftragen --> `"Reparatur durchfuehren"` --> `"Reparatur erhalten"`
- **Ablehnung**: Prozess endet (ggf. mit Rueckgabe des Geraets)

Ohne diese Entscheidung ist der Kostenvoranschlag eine Sackgasse ohne Handlungsoption fuer den Kunden.

### Dead End: "Kostenvoranschlag erhalten"

Der Knoten `"Kostenvoranschlag erhalten"` fuehrt direkt zu `"Ende"`, ohne dass der Kunde eine Reaktion auf den Kostenvoranschlag zeigen kann. Der Prozess behandelt den Erhalt des Kostenvoranschlags als Abschluss, obwohl er eigentlich ein Zwischenschritt ist.

### Fehlende Lane: Recht/Rechtsabteilung

Im Kontext eines Reklamationsprozesses waere eine Lane fuer rechtliche Pruefung (z.B. Gewaehrleistungsrecht, Verbraucherschutz) erwartbar, insbesondere da der Knoten `"Gewaehr-leistung?"` eine rechtliche Entscheidung abbildet. Diese Entscheidung liegt im Modell in der Lane "Technik" -- ob das organisatorisch korrekt ist, haengt vom Unternehmen ab, ist aber zumindest diskussionswuerdig.

## 2. Organisatorische Probleme

### Bottleneck: "Reklamation aufnehmen" (Service)

Saemtliche Reklamationen -- unabhaengig von Typ und Komplexitaet -- muessen durch den Knoten `"Reklamation aufnehmen"` in der Service-Lane. Dieser Knoten ist der einzige Einstiegspunkt nach der Kundeneinreichung und damit ein potenzieller Engpass.

### Technik-Lane traegt die meiste Last

Die Lane "Technik" enthaelt 5 Knoten: `"Fehler analysieren"`, `"Gutachten erstellen"`, `"Gewaehr-leistung?"`, `"Kostenvoranschlag erstellen"`, `"Reparatur durchfuehren"`. Das ist die hoechste Knotendichte aller Lanes. Zudem sind die Aufgaben inhaltlich heterogen (Analyse, Dokumentation, Entscheidung, Kostenkalkulation, Ausfuehrung).

## 3. Effizienz-Probleme

### Keine Rueckkopplung nach Reparatur

Nach `"Reparatur durchfuehren"` (Technik) geht der Prozess direkt zu `"Reparatur erhalten"` (Kunde) und dann zu `"Ende"`. Es fehlt ein Qualitaetscheck oder eine Abnahme der Reparatur, bevor sie an den Kunden geht.

### Kein Feedback-Kanal fuer den Kunden

Der Kunde hat im gesamten Prozess nach `"Reklamation einreichen"` keine weitere aktive Rolle. Er "erhaelt" lediglich Ergebnisse (`"Kostenvoranschlag erhalten"`, `"Reparatur erhalten"`, `"Erstattung erhalten"`). Es gibt keinen modellierten Pfad fuer Rueckfragen, Ablehnung oder Eskalation.
