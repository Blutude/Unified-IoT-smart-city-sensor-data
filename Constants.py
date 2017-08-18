class Constants:

    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[name] = value

    ## All final constant values
    FILE_SIZE_LIMIT = 25000
    URL = ''
    KEY = '' # primary key
    DATABASE_NAME = 'BCRL-TLN-database'
    COLL_NAME = 'BCRL-TLN-collection'
    ADDRESSES = ['192.168.10.50', '192.168.10.51', '192.168.10.52', '192.168.10.53']