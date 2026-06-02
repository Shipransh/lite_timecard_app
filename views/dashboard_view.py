import tkinter as tk
from tkinter import ttk
import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import config
import utils

# Chart palette — Genpact brand safe
C_MIDNIGHT   = "#161916"
C_CORAL      = "#FF555F"
C_GOLD       = "#FFAD28"
C_FL01       = "#444744"
C_FL02       = "#6D706B"
C_FL03       = "#ADB1AC"
C_CREAM      = "#FFF2DF"
C_GOLD_BG    = "#FFF8EC"
C_BAR_NORMAL = "#444744"   # FL-01 — neutral bar (worked, under target)
C_BAR_OT     = "#FF555F"   # Coral — overtime (functional alert)
C_BAR_EMPTY  = "#E8E6E0"   # muted for zero/no-data
C_LUNCH      = "#FFAD28"   # Gold fill for lunch block
C_WORK       = "#444744"   # FL-01 for work blocks


def _style_ax(ax, title):
    ax.set_title(title, fontsize=10, fontweight="bold", pad=8,
                 color=C_FL01, loc="left")
    ax.tick_params(labelsize=7.5, colors=C_FL02)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(C_FL03)
    ax.set_facecolor("#FDFCFA")


class DashboardView(tk.Frame):
    def __init__(self, parent, backend):
        super().__init__(parent, bg=config.CONTENT_BG)
        self.backend = backend
        self._week_start = None
        self._figs = {}
        self._axes = {}
        self._canvases = {}
        self._build()

    # ── Build ──────────────────────────────────────────────────────────────

    def _build(self):
        # Controls bar
        ctrl = tk.Frame(self, bg=config.CONTENT_BG)
        ctrl.pack(fill=tk.X, padx=20, pady=(18, 10))

        tk.Label(
            ctrl, text="Dashboard",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 16, "bold")
        ).pack(side=tk.LEFT)

        week_ctrl = tk.Frame(ctrl, bg=config.CONTENT_BG)
        week_ctrl.pack(side=tk.RIGHT)

        tk.Button(
            week_ctrl, text="◀ Prev",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 9), relief=tk.FLAT, cursor="hand2",
            command=self._prev_week
        ).pack(side=tk.LEFT, padx=4)

        self._week_lbl = tk.Label(
            week_ctrl, text="",
            bg=config.CONTENT_BG, fg=config.FL_02,
            font=(config.FONT_FAMILY, 9)
        )
        self._week_lbl.pack(side=tk.LEFT, padx=10)

        tk.Button(
            week_ctrl, text="Next ▶",
            bg=config.CONTENT_BG, fg=config.FL_01,
            font=(config.FONT_FAMILY, 9), relief=tk.FLAT, cursor="hand2",
            command=self._next_week
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            week_ctrl, text="This Week",
            bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
            font=(config.FONT_FAMILY, 9, "bold"),
            relief=tk.FLAT, padx=12, pady=4,
            cursor="hand2", command=self._this_week
        ).pack(side=tk.LEFT, padx=(12, 0))

        # 2 × 2 chart grid
        grid = tk.Frame(self, bg=config.CONTENT_BG)
        grid.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)

        for key, row, col in [
            ("weekly_hours", 0, 0),
            ("timeline",     0, 1),
            ("heatmap",      1, 0),
            ("trends",       1, 1),
        ]:
            frame = tk.Frame(
                grid, bg=config.CARD_BG,
                highlightbackground=config.FL_03,
                highlightthickness=1
            )
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            fig, ax = plt.subplots(figsize=(5, 3.5), dpi=85)
            fig.patch.set_facecolor(config.CARD_BG)
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

            self._figs[key]    = fig
            self._axes[key]    = ax
            self._canvases[key]= canvas

    # ── Navigation ─────────────────────────────────────────────────────────

    def on_show(self):
        if self._week_start is None:
            self._this_week()
        else:
            self._refresh()

    def _this_week(self):
        today = datetime.date.today()
        self._week_start = today - datetime.timedelta(days=today.weekday())
        self._refresh()

    def _prev_week(self):
        if self._week_start is None:
            self._this_week(); return
        self._week_start -= datetime.timedelta(weeks=1)
        self._refresh()

    def _next_week(self):
        if self._week_start is None:
            self._this_week(); return
        self._week_start += datetime.timedelta(weeks=1)
        self._refresh()

    # ── Refresh ────────────────────────────────────────────────────────────

    def _refresh(self):
        week = [self._week_start + datetime.timedelta(days=i) for i in range(7)]
        self._week_lbl.configure(
            text="{} – {}".format(
                week[0].strftime("%b %d"), week[6].strftime("%b %d, %Y")
            )
        )
        week_data = [self.backend.read_day(d) for d in week]
        self._draw_weekly_hours(week, week_data)
        self._draw_timeline(week, week_data)
        self._draw_heatmap()
        self._draw_trends()

    # ── Chart 1: Weekly Hours ──────────────────────────────────────────────

    def _draw_weekly_hours(self, week, week_data):
        ax = self._axes["weekly_hours"]
        ax.clear()

        labels = [d.strftime("%a\n%m/%d") for d in week]
        hours  = [r.get("total_hours") or 0.0 for r in week_data]
        colors = [
            C_BAR_OT if h > config.WORK_HOURS_DAILY else
            C_BAR_NORMAL if h > 0 else C_BAR_EMPTY
            for h in hours
        ]

        bars = ax.bar(labels, hours, color=colors, width=0.55, zorder=2)
        ax.axhline(
            y=config.WORK_HOURS_DAILY,
            color=C_FL03, linestyle="--", linewidth=1, zorder=1
        )
        ax.set_ylim(0, max(12, max(hours) + 1.5) if any(h > 0 for h in hours) else 12)
        ax.set_ylabel("Hours", fontsize=8, color=C_FL02)
        ax.grid(axis="y", alpha=0.25, zorder=0, color=C_FL03)
        _style_ax(ax, "Weekly Hours")

        for bar, h in zip(bars, hours):
            if h > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.1,
                    utils.decimal_to_hhmm(h),
                    ha="center", va="bottom", fontsize=6.5, color=C_FL01
                )

        self._figs["weekly_hours"].tight_layout()
        self._canvases["weekly_hours"].draw()

    # ── Chart 2: Daily Timeline ────────────────────────────────────────────

    def _draw_timeline(self, week, week_data):
        ax = self._axes["timeline"]
        ax.clear()

        has_any = False
        for i, row in enumerate(week_data):
            sessions = row.get("sessions") or []
            if sessions:
                has_any = True
            for s in sessions:
                pi = utils.hhmm_to_decimal(s.get("punch_in", ""))
                ls = utils.hhmm_to_decimal(s.get("lunch_start", ""))
                le = utils.hhmm_to_decimal(s.get("lunch_end", ""))
                po = utils.hhmm_to_decimal(s.get("punch_out", ""))
                if pi is None or po is None:
                    continue
                if ls is not None and le is not None:
                    ax.barh(i, ls - pi, left=pi, color=C_WORK, height=0.45, alpha=0.9)
                    ax.barh(i, le - ls, left=ls, color=C_GOLD, height=0.45, alpha=0.85)
                    ax.barh(i, po - le, left=le, color=C_WORK, height=0.45, alpha=0.9)
                else:
                    ax.barh(i, po - pi, left=pi, color=C_WORK, height=0.45, alpha=0.9)

        ax.set_yticks(list(range(7)))
        ax.set_yticklabels([d.strftime("%a") for d in week], fontsize=8)
        ax.set_xlabel("Hour of day", fontsize=7.5, color=C_FL02)
        ax.set_xlim(6, 22)
        ax.set_xticks(list(range(7, 22, 2)))
        ax.set_xticklabels(["{}:00".format(h) for h in range(7, 22, 2)], fontsize=6.5)

        if not has_any:
            ax.text(
                0.5, 0.5, "No data this week",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=9, color=C_FL03
            )

        _style_ax(ax, "Daily Timeline")
        self._figs["timeline"].tight_layout()
        self._canvases["timeline"].draw()

    # ── Chart 3: Monthly Heatmap ───────────────────────────────────────────

    def _draw_heatmap(self):
        ax = self._axes["heatmap"]
        ax.clear()

        today = datetime.date.today()
        rows  = self.backend.read_month(today.year, today.month)
        data_map = {
            r["date"].isoformat(): (r.get("total_hours") or 0.0)
            for r in rows if r.get("date")
        }

        grid = utils.month_calendar_grid(today.year, today.month)

        for ri, week in enumerate(grid):
            for ci, date in enumerate(week):
                if date is None:
                    continue
                key    = date.isoformat()
                in_map = key in data_map
                h      = data_map.get(key, 0.0)

                if not in_map:
                    color = "#F0EDE8"         # empty day — warm neutral
                elif h > config.WORK_HOURS_DAILY:
                    color = config.CORAL_LIGHT  # overtime — coral tint
                elif h >= 6:
                    color = "#E8F5EE"           # good day — muted green
                elif h > 0:
                    color = config.GOLD_BG      # short day — gold tint
                else:
                    color = "#F0EDE8"           # logged but 0h

                rect = plt.Rectangle(
                    [ci, 5 - ri], 1, 1,
                    color=color, ec=config.MORNING_WHITE, lw=2
                )
                ax.add_patch(rect)

                txt_color = (
                    config.CORAL   if (in_map and h > config.WORK_HOURS_DAILY) else
                    config.FL_03   if not in_map else
                    config.FL_01
                )
                ax.text(
                    ci + 0.5, 5 - ri + 0.5, str(date.day),
                    ha="center", va="center", fontsize=8, color=txt_color
                )

        ax.set_xlim(0, 7)
        ax.set_ylim(0, 6)
        ax.set_xticks([i + 0.5 for i in range(7)])
        ax.set_xticklabels(["M", "T", "W", "T", "F", "S", "S"], fontsize=8)
        ax.set_yticks([])
        ax.spines[:].set_visible(False)
        ax.tick_params(length=0, colors=C_FL02)
        _style_ax(ax, datetime.date(today.year, today.month, 1).strftime("%B %Y"))
        self._figs["heatmap"].tight_layout()
        self._canvases["heatmap"].draw()

    # ── Chart 4: 90-Day Trends ─────────────────────────────────────────────

    def _draw_trends(self):
        ax = self._axes["trends"]
        ax.clear()

        all_data = self.backend.read_all()
        today    = datetime.date.today()
        cutoff   = today - datetime.timedelta(days=90)

        filtered = sorted(
            [r for r in all_data
             if r.get("date") and r["date"] >= cutoff
             and r.get("total_hours") is not None],
            key=lambda r: r["date"]
        )

        if not filtered:
            ax.text(
                0.5, 0.5, "No data in the last 90 days",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=9, color=C_FL03
            )
            _style_ax(ax, "90-Day Trends")
            self._figs["trends"].tight_layout()
            self._canvases["trends"].draw()
            return

        dates     = [r["date"] for r in filtered]
        hours     = [r["total_hours"] for r in filtered]
        hours_arr = np.array(hours, dtype=float)

        # Raw dots
        ax.scatter(dates, hours, color=C_FL03, s=18, zorder=2, alpha=0.7)

        # Rolling average
        window = min(5, len(hours_arr))
        if len(hours_arr) >= window:
            rolling       = np.convolve(hours_arr, np.ones(window) / window, mode="valid")
            rolling_dates = dates[window - 1:]
            ax.plot(
                rolling_dates, rolling,
                color=C_MIDNIGHT, linewidth=2, zorder=3,
                label="{}-day avg".format(window)
            )

        ax.axhline(
            y=config.WORK_HOURS_DAILY,
            color=C_CORAL, linestyle="--", linewidth=1, alpha=0.6
        )

        ax.set_ylabel("Hours", fontsize=8, color=C_FL02)
        ax.grid(alpha=0.15, color=C_FL03)
        _style_ax(ax, "90-Day Trends")

        # Stats as xlabel — use first session's punch_in and last session's punch_out
        start_vals = []
        end_vals   = []
        for r in filtered:
            sessions = r.get("sessions") or []
            if sessions:
                first_pi = sessions[0].get("punch_in", "")
                last_po  = sessions[-1].get("punch_out", "")
            else:
                first_pi = r.get("punch_in", "")
                last_po  = r.get("punch_out", "")
            v = utils.hhmm_to_decimal(first_pi)
            if v is not None:
                start_vals.append(v)
            v = utils.hhmm_to_decimal(last_po)
            if v is not None:
                end_vals.append(v)
        ot_days    = sum(1 for h in hours if h > config.WORK_HOURS_DAILY)
        avg_hrs    = sum(hours) / len(hours) if hours else 0

        def dec_to_hm(vals):
            if not vals: return "--"
            avg = sum(vals) / len(vals)
            return "{:02d}:{:02d}".format(int(avg), int((avg % 1) * 60))

        ax.set_xlabel(
            "Avg start: {}   Avg end: {}   OT days: {}   Avg daily: {}".format(
                dec_to_hm(start_vals), dec_to_hm(end_vals),
                ot_days, utils.decimal_to_hhmm(avg_hrs)
            ),
            fontsize=6.5, color=C_FL02, labelpad=6
        )

        self._figs["trends"].tight_layout()
        self._canvases["trends"].draw()
