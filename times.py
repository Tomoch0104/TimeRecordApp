class Times(object):
    def convertTime(self, study_time):
        if study_time < 60:
            study_time = "0"
        else :
            minute = int(study_time / 60)
            study_time = str(minute)

        # if study_time < 60:
        #     study_time = "0"
        # elif study_time >= 60 and study_time < 3600:
        #     minute = int(study_time / 60)
        #     study_time = str(minute) + "分"
        # else:
        #     hour = study_time / 3600
        #     minute = study_time % 3600
        #     study_time = str(hour) + "時間" + str(minute) + "分"

        return study_time