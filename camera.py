import cv2

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_fram(self):
        ret, fram = self.video.read() # fram -> ndarray
        result, fram_image = cv2.imencode(".jpg", fram) # fram_image -> ndarray
        return fram_image.tobytes()