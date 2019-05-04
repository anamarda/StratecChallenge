import numpy as np
from Repo import Repo

class Service():
    def __init__(self, repoBasics, repoDuplicates, repoDuplicatesAdvanced):
        '''
        Initialize the repos.
        '''
        self.__repoBasics = repoBasics
        self.__repoDuplicates = repoDuplicates
        self.__repoDuplicatesAdvanced = repoDuplicatesAdvanced

        

    def level_1(self, repo):
        '''
        Find the non-noise objects.
        Returns a dictionary with the following information:
            - the list of the non-noise objects;
            - the number of the non-noise objects.
        '''
        
        objects = self.__findObjects(repo)
        nonNoise = []
        for object in objects:
            #considering the object as a noisy one
            noisyX = True
            noisyY = True
            
            #verify for x-coordinate
            x = object[0][0]
            for pair in object:
                if(pair[0] != x):
                    noisyX = False

            #verify for y-coordinate
            y = object[0][1]
            for pair in object:
                if(pair[1] != y):
                    noisyY = False

            if((noisyX or noisyY) == False):
                nonNoise.append(object)

        return {
                "nonNoise" : nonNoise,
                "numberNonNoise" : len(nonNoise)
                }



    def level_2(self, repo):
        '''
        Find the (X, Y) coordinates for the bounding boxes surrounding each object.
        Returns a dictionary with the following information:
            - the list of the non-noise objects;
            - the number of the non-noise objects;
            - a list for each object with its origin, width and height.
        '''

        dict = self.level_1(repo)
        nonNoise = dict["nonNoise"]
        boundingBoxes = []

        #sorting the pairs corresponding to each object, firstly after x, secondly after y
        for object in nonNoise:
            object.sort(key = lambda x: (x[0]))
            xmin = object[0][0] - 1
            xmax = object[-1][0] - 1

            object.sort(key = lambda x: (x[1]))
            ymin = object[0][1] - 1
            ymax = object[-1][1] - 1

            origin = [xmin, ymin]
            w = ymax - ymin + 3           
            h = xmax - xmin + 3

            boundingBoxes.append([origin, w, h])

        return {
            "nonNoise" : dict["nonNoise"],
            "numberNonNoise" : len(nonNoise),
            "boundingBoxes" : boundingBoxes
            }



    def level_3(self, repo):
        '''
        Find the duplicates of the objects.
        Returns a dictionary with the following information:
            - the list of the non-noise objects;
            - the number of the non-noise objects;
            - a list for each object with its origin, width and height;
            - a list of lists. Each list from the list consists of the objects that are duplicated and their information (origin, height, width).
        '''

        dict = self.level_2(repo)
        nonNoise = dict["nonNoise"]
        numberNonNoise = dict["numberNonNoise"]
        boundingBoxes = dict["boundingBoxes"]

        #a list of lists - each element is a list with the duplicate objects
        duplicatesList = []

        #list of checked bounding boxes
        checkedBoxes = []

        for boundingBox in boundingBoxes:
            #duplicates for this object
            list = []

            if(boundingBox not in checkedBoxes):               
                checkedBoxes.append(boundingBox)

                origin = boundingBox[0]
                width = boundingBox[1]
                height = boundingBox[2]
                crtObject = self.__buildMatrix(repo.getMatrix(), origin[0], origin[1], height, width)
            
                list.append(boundingBox)

                for boundingBoxOther in boundingBoxes:
                    if(boundingBoxOther not in checkedBoxes):
                        originOther = boundingBoxOther[0]
                        widthOther = boundingBoxOther[1]
                        heightOther = boundingBoxOther[2]
                        otherObject = self.__buildMatrix(repo.getMatrix(), originOther[0], originOther[1], heightOther, widthOther)

                        if(np.array_equal(crtObject, otherObject)):
                            list.append(boundingBoxOther)
                            checkedBoxes.append(boundingBoxOther)

                duplicatesList.append(list)
       
        return {
            "nonNoise" : dict["nonNoise"],
            "numberNonNoise" : len(nonNoise),
            "boundingBoxes" : boundingBoxes,
            "duplicatesList" : duplicatesList
            }



    def  level_4(self, repo):
        '''
        Find the duplicates of the objects, some of them rotated.
        Returns a dictionary with the following information:
            - the list of the non-noise objects;
            - the number of the non-noise objects;
            - a list for each object with its origin, width and height;
            - a list of lists. Each list from the list consists of the objects that are duplicated and their information (origin, height, width);
            - a list of lists. Each list from the list consists of the objects that are duplicated (rotated or not) and 
                their information (origin, height, width).
        '''

        dict = self.level_3(repo)
        nonNoise = dict["nonNoise"]
        numberNonNoise = dict["numberNonNoise"]
        boundingBoxes = dict["boundingBoxes"]
        duplicatesList = dict["duplicatesList"]

        #a list of lists - each element is a list with the duplicate objects and the degree
        duplicatesListAdvanced = []

        #list of checked bounding boxes
        checkedBoxes = []

        for boundingBox in boundingBoxes:
            #duplicates for this object
            list = []

            if(boundingBox not in checkedBoxes):               
                checkedBoxes.append(boundingBox)

                origin = boundingBox[0]
                width = boundingBox[1]
                height = boundingBox[2]
                crtObject = self.__buildMatrix(repo.getMatrix(), origin[0], origin[1], height, width)
            
                list.append([boundingBox, 0])

                for boundingBoxOther in boundingBoxes:
                    if(boundingBoxOther not in checkedBoxes):
                        originOther = boundingBoxOther[0]
                        widthOther = boundingBoxOther[1]
                        heightOther = boundingBoxOther[2]
                        otherObject = self.__buildMatrix(repo.getMatrix(), originOther[0], originOther[1], heightOther, widthOther)

                        list, checkedBoxes = self.__check2Objects(crtObject, otherObject, list, checkedBoxes, boundingBoxOther)

                duplicatesListAdvanced.append(list)
       
        return {
            "nonNoise" : dict["nonNoise"],
            "numberNonNoise" : len(nonNoise),
            "boundingBoxes" : boundingBoxes,
            "duplicatesList" : duplicatesList,
            "duplicatesListAdvanced" : duplicatesListAdvanced
            }

    

    def __check2Objects(self, crtObject, otherObject, list, checkedBoxes, boundingBoxOther):   
        '''
        Checks if 2 objects are alike, rotated or not.
        Input:
            - crtObject, otherObject: matrixes;
            - list: the list of the information (origin, width, height, rotation degrees) of the identical objects;
            - checkedBoxes: a list of the information of the objects that have been checked;
            - boundingBoxOther: the information (origin, width, height) of the otherObject.
        Returns the list and the checkedBoxes list.
        '''

        if(np.array_equal(crtObject, otherObject)):
            degrees = 0
            list.append([boundingBoxOther, degrees])
            checkedBoxes.append(boundingBoxOther)
        elif(np.array_equal(crtObject, np.rot90(otherObject, k=3))):
            degrees = 90
            list.append([boundingBoxOther, degrees])
            checkedBoxes.append(boundingBoxOther)
        elif(np.array_equal(crtObject, np.rot90(otherObject, k=2))):
            degrees = 180
            list.append([boundingBoxOther, degrees])
            checkedBoxes.append(boundingBoxOther)
        elif(np.array_equal(crtObject, np.rot90(otherObject, k=1))):
            degrees = 270
            list.append([boundingBoxOther, degrees])
            checkedBoxes.append(boundingBoxOther)
        return list, checkedBoxes


    def __findObjects(self, repo):
        '''
        Function that finds all the objects (noise + non-noise).
        Returns a list of objects (noise + non-noise).
        '''

        matrix = np.copy(repo.getMatrix())
        objects = []

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if(matrix[i][j] == '1'):
                    XY = []
                    self.__verifyObject(i, j, matrix, XY)
                    objects.append(XY)
        return objects



    def __verifyObject(self, start_x, start_y, matrix, XY):
        '''
        Function that finds the limits of an object.
        Input:
            start_x - starting point of the object on the x-coordinate
            start_y - starting point of the object on the y-coordinate
            matrix - the given matrix with objects
            XY - array with the coordinates of each '1' of the object
        '''
        q = Queue()
        q.enqueue([start_x, start_y])

        while(q.isEmpty() == False):
            #pair of coordinates (x, y)
            pair = q.dequeue()

            if(pair not in XY):
                x = pair[0]
                y = pair[1]
            
                #mark as visited
                matrix[x][y] = '2'
                XY.append([x, y])

                if(x < len(matrix) - 1 and matrix[x+1][y] == '1'):
                   q.enqueue([x + 1, y])
                if(y < len(matrix[0]) - 1 and matrix[x][y+1] == '1'):
                   q.enqueue([x, y + 1])
                if(x > 0 and matrix[x-1][y] == '1'):
                    q.enqueue([x - 1, y])
                if(y > 0 and matrix[x][y-1] == '1'):
                    q.enqueue([x, y - 1])        

    


    def getBasicMatrix(self):
        '''
        Getter of the matrix of the Basics file.
        Output: returns the matrix.
        '''
        return self.__repoBasics.getMatrix()


    def getDuplicatesMatrix(self):
        '''
        Getter of the matrix of the Duplicates file.
        Output: returns the matrix.
        '''
        return self.__repoDuplicates.getMatrix()


    def getRepoBasics(self):
        '''
        Getter of the repoBasics.
        Output: returns the repo.
        '''
        return self.__repoBasics


    def getRepoDuplicates(self):
        '''
        Getter of the repoDuplicates.
        Output: returns the repo.
        '''
        return self.__repoDuplicates     
    

    def getRepoDuplicatesAdvanced(self):
        '''
        Getter of the repoDuplicatesAdvanced.
        Output: returns the repo.
        '''
        return self.__repoDuplicatesAdvanced  



    def __buildMatrix(self, matrix, originX, originY, height, width):
        '''
        Function that builds a submatrix from a matrix. 
        Input:
            - matrix: the given matrix which contains tha submatrix;
            - originX, originY: the starting point of the submatrix;
            - height, width: the height and the width of the submatrix;
        Output: returns the submatrix.
        '''
        mat = np.zeros((height, width))
        for x in range(height):
            for y in range(width):
                mat[x][y] = matrix[x + originX][y + originY]

        return mat




class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)