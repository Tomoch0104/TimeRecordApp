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
import maketable
from flask import Flask, render_template, Response, request, redirect, url_for
import log


app = Flask(__name__)

# フレーム画像から顔検出，結果に応じて処理
def gen(camera, faceApi, firestore, times, userID):
    # フレームカウント数
    count = 0
    # 顔検出成功カウンター
    time_count = 1
    # 合計時間
    total_time = None
    # 顔検出成功カウンター開始
    start_time = None
    # 顔検出成功カウンター終了
    end_time = None
    # 顔検出開始Unix時間
    start_time_ut = None
    # 顔検出終了Unix時間
    end_time_ut = None
    # 瞬間勉強時間
    study_time = None
    # 勉強開始日
    start_time_day = None
    # 合計時間の取得
    total_time = firestore.addtotaltime(total_time, userID) * 60
    print(total_time/60)

    while True:
        # カメラ画像を取得
        fram_image = camera.get_fram()
        if count == 100:
            count = 0 # countを0に戻す
            # 顔検出
            rect_image, judgment = faceApi.surround_rect(fram_image)
            if judgment == 0: # 未検出
                if rect_image is not None:
                    # end_time_utに値が入っていないかつ，start_time_utに値が入っているときのみ実行
                    if end_time_ut is None and start_time_ut is not None:
                        # 終了時刻を取得
                        end_time = datetime.datetime.now()
                        date = str(end_time.year) + str(end_time.month).zfill(2) + str(end_time.day).zfill(2) #　現在の日付
                        end_time = str(end_time.hour).zfill(2) + ":" + str(end_time.minute).zfill(2)
                        end_time_ut = time.time() # 顔検出停止Unix時間
                        study_time = int(end_time_ut - start_time_ut) # 勉強時間を計算
                        total_time += study_time
                        print(total_time)
                        # firestore保存用に時間表示を変換
                        study_time = times.convertTime(study_time)
                        total_time_convert = times.convertTime(total_time)

                        # firestoreに追加
                        firestore.addDatabese(date, start_time, end_time, study_time, total_time_convert, time_count, userID)

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

@app.route("/preview", methods=["GET","POST"])
def preview():
    UserName = request.form["UserName"]
    return render_template("preview.html", UserID=UserName)

@app.route("/video_feed/<string:ID>")
def video_feed(ID):
    return Response(gen(Camera(), FaceApi(), Firestore(), Times(), ID),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/menu", methods=["GET","POST"])
def menu():
    if(request.method == "GET"):
        return render_template("/")
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
                return render_template("index_errornew.html")
            else:
                # 新規登録に成功した場合の処理
                return render_template("menu.html", UserID=newID)
        # ログイン処理
        elif newID == "" and newPass == "" and loginID != "" and loginPass != "":
            state = Firestore().checkLoginID(loginID, loginPass)
            if state == "permission":
                # ログインに成功した場合の処理
                return render_template("menu.html", UserID=loginID)
            else:
                return render_template("index_errorlog.html")
        else:
            return render_template("index_errorinput.html")


@app.route("/log", methods=["GET","POST"])
# 過去のデータを用意する関数
def log():
    # GETの時
    if(request.method == "GET"):
        print("get")
        return render_template("/")
    # POSTの時
    else:
        # htmlから各入力値を格納
        UserID = request.form["UserName"]
        Y = request.form["Year"]
        M = request.form["Month"]
        D = request.form["Day"]
        # 2021##の文字列
        YM = Y + M
        # 2021####の文字列
        YMD = YM + D
        # 特定月のデータを取得
        # 表示用の文字列を用意
        img_path = "fig/" + UserID + "/" + YM + ".png" 
        Month = Y + "年" + M + "月の勉強時間"
        # 表，グラフの作成
        table = maketable.makeTable(YM, UserID)
        # データをリストに格納
        data = []
        data.append(table)
        data.append(UserID)
        data.append(Month)
        data.append(img_path)
        # print(img_path)
        # print(YM)
        return render_template("log.html", Data=data)
        """
        試行錯誤
        """
        # 特定月のデータを取得
        # if(Y != "" and M != "" and D == ""):
        #     # 表示用の文字列を用意
        #     img_path = "fig/" + UserID + "/" + YM + ".png" 
        #     Month = Y + "年" + M + "月の勉強時間"
        #     # 表，グラフの作成
        #     table = maketable.makeTable(YM, UserID)
        #     # データをリストに格納
        #     data = []
        #     data.append(table)
        #     data.append(UserID)
        #     data.append(Month)
        #     data.append(img_path)
        #     # print(img_path)
        #     # print(YM)
        #     return render_template("log.html", Data=data)
        # # 特定日のデータを取得
        # elif(Y != "" and M != "" and D != ""):
        #     # 表示用の文字列を用意
        #     img_path = "fig_d/" + UserID + "/" + YM + "/" + D + ".png"
        #     Day = Y + "年" + M + "月" + D + "日の勉強時間"
        #     # 表，グラフの作成
        #     table = maketable.makeDaytable(YMD, UserID)
        #     # データをリストに格納
        #     data = []
        #     data.append(table)
        #     data.append(UserID)
        #     data.append(Day)
        #     data.append(img_path)
        #     # print(img_path)
        #     return render_template("log.html", Data=data)
        # # 適切な入力でないとエラーをはく
        # else:
        #     return render_template("input_error.html")


if __name__ == "__main__":
    app.run(debug=True)
    
