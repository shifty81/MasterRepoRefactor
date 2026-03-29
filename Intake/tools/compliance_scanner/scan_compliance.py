#!/usr/bin/env python3
import argparse
import json
import os
import re
from pathlib import Path

def emit(level, code, message):
    print(f"{level} [{code}] {message}")

def any_readme_in_dir(path):
    if not os.path.isdir(path):
        return False
    for name in os.listdir(path):
        if name.lower().startswith("readme"):
            return True
    return False

def file_contains_token(path, token):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return token in f.read()
    except Exception:
        return False

def iter_text_files(repo):
    for dp, _, fns in os.walk(repo):
        for fn in fns:
            if fn.lower().endswith((".cpp",".h",".hpp",".c",".cc",".md",".txt",".json",".ini",".cmake",".py")):
                yield os.path.join(dp, fn)

def main():
    parser = argparse.ArgumentParser(description="Scan repo compliance against the Split Docs Pack standard.")
    parser.add_argument("--repo", required=True, help="Repo root to scan")
    parser.add_argument("--docs", required=True, help="Docs pack root to validate")
    parser.add_argument("--rules", default=None, help="Optional rules JSON path")
    args = parser.parse_args()

    rules_path = args.rules or os.path.join(os.path.dirname(__file__), "rules.json")
    with open(rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    fail_count = 0
    warn_count = 0

    # required dirs
    for rel in rules.get("required_top_level_dirs", []):
        if os.path.isdir(os.path.join(args.repo, rel)):
            emit("PASS", "DIR_OK", f"Found required directory: {rel}")
        else:
            emit("FAIL", "DIR_MISSING", f"Missing required directory: {rel}")
            fail_count += 1

    # required docs
    for rel in rules.get("required_pack_docs", []):
        if os.path.isfile(os.path.join(args.docs, rel)):
            emit("PASS", "DOC_OK", f"Found docs pack file: {rel}")
        else:
            emit("FAIL", "DOC_MISSING", f"Missing docs pack file: {rel}")
            fail_count += 1

    # required JSON
    for rel in rules.get("required_json_files", []):
        if os.path.isfile(os.path.join(args.repo, rel)):
            emit("PASS", "JSON_OK", f"Found required JSON: {rel}")
        else:
            emit("FAIL", "JSON_MISSING", f"Missing required JSON: {rel}")
            fail_count += 1

    # duplicate domain pairs
    for a, b in rules.get("duplicate_domain_pairs", []):
        a_exists = os.path.exists(os.path.join(args.repo, a))
        b_exists = os.path.exists(os.path.join(args.repo, b))
        if a_exists and b_exists:
            emit("WARN", "DUP_DOMAIN", f"Both canonical-domain candidates exist: {a} and {b}")
            warn_count += 1
        else:
            emit("PASS", "DUP_DOMAIN_OK", f"No duplicate domain pair conflict for: {a} / {b}")

    # banned token scan
    banned_tokens = rules.get("banned_tokens", [])
    for token in banned_tokens:
        hits = []
        for path in iter_text_files(args.repo):
            if file_contains_token(path, token):
                hits.append(os.path.relpath(path, args.repo))
                if len(hits) >= 10:
                    break
        if hits:
            emit("WARN", "BANNED_TOKEN", f"Token '{token}' found in: {', '.join(hits)}")
            warn_count += 1
        else:
            emit("PASS", "BANNED_TOKEN_OK", f"Token not found: {token}")

    # readme coverage
    for rel in rules.get("warn_on_missing_readme_dirs", []):
        full = os.path.join(args.repo, rel)
        if os.path.isdir(full):
            if any_readme_in_dir(full):
                emit("PASS", "README_OK", f"README present in {rel}")
            else:
                emit("WARN", "README_MISSING", f"No top-level README found in {rel}")
                warn_count += 1

    # TODO/FIXME scan
    todo_hits = []
    for path in iter_text_files(args.repo):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception:
            continue
        if "TODO" in text or "FIXME" in text:
            todo_hits.append(os.path.relpath(path, args.repo))
            if len(todo_hits) >= 15:
                break
    if todo_hits:
        emit("WARN", "TODO_PRESENT", f"TODO/FIXME markers found in: {', '.join(todo_hits)}")
        warn_count += 1
    else:
        emit("PASS", "TODO_NONE", "No TODO/FIXME markers found in scanned text files")

    print("")
    print(f"Summary: FAIL={fail_count} WARN={warn_count}")
    raise SystemExit(1 if fail_count else 0)

if __name__ == "__main__":
    main()
