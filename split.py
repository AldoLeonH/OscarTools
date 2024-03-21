import os
import shutil
import argparse
import threading

class FolderSplitter:
    def __init__(self, source_path, output_path, max_part_size, num_threads):
        self.source_path = source_path
        self.output_path = output_path
        self.max_part_size = max_part_size
        self.num_threads = num_threads

    def split_folder(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.split_recursive(self.source_path, self.output_path)

    def split_recursive(self, source_folder, output_folder):
        files = [f for f in os.listdir(source_folder)]
        files.sort(key=lambda x: os.path.getsize(os.path.join(source_folder, x)), reverse=True)

        current_part_size = 0
        part_number = 1
        part_folder = os.path.join(output_folder, f"part{part_number}")
        os.makedirs(part_folder)

        for file in files:
            file_path = os.path.join(source_folder, file)
            file_size = os.path.getsize(file_path)
            
            if current_part_size + file_size > self.max_part_size:
                part_number += 1
                part_folder = os.path.join(output_folder, f"part{part_number}")
                os.makedirs(part_folder)
                current_part_size = 0
            
            shutil.copy(file_path, os.path.join(part_folder, file))
            current_part_size += file_size

        subfolders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]
        for folder in subfolders:
            self.split_recursive(os.path.join(source_folder, folder), os.path.join(output_folder, folder))

def split_folder(source_path, output_path=None, max_part_size=50 * 1024 * 1024, num_threads=1):
    if output_path is None:
        output_path = os.path.join(source_path, "output")

    splitter = FolderSplitter(source_path, output_path, max_part_size, num_threads)
    splitter.split_folder()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a folder into smaller pieces while keeping the folder structure intact.")
    parser.add_argument("source_path", help="Path to the source folder to split")
    parser.add_argument("--output_path", help="Custom output path for the split parts (default: ./output)")
    parser.add_argument("--max_part_size", type=int, default=50 * 1024 * 1024, help="Maximum size of each split part in bytes (default: 50MB)")
    parser.add_argument("--num_threads", type=int, default=1, help="Number of threads to use for copying (default: 1)")
    args = parser.parse_args()

    split_folder(args.source_path, args.output_path, args.max_part_size, args.num_threads)
