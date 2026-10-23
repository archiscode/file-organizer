# File Organizer

A small Python command-line tool that tidies a messy folder (like Downloads) by moving every file into a sub-folder based on its type: Images, Documents, Spreadsheets, Archives, Code and so on.

## Features
- `--dry-run` mode to preview changes before anything moves
- Never overwrites: duplicate names become `name_1.ext`, `name_2.ext`
- Skips hidden files and existing sub-folders
- No external dependencies (Python 3.9+)
- Unit tests included

## Usage
```bash
python organizer.py ~/Downloads --dry-run
python organizer.py ~/Downloads
```

## Run the tests
```bash
python -m unittest discover tests
```

## Customise
Edit the `CATEGORIES` dictionary in `organizer.py` to add your own file types.

## Tech
Python, `pathlib`, `shutil`, `argparse`, `unittest`
