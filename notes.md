## arrays with python lists
### intro to arrays
```python
from copy import deepcopy
v = [0.5, 0.75, 1.0, 1.5, 2.0]
m = 3 * [deepcopy(v), ] 
# scalar multiplication against a list object, repeats the objects.
v * 2 =  [0.5, 0.75, 1.0, 1.5, 2.0, 0.5, 0.75, 1.0, 1.5, 2.0]
```
```python
import array
# adds some type safety.
# lets us store and restore from files.
a = array.array('f', v)
```
### numpy's ndarray
```python
import numpy as np  
# immutable, single data-type
a = np.array([0, 0.5, 1.0, 1.5, 2.0])  
# indexing works for 1-dimensional ndarray objects
a[:2] # output [0, 0.5]
# mathematical operations are vectorized
a * 2 # output: [0, 1, 2, 3, 4]
a > 1 # output: [false, false, false, true, true]
# predicates can be used for indexing
a[a > 1] # output: [1.5, 2.0]
# universal function from the numPy library 
# are only optimized for numPy objects.
# use math library for other types like floats
np.sqrt(a) # good
math.sqrt(a) # bad
math.sqrt(2.5) # good
np.sqrt(2.5) # bad

b = np.array([a, a * 2])
b.sum(axis=0) # calculates the sum column-wise
b.sum(axis=1) # calculates the sum row-wise

# creates a clone like the ndarray object
# the order specifies how to store data,
# C = column-wise
d = np.zeros_like(ndarray, dtype='f16', order='C')

# metainformation
d.size
d.itemsize # bytes of each item
d.ndim
d.dtype
```
#### reshaping and resizing
```python
# Reshaping does not modify the number of elements
g = np.arange(15)
np.shape(g) # (15,)
h = np.reshape(g, (3,5))
np.shape(g) # (15,) wont modify original ndarray
h.T # the transpose
# resizing increases or decrease the size
np.resize(h, (1,3)) # output: array([[0, 1, 2]])
# stacking only works if the dimensions 
# are the same for the selected axis
np.hstack(h, h * 2)
np.vstack(h, h * 2)
# good ol' fashion flatten.
h.flatten()
# memory layout matters, these decide which axis
# takes up continguous space in memory.
# C order is faster for general summation, and usmmation over rows when axis=0.
# F order is faster for summation over columns when axis=1
h.flatten(order='C') # row-by-row flatten
h.flatten(order='F') # column-by-column flatten

```
#### Structured Arrays
```python
# initialize the column name, and data type.
dt = np.dtype([('name', 'S10'), ('age', 'i4')])
# initialize the array, very sql-like
s = np.array([('smith', 45), ('miguel','26')], dtype=dt)
# access by column
s['name'] # output: array([b'smith', b'miguel'], dtype='|S10')
s[1]['age'] # select a row, and it's field.
```

#### Basic Vectorization
```python
np.random.seed(100)
r = np.arange(12).reshape((4, 3))
s = np.arange(0, 12, 4) # (start, end, interval)
```

## Pandas
### Dataframe class
- designed to efficiently handle data characterized by columnar organization
### Seriess class