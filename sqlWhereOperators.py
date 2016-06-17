class Operators:
    """   SQL comparison operators   """
    Equal          = '='
    NotEqual       = '<>'
    LessThan       = '<'
    LessOrEqual    = '<='
    GreaterThan    = '>'
    GreaterOrEqual = '>='
    Like           = 'LIKE'         # functional for        CONTAINS / STARTS WITH / ENDS WITH
    NotLike        = 'NOT LIKE'     # functional for   NOT  CONTAINS / STARTS WITH / ENDS WITH
    IsNull         = 'IS NULL'
    IsNotNull      = 'IS NOT NULL'
    Between        = 'BETWEEN'

    @classmethod
    def getMemberName(cls, value):
        try:
            # Python 2
            #enums = dict([(k, v) for k, v in cls.__dict__.iteritems() if isinstance(v, int)])
            #return enums.keys()[enums.values().index(value)]

            # Python 3
            enums = dict([(k, v) for k, v in cls.__dict__.items() if v == value])
            return next((v for i, v in enumerate(enums.keys()) if i == 0))
        except:
            return None
