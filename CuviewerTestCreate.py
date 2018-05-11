import numpy as np
import cuviewer
import WriteGLFile as w
import random

# Create gl file

output_file = 'Test.gl'

fid = w.WriteInitGLFile(output_file)

w.WriteSceneBegin(fid, '100000 Points')

for x in range(100000):
    p1 = [random.uniform(-10, -5), random.uniform(-10, -5),  random.uniform(-10, -5)]
    c1 = [1, 0, 0]
    w.Write_GL_point(fid, p1, c1, 0.0);

w.WriteSceneEnd(fid)


w.WriteSceneBegin(fid, '100000 lines')

for x in range(100000):
    p1 = [0, 0, 0]
    p2 = [random.randint(1,5), random.randint(1,5), random.randint(1,5)]
    c1 = [0, 0, 1]
    c2 = [1, 0, 0]
    w.Write_GL_line(fid, p1, p2, c1, c2, 0.0, 1)


w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, '100000 Triangles')

for x in range(100000):
    p1 = [20, 20, 20]
    p2 = [random.randint(5,10), random.randint(5,10), random.randint(5,10)]
    p3 = [random.randint(10,15), random.randint(10,15), random.randint(10,15)]
    c1 = [0, 0, 1]
    c2 = [1, 0, 0]
    c3 = [1, 0, 0]
    w.Write_GL_tri(fid, p1, p2, p3, c1, c2, c3, 0.0, 1, 1)


w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, '100000 Quads')

for x in range(100000):
    p1 = [random.randint(40,50), random.randint(40,50), 45]
    p2 = [random.randint(40,50), 45, random.randint(40,50)]
    p3 = [45, random.randint(40,50), random.randint(40,50)]
    p4 = [random.randint(50,60), random.randint(50,60), random.randint(50,60)]

    c1 = [1, 0, 0]
    c2 = [0, 1, 0]
    c3 = [1, 0, 0]
    c4 = [1, 1, 0]
    w.Write_GL_quad(fid, p1, p2, p3, p4, c1, c2, c3, c4, 0.0, 1, 1)


w.WriteSceneEnd(fid)


'''
w.WriteSceneBegin(fid, '2 Points')


p1 = [0.2, 0.7, 1.1]
color = [1, 0.2, 1]
w.Write_GL_point(fid, p1, color, 0.0);

w.WriteSceneEnd(fid)


w.WriteSceneBegin(fid, 'Quads')
nx = 101
ny = 11

x = np.linspace(0, 1, nx)
y = np.linspace(0, 0.1,ny)


dx = x/nx
dy = y/ny

for j in range(0, ny-1):
    for i in range(0, nx-1):

        # vec = [dx, dy, dx + dx*(i*dx/nx)]
        vec = [0.05, 0.1, 0.1 + i*.01]

        p1 = [x[i], y[j], 0]
        p2 = [x[i], y[j+1], 0]
        p3 = [x[i+1], y[j+1], 0]
        p4 = [x[i+1], y[j], 0]

        color1 = [x[i],0,1-x[i]]
        color2 = [x[i],0,1-x[i]]
        color3 = [x[i+1],0,1-x[i+1]]
        color4 = [x[i+1],0,1-x[i+1]]

        w.Write_GL_quad(fid, p1, p2, p3, p4, color1, color2, color3, color4, 0.0, 1, 1)
        # w.Write_GL_vector(fid,p1,vec)

w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, 'Triangles')
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

        w.Write_GL_tri(fid, p1, p2, p3, color1, color2, color3, 0.0, 1, 1)


w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, '')

w.WriteSceneEnd(fid)
'''
w.WriteCloseGLFile(fid)

# Read and View

vtkCuv = cuviewer.CreateVtkCuv()
vtkCuv.ReadCuvFile(output_file)
vtkCuv.SetRenderWin()
vtkCuv.renderWindow.Render()
vtkCuv.renderWindowInteractor.Start()

