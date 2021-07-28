from tkinter import Canvas, CENTER
import numpy as np
from dijkstar import Graph, find_path
from collections import deque

class Configspace:

    def off(self, x):
        return x + self.theOffset

    def __init__(self, root, workspace):
        self.initConfig = -1, -1
        self.goalConfig = -1, -1
        self.solutionPath = []
        self.isInitialize = False
        self.root = root
        self.xExt = 0
        self.yExt = 0
        self.canvas = Canvas(self.root)
        self.theOffset = 24
        self.workspace = workspace

    def setDimensions(self, x, y):
        self.xExt = x
        self.yExt = y
        off = self.theOffset
        self.canvas.config(bd=0, height=y + 2 * self.theOffset, width=x + 2 * self.theOffset)
        self.drawSpace()
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def drawSpace(self):
        self.canvas.delete("all")
        y = self.yExt
        x = self.xExt
        self.canvas.create_line(self.off(0), self.off(0), self.off(0), self.off(y))
        self.canvas.create_line(self.off(0), self.off(0), self.off(x), self.off(0))
        self.canvas.create_line(self.off(x), self.off(y), self.off(x), self.off(0))
        self.canvas.create_line(self.off(x), self.off(y), self.off(0), self.off(y))

        if len(self.solutionPath) > 0: self.drawSolutionPath()
        if self.initConfig[0] > -1: self.drawConfiguration(self.initConfig[0], self.initConfig[1], 'green')
        if self.goalConfig[0] > -1: self.drawConfiguration(self.goalConfig[0], self.goalConfig[1], 'red')

    def drawConfiguration(self, x, y, color):
        r = 5
        self.canvas.create_oval(self.off(x - r), self.off(y - r), self.off(x + r), self.off(y + r), fill=color)

    def drawSolutionPath(self):
        for i in range(1, len(self.solutionPath)):
            c1 = self.solutionPath[i - 1]
            c2 = self.solutionPath[i]
            self.canvas.create_line(self.off(c1[0]), self.off(c1[1]), self.off(c2[0]), self.off(c2[1]), fill='purple1')

    def drawCObs(self, x, y):
        for i in range(1081, 1302):
            for j in range(197, 392):
                if self.workspace.isInCollision(i, j):
                    self.canvas.create_line(self.off(i), self.off(j), self.off(i+1), self.off(j))
        pass

    def setIntialSolutionPath(self):
        resolution = max(abs(
            self.initConfig[0] - self.goalConfig[0]), abs(self.initConfig[1] - self.goalConfig[1]))

        pathSPRM = self.sprmPath(self.initConfig, self.goalConfig, r=20, n=100)

        if len(pathSPRM) > 1:
            self.solutionPath = pathSPRM[0]
        else:
            self.solutionPath.append(self.initConfig)
            for i in range(1, resolution):
                deltaX = round(i * float(self.goalConfig[0] - self.initConfig[0]) / float(resolution))
                deltaY = round(i * float(self.goalConfig[1] - self.initConfig[1]) / float(resolution))
                newX = self.initConfig[0] + deltaX
                newY = self.initConfig[1] + deltaY
                self.solutionPath.append((newX, newY))
            self.solutionPath.append(self.goalConfig)

    def sprmPath(self, init, goal, r, n):
        edges = deque()
        vertices = []
        vertices.append(init)
        vertices.append(goal)

        xMin = goal[0]
        xMax = init[0]

        yMin = goal[1]
        yMax = init[1]

        if init[0] <= goal[0]:
            xMin = init[0]
            xMax = goal[0]

        if init[1] <= goal[1]:
            yMin = init[1]
            yMax = goal[1]

        for i in range(0, n):
            vertices.append(self.cFreeSpace(xMin, xMax, yMin, yMax))

        for v in vertices:
            uTemp = self.neighbors(v, vertices, r)

            for u in uTemp:
                if self.edgeIsValid(u, v):
                    weight = np.sqrt(np.square(u[0]-v[0]) + np.square(u[1]-v[1]))
                    edges.append((u, v, weight))

        graph = Graph()
        for e in edges:
            graph.add_edge(e[0], e[1], e[2])

        try:
            path = find_path(graph, init, goal)
            return path
        except Exception as e:
            print(e)
            return []

    def cFreeSpace(self, xMin, xMax, yMin, yMax):
        x = np.random.randint(xMin, xMax)
        y = np.random.randint(yMin, yMax)

        while self.workspace.isInCollision(x, y):
            x = np.random.randint(xMin, xMax)
            y = np.random.randint(yMin, yMax)

        return x, y

    def neighbors(self, v, vertices, r):
        neighbors = []
        for vTemp in vertices:
            if vTemp[0] == v[0] and vTemp[1] == v[1]:
                continue
            if np.square(vTemp[0] - v[0]) + np.square(vTemp[1] - v[1]) <= np.square(r):
                neighbors.append(vTemp)

        return neighbors

    def edgeIsValid(self, u, v):
        resolution = max(abs(v[0] - u[0]), abs(v[1] - u[1]))

        for i in range(1, resolution):
            deltaX = round(i * float(u[0] -v[0]) / float(resolution))
            deltaY = round(i * float(u[1] - v[1]) / float(resolution))
            newX = v[0] + deltaX
            newY = v[1] + deltaY
            if self.workspace.isInCollision(newX, newY):
                return False

        return True








