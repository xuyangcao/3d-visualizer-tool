from PyQt5 import QtCore
import PyQt5.QtWidgets as QtWidgets

class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, ):
        QtWidgets.QDialog.__init__(self, None)
        self.setWindowTitle("Preference")