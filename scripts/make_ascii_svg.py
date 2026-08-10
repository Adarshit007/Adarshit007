from pathlib import Path
import sys

from PIL import Image


INPUT_IMAGE = Path("source-prepped.png")
OUTPUT_SVG = Path("avi-ascii.svg")

ASCII_WIDTH = 90

# IMPORTANT:
# White = space
# Dark = @
RAMP = " .:-=+*#%@"

FONT_SIZE = 8
LINE_HEIGHT = 9

TEXT_COLOR = "#333333"


def crop_subject(image):
    """Remove large white areas around the person."""

    gray = image.convert("L")

    # Find pixels that are darker than white.
    mask = gray.point(
        lambda p: 255 if p < 245 else 0
    )

    bbox = mask.getbbox()

    if bbox is None:
        return image

    left, top, right, bottom = bbox

    width = right - left
    height = bottom - top

    # Small margin around the person.
    mx = int(width * 0.05)
    my = int(height * 0.05)

    left = max(0, left - mx)
    top = max(0, top - my)
    right = min(image.width, right + mx)
    bottom = min(image.height, bottom + my)

    return image.crop(
        (left, top, right, bottom)
    )


def image_to_ascii(image):

    image = image.convert("L")

    width, height = image.size

    # Compensate for terminal characters being taller
    # than they are wide.
    new_height = max(
        1,
        int(ASCII_WIDTH * height / width * 0.45)
    )

    image = image.resize(
        (ASCII_WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    pixels = image.load()

    rows = []

    for y in range(new_height):

        row = ""

        for x in range(ASCII_WIDTH):

            brightness = pixels[x, y]

            # Dark pixels become dense characters.
            index = int(
                (255 - brightness)
                / 255
                * (len(RAMP) - 1)
            )

            row += RAMP[index]

        rows.append(row)

    return rows


def escape_xml(text):

    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def create_svg(rows):

    # Character dimensions.
    char_width = FONT_SIZE * 0.62

    width = ASCII_WIDTH * char_width + 20
    height = len(rows) * LINE_HEIGHT + 20

    svg = []

    svg.append(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width:.0f}"
    height="{height:.0f}"
    viewBox="0 0 {width:.0f} {height:.0f}"
    role="img"
    aria-label="Animated ASCII portrait">
'''
    )

    # White background.
    svg.append(
        f'''<rect
    x="0"
    y="0"
    width="{width:.0f}"
    height="{height:.0f}"
    fill="#ffffff"/>
'''
    )

    # Draw every row.
    for i, row in enumerate(rows):

        y = 12 + i * LINE_HEIGHT

        delay = i * 0.035

        safe = escape_xml(row)

        svg.append(
            f'''<text
    x="10"
    y="{y}"
    font-family="Consolas, Courier New, monospace"
    font-size="{FONT_SIZE}px"
    font-weight="600"
    fill="{TEXT_COLOR}"
    xml:space="preserve"
    opacity="0">

    {safe}

    <animate
        attributeName="opacity"
        from="0"
        to="1"
        begin="{delay:.3f}s"
        dur="0.25s"
        fill="freeze"/>
</text>
'''
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main():

    if not INPUT_IMAGE.exists():

        print()
        print("ERROR: source-prepped.png not found.")
        print()

        sys.exit(1)

    print("Loading photo...")

    image = Image.open(INPUT_IMAGE)

    print("Cropping white space...")

    image = crop_subject(image)

    print(
        f"Image size after crop: "
        f"{image.width} x {image.height}"
    )

    print("Converting to ASCII...")

    rows = image_to_ascii(image)

    print(
        f"ASCII dimensions: "
        f"{ASCII_WIDTH} x {len(rows)}"
    )

    print("Creating SVG...")

    svg = create_svg(rows)

    OUTPUT_SVG.write_text(
        svg,
        encoding="utf-8"
    )

    print()
    print("==============================")
    print("SUCCESS!")
    print("==============================")
    print()
    print("Created:")
    print("avi-ascii.svg")
    print()


if __name__ == "__main__":
    main()