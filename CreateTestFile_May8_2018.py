import numpy as np
import cuviewer
import WriteGLFile as w
import random

def write_points_scene(fid):
    w.WriteSceneBegin(fid, '100 Points')
    w.WriteGLTag(fid, cuviewer.MULTIPLE_SPOINT)
    w.WriteGLTag(fid, cuviewer.SFILL)

    for x in range(100):
        p1 = [random.uniform(+10, +5), random.uniform(10, 5),  random.uniform(10, 5)]
        c1 = [1, 0, 0]
        w.Write_GL_points_position(fid, p1)
        w.Write_GL_points_color(fid, c1)

    w.WriteSceneEnd(fid)
    
def write_lines_scene(fid):
    
    w.WriteSceneBegin(fid, '100 lines')
    w.WriteGLTag(fid,cuviewer.MULTIPLE_SLINE)
    
    # We dont want transparent and we want multi color
    trans = 0.0
    multi = 1
    
    flags = cuviewer.SOUTLINE
    if trans != 0.0:
        flags = bytes([flags[0] | cuviewer.STRANSPARENT[0]])
    if multi:
        flags = bytes([flags[0] | cuviewer.SMULTICOLOR[0]])

    w.WriteGLTag(fid, flags)
    
    for x in range(100):
        p1 = [0, 0, 0]
        p2 = [random.randint(1,5), random.randint(1,5), random.randint(1,5)]
        c1 = [0, 0, 1]
        c2 = [1, 0, 0]
        w.write_GL_lines_position(fid, p1, p2)
        w.write_GL_lines_color(fid, c1, c2, flags)
        
    w.WriteSceneEnd(fid)

def write_triangles_scene(fid):
    w.WriteSceneBegin(fid, '100 triangles')
    w.WriteGLTag(fid,cuviewer.MULTIPLE_STRIA)
    
    # We dont want transparent and we want multi color
    trans = 0.0
    multi = 1
    out = 1
    
    # Set the flags
    flags = cuviewer.SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | cuviewer.STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | cuviewer.SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | cuviewer.SOUTLINE[0]])
    
    w.WriteGLTag(fid, flags)
    
    for x in range(100):
        p1 = [20, 20, 20]
        p2 = [random.randint(5,10), random.randint(5,10), random.randint(5,10)]
        p3 = [random.randint(10,15), random.randint(10,15), random.randint(10,15)]
        c1 = [0, 0, 1]
        c2 = [1, 0, 0]
        c3 = [1, 0, 0]
        w.write_GL_triangles_position(fid, p1, p2, p3)
        w.write_GL_triangles_color(fid, c1, c2, c3, flags)
        
    w.WriteSceneEnd(fid)
    
def write_quads_scene(fid):
    w.WriteSceneBegin(fid, '100 quads')
    w.WriteGLTag(fid,cuviewer.MULTIPLE_SQUADRI)
    
    #We dont want transparent and we want multi color
    trans = 0.0
    multi = 1
    out = 1
    
    flags = cuviewer.SFILL
    if trans != 0.0:
        flags =  bytes([flags[0] | cuviewer.STRANSPARENT[0]])
    if multi:
        flags =  bytes([flags[0] | cuviewer.SMULTICOLOR[0]])
    if out:
        flags =  bytes([flags[0] | cuviewer.SOUTLINE[0]])

    w.WriteGLTag(fid, flags)
    
    for x in range(100):
        p1 = [random.randint(40,50), random.randint(40,50), 45]
        p2 = [random.randint(40,50), 45, random.randint(40,50)]
        p3 = [45, random.randint(40,50), random.randint(40,50)]
        p4 = [random.randint(50,60), random.randint(50,60), random.randint(50,60)]

        c1 = [1, 0, 0]
        c2 = [0, 1, 0]
        c3 = [1, 0, 0]
        c4 = [1, 1, 0]
	
        w.write_GL_quad_position(fid, p1, p2, p3, p4)
        w.write_GL_quad_color(fid, c1, c2, c3, c4, flags)
        
    w.WriteSceneEnd(fid)

def write_spheres_scene(fid):
    w.WriteSceneBegin(fid, '10 Spheres')

    for x in range(10):
        p1 = [random.uniform(-10, -5), random.uniform(-10, -5),  random.uniform(-10, -5)]
        c1 = [1, 0, 0]
        r1 = [random.uniform(0, 5)]
        w.Write_GL_sphere(fid, p1, r1, c1, 0.0)

    w.WriteSceneEnd(fid)
    
def write_spheroid_scene(fid):
    w.WriteSceneBegin(fid, '2 Spheroid')

    for x in range(10):
        p1 = [random.uniform(10, 50), random.uniform(10, 50),  random.uniform(10, 50)]
        c1 = [1, 0, 0]
        r1 = [random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3)]
        w.Write_GL_spheroid(fid, p1, r1, c1, 0.0)

    w.WriteSceneEnd(fid)
    
def visualize(output_file):
    # Read and View
    vtkCuv = cuviewer.CreateVtkCuv()
    vtkCuv.ReadCuvFile(output_file)
    vtkCuv.SetRenderWin()
    vtkCuv.renderWindow.Render()
    vtkCuv.renderWindowInteractor.Start()
    
def main():
    # Create gl file
    output_file = 'Points.gl'
    fid = w.WriteInitGLFile(output_file)
    
    # Write some points in the GL file
    write_points_scene(fid)
    
    # Write some lines in the GL file
    #write_lines_scene(fid)
    
    # Write some triangles
    #write_triangles_scene(fid)
    
    # Write some quads
    #write_quads_scene(fid)
    
    # Write some spheres
    #write_spheres_scene(fid)
    
    # Write some spheroids
    write_spheroid_scene(fid)
    
    #Close tag for GL file
    w.WriteCloseGLFile(fid)
    
    #Visualize the file just written
    visualize(output_file)


if __name__ == '__main__':
	main()
