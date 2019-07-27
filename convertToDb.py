import subprocess
from os import path, remove
# from subprocess import PIPE, STDOUT
import sqlite3


def generatePVDB(rectLen, ellipseDia):
    sqlFileName = './templates/test without flange INCH UNITS.sql'
    tempFileName = './output/temp.sql'
    newPvdbFileName = './output/test.pvdb'
    if path.exists(tempFileName):
        remove(tempFileName)
    if(path.exists(newPvdbFileName)):
        remove(newPvdbFileName)
    with open(sqlFileName) as f:
        data = f.read()
        newData = data.replace('LR', str(rectLen))
        newData = newData.replace('DE', str(ellipseDia))
    with open(tempFileName, "w+") as nf:
        nf.write(newData)
    pvdbFile = open(newPvdbFileName, "w+")
    pvdbFile.close()
    cursor = sqlite3.connect(newPvdbFileName)
    with open(tempFileName) as nf:
        newSqls = nf.readlines()
        for newSql in newSqls:
            cursor.execute(newSql)
        cursor.close()
    # sqlite3Proc = subprocess.Popen([".\\tools\\sqlite3.exe"],
    #                                stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True, universal_newlines=True)
    # sqlite3Proc.wait()
    # sqlite3Proc.stdin.write('.read ' + tempFileName)
    # sqlite3Proc.stdin.write('.save ' + newPvdbFileName)
    # sqlite3Proc.stdin.write('.exit')
    # sqlite3Proc.kill()
    remove(tempFileName)
    return

    # region oldcode

    # import re
    # ELEMENTDATA = 'INSERT INTO ElementData VALUES('
    # decimalIntPattern = r'\d*\.\d+|\d+|\d*\.'

    # data=f.readlines()
    # for line in data:
    #     insertStatIndex = line.find(ELEMENTDATA)
    #     isRectangle = False
    #     if insertStatIndex > -1:
    #         for (index, match) in enumerate(re.finditer("(?<=\s)"+decimalIntPattern+"(?=\s)", line)):
    #             if index == 1 and line[match.start(0):match.end(0)].strip() == '1':
    #                 isRectangle = True
    #             elif isRectangle:
    #                 if index == 2:
    #                     re.sub(decimalIntPattern, rectLen,
    #                            line[match.start(0):match.end(0)])
    #                 else:
    #                     re.sub(decimalIntPattern, ellipseDia+'.',
    #                            line[match.start(0):match.end(0)])
    # endregion
