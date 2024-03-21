import os
import time
import shutil
import argparse
from multiprocessing.pool import ThreadPool

st = time.time()  # Time when the script was initially started

base_path = ""  # Base path which will be filled with user input from CLI
max_copy_threads = 8


def _copyfileobj_patched(fsrc, fdst, length=64 * 1024 * 1024):
    """Patches shutil method to hugely improve copy speed by increasing the copy buffer size to 64MB"""
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)


# Override internal shutil method with the optimized one
shutil.copyfileobj = _copyfileobj_patched


class MultithreadedCopier:
    """Class which utilises a thread pool to multithread copying of folder trees"""

    def __init__(self, max_threads):
        self.pool = ThreadPool(max_threads)

    def copy(self, source, dest):
        self.pool.apply_async(
            shutil.copy, args=(source, dest)
        )  # Repace shutil.copy with copy2 if metadata needs to be preserved

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()


def copytree_multithreaded(src_path, dest_path):
    """Method which wraps shutil.copytree with the multithreaded copier from above"""
    with MultithreadedCopier(
        max_threads=max_copy_threads
    ) as copier:  # max_threads could be a CLI arg
        shutil.copytree(src_path, dest_path, copy_function=copier.copy)


def main():
    """Main entry point"""
    # Initialize CLI argument parsing
    parser = argparse.ArgumentParser(
        description="Split a big folder into many small pieces while maintaining the folder structure."
    )
    parser.add_argument("path", type=str, help="The path of the folder to be split")
    parser.add_argument(
        "--output",
        type=str,
        help="The path where the split folder parts should be output. (Defaults to the current working directory if not specified)",
    )
    parser.add_argument(
        "--size",
        type=str,
        help="The maximum size of the parts to split into (Only numbers with no decimals accepted). Format: 2GB, 500MB, 10KB, 50B",
    )
    parser.add_argument(
        "--copy-threads",
        type=int,
        help="The number of threads to use when copying large file trees",
    )
    args = parser.parse_args()

    global max_copy_threads
    max_copy_threads = args.copy_threads or 8

    global base_path
    base_path = (
        os.path.abspath(args.path) if not os.path.isabs(args.path) else args.path
    )

    max_part_size = path_string_to_bytes(args.size) or 2147483648

    full_output_path = os.getcwd()
    if args.output:
        if not os.path.isdir(args.output):
            os.mkdir(args.output)
        full_output_path = (
            os.path.abspath(args.output)
            if not os.path.isabs(args.output)
            else args.output
        )

    print(
        "Starting to split folders... Please wait, this might take a long time depending on the folder size and amount of files."
    )
    split_folder(base_path, max_part_size, 1, output_path=full_output_path)

    et = time.time()
    elapsed_time = et - st
    print("Finished splitting in", elapsed_time, "seconds")


def set_base_path(path):
    global base_path
    base_path = path


def path_string_to_bytes(path_string: str):
    """Converts a string which is formatted like 2GB into bytes"""
    if path_string.endswith("GB"):
        return (
            int(path_string[:-2]) * 1024 * 1024 * 1024 - 10000
        )  # small adjustments to compensate file size calculation errors
    elif path_string.endswith("MB"):
        return int(path_string[:-2]) * 1024 * 1024 - 1000
    elif path_string.endswith("KB"):
        return int(path_string[:-2]) * 1024 - 100
    elif path_string.endswith("B"):
        return int(path_string[:-1])
    else:
        raise ValueError(f"Unknown size string: {path_string}")


def get_folder_size(path="."):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Skip if it is a symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def get_size_of_file_or_folder(path="."):
    return os.path.getsize(path) if os.path.isfile(path) else get_folder_size(path)


