import subprocess as sb
import time
from time import sleep
from rich import print
from rich.progress import Progress
from rich.prompt import Prompt, Confirm
import os
import json
from pathlib import Path
import importlib as imlib
import itertools
import shutil
from shlex import split
import inspect as ins

mainPath = Path(__file__).resolve().parent
settings = None
commandDeclaration = None

dirPointer = Path.home()

spinner = itertools.cycle(["|", "/", "-", "\\"])

running = True


def load():
    sb.run("cls" if os.name == "nt" else "clear", shell=True)
    title()
    global settings
    global commandDeclaration
    tstart = time.time()
    with Progress() as progress:
        loadingbar = progress.add_task("")
        loadingbar2 = progress.add_task("")
        while not progress.finished:
            text = f"Loading settings.json {next(spinner)}"
            progress.update(loadingbar, description=f"[green]{text}\b")

            file = open(mainPath / "json/settings.json", "r")
            wrapped_file = progress.wrap_file(file, task_id=loadingbar)
            settings = json.load(wrapped_file)

            text2 = f"Loading commandDeclaration.json {next(spinner)}"
            progress.update(loadingbar2, description=f"[green]{text2}\b")

            file2 = open(mainPath / "json/commandDeclaration.json", "r")
            wrapped_file2 = progress.wrap_file(file2, task_id=loadingbar2)
            commandDeclaration = json.load(wrapped_file2)
    print(f"[italic gray66]took -> {time.time() - tstart:0.2f}s")
    sleep(1)
    sb.run("cls" if os.name == "nt" else "clear", shell=True)
    title()


def title():
    print("""[bold green]

  ▄▄                 ▄▄
 ██         ██   ▀▀  ██
▀██▀ ██ ██ ▀██▀▀ ██  ██ ▄█▀▀▀
 ██  ██ ██  ██   ██  ██ ▀███▄
 ██  ▀██▀█  ██   ██▄ ██ ▄▄▄█▀

[italic red]futils {version α0.50.0/}\n\n""")


def checkIfDirectory(dirName: str = None):
    if dirName is None:
        print(
            "[italic dark_red] Internal Error: checkIfDirectory --> dirName <ARG 0> IS NONE"
        )
        return None

    if checkIfExists(dirPointer / dirName):
        return True
    elif checkIfExists(dirName):
        return True
    elif dirName == "..":
        return True
    elif dirName == "/r":
        return True
    else:
        return False


def checkIfCommand(command):
    try:
        a = commandDeclaration[command]
    except:
        # print(f"[red] Error: command <{command}> does not exists or isnt declared")
        return False

    if a is None:
        return False

    try:
        if a["module"] == "main":
            a = getattr(
                imlib.import_module(__name__),
                commandDeclaration[command]["functionName"],
            )
        else:
            a = getattr(
                imlib.import_module(f"modules.{commandDeclaration[command]['module']}"),
                commandDeclaration[command]["functionName"],
            )
    except:
        # print(f"[red] Error: command <{command}> is declared but not found")
        return False

    if a is None:
        return False

    return True


def help(moduleFilter=None):
    print("\n")
    print("[yellow]<list>")
    if moduleFilter is None:
        for commandName, vals in commandDeclaration.items():
            print(
                f"{commandName} <[green]{vals['module']}[/green].{vals['functionName']}> --> [italic blue]{vals.get('desc') or '~~None~~'}"
            )
    else:
        for commandName, vals in commandDeclaration.items():
            if moduleFilter == vals["module"]:
                print(
                    f"{commandName} <[green]{vals['module']}[/green].{vals['functionName']}> --> [italic blue]{vals.get('desc') or '~~None~~'}"
                )
    print("[yellow]<list>")
    return True


def calculate(components):
    print(f"[italic blue] Return: eval >> {eval(components)}")
    return True


def checkIfExists(inputDir):
    if not isinstance(inputDir, Path):
        return False

    if inputDir.exists():
        return True
    else:
        return False


