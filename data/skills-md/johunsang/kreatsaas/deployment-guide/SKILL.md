---
name: deployment-guide
description: SaaS 배포 완벽 가이드 - Vercel, Railway, AWS, Docker
triggers:
  - deploy
  - 배포
  - vercel
  - railway
  - docker
---

# SaaS 배포 완벽 가이드

> SaaS 프로젝트를 프로덕션에 배포하는 완벽 가이드

---

## 1. 배포 전 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 배포 전 체크리스트                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 🔧 코드 준비                                                  │
│ □ 모든 테스트 통과                                           │
│ □ 린트/타입 에러 없음                                        │
│ □ console.log 제거                                           │
│ □ 하드코딩된 URL 제거                                        │
│ □ 환경변수 분리 완료                                         │
│                                                              │
│ 🔒 보안                                                       │
│ □ API 키 환경변수 처리                                       │
│ □ CORS 설정                                                  │
│ □ Rate Limiting 적용                                         │
│ □ SQL Injection 방지                                         │
│ □ XSS 방지                                                   │
│                                                              │
│ 📊 성능                                                       │
│ □ 이미지 최적화                                              │
│ □ 번들 크기 확인                                             │
│ □ Lighthouse 점수 80+                                        │
│                                                              │
│ 📝 문서                                                       │
│ □ README 작성                                                │
│ □ 환경변수 문서화                                            │
│ □ API 문서화                                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Vercel 배포 (권장)

### 2.1 기본 배포

```bash
# 1. Vercel CLI 설치
npm i -g vercel

# 2. 프로젝트 연결 및 배포
vercel

# 3. 프로덕션 배포
vercel --prod
```

### 2.2 환경변수 설정

```bash
# CLI로 환경변수 추가
vercel env add DATABASE_URL production
vercel env add NEXTAUTH_SECRET production
vercel env add STRIPE_SECRET_KEY production

# 또는 Vercel 대시보드에서:
# Project Settings → Environment Variables
```

### 2.3 vercel.json 설정

```json
{
  "framework": "nextjs",
  "buildCommand": "prisma generate && next build",
  "installCommand": "npm install",
  "regions": ["icn1"],
  "functions": {
    "src/app/api/**/*.ts": {
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Credentials", "value": "true" },
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/sitemap.xml", "destination": "/api/sitemap" }
  ]
}
```

### 2.4 데이터베이스 연결 (Vercel Postgres)

```bash
# Vercel Postgres 추가
vercel link
vercel storage add

# 환경변수 자동 설정됨
# POSTGRES_URL, POSTGRES_PRISMA_URL 등
```

### 2.5 도메인 연결

```bash
# 도메인 추가
vercel domains add mysaas.com

# DNS 설정 (도메인 제공업체에서)
# A 레코드: 76.76.21.21
# CNAME: cname.vercel-dns.com
```

### 2.6 자동 배포 설정

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 3. Railway 배포

### 3.1 기본 배포

```bash
# 1. Railway CLI 설치
npm install -g @railway/cli

# 2. 로그인
railway login

# 3. 프로젝트 초기화
railway init

# 4. 배포
railway up
```

### 3.2 railway.json 설정

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm run start",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 3.3 데이터베이스 추가

```bash
# PostgreSQL 추가
railway add -p postgresql

# 환경변수 자동 설정됨
# DATABASE_URL 등
```

### 3.4 도메인 설정

```bash
# 커스텀 도메인
railway domain add mysaas.com

# 또는 Railway 대시보드에서:
# Settings → Domains → Add Custom Domain
```

---

## 4. AWS 배포

### 4.1 AWS Amplify (가장 쉬움)

```bash
# 1. Amplify CLI 설치
npm install -g @aws-amplify/cli

# 2. 초기화
amplify init

# 3. 호스팅 추가
amplify add hosting

# 4. 배포
amplify publish
```

### 4.2 amplify.yml

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: .next
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
      - .next/cache/**/*
```

### 4.3 AWS EC2 + Docker

```bash
# EC2 인스턴스에서
# 1. Docker 설치
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker

# 2. 이미지 빌드 및 실행
docker build -t mysaas .
docker run -d -p 80:3000 --env-file .env.production mysaas
```

### 4.4 AWS ECS + Fargate

```yaml
# task-definition.json
{
  "family": "mysaas",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "mysaas",
      "image": "123456789.dkr.ecr.ap-northeast-2.amazonaws.com/mysaas:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        { "name": "NODE_ENV", "value": "production" }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:ap-northeast-2:123456789:secret:mysaas/db"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/mysaas",
          "awslogs-region": "ap-northeast-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512"
}
```

---

## 5. Docker 배포

### 5.1 Dockerfile

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# 의존성 설치
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

# 빌드
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npx prisma generate
RUN npm run build

# 실행
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### 5.2 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mysaas
      - NEXTAUTH_URL=https://mysaas.com
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mysaas
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 5.3 nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:3000;
    }

    server {
        listen 80;
        server_name mysaas.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name mysaas.com;

        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;

        # 보안 헤더
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Gzip
        gzip on;
        gzip_types text/plain text/css application/json application/javascript;

        location / {
            proxy_pass http://app;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # 정적 파일 캐싱
        location /_next/static {
            proxy_pass http://app;
            add_header Cache-Control "public, max-age=31536000, immutable";
        }
    }
}
```

---

## 6. CI/CD 파이프라인

### 6.1 GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # 테스트
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test

  # 빌드
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  # 배포
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /app/mysaas
            docker compose pull
            docker compose up -d
            docker system prune -f
