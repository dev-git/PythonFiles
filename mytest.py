from random import randint

import time
import os
import uuid
import cv2
import cognitive_face as CF
import util
import model

#import glob

KEY = ''  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://australiaeast.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
#result = CF.face.detect(img_url)
imgDir = "../Face-Detect/data_geis_2/"
fileList = []

trainingdata = "E:/Data/repo/mydev/Tensorflow/tensorflow-1.8.0/tensorflow/examples/image_retraining/tf_files/kids_photos/niamh/"
large_face_list_id = str(uuid.uuid1())
face_paths = []
detected_face_paths = []
faces = {}
persisted_faces = {}

def detect_face(img_path):
    print(img_path)
    if (img_path == "temp"):
        return

    tempFilePath = imgDir + '/temp/' + img_path
    if os.path.exists(tempFilePath):
        return

    #print(os.path.getsize(imgDir + img_path))
    imgSize = os.path.getsize(imgDir + img_path) 
    if imgSize > 4000000:
        # we need to resize
        im = cv2.imread(imgDir + img_path)
        old_size = im.shape[:2] 
        print(old_size)
        ratio = float(3000000 / imgSize )
        #print(ratio)
        new_size = tuple([int(x*ratio) for x in old_size])
        #print (new_size)
        image = cv2.resize(im, (new_size[1], new_size[0]))
        cv2.imwrite(imgDir + '/temp/' + img_path, image)
        time.sleep(10) 
        faces = CF.face.detect(imgDir + '/temp/' + img_path)
    else:
        return        
        #faces = CF.face.detect(imgDir + img_path)
        #image=cv2.imread(imgDir + img_path)
    #return
    #img_path = '../Face-Detect/data_geis_1/2017-08-22 09-57-33.jpg'
    
    #print("Extracted/" + os.path.splitext(os.path.basename(img_path))[0] + "_" + str(randint(0,10000))+".jpg")
    #return
    
    #os.chdir("Extracted")
    print(faces)
    for face in faces:
        #top': 376, 'left': 1129, 'width': 171, 'height': 171
        rect = face['faceRectangle']
        left = rect['left'] - 20
        top = rect['top'] - 20  #376
        bottom = left + rect['height'] + 20
        right = top + rect['width'] + 20
        sub_img = image[top:right, left:bottom]
        cv2.imwrite("Extracted/" + os.path.splitext(os.path.basename(img_path))[0] + "_" + str(randint(0,10000))+".jpg", sub_img)

def traindata():
    #for ef in os.listdir(traingdata):
    #    print(ef)
    #del self.detected_face_paths[:]
    util.CF.large_face_list.create(large_face_list_id)
    for ef in os.listdir(trainingdata):
        print(ef)
        res = util.CF.large_face_list_face.add(trainingdata + ef, large_face_list_id)
        print( 'Response: Success. Add with Persisted Face Id {}'.format(res['persistedFaceId']))
        detected_face_paths.append(ef)
        face = model.Face(res, ef)
        persisted_faces[face.persisted_id] = face
        time.sleep(10)  

    res = util.CF.large_face_list.train(large_face_list_id)


if __name__ == "__main__":
	
	if not "Output" in os.listdir("."):
		os.mkdir("Output")
traindata()
    
#for ef in os.listdir(imgDir):
#    detect_face(ef)

    
    #time.sleep(10) 
        #fileList.append(os.path.splitext(os.path.basename(ef))[0])

#print(faces)

#def getRectangle(faceDictionary):
#    rect = faceDictionary['faceRectangle']
#    left = rect['left'] - 10
#    top = rect['top'] - 10
#    bottom = left + rect['height'] + 10
#    right = top + rect['width'] + 10
    #return ((left, top), (bottom, right))
 #   return  ((top,right), (left,bottom))
    #return  '(' + str(top) + ':' + str(bottom) + '),(' + str(left) + ':' + str(right) + ')'


    #draw.rectangle(getRectangle(face), outline='red')
