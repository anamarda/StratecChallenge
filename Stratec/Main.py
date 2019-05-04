from tkinter import *

from Repo import Repo
from Service import Service
from GUI import GUI

repoBasics = Repo("data\The_Basics.csv")
repoDuplicates = Repo("data\Duplicates.csv")
repoDuplicatesAdvanced = Repo("data\Duplicates_Advanced.csv")

srv = Service(repoBasics, repoDuplicates, repoDuplicatesAdvanced)

window = Tk()
window.title("I am an Object")
window.configure(background="white")

app = GUI(window, srv)

window.mainloop()
