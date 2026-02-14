# Defekt-Analyse: Rechnungsfreigabe (from_xml.dot)

## 1. Strukturelle Probleme

### Fehlender Pfad am XOR-Gateway
Der Entscheidungsknoten **"Betrag < 1000?"** (Gateway_XOR_Betrag) hat nur einen ausgehenden Pfad (`ja` -> "Automatische Freigabe"). Der `nein`-Pfad fehlt vollstaendig. Bei einer binaeren Entscheidung muessen beide Ausgaenge modelliert sein. Rechnungen mit einem Betrag >= 1000 Euro haben keinen definierten Prozessweg und enden als Dead End am Gateway.

### Unerreichbare / funktionslose Cluster
Die Cluster **"Abteilungsleiter"** und **"Geschaeftsfuehrung"** enthalten keine Aktivitaeten, sondern ausschliesslich unsichtbare Platzhalter-Knoten (`AL_placeholder`, `GF_placeholder`). Kein Prozesspfad fuehrt durch diese Lanes.

## 2. Organisatorische Probleme

### Unklare Verantwortlichkeiten
**"Abteilungsleiter"** und **"Geschaeftsfuehrung"** sind als Lanes angelegt, besitzen aber keinerlei Aufgaben. Ihre Rolle im Freigabeprozess ist nicht erkennbar. Typischerweise waere zu erwarten, dass Rechnungen >= 1000 Euro eine manuelle Freigabe durch den Abteilungsleiter oder die Geschaeftsfuehrung erfordern -- genau dieser Pfad fehlt.

### Ueberlastung der Buchhaltung
Alle Aktivitaeten -- **"Rechnung erfassen"**, **"Automatische Freigabe"**, **"Buchung erstellen"**, **"Beleg archivieren"**, **"Zahlung veranlassen"** -- liegen ausschliesslich in der Lane **"Buchhaltung"**. Es gibt keine Aufgabenteilung mit anderen Akteuren und kein Vier-Augen-Prinzip.

## 3. Effizienz-Probleme

Keine Effizienz-Probleme identifiziert. Der modellierte Happy Path ist linear und sinnvoll strukturiert. Die parallele Ausfuehrung von **"Buchung erstellen"** und **"Beleg archivieren"** ueber den AND-Split/Join ist ein angemessenes Muster.

## Zusammenfassung

| Kategorie | Anzahl | Schweregrad |
|-----------|--------|-------------|
| Strukturell | 2 | Hoch (fehlender Pfad), Mittel (leere Cluster) |
| Organisatorisch | 2 | Hoch (keine Verantwortlichkeiten fuer AL/GF), Mittel (Buchhaltung-Ueberlastung) |
| Effizienz | 0 | -- |

Der schwerwiegendste Defekt ist der fehlende `nein`-Pfad am XOR-Gateway: Rechnungen ab 1000 Euro haben keinen modellierten Prozessweg. Die leeren Lanes "Abteilungsleiter" und "Geschaeftsfuehrung" verstaerken den Verdacht, dass hier ein ganzer Prozessteil (manuelle Freigabe) nicht uebersetzt wurde.
