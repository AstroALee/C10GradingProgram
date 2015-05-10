# Import the Config variables
from GPv2_config import *

import sys


def CoursePoints(rawgrades,netgrades):
	calc_FE(rawgrades,netgrades)
	calc_SP(rawgrades,netgrades)
	calc_LB(rawgrades,netgrades)
	calc_QZ(rawgrades,netgrades)
	calc_MT(rawgrades,netgrades)
	calc_HW(rawgrades,netgrades)
	calc_CP(netgrades)



def calc_FE(raw,net):
	iFE = 3 + numHW + numQZ + numMT + numLB + 2 - 1
	if( (raw[iFE] > maxFE) and ("FE" in prorateMe) ):
		#Prorating
		net[9].append("Final")
	elif( raw[iFE] > maxFE ):
		#Weird
		sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on the Final Exam...") 
	else:
		net[5] = raw[iFE]/(1.0*maxFE)*cpFE
		net[7] = net[7] + cpFE	
		
def calc_SP(raw,net):
	iSP = 3 + numHW + numQZ + numMT + numLB + 1 - 1
	if( (raw[iSP] > maxSP) and ("SP" in prorateMe) ):
		#Prorating
		net[9].append("Participation")
	elif( raw[iSP] > maxSP ):
		#Weird
		sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on Section Participation...") 
	else:
		net[4] = raw[iSP]/(1.0*maxSP)*cpSP
		net[7] = net[7] + cpSP
		
def calc_LB(raw,net):
	iLB = 3 + numHW + numQZ + numMT
	score = 0.0
	for i in range(0,numLB): score = score + raw[iLB+i] 
	if( (score > maxLB) and ("LB" in prorateMe) ):
		#Prorating
		net[9].append("Labs")
	elif( score > maxLB ):
		#Weird
		sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on Labs...")
	else:
		net[3] = score/(1.0*maxLB)*cpLB
		net[7] = net[7] + cpLB
		
def calc_QZ(raw,net):
	iQZ = 3 + numHW
	for i in range(0,numQZ):
		if( (raw[iQZ+i] > maxQZ) and ("QZ" in prorateMe) ):
			#Prorating
			net[9].append("Quiz " + str(i+1))
		elif(raw[iQZ+i] > maxQZ):
			#Weird
			sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on a Quiz...")
		else:
			net[1] = net[1] + raw[iQZ+i]/(1.0*maxQZ)*(1.0*cpQZ/numQZ)
			net[7] = net[7] + 1.0*cpQZ/numQZ
			

def calc_MT(raw,net):
	iMT = 3 + numHW + numQZ
	mtscores = raw[iMT:iMT+numMT]
	mtscores.sort()
	mtscores.reverse()
	for i in range(0,keepMT):
		if( (mtscores[i]>maxMT) and ("MT" in prorateMe) ):
			#Prorating
			net[9].append("Midterm")
		elif(mtscores[i]>maxMT):
			#Weird
			sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on a Midterm...")
		else:
			net[2] = net[2] + mtscores[i]/(1.0*maxMT)*(1.0*cpMT/keepMT)
			net[7] = net[7] + 1.0*cpMT/keepMT
			
def calc_HW(raw,net):
	iHW = 3
	hwscores = raw[iHW:iHW+numHW]
	hwscores.sort()
	hwscores.reverse()
	for i in range(0,keepHW):
		if( (hwscores[i]>maxHW) and ("HW" in prorateMe) ):
			#Prorating
			net[9].append("Homework")
		elif( hwscores[i] > maxHW ):
			#Weird
			sys.exit("Student " + str(raw[1]) + " (" + raw[0] + ") has over 100% on a Homework...")
		else:
			net[0] = net[0] + hwscores[i]/(1.0*maxHW)*(1.0*cpHW/(1.0*keepHW))
			net[7] = net[7] + 1.0*cpHW/(1.0*keepHW)	
			
def calc_CP(net):
	for i in range(0,6): net[6] = net[6] + net[i]
	# Uncomment the below line if you want to round course points. This can have big consequences!
	# net[6] = round(net[6])
	
	
def LetterGrades(net,letterNames):
	# Percent Score:
	percent = net[6]/net[7]
	for i in range(0,len(gradebdys)):
		if( percent >= gradebdys[i] ):
			net[8] = letterNames[i]
			break		
	
def ApplyOverrides(net,gbook):
	# Searching the book for the student id you provided. Once found, changes the letter grade
	for ostud in Overrides:
		jsave = -1
		curStud = ostud[0]
		for i in range(0,len(net)):
			if(curStud==gbook[i][1]):
				net[i][8] = ostud[1]
				net[i][10] = 'Y'
				
	
	
	