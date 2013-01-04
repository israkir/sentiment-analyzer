import sys

resultOutFile = file('data/dev.in.real_results' , 'r') # real results
testOutFile = file('data/output/dev.in.analysis_results' , 'r') # our results

totalNum = 0
correctNum = 0
correctNumClause1 = 0
correctNumClause2 = 0
correctNumEverything = 0

for i in range(5000):
    r1 = resultOutFile.readline().strip()
    r2 = resultOutFile.readline().strip()
    rOut = resultOutFile.readline().strip()
    t1 = testOutFile.readline().strip()
    t2 = testOutFile.readline().strip()
    tOut = testOutFile.readline().strip()

    totalNum = totalNum+1
    if rOut == tOut:
        correctNum = correctNum+1

    if r1 == t1:
        correctNumClause1 += 1

    if r2 == t2:
        correctNumClause2 += 1

    if r1 == t1 and r2 == t2 and rOut == tOut:
        correctNumEverything += 1


correctRate = float(correctNum)/float(totalNum)
correctRateClause1 = float(correctNumClause1)/float(totalNum)
correctRateClause2 = float(correctNumClause2)/float(totalNum)
correctRateEverything = float(correctNumEverything)/float(totalNum)

print
print "total # of sentences: " + str(totalNum)
print
print "# of first clause polarity is correct: " + str(correctNumClause1)
print "correctness rate for clause1 polarity: " + str(correctRateClause1)
print
print "# of second clause polarity is correct: " + str(correctNumClause2)
print "correctness rate for clause2 polarity: " + str(correctRateClause2)
print
print "# of sentence polarity is correct: " + str(correctNum)
print "correctness rate for sentence polarity: " + str(correctRate)
print
print "# of first clause and second clause and sentence polarity all together are correct: " + str(correctNumEverything)
print "correctness rate for everything together polarity: " + str(correctRateEverything)
print