```

### 6.2 배포 스크립트

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Starting deployment..."

# 변수
DOCKER_IMAGE="ghcr.io/your-username/mysaas:latest"
COMPOSE_FILE="docker-compose.prod.yml"

# 이미지 풀
echo "📦 Pulling latest image..."
docker pull $DOCKER_IMAGE

# 서비스 재시작
echo "🔄 Restarting services..."
docker compose -f $COMPOSE_FILE up -d --force-recreate

# 헬스 체크
echo "🏥 Health check..."
sleep 10
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health)

if [ $HEALTH -eq 200 ]; then
  echo "✅ Deployment successful!"
else
  echo "❌ Health check failed! Rolling back..."
  docker compose -f $COMPOSE_FILE rollback
  exit 1
fi

# 정리
echo "🧹 Cleaning up..."
docker system prune -f

echo "🎉 Done!"
```

---

## 7. 모니터링 설정

### 7.1 Sentry 에러 추적

```bash
npm install @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
});
```

### 7.2 Uptime 모니터링

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  try {
    // DB 연결 확인
    await prisma.$queryRaw`SELECT 1`;

    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'connected',
        cache: 'connected',
      },
    });
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: String(error) },
      { status: 500 }
    );
  }
}
```

### 7.3 로깅 (Axiom/Logtail)

```bash
npm install @axiomhq/winston
```

```typescript
// src/lib/logger.ts
import winston from 'winston';
import { WinstonTransport as AxiomTransport } from '@axiomhq/winston';

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new AxiomTransport({
      dataset: process.env.AXIOM_DATASET!,
      token: process.env.AXIOM_TOKEN!,
    }),
    new winston.transports.Console({
      format: winston.format.simple(),
    }),
  ],
});

export default logger;
```

---

## 8. 환경변수 관리

### 8.1 환경변수 템플릿

```env
# .env.example

# App
NODE_ENV=production
NEXT_PUBLIC_APP_URL=https://mysaas.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/db?schema=public

# Auth
NEXTAUTH_URL=https://mysaas.com
NEXTAUTH_SECRET=your-secret-key-at-least-32-chars

# OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# Payment
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx

# Storage
CLOUDFLARE_R2_ACCESS_KEY=
CLOUDFLARE_R2_SECRET_KEY=
CLOUDFLARE_R2_BUCKET=

# AI
OPENAI_API_KEY=

# Monitoring
SENTRY_DSN=
NEXT_PUBLIC_SENTRY_DSN=

# Analytics
NEXT_PUBLIC_GA_ID=G-XXXXXX
```

### 8.2 환경변수 검증

```typescript
// src/lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  OPENAI_API_KEY: z.string().startsWith('sk-'),
});

export function validateEnv() {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('❌ Invalid environment variables:');
    console.error(result.error.format());
    throw new Error('Invalid environment variables');
  }

  return result.data;
}

// 앱 시작 시 검증
validateEnv();
```

---

## 9. 배포 플랫폼 비교

```
┌────────────────────────────────────────────────────────────────────────┐
│ 📊 배포 플랫폼 비교                                                      │
├────────────┬──────────┬──────────┬──────────┬──────────────────────────┤
│ 플랫폼     │ 난이도    │ 가격     │ 특징     │ 추천 대상               │
├────────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ Vercel     │ ⭐⭐⭐⭐⭐ │ 무료~$20 │ Next.js  │ 초보자, 프론트엔드 중심  │
│            │          │          │ 최적화   │                          │
├────────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ Railway    │ ⭐⭐⭐⭐   │ $5~     │ 간편     │ 풀스택, DB 포함         │
│            │          │          │ 올인원   │                          │
├────────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ AWS        │ ⭐⭐       │ 사용량  │ 유연성   │ 대규모, 엔터프라이즈    │
│            │          │          │ 최고     │                          │
├────────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ Docker +   │ ⭐⭐       │ VPS비용 │ 완전한   │ 숙련자, 커스텀 필요     │
│ VPS        │          │          │ 제어     │                          │
├────────────┼──────────┼──────────┼──────────┼──────────────────────────┤
│ Cloudflare │ ⭐⭐⭐     │ 무료~   │ Edge,    │ 글로벌, 정적 중심       │
│ Pages      │          │          │ 빠름     │                          │
└────────────┴──────────┴──────────┴──────────┴──────────────────────────┘
```

---

## 10. 배포 후 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ 배포 후 체크리스트                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 🌐 접근성                                                     │
│ □ 메인 페이지 로딩 확인                                      │
│ □ 모든 라우트 접근 가능                                      │
│ □ API 엔드포인트 동작                                        │
│ □ 모바일 반응형 확인                                         │
│                                                              │
│ 🔒 보안                                                       │
│ □ HTTPS 적용 확인                                            │
│ □ 환경변수 노출 없음                                         │
│ □ 보안 헤더 설정                                             │
│                                                              │
│ 📊 성능                                                       │
│ □ Lighthouse 점수 확인                                       │
│ □ Core Web Vitals 통과                                       │
│ □ 첫 페이지 로드 3초 이내                                    │
│                                                              │
│ 🔍 SEO                                                        │
│ □ sitemap.xml 생성 확인                                      │
│ □ robots.txt 확인                                            │
│ □ Open Graph 이미지 확인                                     │
│ □ Google Search Console 제출                                 │
│                                                              │
│ 📈 모니터링                                                   │
│ □ 에러 추적 연동 (Sentry)                                    │
│ □ 업타임 모니터링 설정                                       │
│ □ 로깅 설정                                                  │
│ □ Analytics 연동                                             │
│                                                              │
│ 💳 결제 (해당 시)                                             │
│ □ Stripe 웹훅 연결 확인                                      │
│ □ 테스트 결제 성공                                           │
│ □ 이메일 알림 동작                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
