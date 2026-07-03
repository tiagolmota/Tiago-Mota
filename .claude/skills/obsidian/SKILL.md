---
name: obsidian
description: Work with Obsidian vaults — folders of markdown notes linked via [[wikilinks]], YAML frontmatter properties, tags, embeds, callouts, daily notes, and a shared "memory" folder of durable notes. Use this whenever the user asks to create, edit, organize, rename, link, or search notes in an Obsidian vault, fix or trace backlinks, find orphan notes, manage tags/properties, work with Obsidian-flavored markdown syntax, connect Claude to a vault via MCP, or use Obsidian notes as persistent memory across sessions/LLMs. Make sure to use this skill whenever the user mentions "my vault", "my notes" in an Obsidian context, a folder of .md files with [[double bracket]] links between them, or wants Claude to "remember" things across sessions using Obsidian.
---

# Obsidian

An Obsidian vault is just a folder of plain markdown files (`.md`), plus a hidden
`.obsidian/` config folder Obsidian itself manages — don't touch that folder unless
asked. Everything else here is regular text, so you can read, write, and grep it
like any other markdown, with a few Obsidian-specific conventions layered on top.

## Core syntax to recognize

- **Wikilinks**: `[[Note Name]]` links to a note by its filename (without `.md`).
  Variants: `[[Note Name|Display Text]]` (alias), `[[Note Name#Heading]]` (link to a
  heading), `[[Note Name#^block-id]]` (link to a block).
- **Embeds**: `![[Note Name]]` transcludes the whole note; `![[image.png]]` embeds an
  image. Same heading/block syntax applies for partial embeds.
- **Tags**: `#tag-name` inline, or a `tags:` list in frontmatter. Nested tags use
  `#parent/child`.
- **Frontmatter (properties)**: a YAML block at the very top of the file between
  `---` lines, e.g. `status: draft`, `tags: [project, urgent]`, `aliases: [...]`.
- **Callouts**: `> [!note]`, `> [!warning]`, etc. — blockquotes with a type marker.
- **Dataview queries** (only if the Dataview plugin is in use — check for
  ` ```dataview ` blocks or `.md` files referencing it): a query language embedded
  in code fences. Treat these as data queries over frontmatter properties across the
  vault, not as regular code.

## Working with notes

- Note identity is the **filename**, not the path — Obsidian resolves `[[Note Name]]`
  by matching filename anywhere in the vault (unless the link includes a path).
  Two notes can't share a filename even in different folders without breaking links.
- When creating a note, check whether the vault has a templates folder (look for a
  `templates:` setting in `.obsidian/` or a folder literally named `Templates`) and
  follow its conventions (frontmatter fields, heading structure) rather than
  inventing a new layout.
- Daily notes typically live in a `Daily Notes/` or similarly named folder with
  filenames like `2026-07-01.md`. Check existing daily notes for the date format and
  frontmatter in use before creating a new one.
- Keep frontmatter valid YAML — list syntax (`tags: [a, b]` or a `-` list) must stay
  consistent with what the rest of the vault uses.

## Renaming or moving a note

This is the one operation where Obsidian's own file-rename tracking doesn't apply,
because you're editing files directly rather than through the app: **renaming a note's
file does not update the `[[old name]]` links inside other notes.** Every wikilink,
alias link, and embed pointing at the old name will silently break unless you update
them too.

Use `scripts/rename_note.py` to do both atomically:

```bash
python3 scripts/rename_note.py <vault_path> "<Old Note Name>" "<New Note Name>"
```

It renames the file and rewrites every `[[Old Note Name]]`, `[[Old Note Name|alias]]`,
`[[Old Note Name#Heading]]`, and `![[Old Note Name]]` reference across the vault to
the new name, preserving aliases/headings/embed markers. Run it with no vault writes
(`--dry-run`) first if the user wants to review the diff before applying it.

## Finding backlinks and orphan notes

- To find every note that links to a given note, use `scripts/find_backlinks.py`
  rather than grepping by hand — it correctly matches all the link variants above
  (aliases, headings, embeds) instead of just a literal substring:

  ```bash
  python3 scripts/find_backlinks.py <vault_path> "<Note Name>"
  ```

- To find notes with no incoming or outgoing links (candidates for cleanup or
  linking into the graph), use `scripts/list_orphans.py`:

  ```bash
  python3 scripts/list_orphans.py <vault_path>
  ```

Both scripts skip the `.obsidian/` folder and any path the user names with
`--exclude`.

## Connecting live via MCP (optional)

If tools named `mcp__obsidian__*` (or similarly named) are already available in
this session, an MCP server is bridging Claude to the vault directly — prefer
those tools over the scripts above for reads/writes, since they don't require
re-passing the vault path on every call and reflect the live state Obsidian
itself sees. The scripts remain the fallback for sessions with only filesystem
access (e.g. a remote/headless session that can't reach the user's machine).
Setting up that MCP connection has to happen on the user's own machine, next to
their running Obsidian — see `references/mcp-setup.md` for how, and don't
attempt it from a session that only has filesystem access to a checked-out vault.

## Shared memory notes

Some vaults dedicate a folder (commonly named `Memory`, `Memoria`, or
`Second Brain`) to small, durable notes — facts, preferences, decisions — meant
to be read back at the start of a session rather than re-derived every time.
The point of keeping this in the vault instead of a model's own memory feature
is that it's plain markdown: any LLM or client with access to the vault (via
MCP or the filesystem) shares the same memory, instead of each tool keeping its
own private, incompatible copy.

- Before starting non-trivial work in a vault, check whether such a folder
  exists and skim it for relevant context. Use `scripts/memory_digest.py
  <vault_path>` to pull all notes in that folder (or one named with `--folder`)
  into a single digest instead of opening each file individually.
- When you learn something durable worth remembering — a stated preference, a
  recurring convention, a decision — write or update a small note in that
  folder rather than letting it live only in the current conversation. Keep
  each note atomic (one fact/decision per note) so it stays easy to skim,
  update, or supersede later.
- Don't invent a new memory folder name if the vault already has one; match
  whatever's there.

## General editing guidance

- Preserve existing frontmatter fields you're not asked to change — don't reformat
  someone's property schema as a side effect of an unrelated edit.
- When adding links between notes, prefer `[[Note Name]]` over relative markdown
  links (`[text](path.md)`) unless the vault's existing notes clearly favor the
  latter — match whatever convention is already there.
- If asked to reorganize notes into folders, remember that's a rename in Obsidian's
  eyes only if the filename changes; moving a file to a new folder without renaming
  it does not break wikilinks (Obsidian resolves by filename), so no link rewriting
  is needed for a pure move.
