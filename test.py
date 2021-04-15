import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 

# firestoreを初期化する(アプリケーションのデフォルトの認証情報を使用)
cred = credentials.Certificate("autorecordapp-cbd37-firebase-adminsdk-59sxe-b959fef264.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# # firestoreのコレクション名の取得
# list_col = []
# cols = db.collections()
# [list_col.append(col.id) for col in cols]

# for i in range(len(list_col)):
#     print(str(list_col[i]))

doc_ref = db.collection("usersId").document("2021年4月14日")
doc = doc_ref.get()
print(doc.to_dict()["total_time"])