import cv2
import numpy as np
import os
from PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()
root = 'dataSet'
arr_path = os.listdir(root)
listFaces = []
faces = []
listMSSVs = []
for path in arr_path:
    MSSV = int(path.split('_')[1])
    # listMSSVs.append(MSSV)
    imagePaths = [os.path.join(root+"/"+path, f) for f in os.listdir(root+"/"+path)]
    for imagePath in imagePaths:
        print(imagePath)
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')

        faces.append(faceNp)
        listMSSVs.append(MSSV)

        # print(faces)
        # print(listMSSVs)
        # # listFaces.append(faces)
    # cv2.imshow('Training', faceNp)
    # cv2.waitKey(1000)
recognizer.train(faces, np.array(listMSSVs))



if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/training.yml')

# cv2.destroyAllWindows()