import sys
import csv

# Import the Config variables
from GPv2_config import *





# Reads in and prepares the raw student scores.
def GetRawData(data,headrow):
    f = open(gradebookFile,"rbU")
    cr = csv.reader(f)
    ''' Read in row by row '''
    i = 1
    for row in cr:
        if(i < startRowNum):
            if(i==headerRowNum):
                headrow.append(row[cNM-1])
                headrow.append(row[cID-1])
                headrow.append(row[cSE-1])
                for j in range(cHWs,cHWe+1): headrow.append(row[j-1])
                for j in range(cQZs,cQZe+1): headrow.append(row[j-1])
                for j in range(cMTs,cMTe+1): headrow.append(row[j-1])
                for j in range(cLBs,cLBe+1): headrow.append(row[j-1])
                headrow.append(row[cSP-1])
                headrow.append(row[cFE-1])
            else:
                if(chatty): print("Skipping row " + str(i))
        else:
            currow = []
            currow.append(row[cNM-1])
            currow.append(row[cID-1])
            currow.append(row[cSE-1])
            for j in range(cHWs,cHWe+1): currow.append(row[j-1])
            for j in range(cQZs,cQZe+1): currow.append(row[j-1])
            for j in range(cMTs,cMTe+1): currow.append(row[j-1])
            for j in range(cLBs,cLBe+1): currow.append(row[j-1])
            currow.append(row[cSP-1])
            currow.append(row[cFE-1])
            data.append(currow)
        i = i+1
    f.close()
    del cr,f
    ''' Now let's go through and format the data. From this point on, it's assumed the 
        data is formated in the order given above.  '''
    for i in range(0,len(data)):
        ''' Make the name all caps '''
        data[i][0] = (data[i][0]).upper()
        ''' Format the SID. Some have a UID prefix that needs to be removed 
            The SID is the primary identifier of students in this program. 
            We want to make sure we do not alter it in any way. We keep it as a string
            for this reason. '''
        if(data[i][1][0:4] == "UID:"): data[i][1] = data[i][1][5:]
        ''' Section Number. The formating of this line will likely change from year to
            year. You may have to remove more or less depending on how you (the head GSI)
            formated the sections on bCourses. '''
        if(data[i][2][0] == "1"): data[i][2] = data[i][2][0:3]
        else: data[i][2] = "No Section"
        ''' Homework, Quizzes, Midterms, Labs, Section Participation, and Final Exam Scores.
            If an entry is empty, replace it with a zero. Make everything a float. '''
        for j in range(3,len(data[0])):
            if not data[i][j]:
            	data[i][j] = 0.0
            else:
            	data[i][j] = float(data[i][j])
        

# Reads in type of grade each student is getting (letter, PNP, SF)
def GetGradeType(data,types,numStudents):
	f = open(gradeTypeC10File,"rbU")
	cr = csv.reader(f)
	i = 1
	for row in cr:
		if(i< startTypeRowNum): 
			if(chatty): print("Skipping row " + str(i))
		else:
			''' Ignore the line that starts with "Concurrent..." '''
			if(row[0][0]=="C"): 
				if(chatty): print("Skipping concurrent title row")
			else:
				currow = []
				currow.append(row[cTypeNM-1])
				currow.append(row[cTypeID-1])
				currow.append(row[cTypeCC-1])
				currow.append("C10")
				types.append(currow)
				numStudents[0] = numStudents[0] + 1
		i = i+1
	f.close()
	del f,cr
	f = open(gradeTypeLaSFile,"rbU")
	cr = csv.reader(f)
	i = 1
	for row in cr:
		if(i< startTypeRowNum): 
			if(chatty): print("Skipping row " + str(i))
		else:
			''' Ignore the line that starts with "Concurrent..." '''
			if(row[0][0]=="C"): 
				if(chatty): print("Skipping concurrent title row")
			else:
				currow = []
				currow.append(row[cTypeNM-1])
				currow.append(row[cTypeID-1])
				currow.append(row[cTypeCC-1])
				currow.append("LS")
				types.append(currow)
				numStudents[1] = numStudents[1] + 1
		i = i+1
	f.close()
	del cr, f
	print("C10 students: " + str(numStudents[0]) + " and in L and S : " + str(numStudents[1]))
	''' Now let's format '''
	for row in types:
		''' Uppercase the name '''
		row[0] = row[0].upper()
		''' Seems like the IDs are all sane and don't need to be adjusted. Double check'''
		row[1] = row[1]
		''' If no grade entry is given, they want a letter grade. Input an L. As of now
		    it looks like the BearFacts file puts a space here rather than leaving it blank.
		    You might need to adjust this if BearFacts changes. '''
		if row[2][0]==" " : row[2] = "Letter Grade"
	''' Get it into alphabetical order (sorts by first entry of list)'''
	types.sort()
	
	
	
def BearFactsFinal(gbook,net,gradebdys):
	fc10 = open("C10BearFacts_final.csv","w")
	flas = open("LaSBearFacts_final.csv","w")
	c10Printed = 0
	lasPrinted = 0
	for j in range(0,len(net)):
		curGrade = net[j][8]
		if(gbook[j][22]=="PN" and net[j][10]=="N"): 
			if( letterNames.index(curGrade) <= letterNames.index(PNPmin) ):
				curGrade = "P"
			else:
				curGrade = "N"
		if(gbook[j][22]=="SF" and net[j][10]=="N"): 
			if( letterNames.index(curGrade) <= letterNames.index(SFmin) ):
				curGrade = "S"
			else:
				curGrade = "F"
		if(gbook[j][23]=="C10"):
			#print this in C10 file
			fc10.write( gbook[j][0] + " , " + curGrade + '\n' )
			c10Printed = c10Printed + 1
		elif(gbook[j][23]=="LS"):
			#print this in LS file
			flas.write( gbook[j][0] + " , " + curGrade + '\n' )
			lasPrinted = lasPrinted + 1
		else:
			sys.exit("Doesn't know which class " + gbook[j][0] + " (" + gbook[j][1] + ") is in!")
	fc10.close()
	flas.close()
	print("C10 students: " + str(c10Printed) + " and in L and S : " + str(lasPrinted))
			



	