#Copyright Laura DeWitt 2013©
#CS300 sequ project
# CL4

# Import the necessary libraries
import sys
import argparse
import string
import roman #local file. Must be in the same directory as sequ.py
import lines #local file. Must be in the same directory as sequ.py

# Checks the inital input for entries that are invalid and --help/--version arguments
def ValidInput():
	# if there are no arguments, exit with error code
	if len(sys.argv) < 2:
		sys.exit("sequ: missing operand")
	# calls the help page. This call ignores all input beyond it
	elif sys.argv[1] == "--help":
		PrintHelp() 
	# calls the version page. This call also ignores all input beyond it
	elif sys.argv[1] == "--version":
		PrintVersion()
	# This one is checked before the length limit because it can potentially exceed it 
	elif sys.argv[1] == "-n" or sys.argv[1] == "--number-lines":
		lines.NumberLinesFormat()
	# checks to make sure there are not more than 5 arguments, exits with error if there are
	# This goes after version and help because they can be called with any further input
	elif len(sys.argv) > 6:
		sys.exit("sequ: extra operand '" + sys.argv[6] + "'")
	else:
		return True;


# This checks to see if an option has been entered into the program.
# If it has, it calls that options list making function.
def CheckOptions():
		okay = ValidInput()
		if okay:
			if sys.argv[1] == "-w" or sys.argv[1] == "--equal-width":
				OptionFixedArgs("w")
			elif sys.argv[1].startswith("-s") or sys.argv[1].startswith("--separator"):
				OptionVaryingArgs("s")
			elif sys.argv[1].startswith("-f") or sys.argv[1].startswith("--format"):
				OptionVaryingArgs("f")
			elif sys.argv[1] == "-W" or sys.argv[1] == "--words":
				OptionFixedArgs("W") 
			elif sys.argv[1].startswith("-p") or sys.argv[1].startswith("--pad"):
				OptionVaryingArgs("p")
			elif sys.argv[1] == "-P" or sys.argv[1] == "--pad-spaces":
				OptionFixedArgs("P")
			elif sys.argv[1].startswith("-F") or sys.argv[1].startswith("--format-word"):
				SetUpFormatWord()
			# Goes to normal NoOption set up if no option requested
			else:
				NoOption()
		else:
			sys.exit("Something unexpected happened. Program terminated.")
		

# PrintHelp prints out the help page info and exits successfully.
# If help is entered as an option, every other argument is ignored.
def PrintHelp():
	print("Usage: sequ [OPTION]... LAST \n  or:  sequ [OPTION]... FIRST LAST\n"
		"  or:  sequ [OPTION]... FIRST INCREMENT LAST\n"
		"Print numbers from FIRST to LAST, in steps of INCREMENT.\n\n"
		"  -f, --format=FORMAT      use printf style floating-point FORMAT\n"
		"  -s, --separator=STRING   use STRING to separate numbers (default: \\n)\n"
		"  -w, --equal-width        equalize width by padding with leading zeroes\n"
		"  -W, --words              separates numbers with spaces (default: \\n)\n"
		"  -p, --pad=CHARACTER      equalizes width by padding with a single character\n"
		"  -P, --pad-spaces         equalizes width by padding with spaces\n"
		"  -F, --format-word=FORMAT determines the type of sequence\n"
		"  -n, --number-lines       numbers the lines of a given textfile\n"
		"      --help     display this help and exit\n"
		"      --version  output version information and exit\n\n"
		"If FIRST or INCREMENT is omitted, it defaults to 1.  That is, an\n"
		"omitted INCREMENT defaults to 1 even when LAST is smaller than FIRST.\n"
		"FIRST, INCREMENT, and LAST are interpreted as floating point values.\n"
		"INCREMENT is usually positive if FIRST is smaller than LAST, and\n"
		"INCREMENT is usually negative if FIRST is greater than LAST.\n"
		"FORMAT must be suitable for printing one argument of type \'double\';\n"
		"it defaults to %.PRECf if FIRST, INCREMENT, and LAST are all fixed point\n"
		"decimal numbers with maximum precision PREC, and to %g otherwise.\n\n"
		"-F accepts 'arabic', 'floating', 'alpha', 'ALPHA', 'roman', and 'ROMAN'.\n"
		"If -F is entered on its own, the type is inferred, with alpha having precedence\n"
		"over roman.\n\n"
		"-n can have optional -F and -s after it (in that order). If they are included,\n"
		"they must specify the option. If they are not included, the format is inferred\n"
		"and the separator is ' '. There MAY NOT be a LAST argument.\n"
		"This option continues until the end of the textfile. FIRST and INCREMENT\n"
		"MUST be entered for this option.\n"
		"A file is read in by < FILENAME and written out to a file by\n"
		"> DIFF_FILENAME.\n\n"
		"Report bugs to some-email@some-address.com\n"
		"GNU coreutils home page: <http://www.gnu.org/software/coreutils/>\n"
		"General help for using GNU software: <http://www.gnu.org/gethelp/>\n"
		"For complete documentation, ask me.")
	
	sys.exit(0)


