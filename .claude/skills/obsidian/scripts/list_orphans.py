#!/usr/bin/env python3
"""List Obsidian vault notes that have no incoming and no outgoing links."""
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


def note_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('--exclude', action='append', default=[],
                     help='Vault-relative path to skip (repeatable)')
    args = ap.parse_args()

    files = list(iter_markdown_files(args.vault_path, args.exclude))
    outgoing = {}
    linked_names = set()
    for path in files:
        with open(path, encoding='utf-8') as fh:
            content = fh.read()
        links = {m.group(1).strip().lower() for m in WIKILINK_RE.finditer(content) if m.group(1).strip()}
        outgoing[path] = links
        linked_names |= links

    orphans = [p for p in files if not outgoing[p] and note_name(p).lower() not in linked_names]

    if not orphans:
        print('No orphan notes found.')
        return
    print(f'{len(orphans)} orphan note(s) (no incoming or outgoing links):')
    for o in orphans:
        print(f'  {o}')


if __name__ == '__main__':
    main()
