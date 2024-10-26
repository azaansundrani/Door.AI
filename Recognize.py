import pandas as pd
import numpy as np
import cv2 as cv
import subprocess

id_names = pd.read_csv('id-names.csv')
id_names = id_names[['id', 'name']]
motorCode = ['python3', '/home/acm/Door.Ai/1testServo.py']

faceClassifier = cv.CascadeClassifier('/home/acm/Door.Ai/Classifiers/haarface.xml')

lbph = cv.face.LBPHFaceRecognizer_create(threshold=500)
lbph.read('/home/acm/Door.Ai/Classifiers/trainedmode.xml')

camera = cv.VideoCapture(0)
count = 0

while cv.waitKey(1) & 0xFF != ord('q'):
    _, img = camera.read()
    grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    faces = faceClassifier.detectMultiScale(grey, scaleFactor=1.1, minNeighbors=4)

    for x, y, w, h in faces:
        faceRegion = grey[y:y + h, x:x + w]
        faceRegion = cv.resize(faceRegion, (220, 220))

        label, trust = lbph.predict(faceRegion)
        if trust < 60:  # Establish a confidence level to recognize the user
            print(trust)
            try:
                name = id_names[id_names['id'] == label]['name'].item()
                cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.putText(img, name, (x, y + h + 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                count += 1
                print(count)
                print(name)
                if count  == 20:
                    subprocess.run(motorCode)
                    print("Opening Door")
                    camera.release()
                    cv.destroyAllWindows()
                    #subprocess.run('python3',motorCode)

            except:
                pass
        else:
            print(trust)
            print('Unknown')
            # if the confidence is low label as unknown...
            print(trust)
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.putText(img, 'unknown', (x, y + h + 30), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

    

camera.release()
cv.destroyAllWindows()
