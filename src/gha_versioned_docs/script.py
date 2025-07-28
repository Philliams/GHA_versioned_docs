import zipfile
import glob
import pathlib

if __name__ == "__main__":
    archives = list(pathlib.Path('./download').glob('*.zip'))
    for zip_file_path in archives:
        extract_path = f"./download/{zip_file_path.stem}/"
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)