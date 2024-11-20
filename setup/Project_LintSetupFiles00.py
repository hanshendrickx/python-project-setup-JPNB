import os
import subprocess
import sys
from pathlib import Path

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode('utf-8'))
        sys.exit(1)
    return output.decode('utf-8')

def check_prerequisites():
    print("Checking prerequisites...")
    result = run_command("check_prerequisites.bat")
    print(result)

def install_global_packages():
    print("Installing required global packages...")
    run_command("pip install -U pip")
    run_command("pip install virtualenv")

def create_project_structure(project_name):
    print(f"Creating project structure for {project_name}...")
    project_dir = Path(project_name)
    project_dir.mkdir(exist_ok=True)
    (project_dir / "src").mkdir(exist_ok=True)
    (project_dir / "tests").mkdir(exist_ok=True)
    (project_dir / "docs").mkdir(exist_ok=True)
    return project_dir

def create_virtual_environment(project_dir):
    print("Creating virtual environment...")
    venv_dir = project_dir / "venv"
    run_command(f"virtualenv {venv_dir}")
    return venv_dir

def install_project_packages(venv_dir):
    print("Installing project packages...")
    pip = venv_dir / "Scripts" / "pip"
    run_command(f"{pip} install jupyterlab numpy pandas matplotlib seaborn scikit-learn pytest black ruff")

def setup_linting_and_formatting(project_dir):
    print("Setting up linting and formatting...")
    pyproject_toml = project_dir / "pyproject.toml"
    with open(pyproject_toml, "w") as f:
        f.write("""
[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N"]
ignore = []
fixable = ["A", "B", "C", "D", "E", "F", "G", "I", "N", "Q", "S", "T", "W", "ANN", "ARG", "BLE", "COM", "DJ", "DTZ", "EM", "ERA", "EXE", "FBT", "ICN", "INP", "ISC", "NPY", "PD", "PGH", "PIE", "PL", "PT", "PTH", "PYI", "RET", "RSE", "RUF", "SIM", "SLF", "TCH", "TID", "TRY", "UP", "YTT"]
unfixable = []
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]
per-file-ignores = {}
""")

def create_sample_files(project_dir):
    print("Creating sample files...")
    src_dir = project_dir / "src"
    tests_dir = project_dir / "tests"

    # Create main.py
    with open(src_dir / "main.py", "w") as f:
        f.write("""
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))
""")

    # Create test_main.py
    with open(tests_dir / "test_main.py", "w") as f:
        f.write("""
import pytest
from src.main import greet

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
""")

def main():
    project_name = input("Enter project name: ")
    
    check_prerequisites()
    install_global_packages()
    project_dir = create_project_structure(project_name)
    venv_dir = create_virtual_environment(project_dir)
    install_project_packages(venv_dir)
    setup_linting_and_formatting(project_dir)
    create_sample_files(project_dir)

    print(f"\nProject '{project_name}' has been set up successfully!")
    print("To activate the virtual environment, run:")
    print(f"    {venv_dir}\\Scripts\\activate")
    print("\nTo run the sample script:")
    print(f"    python {project_name}\\src\\main.py")
    print("\nTo run tests:")
    print(f"    pytest {project_name}\\tests")

if __name__ == "__main__":
    main()