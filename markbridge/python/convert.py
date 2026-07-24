#!/usr/bin/env python3
"""
convert.py — MarkBridge conversion worker.
Called by Electron main process via child_process.spawn.
Reads JSON from stdin, writes JSON to stdout.

Protocol:
  stdin:  {"action":"convert","source":"path/or/url","dest":"folder","profile":"Claude","tags":[]}
  stdin:  {"action":"ping"}
  stdout: {"ok":true,"out":"path.md","bytes":1234}
  stdout: {"ok":false,"error":"message"}
  stdout: {"pong":true,"version":"markitdown x.y.z"}
"""

import sys
import json
import re
from datetime import date
from pathlib import Path

def get_md():
    try:
        from markitdown import MarkItDown
        import markitdown
        return MarkItDown(), getattr(markitdown, "__version__", "?")
    except ImportError:
        return None, None

PROFILES = {
    "Claude":     {"frontmatter": True,  "tags": ["markitdown/import"]},
    "NotebookLM": {"frontmatter": False, "tags": []},
    "ChatGPT":    {"frontmatter": False, "tags": []},
    "Generic":    {"frontmatter": False, "tags": []},
}

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", str(s))
    s = re.sub(r"[\s_]+", "-", s.strip())
    return s[:80].lower()

def build_note(title, source, content, profile_name, extra_tags):
    p = PROFILES.get(profile_name, PROFILES["Generic"])
    lines = []
    if p["frontmatter"]:
        tags = p["tags"] + extra_tags
        lines += ["---", f'title: "{title}"', f'source: "{source}"',
                  f'imported: "{date.today()}"', "tags:"] + \
                 [f"  - {t}" for t in tags] + ["---", ""]
    lines.append(content)
    return "\n".join(lines) + "\n"

def handle(req, md):
    action = req.get("action")

    if action == "ping":
        _, ver = get_md() if md is None else (md, "?")
        return {"pong": True, "version": ver}

    if action == "convert":
        source  = req["source"]
        dest    = Path(req["dest"])
        profile = req.get("profile", "Generic")
        tags    = req.get("tags", [])

        dest.mkdir(parents=True, exist_ok=True)

        result = md.convert(source)
        content = result.text_content.strip()
        if not content:
            return {"ok": False, "error": "Empty output"}

        # title from first heading or stem
        first = content.splitlines()[0] if content else ""
        title = first.lstrip("# ").strip() if first.startswith("#") else Path(source).stem

        stem = slugify(Path(source).stem if not source.startswith("http") else
                       re.sub(r"https?://", "", source).split("?")[0])
        out = dest / (stem + ".md")
        n = 1
        while out.exists():
            n += 1
            out = dest / f"{stem}_{n}.md"

        out.write_text(build_note(title, source, content, profile, tags), encoding="utf-8")
        return {"ok": True, "out": str(out), "bytes": out.stat().st_size}

    return {"ok": False, "error": f"Unknown action: {action}"}

def main():
    md, ver = get_md()
    if md is None:
        sys.stdout.write(json.dumps({"ok": False, "error": "markitdown not installed"}) + "\n")
        sys.stdout.flush()
        sys.exit(1)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle(req, md)
        except Exception as e:
            resp = {"ok": False, "error": str(e)}
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
