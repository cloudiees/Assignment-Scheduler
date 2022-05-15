import time
from collections import Counter
from operator import concat, length_hint
from os import name
import string

def getAssignments():
	assignmentList = []
	while True:
		assignmentName = input("What is the name of the assignment? (Press enter to finish) ")
		if assignmentName == "":
			break
		validLength = False
		time.sleep(0.3)
		print()
		while validLength == False:
			assignmentLength = input("What is the length (in hours) of the assignment? ")
			if not assignmentLength.isdigit():
				print("Invalid input")
			else:
				validLength = True
		validDay = False
		time.sleep(0.3)
		print()
		while validDay == False:
			assignmentDueDay = input("What day is the assignment due?\n(1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday, 7=Sunday) ")
			if not assignmentDueDay.isdigit() or (int(assignmentDueDay) > 7 or int(assignmentDueDay) <= 0):
				print("Invalid input")
			else:
				validDay = True
		time.sleep(0.3)
		print()
		assignmentList.append({"name":assignmentName, "day": int(assignmentDueDay), "length":int(assignmentLength), "hoursScheduled":0})
	assignmentList.sort(key=lambda x: x["length"], reverse=True)
	assignmentList.sort(key=lambda x: x["day"])
	print()
	time.sleep(0.4)
	return assignmentList

def getSchedule():
	dayFreeTimeDictionary = {}
	dayFreeTimeDictionary["Sunday"] = getFreeTimeInDay("Sunday")
	dayFreeTimeDictionary["Monday"] = getFreeTimeInDay("Monday")
	dayFreeTimeDictionary["Tuesday"] = getFreeTimeInDay("Tuesday")
	dayFreeTimeDictionary["Wednesday"] = getFreeTimeInDay("Wednesday")
	dayFreeTimeDictionary["Thursday"] = getFreeTimeInDay("Thursday")
	dayFreeTimeDictionary["Friday"] = getFreeTimeInDay("Friday")
	dayFreeTimeDictionary["Saturday"] = getFreeTimeInDay("Saturday")
	return dayFreeTimeDictionary

def isHoursValid(hours):
	if not hours.isdigit():
		return False
	if int(hours) > 24:
		return False
	return True

def getFreeTimeInDay(day):
	isValid = False
	while not isValid:
		freeTime = input("How many hours of free time do you have on " + day + "? ")
		isValid = isHoursValid(freeTime)
		if not isValid:
			print("Invalid input")
		time.sleep(0.3)
		print()
	return int(freeTime)
			
def makeSchedule(freeTimeInDays, assignments):
	schedule = [
		{"dayName":"Sunday", "freeTime":freeTimeInDays["Sunday"], "workUnits":[]},
		{"dayName":"Monday", "freeTime":freeTimeInDays["Monday"], "workUnits":[]},
		{"dayName":"Tuesday", "freeTime":freeTimeInDays["Tuesday"], "workUnits":[]},
		{"dayName":"Wednesday", "freeTime":freeTimeInDays["Wednesday"], "workUnits":[]},
		{"dayName":"Thursday", "freeTime":freeTimeInDays["Thursday"], "workUnits":[]},
		{"dayName":"Friday", "freeTime":freeTimeInDays["Friday"], "workUnits":[]},
		{"dayName":"Saturday", "freeTime":freeTimeInDays["Saturday"], "workUnits":[]}
		]
	for assignment in assignments:
		for i in range(assignment["day"]):
			assignmentHoursLeft = assignment["length"] - assignment["hoursScheduled"]
			if assignmentHoursLeft != 0:
				if schedule[i]["freeTime"] - len(schedule[i]["workUnits"]) != 0:
					if assignmentHoursLeft <= schedule[i]["freeTime"] - len(schedule[i]["workUnits"]):
						for x in range(assignmentHoursLeft):
							schedule[i]["workUnits"].append(assignment["name"])
							assignment["hoursScheduled"] += 1
					else:
						for x in range(schedule[i]["freeTime"] - len(schedule[i]["workUnits"])):
							schedule[i]["workUnits"].append(assignment["name"])
							assignment["hoursScheduled"] += 1
		if(assignment["hoursScheduled"] - assignment["length"] != 0):
			print(assignment["name"] + " is too long to complete in the free time given, " + str(assignment["length"] - assignment["hoursScheduled"]) + " more hours are needed.")
			print()		
	return schedule
			
def main():
	dayFreeTimeDictionary = getSchedule()
	assignmentList = getAssignments()
	schedule = makeSchedule(dayFreeTimeDictionary, assignmentList)
	for day in schedule:
		scheduleMsg = "On " + day["dayName"] + " you will work on "
		assignmentsThatDay = day["workUnits"]
		assignmentAndHours = {}
		for i in assignmentsThatDay:
			assignmentAndHours[i] = assignmentsThatDay.count(i)
		assignmentNameList = assignmentAndHours.keys()
		stringList = []
		for assignment in assignmentNameList:
			hoursHolder = assignmentAndHours[assignment]
			stringList.append(assignment + " for " + str(hoursHolder) + " hours")
		if len(stringList) == 0:
			scheduleMsg += "nothing."
		elif len(stringList) == 2:
			scheduleMsg += stringList[0] + " and " + stringList[1]	
		elif len(stringList) == 1:
				scheduleMsg += stringList[0] + "."
		else:
			for i in range(len(stringList)):
				if stringList[i] == stringList[-1]:
					scheduleMsg += "and " + stringList[i] + "."
				else:
					scheduleMsg += stringList[i] + ", "
			
		print(scheduleMsg)
		time.sleep(0.3)
		print()

main()