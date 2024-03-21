# Author Aldo Leon (uig02071)
# Continental Corporation

import os
import argparse
import re
import subprocess

def main():
    '''The main function executes a shell command to scan in BlackDuckHub with specified project details
    and saves the command output to a text file.
    
    Returns
    -------
        The `main()` function does not explicitly return any value. If the function completes successfully,
    it will implicitly return `None`.
    
    '''
    parser = argparse.ArgumentParser(description='Execute shell command to scan in BlackDuckHub')
    parser.add_argument('-p', '--name', required=True, help='Project_Name')
    parser.add_argument('-v', '--version', required=True, help='Project_Version')
    parser.add_argument('-i', '--id', required=True, help='id')
    parser.add_argument('-m', '--multiPart', required=False, help='multiPart')
    args = parser.parse_args()
    path= os.getcwd()
    token=os.environ["TOKEN"]
    out_path = os.path.join(os.path.dirname(path), "Output")
    result = subprocess.run(["find . -type d -printf '%d\n' | sort -rn | head -1"], capture_output=True, text=True, shell=True)
    depth = result.stdout.strip()
    output_filename = f"ReqID_{args.id}_{args.name}_{args.version}_scan.txt"
    path_txt = "/mnt/c/Users/uig02071/Desktop/Scan_WSL/"
    detect_sh_cmd = "curl -k -L https://detect.synopsys.com/detect8.sh -o detect.sh && chmod +x detect.sh"
    validation = re.search("^/.*/Workarea/.*/SW$", path)
    if validation:
        try:
            subprocess.run(detect_sh_cmd, shell=True, check=True)                        
            blackduck_cmd = (
                f"./detect.sh "
                f"--blackduck.url='https://blackduck-ccif.cmo.conti.de/' "
                f"--blackduck.api.token={token}  "
                f"--detect.tools=SIGNATURE_SCAN "
                f"--detect.detector.search.depth='{depth}' "
                f"--detect.source.path='{path}' "
                f"--detect.scan.output.path='{out_path}' "
                f"--detect.project.name='{args.name}' "
                f"--detect.project.version.name='ReqID-{args.id}_{args.version}' "
                f"--blackduck.trust.cert=true "
                f"--detect.project.level.adjustments=false "
                f"--detect.blackduck.signature.scanner.upload.source.mode=true "
                f"--detect.blackduck.signature.scanner.license.search=true "
                f"--detect.blackduck.signature.scanner.individual.file.matching=ALL "
                f"--detect.blackduck.signature.scanner.snippet.matching=SNIPPET_MATCHING "
                f"--detect.blackduck.signature.scanner.copyright.search=true "
                f"--detect.code.location.name='ReqID_{args.id}_{args.name}_{args.version}_slayer_src_Part_1' " #This need to be counted by itself
                f"--detect.parallel.processors=4 "
                f"--detect.blackduck.signature.scanner.memory=60000"
            )
            with open(os.path.join(path_txt, output_filename), 'w') as file:
                file.write(blackduck_cmd)
            try:
                output = subprocess.check_output(blackduck_cmd, shell=True, stderr=subprocess.STDOUT)
                print(output.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.returncode}\n{e.output.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            print(f"Error detect.sh coulnd't be downloaded: {e.returncode}\n{e.output.decode('utf-8')}")
            return
    else:
        print("Your software is not allocated in a safe path to be scanned please ensure that you are in the following path '/usr/local/osrb/Workarea' and the directory to be scanned is 'SW/', example /usr/local/osrb/Workarea/AM/ALH120397/SW/")



if __name__ == "__main__":
    main()
