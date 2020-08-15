import vtk
from utils import VTKUtils
from config import *

if __name__ == '__main__':
    # file_name = '../data/truth.nii.gz'
    file_name = '../data/haha.nii.gz'
    vtk_utils = VTKUtils()

    # reader
    reader = vtk_utils.read_volume(file_name)

    # renderer
    renderer = vtk_utils.create_renderer()

    # mapper, actors
    n_labels = int(reader.GetOutput().GetScalarRange()[1])
    for idx in range(n_labels):
        extracter = vtk_utils.create_mask_extractor(reader)
        extracter.SetValue(0, idx+1)
        mapper = vtk_utils.create_mapper(extracter=extracter)
        prop = vtk_utils.create_property(opacity=MASK_OPACITY[idx], color=MASK_COLORS[idx])
        actor = vtk_utils.create_actor(mapper=mapper, prop=prop)
        renderer.AddActor(actor)

    # outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    outline.GenerateFacesOn()
    extracter = vtk_utils.create_mask_extractor(reader)
    mapper = vtk_utils.create_mapper(extracter=outline)
    prop = vtk_utils.create_property(opacity=OUTLINE_OPACITY, color=OUTLINE_COLOR)
    actor = vtk_utils.create_actor(mapper=mapper, prop=prop)
    renderer.AddActor(actor)
    
    # render window
    render_window = vtk_utils.create_renderwindow()
    render_window.AddRenderer(renderer)

    # interactor 
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()