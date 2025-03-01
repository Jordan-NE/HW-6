from CollectiveImpurityEntropy import CollectiveImpurityEntropy
from CollectiveImpurityGini import CollectiveImpurityGini
from config import PIVOTS2

class TreeNode:

    def __init__(self, recordList, pivotDict):
        self.records = recordList
        self.pivots = pivotDict
        self.children = []
        #  Labels apply to treenodes specifically, which risk level they have more of
        self.label_to_apply = None
        #  Used to tell what the next split will
        self.partitionLogic = None
        self.matchingRecords = None
        self.lowCount = 0
        self.highCount = 0
        self.pivotChoices = []


    #  Updates counts of low and high risk records
    def countLabels(self):
        for record in self.records:
            if record.actual_label == "High Risk":
                self.highCount += 1
            else:
                self.lowCount += 1


    #  Checks that all record objects in the records attribute have the same label
    def labelsMatch(self):
        if self.lowCount == len(self.records) or self.highCount == len(self.records):
            self.matchingRecords = True
        else:
            self.matchingRecords = False

    #  Params - list of record objects and lambda
    #  Returns two lists of records based on lambda calculations
    def make_partition(self, recordList, lam):
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
    def find_best_partition(self, strategy):
        #  Selecting base value for lowest entropy since 2 is an impossible value
        lowestEntropy  = 2
        bestPivot = None
        for key, value in self.pivots.items():
            newPartition = self.make_partition(self.records, self.pivots[key])
            tempEntropy = strategy.calculate(newPartition)
            # print(key + str(tempEntropy))
            if tempEntropy < lowestEntropy:
                lowestEntropy = tempEntropy
                bestPivot = [key, value]
                #print("BEST PIVOT HERE")
                #print(bestPivot)
                self.partitionLogic = value
        
        return bestPivot

    #  Must run methods to update matchingRecords value
    def grow_tree(self, impurityClass):
        self.countLabels()
        self.labelsMatch()
        if self.pivots is None or self.labelsMatch():
            return
        elif self.matchingRecords:
            if self.lowCount > self.highCount:
                self.label_to_apply = "Low Risk"
            else:
                self.label_to_apply = "High Risk"
        else:
            lamSplit = self.find_best_partition(impurityClass)
            if lamSplit is None:
                return
            else:
                #print("Split on: " + lamSplit[0])
                leftPivots = self.pivots.copy()
                rightPivots = self.pivots.copy()
                partitionedLists = self.make_partition(self.records, self.pivots[lamSplit[0]])
                del leftPivots[lamSplit[0]]
                del rightPivots[lamSplit[0]]
                leftNode = TreeNode(partitionedLists[0], leftPivots)
                rightNode = TreeNode(partitionedLists[1], rightPivots)
                self.add_child(leftNode)
                self.add_child(rightNode)

                for child in self.children:
                    child.grow_tree(impurityClass)

    #  Takes in list where each index is a list of record objects
    def add_child(self, treeNode):
        self.children.append(treeNode)

    #  Classifies single record based on predicted vs label to apply
    def classify_record_single(self, record_object):
        """classifies a single record object
        Param: record_object - an object of the record class
        returns: that record object with the predicted_label field set"""
        if len(self.children) == 0:
            record_object.predicted_label = self.label_to_apply
            record_object
        else:
            if self.partitionLogic(record_object) == True:
                child = self.children[0]
            else:
                child = self.children[1]
            child.classify_record_single(record_object)


    #  Classifies a record list
    def classify_records(self, record_list):
        """
        classifies a list of record objects
        """
        for record_object in record_list:
            self.classify_record_single(record_object)
        return record_list