def makeFolder(name: str = None, dirAddition: str = None):
    if name is None:
        print("[italic dark_red] Internal Error: makeFolder --> name <ARG 0> IS NONE")
        return

    if dirAddition == "." or dirAddition is None:
        if not checkIfExists((dirPointer / name)):
            (dirPointer / name).mkdir()
        else:
            print(
                f"[italic dark_red] Internal Error: makeFolder --> Already exists <{(dirPointer / name)}>"
            )
            return
    else:
        if not checkIfExists((dirPointer / dirAddition / name)):
            (dirPointer / dirAddition / name).mkdir()
        else:
            print(
                f"[italic dark_red] Internal Error: makeFolder --> Already exists <{(dirPointer / dirAddition / name)}>"
            )
            return
    return True


def makeFile(name: str = None, type: str = "", dirAddition: str = None):
    if name is None:
        print("[italic dark_red] Internal Error: makeFile --> name <ARG 0> IS NONE")
        return
    if dirAddition == "." or dirAddition is None:
        if not checkIfExists(dirPointer / str(name + type)):
            (dirPointer / str(name + type)).touch()
        else:
            print(
                f"[italic dark_red] Internal Error: makeFile --> Already exists <{(dirPointer / str(name + type))}>"
            )
            return
    else:
        if not checkIfExists(dirPointer / dirAddition / str(name + type)):
            (dirPointer / dirAddition / str(name + type)).touch()
        else:
            print(
                f"[italic dark_red] Internal Error: makeFile --> Already exists <{(dirPointer / dirAddition / str(name + type))}>"
            )
            return
    print(f"[italic blue] Return: created {name, type}")
    return True


def changePointer(point):
    global dirPointer
    if point == "..":
        if dirPointer == Path.home():
            return True
        dirPointer = dirPointer.parent
    elif point == "/r":
        dirPointer = Path.home()
    elif Path(point).exists() and Path(point).is_dir():
        dirPointer = Path(point)
    elif (dirPointer / point).exists() and (dirPointer / point).is_dir():
        dirPointer = dirPointer / point
    else:
        print(
            f"[italic dark_red] Internal Error: changePointer --> Does not exists <{point}>"
        )
        return False
    return True


def run():
    load()
    running = True
    while running:
        running = interp(
            Prompt.ask(f"\n\n[green]@ [magenta]'{dirPointer}' [bright_white]\n")
        )


def interp(command: str):
    commandSplit = split(command)

    commandKeyword = commandSplit[0]
    commandArgs = commandSplit[1:]
    print(commandSplit)

    if commandKeyword == "exit":
        sb.run("cls" if os.name == "nt" else "clear", shell=True)
        return False
    elif commandKeyword == "clear":
        sb.run("cls" if os.name == "nt" else "clear", shell=True)
        title()
        return True

    if not checkIfCommand(commandKeyword) and checkIfDirectory(command):
        changePointer(command)
        return True

    if not checkIfCommand(commandKeyword) and not checkIfDirectory(command):
        print(f"[red] Error: command/Path <{command}> does not exist")
        return True

    try:
        if commandDeclaration[commandKeyword]["module"] == "main":
            funk = getattr(
                imlib.import_module(__name__),
                commandDeclaration[commandKeyword]["functionName"],
            )
        else:
            funk = getattr(
                imlib.import_module(
                    f"modules.{commandDeclaration[commandKeyword]['module']}"
                ),
                commandDeclaration[commandKeyword]["functionName"],
            )
    except Exception as e:
        print("255:::::")
        print(e)
        return True

    if funk:
        if len(commandDeclaration[commandKeyword]["args"]) <= len(commandArgs):
            try:
                if "dirPointer" in (ins.signature(funk)).parameters:
                    return funk(*commandArgs, dirPointer=dirPointer)
                else:
                    return funk(*commandArgs)
            except Exception as e:
                print(e)
                pass
        else:
            try:
                if "dirPointer" in (ins.signature(funk)).parameters:
                    return funk(dirPointer=dirPointer)
                else:
                    return funk()
            except:
                print(
                    f"[red] Error: command <{commandKeyword}> has <{len(commandDeclaration[commandKeyword]['args'])}> including optional"
                )
    else:
        print(f"[red] Error: command <{commandKeyword}> doesnt want to work rn")
    return True


