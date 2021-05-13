import tkinter
from tkinter import ttk, RIGHT, Canvas, BOTH, Scale, HORIZONTAL
from workspace import Workspace
from configspace import Configspace
from controller import Controller
from PIL import ImageTk, Image
import os
from utils import setBackgroundColor
import numpy as np
from sklearn import neighbors



def demo():
    root = tkinter.Tk()
    root.title("Motion Planning")
    universal_height = 1000

    nb = ttk.Notebook(root)
    page1 = ttk.Frame(nb, width=1080, height=universal_height)
    page2 = ttk.Frame(nb, width=1080, height=universal_height)

    nb.add(page1, text='Workspace')
    nb.add(page2, text='Configspace')
    nb.grid(column=0)

    workspace = Workspace("./resources/robot_BW_small.bmp", "./resources/Room_BW_small.bmp", page1)
    configspace = Configspace(page2, workspace=workspace)
    controller = Controller(workspace, configspace)

    workspace.drawAll(workspace.currentPos[0], workspace.currentPos[1])

    def callback(event):
        controller.drawMouseOffSet(event.x, event.y)
        if controller.isInCollision():
            setBackgroundColor(page1, "red")
        else:
            setBackgroundColor(page1, "green")

    workspace.label.bind("<Button-1>", callback)

    def moveRobotOnPath(val):
        if controller.isAllInitialized():
            controller.setSolutionPathOnCurrentPos(int(val))
            controller.drawCurrentPos()
            if controller.isInCollision():
                setBackgroundColor(page1, "red")
            else:
                setBackgroundColor(page1, "green")

    slider = Scale(page1, from_=0, to=200, orient=HORIZONTAL, command=moveRobotOnPath)
    slider.config(length=600)

    def set_goal():
        controller.setCurrentPosAsGoal()
        slider['from_'] = 0
        slider['to_'] = len(configspace.solutionPath) - 1

    setGoalButton = ttk.Button(page1, text='Set Goal', command=set_goal)
    setGoalButton.pack(side=tkinter.RIGHT)

    def set_init():
        controller.setCurrentPosAsInit()

    setInitButton = ttk.Button(page1, text='Set Init', command=set_init)
    setInitButton.pack(side=tkinter.RIGHT)

    slider.pack()

    root.mainloop()


def testKDTree():
    X = np.array([[7, 1], [3, 2], [1, 5], [0, 8], [7, 4], [5, 5], [8, 4], [6, 2]])
    tree = neighbors.KDTree(X)
    index = tree.query(X[7:], k=2, return_distance=False)[0][1]
    print(index)


if __name__ == "__main__":
    demo()
    #testKDTree()
