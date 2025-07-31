import os
import shutil
import json
import time

def list_immediate_directories_os(path):
    """
    Lists all immediate subdirectories within the given path using os.scandir().
    """
    with os.scandir(path) as entries:
        return [entry for entry in entries if entry.is_dir()]

def make_link(text, url):
    return f'`{text} <{url}>`_'

def generate_index_page(static_directories, sku_info, version_info):
    rst_string = f"{version_info} - {sku_info}"
    rst_string += f"\n" + (len(rst_string) * "=")

    for dir_ in static_directories:
        rst_string += "\n" + make_link(dir_.name, f"../../_static/{sku_info}/{version_info}/{dir_.name}/index.html")

    return rst_string

if __name__ == "__main__":

    # paths for output
    docs_dir = './documentation/versioned_docs'
    static_dir = f"{docs_dir}/_static"
    output_dir = f"{docs_dir}/rst"

    # path for input
    temp_dir_path = "./tmp"

    # metadata
    sku_info = "ADF"
    version_info = f"AIA_2506_{time.time()}"

    # identify all dirs to copy
    static_subdirs = list_immediate_directories_os(temp_dir_path)

    # create subdir for static assets
    try:
        os.mkdir(f'{static_dir}/{sku_info}')
    except:
        pass
    try:
        os.mkdir(f'{static_dir}/{sku_info}/{version_info}')
    except:
        pass

    for subdir in static_subdirs:
        shutil.copytree(
            f"{temp_dir_path}/{subdir.name}",
            f"{static_dir}/{sku_info}/{version_info}/{subdir.name}"
        )

    index_rst = generate_index_page(static_subdirs, sku_info, version_info)

    with open(output_dir + "/gen_docs.rst", mode="w+") as f:
        f.write(index_rst)

    with open(output_dir + "/metadata.json", mode="w+") as f:
        json.dump(
            {
                'sku': sku_info,
                'version': version_info
            },
            f
        )