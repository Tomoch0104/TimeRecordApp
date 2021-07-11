import cv2

# カメラから画像を取得
class Camera(object):
    # イニシャライズでインスタンス化
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # フレーム画像の取得
    def get_fram(self):
        # 画像の取得
        ret, fram = self.video.read() # fram -> ndarray
        result, fram_image = cv2.imencode(".jpg", fram) # fram_image -> ndarray

        # バイト型に変換して返す
        return fram_image.tobytes()