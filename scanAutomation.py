# Author Aldo Leon (uig02071)
# Continental Corporation

#
#  TO RUN THIS SCRIPT: > scan -p ProjectName -v ProjectVersion -i ReqID(numbers only) -t FunctionalToken
#  The software to be scanned has to be located in the next path /usr/local/osrb/Workarea/*/SW
#  Also the Output directory will be created by itself.
#
#  The .txt output will be located in ~/leon/scan_commands
#

import os
import argparse
import re
import subprocess
from datetime import datetime

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
    parser.add_argument('-t', '--token', required=True, help='Functional Token from BlackDuckHub')
    args = parser.parse_args()
    
    path = os.getcwd()
    out_path = os.path.join(os.path.dirname(path), "Output")
    result = subprocess.run(["find . -type d -printf '%d\n' | sort -rn | head -1"], capture_output=True, text=True, shell=True)
    depth = result.stdout.strip()
    output_filename = f"ReqID_{args.id}_{args.name}_{args.version}_scan.txt"
    path_txt = os.path.join(os.path.dirname(path), "ScanCommand")
    detect_sh_cmd = "curl -k -L https://detect.synopsys.com/detect8.sh -o detect.sh && chmod +x detect.sh"
    
    validation = re.search("^/.*/Workarea/.*/SW$", path)
    
    if validation:
        try:
            subprocess.run(detect_sh_cmd, shell=True, check=True)
            blackduck_cmd = (
                f"./detect.sh --blackduck.url='https://blackduck.zone2.agileci.conti.de/' "
                f"--blackduck.api.token='{args.token}' "
                f"--detect.tools=SIGNATURE_SCAN,BINARY_SCAN "
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
                f"--detect.code.location.name='ReqID_{args.id}_{args.name}_{args.version}_slayer_src' "
                f"--detect.parallel.processors=8 "
                f"--detect.blackduck.signature.scanner.memory=60000"
            )
            
            # Format the command with new lines for every two spaces
            
            formatted_cmd = re.sub(r'--', ' \n --', blackduck_cmd)
            formatted_cmd = re.sub(r"--blackduck.api.token='.* ", '', formatted_cmd)

            with open(os.path.join(path_txt, output_filename), 'w') as file:
                file.write(f"Date of creation: ")
                file.write(str(datetime.now()) + '\n \n')
                file.write(f"Scan command used for {args.name}_{args.version}_ReqID-{args.id} \n \n")
                file.write(formatted_cmd)

            try:
                output = subprocess.check_output(blackduck_cmd, shell=True, stderr=subprocess.STDOUT)
                print(output.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.returncode}\n{e.output.decode('utf-8')}")
        except subprocess.CalledProcessError as e:
            print(f"Error detect.sh couldn't be downloaded: {e.returncode}\n{e.output.decode('utf-8')}")
            return
    else:
        print("Your software is not allocated in a safe path to be scanned. Please ensure that you are in the following path '/usr/local/osrb/Workarea' and the directory to be scanned is 'SW/', example: /usr/local/osrb/Workarea/AM/ALH120397/SW/")

if __name__ == "__main__":
    main()
