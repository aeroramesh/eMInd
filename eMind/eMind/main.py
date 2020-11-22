import os
import sys
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from eMind_window import eMindWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = eMindWindow()
    wnd.show()

    sys.exit(app.exec_())
