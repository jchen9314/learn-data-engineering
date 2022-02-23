# Two Pointers

## Left-Right Pointers

```py
left = 0
right = len(nums) - 1
```

### [Binary Search Template](https://labuladong.github.io/algo/2/21/61/) (Sorted Array, Time: O(logN))

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
    
    if (left >= len(nums)) or (nums[left] != target): # check if index is out of bound
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

### [LC 34. First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) (Medium)

- check left and right bound (use function twice -> add a `bool` parameter)

```py
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        left = self.check_bound(nums, target, left_bound=True)
        right = self.check_bound(nums, target, left_bound=False)
        return [left, right]
        
    def check_bound(self, nums, target, left_bound=True):
        l, r = 0, len(nums) - 1
        i = -1
        while (l <= r):
            mid = l + (r - l) // 2
            if nums[mid] == target:
                i = mid
                if left_bound == True:
                    r = mid - 1
                else:
                    l = mid + 1
            elif nums[mid] < target:
                l = mid + 1
            elif nums[mid] > target:
                r = mid - 1
        
        return i
```





## Reference

1. https://labuladong.github.io/algo/2/21/61/
2. https://www.youtube.com/watch?v=4sQL7R5ySUU&ab_channel=NeetCode
