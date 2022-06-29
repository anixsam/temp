from tabnanny import check
from tkinter import Image
import cv2
import numpy as np
import face_recognition
import os
import pyrebase
from firebase import *
from folderInitialize import *

initializeImageData()

config = {
    "apiKey": "AIzaSyCWiW32lafGna4ANrhma-9E4Ck8ZH07fa8",
    "authDomain": "manless-bus-ticket-system.firebaseapp.com",
    "databaseURL": "https://manless-bus-ticket-system-default-rtdb.firebaseio.com",
    "projectId": "manless-bus-ticket-system",
    "storageBucket": "manless-bus-ticket-system.appspot.com",
    "messagingSenderId": "943986302767",
    "appId": "1:943986302767:web:da972a6c1ee19028c38bda"
  }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
old_user = ""
users = read_users()
COLOR=[]
#IMG=[]
# IMAGE=[]
face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
while True:
  users = read_users()
  file = open("names.txt","r")
  names = file.readlines()
  file.close()
  ret,frame=cap.read()
  gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  faces=face_cascade.detectMultiScale(gray,1.1,5)
  for(x,y,w,h) in faces:
    COLOR=frame[y:y+h,x:x+w]
    img_item='person.jpg'
    cv2.imwrite(img_item,COLOR)
    clr = (255, 0, 0)  # BGR 0-255
    stroke = 2
    end_cord_x = x + w
    end_cord_y = y + h
    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), clr, stroke)
    try:
      IMAGE=cv2.cvtColor(COLOR,cv2.COLOR_BGR2RGB)
      IMG=face_recognition.face_encodings(IMAGE)[0]
    except:
      print("Face not detected")
    
    


    for i in range(0,len(names)):
      
      preset = cv2.imread("image_data/"+str(names[i][0:len(names[i])-1])+".jpg")
      IMG_PRESET=face_recognition.face_encodings(preset)[0]
      try:
        global result
        result = face_recognition.compare_faces([IMG_PRESET], IMG)
      except:
        print("")
      if(result[0] == True):
        name = names[i][0:(len(names[i])-1)]
        print(name)
        if name in users.keys() and old_user != name:
          wallet = int(db.child(str("users/"+users[name])).get().val()['walletBalance'])
          new_amount = wallet - 10 
          if new_amount > 0 :
            db.child(str("users/"+users[name])).update({'walletBalance' : new_amount})
          old_user = name
        else:
          print("*************************")


    # IMAGE = []
    
  cv2.imshow('frame', frame)
  if cv2.waitKey(20) & 0xFF == ord('q'):
      break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
