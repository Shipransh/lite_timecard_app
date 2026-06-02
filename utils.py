import re
import datetime
import calendar as _cal


def parse_time(value):
    if value is None or value == "":
        return None
    if isinstance(value, datetime.time):
        return value
    if isinstance(value, datetime.datetime):
        return value.time()
    s = str(value).strip()
    m = re.match(r'^(\d{1,2}):(\d{2})$', s)
    if m:
        h, mn = int(m.group(1)), int(m.group(2))
        if 0 <= h <= 23 and 0 <= mn <= 59:
            return datetime.time(h, mn)
    return None


def format_time(t):
    if t is None:
        return ""
    return t.strftime("%H:%M")


def validate_hhmm(s):
    return bool(re.match(r'^([01]\d|2[0-3]):[0-5]\d$', s.strip()))


def hhmm_to_decimal(s):
    t = parse_time(s)
    if t is None:
        return None
    return t.hour + t.minute / 60.0


def decimal_to_hhmm(hours):
    if hours is None:
        return "--"
    h = int(abs(hours))
    m = int(round((abs(hours) - h) * 60))
    sign = "-" if hours < 0 else ""
    return "{}{}h {:02d}m".format(sign, h, m)


def sheet_name_for_date(d):
    return d.strftime("%b %Y")


def compute_hours(punch_in, lunch_start, lunch_end, punch_out, adhoc):
    if punch_in is None or punch_out is None:
        return None
    base = datetime.date(2000, 1, 1)
    dt_in = datetime.datetime.combine(base, punch_in)
    dt_out = datetime.datetime.combine(base, punch_out)
    if dt_out < dt_in:
        dt_out += datetime.timedelta(days=1)
    total = (dt_out - dt_in).total_seconds() / 3600.0
    if lunch_start is not None and lunch_end is not None:
        dt_ls = datetime.datetime.combine(base, lunch_start)
        dt_le = datetime.datetime.combine(base, lunch_end)
        if dt_le < dt_ls:
            dt_le += datetime.timedelta(days=1)
        lunch_hrs = (dt_le - dt_ls).total_seconds() / 3600.0
        total -= lunch_hrs
    if adhoc:
        total += adhoc
    return round(total, 2)


def week_dates(d):
    monday = d - datetime.timedelta(days=d.weekday())
    return [monday + datetime.timedelta(days=i) for i in range(7)]


def month_calendar_grid(year, month):
    first = datetime.date(year, month, 1)
    last_day = _cal.monthrange(year, month)[1]
    start_weekday = first.weekday()
    grid = []
    day_num = 1
    for week in range(6):
        row = []
        for wd in range(7):
            cell_index = week * 7 + wd
            if cell_index < start_weekday or day_num > last_day:
                row.append(None)
            else:
                row.append(datetime.date(year, month, day_num))
                day_num += 1
        grid.append(row)
    return grid
