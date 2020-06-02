# list = [
#         13048052194
#
#     ]
# print(type(list))
#
# tuple = (1)
# print(type(tuple))
#
# tuple1 = (1,)
# print(type(tuple1))

list = {
    "success": "true", "error": "null", "data": {"token": "09702094d2ba4402a77ad786370b78ea", "user":
        {
            "id": 212, "melotUserId": "null", "mobile": "13048052195", "studentName": "Kitty", "gender": 0,
            "birthday": "2014",
            "diamonds": 0, "hasCompleteInfo": 1, "mvps": 0, "headPortraitUrl": "null", "courseList": [],
            "effectiveCourse": "null",
            "expireCourse": "null"}
                                                 }
}

a = list['data']['user']['id']
b = list['data']['token']
if a:
    print(a)
else:
    print("F")

# if __name__ == "__main__":
#
