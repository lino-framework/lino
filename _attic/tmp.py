colCount = 3
row = [[]] * colCount
print row

for i in range(colCount):
   cell = row[i]
   cell.append(i)
   print str(i) + str(row)
