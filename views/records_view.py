import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import datetime
import csv

import config
import utils
from widgets import FlatButton, section_title

COLUMNS = [
    ("date",          "Date",        100),
    ("punch_in",      "In",           70),
    ("lunch_start",   "Lunch Out",    85),
    ("lunch_end",     "Lunch In",     80),
    ("punch_out",     "Out",          70),
    ("punch_comment", "Comment",     160),
    ("adhoc_hours",   "Ad-hoc",       70),
    ("adhoc_note",    "Ad-hoc Note", 160),
    ("total_hours",   "Total",        75),
]


class RecordsView(tk.Frame):
    def __init__(self, parent, backend):
        super().__init__(parent, bg=config.CONTENT_BG)
        self.backend    = backend
        self._all_data  = []
        self._filtered  = []
        self._sort_col  = "date"
        self._sort_rev  = True
        self._edit_date = None
        self._build()

    # ── Build ──────────────────────────────────────────────────────────────

    def _build(self):
        self._build_bar()
        self._build_tree()
        self._build_edit_panel()

    def _build_bar(self):
        bar = tk.Frame(self, bg=config.CONTENT_BG, pady=16)
        bar.pack(fill=tk.X, padx=20)

        tk.Label(
            bar, text="Records",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 16, "bold")
        ).pack(side=tk.LEFT, padx=(0, 24))

        tk.Label(
            bar, text="Month:",
            bg=config.CONTENT_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 10)
        ).pack(side=tk.LEFT, padx=(0, 6))

        self._month_var   = tk.StringVar(value="All months")
        self._month_combo = ttk.Combobox(
            bar, textvariable=self._month_var,
            width=13, font=(config.FONT_FAMILY, 10), state="readonly"
        )
        self._month_combo.pack(side=tk.LEFT, padx=(0, 14))
        self._month_combo.bind("<<ComboboxSelected>>", lambda _: self._apply())

        tk.Label(
            bar, text="Search:",
            bg=config.CONTENT_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 10)
        ).pack(side=tk.LEFT, padx=(0, 6))

        self._search_var = tk.StringVar()
        se = ttk.Entry(bar, textvariable=self._search_var,
                       width=18, font=(config.FONT_FAMILY, 10))
        se.pack(side=tk.LEFT, padx=(0, 8))
        se.bind("<Return>", lambda _: self._apply())

        FlatButton(
            bar, "Search",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=14, pady=5,
            font=(config.FONT_FAMILY, 9, "bold"),
            command=self._apply
        ).pack(side=tk.LEFT, padx=(0, 8))

        FlatButton(
            bar, "Export CSV",
            bg=config.SUNRISE_CREAM, fg=config.FL_01,
            padx=14, pady=5,
            font=(config.FONT_FAMILY, 9),
            command=self._export_csv
        ).pack(side=tk.LEFT)

        self._count_lbl = tk.Label(
            bar, text="",
            bg=config.CONTENT_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        )
        self._count_lbl.pack(side=tk.RIGHT)

    def _build_tree(self):
        frm = tk.Frame(self, bg=config.CONTENT_BG)
        frm.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 4))

        cols = [c[0] for c in COLUMNS]
        self._tree = ttk.Treeview(
            frm, columns=cols, show="headings", selectmode="browse"
        )
        for col_id, col_lbl, col_w in COLUMNS:
            self._tree.heading(
                col_id, text=col_lbl,
                command=lambda c=col_id: self._sort_by(c)
            )
            self._tree.column(col_id, width=col_w, minwidth=55)

        ys = ttk.Scrollbar(frm, orient="vertical",   command=self._tree.yview)
        xs = ttk.Scrollbar(frm, orient="horizontal",  command=self._tree.xview)
        self._tree.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
        ys.pack(side=tk.RIGHT,  fill=tk.Y)
        xs.pack(side=tk.BOTTOM, fill=tk.X)
        self._tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview",
                        rowheight=27,
                        font=(config.FONT_FAMILY, 9),
                        background=config.MORNING_WHITE,
                        fieldbackground=config.MORNING_WHITE)
        style.configure("Treeview.Heading",
                        font=(config.FONT_FAMILY, 9, "bold"))
        self._tree.tag_configure("odd",  background=config.MORNING_WHITE)
        self._tree.tag_configure("even", background=config.SUNRISE_WHITE)
        self._tree.tag_configure("ot",   background=config.CORAL_LIGHT,
                                          foreground=config.CORAL)

        self._tree.bind("<Double-1>", self._dbl_click)

        tk.Label(
            self, text="Double-click a row to edit",
            bg=config.CONTENT_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 8)
        ).pack(anchor="e", padx=20, pady=(0, 2))

    def _build_edit_panel(self):
        self._edit_frame = tk.Frame(
            self, bg=config.CARD_BG,
            highlightbackground="#CCCDC9", highlightthickness=1
        )

        inner = tk.Frame(self._edit_frame, bg=config.CARD_BG, padx=26, pady=18)
        inner.pack(fill=tk.BOTH, expand=True)

        hdr = tk.Frame(inner, bg=config.CARD_BG)
        hdr.pack(fill=tk.X, pady=(0, 12))

        self._edit_title = tk.Label(
            hdr, text="Edit Record",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 12, "bold")
        )
        self._edit_title.pack(side=tk.LEFT)

        close_lbl = tk.Label(
            hdr, text="✕",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 12), cursor="hand2"
        )
        close_lbl.pack(side=tk.RIGHT)
        close_lbl.bind("<Button-1>", lambda _: self._hide_edit())

        # Time fields — 3-up row
        form = tk.Frame(inner, bg=config.CARD_BG)
        form.pack(fill=tk.X)

        self._edit_fields = {}
        for i, (key, lbl) in enumerate([
            ("punch_in",      "Punch In"),
            ("lunch_start",   "Lunch Start"),
            ("lunch_end",     "Lunch End"),
            ("punch_out",     "Punch Out"),
            ("punch_comment", "Comment"),
        ]):
            col = (i % 3) * 2
            row = i // 3
            tk.Label(
                form, text=lbl + ":",
                bg=config.CARD_BG, fg=config.FL_02,
                font=(config.FONT_FAMILY, 9)
            ).grid(row=row, column=col, sticky="w", padx=(0, 6), pady=5)

            e = ttk.Entry(form, font=(config.FONT_FAMILY, 10), width=20)
            e.grid(row=row, column=col + 1, sticky="ew", padx=(0, 20), pady=5)
            form.columnconfigure(col + 1, weight=1)
            self._edit_fields[key] = e

        # Ad-hoc
        ah_row = tk.Frame(inner, bg=config.CARD_BG)
        ah_row.pack(fill=tk.X, pady=(8, 0))

        tk.Label(
            ah_row, text="Ad-hoc Hrs:",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(side=tk.LEFT, padx=(0, 6))

        self._edit_ah_spin = ttk.Spinbox(
            ah_row, from_=0.0, to=24.0, increment=0.25,
            width=8, font=(config.FONT_FAMILY, 10)
        )
        self._edit_ah_spin.set("0.0")
        self._edit_ah_spin.pack(side=tk.LEFT, padx=(0, 18))

        tk.Label(
            ah_row, text="Note:",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(side=tk.LEFT, padx=(0, 6))

        self._edit_ah_note = ttk.Entry(ah_row, font=(config.FONT_FAMILY, 10))
        self._edit_ah_note.pack(side=tk.LEFT, expand=True, fill=tk.X)

        btn_row = tk.Frame(inner, bg=config.CARD_BG)
        btn_row.pack(fill=tk.X, pady=(14, 0))

        FlatButton(
            btn_row, "Save Changes",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=18, pady=7, command=self._save_edit
        ).pack(side=tk.LEFT, padx=(0, 8))

        FlatButton(
            btn_row, "Cancel",
            bg=config.SUNRISE_CREAM, fg=config.FL_01,
            padx=18, pady=7, command=self._hide_edit
        ).pack(side=tk.LEFT)

    # ── Data ────────────────────────────────────────────────────────────────

    def _reload(self):
        self._all_data = self.backend.read_all()
        months  = self.backend.get_months_with_data()
        options = ["All months"] + [
            datetime.date(y, m, 1).strftime("%b %Y")
            for y, m in sorted(months)
        ]
        self._month_combo["values"] = options
        if self._month_var.get() not in options:
            self._month_var.set("All months")
        self._apply()

    def _apply(self):
        sel    = self._month_var.get()
        search = self._search_var.get().lower().strip()
        data   = self._all_data

        if sel != "All months":
            try:
                sd   = datetime.datetime.strptime(sel, "%b %Y")
                data = [r for r in data if r["date"] and
                        r["date"].year == sd.year and r["date"].month == sd.month]
            except ValueError:
                pass

        if search:
            data = [r for r in data if any(
                search in str(v).lower()
                for v in [r.get("date"), r.get("punch_in"), r.get("punch_out"),
                          r.get("punch_comment"), r.get("adhoc_note"), r.get("total_hours")]
            )]

        self._filtered = data
        self._filtered.sort(
            key=lambda r: str(r.get(self._sort_col) or ""),
            reverse=self._sort_rev
        )
        self._fill_tree()

    def _sort_by(self, col):
        self._sort_rev = not self._sort_rev if self._sort_col == col else False
        self._sort_col = col
        self._apply()

    def _fill_tree(self):
        for item in self._tree.get_children():
            self._tree.delete(item)

        for i, r in enumerate(self._filtered):
            ot  = (r.get("total_hours") or 0) > config.WORK_HOURS_DAILY
            tag = "ot" if ot else ("even" if i % 2 == 0 else "odd")
            total = r.get("total_hours")
            self._tree.insert("", "end", tags=(tag,), values=(
                r["date"].isoformat() if r.get("date") else "",
                r.get("punch_in")      or "",
                r.get("lunch_start")   or "",
                r.get("lunch_end")     or "",
                r.get("punch_out")     or "",
                r.get("punch_comment") or "",
                str(r.get("adhoc_hours") or ""),
                r.get("adhoc_note")    or "",
                utils.decimal_to_hhmm(total) if total is not None else "",
            ))

        self._count_lbl.configure(text="{} records".format(len(self._filtered)))

    # ── Edit ────────────────────────────────────────────────────────────────

    def _dbl_click(self, _):
        item = self._tree.focus()
        if not item:
            return
        values = self._tree.item(item)["values"]
        if not values:
            return
        try:
            date = datetime.date.fromisoformat(str(values[0]))
        except ValueError:
            return

        self._edit_date = date
        data = self.backend.read_day(date)
        self._edit_title.configure(text="Edit: {}".format(date.strftime("%A, %B %d %Y")))

        for key, e in self._edit_fields.items():
            e.delete(0, tk.END)
            e.insert(0, data.get(key) or "")

        ah = data.get("adhoc_hours")
        self._edit_ah_spin.set(str(ah) if ah else "0.0")
        self._edit_ah_note.delete(0, tk.END)
        self._edit_ah_note.insert(0, data.get("adhoc_note") or "")

        self._edit_frame.pack(fill=tk.X, padx=20, pady=(0, 12))

    def _hide_edit(self):
        self._edit_frame.pack_forget()
        self._edit_date = None

    def _save_edit(self):
        if self._edit_date is None:
            return
        for key in ("punch_in", "lunch_start", "lunch_end", "punch_out"):
            val = self._edit_fields[key].get().strip()
            if val and not utils.validate_hhmm(val):
                messagebox.showerror(
                    "Invalid time",
                    "'{}' is not valid for {}. Use HH:MM.".format(
                        val, key.replace("_", " ").title()
                    )
                )
                return

        try:
            ah = float(self._edit_ah_spin.get())
            ah = ah if ah > 0 else None
        except ValueError:
            ah = None

        try:
            self.backend.write_day(self._edit_date, {
                "punch_in":      self._edit_fields["punch_in"].get().strip(),
                "lunch_start":   self._edit_fields["lunch_start"].get().strip(),
                "lunch_end":     self._edit_fields["lunch_end"].get().strip(),
                "punch_out":     self._edit_fields["punch_out"].get().strip(),
                "punch_comment": self._edit_fields["punch_comment"].get().strip(),
                "adhoc_hours":   ah,
                "adhoc_note":    self._edit_ah_note.get().strip(),
            })
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return

        self._hide_edit()
        self._reload()

    # ── Export ──────────────────────────────────────────────────────────────

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Records"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([c[1] for c in COLUMNS])
                for r in self._filtered:
                    w.writerow([
                        r["date"].isoformat() if r.get("date") else "",
                        r.get("punch_in") or "", r.get("lunch_start") or "",
                        r.get("lunch_end") or "", r.get("punch_out") or "",
                        r.get("punch_comment") or "",
                        r.get("adhoc_hours") or "", r.get("adhoc_note") or "",
                        r.get("total_hours") or "",
                    ])
            messagebox.showinfo("Exported", "Saved to:\n{}".format(path))
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def on_show(self):
        self._reload()
