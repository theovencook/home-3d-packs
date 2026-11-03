"""Build and check index.json, the list of packs Home 3D's Library offers under "Browse packs".

    python tools/build_index.py build . --home3d ../home-3d [--fetch]
        Writes index.json from the pack folders in this repository and the community packs in community.json.
        Without --fetch the community entries already in index.json are kept; with it each one is fetched from
        GitHub and checked again (a new community pack needs --fetch).

    python tools/build_index.py check . --home3d ../home-3d
        What CI runs: fetches and checks every listed pack and fails when any breaks a rule, or when index.json is
        not what `build --fetch` would write.

The rules (every listed pack):
- it passes Home 3D's own pack check (custom_components/home_3d/packs.py from the Home 3D checkout named by
  --home3d): the same schema and limits Home Assistant applies on install. That check also refuses anything that is
  not data: only pack.json, item .json files and a README/LICENSE/CHANGELOG text may be in the folder, and no text
  in them may hold a link;
- its licence is MIT, and an MIT licence text is in the pack folder or at the top of its repository;
- its id is unique in the index, and a community pack does not use the theovencook publisher or a reserved id.

Needs Python 3.11+ and the package "voluptuous". GITHUB_TOKEN, when set, is sent to the GitHub API (CI sets it).
"""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from types import ModuleType
from typing import Any
import urllib.error
import urllib.request

REPO = "theovencook/home-3d-packs"
BRANCH = "main"
INDEX_FILE = "index.json"
COMMUNITY_FILE = "community.json"
INDEX_FORMAT = "home3d-pack-index"
INDEX_VERSION = 1
# whole items in an entry, drawn as the pack's pictures before it is installed
PREVIEWS = 6
OFFICIAL_PUBLISHER = "theovencook"
RESERVED_IDS = {"household.custom"}
LICENCE = "MIT"
MIT_TEXT = re.compile(r"MIT License|Permission is hereby granted, free of charge", re.IGNORECASE)
_LICENCE_FILE = re.compile(r"^(?:LICEN[CS]E|COPYING)(?:\.(?:md|txt))?$", re.IGNORECASE)
_TREE_URL = re.compile(
    r"^https://github\.com/(?P<owner>[A-Za-z0-9][A-Za-z0-9-]{0,38})/(?P<repo>[A-Za-z0-9_.-]{1,100})"
    r"(?:/tree/(?P<ref>[A-Za-z0-9_][A-Za-z0-9_.-]{0,99})(?:/(?P<folder>[A-Za-z0-9_][A-Za-z0-9_./-]{0,399}))?)?/?$"
)
TIMEOUT = 30
MAX_BYTES = 5_000_000


class PackIndexError(Exception):
    """A listed pack breaks a rule, or the index cannot be built."""