# PrintVersion prints out the version page info and exits successfully.
# If version is entered as an option, every other argument is ignored.
def PrintVersion():
	print("sequ (My program) 1.4\nCopyright (C) 2013 Laura DeWitt\n"
		"License GPLv3+: GNU GPL Version 3 or later <http://gnu.org/licenses/gpl.html>.\n"
		"This is free software: you are free to change and redistribute it.\n"
		"There is NO WARRANTY, to the extent permitted by law.\n\n"
		"Written by Laura DeWitt.")

	sys.exit(0)


# This function creates the list that holds all of the values that need
# to be printed in the sequence. This will replace part of range() from CL0 since
# range only applies to integer values.
def CreateRange(start, step, stop):
	if step == 0:
		raise ZeroDivisionError(sys.exit("sequ: cannot increment by zero"))
	delta = stop - start
	numIterations = int(delta / step)
	# If START > STOP and STEP is not a decrement, print nothing and exit with success
	if numIterations < 0 and step > 0 and stop != start:
		sys.exit(0)
	# cuts off the trailing 0's if the start and step are whole numbers
	# There is no need for a float if that is the case
	if start == int(start) and step == int(step):
		start = int(start)
		step = int(step)
	theList = [start]
	for x in range(numIterations):
		start = start + step
		theList.append(start)
	return theList
	

# This prints the numbers according to the arguments entered on the command line
# and the options selected (if any)
def PrintNumbers(theList, option):
	separator = GetSeparator(option)

	# Zeroes are added to even the digits to the length of the maximum digit
	if option == 'w':
		# This is the number of digits in the largest number in theList
		maxlen = int(len(str(max(theList))))
		theList = AdjustWidth(maxlen, theList, '0')
		# Goes through theList and pads with 0's where needed for equal length
		for x in theList:
			print(x)

	# A character is selected to pad for equal width of the maximum digit
	elif option == 'p':
		pad = verifyPad(separator)
		# This is the number of digits in the largest number in theList
		maxlen = int(len(str(max(theList))))
		theList = AdjustWidth(maxlen, theList, pad)
		# Goes through theList and pads with 0's where needed for equal length
		for x in theList:
			print(x)

	# Spaces are added to pad for equal width of the maximum digit
	elif option == 'P':
		# This is the number of digits in the largest number in theList
		maxlen = int(len(str(max(theList))))
		theList = AdjustWidth(maxlen, theList, " ")
		# Goes through theList and pads with 0's where needed for equal length
		for x in theList:
			print(x)

	# Prints the values with the separator instead of carriage return
	elif option == 's':
		for x in theList:
			print(x, end = separator)
		print()
		sys.exit(0)

	# Prints with a space separator
	elif option == 'W':
		for x in theList:
			print(x, end = " ")
		print()
		sys.exit(0)

	# Prints according to the format given
	elif option == 'f':
		# verify the requested format
		okay = VerifyFormat(separator)
		if okay == 'f':
			for x in theList:
				print("{:f}".format(x))
		elif okay == 'e':
			for x in theList:
				print("{:e}".format(x))
		elif okay == 'a':
			for x in theList:
				print("{:a}".format(x))
		elif okay == 'g':
			for x in theList:
				print("{:g}".format(x))

	elif option == "F" or option == "I":
		if separator == "floating":
			for x in theList:
				print("{:f}".format(x))
		elif separator == "arabic":		
				for x in theList:
					print(x)
		elif separator == "roman":
			for x in theList:
				print(roman.toRomanLower(x))
		elif separator == "ROMAN":
			for x in theList:
				print(roman.toRomanUpper(x))
		elif separator == "alpha" or "ALPHA":
			for x in theList:
				print(chr(x))
		
	# No option was given so list is printed without extra formatting
	elif option == 'na':
		# print the sequence
		for x in theList:
			print(x)
	else:
		sys.exit("sequ: Something unexpected happened.")

	sys.exit(0)


