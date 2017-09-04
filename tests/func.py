

class A:
    def f(self, a):
        print("A.f(%s)" % str(a))

# Create an object and call member function f()
a = A()
a.f(4)

def check(func):
    def wrapper(*args, **kwargs):
        print("decorated", end=' ')
        func(*args, **kwargs)
    return wrapper

# Dynamically decoration the member functions
A.f = check(A.f)

# Recall the function, this function has been decorated.
a.f(5)

b = A()
b.f(4)

