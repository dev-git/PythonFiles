from os import listdir
from shutil import copyfile
import sys
import os

photoDir = "C:/Users/Paul/Pictures/Training/kids_photos/owen/"
outputDir = "C:/Users/Paul/Pictures/Training/kids_photos/training/"
trainingSeed = "3"
for ef in os.listdir(photoDir):
    #print(photoDir + ef)
    fileList = os.path.splitext(os.path.basename(ef))
    newfilename = outputDir + fileList[0].split('.')[0] + "." + trainingSeed + fileList[1]
    print(newfilename)
    #copyfile(photoDir + ef, newfilename)
#C:\Users\Paul\Pictures\Training\kids_photos\murphy
