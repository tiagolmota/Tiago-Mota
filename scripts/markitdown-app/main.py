#!/usr/bin/env python3
"""
MarkBridge — Desktop app for converting documents to AI-ready Markdown.
Powered by Microsoft MarkItDown.

Usage: python scripts/markitdown-app/main.py
"""

import os
import sys
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from pathlib import Path

try:
    import customtkinter as ctk
except ImportError:
    sys.exit("Missing dependency: pip install customtkinter")

try:
    from markitdown import MarkItDown
except ImportError:
    sys.exit("Missing dependency: pip install 'markitdown[pdf,docx,pptx,xlsx]'")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_OK = True
except ImportError:
    WATCHDOG_OK = False

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_OK = True
except ImportError:
    TRAY_OK = False

# ── Config ──────────────────────────────────────────────────────────────────

SUPPORTED_EXT = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".html", ".htm",
                 ".csv", ".json", ".xml", ".epub", ".msg"}

AI_PROFILES = {
    "Claude":      {"frontmatter": True,  "tags": ["markitdown/import", "claude"]},
    "NotebookLM":  {"frontmatter": False, "tags": []},
    "ChatGPT":     {"frontmatter": False, "tags": []},
    "Genérico":    {"frontmatter": False, "tags": []},
}

APP_NAME = "MarkBridge"
VERSION  = "1.0.0"

# ── Conversion ───────────────────────────────────────────────────────────────

def convert_file(src: Path, dest_dir: Path, ai_profile: str, extra_tags: list[str]) -> Path:
    md = MarkItDown()
    result = md.convert(str(src))
    content = result.text_content.strip()
    if not content:
        raise ValueError("Conversion produced empty output")

    profile = AI_PROFILES.get(ai_profile, AI_PROFILES["Genérico"])
    slug = src.stem.lower().replace(" ", "-")
    out_path = dest_dir / (slug + ".md")

    n = 1
    while out_path.exists():
        n += 1
        out_path = dest_dir / f"{slug}_{n}.md"

    lines = []
    if profile["frontmatter"]:
        tags = profile["tags"] + extra_tags
        lines += [
            "---",
            f'title: "{src.stem}"',
            f'source: "{src}"',
            f'imported: "{datetime.now().date()}"',
            "tags:",
        ] + [f"  - {t}" for t in tags] + ["---", ""]

    lines.append(content)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def convert_url(url: str, dest_dir: Path, ai_profile: str) -> Path:
    import re
    md = MarkItDown()
    result = md.convert(url)
    content = result.text_content.strip()
    if not content:
        raise ValueError("Empty output for URL")

    slug = re.sub(r"[^\w-]", "-", re.sub(r"https?://", "", url).split("?")[0])[:60]
    profile = AI_PROFILES.get(ai_profile, AI_PROFILES["Genérico"])
    out_path = dest_dir / (slug + ".md")
    lines = []
    if profile["frontmatter"]:
        lines += ["---", f'source: "{url}"', f'imported: "{datetime.now().date()}"',
                  "tags:", "  - markitdown/url", "---", ""]
    lines.append(content)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


# ── Watcher ──────────────────────────────────────────────────────────────────

class VaultWatcher(FileSystemEventHandler):
    def __init__(self, dest_dir: Path, ai_profile_fn, log_fn):
        self._dest = dest_dir
        self._ai_profile_fn = ai_profile_fn
        self._log = log_fn
        self._seen: set[Path] = set()

    def on_created(self, event):
        if event.is_directory:
            return
        src = Path(event.src_path)
        if src.suffix.lower() not in SUPPORTED_EXT or src in self._seen:
            return
        self._seen.add(src)
        threading.Thread(target=self._run, args=(src,), daemon=True).start()

    def _run(self, src: Path):
        import time; time.sleep(0.5)  # wait for file to finish writing
        try:
            out = convert_file(src, self._dest, self._ai_profile_fn(), [])
            self._log("ok", f"✓ {src.name} → {out.name} ({out.stat().st_size // 1024 + 1} KB)")
        except Exception as e:
            self._log("err", f"✗ {src.name}: {e}")


# ── Tray ─────────────────────────────────────────────────────────────────────

def make_tray_icon(show_fn, quit_fn):
    if not TRAY_OK:
        return None
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 60, 60], radius=12, fill="#5B6FFF")
    d.text((18, 18), "M", fill="white")
    menu = pystray.Menu(
        pystray.MenuItem("Mostrar MarkBridge", show_fn, default=True),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Sair", quit_fn),
    )
    return pystray.Icon(APP_NAME, img, APP_NAME, menu)


