

class RingList:
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
        return self.__items[self.__head + n % self.__window_size]

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






