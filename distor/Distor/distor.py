#! /usr/bin/env python3

import os
import json
import argparse
from datetime import datetime, date
from sty import fg, ef, rs
from .sheet import Sheet

HOME = "/home/ahacad/.distor/Dev/"
storedPath = HOME + "stored.json"
#deprecatedPath = HOME + "deprecated.json"
#extendedPath = HOME + "extended.json"
metaPath = HOME + "meta.json"  # store color schemes
colorsDic = {"red": fg.red,
             "green": fg.green,
             "yellow": fg.yellow,
             "blue": fg.blue,
             "magenta": fg.magenta,
             "cyan": fg.cyan,
             "white": fg.white,
             "": ""}


class Distor(Sheet):

    ## Add option for automatically increase N days when copying a row
    ## Calculate whether you can make it before ddl

    def __init__(self, sheet):
        self.sheet = sheet
        self.width = len(sheet[0])
        self.height = len(sheet)
        self.remainSections = 0
        self.skipColList = [0, 7, 8]
        self.skipRowList = []

        self.manageArgs()
        self.manageColors()
        self.manageOperations()
        self.managePrints()
        #self.printDistor()

        self.saveSheet(storedPath)

    def manageArgs(self):
        """manage argparse"""
        parser = argparse.ArgumentParser()
        parser.add_argument("--colorScheme", action="store_true")
        parser.add_argument("-a", nargs=6)
        parser.add_argument("-d", nargs=1)
        parser.add_argument("-c", nargs=1)
        parser.add_argument("-f", nargs=3)
        parser.add_argument("-m", nargs=2)
        parser.add_argument("-n", action="store_true")
        parser.add_argument("--all", action="store_true")
        parser.add_argument("--ddl", action="store_true")
        parser.add_argument("-p", nargs=1, default="2")  # padding in printing
        self.args = parser.parse_args()

    def loadColorScheme(self):
        """load color scheme, if not exist, creat one"""
        if not os.path.exists(metaPath):
            defaultColorScheme = ["white", "green", "blue", "yellow",
                                  "cyan", "red", "magenta", "white", "white"]
            with open(metaPath, "w") as json_file:
                json.dump(defaultColorScheme, json_file, indent=4)
        with open(metaPath) as json_file:
            self.metas = json.load(json_file)
            self.colorScheme = self.metas[0]

    def changeColorScheme(self):
        """change the color scheme"""
        pass

    def printColorScheme(self):
        """print the color scheme along with header"""
        if self.args.colorScheme:
            for i in range(len(self.colorScheme)):
                print(self.colorScheme[i], " ")
    
    def manageColors(self):
        """manage color related things"""
        self.loadColorScheme()
        self.printColorScheme()

    def sortFunc(self, colNum, fromRowNum, toRowNum):
        """sort the rows according to the specific column
        in the rows [fromRowNum, toRowNum]
        """
        if 0 <= fromRowNum and fromRowNum <= toRowNum and toRowNum <= self.height:
            self.sheet[fromRowNum:toRowNum] = sorted(self.sheet[fromRowNum:toRowNum], key=lambda x: x[colNum])

    def sortDistor(self):
        """sort the sheet"""
        self.sortFunc(5, 1, self.height)

    def metaNumberPlus(self):
        """increase number by one"""
        number = self.metas[1][0]
        num = int(number) + 1
        number = str(num)
        self.metas[1][0] = "0" * (5 - len(number)) + number
        return self.metas[1][0]

    def metaNumberMinus(self):
        """increase number by one"""
        number = self.metas[1][0]
        num = int(number) - 1
        number = str(num)
        self.metas[1][0] = "0" * (5 - len(number)) + number
        return self.metas[1][0]

    def filtDistor(self):
        """filt"""
        filtRowList = self.filt(int(self.args.f[0]), self.args.f[1], 1, self.height, rule=self.args.f[2])
        for i in range(1, self.height):
            if i not in filtRowList:
                self.skipRowList.append(i)

    def addToDistor(self):
        """add to distor"""
        newRow = self.sheet[0][:]
        newRow[0] = self.metaNumberPlus()
        newRow[1] = self.args.a[0]
        newRow[2] = self.args.a[1]
        newRow[3] = self.args.a[2]
        newRow[4] = self.args.a[3]
        newRow[5] = self.args.a[4]
        newRow[6] = self.args.a[5]
        self.addRow(newRow)

    def distorDelete(self):
        """delete a row"""
        if int(self.args.d[0]) > 0:
            self.deleteRow(int(self.args.d[0]))
        self.height -= 1

    def modifyDistorRow(self):
        """modify a row in distor"""
        rowNum = int(self.args.m[0])
        colNum = int(self.args.m[1].split("=")[0])
        cell = self.args.m[1].split("=")[1]
        self.modifyCell(rowNum, colNum, cell)


    def manageOperations(self):
        """"""
        if self.args.a:  # add
            self.addToDistor()
        elif self.args.d:  # delete
            self.distorDelete()
        elif self.args.c:  # copy
            newRow = self.sheet[int(self.args.c[0])][:]
            newRow[0] = self.metaNumberPlus()
            self.addRow(newRow)
        elif self.args.m:
            self.modifyDistorRow()
        if self.args.f:  # filt
            self.filtDistor()
        if self.args.ddl:
            pass
        self.sortDistor()

    def getInt(self, x):
        """convert x to int"""
        if x.isdigit():
            return int(x)
        else:
            return 0

    def calculateDDL(self, rowNum, padding):
        """calculate DDL and print"""
        if rowNum == 0:
            print(f"{'SUM':^{3 + padding}}|", end="")
        else:
            self.remainSections += int(self.sheet[rowNum][3]) - self.getInt(self.sheet[rowNum][7])
            print(f"{self.remainSections:^{3 + padding}}|", end="")

    def printRow(self, rowNum, padding=2, color="YES"):
        """print one row in distor, according to the color scheme"""
        if rowNum in self.skipRowList:
            return 0
        if color:
            colorScheme = self.colorScheme
        else:
            colorScheme = ["" for i in range(len(self.colorScheme))]
        for j in range(self.width):
            if j in self.skipColList:
                continue
            print(colorsDic[colorScheme[j]], end="")
            print(f"{self.sheet[rowNum][j]:^{self.colWidth[j] + padding}}", end="")
            print(fg.rs, end="")
            print("|", end="")
        if self.args.ddl:
            self.calculateDDL(rowNum, padding)

    def managePrints(self):
        """"""
        self.colWidth = [0 for i in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                self.colWidth[j] = max(self.colWidth[j], len(self.sheet[i][j]))
        if self.args.all:
            self.printSheetWithNumber()
        else:
            if self.args.n:
                self.skipColList = []
            self.printRow(0, padding=int(self.args.p[0]), color="")
            print("\n", end="")
            for i in range(1, self.height):
                self.printRow(i, padding=int(self.args.p[0]))
                print("\n", end="")
    
    def saveSheet(self, storedPath):
        """save the sheet"""
        with open(storedPath, "w") as json_file:
            json.dump(self.sheet, json_file, indent=4)
        with open(metaPath, "w") as json_file:
            json.dump(self.metas, json_file, indent=4)


    # CALCULATE DDL MODULE

def loadSheet():
    """load sections from the stored json file
    """
    with open(storedPath) as json_file:
        sheet = json.load(json_file)
    #with open(deprecatedPath) as json_file:
    #    deprecatedSheet = json.load(json_file)
    #with open(extendedPath) as json_file:
    #    extendedSheet = json.load(json_file)
    #return sheet, deprecatedSheet, extendedSheet
    return sheet


distor = Distor(loadSheet())






# WHAT NEXT
# learn to use argparse better, and build usages around it
#
#
# YET TO BUILD:
## LITTLE THINGS
# testInput (with python raise exceptions, help ensure input quality)
#
#
## MAIN FEATURE

### What next
#   - learn OOP
#   - learn click
# ==> fininsh the features
#   - learn urwid
# ==> make the gui interface
### REWRITE the whole program with OOP
### REwrite data structures into more flexible excel-like columns and rows
### rewrite cli with click, substituting argparse
#      more flexible prints
###  CHECK whether you can make it before DDL


# techniques used:
# - json, for data process
# - format alignment and colored printing
# - sty, for colors
# - argParse, for cli
