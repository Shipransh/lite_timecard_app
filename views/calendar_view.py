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
        self.backend          = backend
        self._year            = datetime.date.today().year
        self._month           = datetime.date.today().month
        self._selected        = datetime.date.today()
        self._month_data      = {}
        self._day_cells       = {}
        self._session_widgets = []   # list of dicts {punch_in, lunch_start, lunch_end, punch_out}
        self._build()

    # ── Build ───────────────────────────────────────────────────────────────

    def _build(self):
        pane = tk.PanedWindow(
            self, orient=tk.HORIZONTAL,
            bg=config.FL_03,
            sashrelief=tk.FLAT, sashwidth=5,
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

        today_btn = tk.Label(
            nav, text="Today",
            bg=config.CONTENT_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 9), cursor="hand2"
        )
        today_btn.pack(side=tk.RIGHT, padx=(0, 4))
        today_btn.bind("<Button-1>", lambda _: self._go_today())
        today_btn.bind("<Enter>", lambda e: today_btn.configure(fg=config.FL_01))
        today_btn.bind("<Leave>", lambda e: today_btn.configure(fg=config.FL_03))

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

        tk.Frame(parent, bg="#E8E5DF", height=1).pack(fill=tk.X, padx=22, pady=(0, 6))

        self._grid_frame = tk.Frame(parent, bg=config.CONTENT_BG)
        self._grid_frame.pack(fill=tk.BOTH, expand=True, padx=22, pady=(0, 16))
        for ci in range(7):
            self._grid_frame.columnconfigure(ci, weight=1, uniform="col")

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
        # has_punch: first session has a punch_in
        sessions   = data.get("sessions") or []
        has_punch  = bool(sessions and sessions[0].get("punch_in"))
        has_adhoc  = bool(data.get("adhoc_hours"))
        hours      = data.get("total_hours") or 0
        is_ot      = has_punch and hours > config.WORK_HOURS_DAILY

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

        day_lbl = tk.Label(
            inner, text=str(date.day),
            bg=cell_bg, fg=day_fg,
            font=(config.FONT_FAMILY, 11, "bold" if is_sel or is_today else "normal"),
            anchor="w"
        )
        day_lbl.pack(anchor="nw")

        if dot_clr:
            dot_row = tk.Frame(inner, bg=cell_bg)
            dot_row.pack(anchor="sw", side=tk.BOTTOM, pady=(0, 2))
            tk.Frame(dot_row, bg=dot_clr, width=6, height=6).pack(side=tk.LEFT)

        if has_punch and not is_sel and hours:
            h_str = utils.decimal_to_hhmm(hours)
            tk.Label(
                inner, text=h_str,
                bg=cell_bg, fg=day_fg,
                font=(config.FONT_FAMILY, 7),
                anchor="e"
            ).pack(anchor="se", side=tk.BOTTOM)

        for w in (cell, inner, day_lbl):
            w.bind("<Button-1>", lambda _, d=date: self._select_day(d))

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

        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(20, 0))

        # ── Punch Times section ─────────────────────────────────────────────
        self._section_hdr(p, "PUNCH TIMES", pady=(18, 10))

        # Sessions container
        self._sessions_container = tk.Frame(p, bg=config.CARD_BG)
        self._sessions_container.pack(fill=tk.X, **pad)

        # "+ Add Session" link
        add_lbl = tk.Label(
            p, text="+ Add Session",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9), cursor="hand2"
        )
        add_lbl.pack(anchor="w", **pad, pady=(6, 0))
        add_lbl.bind("<Button-1>", lambda _: self._add_session())
        add_lbl.bind("<Enter>", lambda e: add_lbl.configure(fg=config.FL_01))
        add_lbl.bind("<Leave>", lambda e: add_lbl.configure(fg=config.FL_02))

        # Comment field — full width below
        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(14, 0))

        tk.Label(
            p, text="Comment",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        ).pack(anchor="w", **pad, pady=(10, 3))

        self._comment_entry = ttk.Entry(p, font=(config.FONT_FAMILY, 11))
        self._comment_entry.pack(fill=tk.X, pady=(0, 0), **pad)

        # ── Ad-hoc section ──────────────────────────────────────────────────
        tk.Frame(p, bg="#EEEBE5", height=1).pack(fill=tk.X, padx=32, pady=(20, 0))
        self._section_hdr(p, "AD-HOC HOURS", pady=(18, 10))

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

    # ── Session widgets ─────────────────────────────────────────────────────

    def _rebuild_sessions_ui(self, sessions_data):
        """Clear sessions container and recreate rows from sessions_data list."""
        for w in self._sessions_container.winfo_children():
            w.destroy()
        self._session_widgets = []

        if not sessions_data:
            sessions_data = [{"punch_in": "", "lunch_start": "", "lunch_end": "", "punch_out": ""}]

        for idx, s in enumerate(sessions_data):
            wdict = self._add_session_row_widget(s, idx)
            self._session_widgets.append(wdict)

    def _add_session_row_widget(self, data, idx):
        """Create one session row in the sessions container. Returns dict of Entry widgets."""
        row_frame = tk.Frame(self._sessions_container, bg=config.CARD_BG)
        row_frame.pack(fill=tk.X, pady=(0, 10))

        # Session label
        tk.Label(
            row_frame,
            text="Session {}".format(idx + 1),
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 8, "bold")
        ).grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 4))

        fields_frame = tk.Frame(row_frame, bg=config.CARD_BG)
        fields_frame.grid(row=1, column=0, sticky="ew")
        row_frame.columnconfigure(0, weight=1)

        entries = {}
        field_defs = [
            ("punch_in",    "Punch In"),
            ("lunch_start", "Lunch Out"),
            ("lunch_end",   "Lunch In"),
            ("punch_out",   "Punch Out"),
        ]
        for col_idx, (key, lbl) in enumerate(field_defs):
            tk.Label(
                fields_frame, text=lbl,
                bg=config.CARD_BG, fg=config.FL_02,
                font=(config.FONT_FAMILY, 9)
            ).grid(row=0, column=col_idx * 2, sticky="w", padx=(0 if col_idx == 0 else 12, 4))

            e = ttk.Entry(fields_frame, font=(config.FONT_FAMILY, 11), width=8)
            e.insert(0, data.get(key) or "")
            e.grid(row=0, column=col_idx * 2 + 1, sticky="ew", padx=(0, 4))
            e.bind("<KeyRelease>", lambda _: self._live_total())
            entries[key] = e
            fields_frame.columnconfigure(col_idx * 2 + 1, weight=1)

        # Remove link
        remove_lbl = tk.Label(
            fields_frame, text="Remove",
            bg=config.CARD_BG, fg=config.FL_03,
            font=(config.FONT_FAMILY, 8), cursor="hand2"
        )
        remove_lbl.grid(row=0, column=8, padx=(8, 0))
        remove_lbl.bind("<Button-1>", lambda _, i=idx: self._remove_session(i))
        remove_lbl.bind("<Enter>", lambda e, w=remove_lbl: w.configure(fg=config.CORAL))
        remove_lbl.bind("<Leave>", lambda e, w=remove_lbl: w.configure(fg=config.FL_03))

        return entries

    def _add_session(self):
        """Append an empty session row."""
        current = self._get_sessions_from_widgets()
        current.append({"punch_in": "", "lunch_start": "", "lunch_end": "", "punch_out": ""})
        self._rebuild_sessions_ui(current)

    def _remove_session(self, idx):
        """Remove a session row. If only one left, clear it instead."""
        current = self._get_sessions_from_widgets()
        if len(current) <= 1:
            # Clear the single session instead of removing
            self._rebuild_sessions_ui([{"punch_in": "", "lunch_start": "", "lunch_end": "", "punch_out": ""}])
        else:
            current.pop(idx)
            self._rebuild_sessions_ui(current)
        self._live_total()

    def _get_sessions_from_widgets(self):
        """Collect current widget values into a list of session dicts."""
        result = []
        for wdict in self._session_widgets:
            result.append({
                "punch_in":    wdict["punch_in"].get().strip(),
                "lunch_start": wdict["lunch_start"].get().strip(),
                "lunch_end":   wdict["lunch_end"].get().strip(),
                "punch_out":   wdict["punch_out"].get().strip(),
            })
        return result

    # ── Select / refresh day ─────────────────────────────────────────────────

    def _select_day(self, date):
        self._selected = date
        data = self.backend.read_day(date)

        dow  = date.strftime("%A").upper()
        full = date.strftime("%B %d, %Y")
        self._detail_dow.configure(text=dow)
        self._detail_date.configure(text=full)

        # Rebuild sessions UI
        sessions = data.get("sessions") or []
        self._rebuild_sessions_ui(sessions)

        # Comment
        self._comment_entry.delete(0, tk.END)
        self._comment_entry.insert(0, data.get("punch_comment") or data.get("comment") or "")

        # Ad-hoc
        ah = data.get("adhoc_hours")
        self._ah_spin.set(str(ah) if ah else "0.0")
        self._ah_note.delete(0, tk.END)
        self._ah_note.insert(0, data.get("adhoc_note") or "")

        self._live_total()
        self._rebuild_grid()

    def _live_total(self):
        sessions = self._get_sessions_from_widgets()
        try:
            ah = float(self._ah_spin.get())
            ah = ah if ah > 0 else None
        except ValueError:
            ah = None
        total = utils.compute_day_hours(sessions, ah)
        self._live_total_lbl.configure(
            text=utils.decimal_to_hhmm(total) if total is not None else "--"
        )

    # ── Save / Clear ────────────────────────────────────────────────────────

    def _validate_times(self):
        for idx, wdict in enumerate(self._session_widgets):
            for key, entry in wdict.items():
                val = entry.get().strip()
                if val and not utils.validate_hhmm(val):
                    messagebox.showerror(
                        "Invalid time",
                        "Session {}: '{}' is not a valid time for {}. Use HH:MM.".format(
                            idx + 1, val, key.replace("_", " ").title()
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

        # Filter out completely empty sessions
        sessions = [
            s for s in self._get_sessions_from_widgets()
            if any(s.get(k) for k in ("punch_in", "lunch_start", "lunch_end", "punch_out"))
        ]

        data = {
            "sessions":      sessions,
            "punch_comment": self._comment_entry.get().strip(),
            "comment":       self._comment_entry.get().strip(),
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
                "sessions": [],
                "punch_comment": "",
                "comment": "",
                "adhoc_hours": None,
                "adhoc_note": "",
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
