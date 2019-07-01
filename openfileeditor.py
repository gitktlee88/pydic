
from PyQt5.QtWidgets import (QMainWindow, QWidget, QTextEdit, QAction, QFileDialog, QFontDialog, )
from PyQt5.QtGui import (QIcon, QTextListFormat, QFont)
#from PyQt5.QtCore import (QRect, )

class OpenFileEditor(QMainWindow):

    def __init__(self, fname=None):
        QMainWindow.__init__(self)
        self.fname = fname
        self.initUI()

    def initUI(self):
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)
        self.text.setText("")

        self.text.setObjectName('msgtext')
        self.text.setStyleSheet("#msgtext {background-color: Aliceblue; color: black; font-size: 12pt; }")

        #self.setWindowIcon(QIcon(".icons/icon.png"))
        #self.text.cursorPositionChanged.connect(self.cursorPosition)

        self.saveAction = QAction(QIcon(".\\pydic\\icons\\sav.png"), "Save", self)
        self.saveAction.setStatusTip("Save document")
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.fontChoice = QAction("Font",self) #".icons/new.png"
        self.fontChoice.setStatusTip("Font.")
        #self.newAction.setShortcut("Ctrl+N")
        self.fontChoice.triggered.connect(self.font_choice)

        bulletAction = QAction(QIcon(".\\pydic\\icons\\bul.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)

        numberedAction = QAction(QIcon(".\\pydic\\icons\\num.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)

        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.fontChoice)
        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)


        self.toolbar.addSeparator()

        # Makes the next toolbar appear underneath this one
        #self.addToolBarBreak()

        #self.initFormatbar()


        # Initialize a statusbar for the window
        #self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)
        self.setWindowTitle('PyDic editor')
        self.show()

        if self.fname:
            self.fileopn()

    def cursorPosition(self):
        cursor = self.text.textCursor()
        # Mortals like 1-indexed things
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()

        self.statusbar.showMessage("Line: {} | Column: {}".format(line,col))

    def bulletList(self):
        cursor = self.text.textCursor()
        # Insert bulleted list
        cursor.insertList(QTextListFormat.ListDisc)

    def numberList(self):
        cursor = self.text.textCursor()
        # Insert list with numbers
        cursor.insertList(QTextListFormat.ListDecimal)


    def initFormatbar(self):
        self.formatbar = self.addToolBar("Format")

    def fileopn(self):
        # getOpenFileName is now the new name for getOpenFileNameAndFilter, which returns
        # a tuple (filename, selected filter).
        # Thus to get the filename, you need the first element of the tuple:
        self.filename = QFileDialog.getOpenFileName(self, 'Open File',".","(*.*)")[0]

        if self.filename:
            with open(self.filename,"rt") as file:
                self.text.setText(file.read())

    def new(self):
        pass

    def save(self):
        # Only open dialog if there is no filename yet
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]  # it returns tuple
        #if not self.filename:
            #self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]  # it returns tuple

        # Append extension if not there yet
        if not self.filename.endswith(".writer"):
            self.filename += ".writer"

        # We just store the contents of the text file along with the
        # format in html, which Qt does in a very nice way for us
        with open(self.filename,"wt") as file:
            file.write(self.text.toHtml())

    def font_choice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.text.setCurrentFont(font)
