import numpy as np
import cv2
from PIL import Image
import pickle
import sqlite3
import smtplib
import os
from datetime import datetime
import re
import sys
import MySQLdb
import RPi.GPIO as GPIO

from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, cast
 	
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.output(20,0)
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#body = MIMEText('<p>Unknown Person <img src=
#Email content and initialization from smtp library
content = "unknown person is at your house"
mail = smtplib.SMTP("smtp.gmail.com",587)
mail.ehlo()
mail.starttls()
mail.login('elite.tr16@gmail.com',"elite.tr16")


db = MySQLdb.connect("localhost", "monitor", "password", "temps")
curs=db.cursor()


facedetector= cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')

picam = cv2.VideoCapture(0)
recognizer=cv2.face.createLBPHFaceRecognizer();

recognizer.load('/home/pi/fr/traineddatabase/traineddata.yml')
userid=0

def erl_handler(function):
    def handler(pin):
        cast(function, pin)
    set_message_handler(handler)
    return Atom("Success")


def getuserdata(userid):
    conn=sqlite3.connect("/home/pi/fr/knownfaces.db")
    cmd="SELECT * FROM People WHERE userid="+str(userid)
    cursor=conn.execute(cmd)
    userdata=None
    for row in cursor:
        userdata=row
    conn.close()
    return userdata

temp2 = "abc"

while(True):
	output, image = pi.read()
	grayscaleimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	detectedfaces = facedetector.detectMultiScale(gray, 1.3, 5)
	if(len(detectedfaces)!=0):
		for (x,y,w,h) in detectedfaces:
		    if(userdata!=None):
			currtime = str(datetime.now())
			temp = userdata[1]
			
			if(temp2 ==temp): #Condition to check if the previous detected face in last iteration was same as the current detected face
				temp3 = 1
				print("Same person")
			if(temp3!=1):
				pathstring = "/home/pi/fr/visitors/"+currtime+".jpg"
				curs.execute ("INSERT INTO visitors  values(%s,%s,%s)",(userdata[1],currtime,pathstring))
				cv2.imwrite("visitors/"+currtime+".jpg", gray[y:y+h,x:x+w])
				db.commit()
				print "Data committed"
				speak="espeak -s 110 'Welcome 'Owner --stdout | aplay -D 'default'"
				os.system(speak)	
				print("Face Detected %r"%(userdata[1]))
		    else:		
				temp = userdata
				temp3 = 0
				if(temp2 ==temp): #Condition to check if the previous detected face in last iteration was same as the current detected face
					temp3 = 1
					print("Same person")
				if(temp3!=1):
					print("Unknown face")
					currtime = str(datetime.now())
					pathstring = "/home/pi/fr/visitors/"+currtime+".jpg"
					curs.execute ("INSERT INTO visitors  values('Unknown Person',%s,%s)",(currtime,pathstring)) #Inserting the log into database
					db.commit()
					print "Data committed"
					cv2.imwrite("visitors/"+currtime+".jpg", gray[y:y+h,x:x+w])
					lighton = "escript functions.erl 20"
					mail.sendmail("elite.tr16@gmail.com","kishan1103@gmail.com",content)
					os.system(lighton)
					state = GPIO.input(20)
					print(state)
					if(state==0):
						print("Error turning the light on")
			temp2 = temp #Updating the value of temp2 to the current recognized faces
		    

	cv2.imshow('window',image)                
	cv.waitKey(0)                   
		
mail.close()
picam.release()
cv2.destroyAllWindows()