# Function creates the appropriate list for options that do not specify format,
# and have fixed locations of args. Sends the proper flag to the print numbers function for proper 
# printing format.
def OptionFixedArgs(flag):
	if len(sys.argv) == 2:
		raise Exception(sys.exit("sequ: missing operand"))
	if len(sys.argv) > 5:
		raise Exception(sys.exit("sequ: extra operand " + sys.argv[5]))
	try:
		if len(sys.argv) == 5:
			start = float(sys.argv[2])
			step = float(sys.argv[3])
			stop = float(sys.argv[4])
		elif len(sys.argv) == 4:
			start = float(sys.argv[2])
			step = 1
			stop = float(sys.argv[3])
		else:
			start = 1
			step = 1
			stop = float(sys.argv[2])
		# Create the list to print
		theList = CreateRange(start, step, stop)

		PrintNumbers(theList, flag)
	except ValueError:
		sys.exit("sequ: invalid floating point argument")


# Function creates the proper list for this option and sends the appropriate flag
# to the print numbers function for correct format depending on which option was chosen.
# These options can be specified and the location of args may vary.
def OptionVaryingArgs(flag):
	# If there is no argument included, or 1 is included but there is no
	# = associated with -s/--separator or -f/--format and the argument is seen as the option, not a digit.
	if len(sys.argv) == 2 or ("=" not in sys.argv[1] and len(sys.argv) == 3) :
		sys.exit("sequ: missing operand")	

	# Setup depends on whether the separator/format is included in the option by '=' or if it is the next argument
	if "=" in sys.argv[1]:
		if len(sys.argv) > 5:
			sys.exit("sequ: extra operand: " + sys.argv[5])
		try:
			if len(sys.argv) == 5:
				start = float(sys.argv[2])
				step = float(sys.argv[3])
				stop = float(sys.argv[4])
			elif len(sys.argv) == 4:
				start = float(sys.argv[2])
				step = 1
				stop = float(sys.argv[3])
			else:
				start = 1
				step = 1
				stop = float(sys.argv[2])

		except ValueError:
			sys.exit("sequ: invalid floating point argument")
	else:
		try:
			if len(sys.argv) == 6:
				start = float(sys.argv[3])
				step = float(sys.argv[4])
				stop = float(sys.argv[5])
			elif len(sys.argv) == 5:
				start = float(sys.argv[3])
				step = 1
				stop = float(sys.argv[4])
			else:
				start = 1
				step = 1
				stop = float(sys.argv[3])

		except ValueError:
				sys.exit("sequ: invalid floating point argument")

	separator = GetSeparator(flag)
	CheckSpecialCases(separator, start, step, stop)
				
	# Create the list to print
	theList = CreateRange(start, step, stop)

	PrintNumbers(theList, flag)


