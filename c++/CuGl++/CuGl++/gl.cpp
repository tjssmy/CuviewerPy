//
//  gl.cpp
//  Atarpp
//
//  Created by Tom Smy on 2017-08-12.
//  Copyright © 2017 Tom Smy. All rights reserved.
//

#include <cmath>

#include "gl.hpp"

CuViewer::CuViewer(){}/*!< default constructor should not be used */
CuViewer::CuViewer(string nm /*!< file name to be written*/)
{
    /*! Cuviewer constructor. 
     
     The constructor sets the output file name and opens the file for writing as a binary file. If the opening fails an error message is printed and the exit() is called. Finally InitGlFile is called to initialize the cuviewer output file.
     */
    name = nm;
    file.open(name, ios::out | ios::binary);

    if (!file) err_msg(1, "Can't open gl file: %s\n",name.c_str());
    
    InitGlFile();
}

void CuViewer::WriteTag(unsigned char tag)
{
    file.write((char*)&tag, sizeof(unsigned char));
    
}

void CuViewer::InitGlFile()
{
    unsigned int check;
    
    check = DATA_ORDER_CHECK;
    file.write((char*)&check, sizeof(unsigned int));
    WriteTag(BEGIN_DATA);
    WriteTag(BEGIN_VERSION);
    file.write((char*)&VERSION_STRING, sizeof(unsigned char)*strlen(VERSION_STRING));
    WriteTag(END_VERSION);
}

void CuViewer::CloseGlFile(int pallet,float min, float max,
                           string units)
{

    WriteTag(BEGIN_VIEW);
    
    WriteTag( VPRESET_VIEW);
    WriteTag( 0x00 );
    
    if (pallet)
    {
//        char deg[10];
        float min,max;
        
//        deg = units;
        
        WriteTag(VBIN_PAL_MIN_MAX);
        file.write((char*)&min, sizeof(float));
        file.write((char*)&max, sizeof(float));
        /*	WriteTag(VBIN_PAL_TYPE);
         file.write((char*)&(deg), sizeof(unsignedpp char)); */
    }
    
    
    WriteTag(END_VIEW);
    WriteTag(END_DATA_STAY);
    
    file.close();
}

void CuViewer::gl_point(FVECTOR_3D p1, FVECTOR_3D color, float trans)
{
    unsigned char flags;
    
    WriteTag(SPOINT);
    
    flags =  SFILL;
    WriteTag(flags);
    
    file.write((char*)&p1,sizeof(FVECTOR_3D));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        WriteColor(color);
        if (flags & STRANSPARENT) file.write((char*)&trans,sizeof(float));
    }
    
    
    return;
}

void CuViewer::WriteColor(FVECTOR_3D color /*!< rgb color to be written */)
{
    /*! Writes a color as three floats to the output file. 
     
     The rgb color (FVECTOR_3D) must have values between 0 and 1. If any field is not in this range *gl_red2* is used and a warning issued.
     
     */
    if (color.x < 0 || color.x > 1.0 ||
        color.y < 0 || color.y > 1.0 ||
        color.z < 0 || color.z > 1.0)
    {
        color = gl_red2;
        warn_msg("CuViewer Warning: color ill-defined using red\n");
    }
    
    file.write((char*)&color,sizeof(FVECTOR_3D));
    
}

void CuViewer::gl_text(FVECTOR_3D p1, FVECTOR_3D color, char *st)
{
    
    /* not functioning I think */
    
    unsigned char flags;
    float trans;
    int len;
    
    WriteTag(STEXT);
    
    flags =  SFILL;
    trans=0;
    
    WriteTag(flags);
    file.write((char*)&p1,sizeof(FVECTOR_3D));
    WriteColor(color);
    /*    file.write((char*)&trans,sizeof(float)); */
    len = (int)strlen(st)+1;
    
    file.write((char*)&len,sizeof(int));
    file.write(st,sizeof(unsigned char)*len);
    
    return;
}

