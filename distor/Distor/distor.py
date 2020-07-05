#! /usr/bin/env python3


#
#        "number": number,
#        "name": name,
#        "project": project,
#        "timeEstimation": timeEstimation,
#        "wtype": wtype,
#        "DDL": DDL,
#        "remarks": remarks,
#        "timeUsed": "",
#        "afterThoughts": ""
#
#


import os
import json
import argparse
from datetime import datetime, date
from sty import fg
from .sheet import Sheet

HOME = "/home/ahacad/.distor/Dev/"
storedPath = HOME + "stored.json"
deprecatedPath = HOME + "deprecated.json"
extendedPath = HOME + "extended.json"
metaPath = HOME + "meta.json"  # store color schemes
widthType = {"number": "medium",
             "name": "long",
             "project": "norm",
             "timeEstimation": "short",
             "wtype": "short",
             "DDL": "norm",
             "remarks": "long",
             "timeUsed": "short",
             "afterThoughts": "long"
             }
widthLength = {"short": 4,
               "medium": 6,
               "norm": 19,
               "long": 30}
colorTypes = {"number": "white",
              "name": "green",
              "project": "blue",
              "timeEstimation": "yellow",
              "wtype": "cyan",
              "DDL": "red",
              "remarks": "magenta",
              "timeUsed": "white",
              "afterThoughts": "white"
              }
colorsDic = {"red": fg.red,
             "green": fg.green,
             "yellow": fg.yellow,
             "blue": fg.blue,
             "magenta": fg.magenta,
             "cyan": fg.cyan,
             "white": fg.white}


class colors:
    BLACK = "\033[0;30m"        # Black
    RED = "\033[0;31m"          # Red
    GREEN = "\033[0;32m"        # Green
    YELLOW = "\033[0;33m"       # Yellow
    BLUE = "\033[0;34m"         # Blue
    PURPLE = "\033[0;35m"       # Purple
    CYAN = "\033[0;36m"         # Cyan
    WHITE = "\033[0;37m"        # White
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m""]"




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
        self.args = parser.parse_args()

    def loadColorScheme(self):
        """load color scheme, if not exist, creat one"""
        if not os.path.exists(metaPath):
            defaultColorScheme = ["white", "green", "blue", "yellow",
                                  "cyan", "red", "magenta", "white", "white"]
            with open(metaPath, "w") as json_file:
                json.dump(defaultColorScheme, json_file, indent=4)
        with open(metaPath) as json_file:
            self.colorScheme = json.load(json_file)

    def changeColorScheme(self):
        """change the color scheme"""
        pass

    def printColorScheme(self):
        """print the color scheme along with header"""
        if self.args.colorScheme:
            pass   # TODO  print color scheme
    
    def manageColors(self):
        """manage color related things"""
        self.loadColorScheme()
        self.printColorScheme()
        
    def copyRow(self):
        """copy a row, but change its number accordingly"""
        pass

    def manageOperations(self):
        """"""
        pass

    def managePrints(self):
        """"""
        pass
    
    



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
