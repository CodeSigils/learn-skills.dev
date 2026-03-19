# [learn-skills.dev](https://www.learn-skills.dev)

Skills d’agents IA sélectionnés et de haute qualité. Recherchez, installez, copiez et partagez.  
Compatible avec Claude Code, Cursor, OpenClaw et d’autres outils de codage assistés par IA.

**Application web :** [https://www.learn-skills.dev](https://www.learn-skills.dev) — Recherchez, installez, copiez et partagez des skills d’agents IA.

**Langues :** [English](README.md) · [简体中文](README.zh.md) · [繁體中文](README.tw.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Sources de données

### Fournisseurs actuels

- **[skills.sh](https://skills.sh)** — Classement communautaire des skills
  - All Time (`/`) — Classement par installations totales
  - Trending (`/trending`) — Classement par croissance récente
  - Hot (`/hot`) — Classement par installations quotidiennes

### Fournisseurs prévus

- **GitHub Trending** — Dépôts de skills populaires sur GitHub
- **Awesome Lists** — Listes awesome-* pour les skills d’agents IA

### Skills manuels

Les skills non suivis par un fournisseur peuvent être ajoutés manuellement via `data/manual_skills.json` :

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

Les skills manuels :

- Récupèrent leur `SKILL.md` depuis GitHub (détection standard des dossiers de skill)
- Sont inclus dans `skills_index.json` avec `providerId: "manual"`
- **Ne sont pas** écrasés par le crawler (ils persistent entre les exécutions)
- **Sont dédupliqués** : si skills.sh suit ensuite un skill manuel, les données de skills.sh priment

Remarque : `installs` doit être au moins 1 (valeur minimale).

## Fichiers générés

Le crawler génère des fichiers dans le répertoire `data/` :

### `data/skills.json`

Données complètes des skills pour les trois classements :

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Index web pour *tous* les skills (construit à partir de `data/skills.json`) :

- Inclut `description` comme **chemin** vers `description_en.txt` (lorsqu’un `SKILL.md` mis en cache existe sous `data/skills-md/`)
- Inclut `skillMdPath` pour que votre site puisse récupérer et afficher le markdown complet
- **Dédupliqué** par `id` (`<source>/<skillId>`). En cas de doublons en amont, l’entrée avec le plus grand `installsAllTime` est conservée

### `data/feed.json`

Format de flux simplifié (top 50 de chaque classement).

Tente d’enrichir chaque élément avec une `description` en récupérant le `SKILL.md` GitHub correspondant (mis en cache sous `data/skills-md/`) :

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

Fichiers `SKILL.md` mis en cache depuis GitHub, avec des emplacements courants tels que :

- `skills/<skillId>/SKILL.md` (le plus courant)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (courant dans les dépôts à plugins, ex. Expo)

Lorsqu’un `SKILL.md` est présent, le crawler génère aussi :

- `description_en.txt` (extrait du frontmatter `description` de SKILL.md quand disponible)

Par défaut, seuls les skills des listes principaux sont récupérés (pour garder le job quotidien rapide).

Pour synchroniser *tous* les skills de `data/skills.json` :

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

Flux RSS 2.0 (XML) pour lecteurs RSS / abonnements.

- Généré à partir du crawl en cours + l’ancien `data/feed.json`
- Ne publie que des changements significatifs (nouvelles entrées / sauts de classement) pour éviter le spam

## Utilisation

### Développement local

```bash
# Installer les dépendances
bun install

# Lancer le crawler
bun run crawl
```

Astuce : pour une couverture plus complète des `SKILL.md` sur GitHub (y compris les chemins type plugin `plugins/*/skills/...`),
définissez `GITHUB_TOKEN` pour limiter les restrictions de l’API GitHub :

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

Après un push sur GitHub, le crawler :

1. S’exécute automatiquement chaque jour à 00:00 UTC
2. Peut être déclenché manuellement (bouton « Run workflow » dans l’onglet Actions)
3. S’exécute automatiquement sur push vers la branche main

## Intégration sur votre site

Vous pouvez récupérer les données via l’URL raw GitHub :

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

Ou via le CDN jsDelivr (souvent plus rapide) :

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### Abonnement RSS (recommandé)

Abonnez-vous au flux RSS :

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

Ou via jsDelivr :

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Exemple de code

```typescript
// Dans Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Revalider toutes les heures
  });
  return res.json();
}
```

## Notes

- Les données sont mises à jour quotidiennement
- Respectez les conditions d’utilisation de chaque fournisseur
- Uniquement pour apprentissage et recherche personnels

## Contribution

Vous souhaitez ajouter une nouvelle source de skills ? Les PR sont les bienvenues ! Consultez les implémentations de fournisseurs existantes dans le dépôt.
