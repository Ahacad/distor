#! /usr/bin/env python3

import click 
import os
import json
from sty import fg, ef, rs
from datetime import datetime, date


class Sheet:

    def __init__(self, sheet):
        self.sheet = sheet
        self.width = len(sheet[0])
        self.height = len(sheet)

    def modifyCell(self, rowNum, colNum, cell):
        """modify a particular cell by sending position and the new value"""
        self.sheet[rowNum][colNum] = cell

    def deleteCell(self, rowNum, colNum):
        """modify a single cell, changing it into empty string"""
        self.sheet[rowNum][colNum] = ""

    def addRow(self, row):
        """add a row, length must be the same to the header row"""
        if len(row) == self.width:
            self.sheet.append(row)
            self.height += 1
        else:
            raise ValueError("The number of elements in the row is incorrect!")

    def deleteRow(self, rowNum):
        """delete a row by its number"""
        if 0 < rowNum < self.sheet.height:
            return self.sheet.pop(rowNum)
        else:
            raise ValueError("Row number out of boundry!")

    def modifyRow(self, rowNum, row):
        """modify a whole row by sending position and all the new values
           specially, when rowNum is 0 you are modifying the header
        """
        if len(row) == self.width:
            self.sheet[rowNum] = row
        else:
            raise ValueError("The number of elements in the row is incorrect!")

    def exchangeRow(self, rowNum1, rowNum2):
        """exchange two rows"""
        if rowNum1 == 0 or rowNum2 == 0:
            raise ValueError("Cannot exchange row with header!")
        self.sheet[rowNum1], self.sheet[rowNum2] = self.sheet[rowNum2], self.sheet[rowNum1]

    def exchangeColumn(self, colNum1, colNum2):
        """exchange two columns"""
        if 0 <= colNum1 < self.width and 0 <= colNum2 < self.width:
            for i in range(self.height):
                self.sheet[i][colNum1], self.sheet[i][colNum2] = self.sheet[i][colNum2], self.sheet[i][colNum1]

    def sortFunc(self, colNum):
        """sort the rows according to the specific column"""
        self.sheet[1:] = sorted(self.sheet[1:], key=lambda x: x[colNum])

    def filt(self, colNum, dest, rule="EQUALTO"):
        """filter the array as according to the rule"""
        if rule == "EQUALTO":
            res = []
            for i in range(1, self.height):
                if self.sheet[i][colNum] == dest:
                    res.append(self.sheet[i])
        elif rule == "GREATERTHAN":
            for i in range(1, self.height):
                if self.sheet[i][colNum] > dest:
                    res.append(self.sheet[i])
        elif rule == "SMALLERTHAN":
            for i in range(1, self.height):
                if self.sheet[i][colNum] < dest:
                    res.append(self.sheet[i])
        return res

    def printSheetWithNumber(self):
        """print the whole sheet with navigating numbers"""
        colWidth = [0 for i in range(self.width)]
        for i in range(self.height):
            for j in range(self.width):
                colWidth[j] = max(colWidth[j], len(self.sheet[i][j]))
        print("    ", end="")  # print the header
        for i in range(self.width):
            print(ef.underl + f"{i:^{colWidth[i] + 1}}"
                  + rs.underl, end="")  # print the header
        print("\n", end="")
        for i in range(self.height):   # print each row
            print(f"{i: >3}" + "|", end="")
            for j in range(self.width):
                print(f"{self.sheet[i][j]:^{colWidth[j] + 1}}", end="")
            print("\n", end="")



    def printSheet(self):
        """print the sheet"""
        for i in range(self.height):
            for j in range(self.width):
                print(self.sheet[i][j], " ", end="")
            print()

    def saveSheet(self, storedPath):
        """store entries to the path
        """
        with open(storedPath, "w") as outfile:
            json.dump(self.sheet, outfile, indent=4)
        #with open(deprecatedPath, "w") as outfile:
        #    json.dump(deprecatedRows, outfile, indent=4)
        #with open(extendedPath, "w") as outfile:
        #    json.dump(extendedRows, outfile, indent=4)

#test = Sheet([["Num", "Ar", "arts"], ["2", "3", "4"], ["1", "2", "3"], ["9", "3", "7"]])
#test.sortFunc(1)
#test.printSheetWithNumber()
#res = test.filt(1, 3)
#print(res)
#test.printSheet()
