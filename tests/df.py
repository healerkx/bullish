



class A:
    def f(self, a):
        print(a)

def cached(f):
    def w(r):
        f(r * r)
    return w

a = A()
a.f(5)

a.f = cached(a.f)

a.f(6)