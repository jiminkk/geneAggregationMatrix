#!/usr/bin/python
"""
	Algorithm used:
		Read the entire csv file (self_score.csv)
		Store keys and values into dictionary:
			Compound as key
			Cell value (connectivity score) and column index as values
"""

import csv
import itertools
from collections import defaultdict

calc
"""
*** Use compoundList.txt under gene_aggregation_matrix folder instead of 
			"/Users/jiminkim/Desktop/Biocomputation/compoundList.txt" ***

compoundList: list of compound names exactly extracted from the "Compound" column in self_score.csv
"""
compList = []
with open("/Users/jiminkim/Desktop/Biocomputation/compoundList.txt", "r") as compListFile:
	for line in compListFile:
		line = line.rstrip('\n')
		compList.append(line)
#print compList

"""
*** Use list.txt under gene_aggregation_matrix folder instead of 
			"/Users/jiminkim/Desktop/Biocomputation/list.txt" ***

simplifiedList: compoundList simplified into a list of non-repetitive compounds
"""
simplifiedList = []
with open("/Users/jiminkim/Desktop/Biocomputation/list.txt", "r") as sListFile:
	for line in sListFile:
		line = line.rstrip('\n')
		simplifiedList.append(line)
#print simplifiedList






print ""
print "////////////////////////////"
print "/////csvData"
print "////////////////////////////"
"""
*** Use self_score.csv under gene_aggregation_matrix folder instead of 
			"/Users/jiminkim/Desktop/Biocomputation/self_score.csv" ***

csvData is a dictionary that contains:
	-key: compound name
	-value: list of lists that include cell value and index number
			(for a given compound/key, there is a list of cell value and index number)
			(this index number increments by one as you iterate across each row)
			(index number starts over for same compound/key in another row)
"""
csvData = {}
csvData = defaultdict(list)
with open("/Users/jiminkim/Desktop/Biocomputation/self_score.csv", "rbU") as csv_file:
	csvreader = csv.reader(csv_file)
	for row in itertools.islice(csvreader, 3, 822):				#restrict row wise (matrix: 3 to 822)
 		count = 0
 		for cell in itertools.islice(row, 3, 822):				#just the values in each row
 			#print row[1], cell, count					#print compound, cell values, and # of compounds counts
			count +=1
			list1 = []
			list1.append(float(cell))							#add in cell value
			list1.append(count)
			csvData[row[1]].append(list1)
print csvData



print ""
print "////////////////////////////"
print "/////avgData1"
print "////////////////////////////"
"""
avgData1 is a dictionary that contains:
	-key: compound name
	-value: lists that contain Average Value & index number
		(Average Value = average of cell values for all values with same index number for the corresponding compound)
		(So this dictionary should not have repeating index numbers for each compound/key)
"""
avgData1 = {}
avgData1 = defaultdict(list)
for key, values in csvData.iteritems():			#iterate csvData dictionary
	for i in range(1, 820):						#start and stop depends on matrix (1-819 inclusive) (1, 820)
		average = sum_row = count = 0
		for value in values:
			if (i == value[1]):					#value[1] represents index of compound count (eg. i = value[1] = 2, if current compound is the second repetition)
				sum_row += value[0]				#value[0] is cell value per column
				count += 1
		average = sum_row/count
		list2 = []
		list2.append(average)					#average = average of cell values for each different compound per row
		list2.append(i)							
		avgData1[key].append(list2)
	print "appending key"
print avgData1



print ""
print "////////////////////////////"
print "/////renamedData"
print "////////////////////////////"
"""
renamedData is a dictionary that contains:
	-key: compound name
	-value: lists that contain another compound "X" and the Average Value from avgData1
		(X = compound name that corresponds to the row index number)
"""
renamedData = {}
renamedData = defaultdict(list)
#tmpList = ['midostaurin', 'midostaurin', 'SB-203580', 'midostaurin', 'SB-203580']
for key, values in avgData1.iteritems():
	for value in values:
		for i in range(len(compList)):
			if (i == value[1]-1):
				list3 = []
				list3.append(compList[i])
				list3.append(value[0])
				renamedData[key].append(list3)
print renamedData



print ""
print "////////////////////////////"
print "/////avgData2"
print "////////////////////////////"
"""
avgData2 is a list that contains:
	-key: compound name
	-another list: another compound from the matrix & average value calculated from cell values corresponding to the compound pair
"""
avgData2 = []
#tmpList2 = ['midostaurin', 'SB-203580']
for key, values in renamedData.iteritems():
	for compound in simplifiedList:
		average = sum_col = count = 0
		for value in values:
			#print key, compound, value[0]
			if (compound == value[0]):
				sum_col += value[1]
				count += 1
		average = sum_col/count
		list4 = []
		list4.append(compound)
		list4.append(average)
		avgData2.append(key)				#avgData2 = [row, [col, avg]]
		avgData2.append(list4)
print avgData2

"""
The below code converts the avgData2 list into the matrix format I wanted
	which is the aggregatedMatrix.csv from the folder
"""

"""

with open("/Users/jiminkim/Desktop/Biocomputation/aggregatedMatrix.csv", "wb") as csvFile:
	csvWriter = csv.writer(csvFile)
	for comp in simplifiedList:
		finalList = []
		for index in range(len(avgData2)):
			if index % 2 == 0:
				if avgData2[index] == comp:
					print comp, avgData2[index+1][0], avgData2[index+1][1]
					finalList.append(avgData2[index+1][1])
		csvWriter.writerow(finalList)
"""
