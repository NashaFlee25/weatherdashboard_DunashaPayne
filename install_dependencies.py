"""Install required dependencies for Weather Dashboard."""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    """Install all required dependencies."""
    print("Installing Weather Dashboard dependencies...")
    print("=" * 50)
    
    # Required packages
    packages = [
        "aiohttp>=3.8.0",
        "requests>=2.28.0",
        "pillow>=9.0.0",
        "matplotlib>=3.5.0",
        "numpy>=1.21.0"
    ]
    
    failed_packages = []
    
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 50)
    if failed_packages:
        print("Some packages failed to install:")
        for package in failed_packages:
            print(f"  - {package}")
        print("\nTry installing them manually using:")
        print("pip install " + " ".join(failed_packages))
    else:
        print("All dependencies installed successfully!")
        print("You can now run the Weather Dashboard with: python src/main.py")

if __name__ == "__main__":
    main()
