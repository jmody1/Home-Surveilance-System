import os
import cv2
import numpy as np
from PIL import Image


recognizer = cv2.face.createLBPHFaceRecognizer()
datasetlocation= 'imagedatabase/' #Folder to store images


def mapimagestoid(datasetlocation): #Function to take each image and id and then write the trained data to traineddata.yml
    imagePaths=[os.path.join(datasetlocation,f) for f in os.listdir(datasetlocation)]
    detectedfaces=[]
    userids=[]
    for datasetlocation in datasetlocation:
        faceImages=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImages,'uint8')
        id=int(os.path.split(datasetlocation)[1].split('.')[1])
        detectedfaces.append(faceNp) #Adding all the images to array
        userids.append(ID) #Adding all the userids in this array
        cv2.waitKey(10)
    return userids,detectedfaces

userids,detectedfaces=mapimagestoid(datasetlocation)
recognizer.train(detectedfaces,np.array(userids)) 
recognizer.save('traineddatabase/traineddata.yml')
cv2.destroyAllWindow()