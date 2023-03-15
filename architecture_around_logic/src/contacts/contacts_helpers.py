import re

# todo probably need a more thorough check for input i.e.
#  check that there is a leading "+" before cleaning input


def check_input_good(input):
	return re.match(r'\+\d{7,15}', input)


def format_number(number):
	formatted_number = re.sub(r'[^0-9]+', '', number)
	return "+" + formatted_number