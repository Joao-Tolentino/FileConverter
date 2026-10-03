# FileConverter

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6.svg?logo=windows&logoColor=white)](#)

A versatile, all-in-one local file conversion suite. Outfitted with a dynamic Tkinter GUI, it autonomously identifies your input file type (Documents, Images, Audio, Video, Archives) and executes the appropriate conversion libraries natively.

---

## Features

- **Tkinter Dynamic GUI**: The `ttk.Combobox` automatically updates its available output formats based purely on the extension of your chosen input file.
- **Archive Extraction**: Natively extracts `.zip`, `.tar`, and `.gz` using standard libraries, while hooking into `patoolib` for `.rar` files.
- **Media Manipulation**: Transcodes Audio/Video using `ffmpeg-python` and `pydub`, and effortlessly converts image channels (like `RGBA` to `RGB`) using `Pillow`.
- **Document Rendering**: Parses DOCX using `python-docx`, extracts PDF text using `PyPDF2`, and utilizes `reportlab` to write new PDFs dynamically.

---

## Quick Start

1. Clone or download the repository.
2. Install Python 3.
3. Install system dependencies: ensure `ffmpeg` is installed and accessible in your system PATH.
4. Install pip requirements: `pip install -r requirements.txt`
5. Run `python main_gui.py`

---

## Configuration Details

No API keys are required. However, for `.rar` extraction to function, your system must have a valid unrar executable installed for `patoolib` to interface with. Similarly, Audio/Video conversion explicitly demands the `ffmpeg` binary.

---

## Usage Guidelines

- Click **Select File** and pick a document, image, media file, or archive.
- The dropdown box will instantly populate with valid conversion targets for your specific file. Select one.
- Click **Convert**. The app will dispatch the request to `functions.py`, crunch the data, and output the newly formatted file to the exact same folder as your input file!

---

## Technical Documentation

For developers interested in directory structures, code architecture, or compilation guidelines, please refer to the **[Documentation.md](Documentation.md)** file.

---

## License

This project is licensed under the **GNU Affero General Public License Version 3 (AGPLv3)**. See the LICENSE file for details.
