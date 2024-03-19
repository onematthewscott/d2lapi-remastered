Instruction of import functions from existing python files:

1. Git clone your desired entire directory.
2. Make a new python file.
3. Make sure there is ''' __init__.py ''' file to be treated as library in the folder.
4. Make sure add ''' if __name__ == "__main__": ... ''' at end of the functions files.
5. At the top of your new python file you need to use, type ''' from YOURFOLDER import YOURFILE '''(capitals need to be your folder name and file name without .py).
6. Call your functions!
