"""
helped by:
https://www.geeksforgeeks.org/function-annotations-python/
https://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function
"""
import doctest

def foo(x:int, y, z:float):
    return x*y*z

def safe_call(func, *args, **kwargs):
    """
    >>> safe_call(foo, x=3,y=3.0,z=3.0)
    27.0
    >>> safe_call(foo, x=3,y=3,z="3")
    Traceback (most recent call last):
    ...
    TypeError: safe_call failed, the arguments don't fit.
    >>> safe_call(foo, x=3.3,y=3.0,z=3)
    Traceback (most recent call last):
    ...
    TypeError: safe_call failed, the arguments don't fit.
    >>> safe_call(foo, x=1,y="3.0",z=3.0)
    Traceback (most recent call last):
    ...
    TypeError: can't multiply sequence by non-int of type 'float'
    >>> safe_call(foo, 3)
    Traceback (most recent call last):
    ...
    TypeError: foo() missing 2 required positional arguments: 'y' and 'z'
    >>> safe_call(foo, x=3,y=3.0,z=3.3,w=3)
    Traceback (most recent call last):
    ...
    TypeError: foo() got an unexpected keyword argument 'w'
    """
    # Check if the function has variable names and variable types
    annotations = func.__annotations__
    # Check if the given arguments (*args **kwargs) fit the function annotations.
    for i in range(len(args)):
        if args[i] in annotations and not isinstance(args[i], annotations[args[i]]):
                raise TypeError("safe_call failed, the arguments don't fit.")
    for i in kwargs:
        if i in annotations and not isinstance(kwargs[i], annotations[i]):
                raise TypeError("safe_call failed, the arguments don't fit.")
    # If it all fits call the function.
    return func(*args, **kwargs)

doctest.testmod()