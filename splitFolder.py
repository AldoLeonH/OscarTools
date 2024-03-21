# Author Aldo Leon (uig02071)
# Continental Corporation

import os
import subprocess

def split():
    path = os.getcwd()
    print("Current directory:", path)
    path_splitter= os.path.abspath(__file__)
    path_splitter= os.path.join(os.path.dirname(path_splitter), "splitter.py")
    size=1
    if size:
        print("Initiating splitting process.")
        subprocess.run(["python3", path_splitter, path, "--output",  os.path.dirname(path)+"/SW", "--size", "2GB"])
        part=1        
    else:
        subprocess.run(["mv", path,  os.path.dirname(path)+"/SW"])
        subprocess.run(["mkdir", path,  os.path.dirname(path)+"/Output"])
        print("Split done")
    target= os.path.dirname(path)+"/SW"
    return target 

def main():
    path= split()
    out=(path)
    print(out)

if __name__ == "__main__":
    main()

