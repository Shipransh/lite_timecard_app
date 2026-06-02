# TimeCard

A local desktop time-card tracker built with Python + tkinter. Stores all data in a single Excel workbook (`.xlsx`) — one sheet per month, fully editable outside the app.

---

## Features

- **Multiple sessions per day** — clock in and out any number of times; each session is a separate row in Excel
- **Lunch tracking** (Start Lunch / End Lunch) within any session
- **Ad-hoc hours** — log extra time with a note (e.g. "1.5 hrs — evening call")
- **Calendar view** — browse any month, click any day to view or edit sessions
- **Dashboard** — weekly hours bar chart, daily punch timeline (all sessions), monthly heatmap, 90-day trend
- **Records table** — full history, sortable columns, month filter, text search, CSV export
- **Inline editing** — fix any past session without leaving the app
- **Excel backend** — `TimeCard.xlsx` is a plain spreadsheet you can open in Excel anytime

---

## Requirements

- Python 3.7+
- `openpyxl` — Excel read/write
- `matplotlib` — dashboard charts
- `numpy` — trend chart rolling average

Install all dependencies:

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install openpyxl matplotlib numpy
```

---

## Run

```bash
python3 main.py
```

`TimeCard.xlsx` is created in the same directory as `main.py` on first use.

**Reset (delete all data and restart):**
```bash
rm TimeCard.xlsx && python3 main.py
```

---

## Package as a standalone app

Uses [PyInstaller](https://pyinstaller.org) (included in `requirements.txt`).

```bash
pip install pyinstaller
pyinstaller --windowed --onefile --name TimeCard main.py
```

The packaged binary is written to `dist/`. On first launch, `TimeCard.xlsx` is created in the same directory as the binary.

---

## Data File

All data lives in `TimeCard.xlsx`, one sheet per month (`Jun 2026`, `Jul 2026`, …).

**Each clock-in/out session is its own row.** A day with two sessions produces two rows sharing the same date.

| Column | Field | Format | Notes |
|--------|-------|--------|-------|
| A | Date | date | Repeated for each session |
| B | Punch In | HH:MM | |
| C | Lunch Start | HH:MM | |
| D | Lunch End | HH:MM | |
| E | Punch Out | HH:MM | |
| F | Comment | text | First session row only |
| G | Ad-hoc Hours | number | First session row only |
| H | Ad-hoc Note | text | First session row only |
| I | Total Hours | number (auto-computed) | First session row only |

You can open and edit this file directly in Excel. Changes made externally will be visible in the app after restarting.

---

## Views

| Tab | Purpose |
|-----|---------|
| **Today** | Clock in/out across multiple sessions; session history shown as labelled rows; "Clock In Again" appears after clocking out |
| **Calendar** | Browse months, click any day to view or edit its sessions; add/remove sessions per day |
| **Dashboard** | Charts: weekly hours, daily timeline (all sessions), monthly heatmap, 90-day trend |
| **Records** | Full history — one row per day showing first in, last out, session count, total hours; double-click to edit sessions inline |

---

## Changing the Data File

Click **Change file…** at the bottom of the sidebar to move or rename `TimeCard.xlsx`. The current data is saved to the new location automatically.
