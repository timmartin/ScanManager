import sys
import os

from PySide import QtCore, QtGui


class ImageModel(QtCore.QAbstractListModel):
    def __init__(self, directory, parent=None):
        super(ImageModel, self).__init__(parent)

        self.imageNames = [name
                           for name in os.listdir(directory)
                           if os.path.isfile(os.path.join(directory, name))
                           and name.endswith('.JPG')]
        self.pixmaps = {}

        for imageName in self.imageNames:
            pixmap = QtGui.QPixmap()
            if not pixmap.load(os.path.join(directory, imageName)):
                raise Exception("Couldn't load image %s" % imageName)
            self.pixmaps[imageName] = pixmap

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.imageNames[index.row()]
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(self.pixmaps[self.imageNames[index.row()]].scaled(400,
                                                                                 400,
                                                                                 QtCore.Qt.KeepAspectRatio,
                                                                                 QtCore.Qt.SmoothTransformation))

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.imageNames)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.imageList = QtGui.QListView()
        self.imageList.setFlow(QtGui.QListView.LeftToRight)
        self.imageList.setWrapping(True)
        self.imageList.setResizeMode(QtGui.QListView.Adjust)
        self.imageList.setIconSize(QtCore.QSize(100, 100))
        self.imageList.setGridSize(QtCore.QSize(200, 100))
        
        self.setCentralWidget(self.imageList)

        self.openAct = QtGui.QAction("&Open", self, triggered=self.newDirectory)
        
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.menuBar().addMenu(self.fileMenu)

    def newDirectory(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self,
                                                           "Choose a directory",
                                                           os.path.expanduser("~"),
                                                           QtGui.QFileDialog.ShowDirsOnly)
        self.imageModel = ImageModel(directory)
        self.imageList.setModel(self.imageModel)

        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())