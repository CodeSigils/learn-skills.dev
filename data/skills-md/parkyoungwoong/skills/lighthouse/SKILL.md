---
name: lighthouse
description: (heropy) Use when analyzing web page performance, accessibility, best practices, or SEO using Google Lighthouse. Runs LHCI CLI locally, parses results, and suggests improvements with optional code fixes.
license: MIT
metadata:
  author: ParkYoungWoong
  version: 1.1.1
---

# Lighthouse Audit

Google Lighthouse를 로컬에서 실행하여 웹 페이지의 성능, 접근성, SEO 등을 분석하고 개선점을 제안하는 스킬.

## 동작 흐름

### 1단계: 대상 URL 결정

사용자가 URL을 명시한 경우 그대로 사용한다. URL이 여러 개이면 모두 수집하여 한 번에 분석한다.
URL이 없으면 프로젝트 설정 파일을 확인하여 프레임워크를 감지하고 기본 로컬 URL을 추론한다.

| 감지 파일 | 프레임워크 | 기본 URL |
|-----------|-----------|----------|
| `vite.config.ts` / `vite.config.js` | Vite (React, Vue 등) | `http://localhost:5173` |
| `next.config.ts` / `next.config.js` / `next.config.mjs` | Next.js | `http://localhost:3000` |
| `nuxt.config.ts` / `nuxt.config.js` | Nuxt | `http://localhost:3000` |
| `svelte.config.js` / `svelte.config.ts` | SvelteKit | `http://localhost:5173` |
| `angular.json` | Angular | `http://localhost:4200` |

사용자가 특정 경로(예: `/about`, `/products/123`)를 지정하면 기본 URL에 경로를 붙여서 분석한다.
프레임워크를 감지할 수 없거나 설정 파일이 없으면 사용자에게 URL을 직접 입력받는다.
외부 URL(`https://...`)이 제공된 경우 프레임워크 감지 없이 바로 사용한다.

### 2단계: 분석 모드 선택

외부 URL인 경우 이 단계를 건너뛴다.

로컬 프로젝트인 경우, 사용자에게 분석 모드를 확인한다:

- **개발 서버 분석**: 현재 실행 중인 개발 서버(`dev`)를 대상으로 분석한다
- **프로덕션 빌드 분석**: 프로젝트를 빌드한 후 프리뷰 서버를 실행하여 분석한다 (실제 배포 환경에 가까운 결과)

**개발 서버 분석을 선택한 경우:**

서버 접근 가능 여부를 확인한다:

```bash
curl -s -o /dev/null -w "%{http_code}" {URL}
```

서버에 접근할 수 없으면 사용자에게 개발 서버 시작을 안내하고 대기한다.

**프로덕션 빌드 분석을 선택한 경우:**

프레임워크에 맞는 빌드 및 프리뷰 명령을 실행한다. 프리뷰 서버의 포트는 `package.json`의 `scripts`에서 프리뷰/스타트 명령의 `--port` 또는 `-p` 옵션을 파싱하거나, 프레임워크별 기본 포트를 사용한다.

| 프레임워크 | 빌드 명령 | 프리뷰 명령 | 기본 포트 |
|-----------|----------|------------|----------|
| Vite (React, Vue 등) | `npm run build` | `npm run preview` | `4173` |
| Next.js | `npm run build` | `npm run start` | `3000` |
| Nuxt | `npm run build` | `npm run preview` | `3000` |
| SvelteKit | `npm run build` | `npm run preview` | `4173` |
| Angular | `npm run build` | `npx serve dist/` | `3000` |

프리뷰 서버 포트 확인 순서:
1. `package.json`의 해당 스크립트에서 `--port`, `-p` 옵션 파싱
2. 프레임워크 설정 파일에서 프리뷰 포트 설정 확인 (예: `vite.config.ts`의 `preview.port`)
3. 위 테이블의 프레임워크별 기본 포트 사용

빌드 완료 후 프리뷰 서버를 백그라운드로 실행하고, 서버가 준비될 때까지 대기한 후 분석을 진행한다. 분석이 완료되면 프리뷰 서버 프로세스를 종료한다.

