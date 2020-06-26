# /usr/bin/env python3

import os
import json

sections = {}
sections["sections"] = []
storedPath = "/home/ahacad/.distor/stored.json"


class colors:
    RED   = "\033[1;31m"  
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m""]"


def loadSection():
    """load sections from the stored json file
    """
    with open(storedPath) as json_file:
        sections = json.load(json_file)
    return sections


def writeEntry():
    """store entries to the path
    """
    with open(storedPath, "w") as outfile:
        json.dump(sections, outfile)


def addEntry(name, project, timeEstimation, DDL, remarks):
    """add an entry to the existing pool
    """
    sections["sections"].append({
        "Name": name,
        "Project": project,
        "Time Estimation": timeEstimation,
        "DDL": DDL,
        "Remarks": remarks
        })
    return 0


def deprecateEntry():
    """remove the entry from the existing pool and add to the deprecated pool

    """
    pass


def printEntry():
    """print the entries in the existing pool, you can choose the way to display
    """
    width = 20
    for section in sections["sections"]:
        name = section["Name"]
        project = section["Project"]
        timeEstimation = section["Time Estimation"]
        DDL = section["DDL"]
        remarks = section["Remarks"]
        print(f"{name:^{width}}|" +
              f"{project:^{width}}|" +
              f"{timeEstimation:^{width}}|" +
              f"{DDL:^{width}}|" +
              f"{remarks:^{width}}")
    return 0


def estimateTime():
    # how the time remained is calculated?
    """estimate whether you can make it before ddl
    """
    pass


def cli():
    """the command line interface

    """
    pass


def main():
    global sections
    # sections = loadSection()
    # addEntry(name, project, timeEstimation, DDL, remarks)
    sections = {"sections": [{"Name": "testname1", "Project": "Mathe", "Time Estimation": "2", "DDL": "2020-06-12", "Remarks": "test"}]}
    printEntry()
    writeEntry()
    pass


if __name__ == "__main__":
    main()



# techniques used:
# - json
# - format alignment and colored printing
