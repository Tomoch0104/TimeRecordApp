import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 


class Firestore(object):
    # firestoreを初期化する(アプリケーションのデフォルトの認証情報を使用)
    cred = credentials.Certificate("自分の秘密鍵を入力")
    firebase_admin.initialize_app(cred)

    def addDatabese(self, date, start_time, end_time, study_time, total_time_convert, time_count):

        db = firestore.client()

        # dataを設定する
        data = {
            str(time_count) + "_start_time" : start_time,
            str(time_count) + "_end_time" : end_time,
            str(time_count) + "_study_time" : study_time,
            "total_time" : total_time_convert
        }

        # 新しいコレクションとドキュメントを作成
        doc_ref = db.collection("usersId").document(date).set(data, merge = True)