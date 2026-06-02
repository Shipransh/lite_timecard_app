import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import config
import utils
from widgets import FlatButton, card_frame, section_title

CHIPS = {
    "IDLE":        (config.SUNRISE_CREAM, config.FL_02),
    "CLOCKED IN":  (config.MIDNIGHT,      config.MORNING_WHITE),
    "ON LUNCH":    (config.GOLD_BG,       config.FL_01),
    "CLOCKED OUT": (config.SUNRISE_CREAM, config.FL_02),
}

BTN_COLORS = {
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
        self._session_history_frame = None
        self._active_grid_frame     = None
        self._clock_in_again_btn    = None
        self._build()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build(self):
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
        self._punch_inner = card_frame(p, pady=(0, 10))

        section_title(self._punch_inner, "Today's Punches").pack(
            anchor="w", pady=(0, 14)
        )

        # ── Session history (dynamically rebuilt) ──────────────────────────
        self._session_history_frame = tk.Frame(self._punch_inner, bg=config.CARD_BG)
        self._session_history_frame.pack(fill=tk.X, pady=(0, 8))

        # ── Active session buttons ─────────────────────────────────────────
        btn_row = tk.Frame(self._punch_inner, bg=config.CARD_BG)
        btn_row.pack(fill=tk.X)

        for key, label in [
            ("punch_in",    "Clock In"),
            ("lunch_start", "Start Lunch"),
            ("lunch_end",   "End Lunch"),
            ("punch_out",   "Clock Out"),
        ]:
            bg, fg = BTN_COLORS[key]
            btn = FlatButton(
                btn_row, text=label,
                bg=bg, fg=fg,
                padx=18, pady=13,
                font=(config.FONT_FAMILY, 10, "bold"),
                command=lambda k=key: self._punch(k)
            )
            btn.pack(side=tk.LEFT, padx=(0, 8))
            self._btns[key] = btn

        # ── Active session time boxes ──────────────────────────────────────
        self._active_grid_frame = tk.Frame(self._punch_inner, bg=config.CARD_BG)
        self._active_grid_frame.pack(fill=tk.X, pady=(18, 0))

        for col, (key, lbl_text) in enumerate([
            ("punch_in",    "Punch In"),
            ("lunch_start", "Lunch Out"),
            ("lunch_end",   "Lunch In"),
            ("punch_out",   "Punch Out"),
        ]):
            self._make_time_cell(self._active_grid_frame, key, lbl_text, col)
            self._active_grid_frame.columnconfigure(col, weight=1)

        # ── "Clock In Again" button (hidden until all sessions complete) ───
        self._clock_in_again_btn = FlatButton(
            self._punch_inner, text="Clock In Again",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            padx=18, pady=13,
            font=(config.FONT_FAMILY, 10, "bold"),
            command=self._punch_new_session
        )
        # Don't pack yet — shown/hidden in _refresh()

        # ── Total + comment ────────────────────────────────────────────────
        foot = tk.Frame(self._punch_inner, bg=config.CARD_BG)
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
            self._punch_inner, text="",
            bg=config.CARD_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9),
            wraplength=700, justify="left"
        )
        self._comment_lbl.pack(anchor="w", pady=(6, 0))

    def _make_time_cell(self, grid, key, lbl_text, col):
        cell = tk.Frame(
            grid, bg=config.SUNRISE_WHITE,
            highlightbackground="#E8E5DF", highlightthickness=1
        )
        cell.grid(row=0, column=col, padx=(0, 8), sticky="ew", ipady=10, ipadx=12)

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

    def _build_adhoc_card(self, p):
        inner = card_frame(p, pady=(0, 28))

        section_title(inner, "Add Ad-hoc Hours").pack(anchor="w", pady=(0, 14))

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

        tk.Label(
            inner, text="Note / reason:",
            bg=config.CARD_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 10)
        ).pack(anchor="w", pady=(0, 4))

        self._adhoc_note = ttk.Entry(
            inner, font=(config.FONT_FAMILY, 11)
        )
        self._adhoc_note.pack(fill=tk.X, pady=(0, 12))

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

    # ── State helpers ────────────────────────────────────────────────────────

    def _active_session(self):
        """Return the last session dict that has no punch_out, or None."""
        sessions = self._data.get("sessions") or []
        for s in reversed(sessions):
            if not s.get("punch_out"):
                return s
        return None

    def _all_sessions_complete(self):
        """True when there is at least one session and all have punch_out."""
        sessions = self._data.get("sessions") or []
        if not sessions:
            return False
        return all(bool(s.get("punch_out")) for s in sessions)

    def _status(self):
        active = self._active_session()
        if active is None and not (self._data.get("sessions") or []):
            return "IDLE"
        if active is None:
            return "CLOCKED OUT"
        if active.get("lunch_start") and not active.get("lunch_end"):
            return "ON LUNCH"
        return "CLOCKED IN"

    # ── Refresh ──────────────────────────────────────────────────────────────

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

        # Rebuild session history rows
        self._rebuild_session_history()

        # Update active session time boxes
        active = self._active_session()
        for key in ("punch_in", "lunch_start", "lunch_end", "punch_out"):
            val = active.get(key, "") if active else ""
            self._tlbls[key].configure(text=val if val else "--:--")

        # Show/hide Clock In Again
        if self._all_sessions_complete():
            self._clock_in_again_btn.pack(side=tk.LEFT, pady=(14, 0))
        else:
            self._clock_in_again_btn.pack_forget()

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

    def _rebuild_session_history(self):
        """Rebuild the compact session-history rows for completed sessions."""
        for w in self._session_history_frame.winfo_children():
            w.destroy()

        sessions = self._data.get("sessions") or []
        # Show only sessions that are fully complete (have punch_out)
        complete = [s for s in sessions if s.get("punch_in") and s.get("punch_out")]
        if not complete:
            return

        for idx, s in enumerate(complete):
            pi = s.get("punch_in", "")
            po = s.get("punch_out", "")
            # Compute duration for display
            ph = utils.compute_session_hours(
                utils.parse_time(pi),
                utils.parse_time(s.get("lunch_start")),
                utils.parse_time(s.get("lunch_end")),
                utils.parse_time(po),
            )
            dur_str = utils.decimal_to_hhmm(ph) if ph is not None else ""

            row = tk.Frame(self._session_history_frame, bg=config.CARD_BG)
            row.pack(fill=tk.X, pady=(0, 4))

            tk.Label(
                row,
                text="● Session {}".format(idx + 1),
                bg=config.CARD_BG, fg=config.FL_02,
                font=(config.FONT_FAMILY, 9, "bold")
            ).pack(side=tk.LEFT, padx=(0, 8))

            tk.Label(
                row,
                text="{} → {}".format(pi, po),
                bg=config.CARD_BG, fg=config.FL_01,
                font=(config.FONT_FAMILY, 9)
            ).pack(side=tk.LEFT)

            if dur_str:
                tk.Label(
                    row,
                    text="({})".format(dur_str),
                    bg=config.CARD_BG, fg=config.FL_03,
                    font=(config.FONT_FAMILY, 9)
                ).pack(side=tk.LEFT, padx=(6, 0))

    def _sync_btns(self):
        active   = self._active_session()
        sessions = self._data.get("sessions") or []
        no_sessions = len(sessions) == 0

        if active is None:
            # No active session — only punch_in is relevant (if no sessions at all)
            enabled = {
                "punch_in":    no_sessions,
                "lunch_start": False,
                "lunch_end":   False,
                "punch_out":   False,
            }
        else:
            has_pi = bool(active.get("punch_in"))
            has_ls = bool(active.get("lunch_start"))
            has_le = bool(active.get("lunch_end"))
            has_po = bool(active.get("punch_out"))

            enabled = {
                "punch_in":    False,  # already in active session
                "lunch_start": has_pi and not has_ls and not has_po,
                "lunch_end":   has_ls and not has_le,
                "punch_out":   has_pi and not has_po,
            }

        for key, btn in self._btns.items():
            btn.set_enabled(enabled[key])

    # ── Actions ──────────────────────────────────────────────────────────────

    def _punch(self, key):
        now   = datetime.datetime.now().strftime("%H:%M")
        today = datetime.date.today()

        sessions = self._data.get("sessions") or []

        if key == "punch_in":
            # Only allowed when no sessions exist yet
            if sessions:
                return
            new_session = {"punch_in": now, "lunch_start": "", "lunch_end": "", "punch_out": ""}
            sessions.append(new_session)
            self._data["sessions"] = sessions

        elif key == "punch_out":
            active = self._active_session()
            if active is None:
                return
            comment = self._ask_comment()
            if comment is None:
                return
            active["punch_out"] = now
            self._data["punch_comment"] = comment
            self._data["comment"]       = comment

        else:
            # lunch_start or lunch_end — set on active session
            active = self._active_session()
            if active is None:
                return
            active[key] = now

        try:
            self.backend.write_day(today, self._data)
        except PermissionError as e:
            messagebox.showerror("File Error", str(e))
            return
        self._refresh()

    def _punch_new_session(self):
        """Start a new session (Clock In Again) after all sessions are complete."""
        now   = datetime.datetime.now().strftime("%H:%M")
        today = datetime.date.today()

        sessions = self._data.get("sessions") or []
        sessions.append({"punch_in": now, "lunch_start": "", "lunch_end": "", "punch_out": ""})
        self._data["sessions"] = sessions

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

        existing = self._data.get("adhoc_hours") or 0.0
        old_note = self._data.get("adhoc_note") or ""

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
