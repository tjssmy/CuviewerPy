//
//  gl.hpp
//  Atarpp
//
//  Created by Tom Smy on 2017-08-12.
//  Copyright © 2017 Tom Smy. All rights reserved.
//

#ifndef gl_hpp
#define gl_hpp

#include <stdio.h>
#include <fstream>
#include <string>

#include "Util.hpp"

/* These are the tags used by the Carleton University 3D Viewer 2.0. */

// for bit/byte order
#define DATA_ORDER_CHECK 1351861536
#define DATA_NORMAL_ORDER 1351861536
#define DATA_MIRROR_ORDER 549819216

// for version checking
#define VERSION_STRING "Carleton University 3D Viewer 2.0"
#define SHORT_VERSION_STRING "Carleton University 3D Viewer "

// tags for the sections
#define BEGIN_DATA    0xC0
#define BEGIN_VERSION 0xC4
#define BEGIN_IMG_SET 0xC5
#define BEGIN_MOV_SET 0xC6
#define BEGIN_SCENE   0xC8
#define USER_INTERACT 0xC9
#define BEGIN_VIEW    0xCC
#define RESET_VIEW    0xCD
#define GRAB_IMAGE    0xCE
#define GRAB_FRAME    0xCF

#define BEGIN_SCENE_LABEL 0xD1
#define END_SCENE_LABEL 0xD2

#define END_DATA_STAY 0xA0
#define END_DATA_EXIT 0xA1
#define END_VERSION   0xA4
#define END_IMG_SET   0xA5
#define END_MOV_SET   0xA6
#define END_SCENE     0xA8
#define END_VIEW      0xAC

// tags while in the scene section
#define SPOINT        0x00
#define SLINE         0x01
#define STRIA         0x02
#define SQUADRI       0x03
#define SSPHERE       0x04
#define SSPHOID       0x05
#define STEXT         0x06
#define SVECTOR          0x07

// shape properties in the scene section
#define SFILL         0x01
#define SOUTLINE      0x02
#define SMULTICOLOR   0x04
#define STRANSPARENT  0x08
#define SNORMALS      0x10
#define SMATERIAL     0x20
#define SUNDEFINED    0x40
#define SPROCESSED    0x80

// tags while in the view section
#define VCAM_TRANS    0x00
#define VCAM_ROTATE   0x01
#define VCAM_ORBIT    0x02
#define VOUTLINE_CLR  0x03
#define VPRESET_VIEW  0x04

#define VVIEW_MODE    0x10
#define VFOV          0x11
#define VCLIP_PLANE   0x12
#define VLINE_WIDTH   0x13
#define VSHADING      0x14
#define VBIN_PAL_SEL  0x15
#define VBIN_PAL_MAP  0x16

#define VLIGHTING     0x20
#define VLIGHT        0x21
#define VAMB_LIGHT    0x22
#define VDIFF_LIGHT   0x23
#define VBG_LIGHT     0x24
#define VGAMMA        0x25

#define VWIREFRAME    0x30
#define VOUTLINES     0x31
#define VTWO_SIDED    0x32
#define VTRANSPARENT  0x33
#define VBIN_PAL      0x34
#define VANTIALIAS    0x35

// deprecated for Cuviewer 3.6e
// #define VBIN_PAL_MIN  0x18
// #define VBIN_PAL_MAX  0x19

// #define BEGIN_VBIN_PAL_TYPE 0x39
// #define END_VBIN_PAL_TYPE  0x40

// arguments to the view tags
#define VRELATIVE     0x00
#define VABSOLUTE     0x01

#define VORHTO        0x00
#define VPERSPECTIVE  0x01

#define VFLAT         0x00
#define VSMOOTH       0x01

#define VOFF          0x00
#define VON           0x01
// needed for cuviewer 3.6e
#define VBIN_PAL_MIN_MAX  0x18
#define VBIN_PAL_TYPE     0x19

typedef enum DRAW_TYPE {
    DRAW_MODEL = 0,
    DRAW_BTYPE,
    DRAW_BC,
    DRAW_TEMP,
    DRAW_MINRES,
    DRAW_ONLY_BADLINKS
} DRAW_TYPE;

class DrawParams {
public:
    bool inter = false;
    bool links = false;
    bool fill = true;
    bool smooth = true;
    bool vectors = false;
    bool SplitLayersIntoScenes = false;        

    DRAW_TYPE type = DRAW_MODEL;
    float trans=0;
    VECTOR_3D min = {-numeric_limits<double>::max(),
        -numeric_limits<double>::max(),
        -numeric_limits<double>::max()};
    VECTOR_3D max = {numeric_limits<double>::max(),
        numeric_limits<double>::max(),
        numeric_limits<double>::max()};
    double maxl=-1;
    double Tmin=0,Tmax=0, Fmax=0;
    double minRes,maxRes;
    DrawParams(bool l, DRAW_TYPE t, float tr);
    DrawParams(bool l, DRAW_TYPE t, float tr, bool internal);
    DrawParams(bool l, DRAW_TYPE t, double Tmin, double Tmax, double Fmax, bool vectors, double lx);
    void SetLimits(VECTOR_3D min,VECTOR_3D max);
};



