import sys
import os.path
import random


# Import the Config variables
from GPv2_config import *


# Welcome message
def Welcome():
	print '''\n\n\n\n\n\n
	=======================================================================================
	======================================================================================= 
	Welcome to the C10 Grading Program, written to determine grades for Alex Filippenko's
	Astro C10 course. Original program written by Aaron Lee in Spring 2015, further modified 
	by future Head GSIs. Users of this program should take note of the comments in the config
	file.
	
	If you are using this program for the first time, please consult the config file for
	instructions. If you need additional help, consult the guidance of past Head GSIs that
	have used this program.
	=======================================================================================
	'''



# Checks to make sure all the entries in the Config file make sense.
def ConfigChecks(): 
    print "Performing checks on the config file...."
    if not isinstance(gradebookFile,str): sys.exit("Doh! Gradebook file name not valid!")
    if not isinstance(gradeTypeC10File,str): sys.exit("Doh! C10 Bearfacts file not valid!")
    if not isinstance(gradeTypeLaSFile,str): sys.exit("Doh! L&S Bearfacts file not valid!")
    if not os.path.isfile(gradebookFile): sys.exit("Doh! Gradebook file" + str(gradebookFile) + " does not exist!")
    if not os.path.isfile(gradeTypeC10File): sys.exit("Doh! Gradebook file" + str(gradeTypeC10File) + " does not exist!")
    if not os.path.isfile(gradeTypeLaSFile): sys.exit("Doh! Gradebook file" + str(gradeTypeLaSFile) + " does not exist!")
    if not isinstance(headerRowNum,int): sys.exit("Doh! headerRowNum not an integer!")
    if not isinstance(startRowNum,int): sys.exit("Doh! startRowNum not an integer?!")
    if not isinstance(cNM+cID+cSE+cHWs+cHWe+cQZs+cQZe+cLBs+cLBe+cMTs+cMTe+cSP+cFE,int): sys.exit("Doh! Gradebook columns aren't integers?!")
    if not isinstance(headerTypeRowNum,int): sys.exit("Doh! headerTypeRowNum not an integer!")
    if not isinstance(startTypeRowNum,int): sys.exit("Doh! startTypeRowNum not an integer!")
    if not isinstance(cTypeID+cTypeNM+cTypeCC,int): sys.exit("Doh! A column in the Bearfacts files is not an integer!")
    if not isinstance(numSections,int): sys.exit("Doh! numSections not an integer!")
    if(len(GSInames) != numSections): sys.exit("Doh! Too few or too many GSI names listed")
    if not isinstance(cpHW+cpQZ+cpMT+cpSP+cpLB+cpFE,int): sys.exit("Doh! Total course points not an integer!")
    if not isinstance(maxHW+maxQZ+maxMT+maxLB+maxSP+maxFE,int): sys.exit("Doh! Max points per assignment not an integer!")
    if not isinstance(keepHW,int): sys.exit("Doh! How can we keep a fraction number of HWs?!")
    if not isinstance(keepMT,int): sys.exit("Doh! How can we keep a fraction number of MTs?!")
    if not isinstance(confident,bool): sys.exit("Doh! Cofidence parameter is not a boolean!")
    if(len(letterNames) != len(gradeBoundaries)): sys.exit("Doh! Number of letter grades does not match number of grade boundaries.")
    for i in range(0,len(gradeBoundaries)-1):
        for j in range(i+1,len(gradeBoundaries)):
            if( gradeBoundaries[i] <= gradeBoundaries[j]): sys.exit("C'mon now, write your letter grades in descending order...")
    for oride in Overrides:
        if(len(oride) != 2): sys.exit("Doh! An override entry is not the proper length!")
    print "Config file checks out! Huzzah."
	
# Creates an array of floating-point percents instead of course points. Checks
# to make sure that you don't need over 100% to get a particular grade.
def PrepGrades(gdbdy):
    for i in range(0,len(gdbdy)):
        gdbdy[i] = 1.0*gradeBoundaries[i]/totPTs
        if(gdbdy[i] > 1.0): sys.exit("Hmmm, getting an " + letterNames[i] + " requires > 100%. That's weird.\n")


