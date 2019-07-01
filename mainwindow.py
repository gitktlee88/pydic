from pydic import treeview as tv, openfileeditor as oe, dbase as db

from PyQt5.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, QAction, QMessageBox, QInputDialog, QWidget, )
from PyQt5.QtGui import (QIcon, )

class MainWindow(QMainWindow):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
    #def __init__(self, parent = None):
        #QMainWindow.__init__(self,parent)
        self.setWindowIcon(QIcon('icons/pig.png'))
        self.setWindowTitle('My Dictionary(PyQt5)')
        self.setGeometry(200, 200, 840, 500)

        _widget = QWidget()
        _layout = QVBoxLayout(_widget)   # or # _widget.setLayout(_layout)

        self.treeview = tv.TreeView()
        _layout.addWidget(self.treeview)


        #scroll = QScrollArea()
        #scroll.setWidgetResizable(True)  # Set to make the inner widget resize with scroll area
        #scroll.setWidget(_widget)

        self.initTools()

        self.setCentralWidget(_widget)


    def initTools(self):
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')

        newAction = QAction(QIcon(".\\pydic\\icons\\new.png"),"New",self) #"icons/new.png"
        newAction.setStatusTip("Create a new document from scratch.")
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.new)
        fileMenu.addAction(newAction)

        openAction = QAction(QIcon(".\\pydic\\icons\\opn.png"),"Open file",self)
        openAction.setStatusTip("Open existing document")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.open)
        fileMenu.addAction(openAction)

        exitButton = QAction(QIcon(".\\pydic\\icons\\ext.png"),"Exit",self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        #refreshMenu = mainMenu.addMenu('Refresh')

        #refreshButton = QAction(QIcon(".icons/refresh.png"),"Refresh",self)
        #refreshButton.setShortcut('Ctrl+R')
        #refreshButton.setStatusTip('Refresh treeview')
        #refreshButton.triggered.connect(self.refresh)
        #refreshMenu.addAction(refreshButton)

        searchMenu = mainMenu.addMenu('Search')

        searchButton = QAction(QIcon(".\\pydic\\icons\\search.png"),"search",self)
        searchButton.setShortcut('Ctrl+F')
        searchButton.setStatusTip('search on treeview')
        searchButton.triggered.connect(self.search)
        searchMenu.addAction(searchButton)

        helpMenu = mainMenu.addMenu('Help')

        aboutButton = QAction(QIcon(".\\pydic\\icons\\cock.png"),"about",self)
        aboutButton.setShortcut('Ctrl+H')
        aboutButton.setStatusTip('about the App')
        aboutButton.triggered.connect(self.about)
        helpMenu.addAction(aboutButton)

    def about(self):
        QMessageBox.about(self, "Message box", "This is a dictionary to add or update" \
        " a title & contents\n\n and also can open a file editor")

    def search(self):
        self.dbcon = db.DBase()
        text, result = QInputDialog.getText(self, "Search box !",
                                            "Type a keyword!")
        text = text.strip()
        if result:
            index = self.treeview.dataView.currentIndex()

            """
            # Find the top-level item in the tree.
            parent = index.parent()
            while parent.isValid():
                print(index)
                index = parent
                parent = parent.parent()
            """

            itemRow = index.row()
            #print(self.treeview.dataView.model.rowCount(index))

            #for i in range(10000):
            while True:
                indexOfColumn0 = index.model().index(itemRow, 0)
                #print(indexOfColumn0.model().itemFromIndex(indexOfColumn0).text(), text)
                try:
                    word = indexOfColumn0.model().itemFromIndex(indexOfColumn0).text()
                except AttributeError:
                    QMessageBox.about(self, "Message box", "Keyword = %s, not in the dictionary" % (text))
                    #print('error', sys.exc_info()[0])
                    break

                if text.upper() == word.upper():
                    #self.treeview.dataView.selectionModel().setCurrentIndex(indexOfColumn0, QItemSelectionModel.NoUpdate)
                    #print(self.treeview.w, indexOfColumn0)
                    descr = self.dbcon.queryDbase("SELECT descr FROM mydic.words WHERE word = '%s' " % (text))

                    if descr:
                        descr = descr[0][0]
                    else:
                        descr ='None'

                    if self.treeview.w:
                        self.treeview.w[0].destroy()
                        self.treeview.w.remove(self.treeview.w[0])

                    self.treeview.w.append(PopTreeEditor(word, descr, indexOfColumn0))
                    break

                itemRow += 1

    def new(self):
        if self.treeview.w:
            self.treeview.w[0].destroy()
            self.treeview.w.remove(self.treeview.w[0])

        #self.treeview.w = OpenFileEditor()
        self.treeview.w.append(oe.OpenFileEditor())


    def open(self):
        if self.treeview.w:
            self.treeview.w[0].destroy()
            self.treeview.w.remove(self.treeview.w[0])

        #self.treeview.w = OpenFileEditor('.writer')
        self.treeview.w.append(oe.OpenFileEditor('.writer'))
