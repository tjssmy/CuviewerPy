import numpy as np
import cuviewer

# Create gl file

output_file = 'Test.gl'

fid = cuviewer.WriteInitGLFile(output_file)

cuviewer.WriteSceneBegin(fid, '3 lines')

p1 = [0, 0, 0]
p2 = [0, 0, 2]
color = [0, 0, 1]
color2 = [1,0,0]
cuviewer.Write_GL_line(fid, p1, p2, color, color, 0.0, 1)

p1 = [0, 0, 0.0]
p2 = [0, 0.5, 0.0]
cuviewer.Write_GL_line(fid, p1, p2, color, color2, 0.0, 1)

p1 = [0, 0, 0.0]
p2 = [1, 0.0, 0.0]
cuviewer.Write_GL_line(fid, p1, p2, color, color2, 0.0, 1)

cuviewer.WriteSceneEnd(fid)

cuviewer.WriteSceneBegin(fid, 'Quads')
nx = 101
ny = 11

x = np.linspace(0, 1, nx)
y = np.linspace(0, 0.1,ny)

for j in range(0, ny-1):
    for i in range(0, nx-1):
        p1 = [x[i], y[j], 0]
        p2 = [x[i], y[j+1], 0]
        p3 = [x[i+1], y[j+1], 0]
        p4 = [x[i+1], y[j], 0]

        color1 = [x[i],0,1-x[i]]
        color2 = [x[i],0,1-x[i]]
        color3 = [x[i+1],0,1-x[i+1]]
        color4 = [x[i+1],0,1-x[i+1]]

        cuviewer.Write_GL_quad(fid, p1, p2, p3, p4, color1, color2, color3, color4, 0.0, 1, 1)

cuviewer.WriteSceneEnd(fid)

cuviewer.WriteSceneBegin(fid, 'Triangles')
nx = 101
ny = 11

x = np.linspace(0, 1, nx)
y = np.linspace(0, 0.1, ny)

for j in range(0, ny - 1):
    for i in range(0, nx - 1):
        p1 = [x[i], y[j], 1.0]
        p2 = [x[i], y[j + 1], 1.0]
        p3 = [x[i + 1], y[j + 1], 1.0]

        color1 = [x[i],0,1-x[i]]
        color2 = [x[i],0,1-x[i]]
        color3 = [x[i+1],0,1-x[i+1]]

        cuviewer.Write_GL_tri(fid, p1, p2, p3, color1, color2, color3, 0.0, 1, 1)

cuviewer.WriteSceneEnd(fid)

cuviewer.WriteSceneBegin(fid, '')

cuviewer.WriteSceneEnd(fid)

cuviewer.WriteCloseGLFile(fid)

# Read and View

vtkCuv = cuviewer.CreateVtkCuv()
vtkCuv.ReadCuvFile(output_file)
vtkCuv.SetRenderWin()
vtkCuv.renderWindow.Render()
vtkCuv.renderWindowInteractor.Start()

