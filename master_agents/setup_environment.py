import subprocess
import sys

def check_and_install_package(package_name_for_pip, package_name_for_import=None):
    """
    Checks if a package is installed and attempts to install it if not.
    Args:
        package_name_for_pip (str): The name of the package as used by pip (e.g., 'scikit-learn').
        package_name_for_import (str, optional): The name of the package as used in Python import
                                                 (e.g., 'sklearn'). Defaults to package_name_for_pip.
    Returns:
        bool: True if the package is available (or successfully installed), False otherwise.
    """
    if package_name_for_import is None:
        package_name_for_import = package_name_for_pip

    try:
        __import__(package_name_for_import)
        print(f"Package '{package_name_for_import}' (pip name: '{package_name_for_pip}') is already installed.")
        return True
    except ImportError:
        print(f"Package '{package_name_for_import}' (pip name: '{package_name_for_pip}') not found. Attempting to install...")
        try:
            # Use sys.executable to ensure pip installs into the current Python environment
            process = subprocess.run([sys.executable, '-m', 'pip', 'install', package_name_for_pip], capture_output=True, text=True, check=True)
            print(f"Successfully installed '{package_name_for_pip}'. Output:\n{process.stdout}")
            if process.stderr:
                print(f"Installation warnings/errors for '{package_name_for_pip}':\n{process.stderr}")
            # Verify installation by trying to import again
            try:
                __import__(package_name_for_import)
                return True
            except ImportError:
                print(f"Failed to re-import '{package_name_for_import}' after installation attempt.")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Failed to install '{package_name_for_pip}'. Command: {' '.join(e.cmd)}. Return Code: {e.returncode}.")
            print(f"Stdout:\n{e.stdout}\nStderr:\n{e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during installation of '{package_name_for_pip}': {e}")
            return False

# Define the packages identified from the ML engineer's plan
# Mapping: {Package Name for Display: (Package Name for pip, Package Name for import)}
required_ml_packages = {
    "NumPy": ("numpy", "numpy"),
    "Pandas": ("pandas", "pandas"),
    "Scikit-learn": ("scikit-learn", "sklearn"), # pip install scikit-learn, import sklearn
    "Matplotlib": ("matplotlib", "matplotlib"),
    "Seaborn": ("seaborn", "seaborn")
}

installation_results = {}

print("--- Starting Package Verification and Installation ---")

for display_name, (pip_name, import_name) in required_ml_packages.items():
    installation_results[display_name] = check_and_install_package(pip_name, import_name)
    print("-" * 50) # Separator for clarity

print("\n--- ML Environment Setup Status Report ---")
all_packages_ready = True
for display_name, is_ready in installation_results.items():
    if is_ready:
        print(f"[READY] {display_name}")
    else:
        print(f"[FAILED] {display_name} - Installation required but failed or could not be verified.")
        all_packages_ready = False

if all_packages_ready:
    print("\nAll identified ML packages are installed and ready for use.")
else:
    print("\nSome packages could not be installed or verified. Please review the logs above.")

print("--- End of Report ---")