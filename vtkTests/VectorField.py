from numpy import *
import vtk


# write solution using VTK

def insertTriangle(Triangles, globalPointId):
    Triangle = vtk.vtkTriangle()
    Triangle.GetPointIds().SetId(0, globalPointId[0])
    Triangle.GetPointIds().SetId(1, globalPointId[1])
    Triangle.GetPointIds().SetId(2, globalPointId[2])
    Triangles.InsertNextCell(Triangle)

def insertQuad(Quads, globalPointId):
    quad = vtk.vtkQuad()
    quad.GetPointIds().SetId(0, globalPointId[0])
    quad.GetPointIds().SetId(1, globalPointId[1])
    quad.GetPointIds().SetId(2, globalPointId[2])
    quad.GetPointIds().SetId(3, globalPointId[3])
    Quads.InsertNextCell(quad)

def insertCell(Cell, nodes):
    for i in nodes:
        l = len(i)
        if(l==3): # triangle
            Triangle = vtk.vtkTriangle()
            Triangle.GetPointIds().SetId(0, i[0])
            Triangle.GetPointIds().SetId(1, i[1])
            Triangle.GetPointIds().SetId(2, i[2])
            Cell.InsertNextCell(Triangle)
        elif(l==4): # rectangle
            Quad = vtk.vtkQuad()
            Quad.GetPointIds().SetId(0, i[0])
            Quad.GetPointIds().SetId(1, i[1])
            Quad.GetPointIds().SetId(2, i[2])
            Quad.GetPointIds().SetId(3, i[3])
            Cell.InsertNextCell(Quad)


# points of square and triangle
pointsSq = array([[0,0,0],[1,0,0], [1,1,0], [0,1,0]])
pointsTri = array([[1,0,0], [2,1,0], [1,1,0]])
# nodes making up cells, one for square, the other for the triangle
nodesofCell = array([[0, 1, 2, 3], [4, 5, 6]])


#setup points and vertices
Points = vtk.vtkPoints()
Cells = vtk.vtkCellArray()
# using position vector instead of say,... velocity
for p in pointsSq:
    Points.InsertNextPoint(p)

for p in pointsTri:
    Points.InsertNextPoint(p)

insertCell(Cells, nodesofCell)

# points between edges
pointsHf = array([[0.5, 0, 0], [1, 0.5, 0],[0.5,1.,0], [0, 0.5,0], \
                  [1.5, 0.5, 0],[1.5,1,0]])

for p in pointsHf:
    Points.InsertNextPoint(p)

Solutions = vtk.vtkDoubleArray()
Solutions.SetNumberOfComponents(3)
Solutions.SetName("vec")

for s in pointsSq:
    Solutions.InsertNextTuple(s)

for s in pointsTri:
    Solutions.InsertNextTuple(s)

for s in pointsHf:
    Solutions.InsertNextTuple(s)

scalar = vtk.vtkDoubleArray()
scalar.SetNumberOfComponents(1)
scalar.SetName("scalar")

def scalarfunc(xyz):
    # some scalar field
    return xyz[0]**xyz[1] + xyz[2]

for s in pointsSq:
    scalar.InsertNextValue(scalarfunc(s))
for s in pointsTri:
    scalar.InsertNextValue(scalarfunc(s))
for s in pointsHf:
    scalar.InsertNextValue(scalarfunc(s))

polydata = vtk.vtkPolyData()
polydata.SetPoints(Points)
# polydata.SetPolys(Cells)
polydata.GetPointData().SetVectors(Solutions)
polydata.GetPointData().SetScalars(scalar)

# Source for the glyph filter
arrow = vtk.vtkArrowSource()
arrow.SetTipResolution(16)
arrow.SetTipLength(0.3)
arrow.SetTipRadius(0.1)

glyph = vtk.vtkGlyph3D()
glyph.SetSourceConnection(arrow.GetOutputPort())
glyph.AddInputData(polydata)
glyph.SetVectorModeToUseVector()
glyph.SetScaleFactor(.1)
glyph.SetColorModeToColorByVector()
glyph.SetScaleModeToScaleByVector()
glyph.OrientOn()
glyph.Update()

# mappergeo = vtk.vtkPolyDataMapper()
# mappergeo.SetScalarRange(0,100)

# if vtk.VTK_MAJOR_VERSION <= 5:
#     # mappergeo.SetInput(polydata)
# else:
#     mappergeo.SetInputData(polydata)
#     # mappergeo2.SetInputConnection(contour.GetOutputPort())

# actor = vtk.vtkActor()
# actor.SetMapper(mappergeo)

# actor2 = vtk.vtkActor()
# actor2.SetMapper(mappergeo2)
glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputConnection(glyph.GetOutputPort())
glyphMapper.SetScalarModeToUsePointFieldData()
glyphMapper.SetColorModeToMapScalars()
glyphMapper.ScalarVisibilityOn()
glyphMapper.SelectColorArray('scalar')
# Colour by scalars.
# scalarRange = polydata.GetScalerRange()
# glyphMapper.SetScalarRange(scalarRange)

glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)

renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

WIDTH = 640
HEIGHT = 480
renderWindow.SetSize(WIDTH, HEIGHT)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.SetBackground(.9, .9, .9)

# renderer.AddActor(actor)
renderer.AddActor(glyphActor)

renderWindow.Render()
renderWindowInteractor.Start()
