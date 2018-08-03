from os import listdir
from shutil import copyfile
import sys
import os
      
fileList = []


def test_loop(image_path):

    fileName = os.path.splitext(os.path.basename(image_path))[0]
    #print(fileName)
    if fileName in fileList:
        print(fileName)
        copyfile('data_geis_1\\' + fileName + '.jpg', 'Output\\' + fileName + '.jpg')
    #print(len(fileList))        

if __name__ == "__main__":
	
	if not "Output" in os.listdir("."):
		os.mkdir("Output")
    
	if len(sys.argv) < 2:
		print( "Usage: python Detect_face.py 'image path'")
		sys.exit()

for ef in os.listdir('data_geis_1\\'):
        fileList.append(os.path.splitext(os.path.basename(ef))[0])

#for ef in os.listdir('data_geis_2\\'):
#       fileList.append(os.path.splitext(os.path.basename(ef))[0])

        #print(os.path.splitext(os.path.basename(ef))[0])

#print(len(fileList))

#test_loop('filename.txt')

dirStr = '..\\Tensorflow\\tensorflow-1.8.0\\tensorflow\\examples\\image_retraining\\tf_files\\kids_photos\\niamh\\'

    #fileList = os.listdir('data')
for eachFile in os.listdir(dirStr):
    #print(eachFile.split('.'))
    test_loop(dirStr + eachFile.split('.')[0])
		#detect_faces(sys.argv[1])
		#detect_faces('data\\' + eachFile)
