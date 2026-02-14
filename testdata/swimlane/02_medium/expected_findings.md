# Expected Findings — Softwarerelease (02_medium)

## Seeded Defect
- **Typ:** Ping-Pong / Ineffizienter Rückschleifen-Prozess
- **Location:** Zwischen Dev-Lane und QA-Lane (Bug fixen → Retest, 3x wiederholt)
- **Beschreibung:** Der Prozess modelliert explizit 3 aufeinanderfolgende Bug-Fix-Retest-Zyklen zwischen Dev und QA. Statt eines einzelnen Rückschleifen-Mechanismus werden 6 zusätzliche Prozessschritte definiert. Dies deutet auf systematische Qualitätsprobleme oder fehlende Testabdeckung hin.
- **Erwartete Erkennung:** LLM sollte das wiederholte Hin-und-Her zwischen Dev und QA als Effizienzproblem identifizieren.
