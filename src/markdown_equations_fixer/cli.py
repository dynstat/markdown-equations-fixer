import click
import sys
from pathlib import Path
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from typing import Optional, List, Literal
import logging
import pypandoc

from . import __version__


# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize rich console
console = Console()


class EquationFixer:
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_modified = 0
        self.errors = 0

    def fix_equations(self, content: str) -> str:
        """Fix mathematical equations in markdown content."""
        try:
            # Pattern to match block equations delimited by standalone lines with [ and ]
            # Allow optional blank/whitespace-only lines after [ and before ]
            # and preserve inner content trimmed of leading/trailing blank lines.
            bracket_block_pattern = re.compile(
                r"(?ms)^[\t ]*\[[\t ]*\r?\n(.*?)(?:\r?\n)^[\t ]*\][\t ]*(?:\r?\n|$)",
            )

            def _replace_bracket_block(match: re.Match) -> str:
                inner = match.group(1)
                # Trim leading/trailing blank lines in the captured block
                lines = inner.splitlines()
                start = 0
                end = len(lines)
                while start < end and lines[start].strip() == "":
                    start += 1
                while end > start and lines[end - 1].strip() == "":
                    end -= 1
                inner_trimmed = "\n".join(lines[start:end])
                return f"$$\n{inner_trimmed}\n$$\n"

            content = bracket_block_pattern.sub(_replace_bracket_block, content)

            # Pattern to match block equations: \[ ... \]
            # The re.DOTALL flag allows the match to span multiple lines.
            content = re.sub(
                r"\\\[\s*(.*?)\s*\\\]",
                r"$$\n\1\n$$",
                content,
                flags=re.DOTALL,
            )

            # Pattern to match inline equations: \( ... \) -> $ ... $
            content = re.sub(r"\\\((.*?)\\\)", r"$\1$", content)

            # This pattern is aggressive and may have unintended consequences.
            # It's intended to fix single-line equations like \[eq\] to $$eq$$.
            content = re.sub(r"\\(\[|\])", "$$", content)

            # Collapse consecutive dollar signs into a single pair. e.g., $$$$ -> $$
            content = re.sub(r"\${2,}", "$$", content)

            # Ensure proper newlines around block equations for better rendering.
            content = re.sub(r"(\S)\s*(\$\$)", r"\1\n\2", content)
            content = re.sub(r"(\$\$)\s*(\S)", r"\1\n\2", content)

            return content
        except Exception as e:
            logger.error(f"Error fixing equations: {str(e)}")
            raise

    def process_file(self, file_path: Path) -> bool:
        """Process a single markdown file."""
        try:
            if self.verbose:
                logger.info(f"Processing {file_path}")

            # Updated file handling with explicit newline handling
            with open(file_path, "r", encoding="utf-8", newline=None) as file:
                content = file.read()

            modified_content = self.fix_equations(content)

            if content != modified_content:
                if not self.dry_run:
                    # Use universal newlines for writing
                    with open(file_path, "w", encoding="utf-8", newline="\n") as file:
                        file.write(modified_content)
                self.files_modified += 1
                rprint(f"[green]✓[/green] Modified: {str(file_path)}")
            else:
                if self.verbose:
                    rprint(f"[blue]ℹ[/blue] No changes needed: {str(file_path)}")

            self.files_processed += 1
            return True

        except Exception as e:
            self.errors += 1
            rprint(f"[red]✗[/red] Error processing {str(file_path)}: {str(e)}")
            return False


def validate_paths(paths: List[Path], recursive: bool) -> List[Path]:
    """Validate and collect markdown files from given paths."""
    valid_files = []
    patterns = ["*.md", "*.markdown"]
    for path in paths:
        if path.is_file() and path.suffix.lower() in [".md", ".markdown"]:
            valid_files.append(path.resolve())
        elif path.is_dir():
            for pattern in patterns:
                glob_method = path.rglob if recursive else path.glob
                valid_files.extend(
                    p.resolve() for p in glob_method(pattern) if p.is_file()
                )
    return sorted(list(set(valid_files)))


@click.group()
@click.version_option(version=__version__)
def cli():
    """Markdown Equation Fixer - Fix mathematical equations in markdown files."""
    pass


@cli.command()
@click.argument("paths", type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes."
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option(
    "--recursive", "-r", is_flag=True, help="Process directories recursively."
)
def fix(paths: tuple, dry_run: bool, verbose: bool, recursive: bool):
    """Fix equations in markdown files."""
    try:
        fixer = EquationFixer(dry_run=dry_run, verbose=verbose)

        # Convert paths to Path objects
        path_objects = [Path(p) for p in paths]

        # Collect all valid markdown files
        markdown_files = validate_paths(path_objects, recursive=recursive)

        if not markdown_files:
            rprint(
                "[yellow]Warning:[/yellow] No markdown files found in specified paths."
            )
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing files...", total=len(markdown_files))

            for file_path in markdown_files:
                fixer.process_file(file_path)
                progress.update(task, advance=1)

        # Print summary
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"Files processed: {fixer.files_processed}")
        console.print(f"Files modified: {fixer.files_modified}")
        if fixer.errors > 0:
            console.print(f"[red]Errors encountered: {fixer.errors}[/red]")

        if dry_run:
            console.print(
                "\n[yellow]Note: This was a dry run. No files were modified.[/yellow]"
            )

    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.option(
    "--from-format",
    "-f",
    "from_fmt",
    type=click.Choice(["markdown", "gfm", "commonmark", "latex", "org", "docx"]),
    default="markdown",
    help="Input format (default: markdown)",
)
@click.option(
    "--to-format",
    "-t",
    "to_fmt",
    type=click.Choice(["markdown", "gfm", "commonmark", "latex", "org", "docx", "pdf"]),
    default="gfm",
    help="Output format (default: gfm)",
)
@click.option("--fix-equations", is_flag=True, help="Fix equations after conversion")
def convert(
    input_file: str, output_file: str, from_fmt: str, to_fmt: str, fix_equations: bool
):
    """Convert between different document formats while preserving equations.

    Supported formats: markdown, gfm (GitHub-Flavored Markdown),
    commonmark, latex, org, docx, pdf
    """
    try:
        # Check if pandoc is installed
        if not pypandoc.get_pandoc_version():
            rprint(
                "[red]Error:[/red] Pandoc is not installed. Please install pandoc first."
            )
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            progress.add_task("Converting document...", total=None)

            # Add extra arguments for better PDF/DOCX output
            extra_args = ["--wrap=none"]

            # Add specific arguments for PDF/DOCX output
            if to_fmt in ["pdf", "docx"]:
                extra_args.extend(
                    [
                        "--standalone",
                        "--variable",
                        "geometry:margin=1in",
                        "--variable",
                        "mainfont:Times New Roman",
                    ]
                )

            # Convert the document
            output = pypandoc.convert_file(
                input_file,
                to=to_fmt,
                format=from_fmt,
                outputfile=output_file,
                extra_args=extra_args,
            )

            if fix_equations and to_fmt in ["markdown", "gfm", "commonmark"]:
                # Fix equations in the converted file (only for markdown formats)
                fixer = EquationFixer(dry_run=False, verbose=False)
                fixer.process_file(Path(output_file))

            rprint(
                f"[green]✓[/green] Successfully converted {input_file} to {output_file}"
            )

    except Exception as e:
        rprint(f"[red]Error:[/red] Conversion failed: {str(e)}")
        logger.error(f"Conversion error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
