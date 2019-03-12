#!/Users/jan-philippthiele/anaconda3/bin/python

import cgi
import sys
import csv

form = cgi.FieldStorage()

color = form.getvalue("color")

with open("colors.csv") as _filehandler:
	csv_file_reader = csv.DictReader(_filehandler)
	check = False
	for row in csv_file_reader:
		if color in row["color-name"]:
			check = True
			break
	if check == True:
		print("""
		<html>
		<body>
		<p> %s
		is a valid color! The hex code is: %s 
		</p>
		</body>
		</html>
		""" %(color, row["hex"]))
	else:
		print("""
		<html>
		<body>
		<p>%s is not a valid color
		</p>
		</body>
		</html>
		""" % color)