### 3단계: Lighthouse 실행 환경 확인

프로젝트의 `.gitignore`에 `.lighthouseci`가 포함되어 있는지 확인한다. 없으면 `.gitignore`에 `.lighthouseci`를 추가하여 분석 결과가 실수로 커밋되지 않도록 한다.

Lighthouse는 Chrome 또는 Chromium 브라우저가 필요하다. 설치 여부를 확인한다.

macOS:

```bash
ls /Applications/Google\ Chrome.app 2>/dev/null || ls /Applications/Chromium.app 2>/dev/null
```

Linux:

```bash
which google-chrome || which chromium-browser
```

Chrome이 설치되어 있지 않으면 사용자에게 설치를 안내하고 중단한다.

### 4단계: LHCI 구성 파일 감지

프로젝트 루트에서 LHCI 구성 파일이 있는지 확인한다. 다음 파일명을 순서대로 탐색한다:

- `.lighthouserc.js`
- `.lighthouserc.cjs`
- `.lighthouserc.json`
- `.lighthouserc.yml`
- `.lighthouserc.yaml`

구성 파일이 존재하는 경우:
- 해당 파일의 설정을 우선 적용한다. `lhci collect` 실행 시 `--config` 플래그 없이도 LHCI가 자동으로 인식한다
- 구성 파일에 `ci.collect.url`이 이미 지정되어 있으면 1단계에서 결정한 URL 대신 구성 파일의 URL을 사용한다
- 구성 파일에 없는 옵션만 CLI 플래그로 보충한다 (예: 구성 파일에 `numberOfRuns`가 없으면 CLI에서 `--numberOfRuns=1`을 추가)
- 사용자에게 감지된 구성 파일명과 주요 설정 내용을 안내한다

구성 파일이 없는 경우:
- 5단계의 기본 CLI 플래그로 실행한다

### 5단계: Lighthouse 실행

`npx @lhci/cli`로 Lighthouse를 실행한다. `lhci collect` 명령은 Lighthouse를 실행하고 결과를 `.lighthouseci/` 디렉토리에 JSON 파일로 저장한다.

구성 파일이 없는 경우의 기본 실행 명령:

```bash
npx @lhci/cli collect \
  --url={URL1} \
  --url={URL2} \
  --numberOfRuns=1 \
  --chrome-flags="--headless --no-sandbox" \
  --only-categories=performance,accessibility,best-practices,seo
```

`--url` 플래그를 여러 번 지정하여 복수의 URL을 한 번에 분석할 수 있다.

구성 파일이 있는 경우, 구성 파일에 정의되지 않은 옵션만 CLI 플래그로 추가한다:

```bash
npx @lhci/cli collect \
  --chrome-flags="--headless --no-sandbox"
```

- `--numberOfRuns`: 기본 1회 실행. 사용자가 더 정확한 결과를 원하면 3~5회로 늘려 중앙값을 사용한다
- 결과 파일은 `.lighthouseci/` 디렉토리에 `lhr-{timestamp}.json` 형식으로 저장된다

디바이스 설정:
- 기본값은 모바일(Lighthouse 기본 동작)
- 사용자가 데스크톱을 요청하면 `--preset=desktop` 플래그를 추가한다
- 사용자가 모바일과 데스크톱 모두 요청하면 각각 실행하여 결과를 비교한다

### 6단계: 결과 파싱 및 요약

`.lighthouseci/` 디렉토리에서 가장 최근 `lhr-*.json` 파일을 읽어서 카테고리별 점수와 개선 항목을 추출한다. 여러 번 실행한 경우 중앙값(median) 결과 파일을 사용한다.

카테고리별 점수 요약 테이블을 출력한다:

| 카테고리 | 점수 | 등급 |
|----------|------|------|
| Performance | 0-100 | Good (90-100) / Needs Improvement (50-89) / Poor (0-49) |
| Accessibility | 0-100 | 동일 기준 |
| Best Practices | 0-100 | 동일 기준 |
| SEO | 0-100 | 동일 기준 |

