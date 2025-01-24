import pytest
from pathlib import Path
from markdown_equations_fixer.cli import EquationFixer, validate_paths


def test_equation_fixer():
    # Test basic equation fixing
    fixer = EquationFixer(dry_run=False, verbose=True)

    # Test case 1: Basic equation
    input_text = r"\[E = mc^2\]"
    expected = "$$\nE = mc^2\n$$"
    assert fixer.fix_equations(input_text) == expected

    # Test case 2: Multi-line equation
    input_text = r"\[\begin{align}f(x) &= x^2\end{align}\]"
    expected = "$$\n\\begin{align}f(x) &= x^2\\end{align}\n$$"
    assert fixer.fix_equations(input_text) == expected

    # Test case 3: Multiple equations
    input_text = r"\[f(x)\]\[g(x)\]"
    expected = "$$\nf(x)\n$$\ng(x)\n$$"
    assert fixer.fix_equations(input_text) == expected


def test_path_validation(tmp_path):
    # Create temporary test files
    md_file = tmp_path / "test.md"
    markdown_file = tmp_path / "test.markdown"
    txt_file = tmp_path / "test.txt"

    md_file.write_text("test")
    markdown_file.write_text("test")
    txt_file.write_text("test")

    # Test path validation
    paths = [tmp_path]
    valid_files = validate_paths(paths)

    assert len(valid_files) == 2
    assert any(str(f).endswith(".md") for f in valid_files)
    assert any(str(f).endswith(".markdown") for f in valid_files)


def test_error_handling():
    fixer = EquationFixer(dry_run=False, verbose=True)

    # Test invalid file handling
    result = fixer.process_file(Path("nonexistent_file.md"))
    assert result == False
    assert fixer.errors == 1
