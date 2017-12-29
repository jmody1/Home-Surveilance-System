import cv2
import sqlite3

picam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml') #This file is attached in the zip but is taken from opencv lib 

#Inserting the new user data into knownfaces.db
def insertOrUpdate(userid,Name) :
	conn=sqlite3.connect("knownfaces.db")
	cmd="SELECT * FROM People WHERE userid="+str(userid)
	cursor=conn.execute(cmd)
	isRecordExist=0
	for row in cursor:
		isRecordExist=1
	if(isRecordExist==1):
		cmd="UPDATE People SET Name="+ str(Name)+"WHERE userid="+str(userid)
	
	else :
		cmd="INSERT INTO People(userid,Name) Values("+str(userid)+","+str(Name)+")"
	conn.execute(cmd)
	conn.commit()
	conn.close()

pic=0 #Pic counter 
userid=raw_input('Kindly Enter your Userid')
name=raw_input('Kindly Enter your Name')
insertOrUpdate(userid,name)

#Will continue to detect faces till pic count reaches 60
while(True):
    out,image = picam.read()
    grayscaleimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detectedfaces = detector.detectMultiScale(grayscaleimage, 1.3, 5)
    for (x,y,w,h) in detectedfaces:
        pic=pic+1
        cv2.imwrite("imagedatabase/User."+userid +'.'+ str(pic) + ".jpg", grayscaleimage[y:y+h,x:x+w]) #Storing each detected image in dataset folder which will be given for training

        cv2.imshow('window',image)
    elif pic>50: #Total number of pics to be taken to make sure the dataset is generated with sufficient confidence
        break
	cv.waitKey(0) 
picam.release()
cv2.destroyAllWindows()