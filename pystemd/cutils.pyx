cimport pystemd.dbusc as dbusc


cpdef int setns(int fd, int nstype):
   return dbusc.syscall(dbusc.__NR_setns, fd, nstype)
