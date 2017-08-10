//sd// start 2012-05-14
//sd//#include <unistd.h>
//sd// end 2012-05-14
#include <signal.h>
#include <string.h>
//sd// start 2012-05-14
//sd//#include <strings.h>
//sd// end 2012-05-14
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include "gl.h"
#include "util.h"

FILE *glfile,*vrmlfile;
int vrml=0;

void WriteTag(unsigned char tag)
{ 
    fwrite(&tag, sizeof(unsigned char),1,glfile);
}

void InitGlFile(char file[100])
{
    unsigned int check;
    
    glfile = fopen(file,"w");
    if (vrml) 
    {
		char temp[100];
		sprintf(temp,"%s.txt_wrl",file);
		vrmlfile = fopen(temp,"w");
		if (vrmlfile == NULL)
		{
			err_msg(1, "Can't open vrml text file: %s\n",temp);
		}
    }
    
    if (glfile == NULL)
    {
		err_msg(1, "Can't open gl file: %s\n",file);
    }
	
    check = DATA_ORDER_CHECK;
    fwrite(&check, sizeof(unsigned int),1,glfile);
    WriteTag(BEGIN_DATA);
    WriteTag(BEGIN_VERSION);
    fwrite(&VERSION_STRING, sizeof(unsigned char),strlen(VERSION_STRING),
		   glfile);
    WriteTag(END_VERSION);	
}

void CloseGlFile(int pallet,float min, float max, 
				 char units[10])
{
    if (vrml) 
    { 
		fclose(vrmlfile);
    }
	
    WriteTag(BEGIN_VIEW); 
	
    WriteTag( VPRESET_VIEW);
    WriteTag( 0x00 );
    
    if (pallet)
    {
		char deg[10];
		float min,max;
		
		strcpy(deg,units);
		
		WriteTag(VBIN_PAL_MIN_MAX);
		fwrite(&min, sizeof(float),1,glfile);
		fwrite(&max, sizeof(float),1,glfile);
		/*	WriteTag(VBIN_PAL_TYPE);
		 fwrite(&(deg), sizeof(unsignedpp char),1,glfile); */
    } 
	
    
    WriteTag(END_VIEW); 
    WriteTag(END_DATA_STAY); 
	
    fclose(glfile);
}

void gl_point(VECTOR_3D p1, VECTOR_3D color, float trans)
{
    unsigned char flags;
	
    if (vrml)
    {
		fprintf(vrmlfile,"1 %f %f %f %f %f %f\n", 
				p1.x,p1.y,p1.z,color.x,color.y,color.z);
    }
    
	
    WriteTag(SPOINT);
    
    flags =  SFILL;
    WriteTag(flags);
    
    fwrite(&p1,sizeof(VECTOR_3D),1,glfile);
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
		fwrite(&color,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) fwrite(&trans,sizeof(float),1,glfile);
    }
	
    
    return;
}

void gl_text(VECTOR_3D p1, VECTOR_3D color, char *st)
{
	
    /* not functioning I think */
	
    unsigned char flags;
    float trans;
    int len;
    
    WriteTag(STEXT);
    
    flags =  SFILL;
    trans=0;
	
    WriteTag(flags);
    fwrite(&p1,sizeof(VECTOR_3D),1,glfile);
    fwrite(&color,sizeof(VECTOR_3D),1,glfile);
	/*    fwrite(&trans,sizeof(float),1,glfile); */
    len = (int) strlen(st)+1;
    
    fwrite(&len,sizeof(int),1,glfile);
    fwrite(st,sizeof(unsigned char),len,glfile);
    
    return;
}

