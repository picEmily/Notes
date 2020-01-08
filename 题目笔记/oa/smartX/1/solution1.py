class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = None
        self.random = None


class Solution(object):
    """
    deep copy a linkedlist with a random pointer
    """

    def copy_list(self, head):
        if not head:
            return None

        # use a map to store {oldNode : newNode}
        m = {}
        p = head
        while p:
            # copy each node
            m[p] = Node(p.val)
            p = p.next

        p = head
        while p:
            # building pointers between nodes
            if p.next:
                m[p].next = m[p.next]
            if p.random:
                m[p].random = m[p.random]
            p = p.next

        return m[head]


class Linkedlist(object):
    def __init__(self):
        self.n1 = Node(1)
        self.n2 = Node(2)
        self.n3 = Node(3)
        self.n4 = Node(4)
        self.n5 = Node(5)
        self.n1.next = self.n2
        self.n2.next = self.n3
        self.n3.next = self.n4
        self.n4.next = self.n5
        self.n1.random = self.n3
        self.n2.random = self.n4
        self.n3.random = self.n5
        self.n4.random = self.n1


class Tests(object):
    def __init__(self):
        self.ll = Linkedlist()
        self.new_ll = Solution().copy_list(self.ll.n1)

        self.ll.n1.val = 3
        self.ll.n1.next = self.ll.n2.random.next

    def test1(self):
        assert(self.new_ll.random.next.val == 4)

    def test2(self):
        assert(self.new_ll.val == 1)

    def test3(self):
        assert(self.new_ll.next.val == 2)

    def test4(self):
        assert(self.new_ll.random.val == 3)

    def test5(self):
        assert(self.new_ll.next.random.val == 4)


if __name__ == "__main__":
    # test
    print('begin tests')
    t = Tests()
    t.test1()
    t.test2()
    t.test3()
    t.test4()
    t.test5()

    print('pass')