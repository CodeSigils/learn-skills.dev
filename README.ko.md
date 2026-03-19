<div align="center">

<h1><a href="https://www.learn-skills.dev">learn-skills.dev</a></h1>

<p>엄선된 고품질 AI 에이전트 스킬. 검색, 설치, 복사 및 공유를 지원합니다.<br>
Claude Code, Cursor, OpenClaw 및 기타 AI 코딩 도구와 함께 사용할 수 있습니다.</p>

<p><strong>웹 앱:</strong> <a href="https://www.learn-skills.dev">https://www.learn-skills.dev</a> — AI 에이전트 스킬 검색, 설치, 복사 및 공유.</p>

<p>
<a href="./README.md">English</a> | <a href="./README.zh.md">简体中文</a> | <a href="./README.tw.md">繁體中文</a> |
<a href="./README.ja.md">日本語</a> |
한국어 |
<a href="./README.fr.md">Français</a> |
<a href="./README.de.md">Deutsch</a> |
<a href="./README.es.md">Español</a> |
<a href="./README.it.md">Italiano</a> |
<a href="./README.ru.md">Русский</a> |
<a href="./README.ar.md">العربية</a>
</p>

</div>

## 데이터 소스

### 현재 제공자

- **[skills.sh](https://skills.sh)** — 커뮤니티 큐레이션 스킬 리더보드
  - All Time (`/`) — 총 설치 수 순위
  - Trending (`/trending`) — 최근 성장 순위
  - Hot (`/hot`) — 일일 설치 순위

### 계획된 제공자

- **GitHub Trending** — GitHub 인기 스킬 저장소
- **Awesome Lists** — AI 에이전트 스킬용 awesome-* 큐레이션 목록

### 수동 스킬

어떤 제공자도 추적하지 않는 스킬은 `data/manual_skills.json`으로 수동 추가할 수 있습니다.

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

수동 스킬은 다음과 같습니다.

- GitHub에서 `SKILL.md`를 가져옴(표준 스킬 폴더 탐지)
- `skills_index.json`에 `providerId: "manual"`로 포함
- 크롤러에 의해 **덮어쓰이지 않음**(실행 간 유지)
- **중복 제거**: 이후 skills.sh가 동일 스킬을 추적하면 skills.sh 데이터를 사용

참고: `installs`는 최소 1이어야 합니다.

## 출력 파일

크롤러는 `data/` 디렉터리에 파일을 생성합니다.

### `data/skills.json`

세 가지 리더보드를 모두 포함한 전체 스킬 데이터.

```json
{
  "updatedAt": "2024-01-27T00:00:00.000Z",
  "allTime": [...],
  "trending": [...],
  "hot": [...]
}
```

### `data/skills_index.json`

*모든* 스킬을 위한 웹 친화적 인덱스(`data/skills.json`에서 생성).

- `data/skills-md/`에 캐시된 `SKILL.md`가 있으면 `description`은 `description_en.txt`에 대한 **경로**
- 전체 마크다운을 가져와 렌더링할 수 있도록 `skillMdPath` 포함
- `id`(`<source>/<skillId>`) 기준 **중복 제거**. 상위에 중복이 있으면 `installsAllTime`이 가장 큰 항목 유지

### `data/feed.json`

간소화된 피드 형식(각 리더보드 상위 50개).

해당 GitHub `SKILL.md`(`data/skills-md/`에 캐시)를 가져와 각 항목에 `description`을 채우려고 시도합니다.

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

GitHub에서 가져와 캐시한 `SKILL.md`. 일반적인 경로:

- `skills/<skillId>/SKILL.md`(가장 흔함)
- `.claude/skills/<skillId>/SKILL.md`
- `.cursor/skills/<skillId>/SKILL.md`
- `.codex/skills/<skillId>/SKILL.md`
- `plugins/<plugin-name>/skills/<skillId>/SKILL.md`(플러그인 기반 저장소에서 흔함, 예: Expo)

`SKILL.md`가 있으면 크롤러는 다음도 생성합니다.

- `description_en.txt`(가능하면 SKILL.md frontmatter의 `description`에서 추출)

기본적으로 일일 작업 속도를 위해 상위 목록에 포함된 스킬의 `SKILL.md`만 가져옵니다.

`data/skills.json`의 *모든* 스킬을 동기화하려면:

```bash
SYNC_ALL_SKILL_MDS=1 bun run crawl
```

### `data/feed.xml`

RSS 2.0(XML). RSS 리더/구독용.

- 현재 크롤 + 이전 `data/feed.json`으로 생성
- 스팸을 줄이기 위해 의미 있는 변경(신규 항목/순위 급등)만 게시

## 사용 방법

### 로컬 개발

```bash
# 의존성 설치
bun install

# 크롤러 실행
bun run crawl
```

팁: GitHub `SKILL.md` 범위를 넓히려면(`plugins/*/skills/...` 같은 플러그인 경로 포함)  
GitHub API 속도 제한을 피하려면 `GITHUB_TOKEN`을 설정하세요.

```bash
export GITHUB_TOKEN=ghp_xxx
bun run crawl
```

### GitHub Actions

GitHub에 푸시한 뒤 크롤러는:

1. 매일 UTC 0:00에 자동 실행
2. 수동 실행 지원(Actions 탭에서 «Run workflow»)
3. `main` 브랜치 푸 시 자동 실행

## 웹사이트에서 사용

GitHub Raw URL로 직접 데이터를 가져올 수 있습니다.

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/skills.json
```

또는 jsDelivr CDN(대개 더 빠름):

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/skills.json
```

### RSS 구독(권장)

RSS 피드 구독:

```
https://raw.githubusercontent.com/<username>/<repo>/main/data/feed.xml
```

jsDelivr 경로:

```
https://cdn.jsdelivr.net/gh/<username>/<repo>@main/data/feed.xml
```

### 예제 코드

```typescript
// Next.js
const SKILLS_DATA_URL = 'https://cdn.jsdelivr.net/gh/your-username/skills-crawler@main/data/skills.json';

export async function getSkillsData() {
  const res = await fetch(SKILLS_DATA_URL, {
    next: { revalidate: 3600 } // 매시간 재검증
  });
  return res.json();
}
```

## 참고

- 데이터는 매일 갱신됩니다
- 각 제공자의 서비스 약관을 준수하세요
- 개인 학습 및 연구 목적으로만 사용하세요

## 기여

새 스킬 소스를 추가하고 싶으신가요? PR을 환영합니다. 코드베이스의 기존 프로바이더 구현을 참고하세요.
