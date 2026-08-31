---
name: deploy-an-app
description: Take an Expo + Cloudflare Worker app that runs on the user's machine and put it into production on Cloudflare — provisioning D1, R2, KV, email, payments, secrets, custom domains; deploying once; proving the live site. Use when the user wants to deploy, ship, publish, launch or go live with an app; when they have finished building and ask how to put it online; or when an already-deployed app needs a database, a custom domain, an email domain, or an integration wired up properly. Covers preflight and stack detection, provisioning D1 and R2, wiring Clerk production keys and webhooks, Cloudflare Email Service and its DNS records, cron triggers and Queues, Stripe webhooks and keys, custom domains and DNS, secrets via wrangler, and a closing pass that checks the deployed site rather than taking the deploy's word for it.
---

# Deploy an App

Take an app that works on one machine and make it work for everyone. The result is a live URL the user owns, backed by real infrastructure, with an honest account of what was done for them and what is still theirs to do.

**Deploying is not building.** This skill provisions infrastructure, sets configuration and runs deploys. It does not add features, redesign pages, or improve code it happens to dislike. Where a change to the code is genuinely required to run in production — and this stack has no standard conversion case, because D1 locally is the same database as D1 remotely — it goes on the sheet in Step 3 and is approved before it happens.

**Most of this is automatable, and the parts that aren't are knowable in advance.** The value of this skill is not that it types `wrangler deploy`. It is that it asks for every human-only credential *once*, in one place, before anything starts — rather than discovering them one failed deploy at a time.

## Ground rules

- Explain every step like you would to a smart friend who doesn't code. Say "the address people will type" before saying "domain". Introduce each term once, briefly, then use it normally.
- **Never write or accept a version number.** Not in an install command, not in prose, not a CLI version to gate on. Every invocation takes the current release, and Step 1 is what establishes what that means today. A version written into a skill file is a lie with a timestamp on it.
- **Nothing deprecated, ever.** If the current release renames or supersedes something a reference file uses, use the replacement, not the old path that "still works".
- **On what Wrangler can do, `--help` outranks everything** — this file, the reference files, the research in Step 1, and Cloudflare's own documentation. Documentation describes the release the writer had. Ask the binary that is about to run. The merged `wrangler` and `workers-best-practices` skills in this family are the first place to look for anything Workers- or Wrangler-shaped; this is the deploy-side twin of the rule that research wins on API detail.
- **The public URL is read back from the platform, never predicted.** The Worker's assigned `*.workers.dev` address — or the custom domain attached to it — is printed by the deploy and read from the platform, never assembled from the name. Every value derived from a guessed URL — the API base the web app calls, the webhook targets, the Clerk redirects, the token audience — is then quietly wrong.
- **Everything the build needs is set before the build runs.** Not just the database. The web export inlines its `EXPO_PUBLIC_*` values at build time, the Worker's bindings must exist in `wrangler.jsonc` before `wrangler types` and the typecheck pass, and no secret is read during a Workers build — bindings arrive per request — so a missing value fails the export or the typecheck, not a runtime warning. Step 7 finishes before Step 8 starts.
- **`.env` and `.dev.vars` are not deployment artefacts.** Some values in them are actively dangerous in production — a test-mode payments key, a development Clerk instance's secret, a localhost address. Each is copied, transformed, regenerated or refused deliberately. `references/env.md` has the table; there is no copy loop.
- **A secret goes from its source into the host and nowhere else.** Never printed, never echoed into the conversation, never asked for as a chat message when a file or an environment variable would do. On Cloudflare a secret lives in `wrangler secret put` and is never written into `wrangler.jsonc`.
- **One approval, and one announced pause.** Step 3 is the only place the user decides anything. Step 6 is a scheduled hand-off where they do browser work no API can do — named on the sheet before it happens, so it is a meeting rather than an interruption.
- **Test mode unless the user says otherwise, separately.** Everything else on the sheet runs under one go-ahead. Taking real money does not: it is the one action that can charge a real card, and live prices cannot be deleted afterwards.
- **Check before creating, and write down what was created.** Every provider here will happily create a second one of anything. Two webhooks on one URL means every event is processed twice, with half the signature checks failing. The record is written as each thing is created, never reconstructed afterwards — `references/recovery.md` has the format, and it is what makes an interrupted run reportable instead of mysterious.
- **When something fails, stop and report — never tear down.** A D1 database a later step couldn't reach still holds the schema that worked. `references/recovery.md` says what can be undone and what cannot.
- **Never delete or overwrite something this run did not create.** A name collision stops and asks. The exception is a value this run wrote itself and is correcting.
- **A check that wasn't run is named, never claimed.** In this skill the specific temptations are saying the environment is verified when only names were read, that the database is connected when only a page returned 200, and that webhooks work when only an endpoint was registered. The user reads silence as success.
- **The gate is passed by fixing the deploy, never by widening the gate.** No build-error suppression, no skipping validation, and above all never removing the migration step from the pipeline to make a red X go green.
- **Never `drizzle-kit push`.** The parent skill's rule, and here the database has the user's real data in it. Its D1 form is the same rule wearing Workers clothes: schema reaches production only as a migration — generated, read, then applied with `wrangler d1 migrations apply`. No hand-run `CREATE TABLE`, no edited migration that already ran.
- The app is deployed **from the repository root** — that folder is the project root. The Worker's own folder (`worker/`) is where wrangler commands run, because `wrangler.jsonc` lives there, and the web app's folder (`app/`) is where the export runs. That is the project's design, not a detour: never create a subfolder and never `cd` into one the project didn't make.
- All commands, package names and config live in the reference files, never in this file. Load only the ones the detected branches need.
- If a reference command fails because a tool changed, check that tool's official docs, use the current equivalent, finish the job, and tell the user at the end which file needs a refresh.

