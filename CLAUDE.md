# TimeCard App

Python + tkinter daily time-card tracker with Excel backend.

**Run:** `python3 main.py`
**Reset:** `pkill -f "python3 main.py"; rm -f TimeCard.xlsx; python3 main.py`

---

## Architecture

```
TimeCard App/
├── main.py             # Entry point — Tk root, geometry, ExcelBackend + App
├── app.py              # App shell — 190px Midnight sidebar, view switching via tkraise()
├── config.py           # Brand colors, font, column indices, WORK_HOURS_DAILY=8.0
├── excel_backend.py    # All openpyxl I/O — ExcelBackend class
├── utils.py            # Pure time-math (no tkinter/openpyxl)
├── widgets.py          # Shared custom widgets — FlatButton, NavItem, card_frame()
└── views/
    ├── today_view.py       # Punch buttons, session history, ad-hoc hours, live status badge
    ├── calendar_view.py    # Month grid + day detail editor with dynamic sessions list
    ├── dashboard_view.py   # 2×2 matplotlib charts (FigureCanvasTkAgg)
    └── records_view.py     # Full history Treeview, filter/search, inline edit, CSV export
```

---

## Excel Schema

One sheet per month, named `"Jun 2026"` etc. Row 1 = bold header, data from row 2.
**Multiple rows share the same date** — one row per clock-in/out session.

| Col | Field | Type | Notes |
|-----|-------|------|-------|
| A | Date | `datetime.date` | Repeated for each session of the day |
| B | Punch In | `"HH:MM"` string | |
| C | Lunch Start | `"HH:MM"` string | |
| D | Lunch End | `"HH:MM"` string | |
| E | Punch Out | `"HH:MM"` string | |
| F | Comment | string | First session row only |
| G | Ad-hoc Hrs | float | First session row only |
| H | Ad-hoc Note | string | First session row only |
| I | Total Hours | float (Python-computed) | First session row only |

Save strategy: `wb.save(path)` on every `write_day()` call — no deferred saves.
`write_day()` deletes all existing rows for the date (bottom-to-top), then inserts fresh rows at the correct chronological position.
Wrap saves in `try/except PermissionError` → show messagebox "Close the file in Excel first."

**New workbook:** `_load()` creates in-memory `openpyxl.Workbook()` without saving. The default "Sheet" is removed and replaced with the month sheet on the first `write_day()` call.

---

## Internal Day Data Format

`read_day(date)` and `write_day(date, data)` use this structure:

```python
{
    "date": datetime.date,
    "sessions": [
        {
            "punch_in":    "09:00",   # HH:MM or ""
            "lunch_start": "12:00",
            "lunch_end":   "12:30",
            "punch_out":   "13:00",
        },
        {
            "punch_in":  "14:00",
            "lunch_start": "",
            "lunch_end":   "",
            "punch_out": "17:30",
        },
    ],
    "comment":      "",         # also keyed as "punch_comment" for compat
    "punch_comment": "",
    "adhoc_hours":  None,       # float | None
    "adhoc_note":   "",
    "total_hours":  7.0,        # float | None, auto-recomputed on write
    # Flat convenience fields (read_day only):
    "punch_in":   "09:00",     # first session's punch_in
    "punch_out":  "17:30",     # last session's punch_out
    "lunch_start": "12:00",    # first session's lunch_start
    "lunch_end":   "12:30",    # first session's lunch_end
}
```

---

## Key Patterns

### Button rendering on macOS
`tk.Button` ignores `bg/fg` on macOS Aqua theme. **Never use `tk.Button` for styled buttons.**
Always use `FlatButton` from `widgets.py` — it's a `tk.Frame` + `tk.Label` with mouse bindings.

```python
from widgets import FlatButton
FlatButton(parent, "Label", bg=config.MIDNIGHT, fg=config.MORNING_WHITE,
           padx=20, pady=9, command=my_fn).pack(...)
```

### Ad-hoc note entry layout
The note `ttk.Entry` **must be on its own row** packed with `fill=tk.X` directly into its parent.
Never put it side-by-side with the spinbox — on macOS the entry collapses to zero width.

