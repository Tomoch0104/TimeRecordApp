import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 


class Firestore(object):
    # firestoreを初期化する(アプリケーションのデフォルトの認証情報を使用)
    cred = credentials.Certificate("autorecordapp-cbd37-firebase-adminsdk-59sxe-b959fef264.json")
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

    
    def checkNewID(self, newID, newPass):

        db = firestore.client()

        data ={
            "pass" : newPass
        }

        list_col = []
        cols = db.collections()
        [list_col.append(col.id) for col in cols]

        for i in range(len(list_col)):
            if list_col[i] == newID:
                return "overlap"
        
        db.collection(newID).document("userInfo").set(data)
        return "No_overlap"


    def checkLoginID(self, loginID, loginPass):

        db = firestore.client()

        doc_ref = db.collection(loginID).document("userInfo")
        doc = doc_ref.get()
        key = doc.to_dict()["pass"]

        # パスワードが存在するなら
        if key == loginPass:
            return "permission"
        else:
            return "No_permission"






        

        # list_col = []
        # cols = db.collections()
        # [list_col.append(col.id) for col in cols]

        # for i in range(len(list_col)):
        #     # 一致するコレクション名とパスワードがあるか確認
        #     if list_col[i] == loginID:
        #         return "permission"

        # return "No_permission"