## Step 0 — Preflight

Find out what is true before promising anything. `references/preflight.md`.

Nothing here changes anything. It establishes: whether wrangler is available and what it can actually do; whether the user is logged in and under which account; what this app is, which package manager each package uses, and what the export and deploy commands really run; which features it has, read from the code rather than asked about; the complete list of environment variables the code reads; and whether the git tree is clean.

**The branch list comes from the code.** An app has payments because there is a Stripe client in it, not because the user remembered to mention it. This is also what lets the skill work on an app it did not build.

**A dirty tree stops here.** Wrangler uploads the working tree, not the committed tree — there is no second mechanism to disagree, so the working tree *is* the deploy, and uncommitted work is a deploy nobody can reproduce.

**Is there already a production deployment with users on it?** If so, the posture changes for the rest of the run: nothing is created from scratch, and Step 8 stops deploying straight to production. Establish it here, not at the moment it matters.

## Step 1 — Check what's current

The branches are known, so find out what deploying them involves *today*.

**First, read the family's own merged skills** — `wrangler` and `workers-best-practices` — for anything about the CLI, the config, bindings or Workers runtime. They are kept current and are the first place to look, ahead of a search. Then dispatch **one research subagent per detected branch, all in a single message**, for what those skills don't answer: Clerk's production setup and webhook flow, Stripe's current API shapes, Cloudflare Email Service's current DNS requirements, Expo's web export output, and the agent-access branch's MCP protocol revision.

Hosting CLIs, dashboards and provider APIs move faster than application libraries, and they move in a way that breaks scripts rather than types. A flag that was renamed is a pipeline that stops halfway through, having already created things.

Each gets the standard brief — current stable release, anything deprecated or renamed, current command and endpoint shapes, any capability added since that would replace hand-written steps in the reference file. Reconcile as the parent skill does: latest stable only, take the new capability when there is one, and on how the pieces fit together this skill wins.

