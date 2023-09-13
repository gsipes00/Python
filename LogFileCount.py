#This script reads a directory of text files and searches for a term input by the user. It then counts the number of times that term is found line by line.
#Lastly it creates a CSV and a text file to summarize the counts and listing the individual log entries. 
# Note that if interpreting this code in python 3, that the input() function directly assumes the input is text, so no quotes are needed.
# Author: Gene Sipes
# Date: 12/1/2021
# Update: 9/13/2023
# Python 2 but compatibly with 3

import os
import getpass
import time
import csv


print("Log File Count Script version 1.1")

dirPath = r'//san_marcos/files/DeptShares/Public Services/Transportation/Drainage/MS4 Program/Annual Reports/PSA_LogFile_Counts/'
textFiles = os.listdir(dirPath)
files = [item for item in textFiles if os.path.isfile(os.path.join(dirPath, item))]
findString = input(' Input Search Terms, Case Insensitive, Use Quotes if Interpreting in Python 2 : ')
timeStamp = time.strftime('%a, %d %b %Y %H:%M:%S')
userName = getpass.getuser()

print('The following files will be searched for string ' + '"' + findString + '"')
print(files)

print('--------------------------------\n Searching text files now..\n--------------------------------')




os.chdir(dirPath)
logList = []
counter = 0
for file in files:
    with open(file, 'r') as f:
        f.readline()
        for line in f:
            if findString.lower() in line.lower():
                counter += 1
                logList.append(line.split("\t"))
                
                


print('Found {} instances of {}'.format(str(counter), findString))

print('Writting output to text file.')
with open(f'//san_marcos/files/DeptShares/Public Services/Transportation/Drainage/MS4 Program/Annual Reports/PSA_LogFile_Counts/Outputs/AdCounts_{findString}.txt', 'w') as f:
    f.write('There are {} mentions of {} in the directory of log files!\n\nThese script results were executed on {} by {}\n\n'.format(counter, findString, timeStamp, userName))
    f.write('List of log file entries used in count:\n\n')
    for log in logList:
        for value in log:
            f.write(value)

fields = ['DateTime', 'Status', 'File', 'Duration']
print('Writting output to csv file.')
with open(f'//san_marcos/files/DeptShares/Public Services/Transportation/Drainage/MS4 Program/Annual Reports/PSA_LogFile_Counts/Outputs/AdCounts_{findString}.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(fields)
    writer.writerows(logList)
    

print('------------------------------')
print(f'Finished, go check your AdCounts_{findString}.txt file for details.')
