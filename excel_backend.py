import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

import config
import utils

HEADERS = [
    "Date", "Punch In", "Lunch Start", "Lunch End", "Punch Out",
    "Comment", "Ad-hoc Hrs", "Ad-hoc Note", "Total Hours"
]
COL_WIDTHS = [12, 10, 12, 10, 10, 30, 11, 30, 12]


class ExcelBackend:
    def __init__(self, path):
        self.path = path
        self._load()

    def _load(self):
        try:
            self.wb = openpyxl.load_workbook(self.path, data_only=True)
        except (FileNotFoundError, Exception):
            # New workbook — default "Sheet" stays until first write_day()
            self.wb = openpyxl.Workbook()

    def _get_or_create_sheet(self, date):
        name = utils.sheet_name_for_date(date)
        # Drop the placeholder default sheet on first real write
        if "Sheet" in self.wb.sheetnames and name not in self.wb.sheetnames:
            del self.wb["Sheet"]
        if name not in self.wb.sheetnames:
            ws = self.wb.create_sheet(name)
            self._write_header(ws)
            self._sort_sheets()
        return self.wb[name]

    def _write_header(self, ws):
        hdr_font = Font(name="Calibri", bold=True, color="FFFFFF")
        hdr_fill = PatternFill(start_color="1E3A5F", end_color="1E3A5F", fill_type="solid")
        for col, h in enumerate(HEADERS, 1):
            cell = ws.cell(row=1, column=col, value=h)
            cell.font = hdr_font
            cell.fill = hdr_fill
            cell.alignment = Alignment(horizontal="center")
        ws.freeze_panes = "A2"
        for col, w in enumerate(COL_WIDTHS, 1):
            ws.column_dimensions[get_column_letter(col)].width = w

    def _sort_sheets(self):
        def sheet_key(name):
            try:
                d = datetime.datetime.strptime(name, "%b %Y")
                return (d.year, d.month)
            except ValueError:
                return (9999, 99)
        self.wb._sheets.sort(key=lambda ws: sheet_key(ws.title))

    def _normalize_date(self, cell_val):
        if cell_val is None:
            return None
        if isinstance(cell_val, datetime.datetime):
            return cell_val.date()
        if isinstance(cell_val, datetime.date):
            return cell_val
        if isinstance(cell_val, str):
            try:
                return datetime.date.fromisoformat(cell_val)
            except ValueError:
                return None
        return None

    def _find_row(self, ws, date):
        for row in range(2, ws.max_row + 1):
            cell_val = ws.cell(row=row, column=config.COL_DATE).value
            if self._normalize_date(cell_val) == date:
                return row
        return None

    def _ensure_row(self, ws, date):
        row = self._find_row(ws, date)
        if row is None:
            row = max(ws.max_row + 1, 2)
            ws.cell(row=row, column=config.COL_DATE).value = date
        return row

    def _empty_day(self, date=None):
        return {
            "date": date,
            "punch_in": "",
            "lunch_start": "",
            "lunch_end": "",
            "punch_out": "",
            "punch_comment": "",
            "adhoc_hours": None,
            "adhoc_note": "",
            "total_hours": None,
        }

    def _row_to_dict(self, ws, row, date):
        def g(col):
            return ws.cell(row=row, column=col).value

        adhoc = g(config.COL_ADHOC_HRS)
        total = g(config.COL_TOTAL_HRS)

        return {
            "date": date,
            "punch_in": str(g(config.COL_PUNCH_IN) or "").strip(),
            "lunch_start": str(g(config.COL_LUNCH_START) or "").strip(),
            "lunch_end": str(g(config.COL_LUNCH_END) or "").strip(),
            "punch_out": str(g(config.COL_PUNCH_OUT) or "").strip(),
            "punch_comment": str(g(config.COL_PUNCH_COMMENT) or "").strip(),
            "adhoc_hours": float(adhoc) if adhoc is not None else None,
            "adhoc_note": str(g(config.COL_ADHOC_NOTE) or "").strip(),
            "total_hours": float(total) if total is not None else None,
        }

    def read_day(self, date):
        name = utils.sheet_name_for_date(date)
        if name not in self.wb.sheetnames:
            return self._empty_day(date)
        ws = self.wb[name]
        row = self._find_row(ws, date)
        if row is None:
            return self._empty_day(date)
        return self._row_to_dict(ws, row, date)

    def write_day(self, date, data):
        ws = self._get_or_create_sheet(date)
        row = self._ensure_row(ws, date)

        def sv(col, val):
            ws.cell(row=row, column=col).value = val or None

        ws.cell(row=row, column=config.COL_DATE).value = date
        sv(config.COL_PUNCH_IN, data.get("punch_in"))
        sv(config.COL_LUNCH_START, data.get("lunch_start"))
        sv(config.COL_LUNCH_END, data.get("lunch_end"))
        sv(config.COL_PUNCH_OUT, data.get("punch_out"))
        sv(config.COL_PUNCH_COMMENT, data.get("punch_comment"))
        ws.cell(row=row, column=config.COL_ADHOC_HRS).value = data.get("adhoc_hours") or None
        sv(config.COL_ADHOC_NOTE, data.get("adhoc_note"))

        pi = utils.parse_time(data.get("punch_in"))
        ls = utils.parse_time(data.get("lunch_start"))
        le = utils.parse_time(data.get("lunch_end"))
        po = utils.parse_time(data.get("punch_out"))
        ah = data.get("adhoc_hours")
        total = utils.compute_hours(pi, ls, le, po, ah)
        ws.cell(row=row, column=config.COL_TOTAL_HRS).value = total

        try:
            self.wb.save(self.path)
        except PermissionError:
            raise PermissionError(
                "The Excel file is open in another program. Close it first."
            )

    def read_month(self, year, month):
        name = utils.sheet_name_for_date(datetime.date(year, month, 1))
        if name not in self.wb.sheetnames:
            return []
        ws = self.wb[name]
        result = []
        for row in range(2, ws.max_row + 1):
            date = self._normalize_date(ws.cell(row=row, column=config.COL_DATE).value)
            if date is None:
                continue
            result.append(self._row_to_dict(ws, row, date))
        return result

    def read_all(self):
        result = []
        for name in self.wb.sheetnames:
            try:
                d = datetime.datetime.strptime(name, "%b %Y")
                result.extend(self.read_month(d.year, d.month))
            except ValueError:
                continue
        return result

    def get_months_with_data(self):
        months = []
        for name in self.wb.sheetnames:
            try:
                d = datetime.datetime.strptime(name, "%b %Y")
                months.append((d.year, d.month))
            except ValueError:
                continue
        return months

    def change_path(self, new_path):
        self.wb.save(new_path)
        self.path = new_path
        self._load()