```python
# Row 1: spinbox
tk.Label(parent, text="Hours:").pack(side=tk.LEFT)
self._spin.pack(side=tk.LEFT)

# Row 2: note entry — own line, full width
tk.Label(parent, text="Note:").pack(anchor="w")
self._note = ttk.Entry(parent)
self._note.pack(fill=tk.X)
```

### View switching
All views are stacked via `place(relx=0, rely=0, relwidth=1, relheight=1)` and raised with `tkraise()`.
Each view implements `on_show()` which is called by `App.show_view()` on every tab switch.

### Calendar grid sizing
Grid cells **require both** `columnconfigure` and `rowconfigure` with weights, or cells won't size correctly on macOS:
```python
self._grid_frame.columnconfigure(ci, weight=1, uniform="col")
self._grid_frame.rowconfigure(ri, weight=1, minsize=52)
```

### Today view — session state machine
```
_active_session()  → last session without punch_out, or None
_all_sessions_complete() → all sessions have punch_out (and ≥1 exists)

IDLE         no sessions
CLOCKED IN   active session has punch_in, no punch_out
ON LUNCH     active session has lunch_start, no lunch_end
CLOCKED OUT  all sessions complete (Clock In Again button shown)
```
`_punch_new_session()` appends a new session dict and saves.

### Calendar view — dynamic sessions UI
`self._session_widgets` = list of dicts `{punch_in, lunch_start, lunch_end, punch_out}` → each value is a `ttk.Entry`.
`_rebuild_sessions_ui(sessions_data)` clears and recreates the container.
`_get_sessions_from_widgets()` collects current entry values into a list of dicts for saving.

---

## Genpact Brand Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `MIDNIGHT` | `#161916` | Nav bar, primary buttons, selected states |
| `MORNING_WHITE` | `#FFFFFF` | Card surfaces |
| `FL_01` | `#444744` | Primary body text |
| `FL_02` | `#6D706B` | Secondary / label text |
| `FL_03` | `#ADB1AC` | Placeholder, disabled, borders |
| `SUNRISE_WHITE` | `#FFFAF4` | App body background |
| `SUNRISE_CREAM` | `#FFF2DF` | Hover states, neutral chips |
| `CORAL` | `#FF555F` | Alerts, overtime, destructive — functional only |
| `CORAL_LIGHT` | `#FFF0F1` | Coral chip background tint |
| `GOLD` | `#FFAD28` | Fill elements only (bars, dots, borders) |
| `GOLD_BG` | `#FFF8EC` | Gold chip background tint |

**Rules:**
- Sunrise Gold (`#FFAD28`) as **text** is only permitted on Midnight backgrounds — never on light surfaces.
- Coral is functional only — never decorative.
- Status chips: dark (Midnight/white) = ok · gold chip (GOLD_BG/FL-01 text) = warning · coral = alert · muted (SUNRISE_CREAM/FL-02) = inactive.

Font: `Helvetica Neue` (macOS) / `Segoe UI` (Windows) — set in `config.FONT_FAMILY`.

---

## ExcelBackend API

```python
backend.read_day(date)           # → day dict with sessions list + flat fields
backend.write_day(date, data)    # deletes old rows, inserts session rows, saves
backend.read_month(year, month)  # → list[day dict] grouped by date
backend.read_all()               # → list[day dict] across all sheets
backend.get_months_with_data()   # → list[(year, month)] for filter dropdowns
backend.change_path(new_path)    # saves current wb to new path, reloads
```

---

## Utils API

```python
utils.parse_time(val)                        # "HH:MM" / time / None → datetime.time | None
utils.validate_hhmm(s)                       # regex check ^([01]\d|2[0-3]):[0-5]\d$
utils.compute_session_hours(pi, ls, le, po)  # datetime.time args → float | None (one session)
utils.compute_day_hours(sessions, adhoc)     # list of dicts with string times → float | None
utils.compute_hours(pi, ls, le, po, ah)      # backward-compat single-session wrapper
utils.decimal_to_hhmm(8.5)                  # → "8h 30m"
utils.sheet_name_for_date(date)             # → "Jun 2026"
utils.month_calendar_grid(y, m)             # → [[date|None]×7] × up-to-6-rows
utils.week_dates(date)                      # → [date×7] Mon–Sun of ISO week
```