#define gl_white FVECTOR_3D(1,1,1)
#define gl_black FVECTOR_3D(0,0,0)
#define gl_red FVECTOR_3D(1,0,0)
#define gl_blue FVECTOR_3D(0,0,1)
#define gl_orange FVECTOR_3D(1.0,130.0/255,0)
#define gl_green FVECTOR_3D(0,1,0)
#define gl_yellow FVECTOR_3D(1,1,0)
#define gl_magenta FVECTOR_3D(1,0,1)
#define gl_dark_green FVECTOR_3D(0,0.35,0)
#define gl_gray FVECTOR_3D(0.5,0.5,0.5)
#define gl_sky_blue FVECTOR_3D(0.5,0.7,0.8)
#define gl_purple FVECTOR_3D(170.0/255,85.0/255,1.0)
#define gl_darkgray FVECTOR_3D(0.3,0.3,0.3)
#define gl_red1 FVECTOR_3D(0.8,0,0)
#define gl_red2 FVECTOR_3D(0.6,0,0)
#define gl_red3 FVECTOR_3D(0.4,0,0)
#define gl_blue1 FVECTOR_3D(0,0,0.8)
#define gl_blue2 FVECTOR_3D(0,0,0.6)
#define gl_blue3 FVECTOR_3D(0,0,0.4)
#define gl_green1 FVECTOR_3D(0,0.8,0)
#define gl_green2 FVECTOR_3D(0,0.6,0.0)
#define gl_green3 FVECTOR_3D(0,0.4,0.0)
#define gl_yellow1 FVECTOR_3D(1,0.8,0)
#define gl_yellow2 FVECTOR_3D(1,215.0/255.0,0)
#define gl_yellow3 FVECTOR_3D(1,0.4,0.0)
#define gl_magenta1 FVECTOR_3D(0.8,0,1)
#define gl_magenta2 FVECTOR_3D(0.6,0,1)
#define gl_magenta3 FVECTOR_3D(0.4,0,1)
#define gl_lightgray FVECTOR_3D(0.7,0.7,0.7)

#define gl_power_col gl_red2

/*! Cuviewer constructor.
 
 This class is used write CuViewer open "gl" files to be read by CuViewer (QT or python) usually the extension ".gl" is used for these files. It creates a binary file in which 3D entities can be written sorted into scenes that can be displayed independently. The basic procedure it to initialize the gl file (InitGlFile()), start a scene (BeginScene()), write some 3D entities (for example gl_quad()), close the scene (EndScene()), repeat and then close the file (CloseGlFile()).
 */

class CuViewer
{
    ofstream file;
    string name;

public:
    
    CuViewer();
    CuViewer(string nm);
    
    void WriteColor(FVECTOR_3D color);
    void WriteTag(unsigned char tag);
    void gl_point(FVECTOR_3D p1, FVECTOR_3D color, float trans);
    void gl_line(FVECTOR_3D p1, FVECTOR_3D p2, FVECTOR_3D color, FVECTOR_3D color2,
                 float trans, int multi);
    void gl_tri(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,
                FVECTOR_3D c1,FVECTOR_3D c2,FVECTOR_3D c3,
                float trans, int multi, int out);
    void gl_quad(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,FVECTOR_3D p4,
                 FVECTOR_3D c1,FVECTOR_3D c2,FVECTOR_3D c3,FVECTOR_3D c4,
                 float trans, int multi, int out, int tri);
    void gl_quad_frame(FVECTOR_3D p1,FVECTOR_3D p2,FVECTOR_3D p3,
                       FVECTOR_3D p4,FVECTOR_3D c);
    void gl_sphere(FVECTOR_3D pos, float radius, FVECTOR_3D color, float
                   trans);
    void gl_spheriod(FVECTOR_3D pos,  FVECTOR_3D radius,
                     FVECTOR_3D color, float trans,
                     FVECTOR_3D axis, float rot);
    void gl_text(FVECTOR_3D p1, FVECTOR_3D color, char *st);
    void gl_square(float x1, float y1, float x2, float y2, FVECTOR_3D c);
    void gl_circle(FVECTOR_3D p0, FVECTOR_3D ori, FVECTOR_3D c, float rad);
    void gl_vector(FVECTOR_3D p0, FVECTOR_3D v);
    void InitGlFile();
    void CloseGlFile(int pallet,float min, float max,
                     string units);
    void gl_unit_box();
    void BeginScene(string label);
    void EndScene();
    
};

#endif /* gl_hpp */
