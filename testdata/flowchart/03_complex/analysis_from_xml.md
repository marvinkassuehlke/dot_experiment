# Analyse: Kreditantrag-Prozess (from_xml.dot)

## 1. Strukturelle Probleme

- **Endlosschleife bei "Nochmalige Pruefung" / "Ergebnis anders?"**: Der Knoten "Ergebnis anders?" hat nur eine ausgehende Kante: "nein" zurueck zu "Nochmalige Pruefung". Es fehlt die Kante fuer den Fall "ja". Der Zyklus "Nochmalige Pruefung" -> "Ergebnis anders?" -> "Nochmalige Pruefung" ist eine Endlosschleife ohne Exit-Bedingung.
- **Fehlender Pfad bei "Ergebnis anders?"**: Die Entscheidung hat nur einen Ausgang ("nein"). Der erwartete "ja"-Pfad fehlt vollstaendig. Dieser sollte vermutlich zu "Kredit genehmigen" oder zum End-Knoten "Abgelehnt" fuehren.
- **Unerreichbarer Knoten "Abgelehnt"**: Der End-Knoten "Abgelehnt" (`done_no`) ist deklariert, aber es existiert keine Kante, die zu ihm fuehrt. Er ist vollstaendig unerreichbar. Abgelehnte Kreditantraege koennen den Prozess nie ordnungsgemaess abschliessen.
- **Dead End bei "Ergebnis anders?"**: Da der einzige Ausgang zurueck in die Schleife fuehrt, ist der gesamte Teilgraph ab "Kredit ablehnen" eine Sackgasse -- man gelangt hinein, aber nie wieder heraus.

## 2. Organisatorische Probleme

- **Bottleneck bei "Alle Pruefungen bestanden?"**: Alle drei parallelen Pruefungspfade ("Schufa-Auskunft", "Einkommens-pruefung", "Sicherheiten-bewertung") konvergieren in diesem einen Entscheidungsknoten. Die Synchronisation der parallelen Pfade ist nicht explizit modelliert.
- **Bottleneck bei "Unterlagen pruefen"**: Sowohl der initiale Pfad als auch die Nachforderungsschleife fuehren durch diesen Knoten.
- **Unklare Verantwortlichkeiten**: Der Prozess definiert keine Lanes oder Cluster. Es bleibt offen, welche Abteilung oder Rolle fuer die einzelnen Pruefschritte, die Genehmigung oder die nochmalige Pruefung zustaendig ist.

## 3. Effizienz-Probleme

- **Parallelisierung unklar modelliert**: Von "Unterlagen vollstaendig?" gehen drei Kanten mit Label "ja" gleichzeitig zu "Schufa-Auskunft", "Einkommens-pruefung" und "Sicherheiten-bewertung". Dies soll parallele Ausfuehrung darstellen, aber GraphViz/DOT kennt kein Fork/Join-Konstrukt. Es fehlt eine explizite Synchronisations-Semantik (wie z.B. ein AND-Gateway in BPMN).
- **Endlose Wiederholungspruefung**: Abgelehnte Antraege geraten in eine Endlosschleife zwischen "Nochmalige Pruefung" und "Ergebnis anders?". Es gibt keinen Mechanismus fuer eine endgueltige Ablehnung, was den Prozess fuer abgelehnte Faelle vollstaendig blockiert.
- **Kein Abbruch- oder Eskalationspfad**: Nach einer Ablehnung existiert kein Weg, den Antrag endgueltig abzulehnen und den Kunden zu benachrichtigen. Der Prozess sieht nur die endlose Wiederholung der Pruefung vor.

## Zusammenfassung

Die Defekte in `from_xml.dot` sind identisch mit denen in `from_image.dot` fuer den Kreditantrag-Prozess: Beide Varianten haben dieselbe Endlosschleife bei der nochmaligen Pruefung, denselben unerreichbaren "Abgelehnt"-Knoten und denselben fehlenden "ja"-Pfad bei "Ergebnis anders?". Die Uebersetzungsfehler sind in beiden Quellen konsistent.
