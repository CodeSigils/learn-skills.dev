# [learn-skills.dev](https://www.learn-skills.dev)

Kuratierte, hochwertige KI-Agenten-Skills. Suchen, installieren, kopieren und teilen.  
Funktioniert mit Claude Code, Cursor, OpenClaw und anderen KI-Coding-Tools.

**Web-App:** [https://www.learn-skills.dev](https://www.learn-skills.dev) — KI-Agenten-Skills suchen, installieren, kopieren und teilen.

**Sprachen:** [English](README.md) · [简体中文](README.zh.md) · [繁體中文](README.tw.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Datenquellen

### Aktuelle Anbieter

- **[skills.sh](https://skills.sh)** — Community-kuratierte Skill-Ranglisten
  - All Time (`/`) — Gesamt-Installations-Ranking
  - Trending (`/trending`) — Ranking nach kürzlichem Wachstum
  - Hot (`/hot`) — Tägliches Installations-Ranking

### Geplante Anbieter

- **GitHub Trending** — Beliebte Skill-Repos auf GitHub
- **Awesome Lists** — Kuratierte awesome-*-Listen für KI-Agenten-Skills

### Manuelle Skills

Skills, die von keinem Anbieter erfasst werden, können über `data/manual_skills.json` manuell ergänzt werden:

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

Manuelle Skills werden:

- Ihr `SKILL.md` von GitHub abgerufen (Standard-Erkennung von Skill-Ordnern)
- In `skills_index.json` mit `providerId: "manual"` aufgenommen
- Vom Crawler **nicht** überschrieben (bleiben über Läufe hinweg erhalten)
- **Dedupliziert**: Wenn skills.sh später einen manuellen Skill aufnimmt, gelten die Daten von skills.sh

Hinweis: `installs` sollte mindestens 1 sein (Mindestwert).

## Ausgabedateien

Der Crawler erzeugt Dateien im Verzeichnis `data/`:

### `data/skills.json`

Vollständige Skill-Daten für alle drei Ranglisten:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Webfreundlicher Index für *alle* Skills (aus `data/skills.json` gebaut):

- Enthält `description` als **Pfad** zu `description_en.txt` (wenn ein gecachtes `SKILL.md` unter `data/skills-md/` existiert)
- Enthält `skillMdPath`, damit eure Website das vollständige Markdown laden und rendern kann
- **Dedupliziert** nach `id` (`<source>/<skillId>`). Bei Duplikaten in den Quelldaten bleibt der Eintrag mit dem höchsten `installsAllTime`

### `data/feed.json`

Vereinfachtes Feed-Format (Top 50 je Rangliste).

Versucht jeden Eintrag mit einer `description` anzureichern, indem das passende GitHub-`SKILL.md` geholt wird (Cache unter `data/skills-md/`):

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

Gecachte `SKILL.md`-Dateien von GitHub, typische Pfade:

- `skills/<skillId>/SKILL.md` (am häufigsten)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (häufig in Plugin-Repos, z. B. Expo)

Wenn ein `SKILL.md` vorhanden ist, erzeugt der Crawler außerdem:

- `description_en.txt` (aus dem Frontmatter-Feld `description` von SKILL.md, falls vorhanden)

Standardmäßig werden nur Skills aus den Top-Listen abgerufen (damit der tägliche Job schnell bleibt).

Um *alle* Skills aus `data/skills.json` zu synchronisieren:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS-2.0-Feed (XML) für RSS-Reader / Abonnements.

- Wird aus dem aktuellen Crawl + dem vorherigen `data/feed.json` generiert
- Veröffentlicht nur sinnvolle Änderungen (neue Einträge / Sprünge in der Rangliste), um Spam zu vermeiden

## Nutzung

### Lokale Entwicklung

```bash
# Abhängigkeiten installieren
bun install

# Crawler ausführen
bun run crawl
```

Tipp: Für vollständigere GitHub-`SKILL.md`-Abdeckung (inkl. Plugin-Pfade wie `plugins/*/skills/...`)
setzt `GITHUB_TOKEN`, um API-Limits zu vermeiden:

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

Nach einem Push zu GitHub:

1. Läuft der Crawler täglich um 00:00 UTC automatisch
2. Manuelles Auslösen ist möglich („Run workflow“ im Actions-Tab)
3. Läuft automatisch bei Push auf den Branch `main`

## Nutzung auf eurer Website

Daten könnt ihr direkt über die GitHub-Raw-URL abrufen:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

Oder über das jsDelivr-CDN (oft schneller):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS-Abonnement (empfohlen)

RSS-Feed abonnieren:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

Oder über jsDelivr:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Beispielcode

```typescript
// In Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Stündlich neu validieren
  });
  return res.json();
}
```

## Hinweise

- Daten werden täglich aktualisiert
- Bitte die Nutzungsbedingungen jedes Anbieters einhalten
- Nur für persönliches Lernen und Forschung

## Mitwirken

Neue Skill-Quelle hinzufügen? PRs sind willkommen! Schaut euch die vorhandenen Provider-Implementierungen im Repo an.
