#!/usr/bin/env python3
"""Load a vault's full session-start context in a single call.

Combines SOUL.md, CLAUDE.md, and the Memory/ folder digest into one output,
instead of three separate reads. Each separate Read/tool call has its own
overhead (a round trip plus repeated framing); collapsing them into one
script run cuts that overhead and gives a single, consistently-formatted
block to work from at the start of a session.
"""
import argparse
import os

MEMORY_FOLDER_NAMES = ['Memory', 'Memoria', 'Memória', 'Memórias', 'Second Brain']


def read_if_exists(path):
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as fh:
            return fh.read().strip()
    return None


def find_memory_folder(vault_path, override):
    if override:
        candidate = os.path.join(vault_path, override)
        return candidate if os.path.isdir(candidate) else None
    for name in MEMORY_FOLDER_NAMES:
        candidate = os.path.join(vault_path, name)
        if os.path.isdir(candidate):
            return candidate
    return None


def memory_digest(folder, vault_path):
    notes = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != '.obsidian']
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            with open(path, encoding='utf-8') as fh:
                content = fh.read().strip()
            rel = os.path.relpath(path, vault_path)
            notes.append(f'### {rel}\n\n{content}')
    return notes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('--memory-folder', help='Memory folder name (default: auto-detect common names)')
    ap.add_argument('--output', help='Write the combined context to this file instead of stdout')
    args = ap.parse_args()

    sections = []

    soul = read_if_exists(os.path.join(args.vault_path, 'SOUL.md'))
    sections.append('## Identity (SOUL.md)\n\n' + (soul if soul else '_Not present in this vault._'))

    claude_md = read_if_exists(os.path.join(args.vault_path, 'CLAUDE.md'))
    sections.append('## Instructions (CLAUDE.md)\n\n' + (claude_md if claude_md else '_Not present in this vault._'))

    mem_folder = find_memory_folder(args.vault_path, args.memory_folder)
    if mem_folder:
        notes = memory_digest(mem_folder, args.vault_path)
        mem_section = (f'_{len(notes)} note(s) from {os.path.relpath(mem_folder, args.vault_path)}/_\n\n'
                        + '\n\n---\n\n'.join(notes)) if notes else '_Folder exists but has no notes yet._'
    else:
        mem_section = '_No memory folder found in this vault._'
    sections.append('## Memory\n\n' + mem_section)

    digest = '# Vault context\n\n' + '\n\n---\n\n'.join(sections) + '\n'

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fh:
            fh.write(digest)
        print(f'Wrote combined vault context to {args.output}')
    else:
        print(digest)


if __name__ == '__main__':
    main()
