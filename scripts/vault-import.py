#!/usr/bin/env python3
"""
vault-import.py — Import any document into the Obsidian vault via MarkItDown.

Converts PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, images, URLs, and
YouTube links to Markdown and saves them as vault notes with YAML frontmatter.

Usage:
  python scripts/vault-import.py file.pdf
  python scripts/vault-import.py slides.pptx --tag ufcd10791 --folder UFCD_imports
  python scripts/vault-import.py https://example.com/article
  python scripts/vault-import.py https://youtu.be/xxx --tag notebooklm
  python scripts/vault-import.py *.pdf --folder PDFs
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("Error: markitdown not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

VAULT = Path("graphify-out/obsidian")


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text.strip())
    return text[:80]


def note_name(source: str) -> str:
    if source.startswith("http"):
        # Extract meaningful part of URL
        clean = re.sub(r"https?://", "", source).split("?")[0].rstrip("/")
        parts = clean.replace("/", "_").replace(".", "_")
        return f"import_{parts}"[:80]
    return Path(source).stem


def build_frontmatter(title: str, source: str, tags: list[str]) -> str:
    today = date.today().isoformat()
    tag_list = "\n".join(f"  - {t}" for t in tags)
    return f"""---
title: "{title}"
source: "{source}"
imported: "{today}"
tags:
{tag_list}
---

"""


def convert_one(source: str, vault: Path, folder: str | None, tags: list[str]) -> Path:
    md = MarkItDown()

    try:
        result = md.convert(source)
    except Exception as e:
        print(f"  ✗ Failed to convert {source}: {e}", file=sys.stderr)
        raise

    content = result.text_content.strip()
    if not content:
        raise ValueError("Conversion produced empty output")

    # Derive title from first heading or filename
    first_line = content.splitlines()[0] if content else ""
    if first_line.startswith("#"):
        title = first_line.lstrip("# ").strip()
    else:
        title = note_name(source)

    # Destination
    dest_dir = vault / folder if folder else vault
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_name = slugify(note_name(source)) + ".md"
    out_path = dest_dir / out_name

    # Avoid overwriting — append _2, _3 …
    n = 1
    while out_path.exists():
        n += 1
        out_path = dest_dir / (slugify(note_name(source)) + f"_{n}.md")

    full_tags = ["markitdown/import"] + tags
    out_path.write_text(build_frontmatter(title, source, full_tags) + content + "\n")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Import documents into the Obsidian vault")
    parser.add_argument("sources", nargs="+", help="Files, URLs, or YouTube links to import")
    parser.add_argument("--vault", default=str(VAULT), help="Vault path (default: graphify-out/obsidian)")
    parser.add_argument("--folder", default=None, help="Subfolder inside the vault (e.g. UFCD_imports)")
    parser.add_argument("--tag", action="append", default=[], dest="tags", metavar="TAG",
                        help="Extra tag to add (repeatable: --tag ufcd10791 --tag security)")
    args = parser.parse_args()

    vault = Path(args.vault)
    if not vault.exists():
        print(f"Error: vault not found at {vault}", file=sys.stderr)
        sys.exit(1)

    ok = fail = 0
    for source in args.sources:
        print(f"↳ Converting: {source}")
        try:
            out = convert_one(source, vault, args.folder, args.tags)
            print(f"  ✓ → {out}")
            ok += 1
        except Exception:
            fail += 1

    print(f"\n{ok} imported, {fail} failed.")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
