#!/usr/bin/env python3
"""Concatenate memory notes from a vault into a single digest.

Lets an LLM load durable, human-readable memory (facts, preferences,
decisions) from a shared Obsidian folder at the start of a session, instead
of relying on any one client's proprietary/ephemeral memory.
"""
import argparse
import os

DEFAULT_FOLDER_NAMES = ['Memory', 'Memoria', 'Memória', 'Memórias', 'Second Brain']


def find_memory_folder(vault_path):
    for name in DEFAULT_FOLDER_NAMES:
        candidate = os.path.join(vault_path, name)
        if os.path.isdir(candidate):
            return candidate
    return None


def iter_notes(folder, tag):
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            if tag:
                with open(path, encoding='utf-8') as fh:
                    content = fh.read()
                if f'#{tag}' not in content and tag not in content:
                    continue
                yield path, content
            else:
                with open(path, encoding='utf-8') as fh:
                    yield path, fh.read()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('--folder', help='Memory folder name (default: auto-detect common names)')
    ap.add_argument('--tag', help='Only include notes containing this tag/word')
    ap.add_argument('--output', help='Write digest to this file instead of stdout')
    args = ap.parse_args()

    folder = os.path.join(args.vault_path, args.folder) if args.folder else find_memory_folder(args.vault_path)
    if not folder or not os.path.isdir(folder):
        print('No memory folder found. Pass --folder to point at one explicitly '
              f'(tried: {", ".join(DEFAULT_FOLDER_NAMES)}).')
        return

    parts = []
    for path, content in iter_notes(folder, args.tag):
        rel = os.path.relpath(path, args.vault_path)
        parts.append(f'## {rel}\n\n{content.strip()}\n')

    if not parts:
        print(f'No memory notes found in {folder}.')
        return

    digest = f'# Memory digest ({len(parts)} note(s) from {os.path.relpath(folder, args.vault_path)})\n\n' + '\n---\n\n'.join(parts)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fh:
            fh.write(digest)
        print(f'Wrote digest of {len(parts)} note(s) to {args.output}')
    else:
        print(digest)


if __name__ == '__main__':
    main()
