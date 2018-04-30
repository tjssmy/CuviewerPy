#!/usr/bin/env python

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

# Create four points (must be in counter clockwise order)
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

# Add the points to a vtkPoints object
points = vtk.vtkPoints()
pid = points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)
points.InsertNextPoint(p4)
points.InsertNextPoint(p5)
points.InsertNextPoint(p6)
points.InsertNextPoint(p7)

# Create a quad on the four points
quad = vtk.vtkQuad()
quad.GetPointIds().SetId(0, 0)
quad.GetPointIds().SetId(1, 1)
quad.GetPointIds().SetId(2, 2)
quad.GetPointIds().SetId(3, 3)

quad2 = vtk.vtkQuad()
quad2.GetPointIds().SetId(0, 4)
quad2.GetPointIds().SetId(1, 5)
quad2.GetPointIds().SetId(2, 6)
quad2.GetPointIds().SetId(3, 7)

points.InsertNextPoint(p8)
pid = points.InsertNextPoint(p9)

line = vtk.vtkLine()
line.GetPointIds().SetId(0, 8)
line.GetPointIds().SetId(1, 9)

# Create a cell array to store the quad in
vertices = vtk.vtkCellArray()
lines = vtk.vtkCellArray()
quads = vtk.vtkCellArray()

vertices.InsertNextCell(1)
vertices.InsertCellPoint(pid)

lines.InsertNextCell(line)

quads.InsertNextCell(quad)
quads.InsertNextCell(quad2)



# Create a polydata to store everything in
polydata = vtk.vtkPolyData()

# Add the points and quads to the dataset
polydata.SetPoints(points)
# polydata.SetVerts(vertices)
polydata.SetPolys(quads)
polydata.SetLines(lines)
polydata.GetPointData().SetScalars(colors)

# Setup actor and mapper
mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(polydata)
else:
    mapper.SetInputData(polydata)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(20)

# Setup render window, renderer, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
WIDTH = 1640
HEIGHT = 1480
renderWindow.SetSize(WIDTH, HEIGHT)

renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)

renderWindow.Render()
renderWindowInteractor.Start()