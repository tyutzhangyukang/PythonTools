
#以下代码的输出将是什么？说出你的答案并解释

def extendList(val, list=[]):
    list.append(val)
    return list

list1 = extendList(10)
list2 = extendList(123, [])
list3 = extendList('a')

print("list1 = {0}".format(list1))
print("list1 = {0}".format(list2))
print("list1 = {0}".format(list3))