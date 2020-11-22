import os
import sys
import inspect
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from nodeeditor.utils import loadStylesheet
from nodeeditor.node_editor_window import NodeEditorWindow


from eMindWindow import eMindWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = eMindWindow()

    wnd.show()


    sys.exit(app.exec_())