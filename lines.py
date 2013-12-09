#Copyright Laura DeWitt 2013©
#CS300 sequ project
# CL4

# Import the necessary libraries
import sys
import argparse
import string
import roman #local file

# This sets up the number lines format and calls the list maker to create the list to print
def NumberLinesFormat():
	count = 2 #The first 2 args always in argv
	# If there is no argument included
	if len(sys.argv) == 2:
		sys.exit("sequ: missing operand")
	# Determining the options
	if sys.argv[2].startswith("-F") or sys.argv[2].startswith("--format-word"):
		word = GetSeparator("F")
		if "=" in sys.argv[2]:
			count += 1
			try:
				if sys.argv[3].startswith("-s") or sys.argv[3].startswith("--separator"):
					separator = GetSeparator("s3")
				else:
					separator = " "
				if "=" in sys.argv[3]:
					count += 1
				else:
					count += 2
			except:
				sys.exit("sequ: missing operand")

		elif "=" not in sys.argv[2]:
			count += 2
			try:
				if sys.argv[4].startswith("-s") or sys.argv[4].startswith("--separator"):
					separator = GetSeparator("s4")
				else:
					separator = " "
				if "=" in sys.argv[4]:
					count += 1
				else:
					count += 2
			except:
				sys.exit("sequ: missing operand")

	elif sys.argv[2].startswith("-s") or sys.argv[2].startswith("--separator"):
		separator = GetSeparator("s2")
		word = GetSeparator("I")
		if "=" in argv[2]:
			count += 1
		else:
			count += 2

	else:
		word = GetSeparator("I")
		separator = " "

	if len(sys.argv) - count != 2:
		sys.exit("Invalid Limits.")

	WriteFile(word, separator)
	
	

# This gets the separator values for format word and separator and returns it
def GetSeparator(option):
	
	# Gets the value associated with the option for format/separator
	if option == "F" or option == "s2":
		try:	
			if "=" in sys.argv[2]:
				separator = sys.argv[2].split('=', 1)
				if "\\" in separator[1] and len(separator[1]) == 1 : 
					separator = separator[1]
				else:
					separator = bytes(str(separator[1]), "utf-8").decode("unicode_escape")
			
			else:
				if "\\" in sys.argv[3] and len(sys.argv[3]) == 1 : 
					separator = sys.argv[3]
				else:
					separator = bytes(str(sys.argv[3]), "utf-8").decode("unicode_escape")
		except:
			sys.exit("Missing Operand")

	elif option == "s3":
		if "=" in sys.argv[3]:
			separator = sys.argv[3].split('=', 1)
			if "\\" in separator[1] and len(separator[1]) == 1 : 
				separator = separator[1]
			else:
				separator = bytes(str(separator[1]), "utf-8").decode("unicode_escape")
			
		else:
			if "\\" in sys.argv[4] and len(sys.argv[4]) == 1 : 
				separator = sys.argv[4]
			else:
				separator = bytes(str(sys.argv[4]), "utf-8").decode("unicode_escape")

	elif option == "s4":
		if "=" in sys.argv[4]:
			separator = sys.argv[4].split('=', 1)
			if "\\" in separator[1] and len(separator[1]) == 1 : 
				separator = separator[1]
			else:
				separator = bytes(str(separator[1]), "utf-8").decode("unicode_escape")
			
		else:
			if "\\" in sys.argv[5] and len(sys.argv[5]) == 1 : 
				separator = sys.argv[5]
			else:
				separator = bytes(str(sys.argv[5]), "utf-8").decode("unicode_escape")
	# When the option has to be inferred
	elif option == "I":
		step = sys.argv[len(sys.argv)-1]
		start = sys.argv[len(sys.argv)-2]
		if start in string.ascii_letters:
			try:
				step = int(step)
				if start == start.upper():
					separator = "ALPHA"
				else:
					separator = "alpha"
			except:
				
				if roman.ValidateRoman(start.upper()) or roman.ValidateRoman(step.upper()):
					if (start == start.upper() and roman.ValidateRoman(start.upper())) or (step == step.upper() and roman.ValidateRoman(step.upper())):
						separator = "ROMAN"
					else:
						separator = "roman"
		else:
			step = float(step)
			if step != int(step):
				separator = "floating"
			else:
				separator = "arabic"
	else:
		separator = ""
	
	return separator

# Checks special cases before the list is created and exits if improper input
def CheckSpecialCases(word, start, step):
	if word == "arabic":
		try:
			start = int(start)
			step = int(step)
		except:
			sys.exit("Arabic numbers must be entered for this format.")
	if word == "floating":
		try:
			start = float(start) 
			step = float(step)
		except:
			sys.exit("Valid numbers must be entered for this format.")
	elif word == "roman" or word == "ROMAN":
		if roman.toInt(start.upper()) < 0 or roman.toInt(start.upper()) > 3999:
			sys.exit("Roman numerals range between 1 and 3999")
		if word == "roman" and start != start.lower():
			sys.exit("sequ: Argument cases must match the requested case.")
		if word == "ROMAN" and start != start.upper():
			sys.exit("sequ: Argument cases must match the requested case.")

# Prints out the numberlines or writes them to a given file
def WriteFile(word, separator):
	if not sys.stdin.isatty():
		data = list(sys.stdin)
	else:
		sys.exit("No file given.")

	step = str(sys.argv[len(sys.argv)-1])
	start = str(sys.argv[len(sys.argv)-2])
	
	CheckSpecialCases(word, start, step)

	if word == "arabic":
		for line in data:
			line = str(start) + separator + line
			print(line, end="")
			start = int(start) + int(step)

	elif word == "floating":
		for line in data:
			print("{:f}".format(float(start)), end=separator)
			print(line, end="")
			start = float(start) + float(step)
	
	elif word == "roman":
		if roman.ValidateRoman(step.upper()):
			step = int(roman.toInt(step))
		for line in data:
			if not roman.ValidateRoman(str(start).upper()):
				start = roman.toRomanLower(start)
			line = start + separator + line
			print(line, end = "")
			start = int(roman.toInt(start)) + step

	elif word == "ROMAN":
		if roman.ValidateRoman(step.upper()):
			step = int(roman.toInt(step))
			for line in data:
				if not roman.ValidateRoman(str(start).upper()):
					start = roman.toRomanUpper(start)
				line = start + separator + line
				print(line, end = "")
				start = int(roman.toInt(start)) + step
		else:
			sys.exit("Invalid Roman Numerals")

	elif word == "alpha" or word == "ALPHA":
		for line in data:
			line = start + separator + line
			print(line, end = "")
			start = chr(ord(start) + int(step))
			if ord(start) == ord('z') + 1 or ord(start) == ord('Z') + 1:
				if word == "alpha":
					start = "a"
				else:
					start = "A"
	else:
		sys.exit("Invalid Option")

	sys.exit(0)