**Say something to the user only when something changed.** Narrating research that found everything fine reads as filler.

## Step 2 — What only the user knows

Short, because Step 0 answered most of it from the code. Ask one thing at a time, with a recommendation.

1. **"What address should this live at?"** — a domain they own, or the free one Cloudflare provides. Asked first because every callback URL, every webhook target and the API base the app calls derive from it, and each one that changes later is manual work done twice.
2. **The credentials the detected branches need**, gathered in **one block** — every provider account and key, what each is for, and where to get it. The Cloudflare login itself opens a browser and cannot be scripted; Clerk production keys live in the Clerk dashboard; Stripe keys live in the Stripe dashboard. Not one question per failure.
3. **Payments, if present: test mode or real money.** Recommend test mode. Real money is a separate, explicit confirmation.

## Step 3 — Deploy sheet

Restate it in plain words and get one clear go-ahead. `start-an-app` Step 3's job, on the deploy side:

> Here's what I'll set up for **TrailLog**:
>
> **It'll live at:** traillog.com — you'll add the domain to Cloudflare, I'll tell you exactly what that involves. Until then it answers on a free Cloudflare address.
> **The app and its brain:** the web app you built gets exported and served by Cloudflare, and the Worker that runs your API goes live on their network — both on the free tier, which is a real allowance, not a trial.
> **Database:** a D1 database, free tier — a real database on Cloudflare's network, the same kind your app already uses locally.
> **Photos:** file storage in R2 — a public store for photos and a private one for uploads, both on the free tier up to a point.
> **Cache:** a KV store for small fast values — a cache, not the source of truth; the free tier is a real allowance.
> **Sign-in:** you'll add the production address to your Clerk dashboard — about two minutes, and I'll give you the exact text.
> **Payments:** set up in test mode. No real cards until you say so.
> **What it costs:** nothing today. Every piece is on a free tier, and I'll tell you where each one ends.
> **One pause:** after I've set up the address, I'll stop and give you a short list of browser work — the domain's DNS and the Clerk dashboard entries. Everything else runs without interrupting you.
>
> Sound right?

Include what will be created, what it costs, what is irreversible, and where the pause lands. The sheet names the free tiers honestly — D1, R2, KV and the `*.workers.dev` subdomain all have allowances, and the dashboard shows the current numbers; a production app with real traffic should expect to leave the free tier, which is a cost line, not a surprise.

## Step 4 — The address

Everything downstream needs the URL, so it is settled before anything else exists. `references/project-and-url.md`.

Settle the Worker's name, **read back the URL the platform actually assigned**, attach the custom domain if there is one, and produce the DNS records the user will need. Start DNS early: it is the slowest thing in the pipeline and it depends on nothing.

Where a domain is involved, decide the canonical host — bare or `www` — and redirect the other to it. A session cookie set on the wrong one is a sign-in that appears to work and then doesn't.

## Step 5 — Provision and prepare

`references/provision-database.md`, plus `references/provision-storage.md` for the uploads and cache branches.

Create the D1 database and the R2 buckets — and the KV namespace where the app caches — and put their bindings in `wrangler.jsonc`. Two details decide whether this works: the binding name in the config must be the name the code reads, and the ids in the config must be the ones the create commands printed — copy the output, never recall it. Then regenerate the Worker's types, apply the migrations to the remote database, and confirm the database answers from the command line.

**Then build it locally, against the real bindings, before deploying anything.** Run the typecheck and `wrangler deploy --dry-run` in the Worker, and `npx expo export -p web` in the app, with the production `EXPO_PUBLIC_*` values set. It catches binding mismatches, a missing variable, and a broken export, and costs no deploys. This is the single best-value check in the skill.

## Step 6 — The rendezvous

The one announced pause. Hand the user everything that needs a human in a browser, in a single block: the DNS records at their registrar if the domain is not on Cloudflare, the Clerk dashboard work — production instance keys, redirect URLs for web and native deep links, the webhook endpoint and its signing secret — and any provider account they still need. Exact values, ready to paste.

