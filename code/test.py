import vtk
import SimpleITK as sitk
import time
from config import *

filename = '../data/truth.nii.gz'

def create_mask_extractor(reader):
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

if __name__ == '__main__':
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileNameSliceOffset(1)
    reader.SetDataByteOrderToBigEndian()
    reader.SetFileName(filename)
    reader.Update()

    # 2. 建图（将点拼接成立方体）
    extracter = create_mask_extractor(reader)
    cube_mapper = vtk.vtkPolyDataMapper()
    cube_mapper.SetInputConnection(extracter.GetOutputPort())

    # 3. 根据2创建执行单元
    cube_actor = vtk.vtkActor()
    cube_actor.SetMapper(cube_mapper)
    cube_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
    cube_actor.GetProperty().SetOpacity(1)
    # cube_actor.GetProperty().SetRepresentationToWireframe()

    # 4. 渲染（将执行单元和背景组合在一起按照某个视角绘制)
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0)#背景只有一个所以是Set()
    renderer.AddActor(cube_actor)#因为actor有可能为多个所以是add()

    # 5. 显示渲染窗口
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("My First Cube")
    render_window.SetSize(600,600)
    render_window.AddRenderer(renderer) # 渲染也会有可能有多个渲染把他们一起显示

    # 6. 创建交互控键（可以用鼠标拖来拖去看三维模型）
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)
    interactor.Initialize()
    render_window.Render()
    interactor.Start()