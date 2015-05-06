'''
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Python Grading Program for Astronomy C10 with Filippenko
    =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
'''

import sys

# Import the Config variables
from GPv2_config import *

# Import various modules. If you change the file names, make sure they are
# correctly written here.
import GPv2_checks as CheckBalance
import GPv2_fileIO as FileIO
import GPv2_calc as Calculate
import GPv2_analyze as GUI


# Let's first check to make sure the config file is OK.
print '\n\n\n'
CheckBalance.ConfigChecks()


# Prepares the list of percentages that determine the final letter grade
# This is the same as the course point gradeBoundaries array in the config file
# but converted to percentages. 
print "Now let's prepare some grade boundaries"
gradebdys = [0.0]*len(gradeBoundaries)
CheckBalance.PrepGrades(gradebdys)
print "Grade boundaries are prepared.\n"


# Assuming all is OK at this point, let's read in the raw student data. The
# list 'data' is the raw data.
print "All seems well. Let's get that student data!"
data=[]
headrow=[]
FileIO.GetRawData(data,headrow)
print "Guess what? Student data is read in and prepared!\n"


# Next step is to read in the BearFacts files and grab their grade type
types=[]
numStudents = [0,0,0]
print("Let's see which students want to take the place PNP.")
FileIO.GetGradeType(data,types,numStudents)
print("All the slackers are now accounted for.\n")


# Next is to combine these lists to make the master gradebook file
print("Let's made the gradebook.")
gbook = []
CheckBalance.MakeGradeBook(data,types,gbook)
print("Gradebook is now made! Oh yeah....\n")
del data, types

numStud = len(gbook)
numStudents[2] = numStud
print "By the way, there are " + str(numStud) + " students in the class."
print "Of these, " + str(numStudents[0]) + " are enrolled in C10."
print "Of these, " + str(numStudents[1]) + " are enrolled in L&S.\n"

# This is a good moment for a sanity check.
if not(confident): CheckBalance.StudentCheck(gbook,numStud)


# Now we can finally do some calculations
# For each entry in the gbook, we'll compute homework totals, quiz totals, etc. and
# convert to course points. 

# zero entries are for hw, quiz, mt, labs, sp, final, course pts, max course pts
# array is for any prorates that are done
# Final letter marks if the score was manually overridden 
netScores = [ [0,0,0,0,0,0,0,0,"X",[],"N"] for i in range(numStud) ]

print("Calculating course points from gradebook.")
for i in range(0,numStud): Calculate.CoursePoints(gbook[i],netScores[i])
print("Calculating letter grades.")
for i in range(0,numStud): Calculate.LetterGrades(netScores[i],gradebdys,letterNames)
print("Applying overrides.")
Calculate.ApplyOverrides(netScores,gbook)
print("Checking to make sure all grades were written.")
CheckBalance.CheckLetters(gbook,netScores)
print("Grades calculated!")



# Here is where the GUI starts. It's a while look that is only exited when you want to exit
# the program.
print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- ")
print("OK, we're done. Let's look at the data.")

GUI.PrintOptions()
while True:
	print("\nWelcome to the main menu.")
	resp = raw_input("\nWhat should we do?: ")
	if( any(x in [resp.upper()] for x in ['E','Q','QUIT','EXIT']) ):
		break
	elif( any(x in [resp.upper()] for x in ['I','INFO']) ):
		GUI.PrintInfo(gbook,netScores,gradebdys)
	elif( any(x in [resp.upper()] for x in ['O','OPTIONS','OPTION']) ):
		GUI.PrintOptions()
	elif( any(x in [resp.upper()] for x in ['P','PRINT','BEARFACTS']) ):
		GUI.PrintFiles(gbook,netScores,gradebdys)
	elif( any(x in [resp.upper()] for x in ['S','STATS','STAT']) ):
		GUI.PrintStats(gbook,netScores)	
	elif( any(x in [resp.upper()] for x in ['A','ALTER']) ):
		GUI.AlterScore(netScores,gbook)	
	elif( any(x in [resp.split()[0].upper()] for x in ['D','DISPLAY']) ):
		if(len(resp.split()) > 1):
			if(any(x in [resp.split()[1].upper()] for x in ['O','OVERRIDE','OVERRIDES']) ):
				print("Here's the array of overrides applied thus far: " + str(Overrides))
				print("Feel free to copy and paste this into the config file.")
			elif(any(x in [resp.split()[1].upper()] for x in ['P','PRORATE','PRORATES']) ):
				GUI.DisplayProrates(gbook,netScores)
			elif(any(x in [resp.split()[1].upper()] for x in letterNames) ):
				GUI.DisplayLetterGrade(resp.split()[1].upper(),gbook,netScores)
			elif( any(x in [resp.split()[1].upper()] for x in ['Z','ZERO','ZEROS']) ):
				gd = raw_input("Enter a category: " + str(netabrev[0:8]) + " : ")
				if( gd.upper() in netabrev):
					GUI.Zeros(gbook,netScores,gd.upper())
				else:
					print("Invalid category.")
			else:
				GUI.DisplayStudent(resp.split()[1],gbook,netScores)
		else:
			print("Display needs multiple arguments. Try again.")
	elif( any(x in [resp.upper()] for x in ['B','BORDER','BORDERS']) ):
		gd = raw_input("Enter a letter grade (A+, B, etc.): ")
		nm = raw_input("How many points need students be away from earning this grade?: ")
		gd = gd.upper()
		if(gd in letterNames):
			if(int(nm) > 0):
				if(gd==letterNames[-1]):
					print("Borderline from getting an " + letterNames[-1] + "? That's weird.")
				else:
					GUI.PrintBorder(gbook,netScores,gd,int(nm),gradebdys)
			else:
				print("Invalid number of boundary points.")
		else:
			print("Invalid letter name. Choose one from " + str(letterNames))
		
	else:
		print("Invalid Option. Try again. (You can view the available options by typing the letter O)")



print("Toodles! Hope Alex isn't giving you a hard time.")

#GUI.DisplayStudent("22744867",gbook,netScores)

