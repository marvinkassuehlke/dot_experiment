# Prozessanalyse: Warenversand Hardware-Haendler

## Prozessbeschreibung

Der Prozess beschreibt den Warenversand eines Hardware-Haendlers. Er beginnt mit dem Startereignis **"Artikel zu versenden"** im Sekretariat und endet mit dem Endereignis **"Warenversand vorbereitet"** beim Lagerarbeiter.

**Beteiligte Rollen (Lanes):**
- Leiter Logistik
- Sekretariat
- Lagerarbeiter

**Prozessablauf:**
1. Startereignis "Artikel zu versenden" (Sekretariat)
2. Paralleles Gateway (AND-Split): Zwei parallele Straenge werden gestartet
3. Strang 1 (Sekretariat): "Versandart klaeren" -> XOR-Gateway "Sonderversand?"
   - Ja: "Angebote von 3 Spediteuren einholen" -> "Spediteur beauftragen" -> XOR-Join
   - Nein: Weiter zu inklusivem Gateway (Kreis mit O-Markierung)
4. Strang 2 (Lagerarbeiter): "Ware verpacken"
5. Vom inklusiven Gateway (bei "nein" / kein Sonderversand):
   - Pfad "immer": "Paketschein ausfuellen" -> inklusives Join-Gateway
   - Pfad "Versicherung erforderlich": "Versicherung abschliessen" (Leiter Logistik) -> inklusives Join-Gateway
6. XOR-Join im Sekretariat sammelt Sonderversand- und Normalversand-Pfade
7. AND-Join beim Lagerarbeiter synchronisiert beide parallelen Straenge
8. "Ware bereitstellen" (Lagerarbeiter)
9. Endereignis "Warenversand vorbereitet"

---

## 1. Strukturelle Probleme

### 1.1 Inklusives Gateway ohne explizite Default-Semantik
**Betroffene Elemente:** Inklusives (OR-)Gateway nach dem "nein"-Pfad von "Sonderversand?"
**Beschreibung:** Das inklusive Gateway hat zwei ausgehende Pfade: "immer" und "Versicherung erforderlich". Der Pfad "immer" suggeriert, dass "Paketschein ausfuellen" stets ausgefuehrt wird. Der Pfad "Versicherung erforderlich" fuehrt zu "Versicherung abschliessen". Grundsaetzlich ist das Muster korrekt -- ein inklusives Gateway erlaubt, dass einer oder beide Pfade aktiv sind. Allerdings fehlt eine klare Bedingung fuer "Versicherung erforderlich" (z.B. Warenwert > X EUR). Ohne definierte Bedingung ist die Ausfuehrungssemantik mehrdeutig.
**Schwere:** Mittel

### 1.2 Inklusives Join-Gateway: Synchronisationsproblem
**Betroffene Elemente:** Inklusives Join-Gateway nach "Paketschein ausfuellen" und "Versicherung abschliessen"
**Beschreibung:** Ein inklusives Join-Gateway muss zur Laufzeit wissen, welche eingehenden Pfade aktiv sind, um korrekt zu synchronisieren. In vielen BPMN-Engines ist das technisch schwierig umzusetzen und fehleranfaellig. Wenn die Engine nicht korrekt erkennt, dass der Versicherungs-Pfad nicht aktiviert wurde, wartet das Join-Gateway ewig (Deadlock). Das ist ein bekanntes Anti-Pattern bei inklusiven Gateways.
**Schwere:** Hoch

### 1.3 Fehlender Pfad: Was passiert bei Sonderversand nach Spediteur-Beauftragung?
**Betroffene Elemente:** "Spediteur beauftragen" -> XOR-Join -> AND-Join
**Beschreibung:** Wenn Sonderversand gewaehlt wird, werden "Angebote von 3 Spediteuren einholen" und "Spediteur beauftragen" ausgefuehrt. Dieser Pfad fuehrt direkt zum XOR-Join und dann zum AND-Join. Es fehlt jedoch: Wird bei Sonderversand ebenfalls ein Paketschein ausgefuellt? Wird eine Versicherung geprueft? Der Sonderversand-Pfad umgeht die gesamte Paketschein-/Versicherungslogik. Das koennte beabsichtigt sein (der Spediteur kuemmert sich darum), ist aber nicht dokumentiert und potenziell ein fachlicher Fehler.
**Schwere:** Mittel

### 1.4 Kein Fehlerbehandlungspfad
**Betroffene Elemente:** Gesamter Prozess
**Beschreibung:** Es gibt keinen einzigen Fehler- oder Eskalationspfad. Was passiert, wenn kein Spediteur verfuegbar ist? Was wenn die Versicherung abgelehnt wird? Was wenn die Ware nicht verpackt werden kann (defekt, fehlt)? Ein Warenversandprozess ohne jegliche Ausnahmebehandlung ist in der Praxis nicht robust.
**Schwere:** Hoch

---

## 2. Organisatorische Probleme

### 2.1 Leiter Logistik nur fuer eine einzige Aufgabe
**Betroffene Elemente:** Lane "Leiter Logistik", Task "Versicherung abschliessen"
**Beschreibung:** Der Leiter Logistik hat im gesamten Prozess nur eine einzige Aufgabe: "Versicherung abschliessen". Diese wird zudem nur bedingt ausgefuehrt (nur bei Versicherungsbedarf und nur bei Normalversand). Es stellt sich die Frage, ob eine Fuehrungskraft die richtige Rolle fuer diesen operativen Schritt ist. Das Abschliessen einer Versicherung koennte vom Sekretariat erledigt werden, was einen Lane-Wechsel (und damit organisatorische Komplexitaet) einsparen wuerde.
**Schwere:** Niedrig

