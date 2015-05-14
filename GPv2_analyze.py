# Import the Config variables
from GPv2_config import *
import GPv2_fileIO as FileIO
import numpy as np

#nethead = ["Homeworks","Quizzes","Midterms","Labs","Participation","Final Exam","Total Course Points","Max Possible Course Points","Letter Grade"]
#netabrev= ["HW","QZ","MT","LB","SP","FE","CP","MCP","LG"]


def PointsToNext(curID,gbook,net):
	if not net[curID][8] in letterNames: 
		return 0
	curGradeIDX = letterNames.index(net[curID][8])
	nextIDX = curGradeIDX-1
	if(nextIDX < 0):
		# They already have an A+ or whatever the highest possible grade is 
		needpoints = 0
	else:
		# They can improve
		percentneed = gradebdys[nextIDX] - net[curID][6]/net[curID][7]
		needpoints = percentneed*net[curID][7]
	return needpoints


def DisplayStudent(curID,gbook,net):
	HWs = 3
	HWe = 3+numHW
	QZs = HWe
	QZe = QZs+numQZ
	MTs = QZe
	MTe = MTs+numMT
	LBs = MTe
	LBe = LBs+numLB
	SPs  = LBe
	FEs  = SPs+1
	# We need to find which row corresponds to this particular student ID
	curLine = -1
	for i in range(0,len(gbook)):
		if(curID == gbook[i][1]):
			curLine = i
			break
	if(curLine == -1): print("Hmm, can't find a student with that ID. Double check and try again.")
	else:
		# Found the student
		print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		print("Name: " + gbook[curLine][0] + " ; SID: " + gbook[curLine][1])
		if(gbook[curLine][2]=="No Section"):
			print("Section: Not Enrolled In A Section")
		else:
			print("Section: " + str(gbook[curLine][2]) + " (GSI: " + GSInames[int(gbook[curLine][2])-101] + ")" ) 
		print("Taking class: " + str(gbook[curLine][22]) )
		print("Enrolled in: " + str(gbook[curLine][23]))
		print("Any prorates? : " + str(net[curLine][9]))
		print(" ")
		print("Raw Scores:")
		print("Homework      : " + str(gbook[curLine][HWs:HWe]))
		print("Quizzes       : " + str(gbook[curLine][QZs:QZe]))
		print("Midterms      : " + str(gbook[curLine][MTs:MTe]))
		print("Labs          : " + str(gbook[curLine][LBs:LBe]))
		print("Participation : " + str(gbook[curLine][SPs:SPs+1]))
		print("Final Exam    : " + str(gbook[curLine][FEs:FEs+1]))
		print(" ")
		print("Course Points:")
		for i in range(0,8): 
			if(nethead[i]=="Labs"): print(nethead[i] + ":\t\t\t" + str(net[curLine][i]))
			elif(nethead[i]=="Max Possible Course Points"): print(nethead[i] + ":\t" + str(net[curLine][i]))
			else: print(nethead[i] + ":\t\t" + str(net[curLine][i]))
		print(nethead[8] + ":\t\t" + str(net[curLine][8]) + " (" + str(100*net[curLine][6]/net[curLine][7]) + "%)" )
		if(net[curLine][10]=='Y'): 
			print("GRADE HAS BEEN OVERWRITTEN!")
		else: 
			print("This student is " + str(PointsToNext(curLine,gbook,net)) + " point(s) away from the next letter grade.") 
		print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		
		
def PrintOptions():
	print("Here are the gradebook options. These are not case-sensitive.\n")
	print("Type D or DISPLAY followed by a space and :")
	print("        an SID to show the gradebook entry for that student.")
	print("        an O to display an array of all the overrides applied thus far.")
	print("        a  P to display all the students with prorated scores.")
	print("        an R to display a new menu to print student rosters for a given section (or see students not in a section).")
	print("        a  Z to enter a menu to display students with zero course points in a particular category.")
	print("        a letter grade (A+, B, C-, etc.) to display all the students getting that grade.")
	print("Type B or BORDER to enter a new menu regarding borderline students.")
	print("Type S or STAT to show the course statistics.")
	print("Type A or ALTER to enter a new menu where you can manually altering student scores.")
	print("Type P or PRINT to enter a new menu where you print various files (including the BearFacts files).")
	print("Type I or INFO to print info regarding the course.")
	print("Type O or OPTIONS to re-print these options.")
	print("Type E or EXIT or Q or QUIT to quit the program.")
	
	
