import os
import sys
import tempfile
import zipfile


def setup_lib_path():
    """Takes the local dependencies and moves them out of the apworld zip file to a temporary directory so the DLLs can be loaded."""
    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "lib")

    # Check if the script is running from a zip archive
    # check if base_path has .apworld in it
    if ".apworld" in __file__:
        print("apworld")
        # Find the actual zip file path
        zip_file_path = __file__
        while not zip_file_path.lower().endswith('.apworld'):
            zip_file_path = os.path.dirname(zip_file_path)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            # Extract the lib folder to the temporary directory
            lib_folder_path = "metroidprime/lib/"
            for member in zip_ref.namelist():
                if member.startswith(lib_folder_path):
                    zip_ref.extract(member, temp_dir)
            # Calculate the path to the extracted lib folder
            temp_lib_path = os.path.join(temp_dir, lib_folder_path)
            # Add the temporary lib path to sys.path
            sys.path.append(temp_lib_path)
            print(f"lib folder extracted to temporary directory and added to path: {temp_lib_path}")
            return temp_lib_path
    else:
        print("local")
        # If not running from a zip, just add the existing lib path to sys.path
        sys.path.append(lib_path)
        print(f"lib folder added to path: {lib_path}")
        return lib_path
