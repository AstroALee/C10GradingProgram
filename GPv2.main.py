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




# Welcome Message
CheckBalance.Welcome()

# Let's first check to make sure the config file is OK.
print "Let's look at the config file and make sure everything looks OK. Wouldn't want"
print "to continue on if you accidentally made an A+ impossible to achieve, or if you"
print "forgot to rename one of the BearFacts files. That would be embarassing."
print ""
CheckBalance.ConfigChecks()
print ""
print "Hey! It looks like the config file checked out. Don't get cocky. That doesn't"
print "mean everything is perfect, but it's a good first step." 
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")

# Prepares the list of percentages that determine the final letter grade
# This is the same as the course point gradeBoundaries array in the config file
# but converted to percentages. 
print "\nNow with the config file out of the way, let's prepare some grade boundaries."
print "All letter grades in this course are determined by overall percentages. Alex will"
print "give you grade boundaries in terms of course points, assuming no prorates. But in"
print "order to make the same boundaries apply to students with prorates, we will first"
print "convert the boundaries into percentages. It is these percentages that will be use"
print "to determine everyone's letter grade, prorate or not."
print ""
CheckBalance.PrepGrades(gradebdys)
print ""
print "Grade boundaries are now prepared."
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")


# Assuming all is OK at this point, let's read in the raw student data. The
# list 'data' is the raw data.
print "\n With that out of the way, let's get that student data! We will open the raw"
print "grade book file from bCourses or whatever and read that into a giant array."
data=[]
headrow=[]
print ""
FileIO.GetRawData(data,headrow)
print ""
print "Guess what? Student data is read in and prepared!"
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")


# Next step is to read in the BearFacts files and grab their grade type
types=[]
numStudents = [0,0,0]
print("\n Now let's look at the BearFacts files. We'll see which students want to take")
print("the class PNP or SF.")
print ""
FileIO.GetGradeType(data,types,numStudents)
print ""
print("OK, all the slackers are now accounted for.")
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")


# Next is to combine these lists to make the master gradebook file
print("\nNow we need to do some work. Let's make the gradebook. Here we will construct")
print("a grade book entry for every student in the BearFacts files. You should quickly")
print("look through all the entries that are printed after this message. Those entries")
print("are names from bCourses but are not in the official UCB BearFacts files.")
print("Many of these entries are probably auditors, visitors, and whatnot. But some")
print("might be students who have been turning in assignments are not actually enrolled")
print("in the course!")
gbook = []
CheckBalance.MakeGradeBook(data,types,gbook)
print("\nGradebook is now made! Oh yeah....\n")
del data, types
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")


numStud = len(gbook)
numStudents[2] = numStud
PLine()
print "By the way, there are " + str(numStud) + " students in the class."
print "Of these, " + str(numStudents[0]) + " are enrolled in C10."
print "Of these, " + str(numStudents[1]) + " are enrolled in L&S.\n"
PLine()
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")


# This is a good moment for a sanity check.
if not(confident): CheckBalance.StudentCheck(gbook,numStud)


# Now we can finally do some calculations
# For each entry in the gbook, we'll compute homework totals, quiz totals, etc. and
# convert to course points. 

# zero entries are for hw, quiz, mt, labs, sp, final, course pts, max course pts
# array is for any prorates that are done
# Final letter marks if the score was manually overridden 
netScores = [ [0,0,0,0,0,0,0,0,"X",[],"N"] for i in range(numStud) ]

PLine()
print("No let's do some calculations.")
print("Calculating course points from gradebook...")
for i in range(0,numStud): Calculate.CoursePoints(gbook[i],netScores[i])
print("... Course Points calculated. Calculating letter grades...")
for i in range(0,numStud): Calculate.LetterGrades(netScores[i],letterNames)
print("... Letter Grades calculated. Note that we will not convert grades to PNP or SF")
print("until we print the final files for BearFacts. Anyway, now applying overrides...")
Calculate.ApplyOverrides(netScores,gbook)
print("... Overrides applied. Double-Checking to make sure all students have a letter grade...")
CheckBalance.CheckLetters(gbook,netScores)
print("... and... and! ... and!!!! .... Grades calculated!\n")
if not confident: checkin = raw_input("\nHit return to continue. If something's wrong, engage the pro-choice option with Control-C.")



# Here is where the GUI starts. It's a while look that is only exited when you want to exit
# the program.
PLine()
print("OK, we're done. Let's look at the data.")

GUI.PrintOptions()
while True:
	PLine()
	print("\nWelcome to the main menu.")
	resp = raw_input("What should we do?: ")
	if not resp.replace(" ",""):
		# Entered nothing.
		print("Type O to see the available options.")
	elif( any(x in [resp.upper()] for x in ['E','Q','QUIT','EXIT']) ):
		break
	elif( any(x in [resp.upper()] for x in ['I','INFO']) ):
		GUI.PrintInfo(gbook,netScores,numStudents)
	elif( any(x in [resp.upper()] for x in ['O','OPTIONS','OPTION']) ):
		GUI.PrintOptions()
	elif( any(x in [resp.upper()] for x in ['P','PRINT','BEARFACTS']) ):
		GUI.PrintFiles(gbook,netScores)
	elif( any(x in [resp.upper()] for x in ['S','STATS','STAT']) ):
		GUI.PrintStats(gbook,netScores)	
	elif( any(x in [resp.upper()] for x in ['A','ALTER']) ):
		GUI.AlterScore(netScores,gbook)	
	elif( any(x in [resp.split()[0].upper()] for x in ['D','DISPLAY']) ):
		if(len(resp.split()) > 1):
			if(any(x in [resp.split()[1].upper()] for x in ['O','OVERRIDE','OVERRIDES']) ):
				GUI.PrintOverrides()
			elif(any(x in [resp.split()[1].upper()] for x in ['P','PRORATE','PRORATES']) ):
				GUI.DisplayProrates(gbook,netScores)
			elif(any(x in [resp.split()[1].upper()] for x in peskyletterNames+letterNames) ):
				GUI.DisplayLetterGrade(resp.split()[1].upper(),gbook,netScores)
			elif( any(x in [resp.split()[1].upper()] for x in ['Z','ZERO','ZEROS']) ):
				gd = raw_input("Enter a category: " + str(netabrev[0:8]) + " : ")
				gd = gd.replace(" ","").upper()
				if( gd in netabrev):
					GUI.Zeros(gbook,netScores,gd.upper())
				else:
					print("Invalid category.")
			else:
				GUI.DisplayStudent(resp.split()[1],gbook,netScores)
		else:
			print("Display needs multiple arguments, foo. Try again.")
	elif( any(x in [resp.upper()] for x in ['B','BORDER','BORDERS']) ):
		print("Let's see how many students are just shy of earning the following grade.")
		gd = raw_input("Enter a letter grade (A+, B, etc.): ")
		nm = raw_input("How many points need students be away from earning this grade?: ")
		gd = gd.upper()
		if(gd in letterNames):
			if(int(nm) > 0):
				if(gd==letterNames[-1]):
					print("Borderline from getting an " + letterNames[-1] + "? That's weird.")
				else:
					GUI.PrintBorder(gbook,netScores,gd,int(nm))
			else:
				print("Invalid number of boundary points.")
		else:
			print("Invalid letter name. Choose one from " + str(letterNames))
		
	else:
		print("Invalid Option. Try again. (You can view the available options by typing the letter O)")



print("\n\nToodles! Hope Alex isn't giving you a hard time. It'll all be over soon.")