def PrintStats(gbook,net):
	print("\n=================================\nCourse Statistics.")

	Nstud = len(net)
	Nstudf = float(len(net))
	
	# Determines who is taking it PNP first
	PNPnum = 0
	SFnum = 0
	for j in range(0,len(net)):
		if(gbook[j][22]=="PN"): PNPnum = PNPnum + 1
		elif(gbook[j][22]=="SF"): SFnum = SFnum+1 
		
	print("Number of students in the coures: " + str(Nstud) + '\n')
	print("Number of students taking PNP: " + str(PNPnum) + ' (' + str(float(PNPnum)/Nstudf*100) + '%)')
	print("Number of students taking SF : " + str(SFnum) + ' (' + str(float(SFnum)/Nstudf*100) + '%)\n')
	
	print("Regarding Course Points:")
	for i in range(0,6):
		d = []
		for j in range(0,Nstud): d.append(net[j][i])
		npd = np.array(d)
		print(nethead[i] + " mean = " + str(npd.mean()) + " (std = " + str(npd.std()) + ")")
	d = []
	for j in range(0,Nstud): d.append(100*net[j][6]/net[j][7])
	npd = np.array(d)
	# Because of prorates, the mean total course points is not meaningful. Everything really
	# depends on the mean percent. For a quick estimate, you can multiply the percent by totPts
	print("Percent mean = " + str(npd.mean()) + " (std = " + str(npd.std()) + ")\n")
	
	
	print 'The number of students with 0 points in each category:'
	print ("(Note: 0 total course points means they have no grades entered!)")
	for i in range(7):
	    ntemp = 0
	    for j in range(0, Nstud):
	        if net[j][i] == 0:
	            ntemp = ntemp + 1
	    print nethead[i] + ' :\t ' + str(ntemp) + ' out of ' + str(Nstud) + '  (' + str(1.0*ntemp/Nstud*100) + '%)'
	print("\n")
		
	print("The number of students getting a/an:")
	for i in range(len(letterNames)):
		ntemp = 0 
		for j in range(0,Nstud): 
			if(net[j][8]==letterNames[i]): ntemp = ntemp+1
		print(str(letterNames[i]) + " \t: " + str(ntemp) + " out of " + str(Nstud) + '  (' + str(1.0*ntemp/Nstud*100) + '%)' )
	print(" ")	
	
	
	print("The number of students <= 1 point away from getting a/an:")
	for i in range(0,len(letterNames)-1):
		ntemp = 0
		for j in range(0,Nstud):
			if(net[j][10] != 'Y' and net[j][8]==letterNames[i+1]):
				if(PointsToNext(j,gbook,net) < 1.0): ntemp = ntemp + 1
		print(str(letterNames[i]) + " \t: " + str(ntemp) + " out of " + str(Nstud) + '  (' + str(1.0*ntemp/Nstud*100) + '%)' )
	
	print(" ")
	ntemp = 0
	for j in range(0,Nstud):
		if(net[j][10]=='Y'): ntemp = ntemp+1
	print("Num. of manually altered scores: " + str(ntemp))
	
	
	print("\n=================================")
	
	
def DisplayProrates(gbook,net):
	count = 0
	for j in range(0,len(gbook)):
		if(net[j][9]): 
			print(gbook[j][0] + " has the following prorates: " + str(net[j][9]))
			count = count + 1
	if(count==0): print("There are 0 students with prorates.")
	else: print("There is/are " + str(count) + " student(s) with prorates.")
		
def getLetter(curGrade,gradebdys):
	retGrade = letterNames[-1]
	for i in range(0,len(letterNames)):
		if( curGrade >= gradebdys[i] ):
			retGrade = letterNames[i]
			break
	return retGrade
	
		
def PrintBorder(gbook,net,curgrade,npoints):
	#First find the boundary corresponding to the curgrade
	curidx = letterNames.index(curgrade)
	count = 0
	print("\nWith " + str(npoints) + " more point(s), the following students' grade will change from " + letterNames[curidx+1] + " to " + curgrade + ":")
	for j in range(0,len(net)):
		if( net[j][8]==letterNames[curidx+1] ):
			if( curgrade == getLetter( (npoints+net[j][6])/net[j][7],gradebdys) ):
				# Student will have a different letter grade
				print(gbook[j][0] + " (" + gbook[j][1] + ") needs " + str(PointsToNext(j,gbook,net)) + " more points")
				count = count+1
	if(count==0): print("No students' grade will change.")
	else: print("\nThere is/are " + str(count) + " student(s) whose grade will change with " + str(npoints) + " more point(s).")
			