JSON 파싱 경로:
- 카테고리 점수: `categories.{category}.score` (0-1 범위, 100을 곱해서 표시)
- 감사 항목 참조: `categories.{category}.auditRefs`에서 `weight > 0`인 항목
- 감사 상세: `audits.{auditId}`에서 `title`, `description`, `score`, `displayValue` 추출

각 카테고리에서 점수가 1 미만인 감사 항목을 `weight` 순으로 정렬하여 상위 항목부터 보고한다.
Performance 카테고리의 경우 `metricSavings` 또는 `overallSavingsMs` 값이 있으면 예상 절감 효과도 함께 표시한다.

### 7단계: 개선점 제안

카테고리별로 구분하여 구체적인 개선 방법을 제안한다. 프로젝트에서 사용 중인 프레임워크에 맞는 해결 방법을 우선 제안한다.

각 개선 항목은 다음 3단계 우선순위로 분류하여 제시한다:

| 우선순위 | 의미 | 기준 |
|---------|------|------|
| **필수** | 반드시 수정해야 하는 항목 | 사용자 경험에 직접적 영향이 크고, 코드 수정으로 명확히 해결 가능한 항목 |
| **권장** | 수정하면 좋지만 상황에 따라 판단할 항목 | 개선 효과가 있으나 수정 난이도가 높거나, 프로젝트 구조 변경이 필요한 항목 |
| **참고** | 인지만 하면 되는 항목 | 외부 환경(서버, CDN 등)에 의존하거나, 수정 대비 효과가 미미하거나, 현실적으로 수정이 어려운 항목 |

우선순위 분류 기준:

1. **감사 항목의 `weight`와 `score`**: weight가 높고 score가 낮을수록 필수에 가까움
2. **수정 가능 여부**: 프로젝트 코드에서 직접 수정 가능하면 필수/권장, 서버 설정이나 인프라 변경이 필요하면 참고
3. **효과 대비 난이도**: `metricSavings`가 크고 수정이 단순하면 필수, 대규모 리팩토링이 필요하면 권장 또는 참고
4. **실용성**: 로컬 개발 환경에서만 발생하는 문제(예: HTTP, 캐시 헤더)는 참고로 분류

**Performance 주요 항목:**

| Lighthouse Audit | 일반적 우선순위 | 개선 제안 |
|-----------------|:---:|-----------|
| `unsized-images` | 필수 | 이미지에 `width`/`height` 속성 추가 |
| `largest-contentful-paint` | 필수 | LCP 요소 최적화 (preload, `fetchpriority="high"`) |
| `cumulative-layout-shift` | 필수 | CLS 개선 (이미지 크기 지정, `font-display: swap`) |
| `render-blocking-resources` | 권장 | CSS/JS 로딩 최적화 (`async`, `defer`, 동적 import) |
| `unused-css-rules` / `unused-javascript` | 권장 | 미사용 코드 제거, 코드 스플리팅 |
| `uses-optimized-images` / `uses-webp-images` | 권장 | 이미지 포맷 변환 (WebP/AVIF), Next.js `<Image>` 활용 |
| `total-blocking-time` | 권장 | TBT 개선 (코드 스플리팅, Web Worker, 무거운 작업 분리) |
| `uses-text-compression` | 참고 | gzip/brotli 압축 (서버/호스팅 설정 필요) |
| `uses-long-cache-ttl` | 참고 | 캐시 헤더 설정 (서버/CDN 설정 필요) |
| `server-response-time` | 참고 | TTFB 개선 (서버/인프라 영역) |

**Accessibility 주요 항목:**

| Lighthouse Audit | 일반적 우선순위 | 개선 제안 |
|-----------------|:---:|-----------|
| `image-alt` | 필수 | 이미지에 `alt` 속성 추가 |
| `html-has-lang` | 필수 | `<html lang="ko">` 속성 추가 |
| `button-name` / `link-name` | 필수 | 버튼/링크에 접근 가능한 이름 추가 (`aria-label` 등) |
| `heading-order` | 권장 | 제목 태그(`h1`~`h6`) 순서 수정 |
| `meta-viewport` | 권장 | 뷰포트 메타 태그 설정 확인 |
| `color-contrast` | 참고 | 색상 대비 비율 조정 (디자인 시스템 변경이 필요할 수 있음) |

