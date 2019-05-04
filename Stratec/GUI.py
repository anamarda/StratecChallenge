from tkinter import *

class GUI():

    def __init__(self, window, service):
        self.__window = window
        self.__service = service

        self.__panel = PanedWindow(orient=VERTICAL)
        self.__panel.configure(background="grey90")
        self.__panel.pack(fill=BOTH, expand=1)

        #the width and height of the canvas
        h = 10 * len(self.__service.getBasicMatrix())
        w = 10 * len(self.__service.getBasicMatrix()[0])

        self.__canvas = Canvas(self.__panel, width=w, height=h)
        self.__canvas.pack()       
        self.__colorCanvas(self.__service.getBasicMatrix())

        #answer label
        self.__label = Label(self.__panel, text="Answer: ", bg="grey90", font="none 15 bold")
        self.__label.pack(side="left")

        #answer textfield
        self.__text = Text(self.__panel, height=10, width=80, font="none 10 bold")
        self.__text.pack(side="left")
        

        #the buttons for the levels
        button_level1 = Button(self.__window, text="Level 1", width=25, command = lambda: self.level_1(self.__service.getRepoBasics())) 
        button_level1.pack(side="left")

        button_level2 = Button(self.__window, text="Level 2", width=25, command = lambda: self.level_2(self.__service.getRepoBasics())) 
        button_level2.pack(side="left")

        button_level3 = Button(self.__window, text="Level 3", width=25, command = lambda: self.level_3(self.__service.getRepoDuplicates())) 
        button_level3.pack(side="left")

        button_level4 = Button(self.__window, text="Level 4", width=25, command = lambda: self.level_4(self.__service.getRepoDuplicatesAdvanced())) 
        button_level4.pack(side="left")
    
        



    def __colorCanvas(self, matrix):
        '''
        Colors the squares of the canvas.
        Input:
            - matrix of '0'-s and '1'-s.
        '''
        w = len(matrix[0])
        h = len(matrix)
        
        for i in range(w):
            for j in range(h):
                if(matrix[j][i] == '0'):          
                    self.__canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="DarkSeaGreen1")
                else:
                    self.__canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, fill="red")




    def level_1(self, repo):
        '''
        The graphic interface of level 1.
        Input:
            - repo: the repository to which is applied the level 1 task.
        Output:
            - printing on the screen
            - printing on the GUI
        '''
        self.__colorCanvas(repo.getMatrix())

        string = "Level 1\n"

        dict = self.__service.level_1(repo)
        nonNoise = dict["nonNoise"]
        numberNonNoise = dict["numberNonNoise"]

        for object in nonNoise:
            for coordinates in object:
                y = coordinates[0]
                x = coordinates[1]
                self.__canvas.create_rectangle(x*10, y*10, x*10+10, y*10+10, fill="azure4")

        string += "{}\n".format(numberNonNoise)

        #printing on the screen
        print(string)

        #printing in the graphic interface
        self.__text.delete('1.0', END)
        self.__text.insert(END, string)



    def level_2(self, repo):
        '''
        The graphic interface of level 2.
        Input:
            - repo: the repository to which is applied the level 2 task.
        Output:
            - printing on the screen
            - printing on the GUI
        '''
        self.__colorCanvas(repo.getMatrix())
        string="Level 2:\n"

        self.level_1(repo)

        dict = self.__service.level_2(repo)
        boundingBoxes = dict["boundingBoxes"]

        for b in boundingBoxes:
            originY = b[0][0]
            originX = b[0][1]
            w = b[1]
            h = b[2]
            
            #paint the bounding squares
            for i in range(w):
                self.__canvas.create_rectangle((originX + i) * 10, originY * 10, (originX + i) * 10 + 10, originY * 10 + 10, fill="yellow")
                self.__canvas.create_rectangle((originX + i) * 10, (originY + h - 1) * 10, (originX + i) * 10 + 10, (originY + h - 1) * 10 + 10, fill="yellow")
            for i in range(h):
                self.__canvas.create_rectangle(originX*10, (originY + i)*10, originX*10+10, (originY + i)*10 + 10, fill="yellow")
                self.__canvas.create_rectangle((originX + w - 1)*10, (originY + i)*10, (originX + w - 1)*10+10, (originY + i)*10 + 10, fill="yellow")

            self.__canvas.create_rectangle(originX * 10, originY * 10, originX*10+10, originY * 10 + 10, fill="SkyBlue1")

            string += "({}, {}) W: {} H: {}\n".format(originX, originY, w, h)

        #printing on the screen
        print(string)

        #printing in the graphic interface
        self.__text.delete('1.0', END)
        self.__text.insert(END, string)



    def level_3(self, repo):
        '''
        The graphic interface of level 3.
        Input:
            - repo: the repository to which is applied the level 3 task.
        Output:
            - printing on the screen
            - printing on the GUI
        '''
        self.__colorCanvas(repo.getMatrix())
        string="Level 3:\n"

        self.level_1(repo)

        dict = self.__service.level_3(repo)
        duplicatesList = dict["duplicatesList"]
        numberObjects = dict["numberNonNoise"]

        string += "{}\n".format(numberObjects)

        self.__colorDuplicates(repo, duplicatesList)

        for row in duplicatesList:
            box = row[0]
            originY = box[0][0]
            originX = box[0][1]
            w = box[1]
            h = box[2]
            string += '({}, {}) W: {} H: {}'.format(originX, originY, w, h)

            if(len(row) > 1):
                string += ' – this object is also found at '
                for i in range(1, len(row) - 1):
                    box = row[i]
                    y = box[0][0]
                    x = box[0][1]
                    string += '({}, {}) and at '.format(x, y)
                b = row[-1]
                y = b[0][0]
                x = b[0][1]
                string += '({}, {})'.format(x, y)
            string += '\n'

        #printing on the screen
        print(string)

        #printing in the graphic interface
        self.__text.delete('1.0', END)
        self.__text.insert(END, string)



    def level_4(self, repo):
        '''
        The graphic interface of level 4.
        Input:
            - repo: the repository to which is applied the level 4 task.
        Output:
            - printing on the screen
            - printing on the GUI
        '''
        self.__colorCanvas(repo.getMatrix())
        string="Level 4:\n"

        self.level_1(repo)

        dict = self.__service.level_4(repo)
        duplicatesListAdvanced = dict["duplicatesListAdvanced"]
        numberObjects = dict["numberNonNoise"]

        string += "{}\n".format(numberObjects)

        self.__colorDuplicatesAdvanced(repo, duplicatesListAdvanced)

        for row in duplicatesListAdvanced:
            box = row[0][0]
            originY = box[0][0]
            originX = box[0][1]
            w = box[1]
            h = box[2]
            string += '({}, {}) W: {} H: {}'.format(originX, originY, w, h)

            if(len(row) > 1):
                string += ' – this object is also found at '
                for i in range(1, len(row) - 1):
                    box = row[i][0]
                    y = box[0][0]
                    x = box[0][1]
                    degrees = row[i][1]
                    if(degrees != 0):
                        string += '({}, {}), rotated by {} degrees, and at '.format(x, y, degrees)
                    else:
                        string += '({}, {}), and at '.format(x, y)

                b = row[-1][0]
                y = b[0][0]
                x = b[0][1]
                degrees = row[-1][1]
                if(degrees != 0):
                    string += '({}, {}), rotated by {} degrees'.format(x, y, degrees)
                else:
                    string += '({}, {})'.format(x, y)

            string += '\n'

        #printing on the screen
        print(string)

        #printing in the graphic interface
        self.__text.delete('1.0', END)
        self.__text.insert(END, string)



    def __colorDuplicates(self, repo, duplicateList):
        '''
        Coloring the duplicated objects.
        Input:
            - repo: the repository;
            - duplicateList: a list of the information of the duplicated objects.
        Output:
            - the duplicated objects are encircled with same color;
            - if an object does not have a duplicate, it will not be encircled (waste of color)
        '''
        matrix = repo.getMatrix()

        colorList = ["purple", "orange", 'deep sky blue', "yellow", "lawn green", "pink", "red", 'snow2', 'gray42', 'orchid3', 'plum1']
        noColor = 0
        for row in duplicateList:
            if(len(row) > 1):
                for k in range(len(row)):
                    box = row[k]
                    originY = box[0][0]
                    originX = box[0][1]
                    w = box[1]
                    h = box[2]
                    color = colorList[noColor]

                    self.__canvas.create_oval(originX*10-5, originY*10-5, (originX + w)*10+5, (originY + h)*10+5, outline=color, width='3')
                noColor += 1


    def __colorDuplicatesAdvanced(self, repo, duplicateList):
        '''
        Coloring the duplicated objects (also rotated).
        Input:
            - repo: the repository;
            - duplicateList: a list of the information of the duplicated objects.
        Output:
            - the duplicated objects are encircled with same color;
            - if an object does not have a duplicate, it will not be encircled (waste of color)
        '''
        matrix = repo.getMatrix()

        colorList = ["purple", "orange", 'deep sky blue', "yellow", "lawn green", "pink", "red", 'snow2', 'gray42', 'orchid3', 'plum1']
        noColor = 0
        for row in duplicateList:
            if(len(row) > 1):
                for k in range(len(row)):
                    box = row[k][0]
                    originY = box[0][0]
                    originX = box[0][1]
                    w = box[1]
                    h = box[2]
                    color = colorList[noColor]

                    self.__canvas.create_oval(originX*10-5, originY*10-5, (originX + w)*10+5, (originY + h)*10+5, outline=color, width='3')
                noColor += 1