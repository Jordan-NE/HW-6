import csv
from Record import Record
from config import PIVOTS2
from CollectiveImpurityEntropy import CollectiveImpurityEntropy
from CollectiveImpurityGini import CollectiveImpurityGini
from TreeNode import TreeNode

#  Function reads in csv file containing medical details
#  Returns list of Record objects from file
#  Records will have dictionaries for attribute with keys being equal to column headers in file
def read_in(filepath):

    recordList = []
    #  Referenced https://www.geeksforgeeks.org/reading-csv-files-in-python/ for refresher on reading in files
    with open(filepath, mode = "r") as newData:
        fileContents = csv.reader(newData)
        firstRow = next(fileContents)
        firstRow[0] = "Age"
        
        for row in fileContents:
            attributeDict = dict()
            for index in range(len(row) - 1):
                if row[index].isnumeric():
                    value = float(row[index])
                else:
                    value = row[index]
                attributeDict[firstRow[index]] = value
            newRecord = Record(attributeDict, row[-1])
            recordList.append(newRecord)


    return(recordList)

#  Params - list of record objects and lambda
#  Returns two lists of records based on lambda calculations
def make_partition(recordList, lam):
    leftSplit = []
    rightSplit = []

    for record in recordList:
        
        if lam(record) == True:
            leftSplit.append(record)
        else:
            rightSplit.append(record)

    return [leftSplit, rightSplit]


#  Params - list of record objects
#         - Strategy subclass
#  Returns - None
#  Prints out the split which produces the lowest impurity
#  Changing the pivots value in this to accommodate other  lambda conditions
def find_best_partition(recordList, strategy, pivots):
    #  Selecting base value for lowest entropy since 2 is an impossible value
    lowestEntropy  = 2
    bestPivot = None
    for key, value in pivots.items():
        newPartition = make_partition(recordList, pivots[key])
        tempEntropy = strategy.calculate(newPartition)
        #  print(key + str(tempEntropy))
        if tempEntropy < lowestEntropy:
            lowestEntropy = tempEntropy
            bestPivot = key

    #  print(bestPivot + ": " + str(lowestEntropy))


#  Main driver function
#  Identifies the optimal partition values and prints out these and the impurity values for each
def main():
    records = read_in("test_data.csv")
    #records = read_in("training_data_more_noise.csv")
    giniCalcObj = CollectiveImpurityGini()
    entropyCalcObj = CollectiveImpurityEntropy()
    newTree = TreeNode(records, PIVOTS2)
    print("at root...")

    newTree.grow_tree(entropyCalcObj)

    test_record_list = read_in("test_data.csv")
    rec = newTree.classify_records(test_record_list)
    
    acc = sum([1 for r in rec if r.actual_label == r.predicted_label])/len(rec)
    print(acc)


if __name__ == "__main__":
    main()

'''
recordList = read_in("training_data_more_noise.csv")

sum = 0
for value in recordList:
    sum += int(value.attrs["HDL cholesterol"])

totsChol = sum / len(recordList)
#  Average Age = 63.61
#  Average blood pressure 150.78
#  Total cholesterol = 206.78
#  HDL cholesterol = 50.23
print(totsChol)
'''