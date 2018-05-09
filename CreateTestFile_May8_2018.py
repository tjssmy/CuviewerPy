import numpy as np
import cuviewer
import WriteGLFile as w
import random

def write_points_scene(fid):
    w.WriteSceneBegin(fid, '100000 Points')
    w.WriteGLTag(fid, cuviewer.MULTIPLE_SPOINT)
    w.WriteGLTag(fid, cuviewer.SFILL)

    for x in range(100000):
        p1 = [random.random(), random.random(),  random.random()]
        w.Write_GL_points_position(fid, p1)
        color = [1, 0, 0]
        w.Write_GL_points_color(fid, color)
    
    #for x in range(10000):
        #color = [1, 0, 0]
        #cuviewer.Write_GL_points_color(fid, color)

    w.WriteSceneEnd(fid)
    
def write_lines_scene(fid):
    
    w.WriteSceneBegin(fid, '100000 lines')
    w.WriteGLTag(fid,cuviewer.MULTIPLE_SLINE)
    
    #We dont want transparent and we want multi color
    trans = 0.0
    multi = 1
    
    flags = cuviewer.SOUTLINE
    if trans != 0.0:
        flags = bytes([flags[0] | cuviewer.STRANSPARENT[0]])
    if multi:
        flags = bytes([flags[0] | cuviewer.SMULTICOLOR[0]])

    w.WriteGLTag(fid, flags)
    
    for x in range(100000):
        p1 = [0, 0, 0]
        p2 = [random.randint(1,10), random.randint(1,10), random.randint(1,10)]
        c1 = [0, 0, 1]
        c2 = [1, 0, 0]
        w.write_GL_lines_position(fid, p1, p2)
        w.write_GL_lines_color(fid, c1, c2, flags)
        
    w.WriteSceneEnd(fid)
    
def write_quads_scene(fid):
    w.WriteSceneBegin(fid, '100000 quads')
    w.WriteGLTag(fid,cuviewer.MULTIPLE_SLINE)
    
    #We dont want transparent and we want multi color
    trans = 0.0
    multi = 1
    
    flags = cuviewer.SOUTLINE
    if trans != 0.0:
        flags = bytes([flags[0] | cuviewer.STRANSPARENT[0]])
    if multi:
        flags = bytes([flags[0] | cuviewer.SMULTICOLOR[0]])

    w.WriteGLTag(fid, flags)
    
    for x in range(100000):
        nx = 101
        ny = 11
        
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 0.1,ny)
        
        
        dx = x/nx
        dy = y/ny
        
        for j in range(0, ny-1):
            for i in range(0, nx-1):

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
    write_lines_scene(fid)
    
    #Close tag for GL file
    w.WriteCloseGLFile(fid)
    
    #Visualize the file just written
    visualize(output_file)


if __name__ == '__main__':
	main()
