# OSCAR Reviewers Tools

This repository contains useful scripts that could help us at the time to perform our daily work as reviewers.

## Installation

```bash
git clone https://github.com/AldoLeonH/OscarTools.git
```
```bash
apt install requirements.txt
```
# scanAutomation
## Usage

To scan in BlackDuckHub you need to enter the directory to be scanned and since that path, you should execute the python script.

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
