class ApiException(Exception): pass

class WrongArguments(ApiException):
    def __init__(self, message=None,*arg, **kwarg):
        if message:
            self.message = message
        else:
            self.message = u'Wrong arguments'