# Function creates the proper list for this option and sends the appropriate flag
# to the print numbers function for correct format depending on which option was chosen.
# These options can be specified and the location of args may vary.
# These lists are for letters, not floats.
def OptionStringArgs(flag):
	if flag == "F":
		# If there is no argument included
		if len(sys.argv) == 2 or ("=" not in sys.argv[1] and len(sys.argv) == 3) :
			sys.exit("sequ: missing operand")	

		# The setup depends on whether the separator/format is included in the option by '=' or
		# if it is the next argument
		if "=" in sys.argv[1]:
			if len(sys.argv) > 5:
				sys.exit("sequ: extra operand: " + sys.argv[5])
			try:
				if len(sys.argv) == 5:
					start = str(sys.argv[2])
					step = int(sys.argv[3])
					stop = str(sys.argv[4])
				elif len(sys.argv) == 4:
					start = str(sys.argv[2])
					step = 1
					stop = str(sys.argv[3])
				else:
					start = "a"
					step = 1
					stop = str(sys.argv[2])

				if len(start) > 1 or len(stop) > 1:
					sys.exit("sequ: only one letter may be specified per position.")

			except ValueError:
				sys.exit("sequ: invalid alpha argument")
		else:
			try:
				if len(sys.argv) == 6:
					start = str(sys.argv[3])
					step = int(sys.argv[4])
					stop = str(sys.argv[5])
				elif len(sys.argv) == 5:
					start = str(sys.argv[3])
					step = 1
					stop = str(sys.argv[4])
				else:
					start = 1
					step = 1
					stop = str(sys.argv[3])

				if len(start) > 1 or len(stop) > 1:
					sys.exit("sequ: only one letter may be specified per position.")
			
			except ValueError:
					sys.exit("sequ: invalid alpha argument")
	elif flag == "I":
		try:
				if len(sys.argv) == 5:
					start = str(sys.argv[2])
					step = int(sys.argv[3])
					stop = str(sys.argv[4])
				elif len(sys.argv) == 4:
					start = str(sys.argv[2])
					step = 1
					stop = str(sys.argv[3])
				else:
					start = 1
					step = 1
					stop = str(sys.argv[2])

				if len(start) > 1 or len(stop) > 1:
					sys.exit("sequ: only one letter may be specified per position.")
			
		except ValueError:
				sys.exit("sequ: invalid alpha argument")
	if start not in string.ascii_letters or stop not in string.ascii_letters:
		raise ValueError(sys.exit("The sequence must be comprised of letters."))

	separator = GetSeparator(flag)
	CheckSpecialCases(separator, start, step, stop)

	# Create the list to print
	theList = CreateRange(ord(start), step, ord(stop))

	PrintNumbers(theList, flag)


