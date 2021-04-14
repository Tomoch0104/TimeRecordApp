import cv2
import numpy
from PIL import Image, ImageDraw
from io import BytesIO
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class FaceApi(object):

    def getRectangle(self, faceDictionary): # 幅・高さを長方形の頂点に変更する
        rect = faceDictionary.face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height
        return ((left, top), (right, bottom))


    def surround_rect(self, fram_image): # 検出した顔を長方形で囲み，画像を返す
        # 認証KEYとENDPOINT
        KEY = "KEYを入力して下さい"
        ENDPOINT = "エンドポイントを入力してください"

        # FaceClientを認証する
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

        # FacedetectionModel3を使用すると精度が上がる
        detected_faces = face_client.face.detect_with_stream(image=BytesIO(fram_image), detection_model="detection_03")

        if not detected_faces:
            print("Not detected face")
            return fram_image, 0 # 顔検出を判定するカウンタ(0 -> 未検出，1 -> 検出)
            # raise Exception("No face detected from image")

        # 取得した顔座標をもとにボックスで囲む
        fram_image_rect = Image.open(BytesIO(fram_image))
        draw = ImageDraw.Draw(fram_image_rect)
        for face in detected_faces:
            draw.rectangle(self.getRectangle(face), outline="red", width=5) # width -> 境界線の太さ
        
        # PIL画像をndarrayに変換誤，エンコードする
        fram_image_rect = numpy.asarray(fram_image_rect)
        result, fram_image_rect = cv2.imencode(".jpg", fram_image_rect) 
        return fram_image_rect.tobytes(), 1
