---
name: garmin-connect
description: Connect to Garmin Connect and query personal health/fitness data — steps, sleep, heart rate, HRV, body battery, training readiness, activities (runs, walks, gym, cycling, swimming). Use when the user asks about their Garmin data, watch data, sleep, workouts, runs, rides, HRV, recovery, training status, or any fitness metric. Supports ad-hoc analytical questions like "how many times did I go to the gym this week?", "how did I sleep last night?", "what's my running pace trend?", "how's my HRV trending?".
license: MIT
compatibility: Requires Bun runtime, a Garmin Connect account, internet access to connectapi.garmin.com, sso.garmin.com, and thegarth.s3.amazonaws.com. Credentials read from GARMIN_EMAIL and GARMIN_PASSWORD env vars.
---

# Garmin Connect

Query your Garmin Connect account from the CLI. Zero npm dependencies, single-file Bun script. Auth uses the mobile JSON login API (the flow Garmin actually supports for third-party clients as of March 2026) and caches tokens locally — MFA is re-prompted only when the ~1-year OAuth1 token expires.

## When to use

Use this skill whenever the user asks a question that requires data from their Garmin watch/account. Examples:

- "How did I sleep last night?"
- "How many gym sessions this week?"
- "What's my average resting HR this month?"
- "Show me my last run"
- "What's my training readiness today?"
- "Did I hit my step goal yesterday?"

For single metrics, call one subcommand. For analytical questions, pull `summary` or `weekly` and reason over the JSON.

## Usage pattern

1. **First run**: user sets env vars and invokes `login`. If MFA is on, two-phase.
2. **Subsequent runs**: any subcommand. Tokens auto-refresh.
3. **Answer the question**: parse the JSON output and respond conversationally.

Always prefer `--pretty` when piping into your own context — compact JSON is for piping into other tools.

## Environment setup (one-time)

```bash
export GARMIN_EMAIL="your@email.com"
export GARMIN_PASSWORD="yourpassword"
# Optional: persist in ~/.config/garmin-api/env and source from shell rc.
```

First login with MFA:

```bash
# Phase 1 — triggers the email/app MFA prompt and exits with code 2.
bun run scripts/garmin.ts login
# → "[auth] MFA required (email) — code sent."

# Phase 2 — supply the code (≤10 minutes after phase 1).
GARMIN_MFA=123456 bun run scripts/garmin.ts login
# → "[auth] authenticated as <displayName> — tokens cached."
```

Without MFA: `bun run scripts/garmin.ts login` completes in one call.

## Subcommands

```bash
# Identity
bun run scripts/garmin.ts whoami --pretty

# Single-date queries (default: today)
bun run scripts/garmin.ts daily 2026-04-14 --pretty
bun run scripts/garmin.ts sleep 2026-04-14 --pretty
bun run scripts/garmin.ts hrv 2026-04-14 --pretty
bun run scripts/garmin.ts readiness 2026-04-14 --pretty
bun run scripts/garmin.ts training 2026-04-14 --pretty

# Bundle for one day (daily + sleep + hrv + readiness + training + activities)
bun run scripts/garmin.ts summary 2026-04-14 --pretty

# Activity list (date range, inclusive)
bun run scripts/garmin.ts activities --from 2026-04-08 --to 2026-04-14 --pretty
bun run scripts/garmin.ts activities --from 2026-04-08 --to 2026-04-14 --limit 100

# 7-day window ending on <date> (default today)
bun run scripts/garmin.ts weekly 2026-04-14 --pretty
```

All commands print JSON to stdout. Errors (including MFA prompts) go to stderr.

## Analytical patterns

When the user asks an analytical question, pick the smallest query that contains the answer, then reason over the JSON.

| User question | Command | What to extract |
|---|---|---|
| "How did I sleep last night?" | `sleep <yesterday>` | `dailySleepDTO.sleepScores`, stage durations, total sleep time |
| "Steps today?" | `daily <today>` | `totalSteps`, `dailyStepGoal` |
| "Gym this week?" | `activities --from <mon> --to <sun>` | count entries where `activityType.typeKey` matches `strength_training\|fitness_equipment\|indoor_cardio` |
| "Runs this month?" | `activities --from <month-start> --to <today>` | filter `typeKey` starts with `running` |
| "Resting HR trend?" | `weekly <today>` | per-day `daily.restingHeartRate` |
| "HRV status?" | `hrv <today>` | `hrvSummary.status`, `weeklyAvg`, `lastNightAvg` |
| "Recovery?" | `readiness <today>` + `training <today>` | readiness score + training status |
| "Last workout?" | `activities --from <7-days-ago> --to <today> --limit 1` | most recent entry |

For "this week" / "this month": compute the date range yourself before calling. Garmin's API is always date-explicit.

## Activity type keys (partial)

Common `activityType.typeKey` values to filter on:

