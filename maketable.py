from firebase_admin import firestore 
import log



def makeTable(request_time, user_ID):
    month_data = []
    month_data2 = []

    db = firestore.client()
    docs = db.collection(user_ID).stream()

    for doc in docs:
        slice_docid = doc.id[0:6]
        if request_time == slice_docid:
            slice_year = doc.id[0:4]
            slice_month = doc.id[4:6]
            slice_day = doc.id[6:8]
            total_time = doc.to_dict()["total_time"]
            total_hour = str(int(int(total_time)/60))
            minutes = str(int(total_time)%60)
            day_data = []
            day_data2 = []
            day_data.append(doc.id)
            day_data2.append(slice_year + "年" + slice_month + "月" + slice_day + "日の勉強時間")
            day_data.append(total_time)
            day_data2.append(total_hour.zfill(2) + "時間" + minutes.zfill(2) + "分間")
            month_data.append(day_data)
            month_data2.append(day_data2)
    
    # グラフを作成
    log.graphmaker(user_ID,month_data)

    return month_data2

# def makeDaytable(request_time, user_ID):
#     day_data = []

#     db = firestore.client()
#     doc_ref = db.collection(user_ID).document(request_time)
#     doc = doc_ref.get()

#     if doc.exists:
#         data = 



# def makeTable(request_time, user_ID):

#     list_data = []

#     db = firestore.client()

#     docs = db.collection(user_ID).stream()

#     for doc in docs:
#         slice_docid = doc.id[0:6]
#         if request_time == slice_docid:
#             total_time = doc.to_dict()["total_time"]
#             day_info = int(doc.id[6:8])
#             list_value = []
#             list_value.append(day_info)
#             list_value.append(total_time)
#             list_data.append(list_value)
    
#     return list_data








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