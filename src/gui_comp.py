import tehr_auth
import sys
import requests
import pprint
import json
from PySide.QtGui import *

def txt_content_dblClick(event):
    txt_content.clear()

def op_changed():
    if cmb_op.currentIndex() == 1:  #POST
        showRow(txt_ehr)
        showRow(txt_templateID)
        showRow(txt_subjectNameSpace)
        hideRow(txt_comp)

    elif cmb_op.currentIndex() == 2:  #GET
        showRow(txt_comp)
        hideRow(txt_subjectNameSpace)
        hideRow(txt_ehr)
        hideRow(txt_templateID)
        txt_content.clear()

def hideRow(field):
    field.hide()
    layout.labelForField(field).hide()

def showRow(field):
    field.show()
    layout.labelForField(field).show()

def on_click():
    url = tehr_auth.baseUrl + "/composition"
    para = {}
    para['format'] = cmb_str.currentText()
    postData = txt_content.toPlainText()
    newData = postData.replace('°C', "Â°C")

    if cmb_op.currentText() == "POST":
        para['templateId'] = txt_templateID.text()
        if txt_subjectNameSpace.text() != "":
            para['subjectNamespace'] = txt_subjectNameSpace.text()
        if txt_ehr.text() != "":
            para['ehrId'] = txt_ehr.text()
        r = sendCompOperation(url, para, "POST", newData)

    elif cmb_op.currentText() == "GET":
        url = url + "/" + txt_comp.text()
        r = sendCompOperation(url, para, "GET")
        #t = pprint.pformat(response.json())
        t = json.dumps(r.json(), indent=4, sort_keys=True)
        txt_content.setText(t)
        #msg = QMessageBox()
        #msg.setText(response.text)
        #msg.exec_()
        #quit()

    win.setWindowTitle(title + ' >>> ' + str(r.status_code))
    print(r.status_code)
    print(r.headers['content-type'])
    print("url:", r.url)
    pprint.pprint(r.json())

def sendCompOperation(url, para, verb, data=None):
    from requests.auth import HTTPBasicAuth
    header = {'Content-Type': 'application/json;charset=UTF-8'}

    if verb == "POST":
        response = requests.post(url, data, headers=header, params=para, auth=HTTPBasicAuth(tehr_auth.username, tehr_auth.password))
    elif verb == "GET":
        response = requests.get(url, params=para, auth=HTTPBasicAuth(tehr_auth.username, tehr_auth.password))
    return response

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()

    win.resize(640, 480)
    title = "Composition Operations"
    win.setWindowTitle(title)

    cmb_op = QComboBox(win)
    cmb_op.addItems(["", "POST", "GET"])

    cmb_str = QComboBox(win)
    cmb_str.addItems(["FLAT", "STRUCTURED", "RAW"])

    btn_ehr = QPushButton("Send Request", win)

    txt_content = QTextEdit("Enter Content", win)

    txt_ehr = QLineEdit(win)
    txt_ehr.setPlaceholderText("Enter EhrId")

    txt_comp = QLineEdit(win)
    txt_comp.setPlaceholderText("Enter Composition Uid")

    txt_templateID = QLineEdit(win)
    txt_templateID.setPlaceholderText("Enter Template ID")

    txt_subjectNameSpace = QLineEdit(win)
    txt_subjectNameSpace.setPlaceholderText("Enter Subject Namespace")

    layout = QFormLayout()
    layout.addRow("REST Verb", cmb_op)
    layout.addRow("Structure", cmb_str)

    layout.addRow(None, txt_content)
    layout.addRow(None, btn_ehr)

    layout.addRow("Ehr ID", txt_ehr)
    layout.addRow("Template ID", txt_templateID)

    layout.addRow("Comp UID", txt_comp)
    layout.addRow("Subject Namespace", txt_subjectNameSpace)

    win.setLayout(layout)

    win.show()

    txt_content.mouseDoubleClickEvent = txt_content_dblClick

    btn_ehr.clicked.connect(on_click)

    cmb_op.currentIndexChanged.connect(op_changed)

    cmb_op.setCurrentIndex(1)
    sys.exit(app.exec_())