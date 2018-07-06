class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: inttony
        """
        max_len = 0
        l = []
        for c in s:
            if c not in l:
                max_len +=1
                l.append(c)

        print(max_len)



s = Solution()
s.lengthOfLongestSubstring("sdfasdflsfsdssd")