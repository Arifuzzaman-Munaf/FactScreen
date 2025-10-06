import os
import subprocess
import sys


def create_virtual_environment():
    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("Virtual environment created successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False


def install_requirements():
    print("Installing required packages...")
    try:
        # Use pip from virtual environment
        if os.name == 'nt':  # Windows
            pip_path = os.path.join("venv", "Scripts", "pip")
        else:  # Unix/Linux/macOS
            pip_path = os.path.join("venv", "bin", "pip")
        
        subprocess.check_call([pip_path, "install", "-r", "requirements.txt", "-q"])
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False



def main():
    print("Starting System Setup")
    print("-" * 50)
    
    # Create virtual environment
    if not create_virtual_environment():
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    print("\nSetup completed successfully!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())