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
        self.robotBorder = self.getRobotBorder()

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

        if self.envArray[y, x][0] != 255:
            return True

        return False

    def getRobotBorder(self):

        for x in range(0, len(self.robotArray)):
            if self.robotArray[0, x] != 255:
                pass