### 2.2 Bottleneck: Sekretariat traegt die Hauptlast
**Betroffene Elemente:** Lane "Sekretariat" -- Versandart klaeren, Sonderversand-Entscheidung, Angebote einholen, Spediteur beauftragen, Paketschein ausfuellen
**Beschreibung:** Das Sekretariat fuehrt 5 von 7 operativen Aktivitaeten aus. Es ist fuer Versandart-Klaerung, Angebotseinholung, Spediteur-Beauftragung UND Paketschein-Ausfuellung zustaendig. Bei hohem Versandvolumen wird das Sekretariat zum Engpass. Besonders kritisch: "Angebote von 3 Spediteuren einholen" ist eine potenziell zeitintensive Aufgabe, die den gesamten Prozess blockiert.
**Schwere:** Mittel

### 2.3 Keine Freigabe-/Vier-Augen-Kontrolle
**Betroffene Elemente:** "Spediteur beauftragen"
**Beschreibung:** Die Beauftragung eines Spediteurs (potenziell kostenintensiv) erfolgt direkt durch das Sekretariat ohne erkennbare Freigabe durch den Leiter Logistik oder eine andere Instanz. Bei hohen Versandkosten waere eine Genehmigungsschleife sinnvoll.
**Schwere:** Niedrig

---

## 3. Effizienz-Probleme

### 3.1 "Angebote von 3 Spediteuren einholen" ist sequenzieller Blocker
**Betroffene Elemente:** Task "Angebote von 3 Spediteuren einholen"
**Beschreibung:** Das Einholen von drei Angeboten ist typischerweise ein zeitaufwaendiger Schritt (Stunden bis Tage). Er liegt auf dem kritischen Pfad des Sonderversands und blockiert den gesamten Prozessfortschritt. Es fehlt jede Angabe, ob die Angebote parallel oder sequenziell eingeholt werden. Ausserdem: Wird wirklich bei jedem Sonderversand neu angefragt, oder gibt es Rahmenvertraege? Der Prozess suggeriert, dass jedes Mal von Null begonnen wird.
**Schwere:** Hoch

### 3.2 Parallelisierung: "Ware verpacken" vs. "Versandart klaeren"
**Betroffene Elemente:** AND-Split nach Startereignis, "Ware verpacken", "Versandart klaeren"
**Beschreibung:** Die Parallelisierung von "Ware verpacken" und "Versandart klaeren" ist grundsaetzlich gut modelliert. Allerdings: Wenn sich herausstellt, dass ein Sonderversand noetig ist, koennte die Art der Verpackung davon abhaengen (z.B. andere Palettierung fuer Spedition vs. Paketdienst). Der Lagerarbeiter verpackt moeglicherweise falsch, weil die Versandart noch nicht feststeht. Die Parallelisierung birgt hier ein fachliches Risiko.
**Schwere:** Mittel

### 3.3 Fehlende Automatisierungspotenziale
**Betroffene Elemente:** "Paketschein ausfuellen", "Versandart klaeren"
**Beschreibung:** "Paketschein ausfuellen" und "Versandart klaeren" sind als manuelle Tasks modelliert (keine Service-Task-Markierung). In modernen Logistikprozessen werden Paketscheine automatisch aus dem ERP-System generiert, und die Versandart kann regelbasiert bestimmt werden (Gewicht, Groesse, Zielort). Der Prozess bildet keine Automatisierung ab.
**Schwere:** Niedrig

### 3.4 Kein Rueckkopplungsmechanismus bei Angebotsvergleich
**Betroffene Elemente:** "Angebote von 3 Spediteuren einholen" -> "Spediteur beauftragen"
**Beschreibung:** Zwischen dem Einholen der Angebote und der Beauftragung fehlt ein expliziter Vergleichs-/Entscheidungsschritt. Der Prozess suggeriert, dass die Auswahl des Spediteurs implizit geschieht. Ein transparenter Vergleichsschritt (evtl. mit Freigabe) wuerde die Nachvollziehbarkeit erhoehen.
**Schwere:** Niedrig

---

## Zusammenfassungstabelle

| Kategorie | ID | Problem | Schwere |
|---|---|---|---|
| Strukturell | 1.1 | Inklusives Gateway ohne explizite Bedingungsdefinition | Mittel |
| Strukturell | 1.2 | Inklusives Join-Gateway: Deadlock-Risiko | Hoch |
| Strukturell | 1.3 | Sonderversand umgeht Paketschein/Versicherung | Mittel |
| Strukturell | 1.4 | Keine Fehler-/Ausnahmebehandlung | Hoch |
| Organisatorisch | 2.1 | Leiter Logistik unterausgelastet (1 Task) | Niedrig |
| Organisatorisch | 2.2 | Sekretariat als Bottleneck (5 von 7 Tasks) | Mittel |
| Organisatorisch | 2.3 | Keine Freigabe bei Spediteur-Beauftragung | Niedrig |
| Effizienz | 3.1 | Angebotseinholung als sequenzieller Blocker | Hoch |
| Effizienz | 3.2 | Parallelisierung birgt Verpackungsrisiko | Mittel |
| Effizienz | 3.3 | Fehlende Automatisierung (Paketschein, Versandart) | Niedrig |
| Effizienz | 3.4 | Kein expliziter Angebotsvergleich | Niedrig |

| Kategorie | Anzahl | davon Hoch | davon Mittel | davon Niedrig |
|---|---|---|---|---|
| Strukturelle Probleme | 4 | 2 | 2 | 0 |
| Organisatorische Probleme | 3 | 0 | 1 | 2 |
| Effizienz-Probleme | 4 | 1 | 1 | 2 |
| **Gesamt** | **11** | **3** | **4** | **4** |
