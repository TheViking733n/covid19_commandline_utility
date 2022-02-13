import requests
import argparse
from difflib import get_close_matches
from colorama import Fore

"""
Author: Anant Prakash Singh
GitHub: https://github.com/TheViking733n/covid19_commandline_utility
Date: 13-02-2022
Description:
* This is a command line utility that fetches the data from the covid19india.org API
  and prints the covid cases data for the given state.

Features:
* Colored output screen
* If no arguments are passes, it prints data for whole India.
* If state code is passed, it prints data for that state.
* If state name is passed, it prints most appropriate state data.
* District names can also be passed.
* If state and district names both are passed then it will search for the district name in the given state.
* If only district name is passed, then it will search for the district name in whole country.

Note:
* Run this code in VS Code for coloured output (if using windows)

"""

STATE_CODES = ['AN', 'AP', 'AR', 'AS', 'BR', 'CH', 'CT', 'DL', 'DN', 'GA', 'GJ', 'HP', 'HR', 'JH', 'JK', 'KA', 'KL', 'LA', 'LD', 'MH', 'ML', 'MN', 'MP', 'MZ', 'NL', 'OR', 'PB', 'PY', 'RJ', 'SK', 'TG', 'TN', 'TR', 'TT', 'UP', 'UT', 'WB']
STATE_NAMES = {
	'AN': 'Andaman and Nicobar Islands',
	'AP': 'Andhra Pradesh',
	'AR': 'Arunachal Pradesh',
	'AS': 'Assam',
	'BR': 'Bihar',
	'CH': 'Chandigarh',
	'CT': 'Chhattisgarh',
	'DN': 'Dadra and Nagar Haveli',
	'DD': 'Daman and Diu',
	'DL': 'Delhi',
	'GA': 'Goa',
	'GJ': 'Gujarat',
	'HR': 'Haryana',
	'HP': 'Himachal Pradesh',
	'JK': 'Jammu and Kashmir',
	'JH': 'Jharkhand',
	'KA': 'Karnataka',
	'KL': 'Kerala',
	'LD': 'Lakshadweep',
	'MP': 'Madhya Pradesh',
	'MH': 'Maharashtra',
	'MN': 'Manipur',
	'ML': 'Meghalaya',
	'MZ': 'Mizoram',
	'NL': 'Nagaland',
	'OR': 'Odisha',
	'PY': 'Puducherry',
	'PB': 'Punjab',
	'RJ': 'Rajasthan',
	'SK': 'Sikkim',
	'TN': 'Tamil Nadu',
	'TG': 'Telangana',
	'TR': 'Tripura',
	'UP': 'Uttar Pradesh',
	'UT': 'Uttarakhand',
	'WB': 'West Bengal'
}

def print_data(cases_dict, name):
	confirmed = 0 if "confirmed" not in cases_dict else cases_dict["confirmed"]
	deceased = 0 if "deceased" not in cases_dict else cases_dict["deceased"]
	recovered = 0 if "recovered" not in cases_dict else cases_dict["recovered"]
	tested = 0 if "tested" not in cases_dict else cases_dict["tested"]
	vaccinated1 = 0 if "vaccinated1" not in cases_dict else cases_dict["vaccinated1"]
	vaccinated2 = 0 if "vaccinated2" not in cases_dict else cases_dict["vaccinated2"]
	
	line = "Covid-19 Cases Statistics for {}:".format(name)
	print(Fore.BLUE + "="*len(line))
	print(Fore.BLUE + line)
	print(Fore.BLUE + "="*len(line))
	print(Fore.MAGENTA + "  Confirmed Cases:  {:,}".format(confirmed))
	print(Fore.RED +     "  Deceased Cases:   {:,}".format(deceased))
	print(Fore.BLUE +    "  Tested Cases:     {:,}".format(tested))
	print(Fore.GREEN +   "  Recovered Cases:  {:,}".format(recovered))
	print(Fore.CYAN +    "  Vaccinated with 1st dose: {:,}".format(vaccinated1))
	print(Fore.CYAN +    "  Vaccinated with 2nd dose: {:,}".format(vaccinated2))
	print(Fore.WHITE + "")


