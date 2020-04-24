
def sum_nums(nums):
    ret = 0
    for value in nums.values():
        if type(value) == int:
          ret += value
    return ret





print(sum_nums({
    "cat": "bob",
    "dog": 23,
    19: 18,
    90: "fish"
  }))
