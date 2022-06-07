def toref(func):
    '''Changes the function/method into a reference to itself.'''
    def wrapper(*args):
        def _wrapper():
            func(*args)
        return _wrapper
    return wrapper