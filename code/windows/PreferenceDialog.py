from PyQt5 import QtCore
from PyQt5 import QtGui
import PyQt5.QtWidgets as QtWidgets

class PreferenceDialog(QtWidgets.QDialog):
    def __init__(self, ):
        QtWidgets.QDialog.__init__(self, None)
        self.init_UI()

    def init_UI(self, ):
        self.setWindowTitle("Preference")
        self.setWindowIcon(QtGui.QIcon('./resource/logo.png'))

        # general 
        # functional widgets->general widget->general tab->right stack->dialog widget (self)
        general_layout = self.set_general_layout()
        self.general = QtWidgets.QWidget()
        self.general.setLayout(general_layout)

        self.general_tab = QtWidgets.QTabWidget()
        self.general_tab.addTab(self.general, "General")

        # appearance 
        self.appearance = QtWidgets.QWidget()

        self.appearance_tab = QtWidgets.QTabWidget()
        self.appearance_tab.addTab(self.appearance, 'Appearance')

        # left list
        self.preference_list = QtWidgets.QListWidget()
        self.preference_list.insertItem(0, 'General')
        self.preference_list.insertItem(1, 'Appearance')
        self.preference_list.setMaximumWidth(150)
        self.preference_list.currentRowChanged.connect(self.display_stack)

        # right stack
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.general_tab)
        self.stack.addWidget(self.appearance_tab)
        self.stack.setMinimumWidth(600)
        self.stack.setMinimumHeight(500)

        # grid
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.preference_list, 0, 0)
        self.grid.addWidget(self.stack, 0, 1)

    def display_stack(self, i):
        self.stack.setCurrentIndex(i)
    
    def set_general_layout(self, ):
        but = QtWidgets.QPushButton('haha')
        layout = QtWidgets.QGridLayout()
        layout.addWidget(but)

        return layout
