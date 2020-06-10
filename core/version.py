# encoding: utf-8

class FtiVersion:
    MAJOR = 0
    MINOR = 0
    PATCH = 1

    @staticmethod
    def get_version():
        """
        Retrieve a string representing the version of the library.
        :return: String containing the version.
        """
        return "{}.{}.{}".format(FtiVersion.MAJOR, FtiVersion.MINOR, FtiVersion.PATCH)
