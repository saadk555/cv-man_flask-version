import os 
from glob import glob
from zipfile import ZipFile

re = r'D:\xamppnew\htdocs\cv-man\result\\'
with ZipFile(r"D:\xamppnew\htdocs\cv-man\result\result.zip", 'w') as zip:
    for file in glob(os.path.join(re, '*.pdf')):
        zip.write(file, os.path.basename(file))