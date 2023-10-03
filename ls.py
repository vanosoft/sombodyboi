import os, sys

if sys.argv[1:]:
    lst = os.listdir(sys.argv[-1])
else:
    lst = os.listdir(".")

i = 0

print()

while i < len(lst):
    print(lst[i]+"    ", end="")
    i += 1
    if i < len(lst):
        print(lst[i])
    i += 1

print()
