import sys
import requests
from datetime import datetime, date

DATE_SOURCES = [
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.cloudflare.com",
    "https://api.github.com"
]

def check_app_expiration(expiration_date=date(2026, 1, 2)): #yy-mm-dd
    """
    Returns True if application is not expired.
    Exits if expired or online date cannot be verified.
    Prints the online date used for validation.
    """

    online_date = None
    source_used = None

    for url in DATE_SOURCES:
        try:
            r = requests.get(url, timeout=10)
            date_header = r.headers.get("Date")

            if not date_header:
                continue

            online_datetime = datetime.strptime(
                date_header, "%a, %d %b %Y %H:%M:%S %Z"
            )
            online_date = online_datetime.date()
            source_used = url
            break

        except Exception:
            continue

    if online_date is None:
        print("❌ Online date verification blocked by environment.")
        sys.exit(1)

    print(f"🕒 Online date detected: {online_date} (source: {source_used})")

    if online_date > expiration_date:
        print("⛔ Application expired.")
        sys.exit(0)

    return True

check_app_expiration()
print("🚀 Application running...")
