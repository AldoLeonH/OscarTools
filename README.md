# scanAutomation

This repository contains a useful script that could help us at the time to perform our daily work as reviewers.
**This script only works on Linux environment**, you could set an alias to call this script with a simple command. this could be called "Scan".

## Installation

```bash
git clone https://github.com/AldoLeonH/OscarTools.git
```

### To set alias in Linux (Ubuntu)
```bash
nano ~/.bashrc
```
Once you get into that file you need to write the absolute file to the location of this script

```bash
alias = "python3 absolute/path/to/this/script/scanAutomation.py"
```
Save the file and you need to reload this file with the following command

```bash
source ~/.bashrc
```
## Usage

To perform a BlackDuckHub scan, navigate to the target directory and execute the Python script. Only three parameters are needed: project name, version, and ReqID.

The script dynamically calculates the project depth, creates the 'Output' directory for scan results, and logs the scan command in a *.txt file.

### **Important Note**
**Caution: Do not execute this command from your home directory.** The script constructs commands based on the location where it is executed. Running it from the home directory may result in unintentional scanning of all directories and cause errors. Always navigate to the desired directory before using the scan alias.

## Flags


**-p** [Project_Name]
**-v** [Project_Version]
**-i** [ReqID]

Remember to include the BA in the Project Name

```bash
scanAutomation.py -p [Project_Name] -v [Project_Version] -i [ReqID]
```
### Example

```bash
scanAutomation.py -p [AM_HLA403TH35] -v [MS11_12.0.3] -i [1642]
```
or with alias

```bash
scan -p [AM_HLA403TH35] -v [MS11_12.0.3] -i [1642]
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
