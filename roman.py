#Copyright Laura DeWitt 2013©
#CS300 sequ project
# CL3
# For Roman numeral conversions validation

# The base of this code is based off of what I've found online in recipes to create a roman numeral
# converter and validate form. I've added to it to limit it to 3999 and positive integers and various checks. 
# I've also added a lower function to allow for the roman version.

import sys
import re

# Map the numerals to their values.
mapping = tuple(zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
    ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')))

# Prints the Upper Case Roman numerals associated with a given int value
def toRomanUpper(i):
	if i < 0 or i > 3999:
		sys.exit("sequ: value must be a positive whole number that is less than 4000")

	result = []

	try:
		for integer, numeral in mapping:
			count = i // integer
			result.append(numeral * count)
			i -= integer * count
		return ''.join(result)
	except:
		ValueError(sys.exit("sequ: invalid argument. Must be an integer."))

# Prints the lower case Roman numerals associated with a given int value
def toRomanLower(i):
	if i < 0 or i > 3999:
		sys.exit("sequ: value must be a positive whole number that is less than 4000")

	result = []

	try:
		for integer, numeral in mapping:
			count = i // integer
			result.append((numeral * count).lower())
			i -= integer * count
		return ''.join(result)
	except:
		ValueError(sys.exit("sequ: invalid argument. Must be an integer."))

# Attempts to turn a roman numeral into an integer value
def toInt(n):
    n = n.upper()
    i = result = 0
    for integer, numeral in mapping:
        while n[i:i + len(numeral)] == numeral:
            result += integer
            i += len(numeral)
	
    if result == 0 or result > 3999:
	    sys.exit("sequ: invalid character. Must be positive whole numbers under 3999")
    return result

# Validates a given Roman Numeral
def ValidateRoman(roman):
	pattern = '''
		^                   # beginning of string
		M{0,3}              # thousands - 0 to 3 Ms
		(CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 Cs),
		                    #            or 500-800 (D, followed by 0 to 3 Cs)
		(XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 Xs),
		                    #        or 50-80 (L, followed by 0 to 3 Xs)
		(IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 Is),
		                    #        or 5-8 (V, followed by 0 to 3 Is)
		$                   # end of string
		'''
	found = re.search(pattern, roman, re.VERBOSE)

	if found:
		return True
	else:
		return False

