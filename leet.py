class Solution(object):
    def minimumLength(self, s):
        """
        :type s: str
        :rtype: int
        """
        if s[0] != s[len(s)-1]:
            return len(s)
        return len(self.rec(self, s))

    def rec(self, s):
        begin = 0
        last = len(s)

        tbegin = 0
        tlast = len(s)

        if len(s) == 0:
            return ""

        if s[0] != s[len(s)-1]:
            return s
        last_char = s[0]

        for i in range(len(s)):
            if s[i] == last_char:
                begin += 1
            else:
                break
        for i in range(len(s) - 1, 0, -1):
            if s[i] == last_char:
                last -= 1
            else:
                break
        if tbegin != begin and tlast != last:
            s = s[begin:last]
            return self.rec(self, s)
        return s


sol = Solution
sol.minimumLength(sol, "cabaabac")
