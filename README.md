
                                                          
                                                            
# futils

A lightweight **CLI file-management utility written in Python**.

`futils` provides a custom command system for navigating and manipulating files and directories directly from the terminal. It also includes a simple module/command declaration system based around `command_decleration.json`.

<img width="800" height=auto alt="futils in Windows Powershell" src="https://github.com/user-attachments/assets/8263b0df-2655-4050-a349-30b660c558d3" />

## Features

- 📁 List files and directories
- 📄 Create files
- 📂 Create directories
- 🚚 Move files and directories
- 🗑️ Remove files and directories
- 🧮 Evaluate mathematical expressions
- ❓ Built-in help system
- 🧩 Command/module declaration system
- 💻 Fully terminal-based

## Commands

| Command | Module | Description |
|---|---|---|
| `help` | `main.help` | Display available commands and help |
| `clear` | `main.clear` | Clear terminal window |
| `ls` | `main.ls` | List children of the current directory |
| `const` | `main.construct` | Create a file |
| `constdir` | `main.constructdir` | Create a directory |
| `mv` | `main.mv` | Move a file or directory from A to B |
| `crunch` | `main.calculate` | Evaluate mathematical expressions using `+`, `-`, `*`, `/` |
| `remv` | `main.rmv` | Remove a file or directory |
| `exit` | `main.exit` | Exit |

## Starting Directory

When `futils` starts, it begins in the user's Windows home directory:

```text
C:\Users\USERNAME
```

For example:

```text
@ 'C:\Users\korisnik' 
: 
```

Commands are executed relative to the current working directory.

## Module System

`futils` uses a command declaration system based around:

```text
command_decleration.json
```

The file contains information used by the program to declare and organize available commands.

Commands are associated with modules such as:

```text
main.help
main.ls
main.construct
main.constructdir
main.mv
main.calculate
main.rmv
```

This allows the command system to be separated from the core application logic.

## Example

A basic session might look like (without colors):

```text


  ▄▄                 ▄▄
 ██         ██   ▀▀  ██
▀██▀ ██ ██ ▀██▀▀ ██  ██ ▄█▀▀▀
 ██  ██ ██  ██   ██  ██ ▀███▄
 ██  ▀██▀█  ██   ██▄ ██ ▄▄▄█▀

futils {version α0.50.0/}




@ 'C:\Users\korisnik'
: crunch 1+1*3
['crunch', '1+1*3']
 Return: eval >> 4


@ 'C:\Users\korisnik'
: help
['help']


<list>
help <main.help> --> Help
ls <main.ls> --> List children
const <main.construct> --> Make a file
constdir <main.constructdir> --> Make a directory
mv <main.mv> --> Move a file from A to B
crunch <main.calculate> --> Eval numbers with operations (+,-,*,/)
remv <main.rmv> --> Remove a file/directory
<list>


@ 'C:\Users\korisnik'
:

```


## Technologies

- **Python**
- **JSON**
- **Windows filesystem**
- **Command-line interface**

## Project Goals

`futils` was built as a learning project to explore:

- CLI application design
- Python modules
- Command parsing
- Filesystem operations
- JSON-based configuration
- Modular application architecture
- Error handling
- Working with Windows paths

## Status

🟢 **Active / Learning Project**

`futils` is primarily a learning project and may receive new commands and architectural improvements over time.
