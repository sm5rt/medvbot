from datetime import datetime, timezone


def days_in_club(date):
    delta = datetime.now(timezone.utc) - date
    return delta.days


def format_date(dt):
    return dt.strftime("%d/%m/%Y")