# Covid19 Commandline Utility
This is a command line utility that fetches the data from the covid19india.org API and prints the covid cases data for Indian states and districts

## Dependencies
- [requests](https://pypi.org/project/requests/)

## Installation
```sh
pip3 install requests
```
## Usage Examples
```sh
python covid.py -s delhi
```
```sh
python covid.py -d varnsi
```
```sh
python covid.py -d gorakh -s up
```


## Features
- Colored output screen
- If no arguments are passes, it prints data for whole India.
- If state code is passed, it prints data for that state.
- If state name is passed, it prints most appropriate state data.
- District names can also be passed.
- If state and district names both are passed then it will search for the district name in the given state.
- If only district name is passed, then it will search for the district name in whole country.



## Note
- Run this code in VS Code for coloured output (if using windows)


## Demonstration Clip
![Covid19-command-line-tool-with-district.gif](https://s10.gifyu.com/images/Covid19-command-line-tool-with-district.gif)

## Credits
Without the API provided in [covid-19-data](https://github.com/nytimes/covid-19-data), this tool wouldn't be possible.
