import numpy as np
from PIL import Image, ImageTk, ImageColor
from io import BytesIO
from tkinter import ttk, Canvas, NW
import os
from configspace import Configspace
from utils import isPixelWhite


class Workspace:
    def __init__(self, robotImagePath, envImagePath, root):

        self.root = root
        self.envImage = Image.open(envImagePath)
        self.envArray = np.array(self.envImage)
        self.envPhoto = ImageTk.PhotoImage(self.envImage)

        self.robotImage = Image.open(robotImagePath)
        self.robotArray = np.array(self.robotImage)
        self.robotPhoto = ImageTk.PhotoImage(self.robotImage)
        self.robotOutline = self.getRobotsOutline()

        self.label = ttk.Label(root, image=self.envPhoto)

        self.currentPos = (0, 0)
        self.isInitialize = False

    def drawAll(self, xCurrent, yCurrent, xInit=-1, yInit=-1, xGoal=-1, yGoal=-1):
        self.currentPos = xCurrent, yCurrent
        self.imageToDraw = self.envImage.copy()
        if xInit > -1: self.imageToDraw.paste(self.robotImage.copy(), (xInit, yInit))
        if xGoal > -1: self.imageToDraw.paste(self.robotImage.copy(), (xGoal, yGoal))
        self.imageToDraw.paste(self.robotImage.copy(), (self.currentPos[0], self.currentPos[1]))
        self.photoToDraw = ImageTk.PhotoImage(self.imageToDraw)
        self.label.configure(image=self.photoToDraw)
        self.label.image = self.photoToDraw
        self.label.pack(side="bottom", fill="both", expand="yes")

    def isInCollision(self, x, y):
        for i in range(len(self.robotOutline)):
            if self.envArray[y+self.robotOutline[i][1], x+self.robotOutline[i][0]][0] != 255:
                return True

        return False

    def getRobotsOutline(self):
        outlineCoordinates = np.empty((0, 2), int)

        for x in range(len(self.robotArray)):
            for y in range(len(self.robotArray[0])):
                if self.robotArray[x][y][0] <= 250 and self.pixelIsPartOfRobotsOutline(x, y):
                    outlineCoordinates = np.append(outlineCoordinates, np.array([[x, y]]), axis=0)

        return outlineCoordinates


    def pixelIsPartOfRobotsOutline(self, x, y):
        if x == 0 or y == 0:
            return True
        if x == len(self.robotArray)-1 or y == len(self.robotArray)-1:
            return True
        if self.robotArray[x-1][y][0] >= 250 or self.robotArray[x+1][y][0] >= 250:
            return True
        if self.robotArray[x][y-1][0] >= 250 or self.robotArray[x][y+1][0] >= 250:
            return True

        return False