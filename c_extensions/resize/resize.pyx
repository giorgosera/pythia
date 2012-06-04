import numpy as np
cimport numpy as np
cimport cython
  
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def resize(term_dict, new, old):
  cdef int length = len(new)
  cdef np.ndarray[double] new_center = np.zeros(length)
  cdef list new_vector = length*['']

  cdef int i = 0
  cdef unicode term
  for i in  range(length) :
    term = new[i]
    if term in old: 
      new_center[i] = term_dict[term][1]
      new_vector[i] = term
    else:
      new_vector[i] = term
  return np.fromiter(new_center, dtype=np.float), new_vector