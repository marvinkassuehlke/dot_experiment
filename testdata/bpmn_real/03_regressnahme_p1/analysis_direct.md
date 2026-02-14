# Prozessanalyse: Regressnahme (Part 1)

**Quelle:** Direkte Bildanalyse von `bpmn_rendered.png`
**Methode:** Visuelle Inspektion ohne Zwischenformat

---

## Prozessuebersicht

Der Prozess beschreibt die Bearbeitung eines erkannten Regressanspruchs. Nach Pruefung wird eine Zahlungsaufforderung versendet, der Vorgang auf Wiedervorlage gesetzt und anschliessend auf eines von drei Ereignissen gewartet: Geldeingang, Widerspruch oder Fristablauf. Je nach Ereignis wird der Vorgang geschlossen, der Widerspruch geprueft oder an einen Inkasso-Dienstleister uebergeben.

---

## 1. Strukturelle Probleme

### 1.1 Fehlender "Nein"-Pfad am Gateway "Moeglichkeit besteht?"

- **Betroffenes Element:** Exklusives Gateway nach "Regress pruefen"
- **Beschreibung:** Das Gateway hat nur einen sichtbaren ausgehenden Pfad mit Label "Ja". Der "Nein"-Pfad (Regressmoeglichkeit besteht nicht) fehlt vollstaendig. Es gibt keinen Abbruchpfad, wenn die Pruefung ergibt, dass kein Regress moeglich ist.
- **Konsequenz:** Prozessinstanzen, bei denen kein Regress moeglich ist, haben kein definiertes Ende -- Dead End.
- **Schwere:** **Hoch** -- Jeder Fall ohne Regressmoeglichkeit bleibt im Prozess haengen.

### 1.2 Fehlende Eskalation / Schleife bei "Frist abgelaufen"

- **Betroffenes Element:** Timer-Event "Frist abgelaufen" und nachfolgendes XOR-Gateway
- **Beschreibung:** Nach Fristablauf fuehrt der Pfad zu einem XOR-Gateway, das direkt in "An den Inkasso-Dienstleister abgeben" muendet. Es gibt keine Zwischenschritte wie eine Mahnung, einen erneuten Kontaktversuch oder eine Eskalationspruefung. Der Prozess springt direkt von "keine Reaktion" zu "Inkasso".
- **Konsequenz:** Kein abgestuftes Mahnverfahren. Rechtlich problematisch, da in vielen Jurisdiktionen mindestens eine Mahnung vor Inkasso-Uebergabe erforderlich ist.
- **Schwere:** **Hoch** -- Potenzielle Rechtskonformitaetsprobleme.

### 1.3 Unklare Zusammenfuehrung bei "Nein" aus "Gerechtfertigt?"

- **Betroffenes Element:** XOR-Gateway "Gerechtfertigt?" -> Nein-Pfad
- **Beschreibung:** Wenn der Widerspruch als nicht gerechtfertigt bewertet wird (Nein), fuehrt der Pfad zu einem XOR-Gateway, das zusammen mit dem Pfad "Frist abgelaufen" in "An den Inkasso-Dienstleister abgeben" muendet. Das bedeutet: ein nicht gerechtfertigter Widerspruch fuehrt direkt zur Inkasso-Uebergabe, ohne dass der Schuldner ueber die Ablehnung des Widerspruchs informiert wird.
- **Konsequenz:** Fehlende Kommunikation mit dem Schuldner. Kein Bescheid ueber die Widerspruchsentscheidung.
- **Schwere:** **Mittel** -- Fehlender Prozessschritt (Ablehnungsbescheid).

### 1.4 Kein Ruecksprung nach Wiedervorlage bei teilweiser Zahlung

- **Betroffenes Element:** Message Event "Geld eingegangen" -> XOR-Gateway -> "Vorgang schliessen"
- **Beschreibung:** Wenn Geld eingeht, wird der Vorgang direkt geschlossen. Es gibt keine Pruefung, ob der vollstaendige Betrag eingegangen ist. Bei einer Teilzahlung wuerde der Vorgang faelschlicherweise als abgeschlossen betrachtet.
- **Konsequenz:** Regressforderungen koennen bei Teilzahlung als erledigt markiert werden, obwohl noch ein Restbetrag aussteht.
- **Schwere:** **Hoch** -- Finanzieller Verlust durch vorzeitiges Schliessen.

### 1.5 Zwei separate Endereignisse ohne Differenzierung

