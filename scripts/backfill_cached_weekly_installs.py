#!/usr/bin/env python3
"""
Backfill weekly installs for cached skills by scraping skills.sh skill pages.

Writes:
  - data/skills-md/<owner>/<repo>/<skillId>/stats.json
  - data/skills_index.json
  - data/skills_search_index*.json (via build_skill_search_index.py)
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
INDEX_PATH = DATA_DIR / "skills_index.json"
SEARCH_INDEX_BUILDER = REPO_ROOT / "scripts" / "build_skill_search_index.py"
USER_AGENT = "skills-feed-weekly-installs-backfill/1.0"

WEEKLY_INSTALLS_PATTERNS = [
    re.compile(r"Weekly Installs</span>\s*</div>\s*<div[^>]*>([\d,]+)</div>", re.IGNORECASE),
    re.compile(r"Weekly Installs</[^>]+>\s*<div[^>]*>([\d,]+)</div>", re.IGNORECASE),
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def skill_page_url(source: str, skill_id: str) -> str:
    return f"https://skills.sh/{source}/{skill_id}"


def github_repo_url(source: str) -> str:
    return f"https://github.com/{source}"


def stats_path(source: str, skill_id: str) -> Path:
    return DATA_DIR / "skills-md" / source / skill_id / "stats.json"


def read_stats(source: str, skill_id: str) -> dict[str, Any] | None:
    path = stats_path(source, skill_id)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def write_stats(source: str, skill_id: str, weekly_installs: int) -> None:
    path = stats_path(source, skill_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updatedAt": utc_now_iso(),
        "weeklyInstalls": weekly_installs,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def extract_weekly_installs(html: str) -> int | None:
    normalized = re.sub(r"\s+", " ", html)
    for pattern in WEEKLY_INSTALLS_PATTERNS:
        match = pattern.search(normalized)
        if not match:
            continue
        value = match.group(1).replace(",", "")
        try:
            return int(value)
        except ValueError:
            continue
    return None


def fetch_html(url: str, timeout: int) -> str | None:
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,*/*",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except (HTTPError, URLError, TimeoutError):
        return None


def load_cached_targets(force: bool, only_ids: set[str] | None) -> list[dict[str, Any]]:
    if not INDEX_PATH.exists():
        raise SystemExit(f"Missing {INDEX_PATH}")

    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    items = index.get("items")
    if not isinstance(items, list):
        raise SystemExit("skills_index.json: expected `items` to be a list")

    targets: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("providerId") != "cached":
            continue
        source = str(item.get("source") or "").strip()
        skill_id = str(item.get("skillId") or "").strip()
        if not source or not skill_id:
            continue
        full_id = f"{source}/{skill_id}"
        if only_ids and full_id not in only_ids:
            continue
        targets.append(
            {
                "source": source,
                "skillId": skill_id,
                "firstSeenAt": str(item.get("firstSeenAt") or ""),
            }
        )

    if not force:
        filtered: list[dict[str, Any]] = []
        for it in targets:
            stats = read_stats(it["source"], it["skillId"])
            if isinstance(stats, dict) and isinstance(stats.get("weeklyInstalls"), int):
                continue
            filtered.append(it)
        targets = filtered

    targets.sort(key=lambda it: (it["firstSeenAt"], f"{it['source']}/{it['skillId']}"), reverse=True)
    return targets


def backfill_one(source: str, skill_id: str, timeout: int, dry_run: bool) -> tuple[str, str, int | None, str]:
    cached = read_stats(source, skill_id)
    if isinstance(cached, dict) and isinstance(cached.get("weeklyInstalls"), int):
        return source, skill_id, int(cached["weeklyInstalls"]), "cached"

    html = fetch_html(skill_page_url(source, skill_id), timeout=timeout)
    if not html:
        return source, skill_id, None, "fetch_failed"

    weekly_installs = extract_weekly_installs(html)
    if weekly_installs is None:
        return source, skill_id, None, "parse_failed"

    if not dry_run:
        write_stats(source, skill_id, weekly_installs)
    return source, skill_id, weekly_installs, "fetched"


def update_index_from_stats(dry_run: bool) -> int:
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    items = index.get("items")
    if not isinstance(items, list):
        raise SystemExit("skills_index.json: expected `items` to be a list")

    changed = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("providerId") != "cached":
            continue
        source = str(item.get("source") or "").strip()
        skill_id = str(item.get("skillId") or "").strip()
        if not source or not skill_id:
            continue
        stats = read_stats(source, skill_id)
        if not isinstance(stats, dict):
            continue
        weekly_installs = stats.get("weeklyInstalls")
        if not isinstance(weekly_installs, int):
            continue

        if item.get("installsAllTime") != weekly_installs:
            item["installsAllTime"] = weekly_installs
            changed += 1

        expected_link = github_repo_url(source)
        if item.get("link") != expected_link:
            item["link"] = expected_link
            changed += 1

    if changed and not dry_run:
        index["updatedAt"] = utc_now_iso()
        INDEX_PATH.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    return changed


def rebuild_search_index(dry_run: bool) -> None:
    if dry_run:
        print("Dry run: skip rebuilding search index")
        return
    subprocess.run([sys.executable, str(SEARCH_INDEX_BUILDER)], cwd=REPO_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=0, help="Max cached skills to fetch (0 = all)")
    parser.add_argument("--concurrency", type=int, default=8, help="Concurrent page fetches")
    parser.add_argument("--timeout", type=int, default=20, help="Per-request timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and report without writing files")
    parser.add_argument("--force", action="store_true", help="Refetch skills even if stats.json already exists")
    parser.add_argument(
        "--id",
        action="append",
        dest="ids",
        default=[],
        help="Only process the given cached skill id (<source>/<skillId>). Repeatable.",
    )
    parser.add_argument(
        "--skip-search-index",
        action="store_true",
        help="Do not rebuild data/skills_search_index*.json after updating skills_index.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    only_ids = {s.strip() for s in args.ids if s.strip()}
    targets = load_cached_targets(force=args.force, only_ids=only_ids or None)
    if args.limit > 0:
        targets = targets[: args.limit]

    print(f"Targets: {len(targets)} cached skills")
    if not targets:
        changed = update_index_from_stats(args.dry_run)
        print(f"Summary: fetched=0 reused=0 failed=0 index_updates={changed} dry_run={args.dry_run}")
        if changed > 0 and not args.skip_search_index:
            rebuild_search_index(args.dry_run)
        return

    fetched = 0
    reused = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as executor:
        futures = {
            executor.submit(backfill_one, it["source"], it["skillId"], args.timeout, args.dry_run): it
            for it in targets
        }

        for future in as_completed(futures):
            source, skill_id, weekly_installs, status = future.result()
            skill_ref = f"{source}/{skill_id}"
            if status == "cached":
                reused += 1
                print(f"[cached] {skill_ref} -> {weekly_installs}")
            elif status == "fetched":
                fetched += 1
                print(f"[fetched] {skill_ref} -> {weekly_installs}")
            else:
                failed += 1
                print(f"[{status}] {skill_ref}")

    changed = update_index_from_stats(args.dry_run)
    print(
        f"Summary: fetched={fetched} reused={reused} failed={failed} "
        f"index_updates={changed} dry_run={args.dry_run}"
    )

    if changed > 0 and not args.skip_search_index:
        rebuild_search_index(args.dry_run)


if __name__ == "__main__":
    main()
