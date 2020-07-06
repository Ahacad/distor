#! /usr/bin/env python3
# PROCESS OF OPERATION
# TODO: different stream of operations:
# DEFAULT: sort defaultly by ddl and print distor 
# Modify: 
#    change   : by number && by name? 
#    add    
#    delete       something and print distor
# filt: filter targeted elements and print>?
# sort by ** and print
# print whether you can make it before DDL
# 
### OPTIONS
# PRINT: partial/ALL print, color/no-color print


import os
import json
import argparse
from datetime import datetime, date
from sty import fg, ef, rs
from .sheet import Sheet

HOME = "/home/ahacad/.distor/Dev/"
storedPath = HOME + "stored.json"
deprecatedPath = HOME + "deprecated.json"
extendedPath = HOME + "extended.json"
metaPath = HOME + "meta.json"  # store color schemes
colorsDic = {"red": fg.red,
             "green": fg.green,
             "yellow": fg.yellow,
             "blue": fg.blue,
             "magenta": fg.magenta,
             "cyan": fg.cyan,
             "white": fg.white,
             "": ""}


# the functions to be achieved:
# First we save all the values as a big 2-dimensional array
# including "rows" and "columns" and the basic cells
# row-0 is the special row - the header
#
# we than can make a series of actions all these basic elements


class Distor(Sheet):

    def __init__(self, sheet):
        self.sheet = sheet
        self.width = len(sheet[0])
        self.height = len(sheet)
        self.skipColList = [0, 7, 8]

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
        parser.add_argument("-n", action="store_true")
        parser.add_argument("--all", action="store_true")
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
        
    def copyRow(self):
        """copy a row, but change its number accordingly"""
        pass


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

    def manageOperations(self):
        """"""
        if self.args.a:  # add
            pass
        elif self.args.d:  # delete
            pass
        elif self.args.c:  # copy
            newRow = self.sheet[int(self.args.c[0])]
            newRow[0] = self.metaNumberPlus()
            self.addRow(newRow)
        if self.args.f:  # filt
            pass
        self.sortDistor()

    def printRow(self, rowNum, padding=2, color="YES"):
        """print one row in distor, according to the color scheme"""
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
        print("\n", end="")

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
            self.printRow(0, color="")
            for i in range(1, self.height):
                self.printRow(i, padding=int(self.args.p))
    
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
### GROUPING
# different coloring for grouped sections
# Divide one section into a series of small sections while being able to
#     represent their relationships
### Initilization generated config
#       and header names to cater to different needs
### Github actions
###  FILTER
### interactive software (like khal)
### BIGGER IDEA:
#       transform this into command line excel?
#
#
#
#
## POSSIBLE FEATURES
# More flexibly add columns, use pandas DataFrame or python lists to manage
#     columns, (allow infinite columnts)
#
# Print that automatically fit the length of string?
#
# modiry entries (I can just modify the json manually)
# database robustness: the mechanism to allow modify the basic sections
#    (maybe add more than the names later, so change them into more
#    flexible sections)
#
# better UI
#
## DONE
# MORE COLORS
#     use sty or the like to manage colors
# x autoclean finished sections
# x delete entries and clear the whole database (with warnings)
# x more flexibility for column names





# techniques used:
# - json, for data process
# - format alignment and colored printing
# - sty, for colors
# - argParse, for cli
