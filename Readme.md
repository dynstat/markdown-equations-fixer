# Markdown Equations Fixer and Converter

[![PyPI version](https://badge.fury.io/py/markdown-equations-fixer.svg)](https://badge.fury.io/py/markdown-equations-fixer)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool to standardize mathematical equations in Markdown files and convert documents between formats (Markdown, LaTeX, DOCX, PDF).

## Key Features

- **Fix Markdown Equations**: Standardizes LaTeX-style equations to Markdown format
  - `\[...\]` → `$$...$$` (block equations)
  - `\(...\)` → `$...$` (inline equations)
  - Multi-line equations supported
- **Document Conversion**: Convert between formats using Pandoc
  - Input: `markdown`, `gfm`, `commonmark`, `latex`, `org`, `docx`
  - Output: `markdown`, `gfm`, `commonmark`, `latex`, `org`, `docx`, `pdf`
- **CLI Features**: Recursive processing, dry-run mode, progress indicators

## Installation

**Prerequisites**: Python 3.7+

```bash
pip install markdown-equations-fixer
```

> **Note:** For fixing equations in Markdown files, you _do not_ need to install Pandoc or LaTeX—only `pip install markdown-equations-fixer` is required.


**For document conversion**, install [Pandoc](https://pandoc.org/installing.html):
- Windows: `choco install pandoc`
- macOS: `brew install pandoc`
- Linux: `sudo apt-get install pandoc`

**For PDF/DOCX output**, install a LaTeX distribution:
- Windows: `choco install miktex`
- macOS: `brew install --cask basictex`
- Linux: `sudo apt-get install texlive-latex-extra`

## Usage

### Fix Equations

Standardize mathematical equations in Markdown files (`.md`, `.markdown`):

```bash
# Fix a single file
meq-fixer fix document.md

# Fix multiple files/directories
meq-fixer fix file1.md file2.md ./docs/

# Recursively process a directory
meq-fixer fix -r ./my-project/

# Preview changes without modifying (dry run)
meq-fixer fix --dry-run thesis.md

# Verbose output
meq-fixer fix -v document.md
```

**Options:**
- `--dry-run`: Preview without making changes
- `--verbose`, `-v`: Show detailed progress
- `--recursive`, `-r`: Process subdirectories

### Convert Documents

Convert between document formats:

```bash
# Markdown to DOCX
meq-fixer convert paper.md paper.docx --to-format docx

# LaTeX to GitHub Markdown
meq-fixer convert report.tex report.md -f latex -t gfm

# Convert and fix equations (Markdown output only)
meq-fixer convert paper.tex paper.md -t markdown --fix-equations

# Markdown to PDF
meq-fixer convert thesis.md thesis.pdf -t pdf
```

**Options:**
- `--from-format`, `-f`: Input format (`markdown`, `gfm`, `commonmark`, `latex`, `org`, `docx`)
- `--to-format`, `-t`: Output format (`markdown`, `gfm`, `commonmark`, `latex`, `pdf`, `docx`, `org`)
- `--fix-equations`: Fix equations in Markdown output (Markdown formats only)

## Examples

**Input:**
```markdown
Here's an equation: \[E = mc^2\]

And a matrix:
\[
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
\]
```

**Output:**  May not format properly on github, but will work on markdown editor apps like obsidian, marktext, etc.
```markdown
Here's an equation: $$E = mc^2$$

And a matrix:
$$
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
$$
```

## Dependencies

**Python packages** (installed automatically):
- `click>=8.0.0`
- `rich>=10.0.0`
- `pypandoc`

See [Installation](#installation) for system dependencies.

## License

MIT License. See [LICENSE](LICENSE) file.

## Contributing

Contributions welcome! Open an [issue](https://github.com/dynstat/markdown-equations-fixer/issues) or submit a [pull request](https://github.com/dynstat/markdown-equations-fixer/pulls).
