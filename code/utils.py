import vtk
from config import *
import SimpleITK as sitk
import numpy as np

class VTKUtils():
    def __init__(self, ):
        pass

    def read_volume(self, file_name):
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileNameSliceOffset(1)
        reader.SetDataByteOrderToBigEndian()
        reader.SetFileName(file_name)
        reader.Update()
        return reader

    def create_mask_extractor(self, reader):
        """
        Given the output from mask (vtkNIFTIImageReader) extract it into 3D using
        vtkDiscreteMarchingCubes algorithm (https://www.vtk.org/doc/release/5.0/html/a01331.html).
        This algorithm is specialized for reading segmented volume labels.
        :param mask: a vtkNIFTIImageReader volume containing the mask
        :return: the extracted volume from vtkDiscreteMarchingCubes
        """
        mask_extractor = vtk.vtkDiscreteMarchingCubes()
        mask_extractor.SetInputConnection(reader.GetOutputPort())
        return mask_extractor
    
    def create_mapper(self, extracter):
        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(extracter.GetOutputPort())
        cube_mapper.ScalarVisibilityOff()
        return cube_mapper


    def create_property(self, opacity=0.9, color=(1.0, 0.0, 0.0)):
        prop = vtk.vtkProperty()
        prop.SetColor(color[0], color[1], color[2])
        prop.SetOpacity(opacity)
        # prop.SetRepresentationToWireframe()
        return prop
    
    def create_actor(self, mapper, prop):
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetProperty(prop)
        return actor

    def create_renderer(self, ):
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(1.0, 1.0, 1.0)
        return renderer

    def create_renderwindow(self, window_name=APPLICATION_TITLE, window_size=(600, 600)):
        render_window = vtk.vtkRenderWindow()
        render_window.SetWindowName(window_name)
        render_window.SetSize(window_size[0], window_size[1])
        return render_window


if __name__ == '__main__':
    file_name = '../data/haha.nii.gz'
    img = sitk.ReadImage(file_name)
    volume = sitk.GetArrayFromImage(img)
    volume[volume != 0] = 1
    volume = volume.astype(np.int8)
    volume += 1
    img = sitk.GetImageFromArray(volume)
    sitk.WriteImage(img, '../data/haha_with_bg.nii.gz')  