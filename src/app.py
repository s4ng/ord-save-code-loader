from tkinter import *
import os
import ctypes.wintypes
import chardet

CSIDL_PERSONAL = 5
SHGFP_TYPE_CURRENT = 0

buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

ordPath = buf.value + '\\Warcraft III\\CustomMapData\\ORD10'
userIdPath = buf.value + '\\OrdSaveCodeLoader\\userId.txt'

root = Tk()

root.title("원랜디 세이브 코드 로더")
root.resizable(False, False)

userIdLabel = Label(root, text="원랜디 ID")
userIdLabel.grid(row = 0, column = 0)


idText = Entry(root)
idText.grid(row = 0, column = 1)

def setSaveCodeEvent(event=None):
    setSaveCode(idText.get())

idText.bind('<Return>', setSaveCodeEvent)

searchBtn = Button(root, text="로드", padx = 2, pady = 2, command=lambda:setSaveCode(idText.get()))
searchBtn.grid(row = 0, column = 2)

saveCodeLableText = StringVar()
saveCodeLableText.set("세이브 코드")

saveCodeLabel = Label(root, textvariable = saveCodeLableText)
saveCodeLabel.grid(row = 1, column = 0)

saveCodeText = Entry(root)
saveCodeText.grid(row = 1, column = 1)

clipboardBtn= Button(root, text="copy", padx = 2, pady = 2, command=lambda:setClipboardSaveCode(saveCodeText.get()))
clipboardBtn.grid(row = 1, column = 2, padx = 2, pady = 2)

def setSaveCodeText(saveCode):
    saveCodeText.delete(0, "end")
    saveCodeText.insert(0, saveCode)

def setSaveCode(userId):
    if os.path.isdir(ordPath) is not True:
        setSaveCodeText("원랜디 폴더가 존재하지 않습니다")
        return
    fileNames = os.listdir(ordPath)
    userFiles = {}
    for fileName in fileNames:
        splitedFileName = fileName[:-4].split('_')
        userIdInFileName = splitedFileName[1]
        if len(splitedFileName) > 3:
            userIdInFileName = '_'.join(splitedFileName[1:-1])
        if userId == userIdInFileName:
            userFiles[int(splitedFileName[-1])] = fileName
    if not userFiles:
        setSaveCodeText("ID 검색 실패")
        return
    
    f = open(userIdPath, 'w', encoding="UTF8")
    f.write(userId)

    sortedUserFiles = sorted(userFiles.items())
    lastSaveFile = sortedUserFiles[-1][1]

    rawF = open(ordPath+'\\'+lastSaveFile, 'rb').read()
    res = chardet.detect(rawF)
    f = open(ordPath+'\\'+lastSaveFile, 'r', encoding=res['encoding'], errors='ignore')

    lines = f.readlines()
    f.close()
    for line in lines:
        if "-load" in line:
            saveCodeLine = line
            break
    saveCodeResult = ''
    isNowSaveCode = False
    for char in saveCodeLine:
        if char == '\"':
            if not isNowSaveCode:
                isNowSaveCode = True
                continue
            else:
                break
        if isNowSaveCode:
            saveCodeResult = saveCodeResult + char
    saveCodeLableText.set(str(sortedUserFiles[-1][0]) + ' 클리어')
    setSaveCodeText(saveCodeResult)
    return

def setClipboardSaveCode(saveCode):
    root.clipboard_clear()
    root.clipboard_append(saveCode)

if os.path.isfile(userIdPath):
    f = open(userIdPath, 'r', encoding="UTF8")
    idText.delete(0,"end")
    idText.insert(0, f.readline())
    setSaveCode(idText.get())

root.mainloop()
