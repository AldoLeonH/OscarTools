# Author Aldo Leon (uig02071)
# Continental Corporation

import argparse
import subprocess
import os
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser(description='Execute shell command to scan in BlackDuckHub')
    parser.add_argument('directory', help='Path to be scanned')
    parser.add_argument('-p', '--name', required=True, help='Project_Name')
    parser.add_argument('-v', '--version', required=True, help='Project_Version')
    parser.add_argument('-o', '--output', required=True , help='Output folder for results.')
    args = parser.parse_args()
    output_folder = os.path.join(args.directory, 'Output')
    os.makedirs(output_folder, exist_ok=True)
    subprocess.run(["chmod 777 -R ."], capture_output=True, text=True, shell=True)
    result = subprocess.run(["find . -type d -printf '%d\n' | sort -rn | head -1"], capture_output=True, text=True, shell=True)
    deepest_depth = result.stdout.strip()
    # print(deepest_depth)
    # blackduck_cmd = f"curl -k -L https://detect.synopsys.com/detect8.sh -o detect.sh && bash detect.sh --blackduck.url='https://blackduck-ccif.cmo.conti.de/' --blackduck.api.token='Y2MyY2QwNjgtZTJkYS00M2NmLThiOTEtN2FiMjlkMGY1Y2VhOmE0MzQyMWE1LTI0MzMtNGEwNy05NmU2LWRhNTlhNjc3YTcyOA==' --detect.tools=SIGNATURE_SCAN --detect.detector.search.depth=12 --detect.source.path='/mnt/c/Users/uig02071/Documents/RAD6XX_SW_Packages-13-11-23/RAD6XX_SW_Packages-13-11-23' --detect.scan.output.path='/mnt/c/Users/uig02071/Documents/RAD6XX_SW_Packages-13-11-23/Output' --detect.project.name='test_Aldo_Leon' --detect.project.version.name='Test_1' --blackduck.trust.cert=true --detect.project.level.adjustments=false --detect.blackduck.signature.scanner.upload.souce.mode=true --detect.blackduck.signature.scanner.license.search=true --detect.blackduck.signature.scanner.individual.file.matching=ALL --detect.blackduck.signature.scanner.snippet.matching=SNIPPET_MATCHING --detect.blackduck.signature.scanner.copyright.search=true --detect.code.location.name=Aldo_test_Python_slayer_src --detect.parallel.processors=4 --detect.blackduck.signature.scanner.memory=60000"
    blackduck_cmd = (
    f"curl -k -L https://detect.synopsys.com/detect8.sh -o detect.sh && "
    f"bash detect.sh --blackduck.url='https://blackduck-ccif.cmo.conti.de/' "
    f"--blackduck.api.token='Y2MyY2QwNjgtZTJkYS00M2NmLThiOTEtN2FiMjlkMGY1Y2VhOmE0MzQyMWE1LTI0MzMtNGEwNy05NmU2LWRhNTlhNjc3YTcyOA==' "
    f"--detect.tools=SIGNATURE_SCAN --detect.detector.search.depth='{deepest_depth}' "
    f"--detect.source.path='{args.directory}' --detect.scan.output.path='{args.output}' "
    f"--detect.project.name='{args.name}' --detect.project.version.name='{args.version}' "
    f"--blackduck.trust.cert=true --detect.project.level.adjustments=false "
    f"--detect.blackduck.signature.scanner.upload.souce.mode=true "
    f"--detect.blackduck.signature.scanner.license.search=true "
    f"--detect.blackduck.signature.scanner.individual.file.matching=ALL "
    f"--detect.blackduck.signature.scanner.snippet.matching=SNIPPET_MATCHING "
    f"--detect.blackduck.signature.scanner.copyright.search=true "
    f"--detect.code.location.name='Algo_x_y_SRC' --detect.parallel.processors=4 "
    f"--detect.blackduck.signature.scanner.memory=60000"
    )
    print(blackduck_cmd)
    try:
        output = subprocess.check_output(blackduck_cmd, shell=True, stderr=subprocess.STDOUT)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}\n{e.output.decode('utf-8')}")
if __name__ == "__main__":
    main()


