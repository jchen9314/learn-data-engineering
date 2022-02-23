# General Notes

- basic storage: chain, order
- basic operation: add, delete, search, modify
- traversal mode: iteration, recursion

## Basic Data Structures

### Array

- sequencial and contiguous storage, data with identical data type is stored in an array

- operations

  - access: O(1): access __element__ based on __index__
    - because it uses base address of the array (memory address of 1st element) + index of the element * num of bytes for each element
  - search: O(N)
  - insert/delete: O(N)
    - insert: if the space is not enough, it needs to reallocate a larger spacce, then __copy all the data__
    - delete: if deleting an element in the middle of an array, we need move all the data behind each time to maintain the continuity

- operations implemented in python

```python
# 1. create
arr = []

# 2. add element: O(1) if it has enough space, otherwise O(N)
arr.append(1)
arr.insert(1, 666) # insert(index, element)

# 3. access element: O(1)
arr[1]

# 4. update element: O(1)
arr[1] = 2

# 5. remove element: O(N)
arr.remove(2) # remove(element), return None
arr.pop() # pop(index), by default pop out the last element (O(1) if pop()), return the element that is deleted

# 6. get the length
len(arr)

# 7. iterate arrary: O(N)
for index, element in enumerate(arr):
    print(index, element)

# 8. find element: O(N)
arr.index(666)

# 9. sort array: O(NlogN)
arr.sort() # inplace operation, doesn't assign a variable
```

### Linked List

- chained storage, not continuous
- needs pointer points to the next element
  - easy to delete or insert an element: O(1)

- operations

  - access: O(N)
  - search: O(N)
  - insert/delete: O(1)

- operations implemented in python
  
```py
# 1. create a linked list
from collections import deque
ll = deque()

# 2. add element
ll.append(1) # O(1)
ll.append(2)
ll.append(3)

# O(N), first search position then insert the value
ll.insert(2, 99)

# 3. access an element
ll[2] # O(N)

# 4. search an element
ll.index(99) # O(N)

# 5. update an element
ll[2] = 88 # O(N)

# 6. delete an element: O(N)
ll.remove(88) 
del ll[2]

# 7. length
len(ll) # O(1)
```

## Reference

1. https://github.com/labuladong/fucking-algorithm/blob/english/think_like_computer/Framework%20and%20thoughts%20about%20learning%20data%20structure%20and%20algorithm.md
2. https://www.youtube.com/watch?v=l7jCybGk1WA&list=PLVCBLinWsHYyYvQlZNAAy81s9z_OezZvl&ab_channel=%E7%88%B1%E5%AD%A6%E4%B9%A0%E7%9A%84%E9%A5%B2%E5%85%BB%E5%91%98