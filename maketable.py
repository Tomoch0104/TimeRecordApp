import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore 


def makeTable(request_time, user_ID):

    list_data = []

    db = firestore.client()

    docs = db.collection(user_ID).stream()

    for doc in docs:
        slice_docid = doc.id[0:6]
        if request_time == slice_docid:
            total_time = doc.to_dict()["total_time"]
            day_info = int(doc.id[6:8])
            list_value = []
            list_value.append(day_info)
            list_value.append(total_time)
            list_data.append(list_value)
    
    return list_data








# def checkLoginID(self, loginID, loginPass):

#     db = firestore.client()

#     doc_ref = db.collection(loginID).document("userInfo")
#     doc = doc_ref.get()
    
#     if doc.exists:
#         key = doc.to_dict()["pass"]
#         if key == loginPass:
#             return "permission"
#         else:
#             return "No_permission"
#     else:
#         return "No_permission"

# # firestoreのコレクション名の取得
# list_col = []
# cols = db.collections()
# [list_col.append(col.id) for col in cols]

# for i in range(len(list_col)):
#     print(str(list_col[i]))

# doc_ref = db.collection("usersId").document("2021年4月14日")
# doc = doc_ref.get()
# print(doc.to_dict()["total_time"])