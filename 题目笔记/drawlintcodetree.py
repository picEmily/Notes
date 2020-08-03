#!/usr/bin/python
# -*- coding: utf-8 -*-
def draw(node_list):

    height = 0 
    temp = len(node_list)
    while temp != 0:
        height += 1
        temp = temp//2
        

    level = 0
    while node_list:
        s = ' '*height*height
        for i in range(2**level):
            if node_list:
                s = s + str(node_list.pop(0)) + ' '*height*height
        print(s)
        level += 1
        height -= 1

if __name__ == '__main__':
    draw([99,1,88,1,1,88,7,'#','#','#',91,'#','#','#',6,77,'#','#',5])
    
    
    