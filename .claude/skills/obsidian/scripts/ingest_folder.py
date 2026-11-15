#!/usr/bin/env python3
"""Bulk-import documents from a source folder into an Obsidian vault as notes.

For pulling an existing folder of files (reports, PDFs, text dumps) into a
vault so their content joins the linkable knowledge graph instead of sitting
outside it in formats Obsidian/Claude can't search or link. Only point this
at folders actually worth importing -- see the caution in the skill's
SKILL.md before running it against something as broad as an entire drive.
"""
import argparse
import datetime
import os
import subprocess

DEFAULT_EXTENSIONS = {'.txt', '.md', '.markdown', '.csv', '.json', '.html', '.htm', '.pdf', '.docx'}
DEFAULT_SKIP_DIRS = {
    '.git', '.obsidian', 'node_modules', '__pycache__',
    '$RECYCLE.BIN', 'System Volume Information', 'Windows',
    'Program Files', 'Program Files (x86)', 'AppData', 'ProgramData',
}
MAX_CHARS = 20000  # ~5k words -- keeps notes skimmable; the rest stays in the source file


def extract_text(path, ext):
    if ext in {'.txt', '.md', '.markdown', '.csv', '.json', '.html', '.htm'}:
        with open(path, encoding='utf-8', errors='ignore') as fh:
            return fh.read()
    if ext == '.pdf':
        try:
            result = subprocess.run(
                ['pdftotext', path, '-'], capture_output=True, text=True, timeout=60)
        except FileNotFoundError:
            return None
        return result.stdout if result.returncode == 0 else None
    if ext == '.docx':
        try:
            import docx
        except ImportError:
            return None
        try:
            return '\n'.join(p.text for p in docx.Document(path).paragraphs)
        except Exception:
            return None
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source_root')
    ap.add_argument('vault_path')
    ap.add_argument('--dest-folder', default='Imported',
                     help='Vault subfolder to import into (default: Imported)')
    ap.add_argument('--extensions', nargs='*', default=None,
                     help=f'File extensions to import (default: {" ".join(sorted(DEFAULT_EXTENSIONS))})')
    ap.add_argument('--exclude-dir', action='append', default=[],
                     help='Additional directory name to skip (repeatable)')
    ap.add_argument('--max-size-mb', type=float, default=20,
                     help='Skip files larger than this (default 20 MB)')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    extensions = {e if e.startswith('.') else f'.{e}' for e in (args.extensions or DEFAULT_EXTENSIONS)}
    skip_dirs = DEFAULT_SKIP_DIRS | set(args.exclude_dir)
    max_bytes = args.max_size_mb * 1024 * 1024
    dest_root = os.path.join(args.vault_path, args.dest_folder)

    imported = skipped_ext = skipped_size = failed = 0

    for root, dirs, files in os.walk(args.source_root):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        for fname in files:
            src = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext not in extensions:
                skipped_ext += 1
                continue
            try:
                if os.path.getsize(src) > max_bytes:
                    skipped_size += 1
                    continue
            except OSError:
                failed += 1
                continue

            text = extract_text(src, ext)
            if text is None:
                failed += 1
                print(f'  Could not extract text from {src} (missing extractor or read error)')
                continue

            rel_dir = os.path.relpath(root, args.source_root)
            note_dir = dest_root if rel_dir == '.' else os.path.join(dest_root, rel_dir)
            note_path = os.path.join(note_dir, os.path.splitext(fname)[0] + '.md')
            top_folder = rel_dir.split(os.sep)[0] if rel_dir != '.' else 'root'

            truncated = len(text) > MAX_CHARS
            note = (
                '---\n'
                'type: imported\n'
                f'source: "{src}"\n'
                f'imported: {datetime.date.today().isoformat()}\n'
                f'tags: [imported, {top_folder}]\n'
                '---\n\n'
                f'{text[:MAX_CHARS].strip()}\n'
            )
            if truncated:
                note += f'\n> [!note] Truncated at {MAX_CHARS} characters. Full content: `{src}`\n'

            imported += 1
            if args.dry_run:
                print(f'[dry-run] Would write {note_path}')
            else:
                os.makedirs(note_dir, exist_ok=True)
                with open(note_path, 'w', encoding='utf-8') as fh:
                    fh.write(note)

    print(f'\n{imported} note(s) {"would be " if args.dry_run else ""}imported into {dest_root}')
    print(f'{skipped_ext} file(s) skipped (extension not in import list)')
    print(f'{skipped_size} file(s) skipped (over {args.max_size_mb} MB)')
    print(f'{failed} file(s) failed to extract (see messages above)')


if __name__ == '__main__':
    main()
