import cv2
import os
import requests
import numpy
import time
import datetime
from PIL import Image, ImageDraw
from io import BytesIO
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from camera import Camera
from faceApi import FaceApi
from firestore import Firestore
from times import Times
from flask import Flask, render_template, Response, request, redirect, url_for


app = Flask(__name__)

def gen(camera, faceApi, firestore, times):
    count = 0
    time_count = 1
    total_time = 0
    start_time = None
    end_time = None
    start_time_ut = None
    end_time_ut = None
    study_time = None
    start_time_day = None

    while True:
        fram_image = camera.get_fram()

        if count == 100:
            count = 0 # countを0に戻す
            rect_image, judgment = faceApi.surround_rect(fram_image)
            if judgment == 0: # 未検出
                if rect_image is not None:
                    # end_time_utに値が入っていないかつ，start_time_utに値が入っているときのみ実行
                    if end_time_ut is None and start_time_ut is not None:
                        end_time = datetime.datetime.now()
                        date = str(end_time.year) + str(end_time.month).zfill(2) + str(end_time.day).zfill(2) #　現在の日付
                        end_time = str(end_time.hour).zfill(2) + ":" + str(end_time.minute).zfill(2)
                        end_time_ut = time.time() # 顔検出停止Unix時間
                        study_time = int(end_time_ut - start_time_ut) # 勉強時間を計算
                        total_time += study_time
                        study_time = times.convertTime(study_time)
                        total_time_convert = times.convertTime(total_time)

                        # firestoreに追加
                        firestore.addDatabese(date, start_time, end_time, study_time, total_time_convert, time_count)

                        # time_countを進める
                        time_count += 1

                        # 各時間変数の値をNoneで初期化する
                        start_time = None
                        end_time = None
                        start_time_ut = None
                        end_time_ut = None
                        study_time = None

                    yield (b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + rect_image + b"\r\n")
                else:
                    print("rect_image is none")
            else: # 検出
                if rect_image is not None:
                    if start_time_ut is None:
                        start_time =  datetime.datetime.now() # 顔検出時間
                        if start_time_day != start_time.day:
                            time_count = 1
                        start_time_day = start_time.day
                        start_time = str(start_time.hour).zfill(2) + ":" + str(start_time.minute).zfill(2)
                        start_time_ut = time.time() # 顔検出開始Unix時間
                    yield (b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + rect_image + b"\r\n")
                else:
                    print("rect_image is none")
        else:
            count += 1
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
    return Response(gen(Camera(), FaceApi(), Firestore(), Times()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/menu", methods=["GET","POST"])
def menu():
    if(request.method == "GET"):
        print("get")
    else:
        # ユーザー情報(idとpass)
        loginID = request.form["loginID"]
        loginPass = request.form["loginPass"]
        newID = request.form["newID"]
        newPass = request.form["newPass"]

        # 新規登録処理
        if loginID == "" and loginPass == "" and newID != "" and newPass != "":
            state = Firestore().checkNewID(newID, newPass)
            if state == "overlap":
                return render_template("preview.html") # エラーページに返す(preview.htmlは仮)
        # ログイン処理
        elif newID == "" and newPass == "" and loginID != "" and loginPass != "":
            state = Firestore().checkLoginID(loginID, loginPass)
            if state == "permission":
                # loginIDを返す
                print(state)
            else:
                return render_template("preview.html") # loginID,loginPassが存在しないので専用のページに移動
        else:
            return render_template("preview.html") # idとpassの両方埋めてくださいのページに移動


    return render_template("menu.html")
    
@app.route("/log")
def log():
    # print(id)
    return render_template("log.html")

if __name__ == "__main__":
    app.run(debug=True)
    
