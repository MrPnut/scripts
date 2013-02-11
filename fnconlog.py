#!/usr/env/bin/python

######################################
# fnconlog.py
# purpose:
#   Parses thru a javaScript file.
#   adds console.log() statements to the beginning of function definitions
#   or reverts the changes if the script is called on a file
#   where fnconlog.py was ran on previously.
# Author: Nick Cavallo

import sys
import os

def findNameOfFunction(functionLine):
	words = functionLine.split()
	functionName = 'undefined'
	nonFunctionNames = {'function':True, '{':True, '}':True, 'var':True, '=':True}
	
	for word in words:
		argumentIndex = word.find('(')

		if (argumentIndex != -1):
			# This is a 'var something = function()', strip the ()s
			word = word[:argumentIndex]

		if word not in nonFunctionNames:
			functionName = word
	
	return functionName


def processfile(file_in, file_out):
	line_buf = file_in.readlines()
	file_in.close()
	rowDeleted = False

	for lineNum in range(len(line_buf)):
		if (rowDeleted == True):
			rowDeleted = False
			continue

		line = line_buf[lineNum]

		rowDeleted = False

		if (line.find('function') != -1):
			functionLine = line
			nextLine = line_buf[lineNum + 1]
			functionName = findNameOfFunction(functionLine)

			# Reverse the change if we find a console.log() on the next line
			if (nextLine.find('console.log(') != -1):
				# Write out the function() line but don't write out
				# the console.log
				print '- ' + functionName + '()'
				file_out.write(line)
				rowDeleted = True
								
				continue

			elif (line.find('{') != -1 or nextLine.find('{') != -1):
				# Found the beginning of a function
				file_out.write(line)
				file_out.write('console.log(\'' + functionName + '()\');\n')
				print  '+ ' + functionName + '()'
			
			else:
				file_out.write(line)

		else:
			file_out.write(line)
	file_out.close()


def isValidFileName(name):
	dot = name.find('.')

	if (dot == -1):
		return False

	ext = name[dot+1:]

	if (ext.lower().find('.js') or ext.lower().find('.jsp') != -1):
		return True

	return False

def moveFiles(filename):
	cwd = os.getcwd()
	filePath = cwd + '/' + filename
	backupPath = filePath + '_BAK'

	if (os.path.isfile(backupPath)):
		os.remove(backupPath)
	
	os.rename(filePath, backupPath)
	os.rename(filePath + '_tmp', filePath)

def main():
	if (len(sys.argv) < 2):
		print "USAGE: fnconlog.py [filename.js]"
		return

	filename = sys.argv[1]
	
	if (isValidFileName(filename) == False):
		print "Not a js or jsp file!"
		return

	
	try:
		file_in = open(filename, 'rt')
		file_out = open(filename + '_tmp', 'wt')
		processfile(file_in, file_out)
		moveFiles(filename)

	except IOError as e:
		print "I/O Error({0}): {1}".format(e.errno, e.strerror)

	
main()

