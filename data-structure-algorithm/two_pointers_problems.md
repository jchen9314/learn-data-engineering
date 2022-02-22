# Two Pointers

## Left-Right Pointers

```py
left = 0
right = len(nums) - 1
```

### [Binary Search Template](https://labuladong.github.io/algo/2/21/61/) (Ordered Array)

- search one element

```py
def problem(nums, target):

    if nums is None or len(nums) == 0:
        return -1

    left = 0
    right = len(nums) - 1
    
    while (left <= right):
        mid = left + (right - left) // 2 # prevent integer overflow (left + right)
        if (nums[mid] == target):
            return mid
        elif (nums[mid] < target):
            left = mid + 1
        elif (nums[mid] > target):
            right = mid - 1
    return -1
```

- search left bound
  - example: `nums = [1,2,2,2,3]` find the first occurrence/index of `target = 2`

```py
def left_bound(nums, target):

    if nums is None or len(nums) == 0:
        return -1

    left = 0
    right = len(nums) - 1

    while (left <= right):
        mid = left + (right - left) // 2
        if (nums[mid] == target):
            right = mid - 1 # shrink the search range -> find the first index
        elif (nums[mid] > target):
            left = mid + 1
        elif (nums[mid] < target):
            right = mid - 1
    
    if (left > len(nums)) or (nums[left] != target): # check if index is out of bound
        return -1
    return left
```

- search right bound

```py
def right_bound(nums, target):

    if nums is None or len(nums) == 0:
        return -1
    
    left, right = 0, len(nums) - 1
    while (left <= right):
        mid = left + (right - left) // 2
        if (nums[mid] == target):
            left = mid + 1
        elif (nums[mid] > target):
            left = mid + 1
        elif nums[mid] < target:
            right = mid - 1
    
    if right < 0 or nums[right] != target:
        return -1
    return right
```

## Reference

1. https://labuladong.github.io/algo/2/21/61/
