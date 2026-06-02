import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import config
import utils
from widgets import FlatButton, card_frame, section_title

# Chip: (bg, fg)
CHIPS = {
    "IDLE":        (config.SUNRISE_CREAM, config.FL_02),
    "CLOCKED IN":  (config.MIDNIGHT,      config.MORNING_WHITE),
    "ON LUNCH":    (config.GOLD_BG,       config.FL_01),
    "CLOCKED OUT": (config.SUNRISE_CREAM, config.FL_02),
}

# Button appearance when active: (bg, fg)
BTN_ACTIVE = {
    "punch_in":    (config.MIDNIGHT,      config.MORNING_WHITE),
    "lunch_start": (config.SUNRISE_CREAM, config.FL_01),
    "lunch_end":   (config.SUNRISE_CREAM, config.FL_01),
    "punch_out":   (config.CORAL,         config.MORNING_WHITE),
}


class TodayView(tk.Frame):
    def __init__(self, parent, backend, root):
        super().__init__(parent, bg=config.CONTENT_BG)
        self.backend = backend
        self.root    = root
        self._data   = {}
        self._btns   = {}
        self._tlbls  = {}
        self._build()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build(self):
        # Simple frame, no scrollable canvas — content fits standard window
        p = tk.Frame(self, bg=config.CONTENT_BG)
        p.pack(fill=tk.BOTH, expand=True)

        self._build_header(p)
        self._build_punch_card(p)
        self._build_adhoc_card(p)

    def _build_header(self, p):
        hdr = tk.Frame(p, bg=config.CONTENT_BG)
        hdr.pack(fill=tk.X, padx=40, pady=(32, 14))

        self._date_lbl = tk.Label(
            hdr, text="",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 19, "bold")
        )
        self._date_lbl.pack(side=tk.LEFT)

        self._badge = tk.Label(
            hdr, text="IDLE",
            bg=config.SUNRISE_CREAM, fg=config.FL_02,
            font=(config.FONT_FAMILY, 8, "bold"),
            padx=10, pady=5
        )
        self._badge.pack(side=tk.LEFT, padx=(16, 0))

    def _build_punch_card(self, p):
        inner = card_frame(p, pady=(0, 10))

        section_title(inner, "Today's Punches").pack(anchor="w", pady=(0, 14))

        # ── Punch buttons ──────────────────────────────────────────────────
        btn_row = tk.Frame(inner, bg=config.CARD_BG)
        btn_row.pack(fill=tk.X)

        specs = [
            ("punch_in",    "Clock In"),
            ("lunch_start", "Start Lunch"),
            ("lunch_end",   "End Lunch"),
            ("punch_out",   "Clock Out"),
        ]
        for key, label in specs:
            bg, fg = BTN_ACTIVE[key]
            btn = FlatButton(
                btn_row, text=label,
                bg=bg, fg=fg,
                padx=18, pady=13,
                font=(config.FONT_FAMILY, 10, "bold"),
                command=lambda k=key: self._punch(k)
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            self._btns[key] = btn

        # ── Time display boxes ─────────────────────────────────────────────
        grid = tk.Frame(inner, bg=config.CARD_BG)
        grid.pack(fill=tk.X, pady=(18, 0))

        fields = [
            ("punch_in",    "Punch In"),
            ("lunch_start", "Lunch Out"),
            ("lunch_end",   "Lunch In"),
            ("punch_out",   "Punch Out"),
        ]
        for col, (key, lbl_text) in enumerate(fields):
            cell = tk.Frame(
                grid, bg=config.SUNRISE_WHITE,
                highlightbackground="#E8E5DF", highlightthickness=1
            )
            cell.grid(row=0, column=col, padx=(0, 8), sticky="ew", ipady=10, ipadx=12)
            grid.columnconfigure(col, weight=1)

            tk.Label(
                cell, text=lbl_text,
                bg=config.SUNRISE_WHITE, fg=config.FL_03,
                font=(config.FONT_FAMILY, 8)
            ).pack(anchor="w", padx=12, pady=(10, 2))

            lbl = tk.Label(
                cell, text="--:--",
                bg=config.SUNRISE_WHITE, fg=config.FL_01,
                font=(config.FONT_FAMILY, 20, "bold")
            )
            lbl.pack(anchor="w", padx=12, pady=(0, 10))
            self._tlbls[key] = lbl

        # ── Total + comment ────────────────────────────────────────────────
        foot = tk.Frame(inner, bg=config.CARD_BG)
        foot.pack(fill=tk.X, pady=(16, 0))

        tk.Label(
            foot, text="Total today:",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 10)
        ).pack(side=tk.LEFT)

        self._total_lbl = tk.Label(
            foot, text="--",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 13, "bold")
        )
        self._total_lbl.pack(side=tk.LEFT, padx=(8, 0))

        self._comment_lbl = tk.Label(
            inner, text="",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9),
            wraplength=700, justify="left"
        )
        self._comment_lbl.pack(anchor="w", pady=(6, 0))

    def _build_adhoc_card(self, p):
        inner = card_frame(p, pady=(0, 28))

        section_title(inner, "Add Ad-hoc Hours").pack(anchor="w", pady=(0, 14))

        # Row 1: hours
        r1 = tk.Frame(inner, bg=config.CARD_BG)
        r1.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            r1, text="Hours to add:",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 10)
        ).pack(side=tk.LEFT, padx=(0, 10))

        self._adhoc_spin = ttk.Spinbox(
            r1, from_=0.25, to=24.0, increment=0.25,
            width=7, font=(config.FONT_FAMILY, 11)
        )
        self._adhoc_spin.set("0.25")
        self._adhoc_spin.pack(side=tk.LEFT)

        # Row 2: note (full-width)
        tk.Label(
            inner, text="Note / reason:",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 10)
        ).pack(anchor="w", pady=(0, 4))

        self._adhoc_note = ttk.Entry(
            inner, font=(config.FONT_FAMILY, 11)
        )
        self._adhoc_note.pack(fill=tk.X, pady=(0, 12))

        # Row 3: button + status
        r3 = tk.Frame(inner, bg=config.CARD_BG)
        r3.pack(fill=tk.X)

        FlatButton(
            r3, text="Add Hours",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=20, pady=8,
            font=(config.FONT_FAMILY, 10, "bold"),
            command=self._add_adhoc
        ).pack(side=tk.LEFT)

        self._adhoc_status = tk.Label(
            r3, text="No ad-hoc hours today",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        )
        self._adhoc_status.pack(side=tk.LEFT, padx=(14, 0))

    # ── Refresh ────────────────────────────────────────────────────────────

    def on_show(self):
        self._refresh()
        self._schedule_refresh()

    def _refresh(self):
        today = datetime.date.today()
        self._data = self.backend.read_day(today)

        self._date_lbl.configure(text=today.strftime("%A, %B %d %Y"))

        status = self._status()
        chip_bg, chip_fg = CHIPS.get(status, CHIPS["IDLE"])
        self._badge.configure(text=status, bg=chip_bg, fg=chip_fg)

        for key in ("punch_in", "lunch_start", "lunch_end", "punch_out"):
            val = self._data.get(key) or ""
            self._tlbls[key].configure(text=val if val else "--:--")

        total = self._data.get("total_hours")
        self._total_lbl.configure(
            text=utils.decimal_to_hhmm(total) if total is not None else "--"
        )

        comment = self._data.get("punch_comment") or ""
        self._comment_lbl.configure(
            text="Note: {}".format(comment) if comment else ""
        )

        ah = self._data.get("adhoc_hours")
        an = self._data.get("adhoc_note") or ""
        self._adhoc_status.configure(
            text="{} hrs ad-hoc{}".format(ah, " — " + an if an else "")
            if ah else "No ad-hoc hours today"
        )

        self._sync_btns()

    def _status(self):
        d = self._data
        if d.get("punch_out"):   return "CLOCKED OUT"
        if d.get("lunch_end"):   return "CLOCKED IN"
        if d.get("lunch_start"): return "ON LUNCH"
        if d.get("punch_in"):    return "CLOCKED IN"
        return "IDLE"

    def _sync_btns(self):
        d = self._data
        enabled = {
            "punch_in":    not d.get("punch_in"),
            "lunch_start": bool(d.get("punch_in"))    and not d.get("lunch_start"),
            "lunch_end":   bool(d.get("lunch_start")) and not d.get("lunch_end"),
            "punch_out":   bool(d.get("punch_in"))    and not d.get("punch_out"),
        }
        for key, btn in self._btns.items():
            btn.set_enabled(enabled[key])

    # ── Actions ────────────────────────────────────────────────────────────

    def _punch(self, key):
        now   = datetime.datetime.now().strftime("%H:%M")
        today = datetime.date.today()

        if key == "punch_out":
            comment = self._ask_comment()
            if comment is None:
                return
            self._data["punch_out"]     = now
            self._data["punch_comment"] = comment
        else:
            self._data[key] = now

        try:
            self.backend.write_day(today, self._data)
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return
        self._refresh()

    def _ask_comment(self):
        dlg = tk.Toplevel(self)
        dlg.title("Clock-out note")
        dlg.geometry("460x180")
        dlg.resizable(False, False)
        dlg.configure(bg=config.CONTENT_BG)
        dlg.grab_set()
        dlg.transient(self)

        result = [None]

        tk.Label(
            dlg, text="Add a note for today's punch-out (optional):",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 10), wraplength=420
        ).pack(padx=30, pady=(28, 8), anchor="w")

        entry = ttk.Entry(dlg, font=(config.FONT_FAMILY, 11))
        entry.pack(fill=tk.X, padx=30)
        entry.focus()

        btn_row = tk.Frame(dlg, bg=config.CONTENT_BG)
        btn_row.pack(pady=18)

        def save():
            result[0] = entry.get().strip()
            dlg.destroy()

        def skip():
            result[0] = ""
            dlg.destroy()

        FlatButton(
            btn_row, "Save",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=22, pady=8, command=save
        ).pack(side=tk.LEFT, padx=(0, 8))

        FlatButton(
            btn_row, "Skip",
            bg=config.SUNRISE_CREAM, fg=config.FL_01,
            padx=22, pady=8, command=skip
        ).pack(side=tk.LEFT)

        entry.bind("<Return>", lambda _: save())
        dlg.wait_window()
        return result[0]

    def _add_adhoc(self):
        try:
            hours = float(self._adhoc_spin.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid number of hours.")
            return
        if hours <= 0:
            messagebox.showerror("Invalid", "Hours must be greater than 0.")
            return

        note  = self._adhoc_note.get().strip()
        today = datetime.date.today()

        existing  = self._data.get("adhoc_hours") or 0.0
        old_note  = self._data.get("adhoc_note")  or ""

        self._data["adhoc_hours"] = round(existing + hours, 2)
        self._data["adhoc_note"]  = (
            "{};  {}".format(old_note, note) if (old_note and note) else
            note if note else old_note
        )

        try:
            self.backend.write_day(today, self._data)
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return

        self._adhoc_note.delete(0, tk.END)
        self._adhoc_spin.set("0.25")
        self._refresh()

    def _schedule_refresh(self):
        self.after(60000, self._auto_refresh)

    def _auto_refresh(self):
        self._refresh()
        self._schedule_refresh()
