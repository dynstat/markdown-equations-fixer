# Markdown Equations Fixer and Converter

[![PyPI version](https://badge.fury.io/py/markdown-equations-fixer.svg)](https://badge.fury.io/py/markdown-equations-fixer)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A versatile command-line tool to standardize and fix mathematical equations in Markdown files and convert documents between various formats like Markdown, LaTeX, DOCX, and PDF.

## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command: `fix`](#command-fix)
  - [Command: `convert`](#command-convert)
- [Requirements](#requirements)
  - [Python Packages](#python-packages)
  - [System Dependencies](#system-dependencies)
- [License](#license)
- [Contributing](#contributing)

## Key Features

- **Fix Markdown Equations**: Standardizes common LaTeX-style equations to a consistent Markdown format.
  - Converts block equations from `\[...\]` to the widely supported `$$...$$`.
  - Converts inline equations from `\(...\)` to `$..$`.
  - Handles both single-line and multi-line equations gracefully.
- **Document Conversion**: Leverages Pandoc to convert files between a variety of formats, including:
  - `markdown`, `gfm` (GitHub-Flavored Markdown), `commonmark`
  - `latex`
  - `org`
  - `docx`
  - `pdf`
- **User-Friendly CLI**:
  - Process multiple files or entire directories at once.
  - `--recursive` flag to scan through subdirectories.
  - `--dry-run` mode to preview changes without modifying files.
  - Rich console output with progress bars and status indicators.

## Installation

You can install the package directly from PyPI:

```bash
pip install markdown-equations-fixer
```

Or, to install the latest development version from GitHub:

```bash
pip install git+https://github.com/dynstat/markdown-equations-fixer.git
```

## Usage

The tool provides two main commands: `fix` and `convert`.

### Command: `fix`

Use the `fix` command to standardize mathematical equations within your Markdown files (`.md`, `.markdown`).

**Syntax:**
```bash
meq-fixer fix [OPTIONS] [PATHS]...
```

**Examples:**

1.  **Fix a single file:**
    ```bash
    meq-fixer fix document.md
    ```

2.  **Fix multiple files and directories:**
    ```bash
    meq-fixer fix file1.md ./docs/
    ```

3.  **Recursively fix all markdown files in a directory:**
    ```bash
    meq-fixer fix -r ./my-project/
    ```

4.  **Preview changes without saving them (dry run):**
    ```bash
    meq-fixer fix --dry-run thesis.md
    ```

**Options:**

-   `--dry-run`: Preview changes without modifying files.
-   `--verbose`, `-v`: Show detailed, file-by-file progress.
-   `--recursive`, `-r`: Process directories recursively.

### Command: `convert`

Use the `convert` command to translate documents between different formats.

**Syntax:**
```bash
meq-fixer convert [OPTIONS] <INPUT_FILE> <OUTPUT_FILE>
```

**Examples:**

1.  **Convert Markdown to a DOCX document:**
    ```bash
    meq-fixer convert my-paper.md my-paper.docx --to-format docx
    ```

2.  **Convert a LaTeX file to GitHub-Flavored Markdown (GFM):**
    ```bash
    meq-fixer convert report.tex report.md --from-format latex --to-format gfm
    ```

3.  **Convert to Markdown and fix equations in one step:**
    The `--fix-equations` flag applies the same logic as the `fix` command to the *output* file. This is only useful when converting *to* a Markdown format.
    ```bash
    meq-fixer convert paper.tex paper.md --to-format markdown --fix-equations
    ```

**Options:**

-   `--from-format`, `-f`: The input format (e.g., `latex`, `markdown`).
-   `--to-format`, `-t`: The output format (e.g., `docx`, `pdf`, `gfm`).
-   `--fix-equations`: Fix equations in the output file (for Markdown output formats only).

## Requirements

### Python Packages

The installer will handle these dependencies automatically.

-   `click>=8.0.0`
-   `rich>=10.0.0`
-   `pypandoc`

### System Dependencies

For the `convert` command to function, especially for DOCX and PDF output, you must have the following software installed on your system:

1.  **Pandoc**: A universal document converter.
    -   **Windows (with Chocolatey)**: `choco install pandoc`
    -   **macOS (with Homebrew)**: `brew install pandoc`
    -   **Linux (Debian/Ubuntu)**: `sudo apt-get install pandoc`

2.  **A LaTeX Distribution**: Required for rendering equations in PDF and DOCX files.
    -   **Windows**: MiKTeX (`choco install miktex`)
    -   **macOS**: MacTeX (`brew install --cask mactex` or `basictex`)
    -   **Linux (Debian/Ubuntu)**: TeX Live (`sudo apt-get install texlive-latex-extra`)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Issues and pull requests are welcome! Please feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/dynstat/markdown-equations-fixer/).
