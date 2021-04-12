import cv2
from camera import Camera
from flask import Flask, render_template, Response
 
app = Flask(__name__)

def gen(camera):
    while True:
        fram_image = camera.get_fram()
        
        if fram_image is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + fram_image + b"\r\n")
        else:
            print("frame is none")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preview")
def preview():
    return render_template("preview.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)








# camera = cv2.VideoCapture(0) # カメラCh.(ここでは0)を指定
 
# # 撮影＝ループ中にフレームを1枚ずつ取得(qキーで撮影終了)
# while True:
#     ret, frame = camera.read() # フレームを取得
#     cv2.imshow('camera', frame) # フレームを画面に表示
 
#     # キー操作があればwhileループを抜ける
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
 
# # 撮影用オブジェクトとウィンドウの解放
# camera.release()
# cv2.destroyAllWindows()
    