# This sorts through the data and types files and creates one file that has all the raw data
def MakeGradeBook(data,types,gbook):
	# For each entry in the types, find the student in the data array and pull all the data
	for i in range(0,len(types)):
		curstudt = types.pop(0) # current student of interest
		found = False
		jsave = -1
		for j in range(0,len(data)):
			if( curstudt[1] == data[j][1] ) : 
				if(found == False):
					curstudg = data[j]
					found = True
					jsave = j
				elif(found == True):
					sys.exit("Hmmm, student id " + str(data[j][1]) + " appears twice in the gradebook. Investigate that and try again.")
		if(jsave == -1): sys.exit("Uh oh, we couldn't locate student " + str(curstudt[1]) + " in the raw gradebook!")
		else: data.pop(jsave)
		# Now make an entry in the gradebook that combines these two arrays
		gbook.append(curstudg + curstudt[2:4])
	print gbook
    # Gradebook is now made!
	if(True):
		PLine()
		PLine()
		print("\nThese are the remaining entries in the raw gradebook. These names aren't in the BearFacts files!")
		print("That might mean they are auditing the course. In that case, there will be no grade book entries.")
		print("These names are in the bCourse grade book, but don't have a single grade entered:")
		for j in range(0,len(data)):
			if( sum(data[j][3:3+numHW+numQZ+numMT+numLB+1]) == 0 ):
				print("\nName: " + data[j][0] + " (" + data[j][1] + ")")
				if(data[j][2]=="No Section"): print("Section: " + data[j][2])
				else: print("Section: " + data[j][2] + " (GSI: " + GSInames[int(data[j][2])-101] + ")" )
		print("\nThese are the names that DO HAVE grade book entries. They might have since dropped the")
		print("course, but some might not realize they are not enrolled in C10!")
		for j in range(0,len(data)):
			if( sum(data[j][3:3+numHW+numQZ+numMT+numLB+1]) > 0 ):
				print("\nName: " + data[j][0] + " (" + data[j][1] + ")")
				if(data[j][2]=="No Section"): print("Section: " + data[j][2])
				else: print("Section: " + data[j][2] + " (GSI: " + GSInames[int(data[j][2])-101] + ")" )
				print("HW Scores: " + str(data[j][3:3+numHW]))
				print("QZ Scores: " + str(data[j][3+numHW:3+numHW+numQZ]))
				print("MT Scores: " + str(data[j][3+numHW+numQZ:3+numHW+numQZ+numMT]))
				print("LB Scores: " + str(data[j][3+numHW+numQZ+numMT:3+numHW+numQZ+numMT+numLB]))
				print("SP Score : " + str(data[j][3+numHW+numQZ+numMT+numLB]))
				print("FE Score : " + str(data[j][3+numHW+numQZ+numMT+numLB+1]))
		PLine()
		PLine()
		
				
def StudentCheck(gbook,NumStud):
	print("Here is a sanity check.")
	j = 63 #random.randrange(0,NumStud,1)
	print("The gradebook entry for a random student is this:")
	print("Name : " +str(gbook[j][0]))
	print("SID : " +str(gbook[j][1]))
	print("Section : " +str(gbook[j][2]))
	for i in range(0,cHWe-cHWs+1):
		print("HW " + str(i+1) + " score : " + str(gbook[j][3+i]))
	for i in range(0,cQZe-cQZs+1):
		print("QZ " + str(i+1) + " score : " + str(gbook[j][3+cHWe-cHWs+1+i]))
	for i in range(0,cMTe-cMTs+1):
		print("MT " + str(i+1) + " score : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+i]))
	for i in range(0,cLBe-cLBs+1):
		print("LB " + str(i+1) + " score : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+cMTe-cMTs+1+i]))
	print("SP score : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+cMTe-cMTs+1+cLBe-cLBs+1]))
	print("FE score : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+cMTe-cMTs+1+cLBe-cLBs+1+1]))
	print("Taking the course : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+cMTe-cMTs+1+cLBe-cLBs+1+1+1]))
	print("Enrolled in : " + str(gbook[j][3+cHWe-cHWs+1+cQZe-cQZs+1+cMTe-cMTs+1+cLBe-cLBs+1+1+1+1]))
	getID = raw_input("\nManually look to see if this is correct. Is it? (Y/Yes or hit return): ")
	if( (any(x in [getID.upper()] for x in ['Y', 'YES', 'y', 'yes','Yes'])) or not getID ):
		print("OK, checks out! Let's move on.")
	else:
		sys.exit("Well, go figure out why!")
    
    
def CheckLetters(gbook,net):
	for j in range(0,len(net)):
		if( net[j][8]=="X" ): sys.exit("Error: Student " + str(gbook[j][0]) + " (" + gbook[j][1] + ") has no letter grade.")    
    