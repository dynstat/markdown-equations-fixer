import click
import sys
from pathlib import Path
import re
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from typing import Optional, List
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
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
            # Pattern to match equations that start with \[ and end with \]
            equation_pattern = r'\\\[(.*?)\\\]'
            
            # Function to replace matches with properly formatted equations
            def replace_equation(match):
                equation = match.group(1).strip()
                return f'$$\n{equation}\n$$'
            
            # Replace \[ ... \] equations
            content = re.sub(equation_pattern, replace_equation, content, flags=re.DOTALL)
            
            # Pattern to match single-line equations with single \[ and \]
            single_line_pattern = r'\\(\[|\])'
            content = re.sub(single_line_pattern, '$$', content)
            
            # Fix cases where multiple $$ appear consecutively
            content = re.sub(r'\${2,}', '$$', content)
            
            # Ensure proper spacing around equation blocks
            content = re.sub(r'(\$\$)\s*(\S)', r'\1\n\2', content)
            content = re.sub(r'(\S)\s*(\$\$)', r'\1\n\2', content)
            
            return content
        except Exception as e:
            logger.error(f"Error fixing equations: {str(e)}")
            raise

    def process_file(self, file_path: Path) -> bool:
        """Process a single markdown file."""
        try:
            if self.verbose:
                logger.info(f"Processing {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            modified_content = self.fix_equations(content)
            
            if content != modified_content:
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(modified_content)
                self.files_modified += 1
                rprint(f"[green]✓[/green] Modified: {file_path}")
            else:
                if self.verbose:
                    rprint(f"[blue]ℹ[/blue] No changes needed: {file_path}")

            self.files_processed += 1
            return True

        except Exception as e:
            self.errors += 1
            rprint(f"[red]✗[/red] Error processing {file_path}: {str(e)}")
            return False

def validate_paths(paths: List[Path]) -> List[Path]:
    """Validate and collect markdown files from given paths."""
    valid_files = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in ['.md', '.markdown']:
            valid_files.append(path)
        elif path.is_dir():
            valid_files.extend(
                p for p in path.rglob('*.md') if p.is_file()
            )
            valid_files.extend(
                p for p in path.rglob('*.markdown') if p.is_file()
            )
    return valid_files

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Markdown Equation Fixer - Fix mathematical equations in markdown files."""
    pass

@cli.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1, required=True)
@click.option('--dry-run', is_flag=True, help="Show what would be done without making changes.")
@click.option('--verbose', '-v', is_flag=True, help="Enable verbose output.")
@click.option('--recursive', '-r', is_flag=True, help="Process directories recursively.")
def fix(paths: tuple, dry_run: bool, verbose: bool, recursive: bool):
    """Fix equations in markdown files."""
    try:
        fixer = EquationFixer(dry_run=dry_run, verbose=verbose)
        
        # Convert paths to Path objects
        path_objects = [Path(p) for p in paths]
        
        # Collect all valid markdown files
        markdown_files = validate_paths(path_objects)
        
        if not markdown_files:
            rprint("[yellow]Warning:[/yellow] No markdown files found in specified paths.")
            sys.exit(1)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                "Processing files...", 
                total=len(markdown_files)
            )

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
            console.print("\n[yellow]Note: This was a dry run. No files were modified.[/yellow]")

    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        sys.exit(1)

@cli.command()
def version():
    """Show the version information."""
    click.echo("Markdown Equation Fixer v1.0.0")

if __name__ == '__main__':
    cli()