void CuViewer::gl_line(FVECTOR_3D p1, FVECTOR_3D p2, FVECTOR_3D color, FVECTOR_3D color2,
             float trans, int multi)
{
    
    unsigned char flags;
    
    WriteTag(SLINE);
    
    flags =  SOUTLINE;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    
    WriteTag(flags);
    file.write((char*)&p1,sizeof(FVECTOR_3D));
    file.write((char*)&p2,sizeof(FVECTOR_3D));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        WriteColor(color);
        if (flags & STRANSPARENT) file.write((char*)&trans,sizeof(float));
        
        if (flags & SMULTICOLOR)
        {
            WriteColor(color2);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
            
        }
    }
    return;
}

void CuViewer::gl_tri(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,
            FVECTOR_3D c1,FVECTOR_3D c2,FVECTOR_3D c3,
            float trans, int multi, int out)
{
    unsigned char flags;
    
    
    WriteTag(STRIA);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    if (out) flags = flags | SOUTLINE;
    
    
    WriteTag(flags);
    file.write((char*)&p1,sizeof(FVECTOR_3D));
    file.write((char*)&p2,sizeof(FVECTOR_3D));
    file.write((char*)&p3,sizeof(FVECTOR_3D));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        file.write((char*)&c1,sizeof(FVECTOR_3D));
        if (flags & STRANSPARENT) file.write((char*)&trans,sizeof(float));
        if (flags & SMULTICOLOR)
        {
            WriteColor(c2);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
            WriteColor(c3);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
        }
    }
    
    return;
}

void CuViewer::gl_vector(FVECTOR_3D p0, FVECTOR_3D v)
{
    WriteTag(SVECTOR);
    
    file.write((char*)&p0,sizeof(FVECTOR_3D));
    file.write((char*)&v,sizeof(FVECTOR_3D));

}
void CuViewer::gl_square(float x1, float y1, float x2, float y2, FVECTOR_3D c)
{
    FVECTOR_3D p1,p2,p3,p4;
    
    p1.x = x1; p1.y = y1; p1.z = 0;
    p2.x = x1; p2.y = y2; p2.z = 0;
    p3.x = x2; p3.y = y2; p3.z = 0;
    p4.x = x2; p4.y = y1; p4.z = 0;
    
    gl_line(p1,p2,c,c,0,0);
    gl_line(p2,p3,c,c,0,0);
    gl_line(p3,p4,c,c,0,0);
    gl_line(p1,p4,c,c,0,0);
}

void CuViewer::gl_circle(FVECTOR_3D p0, FVECTOR_3D ori, FVECTOR_3D c, float rad)
{
    int i;
    double a;
    FVECTOR_3D p,pp;
    pp.z = p0.z; pp.x = p0.x + rad; pp.y = p0.y;
    p.z = p0.z;
    
    for (i =1; i <= 360; i++)
    {
        a = i/360.0*2*M_PI;
        p.x = p0.x + rad*cos(a);
        p.y = p0.y + rad*sin(a);
        
        gl_line(pp,p,c,c,0,0);
        
        pp = p;
    }
    
    //    gl_square(p0.x-rad,p0.y-rad,p0.x+rad,p0.y+rad,c);
}

void CuViewer::gl_quad_frame(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,
                   FVECTOR_3D p4,FVECTOR_3D c)
{
    gl_line(p1,p2,c,c,0,0);
    gl_line(p2,p3,c,c,0,0);
    gl_line(p3,p4,c,c,0,0);
    gl_line(p1,p4,c,c,0,0);
}


void CuViewer::gl_quad(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,FVECTOR_3D p4,
             FVECTOR_3D c1,FVECTOR_3D c2,FVECTOR_3D c3,FVECTOR_3D c4,
             float trans, int multi, int out, int tri)

