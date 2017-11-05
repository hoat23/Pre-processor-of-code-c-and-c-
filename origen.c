#include <stdlib.h>

#include <stdio.h>
#include <string.h>

#include "header1.h"
#include "header2.h"
#include "header3.h"

#ifdef _HOAT_
  #include "zfsmemv2.h"
#endif

void *m_calloc(int len)
{
#ifdef _LB_22_
  return (zfmalloc(len));
#else
  void *ptmp;
  ptmp= malloc(len);
  if (ptmp) memset(ptmp,0,len);
  return ptmp;
#endif
}

int zf_free(void *buff)
{
#ifdef _LB_22_
  zffree(buff);
#else
  if (buff)
    free(buff);
#endif
  return 1;
}

void *f_calloc(int n,int sz)
{
  return (m_calloc((int) (n * sz)) );
}

void *zf_realloc(void *buff,int len)
{
#ifdef _LB_22_
  return (zfrealloc(buff,len) );
#else
  return (realloc(buff,len) );
#endif
}
