#!/usr/bin/env python3
"""
pulisci_exif.py — ai riparo (Alex Lunalbi)
Rimuove i metadati EXIF (inclusi GPS, data di scatto, modello dispositivo)
da un'immagine, salvando una copia locale senza sovrascrivere l'originale.

Non invia nulla online. Nessuna telemetria.

Licenza: MIT
Requisiti: Python 3.9+, Pillow (python -m pip install Pillow / python3 -m pip)
Versione: 1.0.0

Uso:
  python pulisci_exif.py foto.jpg
  python3 pulisci_exif.py foto.jpg
  python pulisci_exif.py "C:\\Users\\Tu\\Foto estate\\foto.jpg"
  python3 pulisci_exif.py "/Users/tu/Foto estate/foto.jpg"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print(
        "Errore: manca la libreria Pillow.\n"
        "Attiva il venv, poi digita:\n"
        "  Windows:  python -m pip install Pillow\n"
        "  macOS/Linux: python3 -m pip install Pillow",
        file=sys.stderr,
    )
    sys.exit(1)

__version__ = "1.0.0"

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def rimuovi_metadati(percorso: Path) -> Path:
    """Crea una copia senza EXIF accanto all'originale (prefisso pulita_)."""
    if not percorso.is_file():
        raise FileNotFoundError(f"Il file non esiste: {percorso}")

    suffix = percorso.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            f"Formato non supportato ({suffix}). "
            f"Usa: {', '.join(sorted(SUPPORTED_SUFFIXES))}"
        )

    output = percorso.with_name(f"pulita_{percorso.name}")

    with Image.open(percorso) as immagine:
        # Applica l'orientamento EXIF ai pixel, poi scarta i metadati.
        # Evita che le foto verticali risultino "sdraiate" dopo la pulizia.
        immagine = ImageOps.exif_transpose(immagine)

        info = dict(immagine.info)
        info.pop("exif", None)
        info.pop("xmp", None)

        save_kwargs: dict = {}
        if suffix in {".jpg", ".jpeg"}:
            # JPEG non supporta la trasparenza; convertiamo se necessario.
            if immagine.mode in {"RGBA", "P"}:
                immagine = immagine.convert("RGB")
            save_kwargs["quality"] = 95
            save_kwargs["optimize"] = True

        immagine.save(output, **save_kwargs)

    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Rimuove i metadati EXIF da un'immagine e salva una copia "
            "con prefisso pulita_ (l'originale non viene toccato)."
        )
    )
    parser.add_argument(
        "immagine",
        type=Path,
        help="Percorso del file immagine da pulire",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        print(f"Lettura: {args.immagine}")
        output = rimuovi_metadati(args.immagine.resolve())
        print(f"Fatto. Immagine senza metadati salvata in: {output}")
        return 0
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Errore: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
