import vtk
from vtk_utils import * 
from config import *

if __name__ == '__main__':
    # configs
    show_axes = True
    show_outline = True
    generate_outline_face = True
    # file_name = '../data/truth.nii.gz'
    file_name = '../data/0001_RLAT.nii.gz'

    # reader
    reader = read_volume(file_name)

    # transform
    mask_transform = vtk.vtkTransform()
    mask_transform.PostMultiply()
    mask_transform.RotateX(ROTATE_X) # rotate
    mask_transform.RotateY(ROTATE_Y)
    mask_transform.RotateZ(ROTATE_Z)
    mask_transform.Scale(SCALE) # scale

    # renderer and render window
    renderer = create_renderer(bg_color=RENDERER_BG_COLOR)
    render_window = create_renderwindow()
    render_window.AddRenderer(renderer)

    # mapper and actors for segmentation results
    n_labels = int(reader.GetOutput().GetScalarRange()[1])
    for idx in range(n_labels):
        extracter = create_mask_extractor(reader) # extracter
        extracter.SetValue(0, idx+1)
        smoother = create_smoother(extracter, SMOOTH_FACTOR) # smoother
        mapper = create_mapper(stripper=smoother)
        prop = create_property(opacity=MASK_OPACITY[idx], color=MASK_COLORS[idx]) # property
        actor = create_actor(mapper=mapper, prop=prop) # actor
        actor.SetUserTransform(mask_transform)
        renderer.AddActor(actor)

    # outline of the whole image
    if show_outline:
        outline = vtk.vtkOutlineFilter() # show outline
        outline.SetInputConnection(reader.GetOutputPort())
        if generate_outline_face: # show surface of the outline
            outline.GenerateFacesOn()
        extracter = create_mask_extractor(reader)
        mapper = create_mapper(stripper=outline)
        prop = create_property(opacity=OUTLINE_OPACITY, color=OUTLINE_COLOR)
        actor = create_actor(mapper=mapper, prop=prop)
        actor.SetUserTransform(mask_transform)
        renderer.AddActor(actor)

    # show axes for better visualization
    if show_axes:
        axes_actor = vtk.vtkAxesActor()
        axes_actor.SetTotalLength(TOTAL_LENGTH[0], TOTAL_LENGTH[1], TOTAL_LENGTH[2]) # set axes length
        renderer.AddActor(axes_actor)
    
    # interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()