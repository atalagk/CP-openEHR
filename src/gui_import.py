import tehr_auth
import sys
import requests
from PySide.QtGui import *
from PySide.QtCore import *

app = QApplication(sys.argv)
win = QWidget()

win.resize(640, 480)
win.setWindowTitle("Enter CSV")

btn_import = QPushButton("Import", win)

#@Slot()
def on_click():
    postData = txt_csv.toPlainText()
    newData =  postData #postData.replace('°C', "Â°C")
    #print(newData)

    r = importCSV(newData)
    print(r)
    print(r.headers['content-type'])
    r.encoding = 'utf-8'
    print("response text:", r.text)
    print("response url:", r.url)
    print("request  url", r.request.url)
    print("request headers", r.request.headers)
    print("request body", r.request.body)

btn_import.clicked.connect(on_click)

txt_csv = QTextEdit("Enter CSV", win)

def text_click(event):
    txt_csv.clear()

txt_csv.mouseDoubleClickEvent = text_click

txt_templateID = QLineEdit(win)
txt_templateID.setPlaceholderText("Enter Template ID")

txt_templateLang = QLineEdit("en", win)

txt_subjectNameSpace = QLineEdit(win)
txt_subjectNameSpace.setPlaceholderText("Enter Subject Namespace")

layout = QVBoxLayout()
layout.addWidget(btn_import)
layout.addWidget(txt_csv)
layout.addWidget(txt_templateID)
layout.addWidget(txt_templateLang)
layout.addWidget(txt_subjectNameSpace)
win.setLayout(layout)

win.show()

def importCSV(data):
    url = tehr_auth.baseUrl + "/import/csv"
    para = {}
    para['templateId'] = txt_templateID.text()
    para['templateLanguage'] = txt_templateLang.text()
    if txt_subjectNameSpace.text() != "":
        para['subjectNamespace'] = txt_subjectNameSpace.text()

    from requests.auth import HTTPBasicAuth
    header = {'Content-Type': 'application/octet-stream'}
    response = requests.post(url, data, headers=header, params=para, auth=HTTPBasicAuth(tehr_auth.username, tehr_auth.password))
    return response

sys.exit(app.exec_())