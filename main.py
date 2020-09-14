import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtTest
from PyQt5 import QtCore
import sys

fontBtn = QtGui.QFont("Saira", 10)
windowIcon = "images/mail.png"
windowBackground = "images/background.jpg"


class main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(750, 700)
        self.setWindowTitle("SMTP EMail Sender")
        self.setWindowIcon(QtGui.QIcon(windowIcon))

        #####################################################
        
        self.subject_email = QtWidgets.QLineEdit()
        self.subject_email.setFixedSize(200, 22)
        self.subject_email.setPlaceholderText("Subject")

        self.sender_email = QtWidgets.QLineEdit()
        self.sender_email.setFixedSize(200, 22)
        self.sender_email.setPlaceholderText("Sender")

        self.receiver_email = QtWidgets.QLineEdit()
        self.receiver_email.setFixedSize(200, 22)
        self.receiver_email.setPlaceholderText("Receiver")

        self.fileBtn = QtWidgets.QPushButton("File Browse...")
        self.fileBtn.setFont(fontBtn)
        self.fileBtn.clicked.connect(self.fileOpen)
        self.fileBtn.setFixedSize(200, 22)

        self.fileLabel = QtWidgets.QLabel("")
        self.fileLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.fileName = QtWidgets.QLineEdit()
        self.fileName.setFixedSize(200, 22)
        self.fileName.setPlaceholderText(
            "The file name that appears in For E-Mail")
        
        #####################################################

        self.domainName = QtWidgets.QLineEdit()
        self.domainName.setFixedSize(200, 22)
        self.domainName.setPlaceholderText("Domain (Forced!) ***")

        self.domainPort = QtWidgets.QLineEdit()
        self.domainPort.setFixedSize(200, 22)
        self.domainPort.setPlaceholderText("Domain Port (Forced!) ***")

        #####################################################

        self.email_text = QtWidgets.QTextEdit()
        self.email_text.setFixedSize(290, 650)
        self.email_text.setPlaceholderText(42*"\t" + "Text")
        self.email_text.setAlignment(QtCore.Qt.AlignCenter)

        #####################################################

        self.email_send_btn = QtWidgets.QPushButton("Send Mail")
        self.email_send_btn.setFixedSize(110, 22)
        self.email_send_btn.setFont(fontBtn)
        self.email_send_btn.clicked.connect(self.command)

        #####################################################

        horizontal1 = QtWidgets.QHBoxLayout()
        vertical1 = QtWidgets.QVBoxLayout()

        vertical1.addStretch()
        vertical1.addWidget(self.subject_email)
        vertical1.addWidget(self.sender_email)
        vertical1.addWidget(self.receiver_email)
        vertical1.addWidget(self.fileName)
        vertical1.addWidget(self.fileBtn)
        vertical1.addWidget(self.fileLabel)
        vertical1.addStretch()
        vertical1.addWidget(self.domainName)
        vertical1.addWidget(self.domainPort)
        vertical1.addStretch()

        horizontal1.addStretch()
        horizontal1.addLayout(vertical1)
        horizontal1.addStretch()

        horizontal2 = QtWidgets.QHBoxLayout()
        vertical2 = QtWidgets.QVBoxLayout()

        horizontal2.addStretch()
        horizontal2.addWidget(self.email_send_btn)
        horizontal2.addStretch()

        vertical2.addStretch()
        vertical2.addLayout(horizontal2)
        vertical2.addStretch()

        mainHorizontal = QtWidgets.QHBoxLayout()
        mainVertical = QtWidgets.QVBoxLayout()

        mainHorizontal.addStretch()
        mainHorizontal.addLayout(horizontal1)
        mainHorizontal.addStretch()
        mainHorizontal.addWidget(self.email_text)
        mainHorizontal.addStretch()
        mainHorizontal.addLayout(vertical2)
        mainHorizontal.addStretch()

        mainVertical.addStretch()
        mainVertical.addLayout(mainHorizontal)
        mainVertical.addStretch()

        oImage = QtGui.QImage(windowBackground)
        # resize Image to widgets size
        sImage = oImage.scaled(QtCore.QSize(750, 700))
        palette = QtGui.QPalette()
        # 10 = Windowrole
        palette.setBrush(10, QtGui.QBrush(sImage))

        self.setPalette(palette)
        self.setLayout(mainVertical)
        self.show()

    def fileOpen(self):
        filE = QtWidgets.QFileDialog.getOpenFileName(self, "Select File")
        self.filePath = filE[0]
        if len(self.filePath) > 0:
            self.fileLabel.setText("File Selected!")

    def command(self):
        try:
            sender_email = self.sender_email.text()
            receiver_email = self.receiver_email.text()

            message = MIMEMultipart("")
            message["Subject"] = self.subject_email.text()
            message["From"] = sender_email
            message["To"] = receiver_email

            text = self.email_text.toPlainText()

            part1 = MIMEText(text, "plain")
            message.attach(part1)

            filepath = self.filePath

            part2 = MIMEBase('application', "octet-stream")
            part2.set_payload(open(filepath, "rb").read())
            encoders.encode_base64(part2)

            fileName = self.fileName.text()
            part2.add_header('Content-Disposition',
                             f'attachment; filename = {fileName}')

            message.attach(part2)

            domain = self.domainName.text()
            domainPort = self.domainPort.text()

            context = ssl.create_default_context()
            server = smtplib.SMTP(domain, domainPort)
            server.starttls()
            server.ehlo_or_helo_if_needed()
            server.sendmail(sender_email, receiver_email, message.as_string())
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(
                self, "Hata!", "File Not Found!", QtWidgets.QMessageBox.Ok
            )
        except AttributeError:
            QtWidgets.QMessageBox.critical(
                self, "Hata!", "File Path Not Found!", QtWidgets.QMessageBox.Ok
            )


stylesheet = """
QPushButton{
    border: 3px solid transparent;
    border-radius: 5px;
    background-color: white;
}
QLineEdit{
    border: 3px solid transparent;
    border-radius: 5px;
    background-color white;
}
QTextEdit{
    border: 3px solid transparent;
    border-radius: 5px;
    background-color: white;
}
"""
app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(stylesheet)
mainWindow = main()
sys.exit(app.exec_())
