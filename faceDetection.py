import os
import cv2
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


# 認証KEYとENDPOINT
KEY = "322c49b0462c4ee78fd110e7e73bb323"
ENDPOINT = "https://tomoki-0104-mina.cognitiveservices.azure.com/"

# FaceClientを認証する
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# 1つの顔を含む画像の顔検出を行う(複数の顔検出も可能)，ネット上の画像
single_face_image_url = "https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg"
single_image_name = os.path.basename(single_face_image_url)

# FacedetectionModel3を使用すると精度が上がる
detected_faces = face_client.face.detect_with_url(url=single_face_image_url, detection_model="detection_03")
if not detected_faces:
    raise Exception("No face detected from image {}".format(single_image_name))

# 幅・高さを長方形の頂点に変更する
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height

    return ((left, top), (right, bottom))

# urlから画像をダウンロードする
response = requests.get(single_face_image_url)
img = Image.open(BytesIO(response.content))

# 取得した顔座標をもとにボックスで囲む
print('Drawing rectangle around face... see popup for results.')
draw = ImageDraw.Draw(img)
for face in detected_faces:
    draw.rectangle(getRectangle(face), outline = "red")

# ブラウザに画像を表示
img.show()










# # 検出された一意のIdを表示
# print("Detected face ID from", single_image_name, ":")
# for face in detected_faces: print(face.face_id)

# # faceIDを"find similar"で使用するために保存する
# # detected_faces[0]で最初に検出された顔のid
# first_image_face_ID = detected_faces[0].face_id