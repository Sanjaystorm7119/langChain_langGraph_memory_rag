# from typing import List
# class Solution:
#     def plusOne(self, digits: List[int]) -> List[int]:
#         if not digits:
#             return [1]
#         for i in range(len(digits)-1,-1,-1):
#             if digits[i] + 1 != 10:
#                 digits[i] += 1
#                 return digits
#             else:
#                 digits[i] = 0
#                 if i == 0 :
#                     return [1]+digits
# ans = Solution()
# res = ans.plusOne([9,9,9])
# print(res)

# Write any import statements here
def getWrongAnswers(N: int, C: str) -> str:
    res = ""
  
  # Write your code here
    for i in range(N):
        res += "A" if C[i] == "B" else "B" if C[i]=="A" else ""
    print(res)

getWrongAnswers(4,"ABAB")