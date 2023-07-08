# Covid19 Commandline Utility
![screenshot-1](https://github.com/TheViking733n/covid19_commandline_utility/assets/69471106/2deae1fa-4c50-4691-b10a-6602526a6404)

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

## Screenshots
![screenshot-2](https://github.com/TheViking733n/covid19_commandline_utility/assets/69471106/ea11d393-fa72-4838-a4ca-325ba79238d4)
![screenshot-3](https://github.com/TheViking733n/covid19_commandline_utility/assets/69471106/8f193855-1a87-4082-8021-d2e27073a360)


## Note
- Run this code in VS Code for coloured output (if using windows)


## Demonstration Clip
![Covid19-command-line-tool-with-district.gif](https://media.giphy.com/media/UaR6nA3i8oHtaNEkXq/giphy.gif)

## Credits
Without the API provided in [covid-19-data](https://github.com/nytimes/covid-19-data), this tool wouldn't be possible.