{
    unsigned char flags;
    
    if (tri)
    {
        gl_tri(p1,p3,p2,c1,c3,c3,trans,multi,out);
        gl_tri(p3,p4,p1,c3,c4,c1,trans,multi,out);
        return;
    }
    
    WriteTag(SQUADRI);
    
    if (trans == 1.0) flags =  !SFILL;
    else flags = SFILL;
    
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    if (out) flags = flags | SOUTLINE;
    
    
    WriteTag(flags);
    file.write((char*)&p1,sizeof(FVECTOR_3D));
    file.write((char*)&p2,sizeof(FVECTOR_3D));
    file.write((char*)&p3,sizeof(FVECTOR_3D));
    file.write((char*)&p4,sizeof(FVECTOR_3D));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        WriteColor(c1);
        if (flags & STRANSPARENT) file.write((char*)&trans,sizeof(float));
        if (flags & SMULTICOLOR)
        {
            WriteColor(c2);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
            WriteColor(c3);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
            WriteColor(c4);
            if (flags & STRANSPARENT)
                file.write((char*)&trans,sizeof(float));
        }
    }
    
    /*	if (flags & FNORMALS)
     {
     WriteFloats(fout, 3, "norm1");
     WriteFloats(fout, 3, "norm2");
     WriteFloats(fout, 3, "norm3");
     WriteFloats(fout, 3, "norm4");
     } */
    
    return;
}

void CuViewer::gl_sphere(FVECTOR_3D pos, float radius, FVECTOR_3D color, float trans)
{
    unsigned char flags;
    

    WriteTag(SSPHERE);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    
    WriteTag(flags);
    file.write((char*)&pos,sizeof(FVECTOR_3D));
    file.write((char*)&radius,sizeof(float));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        
        WriteColor(color);
        if (flags & STRANSPARENT)
            file.write((char*)&trans,sizeof(float));
    }
    
    return;
}

void CuViewer::gl_spheriod(FVECTOR_3D pos,  FVECTOR_3D radius,
                 FVECTOR_3D color, float trans,
                 FVECTOR_3D axis, float rot)
{
    unsigned char flags;
    
    WriteTag(SSPHOID);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    
    WriteTag(flags);
    file.write((char*)&pos,sizeof(FVECTOR_3D));
    file.write((char*)&radius,sizeof(FVECTOR_3D));
    file.write((char*)&axis,sizeof(FVECTOR_3D));
    file.write((char*)&rot,sizeof(float));
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
        
        WriteColor(color);
        if (flags & STRANSPARENT) 
            file.write((char*)&trans,sizeof(float));
    }
    
    return;
}

void CuViewer::gl_unit_box()
{
    gl_line(FVECTOR_3D(0,0,0),FVECTOR_3D(1,0,0),
            FVECTOR_3D(0,0,1),  FVECTOR_3D(0,0,1), 0, 0);
    gl_line(FVECTOR_3D(0,0,0),FVECTOR_3D(0,1,0),
            FVECTOR_3D(0,1,0),  FVECTOR_3D(0,1,0), 0, 0);
    gl_line(FVECTOR_3D(0,0,0),FVECTOR_3D(0,0,1), 
            FVECTOR_3D(1,0,0),  FVECTOR_3D(1,0,0), 0, 0);
}

void CuViewer::BeginScene(string label)
{

    WriteTag(BEGIN_SCENE);
    WriteTag(BEGIN_SCENE_LABEL);
    file.write((char*)label.c_str(), sizeof(unsigned char)*strlen(label.c_str()));
    WriteTag(END_SCENE_LABEL);
}

void CuViewer::EndScene()
{
    WriteTag(END_SCENE);
}


DrawParams::DrawParams(bool l, DRAW_TYPE t, float tr){
    links = l;
    type = t;
    trans = tr;
}

DrawParams::DrawParams(bool l, DRAW_TYPE t, float tr, bool internal){
    links = l;
    type = t;
    trans = tr;
    inter = internal;
}

DrawParams::DrawParams(bool l, DRAW_TYPE t, double Tn, double Tx, double Fx, bool vec, double lx){
    links = l;
    type = t;
    Tmin = Tn;
    Tmax = Tx;
    Fmax = Fx;
    vectors = vec;
    maxl = lx;
}

void DrawParams::SetLimits(VECTOR_3D mn,VECTOR_3D mx){
    min = mn;
    max = mx;
}
