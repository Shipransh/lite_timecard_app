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
    ├── today_view.py       # Punch buttons, ad-hoc hours, live status badge
    ├── calendar_view.py    # Month grid + day detail editor
    ├── dashboard_view.py   # 2×2 matplotlib charts (FigureCanvasTkAgg)
    └── records_view.py     # Full history Treeview, filter/search, inline edit, CSV export
```

---

## Excel Schema

One sheet per month, named `"Jun 2026"` etc. Row 1 = bold header, data from row 2.

| Col | Field | Type |
|-----|-------|------|
| A | Date | `datetime.date` |
| B | Punch In | `"HH:MM"` string |
| C | Lunch Start | `"HH:MM"` string |
| D | Lunch End | `"HH:MM"` string |
| E | Punch Out | `"HH:MM"` string |
| F | Comment | string |
| G | Ad-hoc Hrs | float |
| H | Ad-hoc Note | string |
| I | Total Hours | float (Python-computed, not a formula) |

Save strategy: `wb.save(path)` on every `write_day()` call — no deferred saves.
Wrap saves in `try/except PermissionError` → show messagebox "Close the file in Excel first."

**New workbook:** `_load()` creates in-memory `openpyxl.Workbook()` without saving. The default "Sheet" is removed and replaced with the month sheet on the first `write_day()` call.

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
# Correct pattern (from today_view.py / calendar_view.py)
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
backend.read_day(date)           # → dict with all 8 fields; empty strings / None if no data
backend.write_day(date, data)    # writes all fields, recomputes total_hours, saves immediately
backend.read_month(year, month)  # → list[dict] for the month sheet
backend.read_all()               # → list[dict] across all sheets (for Records + Dashboard)
backend.get_months_with_data()   # → list[(year, month)] for filter dropdowns
backend.change_path(new_path)    # saves current wb to new path, reloads
```

---

## Utils API

```python
utils.parse_time(val)              # "HH:MM" str / time / None → datetime.time | None
utils.validate_hhmm(s)            # regex check ^([01]\d|2[0-3]):[0-5]\d$
utils.compute_hours(pi, ls, le, po, ah)  # → float | None
utils.decimal_to_hhmm(8.5)        # → "8h 30m"
utils.sheet_name_for_date(date)   # → "Jun 2026"
utils.month_calendar_grid(y, m)   # → [[date|None]×7] × up-to-6-rows
utils.week_dates(date)            # → [date×7] Mon–Sun of ISO week
```