def sort_folder_content_by_size(path):
    """
    Sort all files of a folder by size
    Returns an array of dicts that consist of additional file information used for the splitting logic later on

    Params:
    - path: The full path of the folder to be sorted
    """
    files = os.listdir(path)
    files_with_info = []

    # For each file, make a dict with important info, and then sort all of those entries by size
    for file in files:
        full_path = f"{path}/{file}"
        file_info_dict = {
            "name": file,
            "full_path": full_path,
            "size": get_size_of_file_or_folder(full_path),
            "folder": os.path.isdir(full_path),
            "parent_folder": full_path.removeprefix(base_path).removesuffix(
                file
            ),  # parent folder structure: everything except main folder down to the file location
        }
        files_with_info.append(file_info_dict)

    sorted_files = sorted(files_with_info, key=lambda x: x["size"], reverse=True)

    return sorted_files


def split_folder(
    folder,
    max_size,
    part_number,
    subfolder=False,
    parent_folder=None,
    output_path=os.getcwd(),
):
    """
    Split a big folder of code into multiple parts of a maximum size.
    Recursive function with the same logic in the loop and slighly differing logic for init of the parent folder or subfolders.

    Params:
    - folder: The subfolder which is supposed to be split
    - max_size: The maximum size of a part folder in bytes
    - part_number: Param to pass the current part number the main method is working with
    - subfolder: Param to specify if this is the root folder or a subfolder (as init logic differs slightly)
    - parent_folder: Param to pass a parent folder if it exists (used for recursion, see below)
    - output_path: Param which can be passed by CLI to modify the path where the split parts are created (Defaults to current working directory if not set otherwise)
    """
    sorted_folder = (
        sort_folder_content_by_size(folder["full_path"])
        if subfolder
        else sort_folder_content_by_size(folder)
    )

    subfolder_extra = (
        f"{parent_folder}{folder['name']}/" if parent_folder is not None else ""
    )

    folder_path = (
        f"{output_path}/Part_{part_number}/{subfolder_extra}"
        if subfolder
        else f"{output_path}/Part_{part_number}"
    )

    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    for file in sorted_folder:
        if file["size"] > max_size:
            # If max size was reached, check if file is a folder or a file
            if file["folder"]:
                # If folder, recursively call this function on the folder
                part_number = split_folder(
                    folder=file,
                    max_size=max_size,
                    part_number=part_number,
                    parent_folder=file["parent_folder"],
                    output_path=output_path,
                    subfolder=True,
                )
                continue
            else:
                return print(
                    f"File exceeds max size and will not be split to maintain folder structure"
                )
        else:
            if file["folder"]:
                # If file is smaller than max size, keep moving files into a part until it is full
                if (
                    get_folder_size(f"{output_path}/Part_{part_number}") + file["size"]
                    < max_size
                ):
                    copytree_multithreaded(
                        file["full_path"],
                        f"{output_path}/Part_{part_number}/{subfolder_extra}/{file['name']}",
                    )
                else:
                    print("Creating a new part folder...")
                    # If part is full, create a new part folder and copy the file to it
                    part_number += 1
                    os.mkdir(f"{output_path}/Part_{part_number}")

                    copytree_multithreaded(
                        file["full_path"],
                        f"{output_path}/Part_{part_number}/{subfolder_extra}/{file['name']}",
                    )
            else:
                # If file is smaller than max size, keep moving files into a part until it is full
                if (
                    get_size_of_file_or_folder(f"{output_path}/Part_{part_number}")
                    + file["size"]
                    < max_size
                ):
                    shutil.copy(
                        file["full_path"],
                        f"{output_path}/Part_{part_number}/{subfolder_extra}/{file['name']}",
                    )
                else:
                    print("Creating a new part folder...")
                    # If part is full, create a new part folder and copy the file to it
                    part_number += 1
                    os.mkdir(f"{output_path}/Part_{part_number}")

                    shutil.copy(
                        file["full_path"],
                        f"{output_path}/Part_{part_number}/{subfolder_extra}/{file['name']}",
                    )

    return part_number


if __name__ == "__main__":
    main()