void gl_line(VECTOR_3D p1, VECTOR_3D p2, VECTOR_3D color, VECTOR_3D color2, 
			 float trans, int multi)
{
    
    unsigned char flags;  
    if (vrml) 
    {
		fprintf(vrmlfile,"2 %f %f %f %f %f %f "
				"%f %f %f %f %f %f\n",
				p1.x,p1.y,p1.z,p2.x,p2.y,p2.z,
				color.x,color.y,color.z,
				color2.x,color2.y,color2.z);
    }
    
    WriteTag(SLINE);
    
    flags =  SOUTLINE;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    
    WriteTag(flags);
    fwrite(&p1,sizeof(VECTOR_3D),1,glfile);
    fwrite(&p2,sizeof(VECTOR_3D),1,glfile);
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {  
		fwrite(&color,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) fwrite(&trans,sizeof(float),1,glfile);
		
		if (flags & SMULTICOLOR)
		{ 
			fwrite(&color2,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
			
		}
    }
    return; 
}

void gl_arrow(VECTOR_3D p1, VECTOR_3D p2, VECTOR_3D color, VECTOR_3D color2, 
			 float trans, int multi)
{
    VECTOR_3D p3;
    double dx,dy,dz;

    dx = (p2.x-p1.x)*.2;
    dy = (p2.y-p1.y)*.2;
    dz = (p2.z-p1.z)*.2;

    p3.x = p2.x - dx;
    p3.y = p2.y - dy;
    p3.z = p2.z - dz;
    
    gl_line(p1,p3,color,color,trans,multi);    
    gl_line(p3,p2,color2,color2,trans,multi);
}



void gl_tri(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,
			VECTOR_3D c1,VECTOR_3D c2,VECTOR_3D c3, 
			float trans, int multi, int out)
{
    unsigned char flags;
    
    if (vrml) 
    {
		fprintf(vrmlfile,"3 %f %f %f %f %f %f %f %f %f "
				"%f %f %f %f %f %f %f %f %f "
				"%f %i\n",
				p1.x,p1.y,p1.z,p2.x,p2.y,p2.z,p3.x,p3.y,p3.z,
				c1.x,c1.y,c1.z,
				c2.x,c2.y,c2.z,
				c3.x,c3.y,c3.z,
				trans,out);
    }
    
    WriteTag(STRIA);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    if (out) flags = flags | SOUTLINE;
	
	
    WriteTag(flags);
    fwrite(&p1,sizeof(VECTOR_3D),1,glfile);
    fwrite(&p2,sizeof(VECTOR_3D),1,glfile);
    fwrite(&p3,sizeof(VECTOR_3D),1,glfile);
	
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
		fwrite(&c1,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) fwrite(&trans,sizeof(float),1,glfile);
		if (flags & SMULTICOLOR)
		{ 
			fwrite(&c2,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
			fwrite(&c3,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
		}
    }
    
	/*	if (flags & FNORMALS)
	 {
	 WriteFloats(fout, 3, "norm1");
	 WriteFloats(fout, 3, "norm2");
	 WriteFloats(fout, 3, "norm3");
	 } */
	
	return;
}    

void gl_square(float x1, float y1, float x2, float y2, VECTOR_3D c)
{
    VECTOR_3D p1,p2,p3,p4;
    
    p1.x = x1; p1.y = y1; p1.z = 0;
    p2.x = x1; p2.y = y2; p2.z = 0;
    p3.x = x2; p3.y = y2; p3.z = 0;
    p4.x = x2; p4.y = y1; p4.z = 0;
	
    gl_line(p1,p2,c,c,0,0);
    gl_line(p2,p3,c,c,0,0);   
    gl_line(p3,p4,c,c,0,0);
    gl_line(p1,p4,c,c,0,0);
}

void gl_circle(VECTOR_3D p0, VECTOR_3D ori, VECTOR_3D c, float rad)
{
    gl_square(p0.x-rad,p0.y-rad,p0.x+rad,p0.y+rad,c);
}

void gl_quad_frame(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,
				   VECTOR_3D p4,VECTOR_3D c)
{
    gl_line(p1,p2,c,c,0,0);
    gl_line(p2,p3,c,c,0,0);   
    gl_line(p3,p4,c,c,0,0);
    gl_line(p1,p4,c,c,0,0);
}

void gl_box_frame(VECTOR_3D c1,VECTOR_3D d,VECTOR_3D c)
{
    VECTOR_3D p1,p2,p3,p4,p5,p6,p7,p8;
    
    d.x = d.x/2.0; d.y = d.y/2.0; d.z = d.z/2.0;
    
    p1.x = c1.x - d.x; p1.y = c1.y - d.y; p1.z = c1.z - d.z;
    p2.x = p1.x;       p2.y = c1.y + d.y; p2.z = p1.z;
    p3.x = c1.x + d.x; p3.y = p2.y;       p3.z = p1.z;
    p4.x = p3.x;       p4.y = c1.y - d.y; p4.z = p1.z;

    p5.x = c1.x - d.x; p5.y = c1.y - d.y; p5.z = c1.z + d.z;
    p6.x = p5.x;       p6.y = c1.y + d.y; p6.z = p5.z;
    p7.x = c1.x + d.x; p7.y = p6.y;       p7.z = p5.z;
    p8.x = p7.x;       p8.y = c1.y - d.y; p8.z = p5.z;

    gl_quad_frame(p1, p2, p3, p4, c);
    gl_quad_frame(p5, p6, p7, p8, c);
    
    gl_line(p1,p5,c,c,0,0);
    gl_line(p2,p6,c,c,0,0);   
    gl_line(p3,p7,c,c,0,0);
    gl_line(p4,p8,c,c,0,0);
}


void gl_quad(VECTOR_3D p1,VECTOR_3D p2,VECTOR_3D p3,VECTOR_3D p4,
			 VECTOR_3D c1,VECTOR_3D c2,VECTOR_3D c3,VECTOR_3D c4, 
			 float trans, int multi, int out)

{
    unsigned char flags;
	
    if (vrml) 
    {
		fprintf(vrmlfile,"4 %f %f %f %f %f %f %f %f %f %f %f %f "
				"%f %f %f %f %f %f %f %f %f %f %f %f "
				"%f %i\n",
				p1.x,p1.y,p1.z,p2.x,p2.y,p2.z,p3.x,p3.y,p3.z,p4.x,p4.y,p4.z,
				c1.x,c1.y,c1.z,
				c2.x,c2.y,c2.z,
				c3.x,c3.y,c3.z,
				c4.x,c4.y,c4.z,trans,out);
    }
    
    WriteTag(SQUADRI);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
    if (multi) flags = flags | SMULTICOLOR;
    if (out) flags = flags | SOUTLINE;
	
	
    WriteTag(flags);
    fwrite(&p1,sizeof(VECTOR_3D),1,glfile);
    fwrite(&p2,sizeof(VECTOR_3D),1,glfile);
    fwrite(&p3,sizeof(VECTOR_3D),1,glfile); 
    fwrite(&p4,sizeof(VECTOR_3D),1,glfile);
	
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
		fwrite(&c1,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) fwrite(&trans,sizeof(float),1,glfile);
		if (flags & SMULTICOLOR)
		{ 
			fwrite(&c2,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
			fwrite(&c3,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
			fwrite(&c4,sizeof(VECTOR_3D),1,glfile);
			if (flags & STRANSPARENT) 
				fwrite(&trans,sizeof(float),1,glfile);
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

void gl_sphere(VECTOR_3D pos, float radius, VECTOR_3D color, float trans)
{
    unsigned char flags;
    
    if (vrml)
    {
		fprintf(vrmlfile,"0 %f %f %f %f %f %f %f\n", 
				pos.x,pos.y,pos.z,radius, color.x,color.y,color.z);
    }
    
    WriteTag(SSPHERE);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
	
    WriteTag(flags);
    fwrite(&pos,sizeof(VECTOR_3D),1,glfile);
    fwrite(&radius,sizeof(float),1,glfile);
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
		
		fwrite(&color,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) 
			fwrite(&trans,sizeof(float),1,glfile);
    }
    
    return;
}

void gl_spheriod(VECTOR_3D pos,  VECTOR_3D radius, 
				 VECTOR_3D color, float trans, 
				 VECTOR_3D axis, float rot)
{
    unsigned char flags;
    
    WriteTag(SSPHOID);
    
    flags =  SFILL;
    if (trans != 0.0) flags = flags | STRANSPARENT;
	
    WriteTag(flags);
    fwrite(&pos,sizeof(VECTOR_3D),1,glfile);
    fwrite(&radius,sizeof(VECTOR_3D),1,glfile);
    fwrite(&axis,sizeof(VECTOR_3D),1,glfile);
    fwrite(&rot,sizeof(float),1,glfile);
    
    if ( (flags & SFILL) || (flags & SOUTLINE) )
    {
		
		fwrite(&color,sizeof(VECTOR_3D),1,glfile);
		if (flags & STRANSPARENT) 
			fwrite(&trans,sizeof(float),1,glfile);
    }
    
    return;
}


void gl_3D_solid(VECTOR_3D Pos, VECTOR_3D Del, VECTOR_3D col, float trans, int multi, int out)
{
    VECTOR_3D p1,p2,p3,p4,p5,p6,p7,p8;
    
    double x,y,z,dx,dy,dz;
    x = Pos.x; y = Pos.y; z = Pos.z;
    dx = Del.x; dy = Del.y; dz = Del.z;
    
    p1 = VECTOR_3D_init(x,y,z);
    p2 = VECTOR_3D_init(x,y+dy,z);
    p3 = VECTOR_3D_init(x,y+dy,z+dz);
    p4 = VECTOR_3D_init(x,y,z+dz);
    
    p5 = VECTOR_3D_init(x+dx,y,z);
    p6 = VECTOR_3D_init(x+dx,y+dy,z);
    p7 = VECTOR_3D_init(x+dx,y+dy,z+dz);
    p8 = VECTOR_3D_init(x+dx,y,z+dz);
    
    gl_quad(p1,p2,p3,p4,col,col,col,col,trans,multi,out);
    gl_quad(p5,p6,p7,p8,col,col,col,col,trans,multi,out);
    gl_quad(p1,p4,p8,p5,col,col,col,col,trans,multi,out);
    gl_quad(p2,p3,p7,p6,col,col,col,col,trans,multi,out);
    gl_quad(p1,p2,p6,p5,col,col,col,col,trans,multi,out);
    gl_quad(p3,p4,p8,p7,col,col,col,col,trans,multi,out);   
}


void gl_3D_CBox(VECTOR_3D Pos, double Del, VECTOR_3D col, float trans, int multi, int out)
{
    VECTOR_3D DDel = VECTOR_3D_init(Del*2,Del*2,Del*2);
    Pos = VECTOR_3D_init(Pos.x - Del,Pos.y - Del,Pos.z - Del);
    gl_3D_solid(Pos,DDel,col,trans,multi, out);
    
}

void gl_unit_box()
{
    gl_line(VECTOR_3D_init(0,0,0),VECTOR_3D_init(1,0,0),
			VECTOR_3D_init(0,0,1),  VECTOR_3D_init(0,0,1), 0, 0);
    gl_line(VECTOR_3D_init(0,0,0),VECTOR_3D_init(0,1,0),
			VECTOR_3D_init(0,1,0),  VECTOR_3D_init(0,1,0), 0, 0);
    gl_line(VECTOR_3D_init(0,0,0),VECTOR_3D_init(0,0,1), 
			VECTOR_3D_init(1,0,0),  VECTOR_3D_init(1,0,0), 0, 0);
}

void BeginScene()
{
    WriteTag(BEGIN_SCENE);
}

void EndScene()
{
    WriteTag(END_SCENE);
}