# ── GUI ──────────────────────────────────────────────────────────────────────

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_NAME} {VERSION}")
        self.geometry("900x580")
        self.minsize(720, 480)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._log_queue: queue.Queue = queue.Queue()
        self._observer: Observer | None = None
        self._tray = None
        self._ai_var = ctk.StringVar(value="Claude")
        self._watch_var = ctk.StringVar(value="")
        self._dest_var  = ctk.StringVar(value=str(Path.home() / "Documents" / "MarkBridge" / "output"))
        self._watching = False

        self._build_ui()
        self._poll_log()

    # ── UI construction ───────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(10, weight=1)

        ctk.CTkLabel(sidebar, text=APP_NAME, font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#5B6FFF").grid(row=0, column=0, padx=20, pady=(20,4), sticky="w")
        ctk.CTkLabel(sidebar, text="Document → Markdown → AI",
                     font=ctk.CTkFont(size=10), text_color="gray").grid(row=1, column=0, padx=20, pady=(0,16), sticky="w")

        ctk.CTkLabel(sidebar, text="IA ALVO", font=ctk.CTkFont(size=10),
                     text_color="gray").grid(row=2, column=0, padx=20, pady=(8,4), sticky="w")
        for i, ai in enumerate(AI_PROFILES):
            ctk.CTkRadioButton(sidebar, text=ai, variable=self._ai_var, value=ai,
                               font=ctk.CTkFont(size=12)).grid(row=3+i, column=0, padx=20, pady=2, sticky="w")

        ctk.CTkLabel(sidebar, text="PASTA DE VIGÍA", font=ctk.CTkFont(size=10),
                     text_color="gray").grid(row=8, column=0, padx=20, pady=(16,4), sticky="w")
        ctk.CTkEntry(sidebar, textvariable=self._watch_var, placeholder_text="(opcional)",
                     font=ctk.CTkFont(size=11)).grid(row=9, column=0, padx=12, pady=2, sticky="ew")
        sidebar.grid_columnconfigure(0, weight=1)

        self._watch_btn = ctk.CTkButton(sidebar, text="Vigiar pasta", height=28,
                                        command=self._toggle_watch,
                                        font=ctk.CTkFont(size=11))
        self._watch_btn.grid(row=10, column=0, padx=12, pady=(4,2), sticky="ew")
        ctk.CTkButton(sidebar, text="Escolher pasta", height=28, fg_color="transparent",
                      command=self._browse_watch, font=ctk.CTkFont(size=11)).grid(row=11, column=0, padx=12, pady=(2,16), sticky="ew")

        # Main panel
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        main.grid_rowconfigure(2, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Output path row
        path_row = ctk.CTkFrame(main, fg_color="transparent")
        path_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        path_row.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(path_row, text="Pasta de saída:", font=ctk.CTkFont(size=12)).grid(row=0, column=0, padx=(0,8))
        ctk.CTkEntry(path_row, textvariable=self._dest_var, font=ctk.CTkFont(size=11)).grid(row=0, column=1, sticky="ew")
        ctk.CTkButton(path_row, text="…", width=36, height=28, command=self._browse_dest).grid(row=0, column=2, padx=(6,0))

        # URL row
        url_row = ctk.CTkFrame(main, fg_color="transparent")
        url_row.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        url_row.grid_columnconfigure(0, weight=1)
        self._url_var = ctk.StringVar()
        ctk.CTkEntry(url_row, textvariable=self._url_var, placeholder_text="Cola URL ou link YouTube e pressiona Enter",
                     font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(url_row, text="Converter URL", width=130, height=32,
                      command=self._convert_url).grid(row=0, column=1, padx=(8,0))

        # Drop zone
        self._dz = ctk.CTkFrame(main, height=140, fg_color="#14142A",
                                 border_color="#3D4FCC", border_width=2, corner_radius=12)
        self._dz.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self._dz.grid_propagate(False)
        self._dz.grid_rowconfigure(0, weight=1)
        self._dz.grid_columnconfigure(0, weight=1)
        dz_inner = ctk.CTkFrame(self._dz, fg_color="transparent")
        dz_inner.grid(row=0, column=0)
        ctk.CTkLabel(dz_inner, text="⬇  Arrasta ficheiros aqui",
                     font=ctk.CTkFont(size=16, weight="bold")).pack()
        ctk.CTkLabel(dz_inner, text="PDF · DOCX · PPTX · XLSX · HTML · CSV · JSON",
                     font=ctk.CTkFont(size=11), text_color="gray").pack(pady=4)
        ctk.CTkButton(dz_inner, text="Selecionar ficheiros", command=self._pick_files,
                      height=32).pack(pady=4)

        # Enable native drag-and-drop via tkdnd if available
        try:
            self.tk.call("package", "require", "tkdnd")
            self._dz.drop_target_register("DND_Files")
            self._dz.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

        # Log
        ctk.CTkLabel(main, text="Log de conversão", font=ctk.CTkFont(size=11),
                     text_color="gray").grid(row=3, column=0, sticky="w", pady=(0,4))
        self._log_box = ctk.CTkTextbox(main, font=ctk.CTkFont(family="Courier New", size=11),
                                       activate_scrollbars=True)
        self._log_box.grid(row=4, column=0, sticky="nsew")
        main.grid_rowconfigure(4, weight=1)

        # Status bar
        self._status = ctk.CTkLabel(main, text=f"MarkBridge {VERSION} · Microsoft MarkItDown",
                                     font=ctk.CTkFont(size=10), text_color="gray")
        self._status.grid(row=5, column=0, sticky="w", pady=(4,0))

        self._log("info", f"{APP_NAME} {VERSION} iniciado")
        self._log("info", f"Destino padrão: {self._dest_var.get()}")

    # ── Actions ───────────────────────────────────────────────────────────

    def _browse_watch(self):
        d = filedialog.askdirectory(title="Pasta a vigiar")
        if d:
            self._watch_var.set(d)

    def _browse_dest(self):
        d = filedialog.askdirectory(title="Pasta de saída")
        if d:
            self._dest_var.set(d)

    def _pick_files(self):
        files = filedialog.askopenfilenames(
            title="Selecionar ficheiros",
            filetypes=[("Documentos", "*.pdf *.docx *.pptx *.xlsx *.xls *.html *.htm *.csv *.json *.xml"),
                       ("Todos os ficheiros", "*.*")]
        )
        for f in files:
            self._run_convert(Path(f))

    def _on_drop(self, event):
        paths = self.tk.splitlist(event.data)
        for p in paths:
            self._run_convert(Path(p))

    def _convert_url(self):
        url = self._url_var.get().strip()
        if not url:
            return
        self._url_var.set("")
        threading.Thread(target=self._run_url_convert, args=(url,), daemon=True).start()

    def _run_convert(self, src: Path):
        threading.Thread(target=self._do_convert, args=(src,), daemon=True).start()

    def _do_convert(self, src: Path):
        dest = Path(self._dest_var.get())
        dest.mkdir(parents=True, exist_ok=True)
        try:
            out = convert_file(src, dest, self._ai_var.get(), [])
            self._log("ok", f"✓ {src.name} → {out.name} ({out.stat().st_size // 1024 + 1} KB)")
        except Exception as e:
            self._log("err", f"✗ {src.name}: {e}")

    def _run_url_convert(self, url: str):
        dest = Path(self._dest_var.get())
        dest.mkdir(parents=True, exist_ok=True)
        try:
            out = convert_url(url, dest, self._ai_var.get())
            self._log("ok", f"✓ URL → {out.name}")
        except Exception as e:
            self._log("err", f"✗ URL: {e}")

    def _toggle_watch(self):
        if self._watching:
            self._stop_watch()
        else:
            self._start_watch()

    def _start_watch(self):
        if not WATCHDOG_OK:
            messagebox.showerror(APP_NAME, "watchdog não instalado.\nRun: pip install watchdog")
            return
        watch_path = self._watch_var.get().strip()
        if not watch_path:
            watch_path = filedialog.askdirectory(title="Pasta a vigiar")
            if not watch_path:
                return
            self._watch_var.set(watch_path)
        watch_dir = Path(watch_path)
        if not watch_dir.exists():
            messagebox.showerror(APP_NAME, f"Pasta não encontrada:\n{watch_dir}")
            return
        handler = VaultWatcher(
            dest_dir=Path(self._dest_var.get()),
            ai_profile_fn=lambda: self._ai_var.get(),
            log_fn=self._log,
        )
        self._observer = Observer()
        self._observer.schedule(handler, str(watch_dir), recursive=False)
        self._observer.start()
        self._watching = True
        self._watch_btn.configure(text="Parar vigía", fg_color="#FF4560")
        self._log("acc", f"👁 A vigiar: {watch_dir}")

    def _stop_watch(self):
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None
        self._watching = False
        self._watch_btn.configure(text="Vigiar pasta", fg_color=("#3B8ED0", "#1F6AA5"))
        self._log("info", "Vigía parada.")

    # ── Log ───────────────────────────────────────────────────────────────

    def _log(self, level: str, msg: str):
        self._log_queue.put((level, msg))

    def _poll_log(self):
        while not self._log_queue.empty():
            level, msg = self._log_queue.get_nowait()
            ts = datetime.now().strftime("%H:%M:%S")
            color_map = {"ok": "#00D4AA", "err": "#FF4560", "acc": "#5B6FFF", "info": "gray"}
            color = color_map.get(level, "gray")
            self._log_box.configure(state="normal")
            self._log_box.insert("end", f"{ts}  {msg}\n")
            self._log_box.tag_add(level, f"end-2l", "end-1l")
            self._log_box.tag_config(level, foreground=color)
            self._log_box.configure(state="disabled")
            self._log_box.see("end")
        self.after(100, self._poll_log)

    # ── Lifecycle ─────────────────────────────────────────────────────────

    def _on_close(self):
        if TRAY_OK:
            self.withdraw()
            if not self._tray:
                self._tray = make_tray_icon(
                    show_fn=lambda icon, item: self.after(0, self.deiconify),
                    quit_fn=lambda icon, item: self._quit(),
                )
                threading.Thread(target=self._tray.run, daemon=True).start()
        else:
            self._quit()

    def _quit(self):
        self._stop_watch()
        if self._tray:
            self._tray.stop()
        self.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
