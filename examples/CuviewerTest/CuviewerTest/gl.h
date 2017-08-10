#if !defined(_gl_h_)
#define _gl_h_
#include "tags.h"
//sd// start 2012-05-14
//sd//#include "util.h"
#include "util.h"
//sd// end 2012-05-14

extern FILE *glfile,*vrlmfile;
extern int vrml;

void WriteTag(unsigned char tag);
void gl_point(VECTOR_3D p1, VECTOR_3D color, float trans);
void gl_line(VECTOR_3D p1, VECTOR_3D p2, VECTOR_3D color, VECTOR_3D color2, 
	     float trans, int multi);
void gl_tri(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,
	    VECTOR_3D c1,VECTOR_3D c2,VECTOR_3D c3, 
	    float trans, int multi, int out);
void gl_quad(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,VECTOR_3D p4,
	     VECTOR_3D c1,VECTOR_3D c2,VECTOR_3D c3,VECTOR_3D c4, 
	     float trans, int multi, int out);
void gl_quad_frame(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,
		   VECTOR_3D p4,VECTOR_3D c);
void gl_sphere(VECTOR_3D pos, float radius, VECTOR_3D color, float
	       trans);
void gl_spheriod(VECTOR_3D pos,  VECTOR_3D radius, 
		 VECTOR_3D color, float trans, 
		 VECTOR_3D axis, float rot);
void gl_text(VECTOR_3D p1, VECTOR_3D color, char *st);
void gl_square(float x1, float y1, float x2, float y2, VECTOR_3D c);
void gl_circle(VECTOR_3D p0, VECTOR_3D ori, VECTOR_3D c, float rad);
void gl_3D_solid(VECTOR_3D Pos, VECTOR_3D Del, VECTOR_3D col, float trans, int multi, int out);
void gl_3D_CBox(VECTOR_3D Pos, double Del, VECTOR_3D col, float trans, int multi, int out);

void InitGlFile(char file[100]);
void CloseGlFile(int pallet,float min, float max, 
		 char units[10]);
void gl_unit_box();
void BeginScene();
void EndScene();

void gl_arrow(VECTOR_3D p1, VECTOR_3D p2, VECTOR_3D color, VECTOR_3D color2, 
              float trans, int multi);
void gl_box_frame(VECTOR_3D c1,VECTOR_3D d,VECTOR_3D c);
#endif









