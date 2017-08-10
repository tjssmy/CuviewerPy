//
//  util.c
//  meshless
//
//  Created by Tom Smy on 11-07-06.
//  Copyright 2011 Carleton. All rights reserved.
//

#include <stdarg.h>
#include "util.h"


#if defined(VS2010) 
double __imp_hypot(double x, double y) { return sqrt(x*x + y*y);} // this is needed for VS2010
#endif

//void err_msg(int a,char *b, ...)
//{ 
//    va_list args;
//    fprintf(stderr, b,args);
//    exit(a);
//}

void *Malloc( size_t s )
{
	void *result;
//    	int i;
	char *t;
    
	if (s == 0)
		return NULL;
	
	result = malloc( s );
	if (result == NULL)
		err_msg(1,"Malloc: No memory allocated\n");
	
	t = (char*) result;
	
//    	if (FillMemory) 
//    for (i = 0; i < s; i++) t[i]  = 'a';
	
	return result;
}

void Free( void *o )
{
    
	if (o == NULL)
	{
		return;
	}
    
	free( o );
}
FILE * fopen_chk(char temp[1000], char s[2])
{
	FILE *f;
	char* cleanedFileName;
    
	cleanedFileName = cleanStringIfQuoted(temp);
	
	if ((f = fopen(cleanedFileName,s)) == NULL)
	{
		Free(cleanedFileName);
		err_msg(1, "Error: Can not open file %s\n", temp);
	}
    
	Free(cleanedFileName);
	
	return(f);
}

void FreeStrInt(strn_int *s)
{
	Free(s->strn);
	Free(s);
}

void FreeStrDouble(strn_double *s)
{
	Free(s->strn);
	Free(s);
}

void FreeStrnArray(char **arr, int n)
{
	int i;
	if (arr == NULL) return;
	for (i=0; i < n; i++) Free(arr[i]);
}
char* cleanStringIfQuoted (char* string)
{
	if (string != NULL)
	{
		char* tmpString;
		
		if ((string[0] == '\'') || (string[0] == '\"'))
		{
			++string;
			tmpString = strdup(string);
			tmpString[strlen(tmpString)-1] = '\0';
			
			return tmpString;
		}
		return strdup(string);
	}
	else
		return NULL;
}

VECTOR_3D VECTOR_3D_init(double x, double y, double z)
{
    VECTOR_3D D;
    D.x = x;
    D.y = y;
    D.z = z;
    
    return D;
}

TRIPLE_3D TRIPLE_3D_init(int i, int j, int k)
{
    TRIPLE_3D T;
    T.i = i;
    T.j = j;
    T.k = k;
    
    return T;
}


DVECTOR_3D DVECTOR_3D_init(double x, double y, double z)
{
    DVECTOR_3D D;
    D.x = x;
    D.y = y;
    D.z = z;
    
    return D;
}

double DVector3d_dist(DVECTOR_3D p, DVECTOR_3D p2)
{
    double l;
    p.x = p2.x-p.x; 
    p.y = p2.y-p.y; 
    p.z = p2.z-p.z; 
    
    l = sqrt((p.x*p.x + p.y*p.y + p.z*p.z));
    return l;
}

DVECTOR_3D DVector3d_diff(DVECTOR_3D p2, DVECTOR_3D p)
{
    p.x = p2.x-p.x; 
    p.y = p2.y-p.y; 
    p.z = p2.z-p.z; 
    return p;
}

DVECTOR_3D DVector3d_ScMulti(DVECTOR_3D p, double s)
{
    p.x = p.x*s; 
    p.y = p.y*s; 
    p.z = p.z*s; 
    return p;
}

DVECTOR_3D DVector3d_sum(DVECTOR_3D p, DVECTOR_3D p2)
{
    p.x = p2.x+p.x; 
    p.y = p2.y+p.y; 
    p.z = p2.z+p.z; 
    return p;
}

DVECTOR_3D DVector3d_sub(DVECTOR_3D p, DVECTOR_3D p2)
{
    p.x = p.x-p2.x; 
    p.y = p.y-p2.y; 
    p.z = p.z-p2.z; 
    return p;
}

DVECTOR_3D DVector3d_ave(DVECTOR_3D p, DVECTOR_3D p2)
{
    p.x = (p2.x+p.x)*0.5; 
    p.y = (p2.y+p.y)*0.5; 
    p.z = (p2.z+p.z)*0.5; 
    return p;
}


double DVector3d_len(DVECTOR_3D p)
{
    double l;
    l = sqrt((p.x*p.x + p.y*p.y + p.z*p.z));
    return l;
}

int DVector3dEq0(DVECTOR_3D p)
{
    if (p.x == 0 && p.y== 0 && p.z ==0) return 1;
    else return 0;
}

int DVector3dAproxEq(DVECTOR_3D p, DVECTOR_3D p2)
{
    
    if (AproxEqual(p.x, p2.x) && 
        AproxEqual(p.y, p2.y) && 
        AproxEqual(p.z, p2.z)) return 1;
    else return 0;
}


double DotProd3D(DVECTOR_3D p, DVECTOR_3D v)
{
    double dp;
    dp = p.x*v.x + p.y*v.y + p.z*v.z;
    return dp;
}
#define FABS_THRESH 1e-6

int AproxEqual(double a, double b)
{
    if (fabs(a-b) < FABS_THRESH) return TRUE;
    else return FALSE;
}

int AproxEqualTol(double a, double b, double tol)
{
    if (fabs(a-b) < tol) return TRUE;
    else return FALSE;
}

int AproxEqualOrLt(double a, double b)
{
    if (fabs(a-b) < FABS_THRESH || a < b) return TRUE;
    else return FALSE;
}

int AproxEqualOrGt(double a, double b)
{
    if (fabs(a-b) < FABS_THRESH || a > b) return TRUE;
    else return FALSE;
}

