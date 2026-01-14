from collections import defaultdict
class TimeMap:

    def __init__(self):
        self.dic = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # if key not in self.dic:
        #     self.dic[key] = []  # Initialize an empty list for the key
        self.dic[key].append([value, timestamp])  # Append value and timestamp
        
        # Print the dictionary after every set operation
        print(self.dic)

    def get(self, key: str, timestamp: int) -> str:
        self.res = ""
        values = self.dic.get(key,[])
        l,r = 0, len(values)-1
        while l<=r:
            m = (l+r)//2
            if values[m][1]<=timestamp:  # 1 is timestamp
                res = values[m][0] #0 is value
                l = m+1

            else:
                r = m-1
        print(self.res)
        return res

# Example usage
ans = TimeMap()
ans.set("foo", "bar", 1)  # Set key "foo" with value "bar" at timestamp 1
ans.set("foo", "baz", 3)  # Set key "foo" with value "baz" at timestamp 3
ans.set("bar", "apple", 2)  # Set key "bar" with value "apple" at timestamp 2
ans.get("foo",1)