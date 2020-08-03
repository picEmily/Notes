import sys
print('Plase input your name: ')
name = sys.stdin.readline()
print('Hello ', name)

# 一行一行的读
import sys
# line1 = sys.stdin.readline()  # 包含换行符"\n"
line1 = sys.stdin.readline().strip('\n')  # 去掉换行符"\n"
line2 = input()  # 不包含换行符"\n"
print(len(line1), len(line2))

# 只读一行
this_line = int(intput().strip())

import sys
try:
    while True:
        print('Please input a number:')
        # 读取一个数字；strip('\n')表示以\n分隔，否则输出是“字符串+\n”的形式
        n = int(sys.stdin.readline().strip('\n')) 

        print('Please input some numbers:')
        # 读取以空格为分割的一行数字
        sn = sys.stdin.readline().strip()#若是多输入，strip()默认是以空格分隔，返回一个包含多个字符串的list。
        if sn == '':
            break
        # 如果是一个list数字强制转换成int等类型，可以调用map()函数。
        sn = list(map(int,sn.split())) 
        print(n)
        print(sn,'\n')
except:
    pass


import sys
list1 = []
while True:
    line = sys.stdin.readline()
    if line is '\n':
            break
    a = line.split()
    for i in a:
        list1.append(int(i))
print(list1)

