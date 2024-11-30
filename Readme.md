# Markdown Equations Fixer

[![PyPI version](https://badge.fury.io/py/markdown-equations-fixer.svg)](https://badge.fury.io/py/markdown-equations-fixer)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool that converts LaTeX-style mathematical equations (`\[...\]`) to proper markdown format (`$$...$$`) in your markdown files.

## Quick Start

```bash
# Install from PyPI
pip install markdown-equations-fixer

# Basic usage
meq-fixer fix document.md
```

## Installation

You can install the package directly from PyPI:

```bash
pip install markdown-equations-fixer
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/dynstat/markdown-equations-fixer.git
```

## Usage

Basic usage:
```bash
meq-fixer fix document.md
```

Multiple files:
```bash
meq-fixer fix file1.md file2.md docs/
```

### Options

- `--dry-run`: Preview changes without modifying files
- `--verbose`, `-v`: Show detailed progress
- `--recursive`, `-r`: Process directories recursively

### Examples

Process a directory recursively:
```bash
meq-fixer fix -r ./docs/
```

Preview changes:
```bash
meq-fixer fix --dry-run thesis.md
```

### Format Conversion

Convert between different document formats:
```bash
# Basic conversion (markdown to GitHub-Flavored Markdown)
meq-fixer convert input.md output.md

# Convert markdown to DOCX (two approaches)
# Method 1: Fix equations first, then convert
meq-fixer fix test_equations.md
meq-fixer convert test_equations.md output.docx --from-format markdown --to-format docx

# Method 2: Fix and convert in one step
meq-fixer convert test_equations.md output.docx --from-format markdown --to-format docx --fix-equations

# Convert from LaTeX to DOCX
meq-fixer convert paper.tex paper.docx --from-format latex --to-format docx

# Convert and fix equations in one go
meq-fixer convert --fix-equations paper.tex paper.md
```

Supported formats:
- markdown
- gfm (GitHub-Flavored Markdown)
- commonmark
- latex
- org
- docx
- pdf

### Requirements for DOCX/PDF Conversion

To ensure proper equation rendering in DOCX and PDF files, you need:

1. Pandoc installed on your system:
   - Windows: `choco install pandoc`
   - macOS: `brew install pandoc`
   - Linux: `sudo apt-get install pandoc`

2. A LaTeX distribution:
   - Windows: `choco install miktex`
   - macOS: `brew install basictex`
   - Linux: `sudo apt-get install texlive-latex-extra`

## Features

- Converts `\[...\]` to `$$...$$` format
- Handles single-line and multi-line equations
- Supports recursive directory processing
- Document format conversion using pandoc (including DOCX and PDF)
- Dry-run mode for safe testing
- Rich console output with progress tracking

## Requirements

- Python 3.7+
- click>=8.0.0
- rich>=10.0.0
- pypandoc>=1.11
- pandoc (system requirement)
- LaTeX distribution (for equation rendering in DOCX/PDF)

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Issues and pull requests are welcome on [GitHub](https://github.com/dynstat/markdown-equations-fixer/).
```
