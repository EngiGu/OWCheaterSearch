class StatusType(type):
    def __contains__(cls, item):
        return item in cls.keys or item in cls.values

    @property
    def keys(cls):
        return [k for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def values(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def items(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('__')}


class UrlStatus(metaclass=StatusType):
    default = 0
    execed = 1  # 执行过


if __name__ == '__main__':
    pass
