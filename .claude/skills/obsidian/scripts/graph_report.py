#!/usr/bin/env python3
"""Report on an Obsidian vault's link graph: connected components, orphans,
and tag-based suggestions for linking isolated clusters into the rest of the
vault so no note is stranded from the knowledge graph.
"""
import argparse
import os
import re

WIKILINK_RE = re.compile(r'!?\[\[([^\]|#]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
FRONTMATTER_RE = re.compile(r'\A---\n(.*?\n)---\n', re.DOTALL)
INLINE_TAG_RE = re.compile(r'(?<!\S)#([A-Za-z0-9_/-]+)')


class DSU:
    def __init__(self, items):
        self.parent = {i: i for i in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


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


def parse_tags(content):
    tags = {m.group(1).lower() for m in INLINE_TAG_RE.finditer(content)}
    fm = FRONTMATTER_RE.match(content)
    if not fm:
        return tags
    block = fm.group(1)
    m = re.search(r'^tags:\s*\[([^\]]*)\]', block, re.MULTILINE)
    if m:
        tags |= {t.strip().strip('"\'').lower() for t in m.group(1).split(',') if t.strip()}
    else:
        m = re.search(r'^tags:\s*\n((?:\s*-\s*.+\n?)+)', block, re.MULTILINE)
        if m:
            tags |= {line.strip('- ').strip().strip('"\'').lower()
                     for line in m.group(1).splitlines() if line.strip()}
    return tags


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('vault_path')
    ap.add_argument('--exclude', action='append', default=[],
                     help='Vault-relative path to skip (repeatable)')
    ap.add_argument('--max-suggestions', type=int, default=20,
                     help='Cap on link suggestions printed (default 20)')
    args = ap.parse_args()

    files = list(iter_markdown_files(args.vault_path, args.exclude))
    names = {note_name(p): p for p in files}
    dsu = DSU(names.keys())
    tags_by_name = {}
    edge_count = 0

    for name, path in names.items():
        with open(path, encoding='utf-8') as fh:
            content = fh.read()
        tags_by_name[name] = parse_tags(content)
        for m in WIKILINK_RE.finditer(content):
            target = m.group(1).strip()
            match = next((n for n in names if n.lower() == target.lower()), None)
            if match and match != name:
                dsu.union(name, match)
                edge_count += 1

    components = {}
    for name in names:
        components.setdefault(dsu.find(name), []).append(name)
    ordered = sorted(components.values(), key=len, reverse=True)

    print(f'{len(names)} note(s), {edge_count} link(s) resolved to notes in the vault.')
    print(f'{len(ordered)} connected component(s):')
    for comp in ordered:
        label = comp[0] if len(comp) > 1 else f'{comp[0]} (isolated)'
        print(f'  [{len(comp)}] {label}' + (f' + {len(comp) - 1} more' if len(comp) > 1 else ''))

    if len(ordered) <= 1:
        print('\nThe vault is already a single connected graph — nothing to merge.')
        return

    main_component = set(ordered[0])
    suggestions = []
    for comp in ordered[1:]:
        best = None  # (shared_tag_count, name_in_comp, name_in_main, shared_tags)
        for name in comp:
            for other in main_component:
                shared = tags_by_name.get(name, set()) & tags_by_name.get(other, set())
                if shared and (best is None or len(shared) > best[0]):
                    best = (len(shared), name, other, shared)
        if best:
            suggestions.append((best[1], best[2], best[3]))
        else:
            suggestions.append((comp[0], None, None))

    print(f'\nSuggested links to connect every cluster to the rest of the vault '
          f'(showing up to {args.max_suggestions}):')
    for name, other, shared in suggestions[:args.max_suggestions]:
        if other:
            print(f'  Link [[{name}]] <-> [[{other}]] — shared tags: {", ".join(sorted(shared))}')
        else:
            print(f'  [[{name}]] shares no tags with the main graph — link it in manually '
                  f'based on its actual content.')


if __name__ == '__main__':
    main()
