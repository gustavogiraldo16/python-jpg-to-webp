"""Convert JPG/JPEG files from input/ to WebP files in output/."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output"
JPEG_EXTENSIONS = {".jpg", ".jpeg"}
WEBP_QUALITY = 90


def find_images() -> list[Path]:
    """Return supported image paths, sorted for predictable progress output."""
    return sorted(
        (path for path in INPUT_DIR.rglob("*")
         if path.is_file() and path.suffix.lower() in JPEG_EXTENSIONS),
        key=lambda path: str(path).lower(),
    )


def convert_image(source: Path) -> Path:
    """Convert one image without replacing any pre-existing output file."""
    relative_path = source.relative_to(INPUT_DIR)
    destination = (OUTPUT_DIR / relative_path).with_suffix(".webp")
    destination.parent.mkdir(parents=True, exist_ok=True)

    # Refuse collisions, including files created by an earlier run.
    if destination.exists():
        raise FileExistsError(f"El destino ya existe; no se sobrescribió: {destination}")

    with Image.open(source) as image:
        # WebP supports RGB/RGBA; normalize uncommon JPEG modes when needed.
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        image.save(destination, format="WEBP", quality=WEBP_QUALITY)
    return destination


def main() -> int:
    if not INPUT_DIR.is_dir():
        print(f"Error: no existe la carpeta de entrada: {INPUT_DIR}", file=sys.stderr)
        return 1

    images = find_images()
    if not images:
        print(f"No se encontraron imágenes JPG/JPEG en {INPUT_DIR}")
        return 0

    converted = 0
    errors: list[tuple[Path, str]] = []
    total = len(images)
    for index, source in enumerate(images, start=1):
        print(f"[{index}/{total}] {source.relative_to(INPUT_DIR)}", end=" ")
        try:
            destination = convert_image(source)
            converted += 1
            print(f"→ {destination.relative_to(OUTPUT_DIR)} (OK)")
        except Exception as exc:
            errors.append((source, str(exc)))
            print(f"(ERROR: {exc})")

    print("\nResumen")
    print(f"  Encontradas: {total}")
    print(f"  Convertidas: {converted}")
    print(f"  Errores/no convertidas: {len(errors)}")
    if errors:
        print("\nArchivos con error:")
        for source, message in errors:
            print(f"  - {source.relative_to(INPUT_DIR)}: {message}")
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
