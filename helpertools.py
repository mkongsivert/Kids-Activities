import datetime as dt
import math

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

def between(string, start, beginTag, endTag):
	'''resturns a substring between two tags'''
	begin = string.find(beginTag, start) + len(beginTag)
	end = string.find(endTag, begin)
	return string[begin:end]

def removeWhitespace(string):
	'''as one might expect, removes all the whitespace from a given string'''
	newString = ''.join([i for i in string if (i != '\t' and i != '\n')])
	return newString

def removeTag(string, tag, middle = True, neg = False):
	'''removes extraneous tags'''
	leftBeg = string.find("<" + tag)
	leftEnd = string.find(">", leftBeg)
	right = string.find("</" + tag + ">", leftEnd)
	if middle:
		#just remove the tags
		return string[0:leftBeg] + string[leftEnd+1:right] + string[right+len(tag)+3:]
	elif (not neg):
		#remove the tags and tagged material
		return string[0:leftBeg] + string[right+len(tag)+3:]
	else:
		#remove everything but the tagged material
		return string[leftEnd+1:right]

def makeIndicesList(siteText, searchTerm):
	'''returns a list of indices of events in a given site text'''
	s = 0
	indices = []
	while True:
		newI = siteText.find(searchTerm, s)
		if newI == -1:
			break
		s = newI + len(searchTerm)
		indices.append(newI)

	return indices

def exhibitions(schedule, begDate, endDate):
	'''takes in a museum schedule and starting and ending dates for an
	exhibition and returns a list of the dates and times when the exhibition
	will be open'''
	allDates = []
	date = begDate
	while date <= endDate:
		if schedule[date.weekday()] != None:
			begTime = dt.datetime.combine(date, schedule[date.weekday()][0])
			endTime = dt.datetime.combine(date, schedule[date.weekday()][1])
			allDates.append((begTime, endTime))
		date += dt.timedelta(days=1)
	return allDates

def findMonth(dString):
	'''takes in a string representing a date and returns the month that
	that date is in'''
	
	month = 0
	for i in range(len(months)):
		if months[i] in dString.lower():
			month = i + 1
			break
	return month

def parseDate(dString, allNums = False):
	'''takes in a string representing a date and returns a datetime object
	representing that same date'''
	dString = dString.replace(' ', '')
	now = dt.datetime.now()
	year = 0
	date = 0
	
	if allNums:
		month = int(dString[:2])
		dString = dString[2:]
	else:
		month = findMonth(dString)
	nums = ''.join([i for i in dString if i.isdigit()])
	if len(nums) <= 2:
		date = int(nums)
		year = now.year if (month >= now.month) else (now.year + 1)
	elif str(now.year) in nums:
		date = int(nums.replace(str(now.year), ''))
		year = now.year
	elif str(now.year+1) in nums:
		date = int(nums.replace(str(now.year+1), ''))
		year = now.year+1
	elif str(now.year-1) in nums:
		date = int(nums.replace(str(now.year-1), ''))
		year = now.year-1
	return dt.date(year, month, date)

def parseTimeHelper(tString):
	num = ''.join([i for i in tString if i.isdigit()])
	time = None
	if len(num) <= 2:
		time = dt.time(int(num))
	else:
		time = dt.time(int(num[:-2]), int(num[-2:]))

	if 'pm' in ''.join([i for i in tString if i.isalpha()]).lower():
		dTime = dt.datetime.combine(dt.datetime.now(), time)
		dTime += dt.timedelta(hours = 12)
		time = dTime.time()
	#TODO: add a.m. and p.m.
	return time

def parseTime(tString):
	'''takes in a string representing a time and returns a datetime object
	representing that same date'''
	if "–" in tString:
		interval = tString.split('–')
		begin = parseTimeHelper(interval[0])
		end = parseTimeHelper(interval[1])
	elif '-' in tString:
		interval = tString.split('-')
		begin = parseTimeHelper(interval[0])
		end = parseTimeHelper(interval[1])
	elif '&ndash;' in tString:
		interval = tString.split('&ndash;')
		begin = parseTimeHelper(interval[0])
		end = parseTimeHelper(interval[1])
	elif 'to' in tString:
		interval = tString.split('to')
		begin = parseTimeHelper(interval[0])
		end = parseTimeHelper(interval[1])
	else:
		begin = parseTimeHelper(tString)
		end = dt.time(hour = begin.hour+2, minute = begin.minute)
	return (begin, end)

def fromDatetime(dtString):
	'''instead of parsing the date from text, read the date from a datetime
	format'''
	dtString = dtString.replace(' ', '')
	dString, tString = dtString.split('T')

	year = int(dString[:4])
	month = int(dString[5:7])
	date = int(dString[8:10])

	beg, end = tString.split('-')
	begHour, begMin = beg.split(':')[0:2]
	endHour, endMin = end.split(':')[0:2]

	begTime = dt.datetime(year, month, date, int(begHour), int(begMin))
	endTime = dt.datetime(year, month, date, int(endHour), int(endMin))
	return(begTime, endTime)

def sortByDate(table):
	'''merge sort of a table by date'''
	if len(table) <= 1:
		return table
	half = len(table)//2
	firstHalf = sortByDate(table[0:half])
	secondHalf = sortByDate(table[half:])
	sortedL = []
	for i in range(len(table)):
		if len(firstHalf) == 0:
			sortedL += secondHalf
			break
		elif len(secondHalf) == 0:
			sortedL += firstHalf
			break
		elif firstHalf[0][1][0] <= secondHalf[0][1][0]:
			sortedL += [firstHalf[0]]
			firstHalf = firstHalf[1:]
		else:
			sortedL +=[secondHalf[0]]
			secondHalf = secondHalf[1:]
	return sortedL

def formatDates(event):
	'''TODO: fix this'''
	Months = ['January', 'Febrary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	begin = event[1][0]
	end = event[1][1]
	newDate = Months[begin.month]
	newDate += " " + str(begin.day) + ", " + str(begin.year)
	newDate += " at " + str(begin.hour%12) + ":" + str(begin.minute)
	newDate += " a.m." if begin.hour < 12 else " p.m."
	newEvent = [event[0]] + [newDate] + event[2:]
	return newEvent

def hexagon(center, coeff, r=20.0):
	vert = coeff*r/2
	horiz = coeff*r*math.sqrt(3)/2
	deg030 = [center[0]+vert, center[1]+horiz]
	deg090 = [center[0]+coeff*r, center[1]]
	deg150 = [center[0]+vert, center[1]-horiz]
	deg210 = [center[0]-vert, center[1]-horiz]
	deg270 = [center[0]-coeff*r, center[1]]
	deg330 = [center[0]-vert, center[1]+horiz]
	return [deg030, deg090, deg150, deg210, deg270, deg330]