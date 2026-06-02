import os
import sys
import platform


def _data_dir():
    """Return the directory where user data (the Excel file) should live.

    When frozen by PyInstaller, __file__ resolves to a read-only temp dir
    inside the bundle.  Use sys.executable's directory instead so the file
    sits next to the app binary / .app bundle.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# ── Excel ──────────────────────────────────────────────────────────────────
EXCEL_PATH = os.path.join(_data_dir(), "TimeCard.xlsx")

COL_DATE         = 1
COL_PUNCH_IN     = 2
COL_LUNCH_START  = 3
COL_LUNCH_END    = 4
COL_PUNCH_OUT    = 5
COL_PUNCH_COMMENT= 6
COL_ADHOC_HRS    = 7
COL_ADHOC_NOTE   = 8
COL_TOTAL_HRS    = 9

# ── Genpact Brand Palette (v0.5) ───────────────────────────────────────────
MIDNIGHT      = "#161916"   # nav bar, primary buttons, dark chips
MORNING_WHITE = "#FFFFFF"   # card surfaces, modal backgrounds
FL_01         = "#444744"   # primary body text
FL_02         = "#6D706B"   # secondary / label text
FL_03         = "#ADB1AC"   # placeholder, disabled, borders
SUNRISE_WHITE = "#FFFAF4"   # app body background
SUNRISE_CREAM = "#FFF2DF"   # sidebar active bg, hover, warning card bg
CORAL         = "#FF555F"   # alerts / overdue — functional only, never decorative
CORAL_LIGHT   = "#FFF0F1"   # coral chip / alert card bg tint
GOLD          = "#FFAD28"   # fill elements only (bars, borders) — NOT text on light bg
GOLD_BG       = "#FFF8EC"   # gold chip / warning card bg tint

# ── UI Semantic Aliases ────────────────────────────────────────────────────
SIDEBAR_BG        = MIDNIGHT
SIDEBAR_TEXT      = FL_03          # default nav item text on dark bg
SIDEBAR_ACTIVE_BG = "#232623"      # slightly lighter midnight for active row
SIDEBAR_ACCENT    = CORAL          # active nav left-border

CONTENT_BG  = SUNRISE_WHITE
CARD_BG     = MORNING_WHITE
BORDER_COLOR= FL_03

TEXT_PRIMARY   = FL_01
TEXT_SECONDARY = FL_02
TEXT_MUTED     = FL_03

PRIMARY  = MIDNIGHT  # primary action buttons
DANGER   = CORAL     # clock-out, destructive
WARNING  = GOLD      # fill accents (not text)

# ── Status chip colours (bg, fg) ──────────────────────────────────────────
CHIP_IDLE        = (SUNRISE_CREAM, FL_02)   # muted / inactive
CHIP_CLOCKED_IN  = (MIDNIGHT,      "#FFFFFF")  # dark chip / ok
CHIP_ON_LUNCH    = (GOLD_BG,       FL_01)   # gold chip / warning — FL_01 text, NOT gold
CHIP_CLOCKED_OUT = (SUNRISE_CREAM, FL_02)   # muted / done

# ── Typography ─────────────────────────────────────────────────────────────
# Funnel Sans (brand) → falls back to platform system sans-serif
if platform.system() == "Windows":
    FONT_FAMILY = "Segoe UI"
elif platform.system() == "Darwin":
    FONT_FAMILY = "Helvetica Neue"
else:
    FONT_FAMILY = "sans-serif"

# ── Work target ────────────────────────────────────────────────────────────
WORK_HOURS_DAILY = 8.0
