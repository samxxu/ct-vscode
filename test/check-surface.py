#!/usr/bin/env python3
"""Syntax-surface gate for syntaxes/ct.tmLanguage.json.

`check-grammar.py` proves *behaviour* on whole samples. This script proves
*coverage*: every CT-only construct listed in `surface.json` still has a grammar
rule and still fires on a known line. Renaming or deleting a rule, dropping a
fixture or breaking the fixture provenance turns `npm test` red.

The list is deliberately small and grouped (`top-level` / `keywords` /
`control` / `types`); the C passthrough surface is not listed, so the gate does
not grow into a full token snapshot (R-VS-1-6).

Samples are reused from `check-grammar.py` (loaded with `importlib`, its
`__main__` guard keeps `main()` from running), so the two gates share one scan
implementation.

    python3 test/check-surface.py
"""

import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "surface.json")
FIXTURES = os.path.join(HERE, "fixtures")
FIXTURES_README = os.path.join(FIXTURES, "README.md")
CHECK_GRAMMAR = os.path.join(HERE, "check-grammar.py")

# Uppercase string constants in check-grammar.py that are paths, not samples.
NOT_SAMPLES = {"HERE", "EXT", "ROOT", "GRAMMAR"}


def load_check_grammar():
    spec = importlib.util.spec_from_file_location("check_grammar", CHECK_GRAMMAR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture_files():
    out = []
    for dirpath, _, files in os.walk(FIXTURES):
        for name in files:
            out.append(os.path.relpath(os.path.join(dirpath, name), FIXTURES))
    return sorted(out)


def main():
    cg = load_check_grammar()
    with open(cg.GRAMMAR) as fh:
        grammar = json.load(fh)
    rules = cg.resolve(grammar["patterns"], grammar["repository"], [])
    rule_names = {name for name, _ in rules}
    samples = {name: value for name, value in vars(cg).items()
               if name.isupper() and isinstance(value, str) and name not in NOT_SAMPLES}

    with open(MANIFEST) as fh:
        manifest = json.load(fh)

    failures = []
    checks = 0
    entry_count = 0
    cache = {}

    def check(desc, cond, detail=""):
        nonlocal checks
        checks += 1
        if cond:
            print("  ok    %s" % desc)
        else:
            print("  FAIL  %s   %s" % (desc, detail))
            failures.append(desc)

    def rows_for(entry):
        if "sample" in entry:
            key = ("sample", entry["sample"])
            if key not in cache:
                cache[key] = cg.scan(samples[entry["sample"]], rules)
            return cache[key]
        key = ("fixture", entry["fixture"])
        if key not in cache:
            with open(os.path.join(FIXTURES, entry["fixture"])) as fh:
                cache[key] = cg.scan(fh.read(), rules)
        return cache[key]

    up = manifest["upstream"]
    print("surface  : %s %s (%s)" % (up["repo"], up["tag"], up["commit"]))
    print("grammar  : %d rules in scan order" % len(rules))
    print()

    for group in manifest["groups"]:
        print("%s -- %s" % (group["id"], group["title"]))
        check("%s: at least 5 entries" % group["id"], len(group["entries"]) >= 5,
              "%d entries" % len(group["entries"]))
        for entry in group["entries"]:
            entry_count += 1
            rule = entry["rule"]
            if "sample" in entry:
                where = "synthetic %s" % entry["sample"]
                source_ok = entry["sample"] in samples
            else:
                where = entry["fixture"]
                source_ok = os.path.isfile(os.path.join(FIXTURES, entry["fixture"]))
            label = "%s -> %s @ %s" % (entry["construct"], rule, where)
            check("rule exists: " + label, rule in rule_names, "not in the grammar")
            if not source_ok:
                check("source exists: " + label, False, "missing sample or fixture")
                continue
            rows = rows_for(entry)
            hit = any(h[0] == rule for _, line, hits in rows
                      if entry["line"] in line for h in hits)
            check("hit: " + label, hit,
                  "no `%s` hit on a line containing %r" % (rule, entry["line"]))
        print()

    print("fixtures provenance -- %s" % os.path.relpath(FIXTURES_README, HERE))
    with open(FIXTURES_README) as fh:
        readme = fh.read()
    check("README names the upstream tag %s" % up["tag"], up["tag"] in readme)
    check("README names the upstream commit %s" % up["commit"], up["commit"] in readme)
    files = fixture_files()
    listed = sorted(re.findall(r"^- `([^`]+)`$", readme, re.M))
    on_disk = set(files) - {"README.md"}
    missing = sorted(on_disk - set(listed))
    extra = sorted(set(listed) - on_disk)
    check("README lists every fixture file (%d)" % len(on_disk), not missing and not extra,
          "only on disk: %s; only in README: %s" % (missing, extra))
    check("README records the fixture count %d" % len(on_disk),
          ("**%d**" % len(on_disk)) in readme, "count marker not found")

    print()
    print("== %d entries in %d groups, %d checks, %d failed =="
          % (entry_count, len(manifest["groups"]), checks, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
