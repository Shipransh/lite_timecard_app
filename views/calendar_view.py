import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import config
import utils
from widgets import FlatButton, section_title

DAY_HDRS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

# Cell state palette
_GREEN_BG  = "#E6F2EB"
_GREEN_FG  = "#1A6641"
_GREEN_DOT = "#27AE60"
_OT_BG     = config.CORAL_LIGHT
_OT_FG     = config.CORAL
_OT_DOT    = config.CORAL
_AH_BG     = config.GOLD_BG
_AH_FG     = config.FL_01
_AH_DOT    = config.GOLD
_WKND_BG   = "#F5F2EC"
_WKDY_BG   = "#FDFBF8"
_EMPTY_FG  = config.FL_03
_TODAY_RING = config.CORAL


class CalendarView(tk.Frame):
    def __init__(self, parent, backend):
        super().__init__(parent, bg=config.CONTENT_BG)
        self.backend     = backend
        self._year       = datetime.date.today().year
        self._month      = datetime.date.today().month
        self._selected   = datetime.date.today()
        self._month_data = {}
        self._day_cells  = {}
        self._build()

    # ── Build ───────────────────────────────────────────────────────────────

    def _build(self):
        # Outer wrapper — two resizable panes
        pane = tk.PanedWindow(
            self, orient=tk.HORIZONTAL,
            bg=config.CONTENT_BG,
            sashrelief=tk.FLAT, sashwidth=1,
            handlesize=0
        )
        pane.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        left_wrap = tk.Frame(pane, bg=config.CONTENT_BG, width=390)
        right_wrap = tk.Frame(
            pane, bg=config.CARD_BG,
            highlightbackground="#E0DDD8", highlightthickness=1
        )

        pane.add(left_wrap,  minsize=340, stretch="never")
        pane.add(right_wrap, minsize=400, stretch="always")

        self._build_cal_panel(left_wrap)
        self._build_detail_panel(right_wrap)

    # ── Calendar panel ──────────────────────────────────────────────────────

    def _build_cal_panel(self, parent):
        parent.pack_propagate(False)

        # Month navigation header
        nav = tk.Frame(parent, bg=config.CONTENT_BG)
        nav.pack(fill=tk.X, padx=22, pady=(24, 0))

        self._month_lbl = tk.Label(
            nav, text="",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 16, "bold"),
            anchor="w"
        )
        self._month_lbl.pack(side=tk.LEFT)

        arrow_frame = tk.Frame(nav, bg=config.CONTENT_BG)
        arrow_frame.pack(side=tk.RIGHT)

        for text, cmd in [("‹", self._prev_month), ("›", self._next_month)]:
            a = tk.Label(
                arrow_frame, text=text,
                bg=config.CONTENT_BG, fg=config.FL_02,
                font=(config.FONT_FAMILY, 18), cursor="hand2",
                padx=6
            )
            a.pack(side=tk.LEFT)
            a.bind("<Button-1>", lambda _, c=cmd: c())
            a.bind("<Enter>", lambda e, w=a: w.configure(fg=config.FL_01))
            a.bind("<Leave>", lambda e, w=a: w.configure(fg=config.FL_02))

        # Today button
        today_btn = tk.Label(
            nav, text="Today",
            bg=config.CONTENT_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 9), cursor="hand2"
        )
        today_btn.pack(side=tk.RIGHT, padx=(0, 4))
        today_btn.bind("<Button-1>", lambda _: self._go_today())
        today_btn.bind("<Enter>", lambda e: today_btn.configure(fg=config.FL_01))
        today_btn.bind("<Leave>", lambda e: today_btn.configure(fg=config.FL_03))

        # Day-of-week header row
        dow_frame = tk.Frame(parent, bg=config.CONTENT_BG)
        dow_frame.pack(fill=tk.X, padx=22, pady=(16, 6))
        for i, d in enumerate(DAY_HDRS):
            dow_frame.columnconfigure(i, weight=1)
            fg = config.FL_03 if i < 5 else "#C8C5BF"
            tk.Label(
                dow_frame, text=d,
                bg=config.CONTENT_BG, fg=fg,
                font=(config.FONT_FAMILY, 8, "bold"),
                anchor="center"
            ).grid(row=0, column=i, sticky="ew")

        # Thin divider
        tk.Frame(parent, bg="#E8E5DF", height=1).pack(fill=tk.X, padx=22, pady=(0, 6))

        # Grid container
        self._grid_frame = tk.Frame(parent, bg=config.CONTENT_BG)
        self._grid_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=(0, 16))
        for ci in range(7):
            self._grid_frame.columnconfigure(ci, weight=1, uniform="col")

        # Legend
        self._build_legend(parent)

    def _build_legend(self, parent):
        leg = tk.Frame(parent, bg=config.CONTENT_BG)
        leg.pack(fill=tk.X, padx=22, pady=(0, 18))

        items = [
            (_GREEN_DOT, "Normal"),
            (_OT_DOT,    "Overtime"),
            (_AH_DOT,    "Ad-hoc"),
            (_TODAY_RING,"Today"),
        ]
        for dot_color, label in items:
            row = tk.Frame(leg, bg=config.CONTENT_BG)
            row.pack(side=tk.LEFT, padx=(0, 14))
            tk.Frame(row, bg=dot_color, width=7, height=7).pack(side=tk.LEFT, pady=1)
            tk.Label(
                row, text=label,
                bg=config.CONTENT_BG, fg=config.FL_03,
                font=(config.FONT_FAMILY, 8)
            ).pack(side=tk.LEFT, padx=(4, 0))

    # ── Grid rebuild ────────────────────────────────────────────────────────

    def _rebuild_grid(self):
        for w in self._grid_frame.winfo_children():
            w.destroy()
        self._day_cells.clear()

        self._month_lbl.configure(
            text=datetime.date(self._year, self._month, 1).strftime("%B %Y")
        )
        today = datetime.date.today()
        weeks = utils.month_calendar_grid(self._year, self._month)

        for ri, week in enumerate(weeks):
            self._grid_frame.rowconfigure(ri, weight=1, minsize=52)
            for ci, date in enumerate(week):
                if date is None:
                    tk.Frame(
                        self._grid_frame,
                        bg=config.CONTENT_BG
                    ).grid(row=ri, column=ci, padx=2, pady=2, sticky="nsew")
                    continue

                self._make_cell(date, ri, ci, today)

    def _make_cell(self, date, ri, ci, today):
        data       = self._month_data.get(date.isoformat(), {})
        is_sel     = (date == self._selected)
        is_today   = (date == today)
        is_weekend = date.weekday() >= 5
        has_punch  = bool(data.get("punch_in"))
        has_adhoc  = bool(data.get("adhoc_hours"))
        hours      = data.get("total_hours") or 0
        is_ot      = has_punch and hours > config.WORK_HOURS_DAILY

        # Determine cell appearance
        if is_sel:
            cell_bg = config.MIDNIGHT
            day_fg  = config.MORNING_WHITE
            dot_clr = None
        elif is_ot:
            cell_bg = _OT_BG
            day_fg  = _OT_FG
            dot_clr = _OT_DOT
        elif has_punch:
            cell_bg = _GREEN_BG
            day_fg  = _GREEN_FG
            dot_clr = _GREEN_DOT
        elif has_adhoc:
            cell_bg = _AH_BG
            day_fg  = _AH_FG
            dot_clr = _AH_DOT
        elif is_today:
            cell_bg = config.SUNRISE_CREAM
            day_fg  = config.FL_01
            dot_clr = _TODAY_RING
        elif is_weekend:
            cell_bg = _WKND_BG
            day_fg  = _EMPTY_FG
            dot_clr = None
        else:
            cell_bg = _WKDY_BG
            day_fg  = config.FL_02
            dot_clr = None

        # Border: today ring or subtle
        if is_today and not is_sel:
            hbg, htk = _TODAY_RING, 2
        elif is_sel:
            hbg, htk = config.MIDNIGHT, 0
        else:
            hbg, htk = "#E8E5DF", 1

        cell = tk.Frame(
            self._grid_frame,
            bg=cell_bg, cursor="hand2",
            highlightbackground=hbg,
            highlightthickness=htk
        )
        cell.grid(row=ri, column=ci, padx=2, pady=2, sticky="nsew")

        inner = tk.Frame(cell, bg=cell_bg)
        inner.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Day number
        day_lbl = tk.Label(
            inner, text=str(date.day),
            bg=cell_bg, fg=day_fg,
            font=(config.FONT_FAMILY, 11, "bold" if is_sel or is_today else "normal"),
            anchor="w"
        )
        day_lbl.pack(anchor="nw")

        # Status dot
        if dot_clr:
            dot_row = tk.Frame(inner, bg=cell_bg)
            dot_row.pack(anchor="sw", side=tk.BOTTOM, pady=(0, 2))
            tk.Frame(dot_row, bg=dot_clr, width=6, height=6).pack(side=tk.LEFT)

        # Hours hint for punch days (small text)
        if has_punch and not is_sel and hours:
            h_str = utils.decimal_to_hhmm(hours)
            tk.Label(
                inner, text=h_str,
                bg=cell_bg, fg=day_fg,
                font=(config.FONT_FAMILY, 7),
                anchor="e"
            ).pack(anchor="se", side=tk.BOTTOM)

        # Bind click
        for w in (cell, inner, day_lbl):
            w.bind("<Button-1>", lambda _, d=date: self._select_day(d))

        # Hover effect (only for unselected cells)
        def on_enter(e, c=cell, orig=cell_bg):
            if date != self._selected:
                hover = _darken(orig, 0.96)
                _recolor(c, hover)

        def on_leave(e, c=cell, orig=cell_bg):
            if date != self._selected:
                _recolor(c, orig)

        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)

        self._day_cells[date] = cell

    # ── Detail panel ────────────────────────────────────────────────────────

    def _build_detail_panel(self, parent):
        scroll_canvas = tk.Canvas(parent, bg=config.CARD_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=scroll_canvas.yview)
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        inner = tk.Frame(scroll_canvas, bg=config.CARD_BG)
        win_id = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_configure(e):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        def _on_canvas_resize(e):
            scroll_canvas.itemconfig(win_id, width=e.width)

        inner.bind("<Configure>", _on_configure)
        scroll_canvas.bind("<Configure>", _on_canvas_resize)

        self._build_detail_inner(inner)

    def _build_detail_inner(self, p):
        pad = dict(padx=32)

        # ── Date header ─────────────────────────────────────────────────────
        hdr = tk.Frame(p, bg=config.CARD_BG)
        hdr.pack(fill=tk.X, pady=(28, 0), **pad)

        self._detail_dow = tk.Label(
            hdr, text="SELECT A DAY",
            bg=config.CARD_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 9, "bold")
        )
        self._detail_dow.pack(anchor="w")

        self._detail_date = tk.Label(
            hdr, text="Click any date on the calendar",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 20, "bold")
        )
        self._detail_date.pack(anchor="w", pady=(2, 0))

        # Total pill
        pill_row = tk.Frame(p, bg=config.CARD_BG)
        pill_row.pack(fill=tk.X, pady=(12, 0), **pad)

        tk.Label(
            pill_row, text="TOTAL",
            bg=config.CARD_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 8, "bold")
        ).pack(side=tk.LEFT, pady=(4, 0))

        self._live_total_lbl = tk.Label(
            pill_row, text="--",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 22, "bold")
        )
        self._live_total_lbl.pack(side=tk.LEFT, padx=(10, 0))

        # Thin divider
        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(20, 0))

        # ── Punch Times section ─────────────────────────────────────────────
        self._section_hdr(p, "PUNCH TIMES", pady=(18, 10))

        form = tk.Frame(p, bg=config.CARD_BG)
        form.pack(fill=tk.X, **pad)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self._fields = {}
        punch_fields = [
            ("punch_in",    "Punch In",    "HH:MM", 0, 0),
            ("punch_out",   "Punch Out",   "HH:MM", 0, 2),
            ("lunch_start", "Lunch Out",   "HH:MM", 1, 0),
            ("lunch_end",   "Lunch In",    "HH:MM", 1, 2),
        ]
        for key, lbl, ph, row, col in punch_fields:
            tk.Label(
                form, text=lbl,
                bg=config.CARD_BG, fg=config.FL_02,
                font=(config.FONT_FAMILY, 9)
            ).grid(row=row*2, column=col, sticky="w", pady=(0, 3), padx=(0, 8 if col == 0 else 0))

            e = ttk.Entry(form, font=(config.FONT_FAMILY, 11), width=12)
            e.grid(row=row*2+1, column=col, sticky="ew",
                   pady=(0, 14), padx=(0, 24 if col == 0 else 0))
            e.bind("<KeyRelease>", lambda _: self._live_total())
            self._fields[key] = e

        # Comment field — full width below
        tk.Label(
            p, text="Comment",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(anchor="w", **pad)

        self._fields["punch_comment"] = ttk.Entry(p, font=(config.FONT_FAMILY, 11))
        self._fields["punch_comment"].pack(fill=tk.X, pady=(4, 0), **pad)

        # ── Ad-hoc section ──────────────────────────────────────────────────
        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(20, 0))
        self._section_hdr(p, "AD-HOC HOURS", pady=(18, 10))

        # Hours row
        ah_hrs_row = tk.Frame(p, bg=config.CARD_BG)
        ah_hrs_row.pack(fill=tk.X, **pad, pady=(0, 10))

        tk.Label(
            ah_hrs_row, text="Hours:",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(side=tk.LEFT, padx=(0, 10))

        self._ah_spin = ttk.Spinbox(
            ah_hrs_row, from_=0.0, to=24.0, increment=0.25,
            width=9, font=(config.FONT_FAMILY, 11)
        )
        self._ah_spin.set("0.0")
        self._ah_spin.pack(side=tk.LEFT)
        self._ah_spin.bind("<KeyRelease>", lambda _: self._live_total())

        # Note row — full width on its own line
        tk.Label(
            p, text="Note:",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(anchor="w", **pad, pady=(0, 3))

        self._ah_note = ttk.Entry(p, font=(config.FONT_FAMILY, 11))
        self._ah_note.pack(fill=tk.X, **pad)

        # ── Buttons ─────────────────────────────────────────────────────────
        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(24, 0))

        btn_row = tk.Frame(p, bg=config.CARD_BG)
        btn_row.pack(fill=tk.X, padx=32, pady=(16, 32))

        FlatButton(
            btn_row, "Save Changes",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=22, pady=10,
            font=(config.FONT_FAMILY, 10, "bold"),
            command=self._save_day
        ).pack(side=tk.LEFT, padx=(0, 10))

        FlatButton(
            btn_row, "Clear Day",
            bg=config.CORAL_LIGHT, fg=config.CORAL,
            padx=22, pady=10,
            font=(config.FONT_FAMILY, 10),
            command=self._clear_day
        ).pack(side=tk.LEFT)

    def _section_hdr(self, parent, text, pady=(14, 8)):
        tk.Label(
            parent, text=text,
            bg=config.CARD_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 8, "bold")
        ).pack(anchor="w", padx=32, pady=pady)

    # ── Select / refresh day ────────────────────────────────────────────────

    def _select_day(self, date):
        self._selected = date
        data = self.backend.read_day(date)

        dow  = date.strftime("%A").upper()
        full = date.strftime("%B %d, %Y")
        self._detail_dow.configure(text=dow)
        self._detail_date.configure(text=full)

        for key, entry in self._fields.items():
            entry.delete(0, tk.END)
            entry.insert(0, data.get(key) or "")

        ah = data.get("adhoc_hours")
        self._ah_spin.set(str(ah) if ah else "0.0")
        self._ah_note.delete(0, tk.END)
        self._ah_note.insert(0, data.get("adhoc_note") or "")

        self._live_total()
        self._rebuild_grid()

    def _live_total(self):
        pi = utils.parse_time(self._fields["punch_in"].get())
        ls = utils.parse_time(self._fields["lunch_start"].get())
        le = utils.parse_time(self._fields["lunch_end"].get())
        po = utils.parse_time(self._fields["punch_out"].get())
        try:
            ah = float(self._ah_spin.get())
            ah = ah if ah > 0 else None
        except ValueError:
            ah = None
        total = utils.compute_hours(pi, ls, le, po, ah)
        self._live_total_lbl.configure(
            text=utils.decimal_to_hhmm(total) if total is not None else "--"
        )

    # ── Save / Clear ────────────────────────────────────────────────────────

    def _validate_times(self):
        for key in ("punch_in", "lunch_start", "lunch_end", "punch_out"):
            val = self._fields[key].get().strip()
            if val and not utils.validate_hhmm(val):
                messagebox.showerror(
                    "Invalid time",
                    "'{}' is not valid for {}. Use HH:MM.".format(
                        val, key.replace("_", " ").title()
                    )
                )
                return False
        return True

    def _save_day(self):
        if not self._validate_times():
            return
        try:
            ah = float(self._ah_spin.get())
            ah = ah if ah > 0 else None
        except ValueError:
            ah = None

        data = {
            "punch_in":      self._fields["punch_in"].get().strip(),
            "lunch_start":   self._fields["lunch_start"].get().strip(),
            "lunch_end":     self._fields["lunch_end"].get().strip(),
            "punch_out":     self._fields["punch_out"].get().strip(),
            "punch_comment": self._fields["punch_comment"].get().strip(),
            "adhoc_hours":   ah,
            "adhoc_note":    self._ah_note.get().strip(),
        }
        try:
            self.backend.write_day(self._selected, data)
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return

        self._load_month_data()
        self._rebuild_grid()
        messagebox.showinfo("Saved", "Record saved for {}.".format(
            self._selected.strftime("%B %d, %Y")
        ))

    def _clear_day(self):
        if not messagebox.askyesno(
            "Clear day",
            "Clear all data for {}?".format(self._selected.strftime("%B %d, %Y"))
        ):
            return
        try:
            self.backend.write_day(self._selected, {
                "punch_in": "", "lunch_start": "", "lunch_end": "",
                "punch_out": "", "punch_comment": "",
                "adhoc_hours": None, "adhoc_note": "",
            })
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return
        self._load_month_data()
        self._select_day(self._selected)

    # ── Month navigation ────────────────────────────────────────────────────

    def _load_month_data(self):
        rows = self.backend.read_month(self._year, self._month)
        self._month_data = {
            r["date"].isoformat(): r for r in rows if r.get("date")
        }

    def _prev_month(self):
        if self._month == 1:
            self._month, self._year = 12, self._year - 1
        else:
            self._month -= 1
        self._load_month_data()
        self._rebuild_grid()

    def _next_month(self):
        if self._month == 12:
            self._month, self._year = 1, self._year + 1
        else:
            self._month += 1
        self._load_month_data()
        self._rebuild_grid()

    def _go_today(self):
        today = datetime.date.today()
        self._year, self._month = today.year, today.month
        self._load_month_data()
        self._select_day(today)

    def on_show(self):
        today = datetime.date.today()
        self._year, self._month, self._selected = today.year, today.month, today
        self._load_month_data()
        self._rebuild_grid()
        self._select_day(today)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _darken(hex_color, f=0.96):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return "#{:02x}{:02x}{:02x}".format(
        max(0, int(r * f)), max(0, int(g * f)), max(0, int(b * f))
    )


def _recolor(widget, color):
    try:
        widget.configure(bg=color)
        for child in widget.winfo_children():
            try:
                child.configure(bg=color)
                for grandchild in child.winfo_children():
                    try:
                        grandchild.configure(bg=color)
                    except tk.TclError:
                        pass
            except tk.TclError:
                pass
    except tk.TclError:
        pass
