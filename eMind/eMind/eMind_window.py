import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow

from eMind_sub_window import CalculatorSubWindow
from eMind_drag_listbox import QDMDragListbox
from nodeeditor.utils import dumpException, pp
from eMind_conf import *

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import *
Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


# images for the dark skin
import qss.nodeeditor_dark_resources


DEBUG = False


class eMindWindow(NodeEditorWindow):

    def initUI(self):
        self.name_company = 'simTestLab'
        self.name_product = 'eMindGraph'

        self.stylesheet_filename = os.path.join(os.path.dirname(__file__), "qss/nodeeditor.qss")
        loadStylesheets(
            os.path.join(os.path.dirname(__file__), "qss/nodeeditor-dark.qss"),
            self.stylesheet_filename
        )

        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(CALC_NODES)


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
        self.createPropertyDock()

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.setUpIconToolBar()
        self.setUpToolBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("eMind -SimTestLab")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)


    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)


    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = CalculatorSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)


    def about(self):
        QMessageBox.about(self, "eMind from SimTestLab",
                "The <b>Calculator NodeEditor</b> example demonstrates how to write multiple "
                "document interface applications using PyQt5 and NodeEditor. For more information visit: "
                "<a href='https://www.blenderfreak.com/'>www.BlenderFreak.com</a>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)



    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()
        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.nodesDock)

    def createPropertyDock(self):
        #self.nodesListWidget = QDMDragListbox()
        self.PropEditor = QLineEdit()


        self.nodesDock = QDockWidget("Properties")
        self.nodesDock.setWidget(self.PropEditor)
        self.nodesDock.setFloating(False)


        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        # nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def setUpIconToolBar(self):
        self.icontoolbar = QToolBar('icon toolbar', self)

        m_signalMapper = QSignalMapper(self)

        system_users_action = QAction(QIcon('/icons/add.png'), 'System-users', self)
        system_users_action.triggered.connect(m_signalMapper.map)
        m_signalMapper.setMapping(system_users_action, '/icons/add.png')
        m_signalMapper.mapped[str].connect(self.dummyFunc)
        self.addToolBar(Qt.LeftToolBarArea, self.icontoolbar)
        self.icontoolbar.hide()

    def dummyFunc(self):
        print('Dummy pAss')

    def setUpToolBar(self):
        pass
        """
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        ###########################################################################
        #  New File
        ###########################################################################
        new_file_action = QAction(QIcon('images/filenew.png'), 'New File', self)
        new_file_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(new_file_action)

        ###########################################################################
        #  Save File
        ###########################################################################
        save_file_action = QAction(QIcon('images/filesave.png'), 'Save File', self)
        save_file_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(save_file_action)

        ###########################################################################
        #  Open File
        ###########################################################################
        open_file_action = QAction(QIcon('/images/fileopen.png'), 'Open File', self)
        open_file_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(open_file_action)

        ###########################################################################
        #  New Sibling Node
        ###########################################################################
        new_siblingNode_action = QAction(QIcon('/images/topicafter.svg'), 'topicafter', self)
        new_siblingNode_action.triggered.connect(self.dummyFunc)
        new_siblingNode_action.setShortcut('shift + enter')
        self.toolbar.addAction(new_siblingNode_action)

        ############################################################################
        #  New Son Node
        ############################################################################
        new_sonNode_action = QAction(QIcon('/images/subtopic.svg'), 'subtopic', self)
        new_sonNode_action.triggered.connect(self.dummyFunc)
        new_sonNode_action.setShortcut('TAB')
        self.toolbar.addAction(new_sonNode_action)

        ############################################################################
        #  Add Branch
        ############################################################################
        add_branch_action = QAction(QIcon('/images/relationship.svg'), 'relation', self)
        add_branch_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(add_branch_action)

        ############################################################################
        #  Add Notes
        ############################################################################
        add_notes_action = QAction(QIcon('/images/notes.svg'), 'note', self)
        add_notes_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(add_notes_action)

        ############################################################################
        #  Delete
        ############################################################################
        addBranch_action = QAction(QIcon('/images/delete.png'), 'Delete', self)
        addBranch_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(addBranch_action)

        ############################################################################
        #  undo
        #############################################################################
        self.undo_action.setIcon(QIcon('/images/undo.png'))
        self.toolbar.addAction(self.dummyFunc)

        ##############################################################################
        #  redo
        ##############################################################################
        self.redo_action.setIcon(QIcon('/images/redo.png'))
        self.toolbar.addAction(self.dummyFunc)

        self.scene.setUndoStack(self.dummyFunc)

        ############################################################################
        #  Generated Graph
        ############################################################################
        add_Graph_action = QAction(QIcon('/images/Graph.png'), 'GraphGen', self)
        add_Graph_action.triggered.connect(self.dummyFunc)
        self.toolbar.addAction(add_Graph_action) """