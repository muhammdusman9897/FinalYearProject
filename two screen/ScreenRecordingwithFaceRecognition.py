from datetime import datetime
import time
import face_recognition
import cv2
import numpy as np
import pyautogui as ptogu
from plyer import notification

def main():
    #Temporary String Variable
    reportVar = "Report: "
    notificationVar = ['']

    SCREEN_SIZE = ptogu.size()
    FRAME_RATE = 7

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter("F://machine learning//two screen//screen-recording3.avi", fourcc, FRAME_RATE, (SCREEN_SIZE))

    usman_image=face_recognition.load_image_file("faces/usman.jpg")
    usman_face_encoding = face_recognition.face_encodings(usman_image)[0]

    usman_image2=face_recognition.load_image_file("faces/usman2.jpg")
    usman2_face_encoding = face_recognition.face_encodings(usman_image2)[0]

    Hammad_image=face_recognition.load_image_file("faces/Hammad.jpg")
    Hammad_face_encoding=face_recognition.face_encodings(Hammad_image)[0]


    Raheel_image=face_recognition.load_image_file("faces/Raheel.jpeg")
    Raheel_face_encoding=face_recognition.face_encodings(Raheel_image)[0]
   
    Daniyal_image = face_recognition.load_image_file("faces/Daniyal.jpeg")
    Daniyal_face_encoding = face_recognition.face_encodings(Daniyal_image)[0]

    Atta_image = face_recognition.load_image_file("faces/Attaullah.jpeg")
    Atta_face_encoding = face_recognition.face_encodings(Atta_image)[0]


    known_face_encodings = [
    
        usman_face_encoding,
        usman2_face_encoding,
        Hammad_face_encoding,
        Raheel_face_encoding,
        Daniyal_face_encoding,
        Atta_face_encoding,
    
    ]
    known_face_names = [
        "Usman",
        "Usman",
        "Hammad",
        "Raheel",
        "Daniyal",
        "Attaullah",
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    facesCount = 0
    while True:
       
        img = ptogu.screenshot()

        frame = np.array(img)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  

        
        if cv2.waitKey(1) == ord('q'):
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                currentTime = datetime.now()
                currentTime = currentTime.strftime("%d/%m/%Y %H:%M:%S")
              
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                facesCount += 1
                faceDetected = "yes"
                faceRecognized = name 
                reportVar = reportVar + str(facesCount) + ". Date: " + currentTime + ", Face Detected: " + faceDetected + ", Face Recognized: " + faceRecognized + "\n"

                print(reportVar)

                face_names.append(name)

                ### NOTIFICATION ###
                if name != "Unknown" and not (name in notificationVar):
                    notification.notify(
                    #title of the notification,
                    title = "{} Present Alert".format(name),
                    #the body of the notification
                    message = "Face Recognized : {faceRecognized}".format(
                                faceRecognized = name),
                    #creating icon for the notification
                    #we need to download a icon of ico file format
                    app_icon = r"StockTick-Icons.ico",
                    # the notification stays for 50sec
                    timeout  = 10
                    )           
                    
                    notificationVar.append(name)
                # obj = DeepFace.analyze(frame, actions = ['gender', 'race', 'emotion'])
                # #objs = DeepFace.analyze(["img1.jpg", "img2.jpg", "img3.jpg"]) #analyzing multiple faces same time
                # print("years old ",obj["dominant_race"]," ",obj["dominant_emotion"]," ", obj["gender"])                
        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            #String Variable for Emotions and Names
            rectangleText = name + "-" 

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, rectangleText, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        out.write(frame)

        print() #next line for the report

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # out.release()
    # cv2.destroyAllWindows()

if __name__ == "__main__":
   main()
