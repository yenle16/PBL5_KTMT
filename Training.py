from facenet_pytorch import MTCNN
import os
from PIL import Image
import facenet
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np



recognizer = MTCNN()
root = 'dataSetMTCNN'
arr_path = os.listdir(root)
faces = []
listMSSVs = []
def extract_face_features(image_path):
    img = Image.open(image_path)
    img = img.resize((160, 160))  # Resize image to the input size of FaceNet model
    img = img.convert('RGB')
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features[0]
FACENET_MODEL_PATH = 'E:\pbl5MiAI_FaceRecog_2\Models\20180402-114759.pb'
model = facenet.load_model(FACENET_MODEL_PATH)
for path in arr_path:
    MSSV = int(path.split('_')[1])
    imagePaths = [os.path.join(root+"/"+path, f) for f in os.listdir(root+"/"+path)]
    for imagePath in imagePaths:
        face_features = extract_face_features(imagePath)
        print(imagePath)
        img = Image.open(imagePath)
        boxes, landmarks = recognizer.detect(img)

        # Kiểm tra xem có nhận diện được khuôn mặt hay không
        if boxes is not None:
            faces.append(img)

        listMSSVs.append(MSSV)
        print(face_features)



# if not os.path.exists('recognizer'):
#     os.makedirs('recognizer')

# recognizer.save('recognizer/trainingmtcnn.yml')
