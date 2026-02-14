# Defekt-Analyse: 03_complex (Holding-Struktur mit Tochtergesellschaften)

**Quelle:** `from_image.dot`

---

## 1. Strukturelle Probleme

### 1.1 Fehlende Geschäftsführung in Tochter B -- Services

"Tochter A -- Manufacturing" hat "Robert Maier\nGeschäftsführer" und "Tochter C -- Digital" hat "Viktor Novak\nGeschäftsführer". Tochter B hat **keine Geschäftsführer-Position**. Stattdessen sind "Martin Scholz\nConsulting" und "Renate Sommer\nSupport" als zwei gleichrangige Knoten abgebildet, die beide direkt von "Susanne Engel" kontrolliert werden. Es fehlt eine übergreifende Leitungsfunktion für die Tochtergesellschaft.

### 1.2 Zwei separate Kontroll-Kanten in Tochter B

Die Holding-Chefin Susanne Engel hat **drei "kontrolliert als"-Kanten** zu Tochter B: eine zu "Martin Scholz\nConsulting" und eine separate zu "Renate Sommer\nSupport". Bei Tochter A und C geht jeweils nur eine Kante zum Geschäftsführer. Das ist strukturell inkonsistent und deutet darauf hin, dass in Tochter B die konsolidierende Führungsebene fehlt.

### 1.3 Keine Verbindung zwischen Martin Scholz und Renate Sommer

Innerhalb von `cluster_tochter_b` gibt es **keine Kante** zwischen "Martin Scholz\nConsulting" und "Renate Sommer\nSupport". Beide operieren als **isolierte Teilbäume**. Consulting (Martin -> Felix, Lena, Jan) und Support (Renate -> Katrin, Tobias) sind nicht organisatorisch verbunden.

### 1.4 Verwaiste Holding-Knoten: Margarete Winter und Prof. Dr. Jens Reuter

"Margarete Winter\nCFO" und "Prof. Dr. Jens Reuter\nCTO" sind als Direct Reports von Susanne Engel definiert, haben aber **keinerlei weitere Kanten** -- weder zu den Tochtergesellschaften noch zu anderen Knoten. In einer Holding-Struktur wäre zu erwarten, dass der CFO Finanzberichtslinien zu den Tochter-GFs hat und der CTO technische Governance-Linien (z.B. dotted-line zu Sophie Keller in Tochter C oder Helmut Braun in Tochter A).

---

## 2. Organisatorische Probleme

### 2.1 Exzessive Leitungsspanne der Holding-Vorsitzenden

"Susanne Engel\nGeschäftsführerin\nVorstandsvorsitzende" hat insgesamt **6 direkte Berichtslinien**: Margarete Winter, Prof. Dr. Jens Reuter, Robert Maier, Martin Scholz, Renate Sommer, Viktor Novak. Das ist im Normalbereich (6), wird aber durch das Fehlen eines GFs in Tochter B de facto zu einer operativen Doppelbelastung, da Susanne die Koordination zwischen Consulting und Support in Tochter B selbst leisten muss.

### 2.2 Unklare Verantwortlichkeiten in Tochter C: gemischte Hierarchietiefe

"Viktor Novak\nGeschäftsführer" hat drei Berichtslinien:
- "Sophie Keller\nEntwicklungsleitung" (mit 3 eigenen Reports: Lukas Bruns, Marie Henkel, Fabian Wolf)
- "Elena Kraft\nData Analyst" (direkt unter Viktor)
- "Stefan Weber\nML Engineer" (direkt unter Viktor)

Elena und Stefan berichten direkt an den GF, während gleichartige technische Rollen (Entwickler) über eine Zwischenebene (Sophie) geführt werden. Entweder fehlt eine "Data & AI"-Teamleitung als Pendant zu Sophie, oder Elena/Stefan sollten unter Sophie eingeordnet sein.

### 2.3 Fehlende Stabsfunktionen in der Holding

Eine Holding AG hat typischerweise Stabsfunktionen wie Recht, Compliance, HR oder Controlling. Im DOT sind nur drei Personen auf Holding-Ebene abgebildet (Susanne, Margarete, Jens). Entweder sind Stabsfunktionen bewusst nicht dargestellt oder sie fehlen in der Organisation.

---

## 3. Effizienz-Probleme

### 3.1 Durchgriff der Holding auf operative Ebene in Tochter B

Dadurch dass Susanne Engel direkt "Martin Scholz" und "Renate Sommer" kontrolliert (statt über einen GF), entsteht ein **kurzer Dienstweg ohne Puffer**. In Tochter A und C gibt es einen Geschäftsführer, der operative Entscheidungen bündelt. In Tochter B fehlt diese Ebene, was zu erhöhtem Koordinationsaufwand auf Holding-Ebene führt.

### 3.2 CFO und CTO ohne funktionale Anbindung

"Margarete Winter\nCFO" und "Prof. Dr. Jens Reuter\nCTO" sind als Holding-Vorstand definiert, haben aber keine sichtbare Steuerungsfunktion gegenüber den Tochtergesellschaften. Das bedeutet entweder:
- Die funktionale Steuerung (Finanzen, Technologie) ist nicht abgebildet -- dann fehlen Kanten.
- Die Positionen haben keine operative Wirkung -- dann wäre die Holding-Ebene überbesetzt.

In beiden Fällen ist die Darstellung unvollständig oder die Struktur ineffizient.

---

## Zusammenfassung

| Kategorie | Anzahl Probleme |
|-----------|----------------|
| Strukturell | 4 |
| Organisatorisch | 3 |
| Effizienz | 2 |

Die schwerwiegendsten Befunde sind die fehlende Geschäftsführung in Tochter B (strukturelle Lücke), die vollständig isolierten Holding-Vorstände Margarete Winter und Prof. Dr. Jens Reuter (keine Anbindung an Tochtergesellschaften), sowie die zwei unverbundenen Teilbäume innerhalb von Tochter B.
