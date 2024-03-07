# OSCAR Reviewers Tools

This repository contains useful scripts that could help us at the time to perform our daily work as reviewers.
This script only works on Linux environment, you could set an alias to call this script with a simple command. this could be called "Scan".

## Installation

```bash
git clone https://github.com/AldoLeonH/OscarTools.git
```
```bash
apt install requirements.txt
```
### To set alias in Linux (Ubuntu)
```bash
nano ~/.bashrc
```
Once you get into that file you net to write the absolute file to the location of this script

```bash
alias = "python3 absolute/path/to/this/script/scanAutomation.py"
```
Save the file and you need to recall this file with the following command

```bash
source ~/.bashrc
```

# scanAutomation
## Usage

To scan in BlackDuckHub you get into the directory to be scanned and since that path, you should execute the python script. 
You only need to know the project name, version and ReqID.

Don't worry the depth of the project will be calculated by the script. This script will create the Output directory to fill out with the scan output. Also, a *.txt will be created with the command used to scan in it.

## Flags

```bash
-p [Project_Name]
-v [Project_Version]
-i [ReqID]
```
Remember to include the BA in the Project Name

```bash
scanAutomation.py -p [Project_Name] -v [Project_Version] -i [ReqID]
```
### Example

```bash
scanAutomation.py -p [HLA403TH35] -v [MS11_12.0.3] -i [1642]
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
