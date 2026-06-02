# TimeCard

A local desktop time-card tracker built with Python + tkinter. Stores all data in a single Excel workbook (`.xlsx`) — one sheet per month, fully editable outside the app.

---

## Features

- **Clock In / Out** with optional punch-out comment
- **Lunch tracking** (Start Lunch / End Lunch)
- **Ad-hoc hours** — log extra time with a note (e.g. "1.5 hrs — evening call")
- **Calendar view** — browse any month, click any day to view or correct entries
- **Dashboard** — weekly hours bar chart, daily punch timeline, monthly heatmap, 90-day trend
- **Records table** — full history, sortable columns, month filter, text search, CSV export
- **Inline editing** — fix any past entry without leaving the app
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

| Column | Field | Format |
|--------|-------|--------|
| A | Date | date |
| B | Punch In | HH:MM |
| C | Lunch Start | HH:MM |
| D | Lunch End | HH:MM |
| E | Punch Out | HH:MM |
| F | Comment | text |
| G | Ad-hoc Hours | number |
| H | Ad-hoc Note | text |
| I | Total Hours | number (auto-computed) |

You can open and edit this file directly in Excel. Changes made externally will be visible in the app after restarting.

---

## Views

| Tab | Purpose |
|-----|---------|
| **Today** | Clock in/out, lunch, ad-hoc hours for the current day |
| **Calendar** | Browse months, click any day to view or edit that day's record |
| **Dashboard** | Charts: weekly hours, daily timeline, monthly heatmap, 90-day trend |
| **Records** | Full history table — filter by month, search, sort, export to CSV |

---

## Changing the Data File

Click **Change file…** at the bottom of the sidebar to move or rename `TimeCard.xlsx`. The current data is saved to the new location automatically.