def ls(extensionFilter=None):
    print("\n")
    print(f"[yellow]<list>")
    if not extensionFilter is None:
        for child in dirPointer.iterdir():
            if child.suffix == extensionFilter:
                print(f"{child.name}", end="")
                if child.name.startswith("."):
                    print("  [italic gray66](hidden)")
                else:
                    print()
    else:
        for child in dirPointer.iterdir():
            if child.is_dir():
                print(f"[italic blue]{child.name}", end="")
                if child.name.startswith("."):
                    print("  [italic gray66](hidden)")
                else:
                    print()
            else:
                print(f"{child.name}", end="")
                if child.name.startswith("."):
                    print("  [italic gray66](hidden)")
                else:
                    print()

    print("[yellow]<list>")
    return True


def construct(name, type="", addition=None):
    makeFile(name, type, addition)
    return True


def constructdir(name, addition=None):
    makeFolder(name, addition)
    return True


def mv(file, destination):
    toPlace = None
    if destination == ".":
        toPlace = dirPointer
    elif destination == ".." and not dirPointer == Path.home():
        toPlace = dirPointer.parent
    elif destination == "/r":
        toPlace = Path.home()
    elif Path(destination).exists() and Path(destination).is_dir():
        toPlace = Path(destination)
    elif (dirPointer / destination).exists() and (dirPointer / destination).is_dir():
        toPlace = dirPointer / destination
    else:
        print(
            f"[italic dark_red] Error: destination does not exist <{dirPointer / destination}>"
        )
        return True

    toParent = False
    toFile = None
    if file == ".":
        toFile = dirPointer
        toParent = True
    elif Path(file).exists():
        toFile = Path(file)
    elif (dirPointer / file).exists():
        toFile = dirPointer / file
    else:
        print(f"[italic dark_red] Error: file does not exist <{dirPointer / file}>")
        return True

    if toPlace == toFile:
        return True
    if toParent:
        if not changePointer(".."):
            return True

    if Confirm.ask(
        f"[light_blue] Are you sure you want to move {toFile} >> {toPlace}? >>>"
    ):
        if (
            Prompt.ask(
                f"[dark_olive_green2]~~~>| admin password [italic](hidden)[/italic]   ",
                password=True,
            )
            == settings["adminPassword"]
        ):
            shutil.move(toFile, toPlace)
            print(f"[italic blue] Return: moved {toFile} >> {toPlace}")
            return True
        else:
            print(f"[italic blue] Return: password entered not correct")
            return True
    else:
        print(f"[italic blue] Return: exited")
        return True


def rmv(file):
    toFile = None
    changeParent = None
    if file == ".":
        toFile = dirPointer
        changeParent = True
    elif Path(file).exists():
        toFile = Path(file)
        if toFile == dirPointer:
            changeParent = True
    elif (dirPointer / file).exists():
        toFile = dirPointer / file
        if toFile == dirPointer:
            changeParent = True
    else:
        print(f"[italic dark_red] Error: file/dir does not exist <{dirPointer / file}>")
        return True

    if changeParent:
        if not changePointer(".."):
            return True

    if toFile in [Path(x) for x in settings["deleteProcetion"]]:
        print(
            f"[italic blue] Return: selected path is in protection; to remove this, edit the settings.json file"
        )
        return True

    if Confirm.ask(
        f"[bright_red] Are you sure you want to PERMANENTLY DELETE {toFile} >>>"
    ):
        if (
            Prompt.ask(
                f"[dark_olive_green2]~~~>| admin password [italic](hidden)[/italic]   ",
                password=True,
            )
            == settings["adminPassword"]
        ):
            print()

            if Confirm.ask(
                f"[bright_red]   ARE YOU SURE THAT YOU WANT TO DELETE {toFile} FROM THIS SYSTEM, ACTION CAN NOT BE UNDONE\n>>>"
            ):
                if toFile.is_file():
                    toFile.unlink()
                elif toFile.is_dir():
                    try:
                        toFile.rmdir()
                    except:
                        shutil.rmtree(toFile)

                print(f"[italic blue] Return: deleted {toFile}")
            else:
                print(f"[italic blue] Return: exited")
        else:
            print(f"[italic blue] Return: password entered not correct")
    else:
        print(f"[italic blue] Return: exited")

    return True


if __name__ == "__main__":
    run()
