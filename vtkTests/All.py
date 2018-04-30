
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
vertices = vtk.vtkCellArray()
lines = vtk.vtkCellArray()
polys = vtk.vtkCellArray()

vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid8)

vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid9)

# create some lines
line = vtk.vtkLine()
line.GetPointIds().SetId(0, pid0)
line.GetPointIds().SetId(1, pid9)
lines.InsertNextCell(line)

line.GetPointIds().SetId(0, pid3)
line.GetPointIds().SetId(1, pid10)
lines.InsertNextCell(line)

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

sphere = vtk.vtkSphereSource()
sphere.SetCenter(2, 2, 2)
sphere.SetRadius(1.0)
sp = sphere.GetOutputPort()
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)

sphere2 = vtk.vtkSphereSource()
sphere2.SetCenter(-2, -2, -2)
sphere2.SetRadius(1.5)
sp2 = sphere2.GetOutputPort()
sphere2.SetPhiResolution(100)
sphere2.SetThetaResolution(100)

elipse = vtk.vtkParametricEllipsoid()
elipse.SetXRadius(2)
elipse.SetYRadius(3)
elipse.SetZRadius(0.2)


elsource = vtk.vtkParametricFunctionSource()
elsource.SetParametricFunction(elipse)
elsource.Update()

# polys.InsertNextCell(sp)

# Create a polydata object
geodata = vtk.vtkPolyData()

# Set the points and vertices we created as the geometry and topology of the polydata
geodata.SetPoints(points)
geodata.SetVerts(vertices)
geodata.SetPolys(polys)
geodata.SetLines(lines)

geodata.GetPointData().SetScalars(colors)

# Visualize
mappergeo = vtk.vtkPolyDataMapper()
mappersp = vtk.vtkPolyDataMapper()
mappersp2 = vtk.vtkPolyDataMapper()
mapperel = vtk.vtkPolyDataMapper()
mappercont = vtk.vtkPolyDataMapper()


if vtk.VTK_MAJOR_VERSION <= 5:
    mappergeo.SetInput(geodata)
else:
    mappergeo.SetInputData(geodata)
    mappersp.SetInputConnection(sp)
    mappersp2.SetInputConnection(sp2)
    mapperel.SetInputConnection(elsource.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mappergeo)
actor.GetProperty().SetPointSize(5)
actor.GetProperty().VertexVisibilityOn()
actor.GetProperty().SetVertexColor([0,0,0])

actor2 = vtk.vtkActor()
actor2.SetMapper(mappersp)
actor2.GetProperty().SetColor([0, 0.5, 0.5])
actor.GetProperty().VertexVisibilityOn()
actor.GetProperty().SetVertexColor([0,0,0])

actor2b = vtk.vtkActor()
actor2b.SetMapper(mappersp2)
actor2b.GetProperty().SetColor([0.1, 0.5, 0.1])

actor3 = vtk.vtkActor()
actor3.SetMapper(mapperel)
actor3.SetPosition(1,4,6)


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
renderer.AddActor(actor2b)
renderer.AddActor(actor3)

renderWindow.Render()
renderWindowInteractor.Start()

