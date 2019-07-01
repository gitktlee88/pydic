from pydic import dbase as db, poptreeeditor as pt

from PyQt5.QtWidgets import (QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QTreeView, )
from PyQt5.QtGui import (QStandardItemModel, )
from PyQt5.QtCore import (Qt, )

class TreeView(QWidget):

    FROM, SUBJECT = range(2)

    def __init__(self):
        #super(TreeView, self).__init__(parent)    # py 2.7
        super().__init__()      # Py 3.5

        self.w = []
        self.dataView = QTreeView()
        self.model = self.createListModel(self)

        self.initUI()


    def initUI(self):
        self.dataGroupBox = QGroupBox("Dictionary TreeView Box")
        self.dataGroupBox.setStyleSheet("font-size: 14px")
        #self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)


        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)

        self.dbcon = db.DBase()
        titles = self.dbcon.queryDbase( "SELECT * FROM mydic.words ORDER BY `word` DESC")

        #model = self.createListModel(self)
        self.dataView.setModel(self.model)

        for title in titles:
            #self.addList(model, title[0], (title[1].split('\n', 1)[0]) )   # this is same as below
            self.addList(self.model, title[0], (title[1].splitlines()[0]) )
            # 인코딩 알아내기
            #print (chardet.detect(title[1].splitlines()[0]) )

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.dataGroupBox)
        self.setLayout(mainLayout)

        self.dataView.doubleClicked.connect(self.dataView_doubleClicked)

    # QStandardItemModel
    def createListModel(self, parent):
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "Title")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Contents")
        return model

    def addList(self, model, tlist, content):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), tlist)
        model.setData(model.index(0, self.SUBJECT), content)

    def dataView_doubleClicked(self,index):
        self.dbcon = db.DBase()
        #print(index.row() ,index.column())
        #print (index.model().itemFromIndex(index).text())
        itemRow = index.row()
        indexOfColumn0 = index.model().index(itemRow, 0)
        #print (indexOfColumn0.model().itemFromIndex(indexOfColumn0).text())
        wkey = indexOfColumn0.model().itemFromIndex(indexOfColumn0).text()
        #print(index,indexOfColumn0)
        descr = self.dbcon.queryDbase("SELECT descr FROM mydic.words WHERE word = '%s' " % (wkey))

        if descr:
            descr = descr[0][0]
        else:
            descr ='None'

        if self.w:
            self.w[0].destroy()
            self.w.remove(self.w[0])

        self.w.append(pt.PopTreeEditor(wkey, descr, index))
