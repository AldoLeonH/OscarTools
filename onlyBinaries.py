# Author Aldo Leon (uig02071)
# Continental Corporation
#
# The inability to view DLL files, EXE files or any applicable content within our compliance tool called BlackDuckHub posed a challenge. 
#
# As a solution, a script was developed to facilitate the visualization of metadata for each binary file 
# contained within a folder. 
#
# This implies that the script must be recursive to access all the information.
"""
    The script recursively processes binary files in a directory, executes a PowerShell command on them,
    and saves the results in a text file along with a summary.
    
    :param file_path: The `file_path` parameter represents the path to a specific file that is being
    processed within the script. This path is used to perform various operations on the file, such as
    checking if it is a binary file, extracting metadata using PowerShell commands, and writing the
    results to an output file
    :return: The script is returning the results of executing a PowerShell command on binary files found
    in a specified directory. The script processes each binary file, checks if it is a binary file, and
    then runs a PowerShell command on it to gather specific information. The results are then written to
    an output file. Additionally, a summary of the processed files and their extensions is written at
    the beginning of the output file.
"""
import subprocess
import argparse
import os
from pathlib import Path
import mimetypes

# This function helps to verify the file type

def is_binary(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('application')


def run_powershell_command(path):

    powershell_command = f'Get-Command "{path}" | Format-List'
    result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
    output_lines = result.stdout.split('\n')

    # State to check if the current file meets the condition as default
    skip_file = False

    # Filter lines and check for specific condition if Product and ProductVersion are void the file will be skipped 
    filtered_lines = []
    for line in output_lines:
        line = line.strip()
        if line != '' and ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            
            # Check the condition
            if key == 'Product' and value == '' and key == 'ProductVersion' and value == '':
                skip_file = True
            
            # Add that information file
            filtered_lines.append(line)

    return '\n'.join(filtered_lines) if not skip_file else ''





def process_directory(directory, output_dir, name, version):
    file_count = 0
    extensions = set()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_count += 1
            extensions.add(Path(file).suffix)

            file_path = os.path.join(root, file)

            if is_binary(file_path):
                folder_name = os.path.basename(root)
                output_file_name = f"{name}_{version}_results_binaries_MD.txt"
                output_file_path = output_dir / output_file_name

                with open(output_file_path, 'a') as output:
                    output.write(f"Results for: {file_path}\n")
                    output.write(run_powershell_command(file_path))
                    output.write('\n' + '-'*50 + '\n')

    # Write summary at the beginning of the file
    summary = f"Summary: Processed {file_count} files with extensions: {', '.join(extensions)}\n\n"
    with open(output_file_path, 'r+') as output:
        content = output.read()
        output.seek(0, 0)
        output.write(summary + content)

def main():
    parser = argparse.ArgumentParser(description='Execute PowerShell command on binary files recursively.')
    parser.add_argument('directory', help='Directory containing binary files.')
    parser.add_argument('-p', '--name', required=True, help='Porject_Name')
    parser.add_argument('-v', '--version', required=True, help='Project_Version')
    parser.add_argument('--output', default=None, help='Output folder for results.')
    args = parser.parse_args()

    # if you do not specify the output path the output_dir will be created in the same location of this scrypt and the .txt file inside of that directory. 
    # It will located like this:
    # .|onlyBinaries.py
    #  |-OutputBinariesMetadata (Dir)
    #  | |output_file.txt
    #  |
    if args.output is None:
        scrypt_path = Path(__file__).parent
        output_dir = scrypt_path / "OutputBinariesMetadata"
        output_dir.mkdir(exist_ok=True)
    else:
        output_dir = Path(args.output)
    process_directory(args.directory, output_dir, args.name, args.version)
    

if __name__ == "__main__":
    main()
