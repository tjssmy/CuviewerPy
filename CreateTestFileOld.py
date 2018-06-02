import numpy as np
import CuViewer
import WriteGLFile as w
import random

# Create gl file

output_file = 'examples\TestFileOld.gl'

fid = w.WriteInitGLFile(output_file)

w.WriteSceneBegin(fid, '1000 Points')

for x in range(1000):
    p1 = [random.uniform(-10, -5), random.uniform(-10, -5),  random.uniform(-10, -5)]
    c1 = [1, 0, 0]
    w.Write_GL_point(fid, p1, c1, 0.0)

w.WriteSceneEnd(fid)


w.WriteSceneBegin(fid, '1000 lines')

for x in range(1000):
    p1 = [0, 0, 0]
    p2 = [random.randint(1,5), random.randint(1,5), random.randint(1,5)]
    c1 = [0, 0, 1]
    c2 = [1, 0, 0]
    w.Write_GL_line(fid, p1, p2, c1, c2, 0.0, 1)


w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, '1000 Triangles')

for x in range(1000):
    p1 = [20, 20, 20]
    p2 = [random.randint(5,10), random.randint(5,10), random.randint(5,10)]
    p3 = [random.randint(10,15), random.randint(10,15), random.randint(10,15)]
    c1 = [0, 0, 1]
    c2 = [1, 0, 0]
    c3 = [1, 0, 0]
    w.Write_GL_tri(fid, p1, p2, p3, c1, c2, c3, 0.0, 1, 1)


w.WriteSceneEnd(fid)

w.WriteSceneBegin(fid, '1000 Quads')

for x in range(1000):
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

w.WriteCloseGLFile(fid)

# Read and View

vtkCuv = CuViewer.CreateVtkCuv()
vtkCuv.ReadCuvFile(output_file)
vtkCuv.SetRenderWin()
vtkCuv.renderWindow.Render()
vtkCuv.renderWindowInteractor.Start()