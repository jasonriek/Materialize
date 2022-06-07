def toref(func):
    '''Wraps the function/method into a reference to itself.'''
    def wrapper(*args):
        def _wrapper():
            return func(*args)
        return _wrapper
    return wrapper
