import sys

resultOutFile = file('data/output/dev.out' , 'r') # real results
testOutFile = file('data/output/dev.in.analysis_results' , 'r') # our results

totalNum = 0
correctNum = 0
correctNumClause1 = 0
correctNumClause2 = 0
correctNumEverything = 0

for i in range(15000):
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


print "correctNum for clause1: "+str(correctNumClause1)
print "correct RATE for clause1: "+str(correctRateClause1)

print "correctNum for clause2: "+str(correctNumClause2)
print "correct RATE for clause2: "+str(correctRateClause2)

print "correctNum for everything together: "+str(correctNumEverything)
print "correct RATE for everything together: "+str(correctRateEverything)

print "correctNum for sentence: "+str(correctNum)
print "totalNum for sentence: "+str(totalNum)
print "correct RATE for sentence: "+str(correctRate)
