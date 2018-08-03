from random import randint
from os import listdir
import cv2
import sys
import os
      
CASCADE="Face_cascade.xml"
FACE_CASCADE=cv2.CascadeClassifier(CASCADE)

def detect_faces(image_path):

	print('Detecting faces in file ' + image_path)
	image=cv2.imread(image_path)	
	image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.04,minNeighbors=5,minSize=(125,125),flags=0)

	for x,y,w,h in faces:
	    sub_img=image[y-10:y+h+10,x-10:x+w+10]
	    os.chdir("Extracted")
	    cv2.imwrite(os.path.splitext(os.path.basename(image_path))[0] + "_" + str(randint(0,10000))+".jpg", sub_img)
	    os.chdir("../")
	    cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)

	cv2.imshow("Faces Found",image)
	if (cv2.waitKey(0) & 0xFF == ord('q')) or (cv2.waitKey(0) & 0xFF == ord('Q')):
		cv2.destroyAllWindows()

def test_loop(image_path):

	print(os.path.splitext(os.path.basename(image_path))[0])

if __name__ == "__main__":
	
	if not "Extracted" in os.listdir("."):
		os.mkdir("Extracted")
    
	if len(sys.argv) < 2:
		print( "Usage: python Detect_face.py 'image path'")
		sys.exit()

	#fileList = os.listdir('data')
	detect_faces(sys.argv[1])
	#for eachFile in os.listdir('data'):
		#detect_faces(sys.argv[1])
		#detect_faces('data\\' + eachFile)
		#test_loop('data\\' + eachFile)