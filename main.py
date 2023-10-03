import os, sys
from colorama import init


init()
os.system("cls")

def cd(path):
    global folder
    path = os.path.abspath(wp(var(path)))
    os.chdir(path)
    folder = path

def echo(*string):
    string = var(" ".join(string))
    if ">" in string:
        file = string.split(">\"", 1)[1].split("\"", 1)[0]
        file = open(file, "wt")
        string = string.replace(">\""+file.name+"\"", "")
    else:
        file = sys.stdout
    if string[0] == string[-1] == '"':
        print(eval(string).strip(), file=file, end=('' if file != sys.stdout else '\n'))
    else:
        print(string.strip(), file=file, end=('' if file != sys.stdout else '\n'))
    return 0

def evals(*string):
    string = var(" ".join(string))
    if ">" in string:
        file = string.split(">\"", 1)[1].split("\"", 1)[0]
        file = open(file, "wt")
        string = string.replace(">\""+file.name+"\"", "")
    else:
        file = sys.stdout
    if string[0] == string[-1] == '"':
        print(eval(eval(string)), file=file, end=('' if file != sys.stdout else '\n'))
    else:
        print(eval(string), file=file, end=('' if file != sys.stdout else '\n'))
    return 0

vars = {
    "ps": "",
    "user": os.getlogin(),
    "device": "ICL-PC",
}

aliases = {
    "ls": '"'+os.path.abspath(".")+"/ls.py\"",
    "python3": "py",
    "clear": "cls"
}

sysaliases = {
    "cd": cd,
    "echo": echo,
    "eval": evals
}

folder = os.path.abspath(".")

def cmd(line: str) -> int:
    if line.startswith("exit"):
        global run
        run = 0
    if line.startswith("set "):
        vars[line.split(" ", 1)[1].split("=")[0].strip()] = eval(line.split(" ", 1)[1].split("=")[1])
        return 0
    else:
        cl = line.split(" ")
        if cl[0] in sysaliases:
            return sysaliases[cl[0]](*cl[1:])
        return os.system(" ".join((ua(cl[0]), *cl[1:])))

def exe(script: str) -> int:
    for i in script.splitlines():
        if status:=cmd(i):
            return status
    return 0

def ask() -> int:
    cmd(input(ps(vars["ps"])))

def ps(line: str) -> str:
    return line.replace("\\u", vars["user"]).replace("\\d", vars["device"]).replace("\\w", up(folder))

def up(path: str) -> str:
    return path.replace("\\", "/").replace("C:", "").replace("/Users/"+vars["user"], "~")

def wp(path: str) -> str:
    return path.replace("/", "\\").replace("\\", "C:\\", 1).replace("~", "/Users/"+vars["user"])

def ua(cmd: str) -> str:
    if cmd in aliases.keys():
        return aliases[cmd]
    return cmd

def var(string: str, x = 0) -> str:
    cls = list(string.split("${(")[1:])
    vrs = []
    for n, i in enumerate(cls):
        cls[n] = i.split(")}", 1)[0]
        if string.find("${(%s)}" % cls[n]) < 0:
            del cls[n]
    for i in cls:
        cmd(i+" >\"._stdout\"")
        with open("._stdout", "rt") as f:
            vrs += [f.read()]
    # print(cls, vrs)
    for n, i in enumerate(cls):
        string = string.replace("${("+i+")}", vrs[n])
    for k in list(vars.keys()):
        # print(k, "${"+k+"}", vars[k])
        string = string.replace("${"+k+"}", vars[k])
    string = string.replace("\{", "{")
    string = string.replace("\}", "}")
    print(" "*(3-x)*4, "\b"+string, cls, vrs)
    return string.split(")}", 1)[0] if x > 3 else var(string.split(")}", 1)[0], x + 1)

with open("bashrc.sh", "rt") as f:
    exe(f.read())

run = 1

while run:
    ask()
