#!/usr/bin/env python3
"""Find every note in an Obsidian vault that links to a given note."""
import argparse
import os
import re

WIKILINK_RE = re.compile(r'!?\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')


def iter_markdown_files(vault_path, exclude):
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, vault_path)
            if any(rel == e or rel.startswith(e + os.sep) for e in exclude):
                continue
            yield path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('note_name', help='Note name without the .md extension')
    ap.add_argument('--exclude', action='append', default=[],
                     help='Vault-relative path to skip (repeatable)')
    args = ap.parse_args()

    target = args.note_name.strip().lower()
    found = []
    for path in iter_markdown_files(args.vault_path, args.exclude):
        with open(path, encoding='utf-8') as fh:
            content = fh.read()
        if any(m.group(1).strip().lower() == target for m in WIKILINK_RE.finditer(content)):
            found.append(path)

    if not found:
        print(f'No backlinks found for "{args.note_name}"')
        return
    print(f'{len(found)} note(s) link to "{args.note_name}":')
    for f in found:
        print(f'  {f}')


if __name__ == '__main__':
    main()
