# encoding: utf-8

class FtiException(Exception):

    def __init__(self, message):
        """
        Build a FTI specific exception.
        :param message: Details on the exception.
        """
        Exception.__init__(self, message)
