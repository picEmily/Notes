# [1,1,0,0,1,0,1,1,1,1,0,0] 只有0 1的数组，找到最大的子序列的长度
# 满足1和0的数量一样多
# in this case is 6

def find_subset(input):
    m = {}
    cnt = 0
    result = 0
    for i in range(len(input)):
        if input[i] == 0:
            cnt += 1
        else:
            cnt -= 1
        m[i] = cnt
    # for [1,1,0,0,1,0,1,1,1,1,0,0] it gets [0:1,1:2,2:1,3:0,4:1,5:0,6:1,7:2,8:3,9:4,10:3,11:2]
    # find two number whose diff is 1, the distance will be the answer
    result = find_len(m)
    return result

def find_len(m):
    result = 0
    for ele in m:
        for abs(1-m[ele]) in m.values():
            if 

        


if name == "__main__":
    input = [1,1,0,0,1,0,1]
    result = find_subset(input)
    return result