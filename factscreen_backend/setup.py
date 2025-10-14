import os
import subprocess
import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # For Python 3.9/3.10, requires 'tomli' package

def create_virtual_environment():
    """
    Create a Python virtual environment in the 'venv' directory using --upgrade-deps.
    Returns:
        bool: True if the environment was created successfully, False otherwise.
    """
    print("Creating virtual environment...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "venv", "--upgrade-deps", "venv"
        ])
        print("Virtual environment created successfully! Run `source venv/bin/activate` to activate the environment.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_dependencies():
    """
    Install project dependencies as specified in pyproject.toml into the virtual environment.
    Returns:
        bool: True if dependencies were installed successfully, False otherwise.
    """
    print("Installing project dependencies from pyproject.toml...")
    try:
        if os.name == 'nt':  # Windows
            pip_path = os.path.join("venv", "Scripts", "pip")
            python_path = os.path.join("venv", "Scripts", "python")
        else:  # Unix/Linux/macOS
            pip_path = os.path.join("venv", "bin", "pip")
            python_path = os.path.join("venv", "bin", "python")

        # Upgrade pip, setuptools, and wheel to the latest versions
        subprocess.check_call([
            pip_path, "install", "-U", "pip", "setuptools", "wheel", "-q", "--disable-pip-version-check"
        ])

        pyproject_path = Path("pyproject.toml")
        if not pyproject_path.exists():
            print("pyproject.toml not found; nothing to install.")
            return True

        # Parse dependencies from pyproject.toml
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)

        deps = list(data.get("project", {}).get("dependencies", []) or [])

        if deps:
            cmd = [pip_path, "install", "-q", "--disable-pip-version-check", *deps]
            subprocess.check_call(cmd)
            print("Dependencies installed successfully from pyproject.toml!")
        else:
            print("No dependencies listed in pyproject.toml.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies from pyproject.toml: {e}")
        return False

def main():
    print("Starting System Setup")
    print("-" * 50)

    if not create_virtual_environment():
        return 1

    if not install_dependencies():
        return 1

    print("\nSetup completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())