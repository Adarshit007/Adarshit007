from pathlib import Path
import os


OUTPUT = Path("info-card.svg")

STATIC = os.getenv("STATIC", "0") == "1"


# ------------------------------------------------------------
# YOUR PROFILE INFORMATION
# ------------------------------------------------------------

NAME = "DATA ANALYST"

ROLE = "Data Analyst"

CURRENT_FOCUS = "Analytics → Machine Learning"

STACK = [
    "Excel",
    "Google Sheets",
    "SQL Server",
    "Python",
    "Power BI",
]

LEARNING = [
    "Machine Learning",
    "Statistics",
    "Predictive Analytics",
]


# ------------------------------------------------------------
# SVG SETTINGS
# ------------------------------------------------------------

WIDTH = 490
HEIGHT = 300

BACKGROUND = "#0d1117"
BORDER = "#30363d"

WHITE = "#f0f6fc"
MUTED = "#8b949e"

GREEN = "#39d353"
BLUE = "#58a6ff"
YELLOW = "#d29922"
PURPLE = "#bc8cff"


def escape(text):
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def text_element(
    text,
    x,
    y,
    size=14,
    color=WHITE,
    weight="400",
    anchor="start",
    opacity="1",
):
    return f'''
    <text
        x="{x}"
        y="{y}"
        fill="{color}"
        font-family="Consolas, 'Courier New', monospace"
        font-size="{size}px"
        font-weight="{weight}"
        text-anchor="{anchor}"
        opacity="{opacity}"
    >{escape(text)}</text>
    '''


def build_svg():

    svg = []

    svg.append(
        f'''<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    role="img"
    aria-label="Data Analyst profile information card"
>'''
    )

    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    svg.append(
        f'''
        <rect
            x="1"
            y="1"
            width="{WIDTH - 2}"
            height="{HEIGHT - 2}"
            rx="12"
            fill="{BACKGROUND}"
            stroke="{BORDER}"
            stroke-width="2"
        />
        '''
    )

    # --------------------------------------------------------
    # TOP TERMINAL BAR
    # --------------------------------------------------------

    svg.append(
        '<circle cx="20" cy="20" r="5" fill="#ff5f56"/>'
    )

    svg.append(
        '<circle cx="38" cy="20" r="5" fill="#ffbd2e"/>'
    )

    svg.append(
        '<circle cx="56" cy="20" r="5" fill="#27c93f"/>'
    )

    svg.append(
        text_element(
            "profile.sh",
            75,
            25,
            12,
            MUTED
        )
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    svg.append(
        text_element(
            "$ whoami",
            25,
            55,
            13,
            GREEN,
            "600"
        )
    )

    svg.append(
        text_element(
            NAME,
            25,
            82,
            22,
            WHITE,
            "700"
        )
    )

    # --------------------------------------------------------
    # ROLE
    # --------------------------------------------------------

    svg.append(
        text_element(
            "ROLE",
            25,
            110,
            11,
            BLUE,
            "700"
        )
    )

    svg.append(
        text_element(
            ROLE,
            115,
            110,
            13,
            WHITE
        )
    )

    # --------------------------------------------------------
    # CURRENT FOCUS
    # --------------------------------------------------------

    svg.append(
        text_element(
            "FOCUS",
            25,
            136,
            11,
            PURPLE,
            "700"
        )
    )

    svg.append(
        text_element(
            CURRENT_FOCUS,
            115,
            136,
            13,
            WHITE
        )
    )

    # --------------------------------------------------------
    # STACK
    # --------------------------------------------------------

    svg.append(
        text_element(
            "STACK",
            25,
            166,
            11,
            YELLOW,
            "700"
        )
    )

    stack_text = " · ".join(STACK)

    svg.append(
        text_element(
            stack_text,
            25,
            187,
            12,
            WHITE
        )
    )

    # --------------------------------------------------------
    # LEARNING
    # --------------------------------------------------------

    svg.append(
        text_element(
            "LEARNING",
            25,
            218,
            11,
            GREEN,
            "700"
        )
    )

    learning_text = " · ".join(LEARNING)

    svg.append(
        text_element(
            learning_text,
            25,
            239,
            12,
            WHITE
        )
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    svg.append(
        text_element(
            "$ ./next_step.sh",
            25,
            274,
            12,
            GREEN,
            "600"
        )
    )

    svg.append(
        text_element(
            "→ building toward ML",
            455,
            274,
            11,
            MUTED,
            "400",
            "end"
        )
    )

    # --------------------------------------------------------
    # ANIMATION
    # --------------------------------------------------------

    if not STATIC:

        # Animate the main groups using CSS.
        svg.append(
            '''
            <style>
                text {
                    animation: appear 0.55s ease-out both;
                }

                text:nth-of-type(1) {
                    animation-delay: 0.15s;
                }

                text:nth-of-type(2) {
                    animation-delay: 0.30s;
                }

                text:nth-of-type(3) {
                    animation-delay: 0.45s;
                }

                text:nth-of-type(4) {
                    animation-delay: 0.60s;
                }

                text:nth-of-type(5) {
                    animation-delay: 0.75s;
                }

                text:nth-of-type(6) {
                    animation-delay: 0.90s;
                }

                text:nth-of-type(7) {
                    animation-delay: 1.05s;
                }

                text:nth-of-type(8) {
                    animation-delay: 1.20s;
                }

                @keyframes appear {
                    from {
                        opacity: 0;
                        transform: translateX(-8px);
                    }

                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
            </style>
            '''
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    print("Creating Data Analyst info card...")

    svg = build_svg()

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("==============================")
    print("INFO CARD CREATED!")
    print("==============================")
    print()
    print(f"Output: {OUTPUT}")
    print()


if __name__ == "__main__":
    main()
