import sqlite3
import sys

ini = sys.argv[1]
hostname = sys.argv[2]
port = sys.argv[3]
student_id = ini.split("=")[1]

# 打开数据库
db = sqlite3.connect('data\Student_data.db')
cursor = db.cursor()

sql = ""
if student_id == "000000":
    sql = "SELECT * from student;"
else:
    sql = "SELECT * from student where id = " + student_id +";"
cursor.execute(sql)

data = cursor.fetchall()
res = ""
with open("cgi-bin/query.html", "r", encoding="utf-8") as f:
    for line in f:
        res += line
    student_data = ''
    for student in data:
        temp = "<tr>"
        temp += "<th>" + str(student[0]) + "</th>"
        temp += "<th>" + student[1] + "</th>"
        temp += "<th>" + student[2] + "</th>"
        temp += "</tr>\n"
        student_data += temp
    res = res.replace("$data", student_data)

print(res)