This is not a prompt for a decision — Step 3 was. It is a scheduled hand-off, promised in advance, so the user can do fifteen minutes of console work in one sitting rather than being interrupted five times.

## Step 7 — The environment

`references/env.md`. Write every variable the code reads, to production, before any build — secrets through `wrangler secret put`, public values as `vars` in `wrangler.jsonc`, and the export's `EXPO_PUBLIC_*` values where the web build reads them.

Three things make this more than a copy: values that must be transformed or refused rather than copied; secrets that are corrupted by an invisible trailing newline and cannot be read back to diagnose; and the fact that a written secret can be confirmed to *exist* but never to be *correct*.

Then wire the external systems that need only the URL, not a live site — payment webhooks, background-job infrastructure, email sending, auth webhooks, agent access. `references/wire-payments.md`, `references/wire-jobs.md`, `references/wire-auth.md`, `references/wire-email.md`, `references/wire-mcp.md`, each only if that branch exists.

## Step 8 — Deploy

`references/deploy.md`. **Once.** Everything the build needs is already in place, so the first deploy is the first one that can succeed rather than a throwaway that fails on a missing database.

The web app was exported in Step 5; `wrangler deploy` from the Worker's folder uploads the Worker and, with static assets configured, serves that export from the same address. The Pages alternative exists for teams that want a Git-connected build; this skill's primary path is Workers static assets, and `references/deploy.md` says how to choose.

Then confirm the deployment that went live is the commit you think it is. It is one command, and it catches the two most common false victories: reading the previous deployment's result while the new one is still going, and deploying a working tree that was never committed.

**Deploy straight to production only for a project this run created.** Where there is already a live site with users, that is a different posture, and `references/deploy.md` has it.

## Step 9 — Prove it

`references/gate.md`. The app is deployed. Nothing yet establishes that it works.

Commands against the live URL, whose output is read. What is genuinely provable from outside without a browser is more than it looks: the deployed version, that migrations ran, that the database answers, every route, the certificate and canonical host, that a webhook endpoint verifies signatures rather than accepting anything, that discovery documents name the real domain, and the logs in `wrangler tail`.

**Distinguish failed from blocked from not attempted.** If DNS has not landed yet, every check behind the domain is red for one reason, and reporting fifteen failures for one cause teaches the user to ignore the gate.

Where a browser is available, use it — a real sign-in on the live domain is the one check that proves the URL, the database and the session cookie are all correct together. Everything still out of reach is named as unperformed.

## Step 10 — Fresh eyes

The gate proves the site answers. It cannot tell whether the deploy did what was agreed, or left something behind. **Dispatch the critics in a single message**, read-only, evidence not access, two rounds then stop. Briefs are in `references/gate.md`.

The lenses differ from the parent skill's, because there is no new app to review — sheet against reality, claim against evidence, secret exposure, and what got left behind.

## Step 11 — Hand off

- **What exists now and what it costs**, from the record kept while creating it — every resource, its free-tier limit, and how to remove it.
- **What the next `git push` does.** It depends on the CI wiring you chose, and that choice was made on the sheet. With CLI deploys and no CI, a push does nothing — say so plainly, and give the one-paragraph GitHub Action that changes it. With a Git-connected Pages build, pushing to the main branch builds and deploys.
- **How to deploy again, and how to roll back** — `wrangler deploy` to redeploy, `wrangler rollback` (or `wrangler versions list` + `wrangler rollback <id>`) to undo, and `wrangler d1 migrations apply --remote` for the next schema change.
- **Every check that could not be run**, with what it would need.
- **The manual steps still outstanding**, if the rendezvous left any.
- If agent access was built, the connector URL, and where it goes in their agent — they will not find it on their own.
- Anything Step 1's research contradicted, named, so this skill can be corrected.
