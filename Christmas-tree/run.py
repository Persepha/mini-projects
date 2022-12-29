import sys
import ctypes
from PySide6 import QtCore, QtWidgets, QtGui


class Main(QtWidgets.QMainWindow):
    _gripSize = 8

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle("Xmas ")
        self.setWindowIcon(QtGui.QIcon('public/tree_ico.ico'))

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.widget = QtWidgets.QLabel()
        self.widget.setScaledContents(True)
        self.widget.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumSize(100, 100)

        self.movie = QtGui.QMovie("public/tree.gif")
        self.widget.setMovie(self.movie)
        self.movie.start()

        self.setCentralWidget(self.widget)


        self.cornerGrips = QtWidgets.QSizeGrip(self)

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        outRect = self.rect()

        inRect = outRect.adjusted(self.gripSize, self.gripSize,
            -self.gripSize, -self.gripSize)

        self.cornerGrips.setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))


    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()
        return super().resizeEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.oldPosition = event.globalPos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        delta = QtCore.QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
        return super().mouseMoveEvent(event)


if __name__ == "__main__":
    # fix taskbar ico on windowns
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QtWidgets.QApplication([])

    m = Main()
    m.show()
    
    sys.exit(app.exec())

