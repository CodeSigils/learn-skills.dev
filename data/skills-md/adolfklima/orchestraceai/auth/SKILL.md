---
name: auth
description: >
  FastAPI authentication with JWT, OAuth 2.1, RBAC, and API keys using python-jose + passlib.
  Use for: login endpoints, token issuance, protected routes, role checks, social login.
  Triggers: auth, JWT, token, login, OAuth, RBAC, password, bearer, session, middleware.
---

# Auth Skill

JWT creation, password hashing, refresh rotation — see `references/jwt.md`.

## Quick Pattern: Auth Dependency

```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials", {"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise exc
    except JWTError:
        raise exc
    user = await db.get(User, int(user_id))
    if not user or not user.is_active:
        raise exc
    return user
```

## Gotchas

1. **Token expiry** — Access tokens must be short-lived (15 min); use refresh tokens for longevity, never extend access token TTL as a workaround
2. **bcrypt rounds** — Default rounds (12) are intentionally slow; do NOT lower them for "performance" — use async thread pool (`run_in_executor`) for hashing
3. **Refresh rotation** — Issue a new refresh token on every use and invalidate the old one; store token family in Redis to detect theft via reuse
4. **CORS credentials** — `allow_credentials=True` requires an explicit `allow_origins` list, never `"*"` — browsers will reject credentialed wildcard CORS
5. **Secret key rotation** — Support multiple active keys with a `kid` header claim; decode with the matching key, not always the latest

## Related Skills
- CRUD endpoint protection: `../fastapi-crud/SKILL.md`
- API design (error responses, versioning): `../api-design/SKILL.md`

## For Details

- JWT creation, refresh rotation, blacklisting: `references/jwt.md`
- OAuth 2.1 + PKCE + social login: `references/oauth.md`
- Middleware, RBAC, API keys, rate limiting: `references/middleware.md`
