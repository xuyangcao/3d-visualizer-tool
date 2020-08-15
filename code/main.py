import sys
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as Qt
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from config import *
from vtk_utils import *

class MainWindow(QtWidgets.QMainWindow, QtWidgets.QApplication):
    def __init__(self, app):
        self.app = app
        QtWidgets.QMainWindow.__init__(self, None)
        # base setup
        self.frame, self.vtk_widget, self.renderer, self.render_window, self.interactor = self.setup()
        
        # create grid for all the widgets
        self.grid = QtWidgets.QGridLayout()

        # add widgets to the grid
        self.add_menubar()
        self.add_main_toolbar(row=0, col=0)
        self.add_views_widget(row=1, col=0)
        self.add_vtk_window_widget(row=0, col=1, row_span=3, col_span=3)

        # set layout and show
        # self.render_window.Render()
        self.setWindowTitle(APPLICATION_TITLE)
        self.frame.setLayout(self.grid)
        self.setCentralWidget(self.frame)
        # self.interactor.Initialize()
        self.show()

    @staticmethod
    def setup():
        # Qt
        frame = QtWidgets.QFrame()
        frame.setAutoFillBackground(True)

        # vtk 
        vtk_widget = QVTKRenderWindowInteractor()
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(RENDERER_BG_COLOR[0], RENDERER_BG_COLOR[1], RENDERER_BG_COLOR[2])
        vtk_widget.GetRenderWindow().AddRenderer(renderer)

        render_window = vtk_widget.GetRenderWindow()
        render_window.AddRenderer(renderer)

        interactor = vtk_widget.GetRenderWindow().GetInteractor()
        interactor.SetRenderWindow(render_window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        return frame, vtk_widget, renderer, render_window, interactor

    def add_menubar(self, ):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        open_file_action = QtWidgets.QAction("Open", self)
        open_file_action.setShortcut("Ctrl+o")
        open_file_action.setStatusTip('Open new File')
        open_file_action.triggered.connect(self.open_file)

        file_menu.addAction(open_file_action)

    def open_file(self, ):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '../data')
        if file_name[0].split('.')[-1] == 'gz':
            self.setup_mask(self.renderer, file_name[0])            
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "file type invalid!")

    def setup_mask(self, renderer, file_name):
        # reader
        reader = read_volume(file_name)

        # transform
        mask_transform = vtk.vtkTransform()
        mask_transform.PostMultiply()
        mask_transform.RotateX(ROTATE_X) # rotate
        mask_transform.RotateY(ROTATE_Y)
        mask_transform.RotateZ(ROTATE_Z)
        mask_transform.Scale(SCALE) # scale

        # mapper and actors for segmentation results
        n_labels = int(reader.GetOutput().GetScalarRange()[1])
        for idx in range(n_labels):
            extracter = create_mask_extractor(reader) # extracter
            extracter.SetValue(0, idx+1)
            smoother = create_smoother(extracter, SMOOTH_FACTOR) # smoother
            mapper = create_mapper(stripper=extracter)
            prop = create_property(opacity=MASK_OPACITY[idx], color=MASK_COLORS[idx]) # property
            actor = create_actor(mapper=mapper, prop=prop) # actor
            actor.SetUserTransform(mask_transform)
            renderer.AddActor(actor)

        # outline of the whole image
        outline = vtk.vtkOutlineFilter() # show outline
        outline.SetInputConnection(reader.GetOutputPort())
        outline.GenerateFacesOn()
        extracter = create_mask_extractor(reader)
        mapper = create_mapper(stripper=outline)
        prop = create_property(opacity=OUTLINE_OPACITY, color=OUTLINE_COLOR)
        actor = create_actor(mapper=mapper, prop=prop)
        actor.SetUserTransform(mask_transform)
        renderer.AddActor(actor)

        # show axes for better visualization
        axes_actor = vtk.vtkAxesActor()
        axes_actor.SetTotalLength(TOTAL_LENGTH[0], TOTAL_LENGTH[1], TOTAL_LENGTH[2]) # set axes length
        renderer.AddActor(axes_actor)

        self.render_window.Render()
        self.interactor.Initialize()

    def add_main_toolbar(self, row, col):
        toolbar_box = QtWidgets.QGroupBox("Main Toolbar")
        self.grid.addWidget(toolbar_box, row, col)

    def add_vtk_window_widget(self, row, col, row_span, col_span):
        object_layout = QtWidgets.QVBoxLayout()
        object_layout.addWidget(self.vtk_widget)

        object_group_box = QtWidgets.QGroupBox("Image")
        object_group_box.setLayout(object_layout)
        self.grid.addWidget(object_group_box, row, col, row_span, col_span)

        # must manually set column width for vtk_widget to maintain height:width ratio
        self.grid.setColumnMinimumWidth(col, MIN_IMG_WINDOW_WIDTH)

    def add_views_widget(self, row, col):
        axial_view = QtWidgets.QPushButton("Axial")
        coronal_view = QtWidgets.QPushButton("Coronal")
        sagittal_view = QtWidgets.QPushButton("Sagittal")
        
        views_box_layout = QtWidgets.QVBoxLayout()
        views_box_layout.addWidget(axial_view)
        views_box_layout.addWidget(coronal_view)
        views_box_layout.addWidget(sagittal_view)

        views_box = QtWidgets.QGroupBox("Views")
        views_box.setLayout(views_box_layout)

        self.grid.addWidget(views_box, row, col)

        # axial_view.clicked.connect(self.set_axial_view)
        # coronal_view.clicked.connect(self.set_coronal_view)
        # sagittal_view.clicked.connect(self.set_sagittal_view)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    sys.exit(app.exec_())