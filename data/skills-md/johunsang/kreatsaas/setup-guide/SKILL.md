---
name: setup-guide
description: 완전 초보자를 위한 단계별 설정 가이드
triggers:
  - 설정
  - 설치
  - 시작
  - 처음
---

# 완전 초보자를 위한 설정 가이드

컴퓨터를 처음 다루는 분도 따라할 수 있도록 모든 과정을 상세히 설명합니다.

---

## 🚀 전체 워크플로우 (큰 그림)

```
┌─────────────────────────────────────────────────────────────────┐
│                    KreatSaaS 워크플로우                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📋 STEP 1: 환경 준비 (30분)                                     │
│  ├── Node.js 설치                                                │
│  ├── VS Code 설치                                                │
│  ├── Git 설치                                                    │
│  └── 계정 가입 (GitHub, Supabase, Vercel)                        │
│                           ↓                                      │
│  💡 STEP 2: 아이디어 정리 (10분)                                  │
│  ├── 어떤 서비스를 만들 건가요?                                   │
│  ├── 누가 사용하나요?                                            │
│  └── 핵심 기능 3가지는?                                          │
│                           ↓                                      │
│  🎨 STEP 3: 디자인 선택 (5분)                                    │
│  ├── 스타일 선택 (10가지 중)                                     │
│  ├── 색상 선택                                                   │
│  └── 로고 생성 (AI)                                              │
│                           ↓                                      │
│  🔧 STEP 4: 기술 선택 (5분)                                      │
│  ├── 데이터베이스 선택                                           │
│  ├── 결제 시스템 선택 (또는 무료)                                 │
│  └── 배포 플랫폼 선택                                            │
│                           ↓                                      │
│  💻 STEP 5: 코드 생성 (자동, 10분)                               │
│  ├── 프로젝트 생성                                               │
│  ├── 로그인 시스템                                               │
│  ├── 대시보드                                                    │
│  └── 결제 (선택 시)                                              │
│                           ↓                                      │
│  🌐 STEP 6: 배포 (5분)                                          │
│  ├── GitHub에 업로드                                             │
│  ├── Vercel에서 배포                                             │
│  └── 도메인 연결 (선택)                                          │
│                           ↓                                      │
│  ✅ 완료! 나만의 SaaS 탄생 🎉                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 STEP 1: 환경 준비 (상세 가이드)

### 1-0. Node.js 버전 체크 및 업그레이드 (자동)

> **Claude Code가 자동으로 확인합니다!**

```
🔍 자동 체크 항목:
1. Node.js 설치 여부
2. 현재 버전 확인
3. 최소 요구 버전 (v20.0.0 이상, v22.x.x 권장)
4. 필요시 업그레이드 안내
```

**Claude Code 실행 시 자동 체크:**
```bash
# 1. Node.js 설치 확인
node --version

# 결과에 따른 처리:
# - 명령어 없음 → Node.js 설치 필요
# - v18.x.x 이하 → 업그레이드 필요
# - v20.x.x 이상 → OK ✅
```

**버전이 낮거나 없을 때 자동 업그레이드:**

```bash
# Mac (Homebrew 사용)
# Homebrew 없으면 먼저 설치
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.js 설치/업그레이드
brew install node@22
# 또는 기존 버전 업그레이드
brew upgrade node

# 확인
node --version  # v22.x.x ✅
```

```bash
# Mac/Linux (nvm 사용 - 권장)
# nvm 설치
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 터미널 재시작 후
nvm install 22
nvm use 22
nvm alias default 22

# 확인
node --version  # v22.x.x ✅
```

```powershell
# Windows (winget 사용)
winget install OpenJS.NodeJS.LTS

# 또는 업그레이드
winget upgrade OpenJS.NodeJS.LTS

# 확인
node --version  # v22.x.x ✅
```

```powershell
# Windows (nvm-windows 사용)
# https://github.com/coreybutler/nvm-windows/releases 에서 설치 후

nvm install 22
nvm use 22

# 확인
node --version  # v22.x.x ✅
```

**버전 체크 스크립트 (Claude Code가 실행):**
```bash
#!/bin/bash
# Node.js 버전 체크 및 안내

MIN_VERSION="20.0.0"
RECOMMENDED_VERSION="22"

