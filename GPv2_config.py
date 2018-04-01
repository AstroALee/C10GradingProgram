# Config File for C10 Grading Program, v2.0    #
# -------------------------------------------- #
# Originally written by Aaron Lee, Spring 2015 #
# and edited by future head GSIs
#
#
# Modifiers of this program should take care with the following:
#
# (1) Readability:   New functionality should be heavily commented and clear.
# (2) Plausibility:  New functionality and changes should make sense in the broad
#                    scheme of things. Little minute additions should no go into
#                    the main() program but should be placed in their own self-
#                    contained module, for example. A function that draws a
#                    comet on the screen has no place in this program.
# (3) Adaptability:  Avoid hard-coding values into functions as much as possible.
#                    Everything should be adaptable and capable of evolution.
#                    Numbers that will change from year to year should be defined
#                    in this config file.
# (4) Functionality: Copious error-checking is encouraged. These are students'
#                    final grades we are dealing with here!
#
#
#
#
# Welcome to the Astro C10 Grading Program! This program is designed to take
# care of all the final course grade determinations, taking into accounts pesky
# things like dropping lowest scores for homework and midterms, prorating,
# identifying students on grade boundaries, and preparing the files that are
# ultimately uploaded to BearFacts. This CONFIG file will hopefully be the only
# file you need to significantly change from year to year. Modifications to
# the other files should obey the four pillars of good coding* above.
#
# * - Aaron Lee made these up on the spot, they are by no means universal.
#
#
# Some commonly used abbreviations:
# ID or sID = student ID number
# NM or sNM = student name
# FE = final exam,  LB = labs,   QZ = quizzes,   MT = midterms
# HW = homework,    SP = section participation
#
#
# Here are some global variable arrays we'll need. Don't alter these.
nethead = ["Homeworks","Quizzes","Midterms","Labs   ","Participation","Final Exam","Total Course Points","Max Possible Course Points","Letter Grade"]
netabrev= ["HW","QZ","MT","LB","SP","FE","CP","MCP","LG"]
#
#
# Before we get started, let's make sure all our files are in order.
#
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                  FILE NAMES
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
#
# This is the name of the .csv file you download directly from bCourses.
# This is the file that contains all the raw scores for every student.
#
gradebookFile = 'mastergradebook.csv'
#
# These are the names of the .csv files you download from BearFacts.
# It contains information regarding which students are taking the course for a
# grade, are PNP, are SF, etc.
# Since this class is crosslisted, there is going to be a file for C10 and L&S.
# To get it, you must have Faculty access to BearFacts. Ask Alex.
# Then for both the full C10 and the full L&S, in the dropdown menu for "Action"
# select "Create Grade Roster". The CSV file should then download.
# Note this file is the format we will need the outputs to look like for
# successful upload to BearFacts.
#
gradeTypeC10File = 'gradesheetC10.csv'
gradeTypeLaSFile = 'gradesheetLaS.csv'
#
#
# If you print single-column files, here is the header of the file name:
# e.g., singlecolumnhead = 'allstudents' will produce a single-column file of homework
# scores called 'allstudents_HW.txt'
singlecolumnhead = 'allstudents'
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                  FILE FORMATS
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# gradebookFile will (hopefully) always be a bunch of headers followed by
# many rows of raw scores for each student. Here we provide information to the
# grading program about which columns have what data.
#
#
# The first thing we'll need to get from the gradebookFile is the headers. What
# row is the header information located on (start counting from 1, not 0). In a
# sane world, this number will always be 1.
headerRowNum = 1
#
# Now there might be some rows between the header and the student data that we
# want to ignore . bCourses or whatever might fill this with random stuff.
# What row number does actual gradebook data start on?
startRowNum = 3
#
# Good. Now which columns correspond to what? This is going to assume that the
# columns for particular assignments are all next to one another. For example,
# both columns for the two quizzes are adjacent columns, rather than the column
# for Quiz 1 being far from the column for Quiz 2. If this is not the case, you
# might manually adjust the CSV file so this is the case.
#
# Which column has student names (again, start counting from 1, not 0).
cNM = 1
# Which column has the student SIS or UID?
cID = 3
# Which column has section information?
cSE = 5
# Which are the start and end columns for homework?
cHWs = 6
cHWe = 16
# Start and end columns for quizzes?
cQZs = 17
cQZe = 18
# Start and end columns for labs?
cLBs = 19
cLBe = 19
# Start and end columns for midterms?
cMTs = 20
cMTe = 22
# Column for section participation?
cSP  = 23
# Column for Final Exam?
cFE  = 24
#
#
# The number of columns determines the number of unique assignments.
numHW = cHWe-cHWs+1
numQZ = cQZe-cQZs+1
numLB = cLBe-cLBs+1
numMT = cMTe-cMTs+1
# The total number of assignments
numAssign = numHW+numQZ+numLB+numMT+2
#
# OK, now we need to read in information from the gradeTypeXXXFiles.
#
# Which row is the header information?
headerTypeRowNum = 1
#
# What row does student data start on?
startTypeRowNum = 2
#
# For checks and balances, let's read in the student IDs and names again.
#
# Which column is the SID? Name?
cTypeID = 1
cTypeNM = 5
#
# Finally, which column gives the credit code?
cTypeCC = 4
#
# That should give us everything we need!
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                                  Section information
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# How many sections are there?
numSections = 26
#
# Input the names of the GSIs for each section, in the correct order
# (e.g., section 101, 102, 103, ... , 126)
GSInames = ['Carina','Jesse','Aaron','Brianna','Nat','Nat','Jesse','Carina','Brianna','Aaron','Jesse','Aaron','Kaylan','Kaylan','Alwin','Avery','Kevin','Kyle','Aaron','Alwin','Kyle','Kaylan','Kaylan','Avery','Jesse','Kevin']
#
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                         Course assignment information
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
#
# Let's first focus on course points. For each item, tell me the TOTAL number
# of course points available (again, the total, not the points / assignment).
cpHW = 23
cpQZ = 14
cpMT = 50
cpSP =  3
cpLB = 15
cpFE = 75
#
# The total course points is the sum. Make sure in the diagnostics page that this
# number matches what you think it should be (traditionally = 180)
totPTs = cpHW + cpQZ + cpMT + cpSP + cpLB + cpFE
#
#
# For which of these assignments are prorates possible? When the score exceeds
# the maximum possible points for that assignment, it will be prorated. Errors
# will be thrown if the assignment is over the max but not in the below list.
prorateMe = ['QZ','MT']
#
#
# Maximum Number of Points for each assignment
maxHW = 50
maxQZ = 50
maxMT = 25
maxLB = 15
maxSP = 3
maxFE = 75
#
#
# (Note: the number of each assignment is based on how many columns there are above)
#
# How many scores are we keeping in various categories? The assumption is that we
# will drop the lowest scores (including missing scores).
#
# How many homeworks are we keeping?
keepHW = 8
#
# How many midterms are we keeping?
keepMT = 2
#
#
#
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                         Course grade information
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# Here are those letter grades that mean so much to the students.
letterNames   = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
#
# And the weird letter names
peskyletterNames = ['P','N','S','I']
#
# Now this is where shiz gets serious. You need to enter the grade boundaries for
# each letter grade. For example, if the first letter name above is 'A+', then
# the first entry of this array is the minimum number of course points needed to
# get an A+. If the second entry is 'A', the second number here is the minimum
# number of course points needed to get an A, assuming they are not getting an A+
#
gradeBoundaries = [162,150,144,137,125,119,114,102,92,87,82,73,0]
#
#
# Identify the minimum letter grade for PNP to pass
PNPmin = "C-"
#
# Identify the minimum letter grade for SF to ... "be satisfactory" 
SFmin = "B-"
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#                          Overrides and Verbosity
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#
# Sometimes we might want to manually change a student's grade. You will be able
# to do that in the grading program. However, if you exit the program and restart
# it later on, you can manually enter all the overrides below, and they will be
# automatically applied at the start of the grading program. Elements of this
# array are arrays of SID and the new letter grade.
# Example: Overrides = [ ['24149505',"A-"] , ['24149494',"A-"] ]
Overrides = [ ['23843637','I'] ]
#
#
# You may also not want to re-confirm that everything checks out before reading
# in files and such. You can automatically accept the results of the checks
# and balances by being confident (boolean: True or False).
confident = True
#
#
# You can also have more outputs to the screen when preparing the data. If you want
# a chatty program, let it know so here  (boolean: True or False).
chatty = False
#
#
#
# That's it. Below are some comments on where else in the code you might have to change. 
#
#
#
#
#
# Print a line function
def PLine():
	print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")

gradebdys = [0.0]*len(gradeBoundaries)
