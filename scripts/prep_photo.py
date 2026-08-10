from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)

    output_path = input_path.parent / "source-prepped.png"

    print("Loading photo...")
    image = Image.open(input_path).convert("RGBA")

    print("Removing background...")
    foreground = remove(image)

    # Convert to OpenCV format
    rgba = np.array(foreground)

    # Extract alpha channel
    alpha = rgba[:, :, 3]

    # Convert RGB to grayscale
    rgb = rgba[:, :, :3]
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    print("Enhancing contrast...")

    # Improve local contrast using CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # White background
    white = np.full_like(enhanced, 255)

    # Composite subject over white
    alpha_float = alpha.astype(np.float32) / 255.0

    result = (
        enhanced.astype(np.float32) * alpha_float
        + white.astype(np.float32) * (1 - alpha_float)
    )

    result = np.clip(result, 0, 255).astype(np.uint8)

    output = Image.fromarray(result, mode="L")

    output.save(output_path)

    print()
    print(f"Done!")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()