- **Betroffene Elemente:** Endereignis nach "Vorgang schliessen" und Endereignis nach "An den Inkasso-Dienstleister abgeben"
- **Beschreibung:** Beide Endereignisse sind als einfache End-Events modelliert (keine unterschiedlichen Typen). Im BPMN-Standard sollten unterschiedliche Prozessausgaenge klar differenziert werden, z.B. durch benannte Endereignisse oder unterschiedliche Event-Typen (Signal, Message, Terminate).
- **Konsequenz:** Bei Prozess-Monitoring und Reporting ist nicht sofort erkennbar, mit welchem Ergebnis der Prozess endete.
- **Schwere:** **Niedrig** -- Kosmetisch, aber relevant fuer Prozess-Monitoring.

---

## 2. Organisatorische Probleme

### 2.1 Keine Lanes / Rollen definiert

- **Betroffenes Element:** Gesamtes Diagramm
- **Beschreibung:** Der Prozess enthaelt keine Swimlanes. Es ist voellig unklar, wer "Regress pruefen" durchfuehrt, wer die "Zahlungsaufforderung senden" verantwortet, wer den "Widerspruch prueft" und wer die Inkasso-Uebergabe veranlasst. Im Regresskontext sind typischerweise Sachbearbeiter, Teamleiter (fuer Eskalationen), Rechtsabteilung (fuer Widersprueche) und ggf. Buchhaltung (fuer Zahlungseingaenge) beteiligt.
- **Konsequenz:** Keine klare Verantwortungszuordnung. Aufgaben koennen liegenbleiben oder doppelt bearbeitet werden.
- **Schwere:** **Hoch** -- Fundamentaler Modellierungsmangel fuer einen operativen Prozess.

### 2.2 Keine Vier-Augen-Pruefung bei Inkasso-Uebergabe

- **Betroffenes Element:** Task "An den Inkasso-Dienstleister abgeben"
- **Beschreibung:** Die Uebergabe an einen externen Inkasso-Dienstleister ist ein gravierender Schritt mit rechtlichen und finanziellen Implikationen. Im Prozess fehlt jede Form von Freigabe, Genehmigung oder Vier-Augen-Prinzip.
- **Konsequenz:** Ein einzelner Sachbearbeiter kann ohne Kontrolle Faelle an Inkasso uebergeben. Risiko fuer fehlerhafte Uebergaben.
- **Schwere:** **Mittel** -- Governance-Risiko.

### 2.3 "Widerspruch pruefen" ohne definierte Kompetenz

- **Betroffenes Element:** Task "Widerspruch pruefen" und Gateway "Gerechtfertigt?"
- **Beschreibung:** Die Pruefung, ob ein Widerspruch gerechtfertigt ist, erfordert juristische oder fachliche Kompetenz. Ohne Rollenzuordnung ist unklar, ob dieselbe Person, die die Zahlungsaufforderung verschickt hat, auch den Widerspruch beurteilt -- was einen Interessenkonflikt darstellen koennte.
- **Konsequenz:** Befangenheitsrisiko und moeglicherweise unqualifizierte Entscheidungen.
- **Schwere:** **Mittel** -- Qualitaetsrisiko bei der Widerspruchsbewertung.

---

## 3. Effizienz-Probleme

### 3.1 Keine Automatisierung bei Zahlungseingang

- **Betroffenes Element:** Message Event "Geld eingegangen"
- **Beschreibung:** Der Zahlungseingang wird als manuelles Message-Event modelliert. In der Praxis sollte ein Zahlungsabgleich (z.B. via SEPA-Referenz oder Buchungssystem) automatisiert erfolgen und den Prozess automatisch triggern.
- **Konsequenz:** Manuelle Ueberwachung von Zahlungseingaengen ist fehleranfaellig und zeitaufwaendig.
- **Schwere:** **Mittel** -- Vermeidbarer manueller Aufwand.

### 3.2 Kein Mahnstufenkonzept

- **Betroffenes Element:** Gesamter Pfad von "Zahlungsaufforderung senden" bis "An den Inkasso-Dienstleister abgeben"
- **Beschreibung:** Der Prozess kennt nur eine einzige Zahlungsaufforderung. Es gibt keine zweite Mahnung, keine Mahnstufen (1. Mahnung, 2. Mahnung, letzte Mahnung vor Inkasso). Der Prozess springt direkt von der ersten Zahlungsaufforderung zur Inkasso-Uebergabe.
- **Konsequenz:** Hoehere Inkasso-Kosten, da viele Faelle durch eine zweite Mahnung haetten geloest werden koennen. Schlechtere Kundenbeziehung.
- **Schwere:** **Hoch** -- Direkte Kosten- und Effizienzeinbusse.