def parse_state(state):
	"""
	Parse the state name and returns a list of most appropriate state codes.
	Reurns None if len(state)==2 and state name is not found.
	"""

	global STATE_CODES

	if len(state) <= 2:
		# It means user has entered a state code.
		state = state.upper()
		if state in STATE_CODES:
			return [state]
		else:
			return None
		
		
	# User has not entered a state code.
	alternate_names = {
		"andaman": "AN",
		"nicobar": "AN",
		"andhra": "AP",
		"arunachal": "AR",
		"assam": "AS",
		"bihar": "BR",
		"chandigarh": "CH",
		"chhattisgarh": "CT",
		"dadra": "DN",
		"nagar": "DN",
		"daman": "DD",
		"diu": "DD",
		"delhi": "DL",
		"goa": "GA",
		"gujarat": "GJ",
		"haryana": "HR",
		"himachal": "HP",
		"jammu": "JK",
		"kashmir": "JK",
		"jharkhand": "JH",
		"karnataka": "KA",
		"kerala": "KL",
		"lakshadweep": "LD",
		"madhya": "MP",
		"maharashtra": "MH",
		"manipur": "MN",
		"meghalaya": "ML",
		"mizoram": "MZ",
		"nagaland": "NL",
		"odisha": "OR",
		"punjab": "PB",
		"puducherry": "PY",
		"rajasthan": "RJ",
		"sikkim": "SK",
		"tamil": "TN",
		"nadu": "TN",
		"telangana": "TG",
		"tripura": "TR",
		"uttar": "UP",
		"uttarakhand": "UT",
		"west": "WB",
		"bengal": "WB"
	}

	if state in alternate_names:
		return [alternate_names[state]]

	else:
		# If state is not found in alternate names, then we will try to find it using difflib.get_close_matches
		state_name_lst = get_close_matches(state, alternate_names.keys())
		if len(state_name_lst) > 0:
			return [alternate_names[st] for st in state_name_lst]
		else:
			return None




def parse_district(district, data_dct, state_codes_list=None):
	"""
	Parses the district name and returns a tuple of state code and correct district name.
	Return (None, None) if district name is not found.

	"""

	global STATE_CODES
	if state_codes_list is None:
		states_to_check = STATE_CODES
	else:
		if type(state_codes_list) is str:
			state_codes_list = [state_codes_list]
		
		states_to_check = state_codes_list
	
	state_code_by_district = {}
	for st_code in states_to_check:
		if "districts" in data_dct[st_code]:
			dist_names = list(data_dct[st_code]["districts"].keys())
			for distr in dist_names:
				state_code_by_district[distr] = st_code

	district_name_lst = get_close_matches(district, state_code_by_district.keys())	

	if len(district_name_lst) > 0:
		return (state_code_by_district[district_name_lst[0]], district_name_lst[0])
	else:
		return (None, None)


def main():
	# Fetching data from API
	api_url = "https://data.covid19india.org/v4/min/data.min.json"
	r = requests.get(api_url)

	if r:
		data_dict = r.json()  # Parsing JSON response as a Python dict

		# Parsing command line arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-s", "--state", required=False,
			help="Enter name of state")
		ap.add_argument("-d", "--district", required=False,
			help="Enter name of district")
		args = vars(ap.parse_args())

		state = args["state"]
		district = args["district"]

		if state is not None:
			state = state.lower()

		if district is not None:
			district = district.lower()


		if (state is not None) and (district is not None):
			# Both state and district are specified.

			_state_code_lst = parse_state(state)
			if _state_code_lst is None:
				print(Fore.RED + "Error: State name was not found !!")
				print(Fore.RED + "Please try again")
				print(Fore.WHITE + "")
				quit()
			
			_state_code, _district_name = parse_district(district, data_dict, _state_code_lst)

			if _district_name is None:
				print(Fore.RED + "Error: District name was not found !!")
				print(Fore.RED + "Please try again")
				print(Fore.WHITE + "")
				quit()
				
			else:
				district_data = data_dict[_state_code]["districts"][_district_name]['total']
				print_data(district_data, _district_name+", "+STATE_NAMES[_state_code])




		elif (state is None) and (district is not None):
			# Only district is specified.

			_state_code, _district_name = parse_district(district, data_dict)

			if _district_name is None:
				print(Fore.RED + "Error: District name was not found !!\n")
				print(Fore.RED + "Please try again\n")
				print(Fore.WHITE + "")
				quit()

			else:
				district_data = data_dict[_state_code]["districts"][_district_name]['total']
				print_data(district_data, _district_name+", "+STATE_NAMES[_state_code])



		elif (state is not None):
			# Only state is specified.

			_state_code_lst = parse_state(state)
			if _state_code_lst is None:
				print(Fore.RED + "Error: State name was not found !!\n")
				print(Fore.RED + "Please try again\n")
				print(Fore.WHITE + "")
				quit()

			for _state_code in _state_code_lst:
				state_data = data_dict[_state_code]["total"]
				print_data(state_data, STATE_NAMES[_state_code])

		else:
			# User didn't enter any state or district code
			# Calculating sum of all cases of INDIA

			total = {
				"confirmed" : 0,
				"deceased" : 0,
				"recovered" : 0,
				"tested" : 0,
				"vaccinated2" : 0,
				"vaccinated1" : 0
			}
			for state in data_dict:
				state_total = data_dict[state]["total"]
				total = {key: state_total[key]+total[key] for key in total}

			print_data(total, "India")



	else:
		print(Fore.RED + "HTTP Error: {}".format(r.status_code))
		print(Fore.WHITE + "")








if __name__ == "__main__":
	main()