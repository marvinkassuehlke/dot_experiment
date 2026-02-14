# Defekt-Analyse: Rechnungsfreigabe (from_image.dot)

## 1. Strukturelle Probleme

### Fehlender Pfad am XOR-Gateway
Der Entscheidungsknoten **"XOR\nBetrag < 1000?"** hat nur einen ausgehenden Pfad (`ja` -> "Automatische\nFreigabe"). Der `nein`-Pfad fehlt vollstaendig. Eine binaere Entscheidung (ja/nein) benoetigt zwingend zwei Ausgaenge. Rechnungen >= 1000 Euro haben keinen definierten Prozessweg -- sie enden effektiv als Dead End am Gateway.

### Unerreichbare / funktionslose Cluster
Die Cluster **"Abteilungsleiter"** und **"Geschaeftsfuehrung"** enthalten keine Aktivitaeten, sondern nur unsichtbare Platzhalter-Knoten (`AL_placeholder`, `GF_placeholder`). Kein einziger Prozesspfad fuehrt durch diese Lanes. Die Akteure sind im Graphen vorhanden, aber prozessual nicht eingebunden.

## 2. Organisatorische Probleme

### Unklare Verantwortlichkeiten
**"Abteilungsleiter"** und **"Geschaeftsfuehrung"** sind als Lanes definiert, haben aber keinerlei Aufgaben. Es ist unklar, welche Rolle sie im Freigabeprozess spielen -- insbesondere, da bei Rechnungen >= 1000 Euro typischerweise eine manuelle Freigabe durch Vorgesetzte erwartet wird. Die leeren Lanes deuten auf einen unvollstaendigen Prozess hin.

### Ueberlastung der Buchhaltung
Saemtliche Aktivitaeten (Erfassen, Freigabe, Buchung, Archivierung, Zahlung) liegen in der Lane **"Buchhaltung"**. Es gibt kein Vier-Augen-Prinzip und keine Eskalation an andere Akteure.

## 3. Effizienz-Probleme

Keine Effizienz-Probleme identifiziert. Der modellierte Happy Path (Betrag < 1000) ist linear und ohne unnoetige Schleifen oder Redundanzen aufgebaut. Die parallele Ausfuehrung von **"Buchung\nerstellen"** und **"Beleg\narchivieren"** ueber den AND-Split/Join ist sinnvoll.

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturell | 2 | Hoch (fehlender Pfad), Mittel (leere Cluster) |
| Organisatorisch | 2 | Hoch (keine Verantwortlichkeiten fuer AL/GF), Mittel (Buchhaltung-Ueberlastung) |
| Effizienz | 0 | -- |

Der schwerwiegendste Defekt ist der fehlende `nein`-Pfad am XOR-Gateway: Rechnungen ab 1000 Euro koennen im modellierten Prozess nicht bearbeitet werden.
