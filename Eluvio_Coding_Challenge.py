from pathlib import Path
import os
import difflib
import itertools
from threading import Thread

#Import the data from the files.
files = [file for file in os.listdir('.') if os.path.isfile(file)]
data = []
for file in files:
    if 'sample' in file:
        data.append([file, Path(file).read_bytes()])

#Helper function to find longest common substring between two strings.
def lcs(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2, autojunk=False)
    return matcher.find_longest_match(0, len(s1), 0, len(s2))

#Helper function to find location of a substring within a string.
def findSubstring(string, substring):
    return string.find(substring)

#Find all unique pairs of files possible. 
uniquePairs = list(itertools.combinations(range(len(data)), 2))

#Threading function to process these unique pairs.
maxMatches = {}
def findMaxMatch(pairs, data, threadNum):
    maxMatch = None
    for pair in pairs:
        file1 = data[pair[0]]
        file2 = data[pair[1]]
        curMatch = lcs(file1[1], file2[1])
        if maxMatch == None or curMatch.size > maxMatch[2].size:
            maxMatch = [pair[0], pair[1], curMatch]
    maxMatches[threadNum] = maxMatch

#Each thread will handle 9 unique pairs. 
#9 is chosen because there are 45 unique pairs possible, giving a nice number of 5 threads.
threads = []
for i in range(len(uniquePairs) // 9):
    thread = Thread(target = findMaxMatch, args = (uniquePairs[(i*9):((i+1)*9)], data, i,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

#Find the maximum match from all the threads. 
maxIndex = 0
for i in range(len(uniquePairs) // 9):
    if (maxMatches[i][2].size > maxMatches[maxIndex][2].size):
        maxIndex = i
maxMatch = maxMatches[maxIndex]
file1 = data[maxMatch[0]]
file2 = data[maxMatch[1]]

#Assert that the subsequences do match.
assert file1[1][maxMatch[2].a:(maxMatch[2].a+maxMatch[2].size)] == file2[1][maxMatch[2].b:(maxMatch[2].b+maxMatch[2].size)]
maxSubstring = file1[1][maxMatch[2].a:(maxMatch[2].a+maxMatch[2].size)]

#Find the location of the maximum substring from all files. Output the length of the substring and the location in each file. 
print("Length of longest strand: " + str(len(maxSubstring)))
for d in data:
    location = findSubstring(d[1], maxSubstring)
    if location != -1:
        print("Found in " + d[0] + " at offset " + str(location))
