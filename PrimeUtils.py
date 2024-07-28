import os
import pkgutil
import platform
import sys
import shutil
import tempfile
import zipfile
import glob


def setup_lib_path():
    """Takes the local dependencies and moves them out of the apworld zip file to a temporary directory so the DLLs can be loaded."""
    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "lib")

    if ".apworld" in __file__:
        print("Extracting library files from metroidprime.apworld ")
        zip_file_path = __file__
        while not zip_file_path.lower().endswith('.apworld'):
            zip_file_path = os.path.dirname(zip_file_path)
        lib_folder_path = get_lib_folder_path()
        version = get_apworld_version()
        print("Using metroidprime.apworld version: ", version)
        temp_dir_name = "ap_metroidprime_temp_lib"
        target_dir_name = f"{temp_dir_name}_{version}"
        temp_base_dir = tempfile.gettempdir()
        target_dir_path = os.path.join(temp_base_dir, target_dir_name)

        # Check if the exact version directory exists
        if os.path.exists(target_dir_path):
            print(f"Using existing directory for version {version}: {target_dir_path}")
        else:
            # Remove other version directories
            try:
                for dir in glob.glob(os.path.join(temp_base_dir, f"{temp_dir_name}_*")):
                    if dir != target_dir_path:
                        shutil.rmtree(dir)
                        print(f"Removed old version directory: {dir}")
            except Exception as e:
                print(f"Failed to remove old version directories, make sure you don't have any archipelago clients/generators already running if you want these removed: {e}")

            # Extract files to the new version directory
            os.makedirs(target_dir_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member.startswith(lib_folder_path):
                        zip_ref.extract(member, target_dir_path)
                print(f"Library files extracted to: {target_dir_path}")

        # Add the library path to sys.path
        temp_lib_path = os.path.join(target_dir_path, lib_folder_path)
        if temp_lib_path not in sys.path:
            sys.path.append(temp_lib_path)
            print(f"Library folder added to path: {temp_lib_path}")

        return temp_lib_path
    else:
        print("Using local lib folder")
        if lib_path not in sys.path:
            sys.path.append(lib_path)
        print(f"lib folder added to path: {lib_path}")
        return lib_path


def get_apworld_version():
    # Get version from ./version.txt
    # detect if on windows since pathing is handled differently from linux
    if platform.system() == "Windows":
        path = os.path.join(os.path.dirname(__file__), "version.txt")
    else:
        path = "version.txt"
    version = pkgutil.get_data(__name__, path).decode().strip()
    return version


def get_lib_folder_path():
    # Get version from ./version.txt
    # detect if on windows since pathing is handled differently from linux
    if platform.system() == "Windows":
        lib_folder_path = "metroidprime/lib"
    else:
        lib_folder_path = os.path.join("metroidprime", "lib")
    return lib_folder_path
