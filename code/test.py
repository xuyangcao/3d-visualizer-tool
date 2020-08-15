import vtk
import SimpleITK as sitk
import time
from config import *


class VTKInstance():
    def __init__(self, ):
        self.file_name = None
        self.reader = None
        self.maskes = []
        self.image_mapper = None
        self.scalar_range = None

class VTKMask():
    def __init__(self, color, opacity, smooth_factor):
        self.actor = None
        self.property = None
        self.smoother = None
        self.color = color
        self.opacity = opacity
        self.smooth_factor = smooth_factor

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

    def create_property(self, opacity=0.9, color=(1.0, 0.0, 0.0)):
        prop = vtk.vtkProperty()
        prop.SetColor(color[0], color[1], color[2])
        prop.SetOpacity(opacity)
        prop.SetRepresentationToSurface()
        return prop


if __name__ == '__main__':
    filename = '../data/truth.nii.gz'
    vtk_utils = VTKUtils()

    # reader
    reader = vtk_utils.read_volume(filename)

    # n_labels = int(reader.GetOutput().GetScalarRange()[1])
    # for idx in range(n_labels):

    #     mask.labels.append(VTKLabel(MASK_COLORS[label_idx], MASK_OPACITY, MASK_SMOOTH_FACTOR))
    #     mask.labels[label_idx].extractor = create_mask_extractor(mask)
    #     add_surface_rendering(mask, label_idx, label_idx + 1)
    #     renderer.AddActor(mask.labels[label_idx].actor)


    extracter = vtk_utils.create_mask_extractor(reader)
    # extracter.SetValue()


    # 2. 建图（将点拼接成立方体）
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(extracter.GetOutputPort())
    cube_mapper.ScalarVisibilityOff()

    # 3. 根据2创建执行单元
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    prop = vtk_utils.create_property()
    cube_actor.SetProperty(prop)

    # 4. 渲染（将执行单元和背景组合在一起按照某个视角绘制)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0) #背景只有一个所以是Set()
    renderer.AddActor(cube_actor) #因为actor有可能为多个所以是add()

    # 5. 显示渲染窗口
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("3D Visualizer Tool")
    render_window.SetSize(600,600)
    render_window.AddRenderer(renderer) # 渲染也会有可能有多个渲染把他们一起显示

    # 6. 创建交互控键（可以用鼠标拖来拖去看三维模型）
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()