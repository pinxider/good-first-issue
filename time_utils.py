import pandas as pd
from datetime import datetime, timezone, timedelta
from dateutil import parser

# Time Constants
SECONDS_IN_MINUTE = 60   
SECONDS_IN_HOUR = 3600
SECONDS_IN_DAY = 86400
SECONDS_IN_30_DAYS = 2592000  # 30 * 24 * 60 * 60
DAYS_IN_30_DAYS = 30
DAYS_IN_6_MONTHS = 180

# Http Constants
API_ITEMS_PER_PAGE = 100
HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_FORBIDDEN = 403
RATE_LIMIT_FALLBACK_SECONDS = 60

# Sidebar Filter Options
TIME_FILTERS = ["24 hours", "7 days", "30 days", "6 months"]


def format_time(secs: float | int) -> str:
    if pd.isna(secs):
        return "N/A"
    
    secs = int(secs)
    days, remainder = divmod(secs, SECONDS_IN_DAY)
    hours, remainder = divmod(remainder, SECONDS_IN_HOUR)
    minutes = remainder // SECONDS_IN_MINUTE

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}min")
    if not parts:
        return "<1min"
    return " ".join(parts)

def to_date_time(date_filter_option: str) -> datetime:
    if date_filter_option == "24 hours":
        return datetime.now(timezone.utc) - timedelta(days=1)
    elif date_filter_option == "7 days":
        return datetime.now(timezone.utc) - timedelta(days=7)
    elif date_filter_option == "30 days":
        return datetime.now(timezone.utc) - timedelta(days=DAYS_IN_30_DAYS)
    elif date_filter_option == "6 months":
        return datetime.now(timezone.utc) - timedelta(days=DAYS_IN_6_MONTHS)

def seconds_since_update(updated_at : str) -> float:
    now = datetime.now(timezone.utc)
    return(now - parser.isoparse(updated_at)).total_seconds()