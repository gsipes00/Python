import os
import getpass
import time
import csv

#This script reads a directory of text files and searches for a term input by the user. It then counts the number of times that term is found line by line.
#Lastly it creates a CSV and a text file to summarize the counts and listing the individual log entries. 

print("Log File Count Script version 1.0")

dirPath = r'//san_marcos/files/DeptShares/Public Services/Transportation/Drainage/MS4 Program/Annual Reports/PSA_LogFile_Counts'
textFiles = os.listdir(dirPath)
findString = input(' Input Search Terms and be sure to use quotes.')
timeStamp = time.strftime('%a, %d %b %Y %H:%M:%S')
userName = getpass.getuser()

print('The following files will be searched for string ' + findString)
print(textFiles)

print('--------------------------------')
print('Searching text files now...')
print('--------------------------------')

os.chdir(dirPath)
logList = []
counter = 0
for file in textFiles:
    with open(file, 'r') as f:
        f.readline()
        for line in f:
            if findString in line:
                counter += 1
                logList.append(line.split("\t"))
                
                


print('Found {} instances of {}'.format(str(counter), findString))

print('Writting output to text file.')
with open('AdCounts.txt', 'w') as f:
    f.write('There are {} mentions of {} in the directory of log files!\n\nThese script results were executed on {} by {}\n\n'.format(counter, findString, timeStamp, userName))
    f.write('List of log file entries used in count:\n\n')
    for log in logList:
        for value in log:
            f.write(value)

fields = ['DateTime', 'Field2', 'File', 'Field3']
print('Writting output to csv file.')
with open('AdCounts.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(fields)
    writer.writerows(logList)
    

print('------------------------------')
print('Finished, go check your AdCounts.txt file for details.')