# This is for Roman numeral sequences.
def OptionRomanArgs(flag):
	if flag == "F":
		# If there is no argument included.
		if len(sys.argv) == 2 or ("=" not in sys.argv[1] and len(sys.argv) == 3) :
			sys.exit("sequ: missing operand")	

		# The setup depends on whether the separator/format is included in the option by '=' or
		# if it is the next argument
		if "=" in sys.argv[1]:
			if len(sys.argv) > 5:
				sys.exit("sequ: extra operand: " + sys.argv[5])
			try:
				if len(sys.argv) == 5:
					start = str(sys.argv[2])
					step = str(sys.argv[3])
					stop = str(sys.argv[4])
				elif len(sys.argv) == 4:
					start = str(sys.argv[2])
					step = str(1)
					stop = str(sys.argv[3])
				else:
					start = str(1)
					step = str(1)
					stop = str(sys.argv[2])

			except ValueError:
				sys.exit("sequ: invalid roman argument")
		else:
			try:
				if len(sys.argv) == 6:
					start = str(sys.argv[3])
					step = str(sys.argv[4])
					stop = str(sys.argv[5])
				elif len(sys.argv) == 5:
					start = str(sys.argv[3])
					step = str(1)
					stop = str(sys.argv[4])
				else:
					start = str(1)
					step = str(1)
					stop = str(sys.argv[3])
			
			except ValueError:
					sys.exit("sequ: invalid roman argument")

	elif flag == "I":
		try:
				if len(sys.argv) == 5:
					start = str(sys.argv[2])
					step = str(sys.argv[3])
					stop = str(sys.argv[4])
				elif len(sys.argv) == 4:
					start = str(sys.argv[2])
					step = str(1)
					stop = str(sys.argv[3])
				else:
					start = str(1)
					step = str(1)
					stop = str(sys.argv[2])
			
		except ValueError:
				sys.exit("sequ: invalid roman argument")

	# Checks to make sure the proper case has been used and validates given roman numerals
	separator = GetSeparator(flag)
	for x in start:
		if x not in string.digits:
			VerifyRoman(separator, start)
			if roman.ValidateRoman(start.upper()):	
				start = roman.toInt(start)
			else:
				raise ValueError(sys.exit("Invalid Roman Numeral"))
			break
	for x in step:
		if x not in string.digits:
			VerifyRoman(separator, step)
			if roman.ValidateRoman(step.upper()):	 
				step = roman.toInt(step)
			else:
				raise ValueError(sys.exit("Invalid Roman Numeral"))
			break
	for x in stop:
		if x not in string.digits:
			VerifyRoman(separator, stop)
			if roman.ValidateRoman(stop.upper()):	
				stop = roman.toInt(stop)
			else:
				raise ValueError(sys.exit("Invalid Roman Numeral"))
			break
	
	start = int(start)
	step = int(step)
	stop = int(stop)
	
	CheckSpecialCases(separator, start, step, stop)

	# Create the list to print
	theList = CreateRange(start, step, stop)
	PrintNumbers(theList, flag)


# This verifies that the requested format is a valid one.
# It checks to see if the first letter is a format character
def VerifyFormat(separator):
	if not separator.startswith('%'):
		sys.exit("sequ: format " + separator + " has no % directive")
	format = []
	for x in separator:
		if x in string.ascii_letters:
			format.append(x)
	if format[0] == 'e' or format [0] == 'f' or format[0] == 'g' or format[0] == 'a':
		return format[0]
	else:
		sys.exit("sequ: format " + separator + " has unknown %" + format[0] + " directive")


# NoOption is used to create the list when there are no options sent in with the arguments
def NoOption():
	try: 
		if len(sys.argv) == 5:
			raise ValueError(sys.exit("sequ: extra operand: " + sys.argv[4]))
		elif len(sys.argv) == 4:
			start = float(sys.argv[1])
			step = float(sys.argv[2])
			stop = float(sys.argv[3])
		elif len(sys.argv) == 3:
			start = float(sys.argv[1])
			step = 1
			stop = float(sys.argv[2])
		else:
			start = 1
			step = 1
			stop = float(sys.argv[1])
	except ValueError:
		sys.exit("sequ: invalid floating point argument")
	# Create the list to print
	theList = CreateRange(start, step, stop)
	PrintNumbers(theList, 'na')	


# Determines where to add padding to equal width
def AdjustWidth(maxlen, theList, pad):
	# number of digits before and after the decimal point
	newList = []
	before = []
	after = []
	if "." in str(theList):
		for x in theList:
			separator = str(x).split('.', 1)
			before.append(separator[0])
			after.append(separator[1])
		maxbefore = int(len(max(before, key=len)))
		maxafter = int(len(max(after, key=len)))
	for x in theList:
		if "." in str(x):
			separator = str(x).split('.', 1)
			currentbefore = int(len(separator[0]))
			currentafter = int(len(separator[1]))			
			x = str(x).rjust((maxbefore - currentbefore) + len(str(x)), pad) 
			x = str(x).ljust((maxafter - currentafter) + len(str(x)), pad)
			newList.append(x)
		else:
			x = str(x).rjust(maxlen, pad)
			newList.append(x) 
	return newList


