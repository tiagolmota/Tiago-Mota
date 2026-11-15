#!/usr/bin/env python3
"""Rename an Obsidian note and rewrite every [[wikilink]] that points to it."""
import argparse
import os
import re
import shutil
import sys

WIKILINK_RE = re.compile(r'(!?)\[\[([^\]|#]+?)((?:#[^\]|]*)?)(\|[^\]]*)?\]\]')


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


def find_note_files(vault_path, name, exclude):
    target = (name + '.md').lower()
    return [p for p in iter_markdown_files(vault_path, exclude) if os.path.basename(p).lower() == target]


def rewrite_links(content, old_name, new_name):
    changed = False

    def repl(m):
        nonlocal changed
        embed, target, anchor, alias = m.groups()
        if target.strip().lower() == old_name.lower():
            changed = True
            target = new_name
        return f'{embed}[[{target}{anchor or ""}{alias or ""}]]'

    return WIKILINK_RE.sub(repl, content), changed


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('old_name', help='Note name without the .md extension')
    ap.add_argument('new_name', help='New note name without the .md extension')
    ap.add_argument('--exclude', action='append', default=[],
                     help='Vault-relative path to skip (repeatable)')
    ap.add_argument('--dry-run', action='store_true', help='Show changes without writing them')
    args = ap.parse_args()

    matches = find_note_files(args.vault_path, args.old_name, args.exclude)
    if not matches:
        print(f'No note file found for "{args.old_name}"', file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1:
        print(f'Warning: multiple files named "{args.old_name}.md" found, renaming all:', file=sys.stderr)
        for m in matches:
            print(f'  {m}', file=sys.stderr)

    prefix = '[dry-run] ' if args.dry_run else ''
    updated_files = []
    for path in iter_markdown_files(args.vault_path, args.exclude):
        with open(path, encoding='utf-8') as fh:
            content = fh.read()
        new_content, changed = rewrite_links(content, args.old_name, args.new_name)
        if changed:
            updated_files.append(path)
            if not args.dry_run:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)

    for path in matches:
        new_path = os.path.join(os.path.dirname(path), args.new_name + '.md')
        if os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(path):
            print(f'Refusing to overwrite existing file: {new_path}', file=sys.stderr)
            sys.exit(1)
        print(f'{prefix}Rename: {path} -> {new_path}')
        if not args.dry_run:
            shutil.move(path, new_path)

    print(f'{prefix}Updated links in {len(updated_files)} file(s):')
    for f in updated_files:
        print(f'  {f}')


if __name__ == '__main__':
    main()
