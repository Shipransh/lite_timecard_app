import tkinter as tk
from tkinter import filedialog, messagebox
import os

import config
from widgets import NavItem
from views.today_view    import TodayView
from views.calendar_view import CalendarView
from views.dashboard_view import DashboardView
from views.records_view  import RecordsView

NAV = [
    ("today",     "Today"),
    ("calendar",  "Calendar"),
    ("dashboard", "Dashboard"),
    ("records",   "Records"),
]


class App:
    def __init__(self, root, backend):
        self.root    = root
        self.backend = backend
        self._nav    = {}
        self._build()
        self.show_view("today")

    def _build(self):
        self.root.configure(bg=config.SIDEBAR_BG)

        # ── Sidebar ────────────────────────────────────────────────────────
        sb = tk.Frame(self.root, bg=config.SIDEBAR_BG, width=190)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack_propagate(False)

        # Brand block
        brand = tk.Frame(sb, bg=config.SIDEBAR_BG)
        brand.pack(fill=tk.X, padx=20, pady=(26, 18))

        tk.Label(
            brand, text="TimeCard",
            bg=config.SIDEBAR_BG, fg=config.MORNING_WHITE,
            font=(config.FONT_FAMILY, 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            brand, text="by Genpact",
            bg=config.SIDEBAR_BG, fg="#3D413D",
            font=(config.FONT_FAMILY, 9)
        ).pack(anchor="w")

        # Divider
        tk.Frame(sb, bg="#272B27", height=1).pack(fill=tk.X, padx=20, pady=(0, 8))

        # Nav items
        for key, label in NAV:
            item = NavItem(sb, label, command=lambda k=key: self.show_view(k))
            item.pack(fill=tk.X, padx=8, pady=2)
            self._nav[key] = item

        # ── Bottom: file path ──────────────────────────────────────────────
        tk.Frame(sb, bg="#272B27", height=1).pack(
            side=tk.BOTTOM, fill=tk.X, padx=20
        )

        bottom = tk.Frame(sb, bg=config.SIDEBAR_BG)
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=16, pady=14)

        tk.Label(
            bottom, text="Data file",
            bg=config.SIDEBAR_BG, fg="#3D413D",
            font=(config.FONT_FAMILY, 8)
        ).pack(anchor="w")

        self._path_lbl = tk.Label(
            bottom, text=os.path.basename(self.backend.path),
            bg=config.SIDEBAR_BG, fg="#555955",
            font=(config.FONT_FAMILY, 8), wraplength=160, justify="left"
        )
        self._path_lbl.pack(anchor="w")

        # Change file link
        lnk = tk.Label(
            bottom, text="Change file…",
            bg=config.SIDEBAR_BG, fg=config.CORAL,
            font=(config.FONT_FAMILY, 8), cursor="hand2"
        )
        lnk.pack(anchor="w", pady=(4, 0))
        lnk.bind("<Button-1>", lambda _: self._change_file())

        # ── Content area ───────────────────────────────────────────────────
        content = tk.Frame(self.root, bg=config.CONTENT_BG)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._views = {
            "today":     TodayView(content, self.backend, self.root),
            "calendar":  CalendarView(content, self.backend),
            "dashboard": DashboardView(content, self.backend),
            "records":   RecordsView(content, self.backend),
        }
        for v in self._views.values():
            v.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_view(self, name):
        self._current = name
        self._views[name].tkraise()
        self._views[name].on_show()
        for key, item in self._nav.items():
            item.set_active(key == name)

    def _change_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel workbook", "*.xlsx")],
            title="Choose TimeCard data file"
        )
        if not path:
            return
        try:
            self.backend.change_path(path)
            self._path_lbl.configure(text=os.path.basename(path))
            self.show_view(self._current)
        except Exception as e:
            messagebox.showerror("Error", str(e))
