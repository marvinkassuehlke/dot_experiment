# Defekt-Analyse: 02_medium (Matrix-Organisation mit Projektleitung)

**Quelle:** `from_image.dot`

---

## 1. Strukturelle Probleme

### 1.1 Verwaister Knoten ohne Berichtslinie nach unten: "Markus Wagner / Projektleitung Beta"

"Markus Wagner\nProjektleitung Beta" ist als direkte Berichtslinie unter dem CEO definiert, hat aber **keinen einzigen Direct Report**. Im Gegensatz dazu hat "Petra Zimmermann\nProjektleitung Alpha" zwei Teammitglieder (Sandra Baumann, Christian Weiß). Projektleitung Beta ist damit eine Führungsposition ohne Team -- entweder fehlen Kanten zu Teammitgliedern oder die Position ist strukturell nicht besetzt.

### 1.2 Fehlende Matrix-Verbindungen

Die Bezeichnung "Matrix-Organisation" impliziert, dass Projektleitungen (Petra Zimmermann, Markus Wagner) **fachübergreifend** auf Ressourcen der Linienfunktionen (Vertrieb, Produkt, Technik) zugreifen. Im DOT existieren aber **keine gestrichelten/dotted Kanten** zwischen den Projektleitungen und den Linienteams. Die Matrix-Dimension ist nicht abgebildet -- die Struktur wirkt wie eine reine Linienorganisation mit Projektleitungen als zusätzliche Ebene.

---

## 2. Organisatorische Probleme

### 2.1 Exzessive Leitungsspanne: "Stefan Hoffmann / Vertriebsleitung"

Stefan Hoffmann hat **12 direkte Berichtslinien**:
- Bernd Meier (Partner Management)
- Anja Schwarz (Sales Operations)
- Oliver Vogel (Sales Operations)
- Nina Hartmann (Inside Sales)
- Ralf Bauer (Inside Sales)
- Monika Krüger (Inside Sales)
- Uwe Friedrich (Außendienst)
- Karin Wolf (Außendienst)
- Dirk Schröder (Außendienst)
- Heike Lorenz (Partner Management)
- Sabine Keller (Key Account Manager)
- Jörg Lehmann (Key Account Manager)

Das liegt weit über der empfohlenen Span of Control von 7-8 Personen. Es fehlt eine **Zwischenebene** (z.B. Teamleiter Inside Sales, Teamleiter Außendienst, Teamleiter Key Account), um die Führbarkeit sicherzustellen.

### 2.2 Unklare Zuordnung der Ingenieure unter Projektleitung

"Sandra Baumann\nFrontend Engineer" und "Christian Weiß\nBackend Engineer" berichten direkt an "Petra Zimmermann\nProjektleitung Alpha". In einer Matrix-Organisation wäre zu erwarten, dass Entwickler fachlich unter "Andreas Schäfer\nTechnikleitung" geführt werden und nur disziplinarisch oder projektbezogen der Projektleitung zugeordnet sind. Die aktuelle Struktur vermischt Linien- und Projektverantwortung.

### 2.3 Asymmetrische Technikleitung

"Andreas Schäfer\nTechnikleitung" hat nur 2 Direct Reports (Eva Schmitt, Patrick Köhler), während die Engineering-Ressourcen (Sandra Baumann, Christian Weiß) unter der Projektleitung Alpha hängen. Entweder fehlen Berichtslinien von Sandra/Christian zu Andreas, oder die Technikleitung ist unterbesetzt.

---

## 3. Effizienz-Probleme

### 3.1 Fehlende Hierarchieebene im Vertrieb

Die flache Vertriebsstruktur unter Stefan Hoffmann erzeugt einen **organisatorischen Bottleneck**: Alle operativen Entscheidungen für 12 Personen müssen über eine einzige Führungskraft laufen. Funktionale Gruppierungen (Inside Sales, Außendienst, Partner Management, Key Account) existieren implizit durch die Rollennamen, sind aber nicht als Zwischenebenen abgebildet.

### 3.2 Redundante Rollenbezeichnungen ohne Differenzierung

Es gibt je zwei Personen mit identischer Rolle ohne erkennbare Differenzierung:
- "Anja Schwarz\nSales Operations" und "Oliver Vogel\nSales Operations"
- "Bernd Meier\nPartner Management" und "Heike Lorenz\nPartner Management"
- "Sabine Keller\nKey Account Manager" und "Jörg Lehmann\nKey Account Manager"

Ob diese Rollen unterschiedliche Verantwortungsbereiche haben (z.B. regional, nach Kundensegment), geht aus dem Orgchart nicht hervor.

---

## Zusammenfassung

| Kategorie | Anzahl Probleme |
|-----------|----------------|
| Strukturell | 2 |
| Organisatorisch | 3 |
| Effizienz | 2 |

Die schwerwiegendsten Befunde sind die exzessive Leitungsspanne von Stefan Hoffmann (12 Direct Reports) und die fehlende Teamzuordnung für Markus Wagner (Projektleitung Beta ohne Team).