def load_packs_module(home3d: Path) -> ModuleType:
    """Home 3D's own pack check (packs.py only needs voluptuous)."""
    path = home3d / "custom_components" / "home_3d" / "packs.py"
    if not path.is_file():
        raise PackIndexError(f"{path} not found: --home3d must name a Home 3D checkout")
    spec = importlib.util.spec_from_file_location("home3d_packs", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------- one entry


def entry_of(pack: dict[str, Any], url: str, source: str, thumbnail: str | None = None) -> dict[str, Any]:
    """The index entry of a checked pack."""
    entry: dict[str, Any] = {
        "id": pack["id"],
        "name": pack["name"],
        "description": pack.get("description", ""),
        "publisher": pack["publisher"],
        "licence": pack["licence"],
        "release": pack.get("release", 1),
        **({"release_note": pack["release_note"]} if pack.get("release_note") else {}),
        "url": url,
        "source": source,
    }
    if pack.get("kind") == "language":
        return {**entry, "kind": "language", "language": pack["language"], "texts": len(pack["strings"]), "items": 0}
    items = pack["items"]
    groups = Counter(item.get("group") or "other" for item in items)
    entry.update(kind="furniture", items=len(items), categories=dict(sorted(groups.items(), key=lambda g: (-g[1], g[0]))))
    # one item of each of the biggest groups (the first by id), the chosen thumbnail first
    by_id = sorted(items, key=lambda i: i["id"])
    previews: list[dict[str, Any]] = []
    chosen = next((i for i in by_id if i["id"] == thumbnail), None)
    if thumbnail and chosen is None:
        raise PackIndexError(f'{pack["id"]}: the thumbnail "{thumbnail}" is not an item of the pack')
    if chosen is not None:
        previews.append(chosen)
    for group, _count in entry["categories"].items():
        if len(previews) >= PREVIEWS:
            break
        first = next((i for i in by_id if (i.get("group") or "other") == group and i not in previews), None)
        if first is not None:
            previews.append(first)
    entry["thumbnail"] = previews[0]["id"]
    entry["previews"] = previews
    return entry


def check_rules(pack: dict[str, Any], source: str, has_licence_text: bool) -> list[str]:
    problems = []
    if pack["licence"] != LICENCE:
        problems.append(f'{pack["id"]}: the licence must be {LICENCE}, not {pack["licence"]}')
    if not has_licence_text:
        problems.append(f"{pack['id']}: no MIT licence text (LICENSE) in the pack folder or at the top of its repository")
    if source == "community" and (pack["id"].split(".")[0] == OFFICIAL_PUBLISHER or pack["id"] in RESERVED_IDS):
        problems.append(f'{pack["id"]}: a community pack cannot use the id of {OFFICIAL_PUBLISHER} or a reserved id')
    return problems


# ---------------------------------------------------------------------------- our packs


def official_packs(root: Path, packs: ModuleType) -> tuple[list[dict[str, Any]], list[str]]:
    """The entries of the pack folders in this repository, and the problems found."""
    entries, problems = [], []
    for folder in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if not (folder / "pack.json").is_file():
            continue
        try:
            pack = packs.verify_folder(packs.read_folder(folder))
        except packs.PackError as err:
            problems.append(f"{folder.name}: {err}")
            continue
        if pack["id"] != folder.name:
            problems.append(f"{folder.name}: the folder must be named after the pack id {pack['id']}")
            continue
        licence_text = any(
            _LICENCE_FILE.match(f.name) and MIT_TEXT.search(f.read_text(encoding="utf-8", errors="replace"))
            for f in [*folder.iterdir(), *root.iterdir()]
            if f.is_file()
        )
        problems += check_rules(pack, "official", licence_text)
        entries.append(entry_of(pack, f"https://github.com/{REPO}/tree/{BRANCH}/{folder.name}", "official"))
    return entries, problems


# ---------------------------------------------------------------------------- community packs


def _get(url: str, accept: str = "application/vnd.github+json") -> bytes:
    headers = {"Accept": accept, "User-Agent": "home-3d-packs-index"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:  # noqa: S310 (https GitHub only)
            body = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as err:
        raise PackIndexError(f"{url}: GitHub answered {err.code}") from err
    except (urllib.error.URLError, TimeoutError) as err:
        raise PackIndexError(f"{url}: {err}") from err
    if len(body) > MAX_BYTES:
        raise PackIndexError(f"{url}: more than {MAX_BYTES} bytes")
    return body


def fetch_community(url: str, packs: ModuleType) -> tuple[dict[str, Any], bool]:
    """A community pack from its GitHub URL, checked with Home 3D's rules, and whether an MIT licence text is there."""
    match = _TREE_URL.match(url)
    if not match:
        raise PackIndexError(f"{url}: not https://github.com/<owner>/<repo>[/tree/<branch>/<folder>]")
    owner, repo, ref, folder = match["owner"], match["repo"], match["ref"], (match["folder"] or "").strip("/")
    api = f"https://api.github.com/repos/{owner}/{repo}"
    if ref is None:
        ref = json.loads(_get(api))["default_branch"]
    sha = json.loads(_get(f"{api}/commits/{ref}"))["sha"]
    tree = json.loads(_get(f"{api}/git/trees/{sha}?recursive=1"))
    if tree.get("truncated"):
        raise PackIndexError(f"{url}: the repository is too large to list")
    prefix = f"{folder}/" if folder else ""
    paths = [
        e["path"][len(prefix) :]
        for e in tree["tree"]
        if e.get("type") == "blob" and e["path"].startswith(prefix)
        and not any(p.startswith(".") for p in e["path"][len(prefix) :].split("/"))
    ]
    try:
        wanted = packs.data_paths(paths)
    except packs.PackError as err:
        raise PackIndexError(f"{url}: {err}") from err
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/"
    files = {path: _get(raw + prefix + path, "*/*").decode("utf-8") for path in wanted}
    try:
        pack = packs.verify_folder(files)
    except packs.PackError as err:
        raise PackIndexError(f"{url}: {err}") from err
    candidates = [prefix + p for p in paths if _LICENCE_FILE.match(p)]
    candidates += [e["path"] for e in tree["tree"] if e.get("type") == "blob" and _LICENCE_FILE.match(e["path"])]
    licence_text = any(MIT_TEXT.search(_get(raw + path, "*/*").decode("utf-8", errors="replace")) for path in candidates)
    return pack, licence_text


def read_community(root: Path) -> list[dict[str, Any]]:
    """The hand-edited community list: {"packs": [{"url": ..., "thumbnail"?: item id}]}."""
    path = root / COMMUNITY_FILE
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    listed = data.get("packs") if isinstance(data, dict) else None
    if not isinstance(listed, list) or not all(isinstance(p, dict) and isinstance(p.get("url"), str) for p in listed):
        raise PackIndexError(f'{COMMUNITY_FILE}: must be {{"packs": [{{"url": "https://github.com/..."}}]}}')
    return listed


def community_packs(
    root: Path, packs: ModuleType, *, fetch: bool, kept: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[str]]:
    entries, problems = [], []
    for listed in read_community(root):
        url = listed["url"].rstrip("/")
        if not fetch:
            entry = next((e for e in kept if e.get("url") == url and e.get("source") == "community"), None)
            if entry is None:
                problems.append(f"{url}: not in {INDEX_FILE} yet; run with --fetch")
            else:
                entries.append(entry)
            continue
        try:
            pack, licence_text = fetch_community(url, packs)
            problems += check_rules(pack, "community", licence_text)
            entries.append(entry_of(pack, url, "community", listed.get("thumbnail")))
        except PackIndexError as err:
            problems.append(str(err))
    return entries, problems


# ---------------------------------------------------------------------------- the index


def build(root: Path, home3d: Path, *, fetch: bool) -> tuple[dict[str, Any], list[str]]:
    """The index and the problems found (an index with problems is not written)."""
    packs = load_packs_module(home3d)
    kept = []
    if (root / INDEX_FILE).exists():
        kept = json.loads((root / INDEX_FILE).read_text(encoding="utf-8")).get("packs", [])
    official, problems = official_packs(root, packs)
    community, more = community_packs(root, packs, fetch=fetch, kept=kept)
    problems += more
    seen: Counter[str] = Counter(e["id"] for e in official + community)
    problems += [f"{pack_id}: listed {n} times; pack ids must be unique" for pack_id, n in seen.items() if n > 1]
    return {"format": INDEX_FORMAT, "version": INDEX_VERSION, "packs": official + community}, problems


def text_of(index: dict[str, Any]) -> str:
    # sorted keys: the check fills in an item's defaults in no fixed order
    return json.dumps(index, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("root", type=Path, help="this repository's checkout")
    parser.add_argument("--home3d", type=Path, required=True, help="a Home 3D checkout (its packs.py checks the packs)")
    parser.add_argument("--fetch", action="store_true", help="fetch and check the community packs again (build)")
    args = parser.parse_args()
    try:
        index, problems = build(args.root, args.home3d, fetch=args.fetch or args.command == "check")
    except PackIndexError as err:
        sys.exit(str(err))
    if problems:
        sys.exit("the index breaks these rules:\n  " + "\n  ".join(problems))
    path = args.root / INDEX_FILE
    if args.command == "build":
        path.write_text(text_of(index), encoding="utf-8", newline="\n")
        print(f"wrote {path}: {len(index['packs'])} packs")
        return
    current = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.exists() else ""
    if current != text_of(index):
        sys.exit(f"{INDEX_FILE} is out of date: run python tools/build_index.py build . --home3d <checkout> --fetch")
    print(f"ok: {len(index['packs'])} packs listed, every one passes the rules")


if __name__ == "__main__":
    main()
