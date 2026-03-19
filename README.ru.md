# [learn-skills.dev](https://www.learn-skills.dev)

Курируемые качественные навыки для ИИ‑агентов. Ищите, устанавливайте, копируйте и делитесь.  
Работает с Claude Code, Cursor, OpenClaw и другими инструментами для кода с ИИ.

**Веб‑приложение:** [https://www.learn-skills.dev](https://www.learn-skills.dev) — поиск, установка, копирование и обмен навыками ИИ‑агентов.

**Языки:** [English](README.md) · [简体中文](README.zh.md) · [繁體中文](README.tw.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Источники данных

### Текущие провайдеры

- **[skills.sh](https://skills.sh)** — сообщественный рейтинг навыков
  - All Time (`/`) — по общему числу установок
  - Trending (`/trending`) — по недавнему росту
  - Hot (`/hot`) — по ежедневным установкам

### Планируемые провайдеры

- **GitHub Trending** — популярные репозитории навыков на GitHub
- **Awesome Lists** — курируемые списки awesome-* для навыков ИИ‑агентов

### Ручные навыки

Навыки, не отслеживаемые провайдерами, можно добавить вручную через `data/manual_skills.json`:

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

Для ручных навыков:

- `SKILL.md` загружается с GitHub (стандартное определение папки навыка)
- Запись попадает в `skills_index.json` с `providerId: "manual"`
- Краулер **не** перезаписывает их (сохраняются между запусками)
- **Дедупликация**: если skills.sh позже подхватит тот же навык, используются данные skills.sh

Примечание: `installs` должен быть не меньше 1 (минимальное значение).

## Выходные файлы

Краулер создаёт файлы в каталоге `data/`:

### `data/skills.json`

Полные данные по всем трём рейтингам:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

Удобный для сайта индекс *всех* навыков (строится из `data/skills.json`):

- Поле `description` — **путь** к `description_en.txt` (если есть кэш `SKILL.md` в `data/skills-md/`)
- Поле `skillMdPath` — чтобы сайт мог загрузить и отрендерить полный markdown
- **Дедупликация** по `id` (`<source>/<skillId>`). При дубликатах остаётся запись с наибольшим `installsAllTime`

### `data/feed.json`

Упрощённый формат (топ‑50 по каждому рейтингу).

Пытается дополнить каждый элемент полем `description`, загружая соответствующий `SKILL.md` с GitHub (кэш в `data/skills-md/`):

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

Кэшированные `SKILL.md` с GitHub, типичные пути:

- `skills/<skillId>/SKILL.md` (чаще всего)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (часто в плагинных репозиториях, напр. Expo)

При наличии `SKILL.md` краулер также создаёт:

- `description_en.txt` (из frontmatter `description` в SKILL.md, если есть)

По умолчанию `SKILL.md` загружается только для навыков из топ‑списков (чтобы ежедневный запуск был быстрым).

Чтобы синхронизировать *все* навыки из `data/skills.json`:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS 2.0 (XML) для читалок / подписок.

- Генерируется из текущего обхода + предыдущего `data/feed.json`
- Публикует только значимые изменения (новые записи / скачки в рейтинге), чтобы не спамить

## Использование

### Локальная разработка

```bash
# Установить зависимости
bun install

# Запустить краулер
bun run crawl
```

Совет: для более полного покрытия `SKILL.md` на GitHub (включая пути вида `plugins/*/skills/...`)
задайте `GITHUB_TOKEN`, чтобы не упираться в лимиты API:

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

После push в GitHub краулер:

1. Запускается автоматически каждый день в 00:00 UTC
2. Доступен ручной запуск (кнопка «Run workflow» во вкладке Actions)
3. Запускается автоматически при push в ветку main

## Использование на сайте

Данные можно брать по raw‑URL GitHub:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

Или через CDN jsDelivr (часто быстрее):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS (рекомендуется)

Подписка на ленту:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

Через jsDelivr:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### Пример кода

```typescript
// В Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // Перепроверка раз в час
  });
  return res.json();
}
```

## Примечания

- Данные обновляются ежедневно
- Соблюдайте условия использования каждого провайдера
- Только для личного обучения и исследований

## Вклад в проект

Хотите добавить новый источник навыков? PR приветствуются! Смотрите существующие реализации провайдеров в репозитории.
