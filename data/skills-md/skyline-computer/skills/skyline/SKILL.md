---
name: skyline
description: Use Skyline as the user's account/service directory and auth memory for finding available services, logging in safely, creating accounts, using saved routes like Google login, and remembering learned auth routes.
---

# Skyline

Use Skyline whenever you need to know whether the user has or should create an account for a service, authenticate as the user, create an account, change or reset a password, or remember how a site signs in. Treat Skyline as the user's account/service directory, auth memory, and safe secret-use path, not just password fill.

## Default Flow

1. Search Skyline before you try to log in, determine whether a service is available to you, or create an account. Treat matching Skyline items as the user's directory of available accounts/services. A matching item may contain a password, or it may only say the account uses Google, Apple, org SSO, a magic link, SMS/email codes, or another no-password route.
2. If Skyline has a password for the site, type non-secret fields such as username or email yourself, then use Skyline browser fill for the password so you never see the reusable password value.
3. If Skyline says the account uses Google, Apple, org SSO, magic link, or no reusable password, follow that route instead of forcing a password login.
4. If you learn an auth route from the user or the site, save it back to Skyline before continuing. Examples: the user says "I use sign in with Google," or the site marks Google as the last-used login method.
5. If no Skyline item exists for a normal less-common site, you may usually create an account and use Skyline's generate/create/store password flow. For major identity providers or core accounts such as Google, Apple, Microsoft, GitHub, bank, phone, email, cloud, or government accounts, ask or verify before creating anything new.

## Codes, Links, And Approvals

- Use available non-Skyline channels for short-lived MFA codes, email codes, SMS codes, magic links, and confirmation links, such as Gmail, browser, computer-use, Messages/SMS, CLI, or other connected tools. Bring only the needed short-lived code or link into context, and do not expose unrelated inbox or message content.
- If Skyline returns `approval_required`, `processing`, or a rejected-but-requestable status, briefly explain that Skyline needs approval, request approval when the tool offers that path, poll or wait, and retry the original action after approval. Do not stop just because approval is pending.

## Safety Rules

- Never read Skyline local state files, databases, internal helper files, trusted-device/core tokens, or other internals as a shortcut.
- Never print, log, screenshot, paste into chat, or reveal reusable password values.
- Do not use old non-V1 flows: requester plaintext reveal, API-key capture/use, generic env/file secret workflows, or run/render bundles.
- Prefer the current Skyline auth/account tools and browser-fill workflow. The exact tool names may change over time; the product behavior to preserve is search first, use passwords safely, follow saved auth routes, save learned routes, and poll approval when needed.