# This verifies that only one character has been selected for the padding and returns it to 
# printnumbers 			
def verifyPad(separator):
	if len(separator) > 1:
		sys.exit("sequ: Only one character accepted for --pad")
	else:
		return separator


# This function is used to determine which list function needs to be called.
# It gets the supplied option and calls the appropriate function. Calls infer function if no word given.
def SetUpFormatWord():
	# If there is no argument included.
	if len(sys.argv) == 2:
		sys.exit("sequ: missing operand")	

	if "=" in sys.argv[1]:
		separator = sys.argv[1].split('=', 1)
		separator = separator[1]
			
	else:
		separator = sys.argv[2]

	if separator == "floating" or separator == "arabic":
		OptionVaryingArgs("F")
	
	elif separator == "roman" or separator == "ROMAN":
		OptionRomanArgs("F")

	elif separator == "alpha" or separator == "ALPHA":
		OptionStringArgs("F")		

	else:
		InferFormatWord()


# This gets the separator value and returns it
def GetSeparator(option):
	# Gets the value associated with the option for format/separator/pad
	if option == "s" or option == "f" or option == "p" or option == "F":	
		if "=" in sys.argv[1]:
			separator = sys.argv[1].split('=', 1)
			if "\\" in separator[1] and len(separator[1]) == 1 : 
				separator = separator[1]
			else:
				separator = bytes(str(separator[1]), "utf-8").decode("unicode_escape")
			
		else:
			if "\\" in sys.argv[2] and len(sys.argv[2]) == 1 : 
				separator = sys.argv[2]
			else:
				separator = bytes(str(sys.argv[2]), "utf-8").decode("unicode_escape")
	# When the option has to be inferred
	elif option == "I":
		stop = sys.argv[len(sys.argv)-1]
		start = sys.argv[2]		
		if stop in string.ascii_letters and start in string.ascii_letters:
			if stop == stop.upper():
				separator = "ALPHA"
			else:
				separator = "alpha"
		elif roman.ValidateRoman(stop.upper()):
			if stop == stop.upper():
				separator = "ROMAN"
			else:
				separator = "roman"
		else:
			stop = float(stop)
			if stop != int(stop):
				separator = "floating"
			else:
				separator = "arabic"
	else:
		separator = ""
	return separator


# Checks special cases before the list is created and exits if improper input
def CheckSpecialCases(separator, start, step, stop):
	if separator == "arabic":
		if start != int(start) or step != int(step) or stop != int(stop):
			sys.exit("sequ: Arabic integers must be entered for this format.")
	elif separator == "roman" or separator == "ROMAN":
		if start < 0 or start > 3999 or stop < 0 or stop > 3999:
			sys.exit("sequ: roman numerals range between 1 and 3999")
	elif separator == "alpha":
		if start == start.upper() or stop == stop.upper():
			sys.exit("sequ: characters must have the appropriate case for the format.")	
	elif separator == "ALPHA":
		if start == start.lower() or stop == stop.lower():
			sys.exit("sequ: characters must have the appropriate case for the format.")


# Checks to make sure the is not mismatched cases
def VerifyRoman(separator, check):
	if separator == "roman" and check != check.lower():
		sys.exit("sequ: Argument cases must match the requested case.")
	if separator == "ROMAN" and check != check.upper():
		sys.exit("sequ: Argument cases must match the requested case.")


# Tries to infer the format word choice by the last argument. If it can be inferred,
# The appropriate function is called to set up the list, otherwise it exits with an error message
def InferFormatWord():
	stop = sys.argv[len(sys.argv)-1]
	start = sys.argv[2]
	if stop in string.ascii_letters and start in string.ascii_letters:
		OptionStringArgs("I")
	elif roman.ValidateRoman(stop.upper()):
		OptionRomanArgs("I")
	else:
		OptionFixedArgs("I")
		
# A created main function to run the functionality of the program
def main():
	CheckOptions()


# Run the program
main()
