<div align="center">

<h1><a href="https://www.learn-skills.dev">learn-skills.dev</a></h1>

<p>Skill per agenti IA curati e di alta qualità. Cerca, installa, copia e condividi.<br>
Compatibile con Claude Code, Cursor, OpenClaw e altri strumenti di coding con IA.</p>

<p><strong>Web app:</strong> <a href="https://www.learn-skills.dev">https://www.learn-skills.dev</a> — Cerca, installa, copia e condividi skill per agenti IA.</p>

<p>
<a href="./README.md">English</a> | <a href="./README.zh.md">简体中文</a> | <a href="./README.tw.md">繁體中文</a> |
<a href="./README.ja.md">日本語</a> |
<a href="./README.ko.md">한국어</a> |
<a href="./README.fr.md">Français</a> |
<a href="./README.de.md">Deutsch</a> |
<a href="./README.es.md">Español</a> |
Italiano |
<a href="./README.ru.md">Русский</a> |
<a href="./README.ar.md">العربية</a>
</p>

</div>

## Fonti dati

### Provider attuali

- **[skills.sh](https://skills.sh)** — Classifica community di skill
  - All Time (`/`) — Classifica per installazioni totali
  - Trending (`/trending`) — Classifica per crescita recente
  - Hot (`/hot`) — Classifica per installazioni giornaliere

### Provider pianificati

- **GitHub Trending** — Repository di skill popolari su GitHub
- **Awesome Lists** — Liste awesome-* curate per skill di agenti IA

### Skill manuali

Gli skill non tracciati da alcun provider possono essere aggiunti manualmente tramite `data/manual_skills.json`:

```json
{
  "skills": [
    {
      "source": "owner/repo",
      "skillId": "skill-name",
      "name": "Skill Display Name",
      "installs": 1
    }
  ]
}
```

Gli skill manuali:

- Recuperano il proprio `SKILL.md` da GitHub (rilevamento standard delle cartelle skill)
- Sono inclusi in `skills_index.json` con `providerId: "manual"`
- **Non** vengono sovrascritti dal crawler (persistono tra le esecuzioni)
- **Sono deduplicati**: se skills.sh traccia in seguito uno skill manuale, prevalgono i dati di skills.sh

Nota: `installs` deve essere almeno 1 (valore minimo).

## File generati

Il crawler genera file nella directory `data/`:

### `data/skills.json`

Dati completi degli skill per tutte e tre le classifiche:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Indice orientato al web per *tutti* gli skill (costruito da `data/skills.json`):

- Include `description` come **percorso** verso `description_en.txt` (quando esiste un `SKILL.md` in cache sotto `data/skills-md/`)
- Include `skillMdPath` così il sito può recuperare e renderizzare il markdown completo
- **Deduplicato** per `id` (`<source>/<skillId>`). Se i dati upstream contengono duplicati, resta l’entry con `installsAllTime` più alto

### `data/feed.json`

Formato feed semplificato (top 50 per classifica).

Cerca di arricchire ogni elemento con `description` recuperando il corrispondente `SKILL.md` su GitHub (in cache sotto `data/skills-md/`):

```json
{
  "title": "Skills Feed",
  "description": "Aggregated AI agent skills from multiple sources",
  "link": "https://github.com/user/skills_feed",
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "topAllTime": [...],
  "topTrending": [...],
  "topHot": [...]
}
```

### `data/skills-md/`

File `SKILL.md` in cache da GitHub, con percorsi comuni come:

- `skills/<skillId>/SKILL.md` (più comune)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (comune nei repo basati su plugin, es. Expo)

Quando è presente un `SKILL.md`, il crawler genera anche:

- `description_en.txt` (estratto dal frontmatter `description` di SKILL.md quando disponibile)

Per impostazione predefinita vengono scaricati solo gli `SKILL.md` degli skill nelle liste top (per mantenere veloce il job giornaliero).

Per sincronizzare *tutti* gli skill da `data/skills.json`:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

Feed RSS 2.0 (XML) per lettori RSS / abbonamenti.

- Generato dal crawl corrente + dal precedente `data/feed.json`
- Pubblica solo cambiamenti significativi (nuove voci / salti in classifica) per evitare spam

## Utilizzo

### Sviluppo locale

```bash
# Installa dipendenze
bun install

# Esegui il crawler
bun run crawl
```

Suggerimento: per una copertura più completa dei `SKILL.md` su GitHub (inclusi percorsi tipo plugin `plugins/*/skills/...`),
imposta `GITHUB_TOKEN` per ridurre i limiti dell’API GitHub:

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

Dopo il push su GitHub, il crawler:

1. Viene eseguito automaticamente ogni giorno alle 00:00 UTC
2. Supporta l’avvio manuale (pulsante «Run workflow» nella scheda Actions)
3. Viene eseguito automaticamente su push al branch main

## Uso sul tuo sito

Puoi recuperare i dati tramite URL raw di GitHub:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

O tramite CDN jsDelivr (spesso più veloce):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### Abbonamento RSS (consigliato)

Abbonati al feed RSS:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

O tramite jsDelivr:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Esempio di codice

```typescript
// In Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Rivalida ogni ora
  });
  return res.json();
}
```

## Note

- I dati sono aggiornati quotidianamente
- Rispetta i termini di servizio di ogni provider
- Solo per apprendimento e ricerca personale

## Strumenti consigliati

Gli output di learn-skills (note, riassunti, dati) si abbinano bene a strumenti di presentazione IA per trasformarli velocemente in slide condivisibili.

**Migliora il tuo flusso di lavoro**  
Vuoi trasformare i risultati di learn-skills in presentazioni professionali? Prova PopAi per presentazioni generate con IA in un clic:  
[https://www.popai.pro](https://www.popai.pro)

## Contributi

Vuoi aggiungere una nuova fonte di skill? Le PR sono benvenute! Consulta le implementazioni dei provider esistenti nel codice.
