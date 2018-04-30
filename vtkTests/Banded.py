
import vtk
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]

# Setup the colors array
colors = vtk.vtkUnsignedCharArray()
colors.SetNumberOfComponents(3)
colors.SetName("Colors")

# Add the colors we created to the colors array
colors.InsertNextTypedTuple(red)
colors.InsertNextTypedTuple(red)
colors.InsertNextTypedTuple(blue)
colors.InsertNextTypedTuple(blue)
colors.InsertNextTypedTuple(blue)
colors.InsertNextTypedTuple(green)
colors.InsertNextTypedTuple(green)
colors.InsertNextTypedTuple(green)
colors.InsertNextTypedTuple(red)
colors.InsertNextTypedTuple(blue)
colors.InsertNextTypedTuple(blue)
colors.InsertNextTypedTuple(green)

# Create the geometry of the points (the coordinate)

p0 = [0.0, 0.0, 0.0]
p1 = [1.0, 0.0, 0.0]
p2 = [1.0, 1.0, 0.0]
p3 = [0.0, 1.0, 0.0]

p4 = [0.0, 0.0, 1.0]
p5 = [1.0, 0.0, 1.0]
p6 = [1.0, 1.0, 0.0]
p7 = [0.0, 1.0, 0.0]

p8 = [0.0, 0.0, 0.0]
p9 = [1, 1.0, 1.0]
p10 = [1, 1.0, 2.0]

points = vtk.vtkPoints()
pid0 = points.InsertNextPoint(p0)
pid1 = points.InsertNextPoint(p1)
pid2 = points.InsertNextPoint(p2)
pid3 = points.InsertNextPoint(p3)
pid4 = points.InsertNextPoint(p4)
pid5 = points.InsertNextPoint(p5)
pid6 = points.InsertNextPoint(p6)
pid7 = points.InsertNextPoint(p7)
pid8 = points.InsertNextPoint(p8)
pid9 = points.InsertNextPoint(p9)
pid10 = points.InsertNextPoint(p10)

# Create the topology of the point (a vertex)
polys = vtk.vtkCellArray()

# create some triangles

tri = vtk.vtkTriangle()
tri.GetPointIds().SetId(0, pid0)
tri.GetPointIds().SetId(1, pid7)
tri.GetPointIds().SetId(2, pid9)

polys.InsertNextCell(tri)

# Create a quad on the four points
quad = vtk.vtkQuad()
quad.GetPointIds().SetId(0, pid0)
quad.GetPointIds().SetId(1, pid1)
quad.GetPointIds().SetId(2, pid2)
quad.GetPointIds().SetId(3, pid3)

quad2 = vtk.vtkQuad()
quad2.GetPointIds().SetId(0, pid4)
quad2.GetPointIds().SetId(1, pid5)
quad2.GetPointIds().SetId(2, pid6)
quad2.GetPointIds().SetId(3, pid7)

polys.InsertNextCell(quad)
polys.InsertNextCell(quad2)



# Create a polydata object
geodata = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and topology of the polydata
geodata.SetPoints(points)
geodata.SetPolys(polys)

# Setup the scalar array
temps = vtk.vtkUnsignedCharArray()
temps.SetNumberOfComponents(1)
temps.SetName("Temps")
red = [50]
green = [0]
blue = [100]
# Add the temps we created to the temps array
temps.InsertNextTypedTuple(red)
temps.InsertNextTypedTuple(red)
temps.InsertNextTypedTuple(blue)
temps.InsertNextTypedTuple(blue)
temps.InsertNextTypedTuple(blue)
temps.InsertNextTypedTuple(green)
temps.InsertNextTypedTuple(green)
temps.InsertNextTypedTuple(green)
temps.InsertNextTypedTuple(red)
temps.InsertNextTypedTuple(blue)
temps.InsertNextTypedTuple(blue)
temps.InsertNextTypedTuple(green)

s0 = [0.0, 0.0, 3.0]
s1 = [1.0, 0.0, 3.0]
s2 = [1.0, 1.0, 3.0]
s3 = [0.0, 1.0, 3.0]

s4 = [0.0, 0.0, 4.0]
s5 = [1.0, 0.0, 4.0]
s6 = [1.0, 1.0, 3.0]
s7 = [0.0, 1.0, 3.0]

s8 = [0.0, 0.0, 3.0]
s9 = [1, 1.0, 4.]
s10 = [1, 1.0, 5.0]

points2 = vtk.vtkPoints()
pid0 = points2.InsertNextPoint(s0)
pid1 = points2.InsertNextPoint(s1)
pid2 = points2.InsertNextPoint(s2)
pid3 = points2.InsertNextPoint(s3)
pid4 = points2.InsertNextPoint(s4)
pid5 = points2.InsertNextPoint(s5)
pid6 = points2.InsertNextPoint(s6)
pid7 = points2.InsertNextPoint(s7)
pid8 = points2.InsertNextPoint(s8)
pid9 = points2.InsertNextPoint(s9)
pid10 = points2.InsertNextPoint(s10)

# Create the topology of the point (a vertex)
polys2 = vtk.vtkCellArray()

# create some triangles

tri = vtk.vtkTriangle()
tri.GetPointIds().SetId(0, pid0)
tri.GetPointIds().SetId(1, pid7)
tri.GetPointIds().SetId(2, pid9)

polys2.InsertNextCell(tri)

# Create a quad on the four points
quad = vtk.vtkQuad()
quad.GetPointIds().SetId(0, pid0)
quad.GetPointIds().SetId(1, pid1)
quad.GetPointIds().SetId(2, pid2)
quad.GetPointIds().SetId(3, pid3)

quad2 = vtk.vtkQuad()
quad2.GetPointIds().SetId(0, pid4)
quad2.GetPointIds().SetId(1, pid5)
quad2.GetPointIds().SetId(2, pid6)
quad2.GetPointIds().SetId(3, pid7)

polys2.InsertNextCell(quad)
polys2.InsertNextCell(quad2)

# Create a polydata object
geodata = vtk.vtkPolyData()
geodata2 = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and topology of the polydata
geodata.SetPoints(points)
geodata.SetPolys(polys)
geodata.GetPointData().SetScalars(colors)

geodata2.SetPoints(points2)
geodata2.SetPolys(polys2)
geodata2.GetPointData().SetScalars(temps)

contour = vtk.vtkBandedPolyDataContourFilter()
contour.SetInputData(geodata2)
contour.GenerateValues(5, 0, 100)

# Visualize
mappergeo = vtk.vtkPolyDataMapper()
mappergeo2 = vtk.vtkPolyDataMapper()


if vtk.VTK_MAJOR_VERSION <= 5:
    mappergeo.SetInput(geodata)
else:
    mappergeo.SetInputData(geodata)
    mappergeo2.SetInputConnection(contour.GetOutputPort())


actor = vtk.vtkActor()
actor.SetMapper(mappergeo)

actor2 = vtk.vtkActor()
actor2.SetMapper(mappergeo2)


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
renderer.AddActor(actor2)

renderWindow.Render()
renderWindowInteractor.Start()

