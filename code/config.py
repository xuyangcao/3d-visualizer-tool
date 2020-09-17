"""
GUI config
"""
# main window, only for Qt GUI
APPLICATION_TITLE = "3D Segmentation Visualizer"
MIN_IMG_WINDOW_WIDTH = 700


"""
VTK config
"""
# mask config
MASK_COLORS = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0.)
]
MASK_OPACITY = [0.9, 0.9, 0.9, 0.9]
SMOOTH_FACTOR = 50 
MAX_LABEL_LENGTH = 10

# renderer
COMPARE = False
RENDERER_BG_COLOR = (1., 1., 1.)

# outline config
SHOW_OUTLINE = True
OUTLINE_COLOR = (0, 1, 1)
OUTLINE_OPACITY = 0.2

# transform config
ROTATE_X = 110
ROTATE_Y = 20
ROTATE_Z = 5
SCALE = (0.5, 0.5, 0.5)

# axes config
SHOW_AXES = False
TOTAL_LENGTH = (30, 30, 30)
