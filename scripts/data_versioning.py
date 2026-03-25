from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


VERSION_MANIFEST_VERSION = 1
VERSION_PATH = "version.json"
SEARCH_INDEX_STEM = "skills_search_index"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json_if_changed(
    path: Path,
    value: Any,
    *,
    ensure_ascii: bool = False,
    indent: int = 2,
) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=ensure_ascii, indent=indent) + "\n"
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except FileNotFoundError:
        pass
    path.write_text(text, encoding="utf-8")
    return True


def _normalize_for_comparison(value: Any, ignored_keys: set[str]) -> Any:
    if isinstance(value, list):
        return [_normalize_for_comparison(item, ignored_keys) for item in value]
    if isinstance(value, dict):
        return {
            key: _normalize_for_comparison(entry, ignored_keys)
            for key, entry in value.items()
            if key not in ignored_keys
        }
    return value


def semantically_equal(prev: Any, nxt: Any, ignored_keys: Iterable[str] = ()) -> bool:
    ignored = set(ignored_keys)
    return _normalize_for_comparison(prev, ignored) == _normalize_for_comparison(nxt, ignored)


def stabilize_json_dict(
    path: Path,
    nxt: dict[str, Any],
    *,
    ignored_keys: Iterable[str] = (),
) -> dict[str, Any]:
    prev = read_json(path)
    if isinstance(prev, dict) and semantically_equal(prev, nxt, ignored_keys):
        return prev
    return nxt


def _extract_updated_at_from_prefix(path: Path) -> str | None:
    try:
        with path.open("rb") as handle:
            prefix = handle.read(8192).decode("utf-8", errors="ignore")
    except Exception:
        return None

    marker = '"updatedAt"'
    idx = prefix.find(marker)
    if idx < 0:
        return None

    rest = prefix[idx + len(marker) :]
    quote_start = rest.find('"')
    if quote_start < 0:
        return None
    quote_end = rest.find('"', quote_start + 1)
    if quote_end < 0:
        return None

    return rest[quote_start + 1 : quote_end].strip() or None


def _sha256_hex(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _repo_relative_path(path: Path, repo_root: Path) -> str:
    return path.relative_to(repo_root).as_posix()


def _collect_file_entry(path: Path, repo_root: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None

    return {
        "path": _repo_relative_path(path, repo_root),
        "updatedAt": _extract_updated_at_from_prefix(path),
        "bytes": path.stat().st_size,
        "sha256": _sha256_hex(path),
    }


def _search_index_sort_key(path: Path) -> int:
    if path.name == f"{SEARCH_INDEX_STEM}.json":
        return 1
    suffix = path.stem[len(SEARCH_INDEX_STEM) :]
    try:
        return int(suffix)
    except ValueError:
        return 1_000_000_000


def _search_index_paths(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob(f"{SEARCH_INDEX_STEM}*.json"), key=_search_index_sort_key)


def _latest_updated_at(values: Iterable[str | None]) -> str | None:
    latest_value: str | None = None
    latest_ts = -1.0
    for value in values:
        if not value:
            continue
        try:
            ts = datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        except ValueError:
            continue
        if ts < latest_ts:
            continue
        latest_ts = ts
        latest_value = value
    return latest_value


def build_version_manifest(repo_root: Path) -> dict[str, Any]:
    data_dir = repo_root / "data"

    skills = _collect_file_entry(data_dir / "skills.json", repo_root)
    primary_index = _collect_file_entry(data_dir / "skills_index.json", repo_root)
    feed = _collect_file_entry(data_dir / "feed.json", repo_root)
    category_index = _collect_file_entry(data_dir / "skills_category_index.json", repo_root)
    first_seen = _collect_file_entry(data_dir / "skills_first_seen.json", repo_root)

    search_parts = [
        entry
        for entry in (_collect_file_entry(path, repo_root) for path in _search_index_paths(data_dir))
        if entry
    ]

    search_index: dict[str, Any] | None = None
    if search_parts:
        aggregate = hashlib.sha256()
        total_bytes = 0
        for part in search_parts:
            aggregate.update(part["path"].encode("utf-8"))
            aggregate.update(b"\0")
            aggregate.update(part["sha256"].encode("utf-8"))
            aggregate.update(b"\0")
            total_bytes += int(part["bytes"])

        search_index = {
            "path": search_parts[0]["path"],
            "updatedAt": _latest_updated_at(part.get("updatedAt") for part in search_parts),
            "bytes": total_bytes,
            "sha256": aggregate.hexdigest(),
            "parts": search_parts,
        }

    manifest: dict[str, Any] = {
        "version": VERSION_MANIFEST_VERSION,
        "updatedAt": _latest_updated_at(
            [
                primary_index.get("updatedAt") if primary_index else None,
                search_index.get("updatedAt") if search_index else None,
                feed.get("updatedAt") if feed else None,
                category_index.get("updatedAt") if category_index else None,
                first_seen.get("updatedAt") if first_seen else None,
                skills.get("updatedAt") if skills else None,
            ]
        ),
        "skillsUpdatedAt": skills.get("updatedAt") if skills else None,
        "primaryIndexUpdatedAt": primary_index.get("updatedAt") if primary_index else None,
        "searchIndexUpdatedAt": search_index.get("updatedAt") if search_index else None,
        "feedUpdatedAt": feed.get("updatedAt") if feed else None,
        "categoryIndexUpdatedAt": category_index.get("updatedAt") if category_index else None,
        "firstSeenUpdatedAt": first_seen.get("updatedAt") if first_seen else None,
        "files": {},
    }

    files = manifest["files"]
    if skills:
        files["skills"] = skills
    if primary_index:
        files["primaryIndex"] = primary_index
    if search_index:
        files["searchIndex"] = search_index
    if feed:
        files["feed"] = feed
    if category_index:
        files["categoryIndex"] = category_index
    if first_seen:
        files["firstSeen"] = first_seen

    return manifest


def write_version_manifest(repo_root: Path) -> bool:
    path = repo_root / "data" / VERSION_PATH
    manifest = build_version_manifest(repo_root)
    return write_json_if_changed(path, manifest)
