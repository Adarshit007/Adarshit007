from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup


USERNAME = "Adarshit007"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def main():

    print()
    print("=" * 45)
    print("GitHub Contribution Fetcher")
    print("=" * 45)
    print()

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Fetching @{USERNAME}...")

    response = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    print(f"HTTP status: {response.status_code}")

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # GitHub contribution cells.
    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    print(
        f"Found {len(cells)} contribution cells."
    )

    if not cells:

        # Fallback for future GitHub HTML changes.
        cells = soup.select(
            "[data-date][data-level]"
        )

        print(
            f"Fallback found {len(cells)} cells."
        )

    days = []

    for cell in cells:

        contribution_date = cell.get(
            "data-date"
        )

        level = cell.get(
            "data-level"
        )

        if not contribution_date:
            continue

        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 0

        days.append(
            {
                "date": contribution_date,
                "level": level
            }
        )

    # Remove duplicates.
    unique = {}

    for day in days:
        unique[day["date"]] = day

    days = sorted(
        unique.values(),
        key=lambda x: x["date"]
    )

    print(
        f"Parsed {len(days)} unique days."
    )

    if not days:

        print()
        print("ERROR: No contribution data found.")
        print()

        return

    # --------------------------------------------------------
    # LEVEL STATISTICS
    # --------------------------------------------------------

    levels = {}

    for day in days:

        level = day["level"]

        levels[level] = (
            levels.get(level, 0) + 1
        )

    print()
    print("Contribution levels:")

    for level in sorted(levels):

        print(
            f"  Level {level}: "
            f"{levels[level]} days"
        )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    result = {
        "username": USERNAME,
        "source": URL,
        "days": days,
        "levels": levels
    }

    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )

    print()
    print("=" * 45)
    print("SUCCESS")
    print("=" * 45)
    print()

    print(
        f"Username: @{USERNAME}"
    )

    print(
        f"Days: {len(days)}"
    )

    print(
        f"Saved: {OUTPUT}"
    )

    print()


if __name__ == "__main__":
    main()