def DisplayLetterGrade(curLetter,gbook,net):
	print('The following students have a grade of ' + curLetter + " : " )
	count = 0
	for j in range(0,len(net)):
		if(curLetter == net[j][8]):
			print( gbook[j][0] + " (" + gbook[j][1] + " ; " + str(PointsToNext(j,gbook,net)) + " points needed to increase)" )
			count = count+1
	if(count==0): print("No students with that letter grade.")
	else: print("\nThere are " + str(count) + " students getting a(n) " + curLetter + " in the course.")
		
	
def PrintFiles(gbook,net):
	print("Let's print some files.")
	print("Do you want to print the BearFacts files (type: BEAR),") 
	print("Do you want to print single-column data (type anything else),")
	choice = raw_input("or do you want to go back (hit return)? : ")
	if not choice:
		print "Returning to main menu."
	elif( any(x in [choice.upper()] for x in ['BEAR','B','BEARFACTS']) ):
		BearFacts(gbook,net)
	else:
		print("Either you mistyped or you don't want a BearFacts file. ")
		print("So I'll assume you want a single-column file.")
		print("What category? " + str(netabrev))
		print("You can also type SEC if you want the sum of HW + QZ + SP")
		choice = raw_input("Pick one: ")		
		if( any(x in [choice.upper()] for x in netabrev + ['SEC']) ):
			if(choice.upper() == 'SEC'): idx = -1
			else: idx = netabrev.index(choice.upper())
			print("Ok, printing a file for the " + choice.upper())
			FileIO.Single(net,choice.upper())
		else:
			print("Invalid choice. Returning to main menu.")
	
def DisplayRoster(gbook,net):
	print("Let's display the roster of students for particular sections.")
	choice = raw_input("Enter a section number (101, 103, etc.) or 'None' for those not in a section: ")
	choice2 = raw_input("Display final grades for each student? (Y/YES): ")
	if not choice2: pgrade = False
	elif( any(x in [choice2.upper().replace(" ","")] for x in ['Y','YES']) ): pgrade = True
	else: pgrade = False
	
	info1 = "Letter Grade = taking for letter grade, PN = taking PNP, SF = taking SF"
	info2 = "Using current grade boundaries, letter grade and number of points to next score is shown at end."
	
	if ( (not choice) or (any(x in [choice.replace(" ","").upper()] for x in ['NO','NONE'])) ):
		print("\nHere are the students no enrolled in a discussion section")
		for j in range(0,len(net)):
			if( gbook[j][2]=="No Section"):
				pme = gbook[j][0] + " (" + gbook[j][1] + " ; " + str(gbook[j][22]) + ")"
				if(pgrade): pme = pme + " has " + str(net[j][6]) + " out of " + str(net[j][7]) + " course points. (" + net[j][8] + " ; " + str(PointsToNext(j,gbook,net)) + " to next grade)" 
				print( pme )
				if(net[j][10]=='Y'): print("       ^-- Final grade has been overwritten.")
		print('\n'+info1)
		print(info2)
	elif( int(choice.replace(" ","")) in range(101,101+numSections) ):
		curSec = int(choice.replace(" ",""))
		print("\nHere are the students in section " + str(curSec) + " (GSI: " + GSInames[curSec-101] + ")")
		for j in range(0,len(net)):
			if( gbook[j][2]==str(curSec) ):
				pme = gbook[j][0] + " (" + gbook[j][1] + " ; " + str(gbook[j][22]) + ")"
				if(pgrade): pme = pme + " has " + str(net[j][6]) + " out of " + str(net[j][7]) + " course points. (" + net[j][8] + " ; " + str(PointsToNext(j,gbook,net)) + " to next grade)"
				print(pme)
				if(net[j][10]=='Y'): print("       ^-- Final grade has been overwritten.")
		print('\n'+info1)
		print(info2)
	else:
		print("Invalid section number. Womp. Returning to main menu.")
	
		
def BearFacts(gbook,net):
	print("Let's prepare to print the files for BearFacts")
	print("The idea here is that it'll open up the BearFacts files it read in earlier again,")
	print("this time filling in the grade column with the appropriate grade.")
	print("In making these files, it'll replace letter grades with PNP or SF where appropriate.")
	print("The minimum grade to pass for PNP is : " + PNPmin)
	print("The minimum grade to pass for SF  is : " + SFmin)
	choice = raw_input("Would you like to make the BearFacts files now? (Yes/Y) : ")
	if( any(x in [choice.upper()] for x in ['Y','YES']) ):
		print("OK, here we go....")
		FileIO.BearFactsFinal(gbook,net)
	else:
		print("OK, returning to main menu.")
	
def PrintOverrides():
	print("Here's the array of overrides applied thus far: " + str(Overrides))
	print("Feel free to copy and paste this into the config file.")
				
