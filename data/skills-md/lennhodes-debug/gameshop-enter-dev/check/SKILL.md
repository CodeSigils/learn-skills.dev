---
name: check
description: Volledige kwaliteitscheck van het project. Gebruik bij "check", "controleer", "klaar om te pushen?".
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent
---

Volledige kwaliteitscheck van het gameshop-enter project.

**Stap 1 — Parallel checks starten:**

1. **Build** (BLOKKEREND):
   ```bash
   NODE_OPTIONS="--max-old-space-size=8192" npm run build
   ```
   Bij OOM/ENOENT: `rm -rf .next` en opnieuw.

2. **Git status**: uncommitted changes + recent commits bekijken

3. **Products.json** validatie:
   - Duplicaat SKUs?
   - Prijzen die niet op .95 eindigen?
   - Verkeerde condities (moet "Goed" of "Redelijke staat" zijn)?
   - isPremium niet sync met prijs (>= 50)?
   - Missende images?

4. **Live API check** (als internet beschikbaar):
   ```bash
   curl -s "https://gameshopenter.com/api/products" -H "User-Agent: Mozilla/5.0" | head -c 300
   ```

**Stap 2 — Fix alle gevonden issues direct**

**Stap 3 — Rapportage:**
- Aantal producten (static + dynamic)
- Eventuele problemen + of ze gefixed zijn
- Build status
- Git status (uncommitted changes?)
- Klaar om te pushen? JA/NEE