check_node() {
  if ! command -v node &> /dev/null; then
    echo "❌ Node.js가 설치되어 있지 않습니다."
    echo "👉 아래 방법으로 설치하세요:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "   brew install node@22"
      echo "   또는 https://nodejs.org 에서 다운로드"
    else
      echo "   https://nodejs.org 에서 LTS 버전 다운로드"
    fi
    return 1
  fi

  CURRENT_VERSION=$(node --version | sed 's/v//')
  echo "📦 현재 Node.js 버전: v$CURRENT_VERSION"

  # 버전 비교 (major 버전만)
  CURRENT_MAJOR=$(echo $CURRENT_VERSION | cut -d. -f1)

  if [ "$CURRENT_MAJOR" -lt 20 ]; then
    echo "⚠️  Node.js v20 이상이 필요합니다. (현재: v$CURRENT_VERSION)"
    echo "👉 업그레이드 방법:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "   brew upgrade node"
      echo "   또는 nvm install 22 && nvm use 22"
    else
      echo "   https://nodejs.org 에서 최신 LTS 다운로드"
    fi
    return 1
  elif [ "$CURRENT_MAJOR" -lt 22 ]; then
    echo "✅ 사용 가능하지만 v22.x.x 권장"
  else
    echo "✅ 최신 버전입니다!"
  fi

  return 0
}

check_node
```

---

### 1-1. Node.js 설치 (수동)

```
Node.js가 뭔가요?
→ JavaScript 코드를 실행해주는 프로그램이에요.
→ 우리가 만들 웹사이트를 개발할 때 필요해요.
```

**Windows에서 설치하기:**
```
1. 인터넷 브라우저를 열어요 (Chrome, Edge 등)

2. 주소창에 입력해요:
   nodejs.org

3. 초록색 버튼 "LTS" 클릭해요
   ┌─────────────────────┐
   │  22.x.x LTS        │ ← 이거 클릭!
   │  Recommended       │
   └─────────────────────┘

4. 다운로드된 파일 실행해요
   - node-v22.x.x-x64.msi 같은 파일

5. 설치 화면에서:
   - Next 클릭
   - 약관 동의 체크 → Next
   - 설치 위치 그대로 → Next
   - Next → Install
   - Finish

6. 설치 확인하기:
   - 키보드에서 Windows키 + R 누르기
   - "cmd" 입력하고 Enter
   - 검은 창이 뜨면 입력:
     node --version
   - "v22.x.x" 같이 나오면 성공! ✅
```

**Mac에서 설치하기:**
```
1. Safari 열기

2. nodejs.org 접속

3. "LTS" 버튼 클릭

4. .pkg 파일 다운로드됨

5. 다운로드된 파일 더블클릭

6. 설치 진행:
   - 계속 → 계속 → 동의 → 설치
   - 비밀번호 입력 → 설치

7. 설치 확인:
   - Spotlight (Cmd + Space) 열기
   - "터미널" 검색해서 실행
   - 입력: node --version
   - "v20.x.x" 나오면 성공! ✅
```

---

### 1-2. VS Code 설치

```
VS Code가 뭔가요?
→ 코드를 작성하는 프로그램이에요.
→ 워드프로세서 같은 건데, 코드 전용이에요.
→ 무료예요!
```

**설치 방법:**
```
1. 브라우저에서 접속:
   code.visualstudio.com

2. 파란색 "Download" 버튼 클릭
   - Windows면 Windows 버전
   - Mac이면 Mac 버전 자동 선택됨

3. 다운로드된 파일 실행

4. 설치 진행 (모두 Next/동의)

5. 설치 완료 후 VS Code 실행

6. 한글로 바꾸기 (선택):
   - 왼쪽 사이드바에서 네모 4개 아이콘 클릭 (Extensions)
   - 검색창에 "Korean" 입력
   - "Korean Language Pack" 설치
   - VS Code 재시작
