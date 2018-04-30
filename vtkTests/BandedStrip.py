import vtk
import numpy as np

nx = 101
ny = 11

x = np.linspace(0,100,nx)
y = np.linspace(0,10,ny)

points = vtk.vtkPoints()
points2 = vtk.vtkPoints()

polys = vtk.vtkCellArray()
polys2 = vtk.vtkCellArray()

temps = vtk.vtkFloatArray()
temps.SetNumberOfComponents(1)
temps.SetName("Temps")

# temps2 = vtk.vtkFloatArray()
# temps2.SetNumberOfComponents(1)
# temps2.SetName("Temps2")


for j in range(0, ny-1):
    for i in range(0, nx-1):
        p1 = [x[i], y[j], 0]
        p2 = [x[i], y[j+1], 0]
        p3 = [x[i+1], y[j+1], 0]
        p4 = [x[i+1], y[j], 0]

        p12 = [x[i], y[j]+12, 0]
        p22 = [x[i], y[j+1]+12, 0]
        p32 = [x[i+1], y[j+1]+12, 0]
        p42 = [x[i+1], y[j]+12, 0]

        temps.InsertNextTypedTuple([x[i]])
        temps.InsertNextTypedTuple([x[i]])
        temps.InsertNextTypedTuple([x[i+1]])
        temps.InsertNextTypedTuple([x[i+1]])

        # temps2.InsertNextTypedTuple([x[i]])
        # temps2.InsertNextTypedTuple([x[i]])
        # temps2.InsertNextTypedTuple([x[i+1]])
        # temps2.InsertNextTypedTuple([x[i+1]])

        pid1 = points.InsertNextPoint(p1)
        pid2 = points.InsertNextPoint(p2)
        pid3 = points.InsertNextPoint(p3)
        pid4 = points.InsertNextPoint(p4)

        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, pid1)
        quad.GetPointIds().SetId(1, pid2)
        quad.GetPointIds().SetId(2, pid3)
        quad.GetPointIds().SetId(3, pid4)

        polys.InsertNextCell(quad)

        # pid1 = points2.InsertNextPoint(p12)
        # pid2 = points2.InsertNextPoint(p22)
        # pid3 = points2.InsertNextPoint(p32)
        # pid4 = points2.InsertNextPoint(p42)
        #
        # quad = vtk.vtkQuad()
        # quad.GetPointIds().SetId(0, pid1)
        # quad.GetPointIds().SetId(1, pid2)
        # quad.GetPointIds().SetId(2, pid3)
        # quad.GetPointIds().SetId(3, pid4)
        #
        # polys2.InsertNextCell(quad)


geodata = vtk.vtkPolyData()
geodata.SetPoints(points)
geodata.SetPolys(polys)
geodata.GetPointData().SetScalars(temps)

mappergeo = vtk.vtkPolyDataMapper()
mappergeo.SetScalarRange(0,100)

# geodata2 = vtk.vtkPolyData()
# geodata2.SetPoints(points2)
# geodata2.SetPolys(polys2)
# geodata2.GetPointData().SetScalars(temps2)

# contour = vtk.vtkBandedPolyDataContourFilter()
# contour.SetInputData(geodata2)
# zmin, zmax = geodata2.GetScalarRange()
# contour.SetNumberOfContours(10)
# contour.GenerateValues(10, zmin, zmax)
# contour.SetScalarModeToValue()
# contour.GenerateContourEdgesOn()
# contour.ClippingOn()
# contour.Update()
#
# mappergeo2 = vtk.vtkPolyDataMapper()
# mappergeo2.SetScalarRange(0, 100)

if vtk.VTK_MAJOR_VERSION <= 5:
    mappergeo.SetInput(geodata)
else:
    mappergeo.SetInputData(geodata)
    # mappergeo2.SetInputConnection(contour.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mappergeo)

# actor2 = vtk.vtkActor()
# actor2.SetMapper(mappergeo2)


renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

WIDTH = 640
HEIGHT = 480
renderWindow.SetSize(WIDTH, HEIGHT)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.SetBackground(.9, .9, .9)

renderer.AddActor(actor)
# renderer.AddActor(actor2)

renderWindow.Render()
renderWindowInteractor.Start()
