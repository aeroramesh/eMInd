import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from nodeeditor.node_editor_window import NodeEditorWindow


class eMindWindow(NodeEditorWindow):

    def __int__(self):
        super.__init__(parent)
        self.initUI()

    def initUI(self):
        self.name_company = 'SimTestLab'
        self.name_product = 'eMind'
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("eMind")


    def updateMenus(self):
        pass

    def createEditMenu(self):
        pass

    def setActiveSubWindow(self):
        pass

    def createNodesDock(self):
        self.nodesDock = QListWidget()
        self.nodesDock.addItem('Add')

        self.items = QDocWidget("Nodes")
        self.items.setWidget(self.nodesDock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")
        pass

