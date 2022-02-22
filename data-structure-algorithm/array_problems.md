# Array LeetCode Problems

## [485. Max Consecutive 1](https://leetcode.com/problems/max-consecutive-ones/) (Easy)

- given: binary array `nums`
- find: find the max count of consecutive 1 in `nums`
- example:
  - input: `nums = [1,1,0,1,1,1]`
  - output: `3`

- note:
  - result is a value, then initialize `result = 0`
  - the count of consecutive ones may change:
    - we need a intermediate variable `count` to store the **current** count value
    - initialize `count = 0` after each update
  - when to update: if the element is 0
    - max value -> use max function `result = max(result, count)` where
      - `result` inside max function is the **previous** max count
      - `count` is the **current** max count

- solution

```py
def soln(nums):
    # boundary condition
    if nums is None or len(nums) == 0:
        return 0
    
    result = 0
    count = 0
    for num in nums:
        if num == 1:
            count += 1
        else:
            result = max(result, count)
            count = 0
    return max(result, count)
```

## [283. Move Zeros](https://leetcode.com/problems/move-zeroes/)(Easy)

- given: an integer array `nums`
- find:
  - move all 0 to the end, and maintain relative order of all non-zeros
  - in-place operation without making a copy of array
- example:
  - input: nums = [0, 1, 0, 3, 12]
  - output: [1, 3, 12, 0, 0]

- note:
  - find and place non-zero element one by one
  - assign 0 to remaining elements

- code

```py
def soln(nums):
    # index that stores a non-zero element
    i = 0

    for num in nums:
        if num != 0:
            nums[i] = num
            i += 1
    for idx in range(i, len(nums)):
        nums[idx] = 0
```

## [27. Remove Element](https://leetcode.com/problems/remove-element/)(Easy)

- given: an integer array `nums` and an integer `val`
- find:
  - remove all occurrences of `val` in-place
  - relative order of the elements may be changed
- example:

  ```md
  - input: nums = [3,2,2,3], val = 3
  - output: 2, nums = [2,2,_,_]
  - explanation: function should return k = 2, with the first two elements of nums being 2.
  ```

- note:
  - **swap element**: place all `val` at the end
    - **two pointers**
      - left pointer (l), right pointer(r)
      - if `nums[l] == val and nums[r] != val` then `nums[l] <-> nums[r]`
    - **termination condition: `l >= r`**
    - **use `while` loop**
  - check the position of `l`
    - if `nums[l] == val`, then return `l`
    - if `nums[l] != val`, then return `l + 1`

- code

```py
def soln(nums, val):
    if nums is None or len(nums) == 0:
        return 0
    
    l, r = 0, len(nums) - 1
    
    while (l < r):
        if nums[l] == val and nums[r] != val:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
        elif nums[l] == val and nums[r] == val:
            r -= 1
        else:
            l += 1
    
    if nums[l] == val:
        return l
    else:
        return l + 1
```
