from time import sleep
from rich import print
from rich.progress import Progress
from rich.prompt import Prompt, Confirm
import os
import json
from pathlib import Path
from datetime import datetime
import itertools
from shlex import split
import inspect as ins


class validCommands:
    def __init__(self, operation, arguments):
        self.operation = operation
        self.args = arguments
        self.hasEnded = False
        if operation == "print":
            print(split(arguments))
        self.hasEnded = True


def checkIfDirectory(dirPointer, dirName: str = None):
    if dirName is None:
        print(
            "[italic dark_red] Internal Error: futilsLang.checkIfDirectory --> dirName <ARG 0> IS NONE"
        )
        return False

    if checkIfExists(dirPointer / dirName):
        return True
    else:
        return False


def checkIfExists(inputDir):
    if not isinstance(inputDir, Path):
        return False

    if inputDir.exists():
        return True
    else:
        return False


def readFile(filePath):
    return open(filePath, "r")


def runFile(filePath, dirPointer):
    if (
        not checkIfDirectory(dirPointer, filePath)
        # (dirPointer / filePath).is_file()
    ):
        print(f"[italic blue] Return: error :>> not a valid file")
        return True

    try:
        file = readFile(dirPointer / filePath).readlines()
    except Exception as e:
        print(e)
        print(f"[italic blue] Return: error :>> failed to read file")
        return True

    toSend = []
    isString = False
    saver = ""
    for text in file[1]:
        if text == "\n":
            continue
        elif text == "(" and isString == False:
            print("set//", toSend)
            toSend.append(saver)
            saver = ""
            continue
        elif text == ")" and isString == False:
            print("reset//", toSend)
            toSend.append(saver)
            saver = ""
            continue
        elif text == ('"' or "'"):
            isString = not isString

        saver += text
    print(toSend[1:])
    commandTest = validCommands("print", toSend[1:])
    while not commandTest.hasEnded:
        pass

    return True
