
class A:
    def __init__(self):
        self.a = 1


class B(A):
    pass

a:str="9"

c=B()

dic:dict[str,A]={}
dic["a"]=c

print(type(dic["a"]))
print(isinstance(dic["a"],B))
if a.isdigit():
    print(1)
else:
    print(2)