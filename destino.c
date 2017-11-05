#include <stdlib.h>

#include <stdio.h>
#include <string.h>

#include "header1.h"
#include "header2.h"
#include "header3.h"

  #include "zfsmemv2.h"

void *m_calloc(int len)
{
  return (zfmalloc(len));
}

int zf_free(void *buff)
{
  zffree(buff);
  return 1;
}

void *f_calloc(int n,int sz)
{
  return (m_calloc((int) (n * sz)) );
}

void *zf_realloc(void *buff,int len)
{
  return (zfrealloc(buff,len) );
}