def Zeros(gbook,net,cat):
	idx = netabrev.index(cat)
	count = 0
	sort = raw_input("Sort by section? (Y/Yes) : ")
	if not sort: sort = "N"
	print("\nThe following students have 0 course points in the " + nethead[idx] + " category.")
	if( any(x in [sort.upper().replace(" ","")] for x in ['Y','YES']) ):
		for i in range(101,101+len(GSInames)):
			for j in range(0,len(net)):
				if( net[j][idx]==0.0 and gbook[j][2]==str(i) ):
					print(gbook[j][0] + " (" + gbook[j][1] + ") in section " + gbook[j][2] + " (" + GSInames[int(gbook[j][2])-101] + ")")
					if(net[j][10]=='Y'): print("       ^-- Final grade has been overwritten.")
					count = count + 1
			print("")
		for j in range(0,len(net)):
			if( net[j][idx]==0.0 and gbook[j][2]=="No Section"):
				print(gbook[j][0] + " (" + gbook[j][1] + ") in no section")
				if(net[j][10]=='Y'): print("       ^-- Final grade has been overwritten.")
				count = count + 1
	else:	
		for j in range(0,len(net)):
			if( net[j][idx] == 0.0 ): 
				if(gbook[j][2] == "No Section"): print(gbook[j][0] + " (" + gbook[j][1] + ") in no section")
				else: print(gbook[j][0] + " (" + gbook[j][1] + ") in section " + gbook[j][2] + " (" + GSInames[int(gbook[j][2])-101] + ")")
				if(net[j][10]=='Y'): print("       ^-- Final grade has been overwritten.")
				count = count + 1
	if(count==0): print("\nNo students with zeros.")
	else: print("\nThere are " + str(count) + " students with zeros in " + nethead[idx])
		
def AlterScore(net,gbook):
	print ("You're in the menu to alter student scores. Please be careful!")
	sid = raw_input("Enter the SID of the student you want to alter. : ")
	idx = -1
	for j in range(0,len(net)):
		if(sid == gbook[j][1]):
			idx = j
			break
	if(idx > -1):
		print("Ok, found the student. Here's their gradebook entry:")
		DisplayStudent(sid,gbook,net)
		check = raw_input("Now, do you want to alter their grade? (YES/Y) : ")
		if( any(x in [check.upper()] for x in ['Y','YES']) ):
			print("What do you want to change their grade to?")
			print("Chose from : " + str(letterNames+peskyletterNames) )
			check = raw_input("New grade : ")
			if( any(x in [check.upper()] for x in letterNames+peskyletterNames) ):
				print("You want to change the grade for " + gbook[idx][0] + " from " + net[idx][8] + " to " + check.upper())
				confirm = raw_input("Is this correct? (YES/Y) : ")
				if( any(x in [confirm.upper()] for x in ['Y','YES']) ):
					confirm = raw_input("Are you absolutely sure?! (Y/YES) : ")
					if( any(x in [confirm.upper()] for x in ['Y','YES']) ):
						print("Ok, changing the grade!!!!")
						net[idx][8] = check
						net[idx][10] = 'Y'
						Overrides.append([sid,check])
					else:
						print("Abandon ship!")
				else:
					print("Abandon ship!")
			else:
				print("Can't understand the desired letter.")
		else:
			print("Abandon ship!")
	else:
		print("Can't find that student. Try again. Again, be careful!")
		
		
		
def PrintInfo(gbook,net,numStudents):
	# Determines who is taking it PNP first
	PNPnum = 0
	SFnum = 0
	for j in range(0,len(net)):
		if(gbook[j][22]=="PN"): PNPnum = PNPnum + 1
		elif(gbook[j][22]=="SF"): SFnum = SFnum+1 
	print("Here's some course info.")
	print("")
	print("There are " + str(numStudents[0]+numStudents[1]) + " students in the course.")
	print("    " + str(numStudents[0]) + " are in C10")
	print("    " + str(numStudents[1]) + " are in L&S")
	print("    " + str(PNPnum) + " are taking it PNP.")
	print("    " + str(SFnum)  + " are taking it SF.")
	print("")
	print("Here is a list of people that were on both teams:")
	print("Alex Filippenko")
	print("")
	print("Here are the grade boundaries:")
	print("Course points assumes the course is out of " + str(totPTs) + " (parentheses show percentages):")
	for j in range(0,len(letterNames)):
		print(letterNames[j] + " requires >= " + str(gradeBoundaries[j]) + " (" + str(100.0*gradeBoundaries[j]/totPTs) + "%)")
	print("")
	print("There are " + str(numSections) + " discussion sections.")
	print("Here are the GSI sections:")
	for j in range(0,len(GSInames)):
		print("Section " + str(101+j) + " : " + GSInames[j])