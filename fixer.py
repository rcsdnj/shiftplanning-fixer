
from ShiftData import ShiftData

print("Hello!")
fname = "/Users/rcsdnj/Desktop/shift.txt"
with open(fname) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content][::-1] 

totalShifts = 0
shiftsToFix = 0
for line in content:
    currentShift = ShiftData(line)
    totalShifts += 1
    if (currentShift.isUnusual()):
        shiftsToFix += 1
        print(currentShift)

print("Shifts totais: "  + str(totalShifts))
print("Shifts a corrigir: " + str(shiftsToFix))


