# [learn-skills.dev](https://www.learn-skills.dev)

Skills de agentes de IA seleccionados y de alta calidad. Busca, instala, copia y comparte.  
Compatible con Claude Code, Cursor, OpenClaw y otras herramientas de programación con IA.

**Aplicación web:** [https://www.learn-skills.dev](https://www.learn-skills.dev) — Busca, instala, copia y comparte skills de agentes de IA.

<p align="center">
    <a href="./README.md">English</a> | <a href="./README.zh.md">简体中文</a> | <a href="./README.tw.md">繁體中文</a> |
    <a href="./README.ja.md">日本語</a> |
    <a href="./README.ko.md">한국어</a> |
    <a href="./README.fr.md">Français</a> |
    <a href="./README.de.md">Deutsch</a> |
    Español |
    <a href="./README.it.md">Italiano</a> |
    <a href="./README.ru.md">Русский</a> |
    <a href="./README.ar.md">العربية</a>
</p>
<p align="center">
    <em>Skills de agentes de IA seleccionados — busca, instala, copia y comparte.</em>
</p>

## Fuentes de datos

### Proveedores actuales

- **[skills.sh](https://skills.sh)** — Clasificación comunitaria de skills
  - All Time (`/`) — Ranking por instalaciones totales
  - Trending (`/trending`) — Ranking por crecimiento reciente
  - Hot (`/hot`) — Ranking por instalaciones diarias

### Proveedores previstos

- **GitHub Trending** — Repositorios populares de skills en GitHub
- **Awesome Lists** — Listas awesome-* curadas para skills de agentes de IA

### Skills manuales

Los skills no rastreados por ningún proveedor se pueden añadir manualmente en `data/manual_skills.json`:

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

Los skills manuales:

- Obtienen su `SKILL.md` desde GitHub (detección estándar de carpetas de skill)
- Se incluyen en `skills_index.json` con `providerId: "manual"`
- **No** se sobrescriben en ejecuciones posteriores del crawler
- **Se deduplican**: si skills.sh empieza a rastrear un skill manual, prevalecen los datos de skills.sh

Nota: `installs` debe ser al menos 1 (valor mínimo).

## Archivos generados

El crawler genera archivos en el directorio `data/`:

### `data/skills.json`

Datos completos de skills con las tres clasificaciones:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Índice orientado a la web para *todos* los skills (construido desde `data/skills.json`):

- Incluye `description` como **ruta** a `description_en.txt` (cuando existe un `SKILL.md` en caché bajo `data/skills-md/`)
- Incluye `skillMdPath` para que tu sitio pueda obtener y renderizar el markdown completo
- **Deduplicado** por `id` (`<source>/<skillId>`). Si hay duplicados en el origen, se conserva la entrada con mayor `installsAllTime`

### `data/feed.json`

Formato de feed simplificado (top 50 de cada clasificación).

Intenta enriquecer cada elemento con `description` obteniendo el `SKILL.md` correspondiente en GitHub (en caché bajo `data/skills-md/`):

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

Archivos `SKILL.md` en caché desde GitHub, con rutas habituales como:

- `skills/<skillId>/SKILL.md` (más común)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (común en repos basados en plugins, p. ej. Expo)

Cuando existe un `SKILL.md`, el crawler también genera:

- `description_en.txt` (extraído del frontmatter `description` de SKILL.md cuando está disponible)

Por defecto solo se obtienen `SKILL.md` para skills en las listas principales (para mantener el trabajo diario rápido).

Para sincronizar *todos* los skills de `data/skills.json`:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

Feed RSS 2.0 (XML) para lectores RSS / suscripciones.

- Se genera a partir del crawl actual + el `data/feed.json` anterior
- Solo publica cambios relevantes (entradas nuevas / saltos de ranking) para no saturar

## Uso

### Desarrollo local

```bash
# Instalar dependencias
bun install

# Ejecutar el crawler
bun run crawl
```

Consejo: para una cobertura más completa de `SKILL.md` en GitHub (incluidas rutas estilo plugin como `plugins/*/skills/...`),
define `GITHUB_TOKEN` para evitar límites de la API de GitHub:

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

Tras hacer push a GitHub, el crawler:

1. Se ejecuta automáticamente cada día a las 00:00 UTC
2. Permite ejecución manual (botón «Run workflow» en la pestaña Actions)
3. Se ejecuta automáticamente en push a la rama main

## Uso en tu sitio web

Puedes obtener los datos con la URL raw de GitHub:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

O con el CDN jsDelivr (a menudo más rápido):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### Suscripción RSS (recomendado)

Suscríbete al feed RSS:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

O vía jsDelivr:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Código de ejemplo

```typescript
// En Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Revalidar cada hora
  });
  return res.json();
}
```

## Notas

- Los datos se actualizan a diario
- Respeta los términos de servicio de cada proveedor
- Solo para aprendizaje e investigación personal

## Contribuciones

¿Quieres añadir una nueva fuente de skills? ¡Las PR son bienvenidas! Revisa las implementaciones de proveedores existentes en el código.
