import os
import shutil
import zipfile

dirPath = "D:\\CrashReport\\receiveFiles"
txtFiles = os.listdir(dirPath)
for txtFile in txtFiles :
    txtFile = os.path.join(dirPath, txtFile)
    dmpFile = os.path.splitext(txtFile)[0] + ".dmp"
    shutil.copy("D:/CrashReport/standard.dmp", dmpFile)
    zipFilePath = os.path.splitext(txtFile)[0] + ".zip"
    zFile = zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED)
    zFile.write(txtFile, os.path.basename(txtFile))
    zFile.write(dmpFile, os.path.basename(dmpFile))
    zFile.close()
    os.remove(txtFile)
    os.remove(dmpFile)