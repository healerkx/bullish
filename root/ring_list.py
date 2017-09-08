
class RingList:
    """
    @param iter
    @param window_size
    针对Iterable items, 可以快速进行Windows Slide的抽象类.
    RingList维护一个环形队列, 当针对items进行forward遍历的时候, 
    只有最新的数据replaced into环形队列的逻辑尾部。而已经处于当前窗口中的数据不需要被重新copy写入,
    例如range(0, 10), 数字下面有---是窗口, window_size=3:
    0123456789
    ---
    而当前环形队列里面维护的数据是0, 1, 2
    当前向遍历的时候:
    逻辑窗口移动到如下位置:
    0123456789
     ---
    而实际环形队列里面维护的数据是3, 1, 2, 其中1和2所在位置并未发生变化, 而逻辑窗口的first变成1, 
    对于实际环形队列来说，改变的有 偏移量, 和数字3的写入。想对消耗比较小

    对于元素3来说, 只是next(iter)操作的返回结果, 
    而没有发生list 根据index进行查找的过程(对于不支持随机遍历的容器来说，是个更快的选择)
    """
    def __init__(self, iter, window_size=10):
        self.__window_size = window_size
        self.__iter = iter
        self.__head = 0
        self.__tail = 0
        self.__items = []

        for i in range(0, window_size):
            self.__items.append(next(iter))
            self.__tail += 1

    def __str__(self):
        return "(%d, %d)" % (self.__head, self.__tail)

    def first(self):
        return self.__items[self.__head]

    def nth(self, n):
        '''
        n is zero based. 
        '''
        return self.__items[(self.__head + n) % self.__window_size]

    def __forward(self):        
        index = self.__tail % self.__window_size
        try:
            self.__items[index] = next(self.__iter)

            self.__head += 1
            self.__head = self.__head % self.__window_size
            
            self.__tail += 1
            self.__tail = self.__tail % self.__window_size
            
            return True
        except:
            return False


    def forward(self, n=1):
        i = 0
        while i < n:
            if self.__forward():
                i += 1
            else:
                break
        return i

    def origin(self):
        return self.__items

    def items(self):
        return self.__items[self.__head:] + self.__items[0: self.__head]


if __name__ == '__main__':
    a = list(range(0, 50))


    l = RingList(iter(a))

    print(l)
    print(l.first())
    print(l.origin())
    print(l.items())

    a = l.forward()
    print(l)
    print(l.nth(0))
    print(a)
    print(l.items())

    a = l.forward(2)
    print(l)
    print(l.nth(0))
    print(a)
    print(l.items())

    a = l.forward(10)
    print(l)
    print(l.nth(0))
    print(a)
    print(l.items())

    s = l.forward(10)
    print(l)
    print(l.nth(0))
    print(s)
    print(l.items())

    s = l.forward(20)
    print(l)
    print(l.nth(0))
    print(s)
    print(l.items())

    s = l.forward(20)
    print(l)
    print(l.nth(0))
    print(s)
    print(l.items())






