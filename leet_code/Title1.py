class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        map = {}
        _len = len(nums)
        for i in range(0, _len):
            map[target - nums[i]] = i
        for j in range(0, _len):
            if nums[j] in map.keys() and map[nums[j]] != j:
                return [map[nums[j]], j]

s = Solution()
print(s.twoSum([2,7,11,15],9))
