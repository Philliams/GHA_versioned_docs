import zipfile
import pathlib
import shutil

if __name__ == "__main__":
    archives = list(pathlib.Path('./download').glob('*.zip'))
    for zip_file_path in archives:
        extract_path = f"./download/{zip_file_path.stem}/"
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        shutil.copytree(
            f"{extract_path}_static",
            "./documentation/combined_docs/source/_static",
            dirs_exist_ok=True
        )

        shutil.copytree(
            f"{extract_path}rst",
            f"./documentation/combined_docs/source/{zip_file_path.stem}/rst",
            dirs_exist_ok=False
        )