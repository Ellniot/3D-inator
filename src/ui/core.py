from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys

class Window(QMainWindow):
    # create the main UI window
        def __init__(self):
            #TODO  not sure if all this is needed
            super().__init__()
            self.sourceWin = None
            self.info = ()
            self.element = ""
            title = "Rename: " + self.element
            self.setWindowTitle(title)

            self.title = 'Reto Film Camera 3D-Inator'
            self.left = 30
            self.top = 100
            self.width = 640
            self.height = 480
            self.initUI()
        
    # init the main UI window
        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            # set layout and add button
            layout = QtWidgets.QGridLayout()
            question = QtWidgets.QLabel("Please enter new name:")
            layout.addWidget(question, 0, 0)
            # self.lineEdit = QtWidgets.QLineEdit()
            # layout.addWidget(self.lineEdit, 0, 1)
            # self.buttonOK = QtWidgets.QPushButton("OK", self)
            # layout.addWidget(self.buttonOK, 1, 1)
            # self.buttonCancel = QtWidgets.QPushButton("Cancel", self)
            # layout.addWidget(self.buttonCancel, 1, 0)
            self.setLayout(layout)

            #self.buttonCancel.clicked.connect(self.cancelClicked)
            #self.buttonOK.clicked.connect(self.okClicked)

            

            # create the menues for the main window


            self.show()
            
            #open_one = self.openFileNameDialog()
            #open_multi = self.openFileNamesDialog()
            #save_file = self.saveFileDialog()

            
            # set the filenames on the screen
            #open_one_label = QLabel(self)
            #open_multi_label = QLabel(self)
            #save_file_label = QLabel(self)

            # set the labels' test
            #open_one_label.setText(open_one)
            #open_multi_label.setText("".join(open_multi))
            #save_file_label.setText(save_file)

            # set the labels' positions
            #open_one_label.move(50,20)
            #open_multi_label.move(50,50)
            #save_file_label.move(50,90)
            
            # make the labels stop clipping
            #open_one_label.adjustSize()
            #open_multi_label.adjustSize()
            #save_file_label.adjustSize()

            self.update()

        
        def openFileNameDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
                return fileName
            else:
                return ""
        
        def openFileNamesDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
            if files:
                print(files)
                return files
            else:
                return ""
        
        def saveFileDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
            if fileName:
                print(fileName)
                return fileName
            else:
                return ""
        
            # self.setGeometry(300, 300, 600, 400)
            # self.setWindowTitle("PyQt5 window")


            # # add file select window
            # self.show()

def main():
    # check input and env configs
    
    # open the main GUI - using PyQT5 lib
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

    # normalize the images' colors
    
    # center the images

    # crop the images

    # output the images
    return 0



if (__name__) == "__main__":
    main()
