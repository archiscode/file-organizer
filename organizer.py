"""File Organizer: sorts the files in a folder into sub-folders by file type.

Usage:
    python organizer.py ~/Downloads --dry-run   # preview only
    python organizer.py ~/Downloads             # actually move files
"""
import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".m4a"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "Code": {".py", ".js", ".html", ".css", ".sql", ".json", ".ipynb", ".sh"},
    "Installers": {".exe", ".msi", ".dmg", ".pkg", ".deb"},
}
FALLBACK = "Other"


def category_for(path: Path) -> str:
    """Return the category folder name for a file, based on its extension."""
    ext = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return FALLBACK


def unique_destination(destination: Path) -> Path:
    """If destination already exists, add _1, _2, ... so nothing is overwritten."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def organize(folder: Path, dry_run: bool = False) -> list[tuple[Path, Path]]:
    """Move every file in `folder` into a sub-folder named after its category.

    Returns a list of (source, destination) pairs. Hidden files and
    sub-folders are left alone. With dry_run=True nothing is moved.
    """
    if not folder.is_dir():
        raise NotADirectoryError(f"{folder} is not a folder")

    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        target_dir = folder / category_for(item)
        destination = unique_destination(target_dir / item.name)
        moves.append((item, destination))
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))
    return moves


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Sort files in a folder by type.")
    parser.add_argument("folder", type=Path, help="folder to organise")
    parser.add_argument("--dry-run", action="store_true", help="show what would happen without moving anything")
    args = parser.parse_args(argv)

    try:
        moves = organize(args.folder.expanduser(), dry_run=args.dry_run)
    except NotADirectoryError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    verb = "Would move" if args.dry_run else "Moved"
    for source, destination in moves:
        print(f"{verb}: {source.name} -> {destination.parent.name}/{destination.name}")
    print(f"\n{verb} {len(moves)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
