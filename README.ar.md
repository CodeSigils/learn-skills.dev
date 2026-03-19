# [learn-skills.dev](https://www.learn-skills.dev)

مهارات وكلاء ذكاء اصطناعي مُنتقاة وعالية الجودة. ابحث، ثبّت، انسخ، وشارك.  
يعمل مع Claude Code وCursor وOpenClaw وأدوات برمجة أخرى مدعومة بالذكاء الاصطناعي.

**تطبيق الويب:** [https://www.learn-skills.dev](https://www.learn-skills.dev) — ابحث، ثبّت، انسخ، وشارك مهارات وكلاء الذكاء الاصطناعي.

**اللغات:** [English](README.md) · [简体中文](README.zh.md) · [繁體中文](README.tw.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## مصادر البيانات

### المزوّدون الحاليون

- **[skills.sh](https://skills.sh)** — لوحة صدارة مهارات من المجتمع
  - All Time (`/`) — ترتيب إجمالي التثبيتات
  - Trending (`/trending`) — ترتيب النمو الأخير
  - Hot (`/hot`) — ترتيب التثبيتات اليومية

### المزوّدون المخططون

- **GitHub Trending** — مستودعات مهارات شائعة على GitHub
- **Awesome Lists** — قوائم awesome-* مُنتقاة لمهارات وكلاء الذكاء الاصطناعي

### المهارات اليدوية

يمكن إضافة المهارات غير المتتبَّعة عبر أي مزوّد يدويًا في `data/manual_skills.json`:

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

المهارات اليدوية:

- تُجلب لها `SKILL.md` من GitHub (باستخدام اكتشاف مجلد المهارة القياسي)
- تُدرَج في `skills_index.json` مع `providerId: "manual"`
- **لا** تُستبدل بالزاحف (تبقى بين التشغيلات)
- **تُزال التكرارات**: إذا بدأ skills.sh بتتبع مهارة يدوية لاحقًا، تُستخدم بيانات skills.sh

ملاحظة: يجب أن يكون `installs` على الأقل 1 (الحد الأدنى).

## الملفات الناتجة

يُنشئ الزاحف ملفات في المجلد `data/`:

### `data/skills.json`

بيانات مهارات كاملة لثلاث لوحات الصدارة:

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

فهرس مناسب للمواقع لـ *جميع* المهارات (يُبنى من `data/skills.json`):

- يتضمن `description` كـ **مسار** إلى `description_en.txt` عند وجود `SKILL.md` مخبأ تحت `data/skills-md/`
- يتضمن `skillMdPath` ليجلب موقعك Markdown الكامل ويعرضه
- **إزالة التكرار** حسب `id` (`<source>/<skillId>`). عند وجود تكرار في المصدر، تُحفظ العنصر ذو أعلى `installsAllTime`

### `data/feed.json`

تنسيق تغذية مبسّط (أفضل 50 من كل لوحة).

يحاول إثراء كل عنصر بـ `description` عبر جلب `SKILL.md` المقابل من GitHub (مخبأ تحت `data/skills-md/`):

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

ملفات `SKILL.md` مخبأة من GitHub، مع مسارات شائعة مثل:

- `skills/<skillId>/SKILL.md` (الأكثر شيوعًا)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md` (شائع في مستودعات الإضافات، مثل Expo)

عند وجود `SKILL.md`، يُنشئ الزاحف أيضًا:

- `description_en.txt` (مستخرج من حقل `description` في frontmatter لـ SKILL.md عند التوفر)

افتراضيًا، يُجلب `SKILL.md` فقط للمهارات ضمن القوائم العليا (لإبقاء المهمة اليومية سريعة).

لمزامنة *جميع* المهارات من `data/skills.json`:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

تغذية RSS 2.0 (XML) لقارئات RSS / الاشتراكات.

- تُولَّد من الزحف الحالي + `data/feed.json` السابق
- تُنشر فقط تغييرات ذات معنى (إدخالات جديدة / قفزات في الترتيب) لتجنب الإزعاج

## الاستخدام

### التطوير المحلي

```bash
# تثبيت التبعيات
bun install

# تشغيل الزاحف
bun run crawl
```

نصيحة: لمزيد من تغطية `SKILL.md` على GitHub (بما في ذلك مسارات الإضافات مثل `plugins/*/skills/...`)،  
اضبط `GITHUB_TOKEN` لتفادي حدود واجهة GitHub:

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

بعد الدفع إلى GitHub، الزاحف:

1. يعمل تلقائيًا يوميًا عند 00:00 UTC
2. يدعم التشغيل اليدوي (زر «Run workflow» في تبويب Actions)
3. يعمل تلقائيًا عند الدفع إلى الفرع main

## الاستخدام في موقعك

يمكن جلب البيانات مباشرة عبر رابط GitHub Raw:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

أو عبر شبكة jsDelivr (غالبًا أسرع):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### اشتراك RSS (موصى به)

اشترك في تغذية RSS:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

أو عبر jsDelivr:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### مثال على الكود

```typescript
// في Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // إعادة التحقق كل ساعة
  });
  return res.json();
}
```

## ملاحظات

- تُحدَّث البيانات يوميًا
- يرجى الالتزام بشروط خدمة كل مزوّد
- للتعلم والبحث الشخصي فقط

## المساهمة

هل تريد إضافة مصدر مهارات جديد؟ طلبات السحب مرحب بها! راجع تطبيقات المزوّدين الحالية في المستودع.
