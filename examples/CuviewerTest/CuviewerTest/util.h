//
//  util.h
//  meshless
//
//  Created by Tom Smy on 11-07-06.
//  Copyright 2011 Carleton. All rights reserved.
//
#if !defined(_util_h_) /* singular inclusion */
#define _util_h_

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
//sd//	start 2012-05-14
//sd//#include <strings.h>


//void err_msg(int a,char *b, ...);

#define err_msg(a,b,...) \
{ { fprintf(stderr, b, ## __VA_ARGS__);exit(a);}}

#define warn_msg(b,...) \
{fprintf(stderr, b, ## __VA_ARGS__)}

#define log_msg(b,...) \
{ { fprintf(stdout, b, ## __VA_ARGS__);}}

#define ZERO_DVECTOR  DVECTOR_3D_init(0,0,0);


#define TRUE 1
#define FALSE 0

typedef struct _OneDVector
{
    int n;
    double *v;
} OneDVector;

typedef struct vector_struct
{
	float x;
	float y;
	float z;
} VECTOR_3D;

typedef struct dvector_struct
{
	double x;
	double y;
	double z;
} DVECTOR_3D;


typedef struct triple_struct
{
	int i;
	int j;
	int k;
} TRIPLE_3D;

typedef struct strn_int
{
	char * strn;
	int in;
} strn_int;

typedef struct strn_double
{
	char * strn;
	double d;
} strn_double;

typedef struct int_double
{
	int i;
	double d;
} int_double;

typedef enum _GGEO_ANGLE {
	GTHETA,GPHI
} GGEO_ANGLE;

typedef enum _GGEO_TYPE {
	// x,y,z first as we use a loop 0 -> 2 to set these.
	GX_Type,GY_Type,GZ_Type,GXY_Type,GXZ_Type,GYZ_Type,GXYZ_Type
} GGEO_TYPE;

void *Malloc( size_t s );
void Free( void *o );
FILE * fopen_chk(char temp[1000], char s[2]);

void FreeStrInt(strn_int *s);
void FreeStrDouble(strn_double *s);
void FreeStrnArray(char **arr, int n);
char* cleanStringIfQuoted (char* string);
double DotProd3D(DVECTOR_3D p, DVECTOR_3D v);
int AproxEqual(double a, double b);
int AproxEqualTol(double a, double b, double tol);

double DVector3d_len(DVECTOR_3D p);
double DVector3d_dist(DVECTOR_3D p, DVECTOR_3D p2);
DVECTOR_3D DVector3d_diff(DVECTOR_3D p, DVECTOR_3D p2);
DVECTOR_3D DVector3d_sum(DVECTOR_3D p, DVECTOR_3D p2);
DVECTOR_3D DVector3d_sub(DVECTOR_3D p, DVECTOR_3D p2);
DVECTOR_3D DVector3d_ave(DVECTOR_3D p, DVECTOR_3D p2);
DVECTOR_3D DVector3d_ScMulti(DVECTOR_3D p, double s);
int DVector3dAproxEq(DVECTOR_3D p, DVECTOR_3D p2);
int DVector3dEq0(DVECTOR_3D p);
int AproxEqualOrLt(double a, double b);
int AproxEqualOrGt(double a, double b);

VECTOR_3D VECTOR_3D_init(double x, double y, double z);
DVECTOR_3D DVECTOR_3D_init(double x, double y, double z);
TRIPLE_3D TRIPLE_3D_init(int i, int j, int k);
#endif