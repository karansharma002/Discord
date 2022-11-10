from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Weather")
        MainWindow.resize(297, 156)
        MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 20, 81, 20))
        self.label.setText("")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(90, 50, 131, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 80, 221, 51))
        font = QtGui.QFont()
        font.setFamily("Constantia")
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Kalam")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n""border-color: rgb(0, 255, 0);")
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.clicked.connect(self.submit)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Weather", "Weather"))
        self.pushButton.setText(_translate("MainWindow", "SUBMIT"))
        self.label_2.setText(_translate("MainWindow", "ENTER CITY"))

    def submit(self):
        a = self.lineEdit.text()
        api_key = 'e03a406d69c0fb92a3938bf93da8d5d9'
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + a
    
        response = requests.get(complete_url) 
        x = response.json() 
        if x["cod"] != "404":
            z = x["weather"] 
            y = x["main"] 
            current_temperature = y["temp"] 
            C = int(current_temperature - 273.15)
            weather_description = z[0]["description"] 
            tmin = y['temp_min']
            tmax = y['temp_max']
            pressure = y['pressure']
            humidity = y['humidity']
            sea_level = y['sea_level'] if 'sea_level' in y else 'N/A'
            grnd_level = y['grnd_level'] if 'grnd_level' in y else 'N/A'

            data = f'𝐓𝐞𝐦𝐩𝐞𝐫𝐚𝐭𝐮𝐫𝐞_𝐌𝐢𝐧: {tmin}\
                \n𝐓𝐞𝐦𝐩𝐞𝐫𝐚𝐭𝐮𝐫𝐞_𝐌𝐚𝐱: {tmax}\
                \n𝐏𝐫𝐞𝐬𝐬𝐮𝐫𝐞: {pressure}\
                \n𝐇𝐮𝐦𝐢𝐝𝐢𝐭𝐲: {humidity}\
                \n𝐒𝐄𝐀_𝐋𝐞𝐯𝐞𝐥: {sea_level}\
                \n𝐆𝐑𝐍𝐃_𝐋𝐞𝐯𝐞𝐥: {grnd_level}'

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"{C}°C {weather_description.upper()}")
            msg.setInformativeText("                                                                                                                                                                                                                                                                                                                                                                                                       ")
            msg.setWindowTitle(f"{a} Weather Details")
            msg.setDetailedText(data)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()

        else:
            show_label = QMessageBox()
            show_label.setIcon(QMessageBox.Warning)
            show_label.setWindowTitle(f'{a} OOPS, Error!!')
            show_label.setText('City Not Found!')
            show_label.exec_() 


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())