from pydic import dbase as db

from PyQt5.QtWidgets import (QMainWindow, QWidget, QLineEdit, QTextEdit, QVBoxLayout, QAction, QMessageBox, )
from PyQt5.QtGui import (QIcon, )#QFont, QTextListFormat, )

class PopTreeEditor(QMainWindow):

    def __init__(self, wkey, descr, model_index, parent = None):
        QMainWindow.__init__(self, parent)

        self.initUI(wkey, descr)
        self.wkey = wkey
        self.model_index = model_index
        self.dbcon = db.DBase()
        #print(self.model_index.row())
    def initUI(self, wkey, descr):

        # main button
        self.wkeytxt = QLineEdit(self)
        self.wkeytxt.setText(wkey)
        self.wkeytxt.setObjectName('msgtext')
        self.wkeytxt.setStyleSheet("#msgtext {background-color: Aliceblue; color: blue; font-size: 12pt; }")
        #self.wkeytxt.resize(20,20)
        #self.wkeytxt.triggered.connect(self.wkeyClicked)

        # text edit
        self.text = QTextEdit(self)
        self.text.setText(descr)
        self.text.setObjectName('msgtext')
        self.text.setStyleSheet("#msgtext {background-color: Aliceblue; color: black; font-size: 9pt; }")
        #self.text.resize(1010,770)
        self.text.cursorPositionChanged.connect(self.cursorPosition)

        # main layout
        self.mainLayout = QVBoxLayout()

        # add all main to the main vLayout
        self.mainLayout.addWidget(self.wkeytxt)
        self.mainLayout.addWidget(self.text)

        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        # Initialize a statusbar for the window
        self.statusbar = self.statusBar()

        # x and y coordinates on the screen, width, height
        self.setGeometry(100,30,1030,800)
        self.setWindowTitle('PyDic editor')
        self.show()


    def initToolbar(self):
        #self.updateAction = QAction(QIcon(".icons/update.png"), "update", self)
        self.updateAction = QAction(QIcon(".\\pydic\\icons\\update.png"), "update", self)
        self.updateAction.setStatusTip("update DB")
        self.updateAction.setShortcut("Ctrl+U")
        self.updateAction.triggered.connect(self.update)

        self.deleteAction = QAction(QIcon(".\\pydic\\icons\\delete.png"), "delete", self)
        self.deleteAction.setStatusTip("delete a word")
        self.deleteAction.setShortcut("Ctrl+D")
        self.deleteAction.triggered.connect(self.delete)

        self.exitButton = QAction(QIcon(".\\pydic\\icons\\ext.png"),"Exit",self)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip('Exit application')
        self.exitButton.triggered.connect(self.close)


        self.cutAction = QAction(QIcon(".\\pydic\\icons\\cut.png"),"Cut to clipboard",self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl+X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QAction(QIcon(".\\pydic\\icons\\cop.png"),"Copy to clipboard",self)
        self.copyAction.setStatusTip("Copy text to clipboard")
        self.copyAction.setShortcut("Ctrl+C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QAction(QIcon(".\\pydic\\icons\\paste.png"),"Paste from clipboard",self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl+V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QAction(QIcon(".\\pydic\\icons\\undo.png"),"Undo last action",self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QAction(QIcon(".\\pydic\\icons\\redo.png"),"Redo last undone thing",self)
        self.redoAction.setStatusTip("Redo last undone thing")
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.text.redo)
        """
        bulletAction = QAction(QIcon(".icons/bul.png"),"Insert bullet List",self)
        bulletAction.setStatusTip("Insert bullet list")
        bulletAction.setShortcut("Ctrl+Shift+B")
        bulletAction.triggered.connect(self.bulletList)
        numberedAction = QAction(QIcon(".icons/num.png"),"Insert numbered List",self)
        numberedAction.setStatusTip("Insert numbered list")
        numberedAction.setShortcut("Ctrl+Shift+L")
        numberedAction.triggered.connect(self.numberList)
        """
        self.toolbar = self.addToolBar("Options")

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        #self.toolbar.addAction(bulletAction)
        #self.toolbar.addAction(numberedAction)

        self.toolbar.addSeparator()

        # Makes the next toolbar appear underneath this one
        self.addToolBarBreak()

    def initFormatbar(self):
        self.formatbar = self.addToolBar("Format")

    def initMenubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        #file.addAction(self.newAction)
        #file.addAction(self.openAction)
        file.addAction(self.updateAction)
        file.addAction(self.deleteAction)
        file.addAction(self.exitButton)

        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)


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

    def delete(self):
        choice = QMessageBox.question(self, 'Confirmation!',
                                        " Really!\n\nDelete now?",
                                        QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            pass
        else:
            return

        if self.wkeytxt.text():
            sql = """DELETE FROM mydic.words WHERE word=%s""" % (repr(self.wkeytxt.text()))

            self.dbcon.updateDbase(sql)
            #self.msgbox('delete')
            self.close()

            self.model_index.model().removeRow(self.model_index.row())


    def update(self):
        #cursor = self.text.textCursor()
        #textSelected = cursor.selectedText()
        textSelectAll = self.text.toPlainText()
        textSelectAll = repr(textSelectAll.replace("\u2029","\n"))

        if  self.wkey == self.wkeytxt.text():   # update
            sql = """UPDATE mydic.words SET descr=%s WHERE word=%s""" % (textSelectAll, repr(self.wkeytxt.text()) )

            self.dbcon.updateDbase(sql)
            self.msgbox('update')

        elif self.wkeytxt.text():                            # add new
            #print('add new', self.wkeytxt.text(), self.wkey)
            sql = """INSERT INTO mydic.words (word, descr) VALUES (%s, %s)""" % (repr(self.wkeytxt.text()), textSelectAll)

            self.dbcon.updateDbase(sql)

            parentmodel = self.model_index.model()
            parentmodel.insertRow(0)
            parentmodel.setData(parentmodel.index(0, 0), self.wkeytxt.text())
            parentmodel.setData(parentmodel.index(0, 1), textSelectAll)
            #parentmodel.endResetModel()
            self.msgbox('insert')

    def msgbox(self, action):
        choice = QMessageBox.question(self, action+' completed!',
                                        action + " completed!\n\nClose the Editor now?",
                                        QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            #print("Extracting Naaaaaaoooww!!!!")
            self.close()
        else:
            self.wkeytxt.clear()
            self.text.clear()

        #need refresh the original treeview after DB change
        #print(self.treeIndex)
        #
