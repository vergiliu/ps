import filecmp
import os
import sys
import time
import shutil

# hash with all the files
# initial root folder where all the files are coming of - we need 2 of these
# folder support needs to be added


class FolderComparatorStatus:
    """The class will store the last update of the FolderComparator and keep track
    of the current status, for long running operations
    """

    def __init__(self):
        self.lastRun = 0
        self.status = None
        pass

    def setStatus(self, aStatus):
        self.status = aStatus
        print(self.status)

    def updateStatus(self, aNewStatus):
        self.status = aNewStatus
        self.lastRun = time.time()
        print(self.status)

    def getLastRun(self):
        return self.lastRun

    def getLastStatus(self):
        return self.status


class FolderComparator:
    """This class will be used to compare and sync 2 different folders
    The folder structure will be considered as LEFT and RIGHT (from a diff view)
    TODO more comments to be added
    """
    syncTypeList = {'keepboth': 0, 'keepbigger': 1, 'keepnewer': 2, }

    def __init__(self, leftFolder, rightFolder):
        self.syncType = 0 # default keepboth
        self.comparatorStatus = FolderComparatorStatus()
        self.leftFolder = leftFolder
        self.rightFolder = rightFolder
        self.filesLeft = {}
        self.filesRight = {}
        self.inBothButDifferent = set()
        self.inRightButNotInLeft = set()
        self.inLeftButNotInRight = set()

    def visitAllSubfolders(self):
        # make 2 threads
        self.comparatorStatus.setStatus("running")
        myElementsLeftFolder = len(self.leftFolder)
        myElementsRightFolder = len(self.rightFolder)
        for root, dirs, files in os.walk(self.leftFolder):
            for myFileName in files:
                myfile = os.path.join(root, myFileName)
                if not myFileName.endswith('lock'):
                    mystat = os.stat(myfile)
                    # print("%s occupies %d bytes" %(myfile, mystat.st_size), end=" ") #add back
                    self.filesLeft[myfile[myElementsLeftFolder:]] = mystat  # .st_size

        for root, dirs, files in os.walk(self.rightFolder):
            for myFileName in files:
                myfile = os.path.join(root, myFileName)
                if not myFileName.endswith('lock'):
                    mystat = os.stat(myfile)
                    # print("%s occupies %d bytes" %(myfile, mystat.st_size), end=" ") # add back
                    self.filesRight[myfile[myElementsRightFolder:]] = mystat


    def getFilesLeft(self):
        return self.filesLeft

    def getFilesRight(self):
        return self.filesRight

    def setSyncType(self, aSyncType):
        if aSyncType.__class__ == "".__class__ and aSyncType in self.syncTypeList.keys():
            self.syncType = self.syncTypeList[aSyncType]

    def copyFromRightToLeft(self, myFile):
        print("copy r->l")
        shutil.copy2(self.rightFolder + myFile, self.leftFolder + myFile)

    def copyFromLeftToRight(self, myFile):
        print("copy l->r")
        shutil.copy2(self.leftFolder + myFile, self.rightFolder + myFile)

    def syncNow(self):
        for myFile in self.inLeftButNotInRight:
            shutil.copy2(self.leftFolder + myFile, self.rightFolder + myFile)
        for myFile in self.inRightButNotInLeft:
            shutil.copy2(self.rightFolder + myFile, self.leftFolder + myFile)

        mySyncMode = self.getSyncType()
        for myFile in self.inBothButDifferent:
            if mySyncMode == 0:
                print("default keep both copies")
                mySplitPath = os.path.split(self.leftFolder + myFile)
                myNewFile = os.path.join(mySplitPath[0], "c0py_" + mySplitPath[1])
                shutil.move(self.leftFolder + myFile, myNewFile) # left.a >> left.new_a
                self.copyFromRightToLeft(myFile) # right.a -> left.a
                mySplitPath = os.path.split(self.rightFolder + myFile)
                myNewFileRight = os.path.join(mySplitPath[0], "c0py_" + mySplitPath[1])
                shutil.copy2(myNewFile, myNewFileRight) # left.new_a -> right.new_a

                # print("L new", myNewFile)
                # print("L", self.leftFolder + myFile)
                # print("R", self.rightFolder + myFile)

            elif mySyncMode == 1:
                print("use bigger file")
                myLFStat = self.filesLeft[myFile]
                myRFStat = self.filesRight[myFile]
                if myLFStat.st_size < myRFStat.st_size:
                    self.copyFromRightToLeft(myFile)
                else:
                    self.copyFromLeftToRight(myFile)
            else:
                myLFStat = self.filesLeft[myFile]
                myRFStat = self.filesRight[myFile]
                print("use newer file")
                if myLFStat.st_mtime < myRFStat.stmtime:
                    self.copyFromRightToLeft(myFile)
                else:
                    self.copyFromLeftToRight(myFile)

            # vector_stanga = [self.leftFolder + f for f in self.inBothButDifferent]
            # vector_dreapta = [self.rightFolder + f for f in self.inBothButDifferent]

            # spl = os.path.split(path)
            # os.path.join(spl[0], 'c0py_' + spl[1]) =>
            # Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that.

    def runComparison(self):

        self.visitAllSubfolders()

        set_a = set(self.getFilesLeft().keys())
        set_b = set(self.getFilesRight().keys())
        for k, v in self.getFilesRight().items():
            print("[%s] = %s" % (self.rightFolder + k, v.st_size))
        self.inLeftButNotInRight = set_a.difference(set_b)
        self.inRightButNotInLeft = set_b.difference(set_a)
        self.inBothButDifferent = set_a.intersection(set_b)

        self.checkSimilarItems()

        self.comparatorStatus.updateStatus("comparison done")

    def printReport(self):
        # filesTestArray = []

        print("LEFT")
        for f in self.inLeftButNotInRight:
            print(" " * 4 + self.leftFolder + f + " in " + self.rightFolder + f)
        print("RIGHT")
        for f in self.inRightButNotInLeft:
            print(" " * 4 + self.rightFolder + f + " in " + self.leftFolder + f)

        # vector_stanga = [self.leftFolder + f for f in self.inBothButDifferent]
        # vector_dreapta = [self.rightFolder + f for f in self.inBothButDifferent]

        print("BOTH")
        # for (myFileLeft, myFileRight) in zip(vector_stanga, vector_dreapta):
        #     print("    %s is similar to other folder %s " % (myFileLeft, filecmp.cmp(myFileLeft, myFileRight)))
        for myFile in self.inBothButDifferent:
            print("    is the same file %s ? %s" % (myFile, filecmp.cmp(self.leftFolder + myFile, self.rightFolder + myFile)))

            # no working?
            # filecmp.cmpfiles(vector_stanga, vector_dreapta, filesTestArray, shallow=False)
            # print("simiar files %s" % filesTestArray)

    def isInSync(self):
        if len(self.inLeftButNotInRight) == 0 and len(self.inRightButNotInLeft) == 0:
            self.comparatorStatus.setStatus("synced")
            return True
        else:
            self.comparatorStatus.setStatus("not synced")
            return False

    def printStats(self):
        print("object size %04d bytes" % sys.getsizeof(self))
        print("comparator size %04d bytes" % sys.getsizeof(self.comparatorStatus))
        print("left array  %d elements occupying %04d Bytes" % (len(self.filesLeft), sys.getsizeof(self.filesLeft)))
        print("right array %d elements occupying %04d Bytes" % (len(self.filesRight), sys.getsizeof(self.filesRight)))

    def checkSimilarItems(self):
        myMatchedFiles = []
        for myFile in self.inBothButDifferent:
            if filecmp.cmp(self.leftFolder + myFile, self.rightFolder + myFile):
                myMatchedFiles.append(myFile)
        for myFile in myMatchedFiles:
            self.inBothButDifferent.remove(myFile)

    def getSyncType(self):
        return self.syncType


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        leftSide = sys.argv[1]
        rightSide = sys.argv[2]

        obiectule = FolderComparator(leftSide, rightSide)
        obiectule.runComparison()
        obiectule.setSyncType("keepboth")
        # print(obiectule.getSyncType())

        if not obiectule.isInSync():
            #obiectule.printStats()
            obiectule.printReport()
            obiectule.syncNow()
            obiectule.runComparison()
            obiectule.printReport()
        else:
            print("a-ok")
    else:
        print("error parsing arguments")
