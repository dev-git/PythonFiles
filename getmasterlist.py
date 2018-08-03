import os
from shutil import copyfile

trainingdata = "E:/Data/repo/mydev/Tensorflow/tensorflow-1.8.0/tensorflow/examples/image_retraining/tf_files/kids_photos/niamh/"
sourceData = "E:/Data/repo/mydev/Cognitive-Face-Python/Extracted/"
geisData = "E:/Data/repo/mydev/Face-Detect/data_geis_1/temp/"

geisList = os.listdir(geisData)

for ef in os.listdir(trainingdata):
    filename = os.path.splitext(os.path.basename(ef))[0].split('.')[0]
    #print(filename)
    for gef in geisList:
        if gef.find(filename) != -1:
            print(gef)
            copyfile(geisData + gef, './Master/' + gef)
            break
