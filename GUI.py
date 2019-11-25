from PyQt5.QtWidgets import (QWidget, QPushButton, QInputDialog, QApplication)
import spider
import sys

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.btn = QPushButton('爬取', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('实习僧 爬虫')
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        '输入想要爬取的页数')

        if ok:
            spider.build_url(int(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
