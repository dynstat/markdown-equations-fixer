import pytest
from pathlib import Path
from markdown_equations_fixer.cli import EquationFixer, validate_paths


@pytest.fixture
def fixer():
    """Returns an EquationFixer instance."""
    return EquationFixer(dry_run=False, verbose=True)


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory with sample markdown files for testing."""
    # Root files
    (tmp_path / "root.md").write_text(r"\[root_eq\]")
    (tmp_path / "file.txt").write_text("not a markdown file")

    # Subdirectory
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "sub.md").write_text(r"\[sub_eq\]")
    (sub_dir / "sub.markdown").write_text(r"\[sub_eq_2\]")

    return tmp_path


def test_fix_block_equations(fixer):
    """Test fixing block equations."""
    # Basic block equation
    assert fixer.fix_equations(r"\[E=mc^2\]") == "$$\nE=mc^2\n$$"
    # Multi-line block equation
    multi_line_input = r"\[\begin{aligned}\na &= b \\ c &= d\n\end{aligned}\]"
    multi_line_expected = "$$\n\\begin{aligned}\na &= b \\ c &= d\n\\end{aligned}\n$$"
    assert fixer.fix_equations(multi_line_input) == multi_line_expected


def test_fix_inline_equations(fixer):
    """Test fixing inline equations."""
    assert (
        fixer.fix_equations(r"inline \(E=mc^2\) equation") == "inline $E=mc^2$ equation"
    )


def test_fix_bracket_line_block(fixer):
    """Test fixing blocks where [ and ] are on their own lines."""
    input_text = "[\nE=mc^2\n]"
    expected = "$$\nE=mc^2\n$$"
    assert fixer.fix_equations(input_text) == expected


def test_fix_bracket_block_with_blank_lines_and_indent(fixer):
    """Blocks with extra blank lines and indentation should be converted."""
    input_text = (
        "\n[\n\n   Z₁ = XW₁ + b₁\n\n]\n\n"  # first block
        "[\n   A₁ = ReLU(Z₁)\n]\n\n"      # second block
        "[\n   Z₂ = A₁W₂ + b₂\n]\n\n"      # third block
        "[\n   \\hat{y} = Z₂\n]\n\n"       # fourth block
        "[\n   L = \\frac{1}{2m} \\sum (y - \\hat{y})^2\n]\n"  # fifth block
    )
    output = fixer.fix_equations(input_text)
    # Ensure each becomes a $$ block and inner content preserved sans surrounding blanks
    assert "$$\nZ₁ = XW₁ + b₁\n$$" in output
    assert "$$\nA₁ = ReLU(Z₁)\n$$" in output
    assert "$$\nZ₂ = A₁W₂ + b₂\n$$" in output
    assert "$$\n\\hat{y} = Z₂\n$$" in output
    assert "$$\nL = \\frac{1}{2m} \\sum (y - \\hat{y})^2\n$$" in output

def test_validate_paths_recursive(temp_dir):
    """Test recursive path validation."""
    paths = [temp_dir]
    valid_files = validate_paths(paths, recursive=True)
    assert len(valid_files) == 3
    assert temp_dir / "root.md" in valid_files
    assert temp_dir / "sub/sub.md" in valid_files
    assert temp_dir / "sub/sub.markdown" in valid_files


def test_validate_paths_non_recursive(temp_dir):
    """Test non-recursive path validation."""
    paths = [temp_dir]
    valid_files = validate_paths(paths, recursive=False)
    assert len(valid_files) == 1
    assert temp_dir / "root.md" in valid_files
    assert temp_dir / "sub/sub.md" not in valid_files


def test_process_file_error_handling(fixer):
    """Test error handling for a non-existent file."""
    invalid_path = Path("non_existent_file.md")
    result = fixer.process_file(invalid_path)
    assert not result
    assert fixer.errors == 1
