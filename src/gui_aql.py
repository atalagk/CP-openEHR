import auth
import sys
import pprint
import requests
from PyQt6.QtWidgets import *
#from PySide.QtGui import *
#from PySide.QtCore import *

default_aql = 'select e/ehr_id/value from EHR e limit 10'

app = QApplication(sys.argv)
win = QWidget()

win.resize(320, 240)
win.setWindowTitle("Enter AQL")

btn_query = QPushButton("Run AQL", win)

#@Slot()
def on_click():
    aql_final = txt_aql.toPlainText()
    #aql_final = aql_final.replace('\n', ' ').replace('\r', '')
    aql_final = ' '.join(aql_final.split())     # gets rid of newline and whitespace

    try:
        r = getAQL(aql_final).json()
    except ValueError:
        print("Opps! - trying non JSON r")
        r = getAQL(aql_final)
        #quit()
    try:
        # for items in r['RESULTSET']:    # try to get nice formatted JSON view within Resultset
        for items in r['rows']:    # try to get nice formatted JSON view within Resultset
            pprint.pprint(items)
    except ValueError:
        pprint.pprint(r)
    except:
        print("Opps!")
        print(r)
        quit()

btn_query.clicked.connect(on_click)

txt_aql = QPlainTextEdit(default_aql, win)

def text_click(event):
    txt_aql.clear()

txt_aql.mouseDoubleClickEvent = text_click

layout = QVBoxLayout()
layout.addWidget(btn_query)
layout.addWidget(txt_aql)
win.setLayout(layout)

win.show()

def getAQL(aql):
    url = auth.baseUrl + "/query/aql"
    from requests.auth import HTTPBasicAuth
    response = requests.get(url, params={'q': aql}, auth=HTTPBasicAuth(auth.username, auth.password))
    return response

sys.exit(app.exec())