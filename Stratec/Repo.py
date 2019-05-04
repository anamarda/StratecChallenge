import numpy as np

class Repo():
    def __readFromFile(self):
        '''
        Reading the data from file.
        '''
        with open(self.__fileName, "r") as f:
            line = f.readline().strip().split(",")
            self.__matrix = np.array(line)

            for line in f.readlines():
                line = line.strip()

                if(len(line) > 0):
                    line = line.split(",")
                    data = np.array(line)
                    self.__matrix = np.vstack((self.__matrix, data))



    def __init__(self, fileName):
        '''
        Initialize the class.
        Input: fileName - the name of the file with data.
        '''
        self.__fileName = fileName
        self.__matrix = []
        self.__readFromFile()



    def getMatrix(self):
        '''
        Getter of the matrix.
        Output: returns the matrix.
        '''
        return self.__matrix