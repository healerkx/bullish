

class A:
    def f(self, a):
        print("A.f(%s)" % str(a))

def f(a):
    print("f(%s)" % str(a))

# Create an object and call member function f()
a = A()
a.f(4)

def check(func):
    def wrapper(*args, **kwargs):
        print("decorated", end=' ')
        func(*args, **kwargs)
    wrapper.origin_func = func
    return wrapper

# Dynamically decoration the member functions
A.f = check(A.f)

# Recall the function, this function has been decorated.
a.f(5)

f(6)
f = check(f)
f(6)

f = f.origin_func

f(8)

f = check(f)
f(6)