- `running`, `treadmill_running`, `trail_running`, `track_running`, `indoor_running`
- `walking`, `hiking`, `casual_walking`
- `cycling`, `road_biking`, `mountain_biking`, `indoor_cycling`, `virtual_ride`
- `strength_training`, `fitness_equipment`, `indoor_cardio`
- `swimming`, `lap_swimming`, `open_water_swimming`
- `yoga`, `pilates`, `stretching`
- `other`

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `MFA_REQUIRED` exit code 2 | Phase 1 of login succeeded | Re-run with `GARMIN_MFA=<code>` within 10 min |
| `401 Unauthorized` on preauthorized | OAuth1 consumer secret rotated (auto-recovers) | On next run the script refetches from `OAUTH_CONSUMER_URL` and retries once. If it still fails, see *Self-repair* below. |
| `404 Not Found` on login | Endpoint moved | See *Self-repair* below. |
| `429` or `403` on login | Cloudflare rate limit or UA block | Wait 10+ minutes |
| `No valid cached tokens` | First run or cache cleared | Run `login` subcommand |

## Self-repair (for Claude)

This skill is designed to be patched in place when Garmin changes its auth or API surface. The compatibility surface is ~6 GET endpoints + the auth flow, and all of them live in `scripts/garmin.ts`. When something breaks, follow this escalation:

### Step 1 — Check if consumer creds rotated

Symptom: `401 Unauthorized` on `/oauth-service/oauth/preauthorized` with `"Invalid signature for signature method HMAC-SHA1"`.

The script already auto-refreshes from `https://thegarth.s3.amazonaws.com/oauth_consumer.json` (24h cache, retry-on-401). If that URL itself stops working:

1. Check the [garth repo](https://github.com/matin/garth) for the current canonical source of the consumer pair. Look at `garth/client.py` or the `sso.py` constants.
2. If `thegarth.s3.amazonaws.com` is dead, find the new host in garth's `OAUTH_CONSUMER_URL`. Update the `OAUTH_CONSUMER_URL` constant in `scripts/garmin.ts`.
3. As a last resort, inspect the current Garmin Connect mobile app traffic (mitmproxy + a rooted Android emulator) and read the pair off the first OAuth1-signed request.

### Step 2 — Check if the login endpoint moved

Symptom: `404 Not Found` on `/sso/mobile/api/login` or `/sso/mobile/api/mfa/verifyCode`.

1. Install the latest garth: `uvx --with garth python3 -c "import garth.sso as s, inspect; print(inspect.getsource(s.login))"`
2. Compare the URL constants, method, body shape, and `clientId` / `service` query params against `loginInit()` / `loginComplete()` in `scripts/garmin.ts`.
3. Port any deltas. Things to watch: `SSO_CLIENT_ID`, `SSO_SERVICE_URL`, the JSON body field names (`rememberMe`, `captchaToken`, `mfaVerificationCode`, etc.), and the `responseStatus.type` values (`SUCCESSFUL`, `MFA_REQUIRED`).

### Step 3 — Check if the User-Agent fingerprint is being blocked

Symptom: `403` immediately, even from a fresh IP.

1. Garmin cycles accepted mobile UAs. Current values:
   - SSO endpoints expect an iPhone Safari UA (`SSO_MOBILE_UA` constant).
   - Connectapi endpoints expect `GCM-iOS-5.22.1.4` (`CONNECTAPI_UA` constant).
2. Check garth's `http.py` for the current `USER_AGENT` dict. Update the constants in `scripts/garmin.ts` to match.

### Step 4 — Check if an API endpoint path or response shape changed

Symptom: `404` on one of the data endpoints (e.g. `/usersummary-service/usersummary/daily/...`), or `JSON.parse` failure.

1. Log into Garmin Connect in a browser, open DevTools → Network tab.
2. Find the equivalent request (the web app also hits `connectapi.garmin.com` via a CSRF-protected proxy; the path is the part after `/gc-api/`).
3. Update the path in the corresponding method on the `Api` object in `scripts/garmin.ts`.
4. Update `references/endpoints.md` with the new path.

### Step 5 — Verify with a fresh login

After any change:

```bash
rm -f ~/.config/garmin-api/tokens.json ~/.config/garmin-api/consumer.json
bun run scripts/garmin.ts login
# Phase 2 if MFA: GARMIN_MFA=xxxxxx bun run scripts/garmin.ts login
bun run scripts/garmin.ts whoami --pretty
bun run scripts/garmin.ts summary $(date +%F) --pretty | head -40
```

If all three succeed, the skill is healthy again.

### What NOT to do

- Don't add new npm dependencies — the whole point is a zero-dep single file.
- Don't try to impersonate the web app's `connect-csrf-token` session flow — it's more brittle than the mobile SSO flow and couples you to cookies.
- Don't hardcode a user-specific value (displayName, ticket, token). They go in `~/.config/garmin-api/tokens.json`.

## Files

- `scripts/garmin.ts` — the CLI (single file, zero deps beyond Bun)
- `references/endpoints.md` — Garmin endpoints this skill calls
- `README.md` — human-facing intro and setup

## Not in scope

- Writing data back to Garmin (activity uploads, settings, etc.)
- Syncing to external systems — that's a downstream concern
- Non-Garmin data sources (Apple Watch, Whoop, Oura, etc.)