```

**VS Code 기본 사용법:**
```
┌─────────────────────────────────────────────────────────────┐
│  📁 탐색기    파일 목록이 보이는 곳                           │
├─────────────────────────────────────────────────────────────┤
│  🔍 검색      파일 내용 검색                                 │
├─────────────────────────────────────────────────────────────┤
│  📦 확장      추가 기능 설치                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│         [     코드 작성 영역     ]                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  터미널  ← 여기서 명령어 입력 (Ctrl + ` 로 열기)              │
└─────────────────────────────────────────────────────────────┘

자주 쓰는 단축키:
- Ctrl + S (Mac: Cmd + S) : 저장
- Ctrl + Z (Mac: Cmd + Z) : 되돌리기
- Ctrl + ` (Mac: Cmd + `) : 터미널 열기
- Ctrl + Shift + P (Mac: Cmd + Shift + P) : 명령 팔레트
```

---

### 1-3. Git 설치

```
Git이 뭔가요?
→ 코드의 변경 이력을 저장해주는 프로그램이에요.
→ "저장" 버튼을 눌렀는데 실수했을 때, 예전 버전으로 돌아갈 수 있어요.
→ 팀 프로젝트할 때 필수예요.
```

**Windows에서 설치:**
```
1. 브라우저에서:
   git-scm.com

2. "Download for Windows" 클릭

3. 다운로드된 파일 실행

4. 설치 진행:
   - 모든 옵션 기본값 그대로 Next
   - VS Code를 기본 에디터로 선택하는 화면 나오면:
     "Use Visual Studio Code as Git's default editor" 선택
   - 나머지는 계속 Next → Install → Finish

5. 확인:
   - VS Code 열기
   - Ctrl + ` 눌러서 터미널 열기
   - 입력: git --version
   - "git version 2.x.x" 나오면 성공! ✅
```

**Mac에서 설치:**
```
Mac은 Git이 기본 설치되어 있을 수 있어요.

1. 터미널 열기

2. 입력: git --version

3. 설치 안 되어 있다면:
   - "Command Line Tools" 설치 팝업 뜨면 "설치" 클릭
   - 또는 Xcode 설치

4. "git version 2.x.x" 나오면 성공! ✅
```

---

### 1-4. 계정 가입

#### GitHub 가입
```
GitHub가 뭔가요?
→ 코드를 인터넷에 저장하는 곳이에요.
→ 클라우드 드라이브인데 코드 전용이에요.
→ 무료예요!

가입 방법:
1. github.com 접속

2. "Sign up" 클릭

3. 정보 입력:
   - 이메일 주소
   - 비밀번호
   - 사용자 이름 (영어, 나중에 주소가 됨: github.com/사용자이름)

4. 이메일 인증

5. 완료! ✅
```

#### Supabase 가입
```
Supabase가 뭔가요?
→ 데이터를 저장하는 곳이에요.
→ 회원 정보, 게시글 같은 것들을 저장해요.
→ 로그인 기능도 제공해요.
→ 무료예요! (500MB까지)

가입 방법:
1. supabase.com 접속

2. "Start your project" 클릭

3. "Continue with GitHub" 클릭
   → 이미 GitHub 가입했으니 간편!

4. GitHub 연동 허용

5. 완료! ✅
```

#### Vercel 가입
```
Vercel이 뭔가요?
→ 만든 웹사이트를 인터넷에 올려주는 곳이에요.
→ 주소(URL)를 만들어줘요.
→ 무료예요!

가입 방법:
1. vercel.com 접속

2. "Sign Up" 클릭

3. "Continue with GitHub" 클릭

4. GitHub 연동 허용

5. 완료! ✅
```

---

## 💡 STEP 2: 아이디어 정리

### 질문에 답해보세요

```
📝 질문 1: 어떤 서비스를 만들고 싶으세요?

예시:
- "할 일 관리 앱"
- "레시피 공유 사이트"
- "영어 단어장"
- "운동 기록 앱"
- "중고 거래 플랫폼"

내 아이디어: ________________________


📝 질문 2: 누가 사용하나요?

예시:
- "바쁜 직장인"
- "요리 좋아하는 사람들"
- "영어 공부하는 학생들"
- "헬스장 다니는 사람들"

타겟 사용자: ________________________


📝 질문 3: 핵심 기능 3가지는?

예시 (할 일 관리 앱):
1. 할 일 추가/삭제
2. 완료 체크
3. 마감일 알림

내 서비스의 핵심 기능:
1. ________________________
2. ________________________
3. ________________________


📝 질문 4: 돈을 받을 건가요?

□ 완전 무료로 운영할래요
□ 기본은 무료, 고급 기능은 유료 (프리미엄)
□ 월 구독료를 받을래요
□ 아직 모르겠어요 (나중에 결정)
```

---

## 🎨 STEP 3: 디자인 선택

### 스타일 선택하기

```
아래 10가지 중 마음에 드는 스타일을 선택하세요:

1️⃣ 미니멀 (Minimal)
   ├── 하얀 배경, 깔끔
   ├── 여백 많음
   └── 적합: 생산성 도구, 노트 앱

2️⃣ 다이나믹 (Maximalist)
   ├── 화려한 색상
   ├── 많은 요소
   └── 적합: 크리에이티브, 게임

3️⃣ 레트로 퓨처 (Retro-Futuristic)
   ├── 복고풍 + 미래 느낌
   ├── 네온 색상
   └── 적합: 기술, AI

4️⃣ 자연친화 (Organic)
   ├── 부드러운 곡선
   ├── 자연스러운 색상
   └── 적합: 웰니스, 건강

5️⃣ 럭셔리 (Luxury)
   ├── 고급스러운 느낌
   ├── 금색, 어두운 색상
   └── 적합: 프리미엄 서비스

6️⃣ 플레이풀 (Playful)
   ├── 재미있고 친근한
   ├── 밝은 색상
   └── 적합: 교육, 어린이용

7️⃣ 에디토리얼 (Editorial)
   ├── 잡지 스타일
   ├── 타이포그래피 중심
   └── 적합: 미디어, 블로그

8️⃣ 브루탈리스트 (Brutalist)
   ├── 거친 느낌
   ├── 대담한 타이포
   └── 적합: 개발자 도구

9️⃣ 아트데코 (Art Deco)
   ├── 기하학적 패턴
   ├── 대칭적
   └── 적합: 부동산, 고급 서비스

🔟  인더스트리얼 (Industrial)
    ├── 기능 중심
    ├── 실용적
    └── 적합: B2B, 엔터프라이즈
```

### 색상 선택하기

```
메인 색상을 선택하세요:

🔵 파랑 계열
   - #3B82F6 (파랑)
   - #0EA5E9 (하늘색)
   - #6366F1 (인디고)
   └── 적합: 기업용, 신뢰감

🟢 초록 계열
   - #22C55E (초록)
   - #10B981 (청록)
   - #14B8A6 (민트)
   └── 적합: 건강, 자연, 돈

🟣 보라 계열
   - #8B5CF6 (보라)
   - #A855F7 (퍼플)
   - #D946EF (마젠타)
   └── 적합: 창의적, 혁신

🟠 주황 계열
   - #F97316 (주황)
   - #EF4444 (빨강)
   - #EC4899 (핑크)
   └── 적합: 에너지, 열정

⚫ 모노크롬
   - #171717 (거의 검정)
   - #404040 (어두운 회색)
   - #FAFAFA (거의 흰색)
   └── 적합: 미니멀, 고급
```

---

## 🔧 STEP 4: 기술 선택

### 선택지를 골라주세요

```
📊 데이터베이스 (데이터 저장소)

□ Supabase (추천! 초보자용)
  ├── 설정 쉬움
  ├── 로그인 기능 포함
  └── 무료 500MB

□ Firebase
  ├── Google 서비스
  ├── 실시간 기능 강점
  └── 무료 1GB

□ 서버 없이 (IndexedDB)
  ├── 브라우저에 저장
  ├── 오프라인 가능
  └── 완전 무료


💳 결제 시스템

□ 결제 안 받음 (무료 서비스)
  └── 가장 간단!

□ 토스페이먼츠 (한국)
  ├── 한국 카드 잘 됨
  └── 수수료 2.5%

□ Stripe (글로벌)
  ├── 해외 결제 가능
  └── 수수료 2.9%


🌐 배포 플랫폼 (웹사이트 공개)

□ Vercel (추천!)
  ├── 가장 간단
  ├── 자동 업데이트
  └── 무료

□ Cloudflare Pages
  ├── 완전 무료
  ├── 빠름
  └── 설정 조금 복잡

□ AWS Amplify
  ├── 아마존 서비스
  ├── 기능 많음
  └── 설정 복잡
```

---

## 💻 STEP 5: 프로젝트 시작하기

### 5-1. 프로젝트 생성

```bash
# 1. VS Code 실행

# 2. 터미널 열기 (Ctrl + ` 또는 메뉴 → Terminal → New Terminal)

# 3. 원하는 폴더로 이동
cd Documents
# (또는 cd Desktop)

# 4. 프로젝트 생성 명령어 입력 (복사해서 붙여넣기!)
npx create-next-app@latest my-saas --typescript --tailwind --eslint --app --src-dir

# 5. 질문이 나오면 모두 Enter (기본값 선택)

# 6. 설치 완료될 때까지 기다리기 (1-2분)
# "Success!" 메시지가 보이면 완료!

# 7. 프로젝트 폴더로 이동
cd my-saas

# 8. VS Code에서 폴더 열기
code .
```

### 5-2. 필수 패키지 설치

```bash
# 터미널에서 아래 명령어를 한 줄씩 실행하세요

# 데이터베이스 (Supabase 선택 시)
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs

# UI 컴포넌트 (예쁜 버튼, 입력창 등)
npm install @radix-ui/react-slot class-variance-authority clsx tailwind-merge

# 아이콘
npm install lucide-react

# 폼 처리 (입력값 검증)
npm install react-hook-form zod @hookform/resolvers
```

### 5-3. 환경 변수 설정

```
1. 프로젝트 폴더에 .env.local 파일 만들기
   - VS Code 왼쪽 탐색기에서 우클릭 → New File
   - 이름: .env.local

2. 아래 내용 복사해서 붙여넣기:
```

```env
# Supabase 설정
# (supabase.com → 프로젝트 → Settings → API에서 복사)
NEXT_PUBLIC_SUPABASE_URL=여기에_URL_붙여넣기
NEXT_PUBLIC_SUPABASE_ANON_KEY=여기에_키_붙여넣기

# 사이트 주소 (나중에 배포 후 변경)
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 5-4. 개발 서버 실행

```bash
# 터미널에서:
npm run dev

# 아래 메시지가 나오면 성공!
# ▲ Next.js 15.x.x
# - Local: http://localhost:3000
```

```
브라우저에서 확인:
1. 브라우저 열기
2. 주소창에 입력: localhost:3000
3. 페이지가 보이면 성공! 🎉
```

---

## 🌐 STEP 6: 배포하기

### 6-1. GitHub에 올리기

```bash
# 터미널에서 한 줄씩 실행:

# Git 초기화
git init

# 모든 파일 추가
git add .

# 첫 번째 저장
git commit -m "첫 번째 커밋"

# 브랜치 이름 설정
git branch -M main
```

```
GitHub에서 저장소 만들기:

1. github.com 접속

2. 오른쪽 위 "+" 버튼 → "New repository"

3. 정보 입력:
   - Repository name: my-saas
   - Description: 나의 첫 SaaS (선택)
   - Private 선택 (나만 보기)

4. "Create repository" 클릭

5. 나온 명령어 중 아래 부분 복사:
   git remote add origin https://github.com/내이름/my-saas.git
   git push -u origin main

6. 터미널에 붙여넣고 실행
```

### 6-2. Vercel에서 배포

```
1. vercel.com 접속 (로그인 상태)

2. "Add New Project" 클릭

3. "Import Git Repository" 에서 my-saas 선택

4. "Import" 클릭

5. Environment Variables 추가:
   - "Add" 버튼 클릭
   - Name: NEXT_PUBLIC_SUPABASE_URL
   - Value: (Supabase에서 복사한 URL)
   - "Add" 클릭

   - 다시 "Add" 버튼
   - Name: NEXT_PUBLIC_SUPABASE_ANON_KEY
   - Value: (Supabase에서 복사한 키)
   - "Add" 클릭

6. "Deploy" 클릭

7. 1-2분 기다리기...

8. "Congratulations!" 메시지와 함께 URL 생성!
   예: https://my-saas.vercel.app

9. 링크 클릭해서 확인! 🎉
```

---

## ✅ 완료!

```
축하합니다! 🎉🎉🎉

당신의 첫 SaaS가 인터넷에 공개되었습니다!

다음 단계:
1. 친구들에게 URL 공유하기
2. 피드백 받기
3. 기능 추가하기

도움이 필요하면:
- /kreatsaas 명령어로 가이드 받기
- GitHub Issues에 질문하기
- 커뮤니티 참여하기

화이팅! 💪
```

---

## 🆘 문제 해결

### 자주 발생하는 오류

```
❌ "npm: command not found"
→ Node.js가 설치 안 됨
→ STEP 1-1 다시 진행

❌ "'next' is not recognized"
→ npm install 안 했거나 실패
→ npm install 다시 실행

❌ "Port 3000 is already in use"
→ 이미 다른 곳에서 실행 중
→ 다른 터미널 창 닫고 다시 시도
→ 또는: npm run dev -- -p 3001

❌ "Module not found"
→ 필요한 패키지 설치 안 됨
→ npm install 다시 실행

❌ GitHub push 에러
→ 로그인 필요할 수 있음
→ 터미널에서 GitHub 로그인 진행
```

### 도움 받기

```
1. 오류 메시지 복사

2. Google에 검색
   예: "npm ERR! code ENOENT"

3. Stack Overflow 답변 참고

4. 또는 AI에게 질문
   예: "이 오류가 뭔가요? [오류 메시지 붙여넣기]"
```
