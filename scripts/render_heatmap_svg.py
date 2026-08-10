from pathlib import Path
import json
from html import escape


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


# GitHub-style green palette.
PALETTE = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


CELL = 13
GAP = 4
STEP = CELL + GAP

LEFT = 40
TOP = 42

WIDTH = 860
HEIGHT = 150


def load_data():

    with INPUT.open(
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def create_svg(data):

    days = data["days"]

    username = data["username"]

    # --------------------------------------------------------
    # Arrange days into weeks.
    #
    # GitHub calendar = 7 rows:
    #
    # Sunday
    # Monday
    # Tuesday
    # Wednesday
    # Thursday
    # Friday
    # Saturday
    # --------------------------------------------------------

    weeks = []

    current_week = []

    for index, day in enumerate(days):

        current_week.append(day)

        if len(current_week) == 7:

            weeks.append(
                current_week
            )

            current_week = []

    if current_week:

        weeks.append(
            current_week
        )

    # Maximum 53 weeks.
    weeks = weeks[-53:]

    svg_parts = []

    # --------------------------------------------------------
    # SVG HEADER
    # --------------------------------------------------------

    svg_parts.append(
        f'''<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">

        <defs>

            <filter
                id="shadow"
                x="-20%"
                y="-20%"
                width="140%"
                height="140%">

                <feDropShadow
                    dx="0"
                    dy="1"
                    stdDeviation="1"
                    flood-color="#000000"
                    flood-opacity="0.35"/>

            </filter>

        </defs>

        <rect
            width="100%"
            height="100%"
            rx="12"
            fill="#0d1117"/>

        <text
            x="20"
            y="25"
            fill="#c9d1d9"
            font-family="monospace"
            font-size="13"
            font-weight="bold">

            @{escape(username)} — contribution activity

        </text>
        '''
    )

    # --------------------------------------------------------
    # DRAW CELLS
    # --------------------------------------------------------

    for week_index, week in enumerate(weeks):

        for day_index, day in enumerate(week):

            level = int(
                day.get(
                    "level",
                    0
                )
            )

            color = PALETTE.get(
                level,
                PALETTE[0]
            )

            x = (
                LEFT
                + week_index * STEP
            )

            y = (
                TOP
                + day_index * STEP
            )

            # Stagger the animation diagonally.
            delay = (
                week_index * 0.025
                + day_index * 0.035
            )

            svg_parts.append(
                f'''
                <rect
                    x="{x}"
                    y="{y}"
                    width="{CELL}"
                    height="{CELL}"
                    rx="3"
                    fill="{color}"
                    opacity="0"
                    filter="url(#shadow)">

                    <animate
                        attributeName="opacity"
                        from="0"
                        to="1"
                        dur="0.35s"
                        begin="{delay:.3f}s"
                        fill="freeze"/>

                    <animateTransform
                        attributeName="transform"
                        type="translate"
                        from="0,-5"
                        to="0,0"
                        dur="0.35s"
                        begin="{delay:.3f}s"
                        fill="freeze"/>

                </rect>
                '''
            )

    # --------------------------------------------------------
    # LEGEND
    # --------------------------------------------------------

    legend_y = TOP + 7 * STEP + 15

    svg_parts.append(
        f'''
        <text
            x="{LEFT}"
            y="{legend_y}"
            fill="#8b949e"
            font-family="monospace"
            font-size="10">

            Less

        </text>
        '''
    )

    legend_x = LEFT + 35

    for level in range(5):

        color = PALETTE[level]

        svg_parts.append(
            f'''
            <rect
                x="{legend_x + level * 18}"
                y="{legend_y - 9}"
                width="12"
                height="12"
                rx="3"
                fill="{color}"/>
            '''
        )

    svg_parts.append(
        f'''
        <text
            x="{legend_x + 5 * 18 + 5}"
            y="{legend_y}"
            fill="#8b949e"
            font-family="monospace"
            font-size="10">

            More

        </text>
        '''
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    svg_parts.append(
        f'''
        <text
            x="{WIDTH - 20}"
            y="{legend_y}"
            text-anchor="end"
            fill="#8b949e"
            font-family="monospace"
            font-size="10">

            live from github.com/{escape(username)}

        </text>

        </svg>
        '''
    )

    return "\n".join(
        svg_parts
    )


def main():

    print()
    print("=" * 45)
    print("Heatmap SVG Generator")
    print("=" * 45)
    print()

    if not INPUT.exists():

        print(
            f"ERROR: {INPUT} does not exist."
        )

        print(
            "Run fetch_contributions.py first."
        )

        return

    data = load_data()

    svg = create_svg(data)

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(
        f"Created: {OUTPUT}"
    )

    print()


if __name__ == "__main__":
    main()