**SEO 주요 항목:**

| Lighthouse Audit | 일반적 우선순위 | 개선 제안 |
|-----------------|:---:|-----------|
| `document-title` | 필수 | 페이지 제목 설정 |
| `meta-description` | 필수 | 메타 설명 추가 |
| `canonical` | 권장 | canonical URL 설정 |
| `robots-txt` | 권장 | robots.txt 확인 및 생성 |
| `hreflang` | 참고 | 다국어 대응 hreflang 추가 (다국어 사이트가 아니면 불필요) |

**Best Practices 주요 항목:**

| Lighthouse Audit | 일반적 우선순위 | 개선 제안 |
|-----------------|:---:|-----------|
| `errors-in-console` | 필수 | 콘솔 에러 해결 |
| `no-vulnerable-libraries` | 권장 | 취약한 라이브러리 업데이트 |
| `deprecations` | 권장 | 사용 중단 예정 API 교체 |
| `is-on-https` | 참고 | HTTPS 적용 확인 (로컬 개발 환경에서는 해당 없음) |

위 테이블의 우선순위는 일반적인 기준이다. 실제 분류 시에는 해당 프로젝트의 맥락(프레임워크, 배포 환경, 페이지 특성 등)을 고려하여 항목별 우선순위를 조정한다.

### 8단계: 코드 수정 (선택적)

개선 항목을 우선순위별로 그룹화하여 사용자에게 제시한 후, 수정 여부를 확인한다.

1. **필수** 항목을 먼저 보여주고, 이어서 **권장**, **참고** 순으로 제시한다
2. 각 항목에 우선순위 라벨, 개선 내용, 예상 효과를 함께 표시한다
3. **참고** 항목은 수정 방법 대신 해당 항목이 참고인 이유(예: 서버 설정 필요, 디자인 변경 수반 등)를 설명한다
4. 사용자가 수정을 원하는 항목을 선택하면 해당 코드를 수정한다
5. 수정 완료 후 재측정을 원하는지 확인한다

코드 수정 가능 범위:
- HTML 메타 태그 추가/수정 (SEO, Accessibility)
- 이미지 태그에 `alt`, `width`, `height` 속성 추가
- Next.js `<Image>` 컴포넌트로 교체 제안
- CSS/JS 로딩 방식 변경 (`async`, `defer`, dynamic import)
- `font-display: swap` 추가
- `<html lang>` 속성 추가/수정
- 색상 대비 수정 (구체적 색상값 제시)

### 9단계: 정리

분석 완료 후 정리 작업을 수행한다.

1. 프로덕션 빌드 분석 모드였다면 백그라운드 프리뷰 서버 프로세스를 종료한다
2. 생성된 리포트 디렉토리를 삭제하여 프로젝트 디렉토리를 깨끗하게 유지한다

```bash
rm -rf ./.lighthouseci
```

## 주의사항

- Lighthouse 실행에는 Chrome 또는 Chromium 브라우저가 반드시 필요하다. 설치되어 있지 않으면 안내 후 중단한다
- 로컬 URL 분석 시 개발 서버가 실행 중이어야 한다. 서버가 꺼져 있으면 시작을 안내하고 대기한다
- Lighthouse 점수는 실행 환경(네트워크, CPU 등)에 따라 매번 달라질 수 있다. 정확도가 필요하면 `--numberOfRuns`를 늘려 중앙값을 사용한다
- `npx @lhci/cli`를 사용하여 실행한다
- 코드 수정은 반드시 사용자 확인 후 진행한다. 자동으로 수정하지 않는다
- `.lighthouseci/` 디렉토리는 분석 완료 후 삭제하여 프로젝트를 오염시키지 않는다
- 외부 URL 분석 시 네트워크 상태에 따라 결과가 달라질 수 있음을 사용자에게 안내한다