### 3.3 Keine Parallelisierung bei Wiedervorlage

- **Betroffenes Element:** Task "Vorgang auf Wiedervorlage setzen" und nachfolgendes Event-Based Gateway
- **Beschreibung:** Nach dem Versand der Zahlungsaufforderung wird der Vorgang passiv auf Wiedervorlage gelegt. Es gibt keine parallelen Aktivitaeten wie z.B. eine automatische Erinnerung nach X Tagen, eine Bonitaetspruefung oder vorbereitende Massnahmen fuer den Inkasso-Fall.
- **Konsequenz:** Reine Wartezeit ohne wertschoepfende Aktivitaet. Potenzial fuer fruehzeitige Risikobewertung bleibt ungenutzt.
- **Schwere:** **Niedrig** -- Optimierungspotenzial, kein akuter Fehler.

### 3.4 Redundante Zusammenfuehrungs-Gateways

- **Betroffene Elemente:** Die beiden XOR-Zusammenfuehrungs-Gateways vor den Endereignissen
- **Beschreibung:** Vor "Vorgang schliessen" gibt es ein XOR-Merge, das den Pfad "Geld eingegangen" mit dem Pfad "Widerspruch gerechtfertigt = Ja" zusammenfuehrt. Vor "An den Inkasso-Dienstleister abgeben" gibt es ein XOR-Merge fuer "Frist abgelaufen" und "Widerspruch nicht gerechtfertigt". Die Gateways sind korrekt, aber die Tatsache, dass ein gerechtfertigter Widerspruch zum gleichen Ergebnis fuehrt wie ein Zahlungseingang (Vorgang schliessen), ist fachlich fragwuerdig -- ein gerechtfertigter Widerspruch sollte in eine andere Abwicklung muenden (z.B. Forderungsverzicht mit Dokumentation).
- **Konsequenz:** Fachlich unterschiedliche Ergebnisse werden gleich behandelt.
- **Schwere:** **Mittel** -- Fachliche Unschaerfe.

---

## Zusammenfassungstabelle

| Kategorie | ID | Problem | Schwere |
|---|---|---|---|
| **Strukturell** | 1.1 | Fehlender "Nein"-Pfad bei "Moeglichkeit besteht?" | Hoch |
| **Strukturell** | 1.2 | Keine Eskalationsstufe vor Inkasso bei Fristablauf | Hoch |
| **Strukturell** | 1.3 | Kein Ablehnungsbescheid bei unberechtigtem Widerspruch | Mittel |
| **Strukturell** | 1.4 | Keine Teilzahlungspruefung bei Geldeingang | Hoch |
| **Strukturell** | 1.5 | Undifferenzierte Endereignisse | Niedrig |
| **Organisatorisch** | 2.1 | Keine Swimlanes / Rollenzuordnung | Hoch |
| **Organisatorisch** | 2.2 | Keine Freigabe / Vier-Augen-Prinzip bei Inkasso-Uebergabe | Mittel |
| **Organisatorisch** | 2.3 | Unklare Kompetenz bei Widerspruchspruefung | Mittel |
| **Effizienz** | 3.1 | Keine Automatisierung bei Zahlungsabgleich | Mittel |
| **Effizienz** | 3.2 | Kein Mahnstufenkonzept (nur eine Zahlungsaufforderung) | Hoch |
| **Effizienz** | 3.3 | Keine parallelen Aktivitaeten waehrend Wartezeit | Niedrig |
| **Effizienz** | 3.4 | Gleiche Behandlung fachlich unterschiedlicher Ergebnisse | Mittel |

### Aggregation

| Kategorie | Anzahl | davon Hoch | davon Mittel | davon Niedrig |
|---|---|---|---|---|
| Strukturelle Probleme | 5 | 3 | 1 | 1 |
| Organisatorische Probleme | 3 | 1 | 2 | 0 |
| Effizienz-Probleme | 4 | 1 | 2 | 1 |
| **Gesamt** | **12** | **5** | **5** | **2** |

---

*Analyse erstellt durch direkte Bildinspektion ohne Zwischenformat.*
