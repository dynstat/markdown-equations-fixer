Here's a concise but complete README.md for your project:


# Markdown Equations Fixer

A command-line tool that converts LaTeX-style mathematical equations (`\[...\]`) to proper markdown format (`$$...$$`) in your markdown files.

## Installation

```bash
pip install markdown-equations-fixer
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

## Features

- Converts `\[...\]` to `$$...$$` format
- Handles single-line and multi-line equations
- Supports recursive directory processing
- Dry-run mode for safe testing
- Rich console output with progress tracking

## Requirements

- Python 3.7+
- click>=8.0.0
- rich>=10.0.0

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Issues and pull requests are welcome on [GitHub](https://github.com/vs15vivek/markdown-equation-fixer).
```
