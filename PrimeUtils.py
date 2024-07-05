import os
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
        zip_file_path = __file__
        while not zip_file_path.lower().endswith('.apworld'):
            zip_file_path = os.path.dirname(zip_file_path)

        # Cleanup step: Attempt to remove any other metroidprime_temp_lib_ folders not in use
        temp_base_dir = tempfile.gettempdir()
        old_temp_dirs = glob.glob(os.path.join(temp_base_dir, "metroidprime_temp_lib_*"))
        for dir_path in old_temp_dirs:
            try:
                shutil.rmtree(dir_path)
                print(f"Removed old temporary directory: {dir_path}")
            except Exception as e:
                print(f"Could not remove {dir_path}: {e}")

        # Use tempfile.mkdtemp to create a new temporary directory with a prefix
        temp_dir_path = tempfile.mkdtemp(prefix="ap_metroidprime_temp_lib_")

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            lib_folder_path = "metroidprime/lib/"
            for member in zip_ref.namelist():
                if member.startswith(lib_folder_path):
                    zip_ref.extract(member, temp_dir_path)
            temp_lib_path = os.path.join(temp_dir_path, lib_folder_path)
            sys.path.append(temp_lib_path)
            print(f"lib folder extracted to temporary directory and added to path: {temp_lib_path}")
            return temp_lib_path
    else:
        sys.path.append(lib_path)
        return lib_path